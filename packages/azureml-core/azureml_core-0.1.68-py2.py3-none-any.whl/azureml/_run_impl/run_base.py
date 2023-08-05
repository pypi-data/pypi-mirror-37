# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from collections import OrderedDict
import logging
import os

from azureml._run_impl.run_context_manager import RunContextManager
from azureml._restclient.constants import RUN_ORIGIN
from azureml.core._portal import HasRunPortal
from azureml.core._docs import get_docs_url
from azureml._logging import ChainedIdentity
from azureml._html.utilities import to_html, make_link

module_logger = logging.getLogger(__name__)


# TODO: Can we get rid of this class soon? Why does it exist?
class _RunBase(ChainedIdentity, HasRunPortal):
    def __init__(self, experiment, run_id, outputs=None,
                 _run_dto=None, _cluster_url=None, logs=None, **kwargs):
        """
        :param experiment: The experiment.
        :type experiment: azureml.core.experiment.Experiment
        :param run_id: The run id for the run.
        :type run_id: str
        :param outputs: The outputs to be tracked
        :type outputs:
        :param logs: The logs directory to be tracked
        :type logs:
        """

        from azureml._run_impl.run_client import RunClient

        self._experiment = experiment

        self._run_id = run_id

        # We need to do this in order to resolve the history object :(
        # Get rid of just name and pass the objects around BUT
        # TODO: Everything needs to use the *SAME PARAMETER NAMES*
        super(_RunBase, self).__init__(
            experiment=self._experiment,
            run_id=self._run_id,
            ** kwargs)

        self._client = RunClient(self._experiment, self._run_id, RUN_ORIGIN,
                                 _cluster_url=_cluster_url)
        self._run_dto = _run_dto if _run_dto else self._client.get_run()
        self._root_run_id = self._run_dto["root_run_id"]
        self._snapshot_ids = []
        self._outputs = outputs
        self._run_number = _string_to_int(self._run_dto["run_number"], "run number")
        self._run_source = self._run_dto.get("properties", {}).get("azureml.runsource", None)
        self._runtype = self._run_dto.get("run_type", self._run_source)
        self._logger.debug("Constructing run from dto. type: %s, source: %s, props: %s",
                           self._runtype,
                           self._run_source,
                           self._run_dto.get("properties", {}))
        self._context_manager = RunContextManager(self, outputs=outputs, logs=logs,
                                                  _parent_logger=self._logger)

    @classmethod
    def get_docs_url(cls):
        return get_docs_url(cls)

    def _get_base_info_dict(self):
        return OrderedDict([
            ('Experiment', self._experiment.name),
            ('Id', self._run_id),
            ('Type', self._runtype),
            ('Status', self._client.get_status())
        ])

    def __str__(self):
        info = self._get_base_info_dict()
        formatted_info = ',\n'.join(["{}: {}".format(k, v) for k, v in info.items()])
        return "Run({0})".format(formatted_info)

    def __repr__(self):
        return self.__str__()

    def _repr_html_(self):
        info = self._get_base_info_dict()
        info.update([
            ('Details Page', make_link(self.get_portal_url(), "Link to Azure Portal")),
            ('Docs Page', make_link(self.get_docs_url(), "Link to Documentation"))
        ])
        return to_html(info)

    def __enter__(self):
        if self._outputs is not None and not os.path.exists(self._outputs):
            os.mkdir(self._outputs)
        return self._context_manager.__enter__()

    def __exit__(self, exit_type, value, traceback):
        return self._context_manager.__exit__(exit_type, value, traceback)

    def _heartbeat(self):
        self._client._client.post_event_run_heartbeat(self._run_id, 120)


def _string_to_int(value, details):
    try:
        return int(value)
    except ValueError as ve:
        raise ValueError("Could not convert [{0}] to int for {1}: {2}".format(value, details, ve))
