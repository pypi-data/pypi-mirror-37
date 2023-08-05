# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import copy
import time

from six.moves import queue

from azureml._logging import ChainedIdentity

from .async_task import AsyncTask
from .worker_pool import WorkerPool

DEFAULT_PRIORITY = 1


class TaskQueue(ChainedIdentity):
    """
    A class for managing async tasks
    """

    def __init__(self, worker_pool=None, error_handler=None, **kwargs):
        """
        :param worker_pool: Thread pool for executing tasks
        :type worker_pool: concurrent.futures.ThreadPoolExecutor
        :param error_handler: Extension point for processing error queue items
        :type error_handler: function(error, logging.Logger
        """
        super(TaskQueue, self).__init__(**kwargs)
        self._work_queue = queue.PriorityQueue()
        self._results_queue = queue.Queue()
        # For right now, don't need queue for errors, but it's
        # probable that we'll want the error handler looping on queue thread
        self._error_queue = queue.Queue()
        self._err_handler = error_handler
        self._finished = False
        self._worker_pool = worker_pool if worker_pool is not None else WorkerPool()
        self._task_number = 0

    def __enter__(self):
        self._logger.debug("[Start]")
        return self

    def __exit__(self, *args):
        self._logger.debug("[Stop]")
        self.finish()

    def _generate_task_number(self):
        self._task_number += 1
        return self._task_number

    def add(self, func, *args, **kwargs):
        """
        :param func: Function to be executed asynchronously
        :type func: builtin.function
        :param task_priority: Priority for the task, higher items have higher priority
        :type task_priority: int or None
        """
        task_priority = kwargs.get("task_priority")
        future = self._worker_pool.submit(func, *args, **kwargs)
        ident = "{}_{}".format(self._generate_task_number(), func.__name__)
        task = AsyncTask(future, _ident=ident, _parent_logger=self._logger)
        self.add_task(task, task_priority=task_priority)
        return task

    def add_task(self, async_task, task_priority=None):
        """
        :param async_task: asynchronous task to be added to the queue and possibly processed
        :type async_task: azureml._async.AsyncTask
        :param task_priority: Priority for the task, higher items have higher priority
        :type task_priority: int or None
        """
        '''Blocking, no timeout add task to queue'''
        if self._finished:
            raise AssertionError("Cannot add task to finished queue")
        if not isinstance(async_task, AsyncTask):
            raise ValueError("Can only add AsyncTask, got {0}".format(type(async_task)))

        if task_priority is None:
            task_priority = DEFAULT_PRIORITY
        entry = (task_priority, async_task)
        self._logger.debug("Adding task {0} to queue with task priority {1}".format(async_task.ident(),
                                                                                    task_priority))
        self._work_queue.put(entry)
        self._logger.debug("Queue size is approx. {}".format(self._work_queue.qsize()))

    def flush(self, source=None):
        with self._log_context("WaitFlush"):
            num_messages = self._work_queue.qsize()
            self._work_queue.put((float("inf"), None))
            futures = []
            while not self._work_queue.empty():
                _, future = self._work_queue.get(False)
                self._results_queue.put(future)
                futures.append(future)
            while not all(map(lambda future: future is None or future.done(), futures)):
                time.sleep(.1)

            self._logger.debug("Finished flushing approx. {} messages. Source={}".format(num_messages, source))

    def finish(self):
        '''Flushes queue and waits for all workers to return'''
        if self._finished:
            return
        with self._log_context("WaitFinish"):
            self.flush()
            self._finished = True

    def results(self):
        while not self._results_queue.empty():
                _, task = self._results_queue.get(True)
                if task is None:
                    break
                yield task.wait()
                self._results_queue.task_done()

    def errors(self):
        '''Returns a copy of all exceptions seen in the queue'''
        if not self._finished:
            raise AssertionError("Can't get errors on unfinished TaskQueue")

        errs = copy.deepcopy(self._error_queue.queue)
        return [e for e in errs]
