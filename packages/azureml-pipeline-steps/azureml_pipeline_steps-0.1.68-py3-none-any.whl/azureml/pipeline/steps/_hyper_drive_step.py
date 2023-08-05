# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""hyper_drive_step.py."""
from azureml.pipeline.core import PipelineStep


class HyperDriveStep(PipelineStep):
    """Creates a Hyper Drive step in a Pipeline.

    :param name: name
    :type name: str
    :param hyperdrive_runconfig: hyper drive run config
    :type hyperdrive_runconfig: azureml.train.hyperdrive.runconfig.HyperDriveRunConfig
    :param inputs: inputs
    :type inputs: list[azureml.pipeline.core.builder.PipelineData, azureml.data.data_reference.DataReference]
    """

    def __init__(self, name, hyperdrive_runconfig, inputs):
        """Initialize a HyperDriveStep.

        :param name: name
        :type name: str
        :param hyperdrive_runconfig: hyper drive run config
        :type hyperdrive_runconfig: azureml.train.hyperdrive.runconfig.HyperDriveRunConfig
        :param inputs: inputs
        :type inputs: list[azureml.data.data_reference.DataReference or azureml.pipeline.core.builder.PipelineData]
        """
        self.hyperdrive_runconfig = hyperdrive_runconfig

    def create_node(self, graph, default_datastore_name, context):
        """
        Create a node from this HyperDrive step and add to the given graph.

        :param graph: The graph object to add the node to.
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_datastore_name: The default datastore name to use.
        :type default_datastore_name: str
        :param context: The graph context.
        :type context: _GraphContext

        :return: The created node.
        :rtype: azureml.pipeline.core.graph.Node
        """
        raise Exception('not implemented')
