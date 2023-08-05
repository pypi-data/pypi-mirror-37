# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""databricks_step.py, module for adding a DataBricks notebook or a python script on DBFS as a node."""
from azureml.pipeline.core import PipelineStep
from azureml.pipeline.core.graph import ParamDef
from azureml.pipeline.core._module_builder import _InterfaceModuleBuilder
from azureml.pipeline.databricks import AutoScale


class DatabricksStep(PipelineStep):
    """Adds a DataBricks notebook or a python script on DBFS as a step in a Pipeline.

    :param name: Name of the step
    :type name: str
    :param inputs: List of input connections for data consumed by this step. Fetch this inside the notebook
                    using dbutils.widgets.get("<input name>")
    :type inputs: list[azureml.pipeline.core.graph.InputPortBinding, azureml.data.data_reference.DataReference,
                     azureml.pipeline.core.PortDataReference, azureml.pipeline.core.builder.PipelineData]
    :param outputs: List of output port definitions for outputs produced by this step. Fetch this inside the
                    notebook using dbutils.widgets.get("<output name>")
    :type outputs: list[azureml.pipeline.core.graph.OutputPortBinding, azureml.pipeline.core.builder.PipelineData]
    :param spark_version: The version of spark for the Databricks run cluster. Example: "4.0.x-scala2.11"
    :type spark_version: str
    :param node_type: The Azure VM node types for the Databricks run cluster. Example: "Standard_D3_v2"
    :type node_type: str
    :param num_workers: The number of workers for the Databricks run cluster
    :type num_workers: int
    :param autoscale: The autoscale configuration for the Databricks run cluster
    :type autoscale: azureml.pipeline.steps.databricks.AutoScale
    :param spark_env_variables: The spark environment variables for the Databricks run cluster
    :type spark_env_variables: dict
    :param notebook_path: The path to the notebook in the Databricks instance
    :type notebook_path: str
    :param notebook_params: Parameters  for the Databricks notebook (dictionary of {str:str}). Fetch this inside
                            the notebook using dbutils.widgets.get("myparam")
    :type notebook_params: dict
    :param python_script_path: The path to the python script in the DBFS or S3.
    :type python_script_path: str
    :param python_script_params: Parameters for the python script (list of str).
    :type python_script_params: list
    :param run_name: The name in Databricks for this run
    :type run_name: str
    :param timeout_seconds: Timeout for the Databricks run
    :type timeout_seconds: int
    :param maven_libraries: maven libraries for the Databricks run
    :type maven_libraries: list[azureml.pipeline.steps.databricks.MavenLibrary]
    :param pypi_libraries: pypi libraries for the Databricks run
    :type pypi_libraries: list[azureml.pipeline.steps.databricks.PyPiLibrary]
    :param egg_libraries: egg libraries for the Databricks run
    :type egg_libraries: list[azureml.pipeline.steps.databricks.EggLibrary]
    :param jar_libraries: jar libraries for the Databricks run
    :type jar_libraries: list[azureml.pipeline.steps.databricks.JarLibrary]
    :param rcran_libraries: rcran libraries for the Databricks run
    :type rcran_libraries: list[azureml.pipeline.steps.databricks.RCranLibrary]
    :param databricks_compute: Azure Databricks compute
    :type databricks_compute: azureml.core.compute.databricks.DatabricksCompute
    :param databricks_compute_name: Name of Azure Databricks compute
    :type databricks_compute_name: str
    :param allow_reuse: Whether the step should reuse previous results when run with the same settings/inputs
    :type allow_reuse: bool
    :param version: Optional version tag to denote a change in functionality for the step
    :type version: str
    """

    def __init__(self, name, inputs=None, outputs=None, spark_version=None, node_type=None,
                 num_workers=None, autoscale=None, spark_env_variables=None, notebook_path=None, notebook_params=None,
                 python_script_path=None, python_script_params=None, run_name=None, timeout_seconds=None,
                 maven_libraries=None, pypi_libraries=None, egg_libraries=None, jar_libraries=None,
                 rcran_libraries=None, databricks_compute=None, databricks_compute_name=None,
                 allow_reuse=True, version=None):
        """
        Add a DataBricks notebook or a python script on DBFS as a node.

        :param name: Name of the step
        :type name: str
        :param inputs: List of input connections for data consumed by this step. Fetch this inside the notebook
                        using dbutils.widgets.get("<input name>")
        :type inputs: [InputPortBinding, DataReference, PortDataReference, PipelineData]
        :param outputs: List of output port definitions for outputs produced by this step. Fetch this inside the
                        notebook using dbutils.widgets.get("<output name>")
        :type outputs: [OutputPortBinding, PipelineData]
        :param spark_version: The version of spark for the Databricks run cluster. Example: "4.0.x-scala2.11"
        :type spark_version: str
        :param node_type: The Azure vm node types for the Databricks run cluster. Example: "Standard_D3_v2"
        :type node_type: str
        :param num_workers: The number of workers for the Databricks run cluster
        :type num_workers: int
        :param autoscale: The autoscale configuration for the Databricks run cluster
        :type autoscale: AutoScale
        :param spark_env_variables: The spark environment variables for the Databricks run cluster
        :type spark_env_variables: {str:str}
        :param notebook_path: The path to the notebook in the Databricks instance
        :type notebook_path: str
        :param notebook_params: Parameters  for the Databricks notebook (dictionary of {str:str}). Fetch this inside
                                the notebook using dbutils.widgets.get("myparam")
        :type notebook_params: {str:str}
        :param python_script_path: The path to the python script in the DBFS or S3.
        :type python_script_path: str
        :param python_script_params: Parameters for the python script (list of str).
        :type python_script_params: list(str)
        :param run_name: The name in Databricks for this run
        :type run_name: str
        :param timeout_seconds: Timeout for the Databricks run
        :type timeout_seconds: int
        :param maven_libraries: maven libraries for the Databricks run
        :type maven_libraries: [MavenLibrary]
        :param pypi_libraries: pypi libraries for the Databricks run
        :type pypi_libraries: [PyPiLibrary]
        :param egg_libraries: egg libraries for the Databricks run
        :type egg_libraries: [EggLibrary]
        :param jar_libraries: jar libraries for the Databricks run
        :type jar_libraries: [JarLibrary]
        :param rcran_libraries: rcran libraries for the Databricks run
        :type rcran_libraries: [RCranLibrary]
        :param databricks_compute: Azure Databricks compute
        :type databricks_compute: DatabricksCompute
        :param databricks_compute_name: Name of Azure Databricks compute
        :type databricks_compute_name: str
        :param allow_reuse: Whether the step should reuse previous results when run with the same settings/inputs
        :type allow_reuse: bool
        :param version: Optional version tag to denote a change in functionality for the step
        :type version: str
        """
        if spark_env_variables is None:
            spark_env_variables = {'PYSPARK_PYTHON': '/databricks/python3/bin/python3'}
        if maven_libraries is None:
            maven_libraries = []
        if pypi_libraries is None:
            pypi_libraries = []
        if egg_libraries is None:
            egg_libraries = []
        if jar_libraries is None:
            jar_libraries = []
        if rcran_libraries is None:
            rcran_libraries = []
        if name is None:
            raise ValueError("name is required")
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if spark_version is None:
            spark_version = "4.0.x-scala2.11"
        if not isinstance(spark_version, str):
            raise ValueError("spark_version must be a string")
        if node_type is None:
            node_type = "Standard_D3_v2"
        if not isinstance(node_type, str):
            raise ValueError("node_type must be a string")
        if num_workers is None and autoscale is None:
            raise ValueError("one of num_workers or AutoScale is required")
        if num_workers is not None and autoscale is not None:
            raise ValueError("exactly one of num_workers or AutoScale is required")
        if num_workers is not None and not isinstance(num_workers, int):
            raise ValueError("num_workers must be an int")
        if autoscale is not None and not isinstance(autoscale, AutoScale):
            raise ValueError("autoscale must be an AutoScale")
        if notebook_path is None and (notebook_params is not None or python_script_path is None):
            raise ValueError("notebook_path or python_script_path is required")
        elif notebook_path is not None and not isinstance(notebook_path, str):
            raise ValueError("notebook_path must be a string")
        if python_script_path is None and (python_script_params is not None or notebook_path is None):
            raise ValueError("notebook_path or python_script_path is required")
        elif python_script_path is not None and not isinstance(python_script_path, str):
            raise ValueError("python_script_path must be a string")
        if notebook_path is not None and notebook_params is None:
            notebook_params = {}
        if python_script_path is not None and python_script_params is None:
            python_script_params = []
        if databricks_compute is None and databricks_compute_name is None:
            raise ValueError('either databricks_compute or databricks_compute_name is required')
        elif databricks_compute is not None and databricks_compute_name is not None:
            raise ValueError('cannot specify both databricks_compute and databricks_compute_name')

        self._databricks_compute = databricks_compute
        self._databricks_compute_name = databricks_compute_name
        self._allow_reuse = allow_reuse
        self._version = version
        self._params = dict()

        # add params
        if timeout_seconds is not None:
            if not isinstance(timeout_seconds, int):
                raise ValueError("timeout_seconds must be an int")
            self._params["timeout_seconds"] = timeout_seconds
        if run_name is not None:
            if not isinstance(run_name, str):
                raise ValueError("run_name must be a string")
            self._params["run_name"] = run_name
        self._params["spark_version"] = spark_version
        self._params["node_type_id"] = node_type
        if num_workers is not None:
            self._params["num_workers"] = num_workers
        else:
            self._params["max_workers"] = autoscale.max_workers
            self._params["min_workers"] = autoscale.min_workers
        self._params["spark_env_vars"] = ";".join('{0}={1}'.format(key, value) for key, value in
                                                  spark_env_variables.items())
        if notebook_path is not None:
            self._params["notebook_path"] = notebook_path
            parameters = ";".join('{0}={1}'.format(key, value) for key, value in notebook_params.items())
            if parameters is not "":
                self._params["base_parameters"] = parameters

        if python_script_path is not None:
            self._params["python_script_path"] = python_script_path
            self._params["python_script_params"] = self._encode_python_params(python_script_params)

        j_libraries = ",".join(j.library for j in jar_libraries)
        if j_libraries is not "":
            self._params["jar_libraries"] = j_libraries
        e_libraries = ",".join(e.library for e in egg_libraries)
        if e_libraries is not "":
            self._params["egg_libraries"] = e_libraries
        p_libraries = ";".join('package={0}|repo={1}'.format(p.package, p.repo) for p in pypi_libraries)
        if p_libraries is not "":
            self._params["pypi_libraries"] = p_libraries
        r_libraries = ";".join('package={0}|repo={1}'.format(r.package, r.repo) for r in rcran_libraries)
        if r_libraries is not "":
            self._params["rcran_libraries"] = r_libraries
        m_libraries = ";".join('coordinates={0}|repo={1}|exclusions={2}'
                               .format(m.coordinates, m.repo, ",".join(m.exclusions))for m in maven_libraries)
        if m_libraries is not "":
            self._params["maven_libraries"] = m_libraries

        if self._databricks_compute_name is not None:
            self._params["compute_name"] = self._databricks_compute_name
        else:
            self._params["compute_name"] = self._databricks_compute.name

        self._pipeline_params_in_step_params = PipelineStep._get_pipeline_parameters_step_params(self._params)

        super().__init__(name, inputs, outputs)

    def __str__(self):
        """
        __str__ override.

        :return: str representation of the Databricks step.
        :rtype: str
        """
        result = "DatabricksStep_{0}".format(self.name)
        return result

    def __repr__(self):
        """
        Return __str__.

        :return: str representation of the Databricks step.
        :rtype: str
        """
        return self.__str__()

    def create_node(self, graph, default_datastore_name, context):
        """
        Create a node from this Databricks step and add to the given graph.

        :param graph: The graph object to add the node to.
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_datastore_name: The default datastore name to use.
        :type default_datastore_name: str
        :param context: The graph context.
        :type context: _GraphContext

        :return: The created node.
        :rtype: azureml.pipeline.core.graph.Node
        """
        input_bindings, output_bindings = self.create_input_output_bindings(self._inputs, self._outputs,
                                                                            default_datastore_name)

        param_defs = []
        for param_name in self._params:
            is_metadata_param = param_name != "notebook_path" and \
                param_name != "base_parameters" and \
                param_name != "python_script_path" and \
                param_name != "python_script_params"

            param_defs.append(ParamDef(param_name, self._params[param_name],
                                       is_metadata_param=is_metadata_param))

        module_def = self.create_module_def(execution_type="databrickscloud", input_bindings=input_bindings,
                                            output_bindings=output_bindings, param_defs=param_defs,
                                            allow_reuse=self._allow_reuse, version=self._version)
        module_builder = _InterfaceModuleBuilder(
            context=context,
            module_def=module_def)
        node = graph.add_module_node(name=self.name, input_bindings=input_bindings, output_bindings=output_bindings,
                                     param_bindings=self._params, module_builder=module_builder)
        PipelineStep.\
            _configure_pipeline_parameters(graph, node,
                                           pipeline_params_in_step_params=self._pipeline_params_in_step_params)
        return node

    @staticmethod
    def _encode_python_params(params_list):
        r"""
        Convert a list of strings to a string.

        Replace every instance of \| with \|- then join all strings using \|\|.
        Eg. ["arg1", "arg\|2"] -> "arg1\|\|arg\|-2".

        :param params_list: List of parameters
        :type params_list: list(str)

        :return: Encoded string
        :rtype: str
        """
        params_list = [param.replace("|", "|-") for param in params_list]
        return "||".join(params_list)
