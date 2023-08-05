# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""mpi_step.py."""
from azureml.pipeline.steps import PythonScriptStep
from azureml.train.estimator import Estimator
from azureml.core.compute_target import BatchAITarget


class MpiStep(PythonScriptStep):
    """Add a step to run a MPI job in a Pipeline.

    :param name: Name of the module
    :type name: str
    :param source_directory: folder that contains the script, conda env etc.
    :type source_directory: str
    :param script_name: name of a python script (relative to source_directory)
    :type script_name: str
    :param arguments: List of command-line arguments
    :type arguments: list
    :param target: Compute target to use
    :type target: azureml.core.compute.BatchAiCompute, azureml.core.compute_target.BatchAITarget, str
    :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
           distributed job will be run. Only BatchAI compute target is supported for distributed jobs.
    :type node_count: int
    :param process_count_per_node: Number of processes per node. If greater than 1, mpi
             distributed job will be run. Only BatchAI compute target is supported for distributed jobs.
    :type process_count_per_node: int
    :param inputs: List of input port bindings
    :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
        azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
    :param outputs: List of output port bindings
    :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
    :param params: Dictionary of name-value pairs. Registered as environment variables with "AML_PARAMETER_"
    :type params: dict
    :param allow_reuse: Whether the module should reuse previous results when run with the same settings/inputs
    :type allow_reuse: bool
    :param version: Optional version tag to denote a change in functionality for the module
    :type version: str
    :param hash_paths: list of paths to hash to detect a change (script file is always hashed)
    :type hash_paths: list
    :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
        If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
        image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_base_image
        parameter is not set. This setting is used only in docker enabled compute targets.
    :type use_gpu: bool
    :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
        custom_docker_base_image (str): The name of the docker image from which the image to use for mpi job
        will be built. If not set, a default CPU based image will be used as the base image. Use this setting only
        for images available in public docker repositories. To use an image from a private docker repository,
        use environment_definition parameter instead.
    :type use_docker: bool
    :param custom_docker_base_image: The name of the docker image from which the image to use for mpi job
    will be built. If not set, a default CPU based image will be used as the base image. Use this setting only
    for images available in public docker repositories. To use an image from a private docker repository,
    use environment_definition parameter instead.
    :type custom_docker_base_image: str
    :param conda_packages: List of strings representing conda packages to be added to the Python environment
        for the experiment.
    :type conda_packages: list
    :param pip_packages: List of strings representing pip packages to be added to the Python environment
        for the experiment.
    :type pip_packages: list
    :param environment_definition: The EnvironmentDefinition for the experiment. It includes
        PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
        exposed through other parameters to the MpiStep construction can be set using environment_definition
        parameter. If this parameter is specified, it will take precedence over other environment related
        parameters like use_gpu, custom_docker_base_image, conda_packages or pip_packages and errors will be
        reported on these invalid combinations.
    :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
    """

    def __init__(self, name=None, source_directory=None, script_name=None, arguments=None, target=None,
                 node_count=None, process_count_per_node=None, inputs=None, outputs=None,
                 allow_reuse=True, version=None, hash_paths=None, **kwargs):
        """Initialize MPI step.

        :param name: Name of the module
        :type name: str
        :param source_directory: folder that contains the script, conda env etc.
        :type source_directory: str
        :param script_name: name of a python script (relative to source_directory)
        :type script_name: str
        :param arguments: List of command-line arguments
        :type arguments: list
        :param target: Compute target to use
        :type target: azureml.core.compute.BatchAiCompute, azureml.core.compute_target.BatchAITarget, str
        :param node_count: Number of nodes in the compute target used for training. If greater than 1, mpi
               distributed job will be run. Only BatchAI compute target is supported for distributed jobs.
        :type node_count: int
        :param process_count_per_node: Number of processes per node. If greater than 1, mpi
                 distributed job will be run. Only BatchAI compute target is supported for distributed jobs.
        :type process_count_per_node: int
        :param inputs: List of input port bindings
        :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
            azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
        :param outputs: List of output port bindings
        :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
        :param params: Dictionary of name-value pairs. Registered as environment variables with "AML_PARAMETER_"
        :type params: dict
        :param allow_reuse: Whether the module should reuse previous results when run with the same settings/inputs
        :type allow_reuse: bool
        :param version: Optional version tag to denote a change in functionality for the module
        :type version: str
        :param hash_paths: list of paths to hash to detect a change (script file is always hashed)
        :type hash_paths: list
        :param use_gpu: A bool value indicating if the environment to run the experiment should support GPUs.
            If set to true, gpu-based default docker image will be used in the environment. If set to false, CPU based
            image will be used. Default docker images (CPU or GPU) will be used only if custom_docker_base_image
            parameter is not set. This setting is used only in docker enabled compute targets.
        :type use_gpu: bool
        :param use_docker: A bool value indicating if the environment to run the experiment should be docker-based.
            custom_docker_base_image (str): The name of the docker image from which the image to use for mpi job
            will be built. If not set, a default CPU based image will be used as the base image. Use this setting only
            for images available in public docker repositories. To use an image from a private docker repository,
            use environment_definition parameter instead.
        :type use_docker: bool
        :param custom_docker_base_image: The name of the docker image from which the image to use for mpi job
        will be built. If not set, a default CPU based image will be used as the base image. Use this setting only
        for images available in public docker repositories. To use an image from a private docker repository,
        use environment_definition parameter instead.
        :type custom_docker_base_image: str
        :param conda_packages: List of strings representing conda packages to be added to the Python environment
            for the experiment.
        :type conda_packages: list
        :param pip_packages: List of strings representing pip packages to be added to the Python environment
            for the experiment.
        :type pip_packages: list
        :param environment_definition: The EnvironmentDefinition for the experiment. It includes
            PythonEnvironment and DockerEnvironment and environment variables. Any environment option not directly
            exposed through other parameters to the MpiStep construction can be set using environment_definition
            parameter. If this parameter is specified, it will take precedence over other environment related
            parameters like use_gpu, custom_docker_base_image, conda_packages or pip_packages and errors will be
            reported on these invalid combinations.
        :type environment_definition: azureml.core.runconfig.EnvironmentDefinition
        """

        environment_variables = kwargs.get("environment_variables", None)
        use_gpu = kwargs.get("use_gpu", False)
        use_docker = kwargs.get("use_docker", True)
        custom_docker_base_image = kwargs.get("custom_docker_base_image", None)
        conda_packages = kwargs.get("conda_packages", None)
        pip_packages = kwargs.get("pip_packages", None)
        pip_requirements_file_path = kwargs.get("pip_requirements_file_path", None)
        environment_definition = kwargs.get("environment_definition", None)

        if None in [name, source_directory, script_name, arguments, target, node_count, process_count_per_node]:
            raise ValueError('One of the requirement parameters (name, source_directory, script_name, '
                             'arguments, target, node_count, process_count_per_node) is not set')

        # use Estimator to construct run config for mpi job
        # not setting script_params because arguments passed to PythonScriptStep will override what is in runconfig
        mpi_estimator = Estimator(source_directory=source_directory, compute_target=target, entry_script=script_name,
                                  script_params={}, node_count=node_count,
                                  distributed_backend='mpi', process_count_per_node=process_count_per_node,
                                  use_gpu=use_gpu, use_docker=use_docker,
                                  custom_docker_base_image=custom_docker_base_image,
                                  conda_packages=conda_packages, pip_packages=pip_packages,
                                  pip_requirements_file_path=pip_requirements_file_path,
                                  environment_definition=environment_definition)
        mpi_run_config = mpi_estimator.run_config

        if target.type.lower() != BatchAITarget._BATCH_AI_TYPE.lower():
            raise Exception("Compute target {0} is not supported in MpiStep. "
                            "Batch AI is the only supported target.".format(target, ))

        super(self.__class__, self).__init__(name=name, source_directory=source_directory, script_name=script_name,
                                             arguments=arguments, runconfig=mpi_run_config,
                                             params=environment_variables,
                                             target=target, inputs=inputs, outputs=outputs,
                                             allow_reuse=allow_reuse, version=version, hash_paths=hash_paths)
