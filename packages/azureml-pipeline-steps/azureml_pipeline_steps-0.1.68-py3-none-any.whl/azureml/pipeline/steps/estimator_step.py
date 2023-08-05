# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""estimator_step.py."""
from azureml.pipeline.steps import PythonScriptStep
from azureml.train.estimator import MMLBaseEstimator


class EstimatorStep(PythonScriptStep):
    """Adds a step to run U-SQL script using Azure Data Lake Analytics.

    :param name: name
    :type name: str
    :param estimator: estimator
    :type estimator: azureml.train.estimator.Estimator
    :param inputs: inputs
    :type inputs: list[azureml.pipeline.core.builder.PipelineData, azureml.data.data_reference.DataReference]
    :param outputs: output is list of PipelineData
    :type outputs: list[azureml.pipeline.core.builder.PipelineData]
    :param allow_reuse: whether to allow reuse
    :type allow_reuse: bool
    :param version: version
    :type version: str
    """

    def __init__(self, name=None, estimator=None, inputs=None, outputs=None, allow_reuse=True, version=None):
        """
        Initialize EstimatorStep.

        :param name: name
        :type name: str
        :param estimator: estimator
        :type estimator: Estimator
        :param inputs: inputs
        :type inputs: list[azureml.pipeline.core.builder.PipelineData, azureml.data.data_reference.DataReference]
        :param outputs: outputs
        :type outputs: list[azureml.pipeline.core.builder.PipelineData]
        :param allow_reuse: whether to allow reuse
        :type allow_reuse: bool
        :param version: version
        :type version: str
        """
        if not isinstance(estimator, MMLBaseEstimator):
            raise Exception("Estimator parameter is not of valid type")
        self.estimator = estimator
        # TODO - validate estimator parameters (possibly by adding a method to estimator
        # and calling it from here as well as within estimator)

        run_config = self.estimator.run_config
        source_directory = self.estimator.source_directory
        script_name = run_config.script
        arguments = run_config.arguments
        target = self.estimator.run_config.target

        # TODO - add support for PythonScriptStep params inputs, outputs, file_outputs, directory_outputs,

        super(EstimatorStep, self).__init__(name=name, script_name=script_name, arguments=arguments, target=target,
                                            runconfig=run_config, inputs=inputs, outputs=outputs,
                                            source_directory=source_directory, allow_reuse=allow_reuse,
                                            version=version)

    def create_node(self, graph, default_target, context):
        """
        Create a node.

        :param graph: graph object
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_target: default target
        :type default_target: str
        :param context: context
        :type context: _GraphContext

        :return: The created node.
        :rtype: azureml.pipeline.core.graph.Node
        """
        return super(PythonScriptStep, self).create_node(graph, default_target, context)
