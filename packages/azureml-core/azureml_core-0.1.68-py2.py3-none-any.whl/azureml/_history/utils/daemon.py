# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import os
import threading

from azureml._history.utils.singleton import singleton


class Daemon(object):
    '''
    Utility class for Azure ML run-tracking daemons
    '''

    def __init__(self, ident, interval_sec, logger, work_func):
        self.ident = ident
        self.interval = interval_sec
        self.logger = logger.getChild(ident)
        self.kill = False
        self.current_timer = None
        self.work = work_func
        self.run_count = 0

    def _do_work(self):
        if self.current_timer:
            # Not first call
            self.logger.debug("Triggering do_work on timer {0}".format(self.current_timer.ident))

        # Start timer again before work in case work is expensive
        self._reset_timer(start=True)
        self.work()

    def start(self):
        '''Start a daemon (does work first). Don't call on started daemon'''
        if self.current_timer:
            # self.logger.debug("Called start() on existing Timer")
            raise AssertionError("Called start() on existing Timer")

        self._do_work()

    def stop(self):
        '''Stop a running daemon. Don't call on unstarted daemon'''
        self.kill = True
        self.current_timer.cancel()

    def _reset_timer(self, start=False, interval_sec=None):
        if self.kill:
            self.logger.debug("Instructed to kill daemon. Ignoring timer reset")
            return

        if interval_sec:
            self.interval = interval_sec
        self.logger.debug("Setting timer for {0}s".format(self.interval))
        self.current_timer = threading.Timer(self.interval, self._do_work)
        self.current_timer.setDaemon(True)

        if start:
            self.logger.debug("Starting timer")
            self.current_timer.start()

    def _change_interval(self, new_interval):
        self.current_timer.cancel()
        self.interval = new_interval
        # Creates new timer
        self._do_work()

    def __str__(self):
        return 'Daemon("{0}", {1}s, work: {2})'.format(self.ident, self.interval, self.work)

    def __repr__(self):
        return str(self)


@singleton
class ResourceMonitor(object):
    '''  Tracks resource usage of the program'''

    def __init__(self, ident, logger, children=True, system=False, is_spark=False):
        super().__init__()
        self.logger = logger
        self.original_py_dir = os.getcwd()

        self._logger = logger.getChild(ident)
        pid = os.getpid()
        import psutil
        self._proc = psutil.Process(pid)
        self._track_children = children
        self._track_system = system
        self._spark_context = {'is_spark': is_spark}
        self._logger.debug("Monitoring process {0}. Recursive:{1}, System:{2}".format(
            self._proc, children, system))
        # Flush some of the one-time bad values (e.g. cpu_percent)
        self._get_stats()

        self._daemon = Daemon('rmdaemon', 1, self._logger, self.log_stats)
        self._daemon.start()

    def __enter__(self):
        if self._spark_context['is_spark']:
            from pyspark import SparkContext
            sc = SparkContext.getOrCreate()
            spark_stats = {'spark.version': str(sc._jsc.sc().version()), 'spark.master': str(sc._jsc.sc().master())}

            def _convertMemtoMegs(memory):
                if memory is None:
                    return 1024  # Should read defaults from Spark, but not sure if possible in Python
                if "g" in memory:
                    return int(memory.replace("g", "")) * 1024
                elif "m" in memory:
                    return int(memory.replace("m", ""))
                elif "k" in memory:
                    return float(memory.replace("k", "")) / 1024
                elif "b" in memory:
                    return float(memory.replace("b", "")) / 1024 / 1024
                return int(memory)

            if sc.getConf().get("spark.driver.cores") is None:
                spark_stats['spark.driver.cores (vcore)'] = 1
            else:
                spark_stats['spark.driver.cores (vcore)'] = int(sc.getConf().get("spark.driver.cores"))
            spark_stats['spark.driver.memory (m)'] = _convertMemtoMegs(sc.getConf().get("spark.driver.memory"))
            spark_stats['spark.yarn.driver.memoryOverhead (m)'] = _convertMemtoMegs(
                sc.getConf().get("spark.yarn.driver.memoryOverhead"))

            spark_stats['spark.executor.instances'] = self._get_spark_executors(sc)
            spark_stats['spark.executor.cores (vcore)'] = int(sc.getConf().get("spark.executor.cores"))
            spark_stats['spark.executor.memory (m)'] = _convertMemtoMegs(sc.getConf().get("spark.executor.memory"))
            spark_stats['spark.yarn.executor.memoryOverhead (m)'] = _convertMemtoMegs(
                sc.getConf().get("spark.yarn.executor.memoryOverhead"))
            spark_stats['spark.executor.memory.status'] = self._get_spark_executor_memory_status(sc)

            _spark_nodes, self._spark_context['_spark_start_nodes'] = self._get_spark_nodes(sc)
            spark_stats['spark.nodes'] = self._spark_context['_spark_start_nodes']

            self._logger.info(json.dumps({'spark.start': spark_stats}))

    def _get_spark_stats_running(self):
        if self._spark_context['is_spark']:
            from pyspark import SparkContext
            sc = SparkContext.getOrCreate()

            spark_stats = {'spark.executor.instances': self._get_spark_executors(sc)}
            spark_stats['spark.executor.memory.status'] = self._get_spark_executor_memory_status(sc)
            nodes, spark_stats['spark.nodes'] = self._get_spark_nodes(sc)

            return spark_stats
        else:
            return {}

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._daemon.stop()
        if self._spark_context['is_spark']:
            from pyspark import SparkContext
            sc = SparkContext.getOrCreate()

            spark_stats = {'spark.executor.instances': self._get_spark_executors(sc)}
            _spark_end_nodes_dic, _spark_end_nodes = self._get_spark_nodes(sc)
            spark_stats['spark.nodes'] = _spark_end_nodes
            if self._spark_context['_spark_start_nodes'] != _spark_end_nodes:
                spark_stats['spark.scaling'] = 1
            else:
                spark_stats['spark.scaling'] = 0

            self._logger.info(json.dumps({'spark.end': spark_stats}))
            sc.stop()

    # Not sure the best way to use this Map, so starting with Raw String
    def _get_spark_executor_memory_status(self, sc):
        return str(sc._jsc.sc().getExecutorMemoryStatus())

    def _get_spark_executors(self, sc):
        return sc._jsc.sc().getExecutorMemoryStatus().size()

    def _get_spark_nodes(self, sc):
        s = sc._jsc.sc().getExecutorMemoryStatus().keys()
        import re
        names = re.sub(r'Set\(|\)', '', s).split(', ')

        d = dict()
        for i in names:
            d[i] = d.get(i, 0) + 1
        return d, len(d.keys())

    def _get_system_stats(self):
        import psutil
        return {
            'cpu_percent_percpu': psutil.cpu_percent(percpu=True),
            'virtual_memory': psutil.virtual_memory()._asdict(),
            'disk_io_counters_perdisk': {
                k: v._asdict() for (k, v) in psutil.disk_io_counters(perdisk=True).items()
            },
            'net_io_counters_pernic': {
                k: v._asdict() for k, v in psutil.net_io_counters(pernic=True).items()
            }
        }

    def _get_proc_stats(self, psutil_proc):
        proc_stats = {'parent': psutil_proc.ppid()}
        with psutil_proc.oneshot():
            proc_stats['running'] = psutil_proc.is_running()
            proc_stats['cpu_percent'] = psutil_proc.cpu_percent()
            proc_stats['memory_info'] = psutil_proc.memory_info()._asdict()
        return proc_stats

    def _get_stats(self):
        '''Gets "foo" counter for tracked lineage'''
        procs = [self._proc]
        if self._track_children:
            procs.extend(self._proc.children(recursive=True))

        all_stats = {}
        if self._track_system:
            all_stats['system'] = self._get_system_stats()

        for proc in procs:
            all_stats[str(proc)] = self._get_proc_stats(proc)

        if (self._spark_context['is_spark']):
            all_stats['spark.running'] = self._get_spark_stats_running()

        return {'azureml.profiles.resource': all_stats}

    def log_stats(self):
        '''Logs stats as calculated by _get_stats() to INFO'''
        msg_data = self._get_stats()
        self._logger.info(json.dumps(msg_data))
