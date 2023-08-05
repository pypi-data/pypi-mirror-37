# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" runconfig.py for handling run configurations. """
import os
import collections
import ruamel.yaml
from abc import ABCMeta

from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.compute_target import AbstractComputeTarget
from azureml.core.compute import ComputeTarget
from azureml.core.run import Run

from azureml._base_sdk_common.common import RUNCONFIGURATION_EXTENSION, AML_CONFIG_DIR, COMPUTECONTEXT_EXTENSION, \
    get_project_files, to_camel_case, to_snake_case
from azureml.exceptions import UserErrorException, RunConfigurationException


DEFAULT_MMLSPARK_CPU_IMAGE = "microsoft/mmlspark:0.12"
DEFAULT_MMLSPARK_GPU_IMAGE = "microsoft/mmlspark:gpu-0.12"

DEFAULT_CPU_IMAGE = "mcr.microsoft.com/azureml/base:0.1.4"
DEFAULT_GPU_IMAGE = "mcr.microsoft.com/azureml/base-gpu:0.1.4"

MPI_CPU_IMAGE = DEFAULT_CPU_IMAGE
MPI_GPU_IMAGE = DEFAULT_GPU_IMAGE

LOCAL_RUNCONFIG_NAME = "local"

SUPPORTED_DATAREF_MODES = ["mount", "download", "upload"]

ATTRIBUTES = ['resource_group', '_distributed_backend', 'worker_count', 'snapshot_project', 'packages', 'group',
              'batchai', 'script', 'cpu_cores', 'environment', 'container_instance', 'tensorflow', 'node_count',
              'username', 'python', 'artifact', 'mpi', 'framework', 'yarn_deploy_mode', 'password',
              'path_on_data_store', 'memory_gb', 'target', '_custom_docker_image', 'user_managed_dependencies',
              'conda_dependencies', 'repositories', 'gpu_support', 'mode', 'auto_prepare_environment',
              'environment_variables', 'hdi', 'history', 'enabled', 'output_collection', 'shared_volumes',
              '_loaded_commented_map', 'overwrite', 'process_count_per_node', '_target', 'version', 'arguments',
              'subscription_id', 'base_image', 'parameter_server_count', 'address', 'interpreter_path', 'spark',
              'configuration', 'path_on_compute', 'data_references', 'region', 'data_store_name',
              'max_run_duration_seconds', '_name', 'base_image_registry', 'conda_dependencies_file',
              'precache_packages', 'docker', '_path']
       

class _FieldInfo(object):
    """
    A class for storing the field information.
    """
    def __init__(self, field_type, documentation, list_element_type=None, user_keys=False, serialized_name=None):
        """
        :param field_type: The data type of field.
        :type field_type: object
        :param documentation: The field information
        :type documentation: str
        :param list_element_type: The type of list element.
        :type list_element_type: object
        :param user_keys: user_keys=True, if keys in the value of the field are user keys.
                          user keys are not case normalized.
        :type user_keys: bool
        :param serialized_name:
        :type serialized_name: str
        """
        self._field_type = field_type
        self._documentation = documentation
        self._list_element_type = list_element_type
        self._user_keys = user_keys
        self._serialized_name = serialized_name


    @property
    def field_type(self):
        """
        :return: Returns the field type.
        :rtype: object
        """
        return self._field_type

    @property
    def documentation(self):
        """
        :return: Returns the documentation.
        :rtype: str
        """
        return self._documentation

    @property
    def list_element_type(self):
        """
        :return: Returns the list element type.
        :rtype: object
        """
        return self._list_element_type

    @property
    def user_keys(self):
        """
        :return: Returns the user keys setting.
        :rtype: bool
        """
        return self._user_keys

    @property
    def serialized_name(self):
        """
        :return: Returns the serialized name.
        :rtype: str
        """
        return self._serialized_name


class AbstractRunConfigElement(object):
    """
    An abstract class for run config elements.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """ Constructor for AbstractRunConfigElement """
        # Used for preserving the comments on load() and save()
        self._loaded_commented_map = None

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(AbstractRunConfigElement, self).__setattr__(name, value)
        else:
            raise AttributeError("AbstractRunConfigElement has no attribute %s" % name)


class PythonEnvironment(AbstractRunConfigElement):
    """ A class for managing PythonEnvironment. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("user_managed_dependencies", _FieldInfo(bool, "user_managed_dependencies=True indicates that the environment"
                                                       "will be user managed. False indicates that AzureML will"
                                                       "manage the user environment.")),
        ("interpreter_path", _FieldInfo(str, "The python interpreter path")),
        ("conda_dependencies_file", _FieldInfo(
            str, "Path to the conda dependencies file to use for this run. If a project\n"
                 "contains multiple programs with different sets of dependencies, it may be\n"
                 "convenient to manage those environments with separate files.")),
        ])

    def __init__(self):
        """ Constructor for PythonEnvironment """
        super(PythonEnvironment, self).__init__()

        self.interpreter_path = "python"
        self.user_managed_dependencies = False
        self.conda_dependencies_file = "aml_config/conda_dependencies.yml"
        self.conda_dependencies = None

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(PythonEnvironment, self).__setattr__(name, value)
        else:
            raise AttributeError("PythonEnvironment has no attribute %s" % name)


class AzureContainerRegistry(AbstractRunConfigElement):
    """ A class for managing AzureContainerRegistry. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("address", _FieldInfo(str, "DNS name or IP address of azure container registry(ACR)")),
        ("username", _FieldInfo(str, "The username for ACR")),
        ("password", _FieldInfo(str, "The password for ACR"))
        ])

    def __init__(self):
        """ Constructor for AzureContainerRegistry """
        super(AzureContainerRegistry, self).__init__()
        self.address = None
        self.username = None
        self.password = None

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(AzureContainerRegistry, self).__setattr__(name, value)
        else:
            raise AttributeError("AzureContainerRegistry has no attribute %s" % name)


class DockerEnvironment(AbstractRunConfigElement):
    """ A class for managing DockerEnvironment. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("enabled", _FieldInfo(bool, "Set True to perform this run inside a Docker container.")),
        ("base_image", _FieldInfo(str, "Base image used for Docker-based runs.")),
        ("shared_volumes", _FieldInfo(bool, "Set False if necessary to work around shared volume bugs.")),
        ("gpu_support", _FieldInfo(bool, "Run with NVidia Docker extension to support GPUs.")),
        ("arguments", _FieldInfo(list, "Extra arguments to the Docker run command.", list_element_type=str)),
        ("base_image_registry", _FieldInfo(AzureContainerRegistry, "Image registry that contains the base image.")),
    ])

    def __init__(self):
        """ Constructor for DockerEnvironment """
        super(DockerEnvironment, self).__init__()
        self.enabled = False
        self.gpu_support = False
        self.shared_volumes = True
        self.arguments = list()
        self.base_image = DEFAULT_CPU_IMAGE
        self.base_image_registry = AzureContainerRegistry()

    def __setattr__(self, name, value):
        """
        Method for managing attribute validation
        :param name:
        :type name: str
        :param value:
        :type value: str
        """

        if name in ATTRIBUTES:
            super(DockerEnvironment, self).__setattr__(name, value)
        else:
            raise AttributeError("DockerEnvironment has no attribute %s" % name)


class SparkPackage(AbstractRunConfigElement):
    """ 
    A class for managing SparkPackage. 
    :param group:
    :type group:
    :param artifact:
    :type artifact:
    :param version:
    :type version:
    """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("group", _FieldInfo(str, "")),
        ("artifact", _FieldInfo(str, "")),
        ("version", _FieldInfo(str, ""))
        ])

    def __init__(self, group=None, artifact=None, version=None):
        """ Constructor for SparkPackage """
        super(SparkPackage, self).__init__()
        self.group = group
        self.artifact = artifact
        self.version = version

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(SparkPackage, self).__setattr__(name, value)
        else:
            raise AttributeError("SparkPackage has no attribute %s" % name)


class SparkEnvironment(AbstractRunConfigElement):
    """ A class for managing SparkEnvironment. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("repositories", _FieldInfo(list, "List of spark repositories.", list_element_type=str)),
        ("packages", _FieldInfo(list, "", list_element_type=SparkPackage)),
        ("precache_packages", _FieldInfo(bool, ""))
        ])

    def __init__(self):
        """ Constructor for SparkEnvironment """
        super(SparkEnvironment, self).__init__()
        self.repositories = [
            "https://mmlspark.azureedge.net/maven"]
        self.packages = [
            SparkPackage("com.microsoft.ml.spark", "mmlspark_2.11", "0.12")]
        self.precache_packages = True

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(SparkEnvironment, self).__setattr__(name, value)
        else:
            raise AttributeError("SparkEnvironment has no attribute %s" % name)


class HdiConfiguration(AbstractRunConfigElement):
    """ A class for managing HdiConfiguration. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("yarn_deploy_mode", _FieldInfo(str, "Yarn deploy mode. Options are cluster and client."))
        ])

    def __init__(self):
        """ Constructor for HdiConfiguration """
        super(HdiConfiguration, self).__init__()
        self.yarn_deploy_mode = "cluster"

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(HdiConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("HdiConfiguration has no attribute %s" % name)


class BatchAiConfiguration(AbstractRunConfigElement):
    """ A class for managing BatchAiConfiguration. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("node_count", _FieldInfo(int, "Number of nodes to use for running batchai jobs"))
        ])

    def __init__(self):
        """ Constructor for BatchAiConfiguration """
        super(BatchAiConfiguration, self).__init__()
        self.node_count = 1

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(BatchAiConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("BatchAiConfiguration has no attribute %s" % name)


class TensorflowConfiguration(AbstractRunConfigElement):
    """ A class for managing TensorflowConfiguration. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("worker_count", _FieldInfo(int, "The number of worker tasks.")),
        ("parameter_server_count", _FieldInfo(int, "The number of parameter server tasks."))
        ])

    def __init__(self):
        """ Constructor for TensorflowConfiguration """
        super(TensorflowConfiguration, self).__init__()
        self.worker_count = 1
        self.parameter_server_count = 1

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(TensorflowConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("TensorflowConfiguration has no attribute %s" % name)


class MpiConfiguration(AbstractRunConfigElement):
    """ A class for managing MpiConfiguration. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("process_count_per_node", _FieldInfo(int, "When using MPI, number of processes per node."))
        ])

    def __init__(self):
        """ Constructor for MpiConfiguration """
        super(MpiConfiguration, self).__init__()
        self.process_count_per_node = 1

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(MpiConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("MpiConfiguration has no attribute %s" % name)


class ContainerInstanceConfiguration(AbstractRunConfigElement):
    """ A class for managing ContainerInstanceConfiguration. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("cpu_cores", _FieldInfo(int, "Number of cores to allocate for the container")),
        ("memory_gb", _FieldInfo(int, "Memory to allocate for the container in GB")),
        ("region", _FieldInfo(str, "Azure region for the container; defaults to the same as workspace"))
        ])

    def __init__(self):
        """ Constructor for ContainerInstanceConfiguration """
        super(ContainerInstanceConfiguration, self).__init__()
        self.cpu_cores = 1
        self.memory_gb = 4
        self.region = None
        self.resource_group = None
        self.subscription_id = None

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(ContainerInstanceConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("ContainerInstanceConfiguration has no attribute %s" % name)


class EnvironmentDefinition(AbstractRunConfigElement):
    """
    Configures the python environment where the experiment is executed.

    :var environment_variables: A dictionary of environment variables names and values.
        These environment variables are set on the process where user script is being executed.
    :vartype environment_variables: dict

    :var python: This section specifies which python environment and interpreter to use on the target compute.
    :vartype python: PythonEnvironment

    :var docker: This section configures if and how Docker containers are used by the run.
    :vartype docker: DockerEnvironment

    :var spark: The section configures Spark settings. It is only used when framework is set to PySpark.
    :vartype spark: SparkEnvironment

    """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        # In dict, values are assumed to be str
        ("environment_variables", _FieldInfo(dict, "Environment variables set for the run.", user_keys=True)),
        ("python", _FieldInfo(PythonEnvironment, "Python details")),
        ("docker", _FieldInfo(DockerEnvironment, "Docker details")),
        ("spark", _FieldInfo(SparkEnvironment, "Spark details"))
        ])

    def __init__(self):
        """ Constructor for EnvironmentDefinition """
        super(EnvironmentDefinition, self).__init__()
        self.python = PythonEnvironment()
        self.environment_variables = {"EXAMPLE_ENV_VAR": "EXAMPLE_VALUE"}
        self.docker = DockerEnvironment()
        self.spark = SparkEnvironment()

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(EnvironmentDefinition, self).__setattr__(name, value)
        else:
            raise AttributeError("EnvironmentDefinition has no attribute %s" % name)


class SparkConfiguration(AbstractRunConfigElement):
    """ A class for managing SparkConfiguration. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        # In dict, values are assumed to be str
        ("configuration", _FieldInfo(dict, "")),
        ])

    def __init__(self):
        """ Constructor for SparkConfiguration """
        super(SparkConfiguration, self).__init__()
        self.configuration = {
            "spark.app.name": "Azure ML Experiment",
            "spark.yarn.maxAppAttempts": 1}

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(SparkConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("SparkConfiguration has no attribute %s" % name)


class HistoryConfiguration(AbstractRunConfigElement):
    """ A class for managing HistoryConfiguration. """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("output_collection", _FieldInfo(bool, "Enable history tracking -- this allows status, logs, metrics, and "
                                               "outputs\nto be collected for a run.")),
        ("snapshot_project", _FieldInfo(bool, "whether to take snapshots for history."))
        ])

    def __init__(self):
        """ Constructor for HistoryConfiguration """
        super(HistoryConfiguration, self).__init__()
        self.output_collection = True
        self.snapshot_project = True

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(HistoryConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("HistoryConfiguration has no attribute %s" % name)


class DataReferenceConfiguration(AbstractRunConfigElement):
    """
    A class for managing DataReferenceConfiguration.
    :param datastore_name:
    :type datastore_name: str
    :param mode:
    :type mode: str
    :param path_on_datastore:
    :type path_on_datastore: str
    :param path_on_compute:
    :type path_on_compute: str
    :param overwrite:
    :type overwrite: bool
    """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("data_store_name", _FieldInfo(str, "Name of the datastore.")),
        ("path_on_data_store", _FieldInfo(str, "relative path on the datastore.")),
        ("mode", _FieldInfo(str, "operation on the datastore, mount, download, upload")),
        ("overwrite", _FieldInfo(bool, "whether to overwrite the data if existing")),
        ("path_on_compute", _FieldInfo(str, "the path on the compute target."))
        ])

    def __init__(self, datastore_name=None, mode="mount", path_on_datastore=None, path_on_compute=None,
                 overwrite=False):
        """
        Constructor for DataReferenceConfiguration
        """
        super(DataReferenceConfiguration, self).__init__()
        self.data_store_name = datastore_name
        self.path_on_data_store = path_on_datastore
        self.path_on_compute = path_on_compute
        self.mode = mode.lower()
        self.overwrite = overwrite

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(DataReferenceConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("DataReferenceConfiguration has no attribute %s" % name)

    def _validate(self):
        if not self.data_store_name:
            raise UserErrorException("Missing data store name")
        if not self.mode or (self.mode.lower() not in SUPPORTED_DATAREF_MODES):
            raise UserErrorException("mode {0} is not supported. Only mount, download allowed".format(self.mode))
        self.mode = self.mode.lower()


class RunConfiguration(AbstractRunConfigElement):
    """
    This class works with ::func:`azureml.core.experiment.Experiment.submit` to configure the execution environment for an experiment trial.

    .. remarks:

        The RunConfiguration encapsulates execution environment settings.
        The configuration include:

        *  Bundling the experiment source directory including the submitted script.
        *  Setting the Command line arguments for the submitted script.
        *  Configuring the path for the Python interpreter. 
        *  Obtain Conda configuration for to manage the application dependencies. The job submission process can use the configuration to 
            provision a temp Conda environment and launch the application within. The temp environments are cached and reused in subsequent runs.
        *  Optional usage of Docker and custom base images. 
        *  Optional choice of submitting the experiment to multiple types of Azure compute.
        *  Advanced runtime settings for common runtimes like spark and tensorflow.

        For example users can submit a simple training script on the local machine using this code.
        . code-block: python

                from azureml.core import ScriptRunConfig, RunConfiguration, Experiment
            
                # create or load an experiment 
                experiment = Experiment(workspace, "MyExperiment")
                # run a trial from the train.py code in your current directory
                config = ScriptRunConfig(source_directory='.', script='train.py',
                    run_config=RunConfiguration())
                run = experiment.submit(config)

    :var script: The relative path to the python script file.
        The file path is relative to the source_directory passed to :func:`azureml.core.experiment.Experiment.submit`.
    :vartype script: str

    :var arguments: Command line arguments for the python script file.
    :vartype arguments: str

    :var framework: The supported frameworks are Python and PySpark.
        When running on Azure Batch AI managed clusters TensorFlowParameterServer and PythonMPI can be used for distributed training jobs.
    :vartype framework: str

    :var environment: The environment definition, This field configures the python environment.
        It can be configured to use an existing Python environment or configure to setup a temp environment for the experiment.
        The definition is also responsible for setting the required application dependencies.
    :vartype environment: EnvironmentDefinition

    :var auto_prepare_environment: Defaulted to True, but if set to False the run will fail if
        no environment was found matching the requirements specified.
        User can set this value to False if they prefer to fail fast when the environment is not found in the cache.
    :vartype auto_prepare_environment: bool

    :var max_run_duration_seconds: Maximum allowed time for the run. The system will attempt to automatically cancel the run, if it took longer than this value 
    :vartype max_run_duration_seconds: int

    :var history: This section is used to disable and enable experiment history logging features.
    :vartype history: HistoryConfiguration

    :var spark: When the platform is set to Pyspark,
        The spark configuration is used to set the default sparkconf for the submitted job.
    :vartype spark: SparkConfiguration

    :var hdi: This attribute takes effect only when the target is set to an Azure HDI compute.
        The HDI Configuration is used to set the YARN deployment mode.
        It is defaulted to cluster mode.
    :vartype hdi: HDIConfiguration

    :var batchai: The attribute is used to configure the required node count for job.
        This parameter takes effect only when the target is set to an Azure Batch AI compute.
    :vartype batchai: BatchAIConfiguration

    :var tensorflow: The attribute is used to configure the distributed tensorflow parameters.
        This parameter takes effect only when the framework is set to TensorFlowParameterServer.
        Azure Batch AI is the only supported compute for this configuration.
    :vartype tensorflow: TensorFlowConfiguration`

    :var  mpi: The attribute is used to configure the distributed MPI job parameters.
        This parameter takes effect only when the framework is set to PythonMPI.
        Azure Batch AI is the only supported compute type for this configuration.
    :vartype mpi: MPIConfiguration

    :var container_instance: The attribute is used to configure a new Azure Container Instance for the submitted experiment.
        The configuration enables the user to select an on-demand size and sku.
        The configuration only takes effect when the target is set to "ContainerInstance"
    :vartype container_instance: ContainerInstanceConfiguration

    :var data_references: All the data sources are made available to the run
        during execution based on each configuration.
    :vartype data_references: list[DataReferenceConfiguration]
    """
    # This is used to deserialize.
    # This is also the order for serialization into a file.
    _field_to_info_dict = collections.OrderedDict([
        ("script", _FieldInfo(str, "The script to run.")),
        ("arguments", _FieldInfo(list, "The arguments to the script file.", list_element_type=str)),
        ("_target", _FieldInfo(str, "The name of the compute target to use for this run.", serialized_name="target")),
        ("framework", _FieldInfo(str, "Framework to execute inside. Allowed values are "
                                      "\"Python\" ,  \"PySpark\", \"TensorFlowParameterServer\" and \"PythonMPI\".")),
        ("auto_prepare_environment", _FieldInfo(bool, "Automatically prepare the run environment as part "
                                                      "of the run itself.")),
        ("max_run_duration_seconds", _FieldInfo(int, "Maximum allowed duration for the run.")),
        ("environment", _FieldInfo(EnvironmentDefinition, "Environment details.")),
        ("history", _FieldInfo(HistoryConfiguration, "History details.")),
        ("spark", _FieldInfo(SparkConfiguration, "Spark configuration details.")),
        ("hdi", _FieldInfo(HdiConfiguration, "HDI details.")),
        ("batchai", _FieldInfo(BatchAiConfiguration, "BatchAI details.")),
        ("tensorflow", _FieldInfo(TensorflowConfiguration, "Tensorflow details.")),
        ("mpi", _FieldInfo(MpiConfiguration, "Mpi details.")),
        ("container_instance", _FieldInfo(ContainerInstanceConfiguration, "Container instance details.")),
        ("data_references", _FieldInfo(dict, "data reference configuration details",
                                      list_element_type=DataReferenceConfiguration))
    ])

    def __init__(self, script=None, arguments=None, framework=None,
                 conda_dependencies=None, _history_enabled=None, _path=None, _name=None):
        """
        Initializes a RunConfiguration with the default settings.
        By default the constructor creates a RunConfiguration for a local run.

        :param script: The relative path to the python script file to be invoked.
        :type script: str
        :param arguments: Command line arguments to the script file.
        :type arguments: list[str]
        :param framework: The supported frameworks are Python and PySpark.
            When running on Batch AI managed clusters the value can allow for
            TensorFlowParameterServer and PythonMPI for distributed training job.
        :type framework: str
        :param conda_dependencies: When :attr:`userManagedEnvironment` is false,
            a new conda environment is created with all packages described in the conda_dependencies object. The program is executed in this new environment.
        :type conda_dependencies: CondaDependencies
        :param _history_enabled:
        :type _history_enabled: bool
        :param _path:
        :type _path: str
        :param _name:
        :type _name: str
        """
        super(RunConfiguration, self).__init__()
        if _name:
            RunConfiguration._check_name_validity(_name)

        # Used for saving to local file
        self._name = _name
        self._path = _path

        # Default values
        self.script = script if script else "train.py"
        self.arguments = arguments if arguments else []
        self._target = LOCAL_RUNCONFIG_NAME
        self.framework = framework if framework else "Python"
        self.auto_prepare_environment = True
        self.max_run_duration_seconds = None

        self.environment = EnvironmentDefinition()
        self.history = HistoryConfiguration()
        self.spark = SparkConfiguration()

        self.hdi = HdiConfiguration()
        self.batchai = BatchAiConfiguration()
        self.tensorflow = TensorflowConfiguration()
        self.mpi = MpiConfiguration()
        self.container_instance = ContainerInstanceConfiguration()
        self.data_references = {}

        if _history_enabled:
            self.history.output_collection = _history_enabled

        conda_dependencies = conda_dependencies if conda_dependencies else CondaDependencies()
        self.environment.python.conda_dependencies = conda_dependencies

    def __setattr__(self, name, value):
        """ Method for managing attribute validation """

        if name in ATTRIBUTES:
            super(RunConfiguration, self).__setattr__(name, value)
        else:
            raise AttributeError("RunConfiguration has no attribute %s" % name)

    @property
    def target(self):
        """
        Target refers to compute where the job is scheduled for execution.
        The default target is "local" refering to the local machine.
        Available cloud compute targets can be found using the
        function :func:`azurml.core.workspace.Workspace.compute_targets`

        :return: The target name
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """
        :param target:
        :type target: str
        """
        if isinstance(target, (AbstractComputeTarget, ComputeTarget)):
            self._target = target.name
        elif isinstance(target, str):
            self._target = target

    def save(self, path=None, name=None, separate_environment_yaml=False):
        """
        Saves the RunConfiguration to a file on disk <run_config_name>.runconfig file.
        This method is useful when editing the configuration manually or when sharing the configuration with the CLI

        :param separate_environment_yaml: separate_environment_yaml=True saves the conda environment configuration file in
            a separate yaml file. The conda environment file name is named environment.yml
        :type separate_environment_yaml: bool
        :param path: A user selected root directory for run configurations. Typically this is the Git Repository
            or the python project root directory. The configuration is saved to a sub dirctory named aml_config.
        :type path: str
        :param name: The configuration file name.
        :type name: str
        :return:
        :rtype: None
        """
        name = name if name else self._name
        path = path if path else self._path

        if not name or len(name) == 0:
            raise UserErrorException("Name is required to save the runconfig")

        # If path is none, then cwd is used.

        self._save_with_default_comments(path, name, separate_environment_yaml=separate_environment_yaml)
        # After this we also save the conda dependencies to the conda dependencies file.

        # If self.environment.python.conda_dependencies_file is none, which can be if
        # runconfig is fetched from cloud, then we default to name_conda_dependencies.yml
        if not self.environment.python.conda_dependencies_file:
            self.environment.python.conda_dependencies_file = AML_CONFIG_DIR + "/" + name + "_conda_dependencies.yml"

        self.environment.python.conda_dependencies.save_to_file(
            path, conda_file_path=self.environment.python.conda_dependencies_file)

    @staticmethod
    def load(path, name):
        """
        Loads a previously saved run configuration file from an on-disk file.

        :param path: A user selected root directory for run configurations. Typically this is the Git Repository
            or the python project root directory. The configuration is loaded from a sub dirctory named aml_config.
        :type path: str
        :param name: The configuration file name.
        :type name: str
        :return: The run configuration object.
        :rtype: RunConfiguration
        """
        # TODO: Check that name doesn't contain the extension.
        all_files_dict = get_project_files(path, RUNCONFIGURATION_EXTENSION)

        if name not in all_files_dict:
            raise UserErrorException("Run config with name = {} doesn't exist in the "
                                     "aml_config folder".format(name))

        full_run_config_path = os.path.join(path, all_files_dict[name])

        with open(full_run_config_path, "r") as run_config:
            # Loads with all the comments intact.
            commented_map_dict = ruamel.yaml.round_trip_load(run_config)
            return RunConfiguration._get_runconfig_using_dict(commented_map_dict,
                                                              path=path, name=name)

    @staticmethod
    def delete(path, name):
        """
        Deletes a run configuration file.

        :param path: A user selected root directory for run configurations. Typically this is the Git Repository
            or the python project root directory. The configuration is deleted from a sub dirctory named aml_config.
        :type path: str
        :param name: The configuration file name.
        :type name: str
        :return:
        :raises: UserErrorException
        """
        full_file_path = os.path.join(path, AML_CONFIG_DIR,
                                      name + RUNCONFIGURATION_EXTENSION)
        if os.path.isfile(full_file_path):
            os.remove(full_file_path)
        else:
            raise UserErrorException('Run config {} not found in {}'.format(name, os.getcwd()))

    @staticmethod
    def _deserialize_and_add_to_object(class_name, serialized_dict, object_to_populate=None):
        """
        A static method to deserialize serialized_dict into an object of class_name.
        object_to_populate is an object of class_name class, if object_to_populate=None, then
        we create class_name(), an object with empty constructor.

        :param class_name: The class name, mainly classes of this file.
        :type class_name: str
        :param serialized_dict: The serialized dict.
        :type serialized_dict: ruamel.yaml.comments.CommentedMap
        :param object_to_populate: An object of class_name class.
        :type object_to_populate: class_name
        :return: Adds the fields and returns object_to_populate
        :rtype: class_name
        """
        if not hasattr(class_name, "_field_to_info_dict"):
            raise RunConfigurationException("{} class doesn't have _field_to_info_dict "
                                            "field, which is required for deserializaiton".format(class_name))

        if not object_to_populate:
            object_to_populate = class_name()
            # For preserving comments in load() and save()
            if (hasattr(object_to_populate, "_loaded_commented_map") and
                    type(serialized_dict) == ruamel.yaml.comments.CommentedMap):
                object_to_populate._loaded_commented_map = serialized_dict

        for field, field_info in class_name._field_to_info_dict.items():
            serialized_name = field_info.serialized_name or field
            dict_key = to_camel_case(serialized_name)
            # We skip the fields that are not present in the serialized_dict
            if dict_key not in serialized_dict:
                continue

            # This should NEVER be replaced with not serialized_dict[dict_key], as that also
            # includes cases like [], False, {}, which are then written as None.
            if serialized_dict[dict_key] is None:
                # None doesn't have a type and doesn't cast well, so make it a special case.
                setattr(object_to_populate, field, None)
            elif field_info.field_type == str:
                setattr(object_to_populate, field, serialized_dict[dict_key])
            elif field_info.field_type == list:
                if field_info.list_element_type:
                    list_element_type = field_info.list_element_type
                    if list_element_type == str:
                        setattr(object_to_populate, field, serialized_dict[dict_key])
                    else:
                        # TODO: Add support for other basic types too.
                        # Else case is our custom class case.
                        list_dict = serialized_dict[dict_key]
                        list_with_objects = list()
                        for object_dict in list_dict:
                            class_object = RunConfiguration._deserialize_and_add_to_object(
                                list_element_type, object_dict)
                            list_with_objects.append(class_object)

                        setattr(object_to_populate, field, list_with_objects)
                else:
                    raise RunConfigurationException("Error in deserialization. List fields "
                                                    "don't have list element type information."
                                                    "field={}, serialized_dict={}".format(field, serialized_dict))
            elif field_info.field_type == dict:
                populate_dict_value = serialized_dict[dict_key]
                if field_info.list_element_type:
                    try:
                        list_element_type = field_info.list_element_type
                        dict_with_objects = dict()
                        for key, value in populate_dict_value.items():
                            class_object = RunConfiguration._deserialize_and_add_to_object(list_element_type, value)
                            if hasattr(class_object, "_validate"):
                                validate_method = getattr(class_object, "_validate")
                                validate_method()

                            dict_with_objects[key] = class_object
                        populate_dict_value = dict_with_objects
                    except Exception as ex:
                        raise RunConfigurationException("Error in deserialization. dict fields "
                                                        "don't have list element type information. "
                                                        "field={}, list_element_type={}, serialized_dict={} with "
                                                        "exception {}".format(field, list_element_type,
                                                                              serialized_dict, ex))
                setattr(object_to_populate, field, populate_dict_value)
            elif field_info.field_type == bool:
                setattr(object_to_populate, field, bool(serialized_dict[dict_key]))
            elif field_info.field_type == int:
                setattr(object_to_populate, field, int(serialized_dict[dict_key]))
            else:
                # Custom class case.
                setattr(object_to_populate, field,
                        RunConfiguration._deserialize_and_add_to_object(
                            field_info.field_type, serialized_dict[dict_key]))

        return object_to_populate

    @staticmethod
    def _serialize_to_dict(entity, use_commented_map=False):
        """
        Serializes entity into a dictionary recursively. entity can be a
        python class object, dict or list.
        :param entity:
        :type entity: class object, dict or list.
        :param use_commented_map: use_commented_map=True, uses the ruamel's CommentedMap instead of dict.
            CommentedMap gives us an ordered dict in which we also add default comments before dumping into the file.
        :type use_commented_map: bool
        :return: The serialized dictionary.
        :rtype: ruamel.yaml.comments.CommentedMap
        """
        # This is a way to find out whether entity is a python object or not.
        if hasattr(entity, "__dict__") and hasattr(entity.__class__, "_field_to_info_dict"):
            if use_commented_map:
                from ruamel.yaml.comments import CommentedMap
                # Preserving the comments from load load()
                if hasattr(entity, "_loaded_commented_map") and entity._loaded_commented_map:
                    result = entity._loaded_commented_map
                else:
                    result = CommentedMap()
            else:
                result = dict()

            first = True
            for key, field_info in entity.__class__._field_to_info_dict.items():
                serialized_name = field_info.serialized_name or key
                if key in entity.__dict__ and (serialized_name[0] != "_"):
                    name = to_camel_case(serialized_name)
                    result[name] = RunConfiguration._serialize_to_dict(entity.__dict__[key],
                                                                       use_commented_map=use_commented_map)
                    if use_commented_map and field_info.documentation:
                        # TODO: Indenting
                        if not RunConfiguration._check_before_comment(result, name, first=first):
                            RunConfiguration._yaml_set_comment_before_after_key_with_error(result, name,
                                                                                           field_info.documentation)
                            # result.yaml_set_comment_before_after_key(name, field_info.documentation)
                    first = False

            return result

        if isinstance(entity, list):
            return [RunConfiguration._serialize_to_dict(x, use_commented_map=use_commented_map) for x in entity]

        if isinstance(entity, dict):
            # Converting a CommentedMap into a regular dict.
            if not use_commented_map:
                entity = dict(entity)

            for key, value in entity.items():
                if hasattr(value, "__dict__"):
                    if hasattr(value.__class__, "_field_to_info_dict"):
                        entity[key] = RunConfiguration._serialize_to_dict(value, use_commented_map=use_commented_map)
                    else:
                        raise UserErrorException("Dictionary with non-native python type values are not "
                                                 "supported in runconfigs.{}".format(entity))

        # A simple literal, so we just return.
        return entity

    @staticmethod
    def _check_old_config(serialized_dict):
        """
        :param serialized_dict:
        :type serialized_dict: dict
        :return: Returns true if serialized_dict is an old config serialization.
        :rtype: bool
        """
        # We check for the new config parameters.
        # TODO: A better way to distinguish, right now we just check
        # these two keys as they occur in the new config.
        # We expect these to be present even in local, docker cases.
        if to_camel_case("environment") in serialized_dict and to_camel_case("history"):
            return False
        else:
            return True

    @staticmethod
    def _check_name_validity(name):
        if name.endswith(RUNCONFIGURATION_EXTENSION):
            raise UserErrorException("Run config name should not be suffixed with {}".format(
                RUNCONFIGURATION_EXTENSION))

    @staticmethod
    def _get_all_run_configurations(path):
        """
        :param path:
        :type path:
        :return: Returns a dictionary of all RunConfiguration objects.
        A key is a run config name, the value is the RunConfiguration object.
        :rtype: dict
        """
        run_configs_dict = dict()

        for _, _, filenames in os.walk(os.path.join(path,
                                                    AML_CONFIG_DIR)):
            for file in filenames:
                file_extension = os.path.splitext(file)[-1]
                name = os.path.splitext(file)[0]
                if file_extension == RUNCONFIGURATION_EXTENSION:
                    run_config_file_path = os.path.join(path,
                                                        AML_CONFIG_DIR, file)
                    if os.path.isfile(run_config_file_path):
                        try:
                            run_config_object = RunConfiguration(_path=run_config_file_path, _name=name)
                            run_configs_dict[name] = run_config_object
                        except Exception:
                            # TODO: Skipping the error run configs.
                            continue

        return run_configs_dict

    @staticmethod
    def _load_legacy_runconfig(path, name, commented_dict):
        """
        Loads legacy runconfig from serialized_dict and returns a RunConfiguration object.

        :param path:
        :type path: str
        :param name: The run config name.
        :type name: str
        :param commented_dict:
        :type commented_dict: ruamel.yaml.comments.CommentedMap
        :return: The run configuration object.
        :rtype: RunConfiguration
        """
        # Old config fields
        script = None
        argument_vector = None
        conda_dependencies = None
        framework = None
        auto_prepare_environment = False
        spark_dependencies_file = None
        target = None
        tracked_run = None

        # Old runconfig case is title case.
        if "ArgumentVector" in commented_dict:
            argument_vector = commented_dict["ArgumentVector"]
            if argument_vector and len(argument_vector) >= 1:
                script = argument_vector[0]
                argument_vector = argument_vector[1:]
            else:
                raise UserErrorException("ArgumentVector in runconfig cannot be empty.")

        if "Target" in commented_dict:
            target = commented_dict["Target"]

        if "Framework" in commented_dict:
            framework = commented_dict["Framework"]

        if "CondaDependenciesFile" in commented_dict:
            conda_dependencies = CondaDependencies(
                conda_dependencies_file_path=commented_dict["CondaDependenciesFile"])

        if "TrackedRun" in commented_dict:
            tracked_run = commented_dict["TrackedRun"]

        run_config_object = RunConfiguration(script=script, _history_enabled=tracked_run, _path=path, _name=name)
        run_config_object.arguments = argument_vector
        run_config_object.target = target
        run_config_object.framework = framework
        run_config_object.environment.python.conda_dependencies = conda_dependencies

        if "AutoPrepareEnvironment" in commented_dict:
            auto_prepare_environment = commented_dict["AutoPrepareEnvironment"]

        run_config_object.auto_prepare_environment = auto_prepare_environment

        if "EnvironmentVariables" in commented_dict:
            run_config_object.environment.environment_variables = commented_dict["EnvironmentVariables"]

        if run_config_object.target:
            RunConfiguration._modify_runconfig_using_compute_config(run_config_object, path)

        if "SparkDependenciesFile" in commented_dict:
            spark_dependencies_file = commented_dict["SparkDependenciesFile"]

        if spark_dependencies_file:
            RunConfiguration._modify_runconfig_using_spark_config(spark_dependencies_file,
                                                                  run_config_object, path)

        # TODO: use_sampling not used.
        return run_config_object

    @staticmethod
    def _modify_runconfig_using_compute_config(run_config_object, path):
        """
        Reads <run_config_object.target>.compute file and updates the required parameters in
        run_config_object

        :param run_config_object:
        :type run_config_object: RunConfiguration
        :param path:
        :type path: str
        :return:
        :rtype: None
        """
        compute_target_path = os.path.join(
            path, AML_CONFIG_DIR,
            run_config_object.target + COMPUTECONTEXT_EXTENSION)

        if not os.path.isfile(compute_target_path):
            raise UserErrorException("Compute target = {} doesn't exist at {}".format(
                run_config_object.target, compute_target_path))

        with open(compute_target_path, "r") as compute_target_file:
            compute_target_dict = ruamel.yaml.round_trip_load(compute_target_file)
            if "baseDockerImage" in compute_target_dict:
                run_config_object.environment.docker.base_image \
                    = compute_target_dict["baseDockerImage"]

            if "pythonLocation" in compute_target_dict:
                run_config_object.environment.python.interpreter_path = compute_target_dict["pythonLocation"]

            # For user managed environment set spark cache packages to false.
            # This will bypass image build step.
            if "userManagedEnvironment" in compute_target_dict:
                run_config_object.environment.python.user_managed_dependencies \
                    = compute_target_dict["userManagedEnvironment"]
                run_config_object.environment.spark.precache_packages \
                    = not compute_target_dict["userManagedEnvironment"]

            if "type" in compute_target_dict:
                if compute_target_dict["type"] == "remotedocker" or \
                        compute_target_dict["type"] == "localdocker" or \
                        compute_target_dict["type"] == "batchai" or \
                        compute_target_dict["type"] == "containerinstance":
                    run_config_object.environment.docker.enabled = True

            if "sharedVolumes" in compute_target_dict:
                run_config_object.environment.docker.shared_volumes = compute_target_dict["sharedVolumes"]

            if "nvidiaDocker" in compute_target_dict:
                run_config_object.environment.docker.gpu_support = compute_target_dict["nvidiaDocker"]

            if "yarnDeployMode" in compute_target_dict:
                run_config_object.hdi.yarn_deploy_mode = compute_target_dict["yarnDeployMode"]

            if "nodeCount" in compute_target_dict:
                run_config_object.batchai.node_count = compute_target_dict["nodeCount"]

    @staticmethod
    def _modify_runconfig_using_spark_config(spark_dependencies_file, run_config_object, path,
                                             use_commented_map=False):
        """
        Reads the spark dependencies file and updates the runconfig.
        :param spark_dependencies_file: The spark dependencies file, the path should be relative to the project
        directory.
        :type spark_dependencies_file: str
        :param run_config_object:
        :type run_config_object: RunConfiguration
        :param path:
        :type path: str
        :param use_commented_map: use_commented_map=True, uses the ruamel's CommentedMap instead of dict.
        CommentedMap gives us an ordered dict in which we also add default comments before dumping into the file.
        :type use_commented_map: bool
        :return:
        :rtpye: None
        """
        if spark_dependencies_file:
            # Reading spark dependencies file.
            spark_dependencies_path = os.path.join(
                path, spark_dependencies_file)

            if not os.path.isfile(spark_dependencies_path):
                raise UserErrorException("Spark dependencies file = {} doesn't exist at {}".format(
                    spark_dependencies_file, spark_dependencies_path))

            with open(spark_dependencies_path, "r") as spark_file:
                if use_commented_map:
                    spark_file_dict = ruamel.yaml.round_trip_load(spark_file)
                else:
                    spark_file_dict = ruamel.yaml.safe_load(spark_file)

                spark_config_object = RunConfiguration._deserialize_and_add_to_object(
                    SparkConfiguration, spark_file_dict)
                spark_environment_object = RunConfiguration._deserialize_and_add_to_object(
                    SparkEnvironment, spark_file_dict)
                run_config_object.spark = spark_config_object
                run_config_object.environment.spark = spark_environment_object

    def _save_with_default_comments(self, path, name, separate_environment_yaml=False):
        """
        Saves the RunConfiguration to the on-disk <run_config_name>.runconfig file with the default comments
        for fields.

        The save() method doesn't do this because we don't want to overwrite a user's comments in a runconfig
        file with the default comments.

        The method is useful to create runconfigs on a compute target attach. After that, we should be using save()
        method.
        This method overwrites <run_config_name>.runconfig on-disk.
        :param path: The path of the run configuration.
        :type path: str
        :param name: The name of the run configuration.
        :type name: str
        :param separate_environment_yaml: separate_environment_yaml=True saves the environment configuration in
        a separate yaml file. The environment file name will be environment.yml
        :type separate_environment_yaml: bool
        :return:
        :rtype: None
        """
        commented_map_dict = RunConfiguration._serialize_to_dict(self, use_commented_map=True)

        # TODO: More documentation for all fields.
        if separate_environment_yaml:
            environment_commented_map = commented_map_dict.get("environment")

            commented_map_dict["environment"] = AML_CONFIG_DIR + "/" + "environment.yml"

            if not RunConfiguration._check_before_comment(commented_map_dict, "environment"):
                # A hack to prevent a ruamel bug.
                # commented_map_dict.ca.items["environment"] = [None, [], None, None]
                RunConfiguration._yaml_set_comment_before_after_key_with_error(
                    commented_map_dict, "environment", "The file path that contains the environment configuration.")

            run_config_file_name = name + RUNCONFIGURATION_EXTENSION
            full_file_path = os.path.join(path,
                                          AML_CONFIG_DIR, run_config_file_name)
            with open(full_file_path, 'w') as outfile:
                ruamel.yaml.round_trip_dump(commented_map_dict, outfile)

            full_file_path = os.path.join(path,
                                          AML_CONFIG_DIR, "environment.yml")
            with open(full_file_path, 'w') as outfile:
                ruamel.yaml.round_trip_dump(environment_commented_map, outfile)
        else:

            # TODO: More documentation for all fields.
            run_config_file_name = name + RUNCONFIGURATION_EXTENSION
            full_file_path = os.path.join(path,
                                          AML_CONFIG_DIR, run_config_file_name)
            with open(full_file_path, 'w') as outfile:
                ruamel.yaml.round_trip_dump(commented_map_dict, outfile)

    @staticmethod
    def _check_before_comment(commented_map, key_to_check, first=False):
        """
        Checks if commented_map has a comment before key_to_check or not.
        All our default comments are before a key, so we just check for that.
        :param commented_map:
        :type commented_map: ruamel.yaml.comments.CommentedMap
        :param key_to_check:
        :type key_to_check: str
        :param first: True if the key is the first key in the yaml file, as that comment is associated with the file
        and not with the key.
        :type first: bool
        :return: True if there is a comment before a key.
        :rtype: bool
        """
        if first:
            # In the first case, the comment is associated to the CommentedMap, and not to the key.
            comments_list = commented_map.ca.comment
            if not comments_list:
                return False

            # This is the comment structure in ruamel. They don't have any good method for us to check.
            return len(comments_list) > 1 and comments_list[1] and len(comments_list[1]) > 0
        else:
            comments_dict = commented_map.ca.items
            if not comments_dict:
                return False
            if key_to_check in comments_dict:
                comments_list = comments_dict[key_to_check]
                # This is the comment structure in ruamel. They don't have nay good method for us to check.
                if len(comments_list) > 1 and comments_list[1] and len(comments_list[1]) > 0:
                    return True
                else:
                    return False
            else:
                # No key exists, so no comments.
                return False

    @staticmethod
    def _yaml_set_comment_before_after_key_with_error(commented_map, field_name, field_documentation):
        """
        Adds the comment with error handling, which is because of a bug in ruamel
        :param commented_map:
        :type commented_map: CommentedMap
        :param field_name:
        :type field_name: str
        :param field_documentation:
        :type field_documentation: str
        :return:
        """
        try:
            commented_map.yaml_set_comment_before_after_key(field_name, field_documentation)
        except Exception:
            commented_map.ca.items[field_name] = [None, [], None, None]
            commented_map.yaml_set_comment_before_after_key(field_name, field_documentation)

    @staticmethod
    def _check_camel_case_keys(current_object, current_class):
        """
        Recursive function that converts all keys to camel case.
        Returns (all_camel_case, new_current_object). where all_camel_case=False
        means that non-camel case keys were found in current_object. new_current_object
        is a copy of current_object where all keys are in camel case.
        :param current_object:
        :type current_object: CommentedMap, list or any basic type.
        :param current_class: The current class whose serialized element we are checking.
        :type current_class: AbstractRunConfigElement
        :return:(all_camel_case, new_current_object)
        :rtype: bool, object
        """
        all_camel_case = True
        new_class_name = None
        from ruamel.yaml.comments import CommentedMap
        if isinstance(current_object, CommentedMap) or isinstance(current_object, dict):
            if isinstance(current_object, CommentedMap):
                new_commented_map = CommentedMap()
            else:
                new_commented_map = dict()

            for (key, value) in current_object.items():
                snake_case_key = to_snake_case(to_camel_case(key))
                field_info = None

                if current_class and issubclass(current_class, AbstractRunConfigElement):
                    field_info = RunConfiguration._get_field_info_object(current_class, snake_case_key)

                # We skip changing case for user keys
                if field_info and field_info.user_keys:
                    new_commented_map[to_camel_case(key)] = value
                else:
                    if field_info:
                        new_class_name = field_info.field_type
                        # list is a special case, where we send the list element type.
                        if isinstance(value, list):
                            new_class_name = field_info.list_element_type

                    sub_all_camel_case, new_value = RunConfiguration._check_camel_case_keys(value, new_class_name)
                    if not sub_all_camel_case or to_camel_case(key) != key:
                        all_camel_case = False

                    new_commented_map[to_camel_case(key)] = new_value
            return all_camel_case, new_commented_map
        elif isinstance(current_object, list):
            new_list = list()
            for list_item in current_object:
                sub_all_camel_case, new_list_item = RunConfiguration._check_camel_case_keys(list_item, current_class)
                if not sub_all_camel_case:
                    all_camel_case = sub_all_camel_case
                new_list.append(new_list_item)

            return all_camel_case, new_list
        else:
            # Basic types case.
            # TODO: We may want to have a deepcopy here, but doesn't look necessary.
            return all_camel_case, current_object

    @staticmethod
    def _get_field_info_object(class_type, snake_case_key):
        """
        Returns a _FieldInfo object for a key. The key has to be a snake case key.
        :param class_type:
        :type class_type: object
        :param snake_case_key:
        :type snake_case_key: str
        :return:
        :rtype: _FieldInfo
        """
        if class_type and issubclass(class_type, AbstractRunConfigElement):
            field_type_dict = class_type._field_to_info_dict
            if snake_case_key in field_type_dict:
                return field_type_dict[snake_case_key]
        return None

    @staticmethod
    def _get_run_config_object(path, run_config):
        """
        :param path:
        :type path: str
        :param run_config:
        :type run_config: RunConfiguration
        :return: Returns the run configuration object
        :rtype: azureml.core.runconfig.RunConfiguration
        """
        if isinstance(run_config, str):
            # If it is a string then we don't need to create a copy.
            return RunConfiguration.load(path, run_config)
        elif isinstance(run_config, RunConfiguration):
            # TODO: Deep copy of project and auth object too.
            import copy
            return copy.deepcopy(run_config)
        else:
            raise UserErrorException("Unsupported runconfig type {}. run_config can be of str or "
                                     "azureml.core.runconfig.RunConfiguration type.".format(type(run_config)))

    @staticmethod
    def _get_runconfig_using_runid(experiment, run_id):
        """
        Returns a runconfig using the experiment and runconfig, by fetching
        the runconfig from the experiment service in the cloud.
        :param experiment:
        :type experiment: azureml.core.experiment.Experiment
        :param run_id:
        :type run_id: str
        :return:
        :rtype: RunConfiguration
        """
        run = Run(experiment, run_id)
        run_details = run.get_details()
        if "runDefinition" in run_details:
            return RunConfiguration._get_runconfig_using_dict(run_details["runDefinition"])
        else:
            raise RunConfigurationException("Run configuration not found for the given experiment and run id.")

    @staticmethod
    def _get_runconfig_using_dict(commented_map_or_dict, path=None, name=None):
        """
        Constructs the runconfig object from the serialized commented_map_or_dict.
        :param commented_map_or_dict:
        :type commented_map_or_dict: dict
        :param path:
        :type path: str
        :param name:
        :type name: str
        :return:
        :rtype:RunConfiguration
        """
        all_camel_case, new_commented_map = RunConfiguration._check_camel_case_keys(commented_map_or_dict,
                                                                                    RunConfiguration)
        if not all_camel_case:
            # Replacing with the new map that has keys in camelCase
            commented_map_or_dict = new_commented_map

        if RunConfiguration._check_old_config(commented_map_or_dict):
            # Old runconfig case.
            return RunConfiguration._load_legacy_runconfig(path, name,
                                                           commented_map_or_dict)
        else:
            # New runconfig case.

            # Check if environment is specified as a dict or a file reference.
            if "environment" in commented_map_or_dict and type(commented_map_or_dict["environment"]) == str:
                # environment is specified as a file reference.
                environment_path = os.path.join(path,
                                                commented_map_or_dict["environment"])
                with open(environment_path, "r") as environment_config:
                    # Replacing string path with the actual environment serialized dictionary.
                    commented_map_or_dict["environment"] = ruamel.yaml.round_trip_load(environment_config)

            run_config_object = RunConfiguration(_path=path, _name=name)

            # Only wants to preserve the comments if it is a commented map.
            if type(commented_map_or_dict) == ruamel.yaml.comments.CommentedMap:
                run_config_object._loaded_commented_map = commented_map_or_dict

            RunConfiguration._deserialize_and_add_to_object(
                RunConfiguration, commented_map_or_dict, object_to_populate=run_config_object)

            # If the runconfig was retrieved from run history, it will have inline dependencies.
            # Extract them here because they won't be recognized as run configuration fields.
            inline_conda_dependencies = \
                commented_map_or_dict.get("environment", {}).get("python", {}).get("condaDependencies", None)

            if inline_conda_dependencies:
                # Replace the raw deserialized struct with the CondaDependencies wrapper class.
                conda_dependencies = CondaDependencies(_underlying_structure=inline_conda_dependencies)
            else:
                # Loading the conda file as conda object and setting that in the runconfig.
                conda_dependencies = CondaDependencies(
                    os.path.join(path,
                                 run_config_object.environment.python.conda_dependencies_file))
            run_config_object.environment.python.conda_dependencies = conda_dependencies

            return run_config_object
