# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""data_transfer_step.py, module for transfering data between Azure Blob and Data Lake accounts."""
from azureml.core.compute import DataFactoryCompute
from azureml.data.data_reference import DataReference
from azureml.pipeline.core import PipelineData, PipelineStep
from azureml.pipeline.core.graph import ParamDef, InputPortBinding, OutputPortBinding, PortDataReference
from azureml.pipeline.core._module_builder import _InterfaceModuleBuilder

import re


class DataTransferStep(PipelineStep):
    """Transfers data between Azure Blob and Data Lake accounts.

    :param name: Name of the step
    :type name: str
    :param source_data_reference: Input connection that serves as source of data transfer operation
    :type source_data_reference: list[azureml.pipeline.core.graph.InputPortBinding,
                  azureml.data.data_reference.DataReference, azureml.pipeline.core.PortDataReference,
                  azureml.pipeline.core.builder.PipelineData]
    :param destination_data_reference: Input connection that serves as destination of data transfer operation
    :type destination_data_reference:
        list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference]
    :param data_factory_compute: Azure Data Factory to use for transferring data
    :type data_factory_compute: DataFactoryCompute, str
    """

    def __init__(self, name, source_data_reference=None, destination_data_reference=None,
                 data_factory_compute=None):
        """
        Initialize DataTransferStep.

        :param name: Name of the step
        :type name: str
        :param source_data_reference: Input connection that serves as source of data transfer operation
        :type source_data_reference: list[azureml.pipeline.core.graph.InputPortBinding,
                    azureml.data.data_reference.DataReference, azureml.pipeline.core.PortDataReference,
                    azureml.pipeline.core.builder.PipelineData]
        :param destination_data_reference: Input connection that serves as destination of data transfer operation
        :type destination_data_reference:
                    list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference]
        :param data_factory_compute: Azure Data Factory to use for transferring data
        :type data_factory_compute: DataFactoryCompute, str
        """
        if name is None:
            raise ValueError('name is required')
        if not isinstance(name, str):
            raise ValueError('name must be a string')

        if data_factory_compute is None:
            raise ValueError('data_factory_compute is required')

        if not isinstance(destination_data_reference, InputPortBinding) and \
                not isinstance(destination_data_reference, DataReference):
            raise ValueError("Unexpected destination_data_reference type: %s" % type(destination_data_reference))

        if isinstance(destination_data_reference, InputPortBinding):
            bind_object = destination_data_reference.bind_object
            if isinstance(bind_object, DataReference):
                destination_data_reference = bind_object
            else:
                raise ValueError("destination_data_reference has unexpected bind_object type: %s" % type(bind_object))

        self._source_data_reference = source_data_reference
        self._destination_data_reference = destination_data_reference
        self._data_factory_compute = data_factory_compute

        source_input = DataTransferStep._create_input_port_binding(self._source_data_reference, 'SourceLocation')
        destination_input = DataTransferStep._create_input_port_binding(
            self._destination_data_reference, 'DestinationLocation')
        inputs = [source_input, destination_input]

        outputs = [OutputPortBinding(name='Output',
                                     datastore_name=self._destination_data_reference.datastore.name,
                                     bind_mode=self._destination_data_reference.mode,
                                     path_on_compute=self._destination_data_reference.path_on_compute,
                                     overwrite=self._destination_data_reference.overwrite)]

        super().__init__(name, inputs, outputs)

    def create_node(self, graph, default_datastore_name, context):
        """
        Create a node from this DataTransfer step and add to the given graph.

        :param graph: The graph object to add the node to.
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_datastore_name: The default datastore name to use.
        :type default_datastore_name: str
        :param context: The graph context.
        :type context: _GraphContext

        :return: The created node.
        :rtype: azureml.pipeline.core.graph.Node
        """
        data_factory_resource_id = self._get_data_factory_resource_id(context)
        data_factory_config = DataTransferStep._get_data_factory_config(data_factory_resource_id)

        param_defs = [ParamDef('Command', 'DataCopy')]
        param_defs += [ParamDef(name, is_metadata_param=True) for name in data_factory_config]

        module_def = self.create_module_def(execution_type="DataTransferCloud",
                                            input_bindings=self._inputs,
                                            output_bindings=self._outputs,
                                            param_defs=param_defs, create_sequencing_ports=False)

        module_builder = _InterfaceModuleBuilder(context=context, module_def=module_def)

        return graph.add_module_node(
            self.name,
            input_bindings=self._inputs,
            param_bindings=data_factory_config,
            module_builder=module_builder)

    def get_output(self):
        """
        Get the output of the step.

        :return: The output of the step.
        :rtype: azureml.pipeline.core.builder.PipelineData
        """
        output = self._destination_data_reference
        if isinstance(output, DataReference):
            output = PipelineData(
                name='Output',
                datastore_name=output.datastore.name,
                output_mode=output.mode,
                output_path_on_compute=output.path_on_compute,
                output_overwrite=output.overwrite)
            output._set_producer(self)
            return output

        raise TypeError('destination_data_reference is not of correct type')

    def _get_data_factory_resource_id(self, context):
        """
        Get the data factory resource id.

        :param context: context
        :type context: _GraphContext

        :return: The id of the data factory.
        :rtype: str
        """
        data_factory_compute = self._data_factory_compute

        if isinstance(data_factory_compute, DataFactoryCompute):
            return data_factory_compute.cluster_resource_id

        if isinstance(data_factory_compute, str):
            try:
                data_factory_compute = DataFactoryCompute(context._workspace, data_factory_compute)
                return data_factory_compute.cluster_resource_id
            except Exception as e:
                raise ValueError('Error in getting data factory compute: {}'.format(e))

        raise ValueError('data_factory_compute is not specified correctly')

    @staticmethod
    def _get_data_factory_config(data_factory_resource_id):
        """
        Get the data factory config.

        :param data_factory_resource_id: data factory resource id
        :type data_factory_resource_id: str

        :return: The data factory config.
        :rtype: dict
        """
        resource_id_regex = \
            r'\/subscriptions\/([^/]+)\/resourceGroups\/([^/]+)\/providers\/Microsoft\.DataFactory\/factories\/([^/]+)'

        match = re.search(resource_id_regex, data_factory_resource_id, re.IGNORECASE)

        if match is None:
            raise ValueError('Data Factory resource Id is not in correct format: {}'.format(data_factory_resource_id))

        return {
            'DataFactorySubscriptionId': match.group(1),
            'DataFactoryResourceGroup': match.group(2),
            'DataFactoryName': match.group(3),
        }

    @staticmethod
    def _create_input_port_binding(input_data_reference, input_port_name):
        """
        Create the input port binding.

        :param input_data_reference: input data reference object
        :type input_data_reference: data reference
        :param input_port_name: input port name
        :type input_port_name: str

        :return: The input port binding.
        :rtype: azureml.pipeline.core.graph.InputPortBinding
        """
        if isinstance(input_data_reference, InputPortBinding):
            return input_data_reference

        if isinstance(input_data_reference, PipelineData) or isinstance(input_data_reference, PortDataReference):
            return input_data_reference.create_input_binding(input_name=input_port_name)

        if isinstance(input_data_reference, DataReference):
            return InputPortBinding(
                name=input_port_name,
                bind_object=input_data_reference,
                bind_mode=input_data_reference.mode,
                path_on_compute=input_data_reference.path_on_compute,
                overwrite=input_data_reference.overwrite)

        raise TypeError('input_data_reference is not of correct type')
