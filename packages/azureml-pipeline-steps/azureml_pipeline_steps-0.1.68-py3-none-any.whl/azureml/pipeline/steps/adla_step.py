# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""adla_step.py, module for adding a node to run U-SQL script using Azure Data Lake Analytics."""
from azureml.core.compute import AdlaCompute
from azureml.pipeline.core import PipelineStep
from azureml.pipeline.core.graph import ParamDef
from azureml.pipeline.core._module_builder import _FolderModuleBuilder

import re


class AdlaStep(PipelineStep):
    """Adds a step to run U-SQL script using Azure Data Lake Analytics.

    :param script_name: name of usql script (relative to source_directory)
    :type script_name: str
    :param name: Name of the step.  If unspecified, script_name will be used
    :type name: str
    :param inputs: List of input port bindings
    :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
                  azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
    :param outputs: List of output port bindings
    :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
    :param params: Dictionary of name-value pairs
    :type params: dict
    :param degree_of_parallelism: the degree of parallelism to use for this job
    :type degree_of_parallelism: int
    :param priority: the priority value to use for the current job
    :type priority: int
    :param runtime_version: the runtime version of the Data Lake Analytics engine
    :type runtime_version: str
    :param adla_compute: the ADLA compute to use for this job
    :type adla_compute: azureml.core.compute.AdlaCompute, str
    :param source_directory: folder that contains the script, assemblies etc.
    :type source_directory: str
    :param allow_reuse: Whether the step should reuse previous results when run with the same settings/inputs
    :type allow_reuse: bool
    :param version: Optional version tag to denote a change in functionality for the step
    :type version: str
    :param hash_paths: list of paths to hash to detect a change (script file is always hashed)
    :type hash_paths: list
    """

    def __init__(self, script_name, name=None, inputs=None, outputs=None, params=None, degree_of_parallelism=None,
                 priority=None, runtime_version=None, adla_compute=None, source_directory=None,
                 allow_reuse=True, version=None, hash_paths=None):
        """
        Initialize AdlaStep.

        :param script_name: name of usql script (relative to source_directory)
        :type script_name: str
        :param name: Name of the step.  If unspecified, script_name will be used
        :type name: str
        :param inputs: List of input port bindings
        :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
                    azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
        :param outputs: List of output port bindings
        :type outputs: list[azureml.pipeline.core.builder.PipelineData, azureml.pipeline.core.graph.OutputPortBinding]
        :param params: Dictionary of name-value pairs
        :type params: {str: str}
        :param degree_of_parallelism: the degree of parallelism to use for this job
        :type degree_of_parallelism: int
        :param priority: the priority value to use for the current job
        :type priority: int
        :param runtime_version: the runtime version of the Data Lake Analytics engine
        :type runtime_version: str
        :param adla_compute: the ADLA compute to use for this job
        :type adla_compute: AdlaCompute, str
        :param source_directory: folder that contains the script, assemblies etc.
        :type source_directory: str
        :param allow_reuse: Whether the step should reuse previous results when run with the same settings/inputs
        :type allow_reuse: bool
        :param version: Optional version tag to denote a change in functionality for the step
        :type version: str
        :param hash_paths: list of paths to hash to detect a change (script file is always hashed)
        :type hash_paths: [str]
        """
        if name is None:
            name = script_name
        if script_name is None:
            raise ValueError("script_name is required")
        if not isinstance(script_name, str):
            raise ValueError("script_name must be a string")
        if adla_compute is None:
            raise ValueError('adla_compute is required')

        self._script_name = script_name
        self._source_directory = source_directory
        self._adla_compute = adla_compute
        self._params = params or {}
        self._allow_reuse = allow_reuse
        self._version = version
        self._pipeline_params_in_step_params = PipelineStep._get_pipeline_parameters_step_params(params)

        self._hash_paths = hash_paths or []
        self._hash_paths.append(self._script_name)

        self._metadata_params = {
            'ScriptName': script_name
        }

        if degree_of_parallelism is not None:
            self._metadata_params['DegreesOfParallelism'] = degree_of_parallelism
        if priority is not None:
            self._metadata_params['Priority'] = priority
        if runtime_version is not None:
            self._metadata_params['RuntimeVersion'] = runtime_version

        super().__init__(name, inputs, outputs)

    def create_node(self, graph, default_datastore_name, context):
        """
        Create a node.

        :param graph: graph object
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_datastore_name: default datastore name
        :type default_datastore_name: str
        :param context: context
        :type context: _GraphContext

        :return: The node object.
        :rtype: azureml.pipeline.core.graph.Node
        """
        adla_resource_id = self._get_adla_resource_id(context)
        adla_config = AdlaStep._get_adla_config(adla_resource_id)

        self._metadata_params['AnalyticsAccountName'] = adla_config['AdlaAccountName']
        self._metadata_params['SubscriptionId'] = adla_config['AdlaSubscriptionId']
        self._metadata_params['ResourceGroupName'] = adla_config['AdlaResourceGroup']

        source_directory, hash_paths = self.get_source_directory_and_hash_paths(
            context, self._source_directory, self._script_name, self._hash_paths)

        input_bindings, output_bindings = self.create_input_output_bindings(self._inputs, self._outputs,
                                                                            default_datastore_name)

        param_defs = [ParamDef(param) for param in self._params]
        param_defs += [ParamDef(param, is_metadata_param=True) for param in self._metadata_params]

        module_def = self.create_module_def(execution_type="adlcloud", input_bindings=input_bindings,
                                            output_bindings=output_bindings, param_defs=param_defs,
                                            allow_reuse=self._allow_reuse, version=self._version)

        module_builder = _FolderModuleBuilder(
            content_root=source_directory,
            hash_paths=hash_paths,
            context=context,
            module_def=module_def)

        param_values = self._params
        param_values.update(self._metadata_params)

        node = graph.add_module_node(self.name, input_bindings, output_bindings, param_values,
                                     module_builder=module_builder)
        PipelineStep.\
            _configure_pipeline_parameters(graph,
                                           node,
                                           pipeline_params_in_step_params=self._pipeline_params_in_step_params)

        return node

    def _get_adla_resource_id(self, context):
        """
        Get ADLA resource ID.

        :param context: The graph context object
        :type context: _GraphContext

        :return: The cluster resource id of adla compute.
        :rtype: str
        """
        adla_compute = self._adla_compute

        if isinstance(adla_compute, AdlaCompute):
            return adla_compute.cluster_resource_id

        if isinstance(adla_compute, str):
            try:
                adla_compute = AdlaCompute(context._workspace, adla_compute)
                return adla_compute.cluster_resource_id
            except Exception as e:
                raise ValueError('error in getting adla compute: {}'.format(e))

        raise ValueError('adla_compute is not specified correctly')

    @staticmethod
    def _get_adla_config(adla_resource_id):
        """
        Get ADLA config.

        :param adla_resource_id: adla resource id
        :type adla_resource_id: str

        :return: Dictionary of adl cluster info.
        :rtype: dict
        """
        resource_id_regex = \
            r'\/subscriptions\/([^/]+)\/resourceGroups\/([^/]+)\/providers' \
            '\/Microsoft\.DataLakeAnalytics\/accounts\/([^/]+)'

        match = re.search(resource_id_regex, adla_resource_id, re.IGNORECASE)

        if match is None:
            raise ValueError('adla resource id is not in correct format: {}'.format(adla_resource_id))

        return {
            'AdlaSubscriptionId': match.group(1),
            'AdlaResourceGroup': match.group(2),
            'AdlaAccountName': match.group(3),
        }
