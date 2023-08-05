# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# Start Temp request solution
import io
import os
import uuid
import logging
import imghdr

from azureml.exceptions import AzureMLException

from azureml._restclient.models.create_run_dto import CreateRunDto

from azureml._restclient.assets_client import AssetsClient
from azureml._restclient.artifacts_client import ArtifactsClient
from azureml._restclient.metrics_client import MetricsClient
from azureml._restclient.run_history_client import RunHistoryClient

from azureml.core.model import Model

STATUS_KEY = "status"
RUN_NAME_DELIM = ">"

module_logger = logging.getLogger(__name__)


class RunClient(object):
    def __init__(self, experiment, run_id, origin, _cluster_url=None):
        """
        :param experiment: The experiment object.
        :type experiment: azureml.core.exepriment.Experiment
        :param run_id:
        :type run_id: str
        :param origin:
        :type origin: str
        :param _cluster_url:
        :type _cluster_url: str
        """
        self._experiment = experiment
        self._origin = origin
        self._run_id = run_id
        self._logger = module_logger.getChild(run_id)  # TODO: chained identity
        # Assets Service has a different host than RunHistoryClients

        self._client = RunHistoryClient.create(experiment.workspace,
                                               experiment.name,
                                               _host=_cluster_url)
        self._cluster = self._client._host

        self.assets_client = AssetsClient.create(self._experiment.workspace,
                                                 host=self._cluster)
        self.artifacts = ArtifactsClient.create(self._experiment.workspace,
                                                host=self._cluster)
        self.metrics = MetricsClient.create(self._experiment.workspace,
                                            self._experiment.name,
                                            host=self._cluster)

    @staticmethod
    def target_name():
        return "sdk"

    @staticmethod
    def create_run(experiment, name=None, run_id=None):
        """

        :param experiment:
        :type experiment: azureml.core.experiment.Experiment
        :param name:
        :param run_id:
        :return:
        """
        client = RunHistoryClient.create(experiment.workspace,
                                         experiment.name)
        run_id = RunClient.create_run_id(run_id)
        if name is None:
            name = "run_{}".format(run_id)
        # TODO what should target be set to?
        # Can target be used to differentiate Run from ExperimentRun
        run_dto = client.create_run(run_id=run_id,
                                    target=RunClient.target_name(),
                                    run_name=name)
        return RunHistoryClient.dto_to_dictionary(run_dto)

    @staticmethod
    def create_run_id(run_id=None):
        return run_id if run_id else str(uuid.uuid4())

    @classmethod
    def chain_names(cls, name, child_name):
        name = name if name else ""
        child_name = child_name if child_name else ""
        return "{}{}{}".format(name, RUN_NAME_DELIM, child_name)

    def get_run(self):
        dto = self._client.get_run(self._run_id)
        return RunHistoryClient.dto_to_dictionary(dto)

    def get_runstatus(self):
        return self._client.get_runstatus(self._run_id)

    def get_status(self):
        run_dto = self._client.get_run(self._run_id)
        return getattr(run_dto, STATUS_KEY)

    def set_tags(self, tags):
        sanitized_tags = self._sanitize_tags(tags)
        create_run_dto = CreateRunDto(run_id=self._run_id, tags=sanitized_tags)
        dto = self._client.patch_run(self._run_id, create_run_dto)
        return RunHistoryClient.dto_to_dictionary(dto)

    def set_tag(self, key, value):
        tags = {key: value}
        return self.set_tags(tags)

    def get_tags(self):
        run_dto = self.get_run()
        return run_dto["tags"]

    def add_properties(self, properties):
        sanitized_props = self._sanitize_tags(properties)
        create_run_dto = CreateRunDto(run_id=self._run_id, properties=sanitized_props)
        dto = self._client.patch_run(self._run_id, create_run_dto)
        return RunHistoryClient.dto_to_dictionary(dto)

    def get_properties(self):
        run_dto = self.get_run()
        return run_dto["properties"]

    def _save_mpl_plot(self, name, plot):
        ext = "png"
        artifact_path = "{}.{}".format(name, ext)
        stream = io.BytesIO()
        try:
            plot.savefig(stream, format=ext)
            stream.seek(0)
            self._upload_image(artifact_path, stream, ext)
        except AttributeError as attribute_error:
            raise AzureMLException("Invalid plot, must be matplotlib.pyplot", inner_exception=attribute_error)
        finally:
            stream.close()
        return artifact_path

    def _save_img_path(self, path):
        image_type = imghdr.what(path)
        if image_type is not None:
            self._upload_image(path, path, image_type)
        else:
            raise AzureMLException("The path provided points to a malformed image file")
        return path

    def _upload_image(self, path, artifact, ext):
        return self.artifacts.upload_artifact(artifact, self._origin, self._run_id, path,
                                              content_type="image/{}".format(ext))

    def log_image(self, name, path=None, plot=None):
        if path is not None and plot is not None:
            raise AzureMLException("Invalid parameters, path and plot were both"
                                   "provided, only one at a time is supported")
        elif path is None and plot is None:
            raise AzureMLException("Invalid parameters, one of path and plot "
                                   "is required as input")
        else:
            artifact_path = (self._save_img_path(path)
                             if path is not None
                             else self._save_mpl_plot(name, plot))
            aml_artifact_uri = "aml://artifactId/{0}".format(artifact_path)
            return self.metrics._log_image(self._run_id, name, aml_artifact_uri)

    @staticmethod
    def get_runs(experiment, **kwargs):
        """
        :param experiment:
        :type experiment: azureml.core.experiment.Experiment
        :return:
        """
        client = RunHistoryClient.create(experiment.workspace,
                                         experiment.name)
        return client.get_runs(**kwargs)

    def get_descendants(self, root_run_id, recursive, **kwargs):
        # Adapter for generator until get_child_runs natively returns a generator of the appropriate
        # subtree
        children = self._client.get_child_runs(self._run_id, root_run_id, recursive=recursive, **kwargs)
        for child in children:
            yield child

    def register_model(self, model_name, model_path=None):
        """
        Register a model with AML
        :param model_name: model name
        :type model_name: str
        :param model_path: relative cloud path to model from outputs/ dir. When model_path is None, model_name is path.
        :type model_path: str
        :rtype: azureml.core.model.Model
        """
        if model_path is None:
            model_path = model_name
        model_path = model_path.rstrip(os.sep)

        artifacts = [{"prefix": "ExperimentRun/{}/{}".format(self._run_id, model_path)}]
        metadata_dict = None
        res = self.assets_client.create_asset(model_name, artifacts,
                                              metadata_dict=metadata_dict,
                                              run_id=self._run_id)
        asset_id = res.json()["id"]
        model = self.register_asset(model_name, asset_id)
        return model

    def register_asset(self, model_name, asset_id):
        return Model._register_with_asset(self._experiment.workspace, model_name, asset_id)

    def create_child_run(self, name, target, child_name=None, run_id=None):
        """
        Creates a child run
        :param name: Name of the current run
        :type name: str:
        :param child_name: Optional name to set for the child run object
        :type child_name: str:
        :param run_id: Optional run_id to set for run, otherwise defaults
        :type run_id: str:
        """
        child_run_id = run_id if run_id else RunClient.create_run_id(run_id)
        child_name = RunClient.chain_names(name, child_name)
        child = self._client.create_child_run(self._run_id,
                                              child_run_id,
                                              target=target,
                                              run_name=child_name)
        return RunHistoryClient.dto_to_dictionary(child)

    def start(self):
        """
        Changes the state of the current run to started
        """
        self._client.post_event_run_start(self._run_id)

    def complete(self):
        """
        Changes the state of the current run to completed
        """
        self._client.post_event_run_completed(self._run_id)

    def fail(self):
        """
        Changes the state of the current run to failed
        """
        self._client.post_event_run_failed(self._run_id)

    def _sanitize_tags(self, tag_or_prop_dict):
        # type: (...) -> {str}
        ret_tags = {}
        # dict comprehension would be nice but logging suffers without more functions
        for key, val in tag_or_prop_dict.items():
            if not isinstance(val, (str, type(None))):  # should be six.str/basestring or something
                self._logger.warn('Converting non-string tag to string: (%s: %s)', key, val)
                ret_tags[key] = str(val)
            else:
                ret_tags[key] = val
        return ret_tags
