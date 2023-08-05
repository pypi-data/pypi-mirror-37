# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""_aeva_provider.py, module for creating/downloading module/datasource,
creating/submitting experiments, fetching for experiment status,
retrieving outputs and logs, creating/using published pipelines.
"""
from ._workflow_provider import _PublishedPipelineProvider
from ._workflow_provider import _ModuleProvider, _GraphProvider, _DataSourceProvider, _DataTypeProvider
from ._workflow_provider import _PipelineRunProvider, _StepRunProvider, _PortDataReferenceProvider
from .graph import ModuleDef, Module, ParamDef, InputPortDef, OutputPortDef
from .graph import DataSource, DataSourceDef, PublishedPipeline, PortDataReference
from .graph import Graph, Node, DataType, PipelineParameter
from .run import StepRunOutput
from azureml._base_sdk_common.create_snapshot import create_snapshot
from azureml._base_sdk_common.project_context import create_project_context
from azureml._base_sdk_common.service_discovery import get_pipelines_url
from azureml.data.data_reference import DataReference
from azureml.core import Datastore
from azureml.pipeline.core._restclients.aeva.models import ExperimentCreationInfo, ExperimentCreationInfoWithGraph
from azureml.pipeline.core._restclients.aeva.models import GraphEntity, GraphModuleNode, GraphEdge, \
    ModuleCreationInfo, EntityInterface, Parameter
from azureml.pipeline.core._restclients.aeva.models import ParameterAssignment, PortInfo, StructuredInterface
from azureml.pipeline.core._restclients.aeva.models import StructuredInterfaceInput, StructuredInterfaceOutput
from azureml.pipeline.core._restclients.aeva.models import StructuredInterfaceParameter, DataSourceCreationInfo
from azureml.pipeline.core._restclients.aeva.models import TemplateCreationInfo, DataTypeCreationInfo
from azureml.pipeline.core._restclients.aeva.models import GraphDatasetNode, OutputSetting
from azureml.pipeline.core._restclients.aeva.service_caller import AE3PServiceCaller


class _AevaModuleSnapshotUploader(object):
    """
    _AevaModuleSnapshotUploader.
    """

    def __init__(self, workspace):
        """Initialize _AevaModuleSnapshotUploader.
        :param workspace: workspace object
        :type workspace: Workspace
        """
        self._workspace = workspace

    def upload(self, experiment_name, directory):
        """Creates a project and snapshot, and return a storage id.
        :param experiment_name: experiment name
        :type experiment_name: str
        :param directory: directory
        :type directory: str
        """
        auth = self._workspace._auth_object
        project_context = create_project_context(auth, subscription_id=self._workspace.subscription_id,
                                                 resource_group=self._workspace.resource_group,
                                                 workspace=self._workspace.name,
                                                 project_name=experiment_name)

        storage_id = create_snapshot(directory, project_context)

        return storage_id


class _AevaWorkflowProvider(object):
    """
    _AevaWorkflowProvider.
    """
    def __init__(self, service_caller, module_uploader, workspace=None):
        """Initialize _AevaWorkflowProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        :param module_uploader: module uploader object
        :type module_uploader: _AevaModuleSnapshotUploader
        :param workspace: workspace object
        :type workspace: Workspace
        """
        self.graph_provider = _AevaGraphProvider(service_caller)
        self.datasource_provider = _AevaDataSourceProvider(service_caller)
        self.module_provider = _AevaModuleProvider(service_caller, module_uploader)
        self.step_run_provider = _AevaStepRunProvider(service_caller)
        self.pipeline_run_provider = _AevaPipelineRunProvider(service_caller, self.step_run_provider)
        self.published_pipeline_provider = _AevaPublishedPipelineProvider(service_caller)
        self.port_data_reference_provider = _AevaPortDataReferenceProvider(workspace)
        self.datatype_provider = _AevaDataTypeProvider(service_caller)
        self._service_caller = service_caller

    @staticmethod
    def create_provider(workspace, experiment_name, service_endpoint=None):
        """Creates a workflow provider.
        :param workspace: workspace object
        :type workspace: Workspace
        :param experiment_name: experiment name
        :type experiment_name: str
        :param service_endpoint: service endpoint
        :type service_endpoint: str
        """
        service_caller = _AevaWorkflowProvider.create_service_caller(workspace=workspace,
                                                                     experiment_name=experiment_name,
                                                                     service_endpoint=service_endpoint)
        module_uploader = _AevaModuleSnapshotUploader(workspace)
        return _AevaWorkflowProvider(service_caller, module_uploader, workspace)

    @staticmethod
    def create_service_caller(workspace, experiment_name, service_endpoint=None):
        """Creates a service caller.
        :param workspace: workspace object
        :type workspace: Workspace
        :param experiment_name: experiment name
        :type experiment_name: str
        :param service_endpoint: service endpoint
        :type service_endpoint: str
        """
        if service_endpoint is None:
            service_endpoint = _AevaWorkflowProvider.get_endpoint_url(workspace, experiment_name)

        service_caller = AE3PServiceCaller(
            base_url=service_endpoint,
            workspace=workspace)

        return service_caller

    @staticmethod
    def get_endpoint_url(workspace, experiment_name):
        """Gets an endpoint url.
        :param workspace: workspace object
        :type workspace: Workspace
        :param experiment_name: experiment name
        :type experiment_name: str
        """
        auth = workspace._auth_object
        project_context = create_project_context(auth, subscription_id=workspace.subscription_id,
                                                 resource_group=workspace.resource_group,
                                                 workspace=workspace.name,
                                                 project_name=experiment_name)
        account_scope = project_context.get_workspace_uri_path()

        return get_pipelines_url(auth, account_scope)


class _AevaModuleProvider(_ModuleProvider):
    """
    _AevaModuleProvider.
    """

    def __init__(self, service_caller, module_uploader):
        """Initialize _AevaModuleProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        :param module_uploader: module uploader object
        :type module_uploader: _AevaModuleSnapshotUploader
        """
        self._service_caller = service_caller
        self._module_uploader = module_uploader

    def create_module(self, module_def, content_path=None, fingerprint=None):
        """Creates a module, and returns a module entity id.
        :param module_def: module def
        :type module_def: ModuleDef
        :param content_path: directory
        :type content_path: str
        :param fingerprint: fingerprint
        :type fingerprint: str
        """
        interface = StructuredInterface(command_line_pattern='', inputs=[], outputs=[], parameters=[],
                                        metadata_parameters=[])

        interface.inputs = []
        for input in module_def.input_port_defs:
            skip_processing = input.name.startswith(ModuleDef.fake_input_prefix)
            interface.inputs.append(StructuredInterfaceInput(name=input.name, label=input.name,
                                                             data_type_ids_list=input.datatypes,
                                                             is_optional=input.is_optional,
                                                             data_store_mode=input.default_datastore_mode,
                                                             path_on_compute=input.default_path_on_compute,
                                                             overwrite=input.default_overwrite,
                                                             data_reference_name=input.default_data_reference_name,
                                                             skip_processing=skip_processing))

        interface.outputs = []
        for output in module_def.output_port_defs:
            skip_processing = output.name.startswith(ModuleDef.fake_output_name)
            interface.outputs.append(StructuredInterfaceOutput(name=output.name, label=output.name,
                                                               data_type_id=output.datatype,
                                                               data_store_name=output.default_datastore_name,
                                                               data_store_mode=output.default_datastore_mode,
                                                               path_on_compute=output.default_path_on_compute,
                                                               overwrite=output.default_overwrite,
                                                               data_reference_name=output.name,
                                                               skip_processing=skip_processing))

        for param in module_def.param_defs:
            structured_param = StructuredInterfaceParameter(name=param.name, parameter_type='String',
                                                            is_optional=param.is_optional,
                                                            default_value=param.default_value,
                                                            set_environment_variable=param.set_env_var,
                                                            environment_variable_override=param.env_var_override)
            if param.is_metadata_param:
                interface.metadata_parameters.append(structured_param)
            else:
                interface.parameters.append(structured_param)

        creation_info = ModuleCreationInfo(name=module_def.name, description=module_def.description,
                                           is_deterministic=module_def.allow_reuse,
                                           module_execution_type=module_def.module_execution_type,
                                           structured_interface=interface, identifier_hash=fingerprint)

        module_entity = self._service_caller.create_module_async(creation_info=creation_info)

        if content_path is not None:
            storage_id = self._module_uploader.upload(experiment_name=module_entity.id, directory=content_path)
            module_entity.data_location.storage_id = storage_id

        module_entity.upload_state = 1
        self._service_caller.update_module_async(module_entity.id, module_entity)

        return module_entity.id

    def download(self, module_id):
        """Downloads a module.
        :param module_id: module id
        :type module_id: str
        """
        module_info = self._service_caller.get_module_async(id=module_id)
        return _AevaModuleProvider.from_module_info(module_info)

    def find_module_by_fingerprint(self, fingerprint):
        """Search module by fingerprint.
        :param fingerprint: fingerprint
        :type fingerprint: str
        """
        module_info = self._service_caller.try_get_module_by_hash_async(fingerprint)
        if module_info is None:
            return None

        return _AevaModuleProvider.from_module_info(module_info)

    @staticmethod
    def from_module_info(module_info):
        """Returns a module object with a given module info.
        :param module_info: module info
        :type module_info: ModuleInfo
        """
        entity_interface = module_info.interface
        module_entity = module_info.data

        # Populate a ModuleDef based on the entity/interface
        param_defs = []
        for parameter in entity_interface.parameters:
            param_defs.append(
                ParamDef(name=parameter.name, default_value=parameter.default_value, is_metadata_param=False))
        for parameter in entity_interface.metadata_parameters:
            param_defs.append(
                ParamDef(name=parameter.name, default_value=parameter.default_value, is_metadata_param=True))

        structured_inputs = {}
        for structured_input in module_entity.structured_interface.inputs:
            structured_inputs[structured_input.name] = structured_input
        input_port_defs = []
        for input_port in entity_interface.ports.inputs:
            structured_input = structured_inputs[input_port.name]
            input_port_defs.append(
                InputPortDef(name=input_port.name, datatypes=input_port.data_types_ids,
                             default_path_on_compute=structured_input.path_on_compute,
                             default_datastore_mode=structured_input.data_store_mode,
                             default_overwrite=structured_input.overwrite,
                             default_data_reference_name=structured_input.data_reference_name)
            )

        structured_outputs = {}
        for structured_output in module_entity.structured_interface.outputs:
            structured_outputs[structured_output.name] = structured_output
        output_port_defs = []
        for output_port in entity_interface.ports.outputs:
            structured_output = structured_outputs[output_port.name]
            output_port_defs.append(
                OutputPortDef(name=output_port.name, default_datastore_name=structured_output.data_store_name,
                              default_datastore_mode=structured_output.data_store_mode,
                              default_path_on_compute=structured_output.path_on_compute,
                              is_directory=(structured_output.data_type_id == "AnyDirectory"),
                              datatype=structured_output.data_type_id, default_overwrite=structured_output.overwrite)
            )

        module_def = ModuleDef(name=module_entity.name,
                               description=module_entity.description,
                               input_port_defs=input_port_defs,
                               output_port_defs=output_port_defs,
                               param_defs=param_defs,
                               allow_reuse=module_entity.is_deterministic)

        return Module(module_id=module_entity.id, module_def=module_def)


class _AevaDataSourceProvider(_DataSourceProvider):
    """
    _AevaDataSourceProvider.
    """

    def __init__(self, service_caller):
        """Initialize _AevaDataSourceProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        """
        self._service_caller = service_caller

    def upload(self, datasource_def, fingerprint=None):
        """Upload a datasource, and returns a datasource entity id.
        :param datasource_def:datasource def
        :type datasource_def: DatasourceDef
        :param fingerprint: fingerprint
        :type fingerprint: str
        """
        creation_info = DataSourceCreationInfo(name=datasource_def.name,
                                               data_type_id=datasource_def.data_type_id,
                                               description=datasource_def.description,
                                               data_store_name=datasource_def.datastore_name,
                                               path_on_data_store=datasource_def.path_on_datastore,
                                               identifier_hash=fingerprint)

        datasource_entity = self._service_caller.create_datasource_async(creation_info=creation_info)
        return datasource_entity.id

    def download(self, datasource_id):
        """Download a datasource, and returns a _AevaDataSourceProvider.
        :param datasource_id:datasource id
        :type datasource_id: str
        """
        datasource_entity = self._service_caller.get_datasource_async(id=datasource_id)
        return _AevaDataSourceProvider.from_datasource_entity(datasource_entity)

    def find_datasource_by_fingerprint(self, fingerprint):
        """Search datasource with a given fingerprint, returns a _AevaDataSourceProvider.
        :param fingerprint: fingerprint
        :type fingerprint: str
        """
        datasource_entity = self._service_caller.try_get_datasource_by_hash_async(fingerprint)
        if datasource_entity is None:
            return None

        return _AevaDataSourceProvider.from_datasource_entity(datasource_entity)

    @staticmethod
    def from_datasource_entity(datasource_entity):
        """Returns a Datasource with a given datasource entity.
        :param datasource_entity: datasource entity
        :type datasource_entity: DataSourceEntity
        """
        datasource_def = DataSourceDef(datasource_entity.name,
                                       description=datasource_entity.description,
                                       data_type_id=datasource_entity.data_type_id)

        if datasource_entity.data_location is not None and datasource_entity.data_location.data_reference is not None:
            type = datasource_entity.data_location.data_reference.type
            if type == '1':
                data_reference = datasource_entity.data_location.data_reference.azure_blob_reference
            elif type == '2':
                data_reference = datasource_entity.data_location.data_reference.azure_data_lake_reference
            elif type == '3':
                data_reference = datasource_entity.data_location.data_reference.azure_files_reference
            else:
                raise ValueError("Unsupported datasource data reference type")
            datasource_def.path_on_datastore = data_reference.relative_path
            datasource_def.datastore_name = data_reference.aml_data_store_name

        return DataSource(datasource_entity.id, datasource_def)


class _AevaGraphProvider(_GraphProvider):
    """
    _AevaGraphProvider.
    """

    def __init__(self, service_caller):
        """Initialize _AevaGraphProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        """
        self._service_caller = service_caller

    def submit(self, graph, pipeline_parameters, continue_on_step_failure, experiment_name):
        """Submit an experiment.
        :param graph: graph
        :type graph: Graph
        :param pipeline_parameters: Parameters to pipeline execution
        :type pipeline_parameters: dict
        :param continue_on_step_failure: continue on step failure
        :type continue_on_step_failure: bool
        :param experiment_name: experiment name
        :type experiment_name: str
        """
        created_experiment_id = self.create_experiment(graph=graph, pipeline_parameters=pipeline_parameters,
                                                       continue_on_step_failure=continue_on_step_failure,
                                                       experiment_name=experiment_name)
        self._service_caller.submit_saved_experiment_async(created_experiment_id)
        print('Submitted experiment id:', created_experiment_id)

        return created_experiment_id

    def create_experiment(self, graph, pipeline_parameters, continue_on_step_failure, experiment_name):
        """Create an unsubmitted experiment.
        :param graph: graph
        :type graph: Graph
        :param pipeline_parameters: Parameters to pipeline execution
        :type pipeline_parameters: dict
        :param continue_on_step_failure: continue on step failure
        :type continue_on_step_failure: bool
        :param experiment_name: experiment name
        :type experiment_name: str
        """
        aeva_graph = _AevaGraphProvider._build_graph(graph)
        graph_parameter_assignment = _AevaGraphProvider._get_parameter_assignments(graph, pipeline_parameters)

        experiment_submission = ExperimentCreationInfoWithGraph()
        experiment_submission.creation_info = \
            ExperimentCreationInfo(description=graph._name,
                                   parameter_assignments=graph_parameter_assignment,
                                   continue_experiment_on_node_failure=continue_on_step_failure,
                                   experiment_name=experiment_name)
        experiment_submission.graph = aeva_graph
        graph_interface = _AevaGraphProvider._get_graph_interface(graph)
        experiment_submission.graph_interface = graph_interface
        _AevaGraphProvider._validate_parameter_types(pipeline_parameters, graph_interface)

        created_experiment = self._service_caller.create_unsubmitted_experiment_async(experiment_submission)

        return created_experiment.id

    @staticmethod
    def _validate_parameter_types(pipeline_parameters, graph_interface):
        if pipeline_parameters is not None:
            for graph_interface_param in graph_interface.parameters:
                if graph_interface_param.name in pipeline_parameters:
                    param_type = _AevaGraphProvider.\
                        _get_backend_param_type_code(pipeline_parameters[graph_interface_param.name])
                    if param_type != graph_interface_param.type:
                        graph_interface_param_type_name = \
                            _AevaGraphProvider._get_sdk_param_type_name(graph_interface_param.type)
                        param_value = pipeline_parameters[graph_interface_param.name]
                        param_value_type = type(param_value).__name__
                        raise Exception('Expected type of the pipeline parameter {0} is {1}, but the value '
                                        '{2} provided is of type {3}'.format(graph_interface_param.name,
                                                                             graph_interface_param_type_name,
                                                                             str(param_value),
                                                                             param_value_type))

    def create_graph_from_run(self, context, pipeline_run_id):
        """Creates the graph from the pipeline_run_id.
        :param context: context object
        :type context: _GraphContext
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        """
        experiment = self._service_caller.get_experiment_async(pipeline_run_id)
        graph_entity = self._service_caller.get_graph_async(experiment.graph_id)

        graph = Graph(name=experiment.description, context=context)

        # add modules
        for module_node in graph_entity.module_nodes:
            node_id = module_node.id

            module_info = self._service_caller.get_module_async(module_node.module_id)

            module = _AevaModuleProvider.from_module_info(module_info)

            node = Node(graph=graph, name=module_info.data.name, node_id=node_id, module=module)

            # set param value overrides
            for parameter in module_node.module_parameters:
                node.get_param(parameter.name).set_value(parameter.value)
            for parameter in module_node.module_metadata_parameters:
                node.get_param(parameter.name).set_value(parameter.value)

            graph._add_node_to_dicts(node)

        for datasource_node in graph_entity.dataset_nodes:
            node_id = datasource_node.id
            datasource_entity = self._service_caller.get_datasource_async(datasource_node.dataset_id)
            datasource = _AevaDataSourceProvider.from_datasource_entity(datasource_entity)
            node = Node(graph=graph, name=datasource_entity.name, node_id=node_id, datasource=datasource)
            graph._add_node_to_dicts(node)

        # add edges
        for edge in graph_entity.edges:
            input_port = graph._nodes[edge.destination_input_port.node_id].get_input(
                edge.destination_input_port.port_name)
            input_port.connect(graph._nodes[edge.source_output_port.node_id].get_output(
                edge.source_output_port.port_name))

        return graph

    @staticmethod
    def _get_parameter_assignments(aeva_graph, pipeline_params):
        param_assignment = {}
        if pipeline_params is not None:
            for param_name, param_value in pipeline_params.items():
                if param_name not in aeva_graph.params:
                    raise Exception('Assertion failure. Validation of pipeline_params should have failed')
                else:
                    # type of the param is preserved in EntityInterface
                    param_assignment[param_name] = str(pipeline_params[param_name])
        return param_assignment

    @staticmethod
    def _build_graph(graph):
        """
        Generate the graph entity to submit to the aeva backend.
        :return the graph entity
        :rtype GraphEntity
        """
        graph_entity = GraphEntity()
        graph_entity.sub_graph_nodes = []
        graph_entity.dataset_nodes = []
        graph_entity.module_nodes = []
        graph_entity.edges = []

        for node_id in graph._nodes:
            node = graph._nodes[node_id]

            if node._module is not None:
                module_node = GraphModuleNode(id=node_id, module_id=node._module.id)
                module_node.module_parameters = []
                module_node.module_metadata_parameters = []

                module_node.module_output_settings = []
                for output in node.outputs:
                    skip_processing = output.name.startswith(ModuleDef.fake_output_name)
                    if not skip_processing:
                        output_setting = OutputSetting(name=output.name, data_store_name=output.datastore_name,
                                                       data_store_mode=output.bind_mode,
                                                       path_on_compute=output.path_on_compute,
                                                       overwrite=output.overwrite,
                                                       data_reference_name=output.name)
                        module_node.module_output_settings.append(output_setting)

                # TODO:  Support node-level settings for inputs

                for param_name in node._params:
                    param = node.get_param(param_name)
                    value = param.value
                    # TODO: Use an enum for value_type
                    if isinstance(value, PipelineParameter):
                        # value is of type PipelineParameter, use its name property
                        # TODO parameter assignment expects 'Literal', 'GraphParameterName', 'Concatenate', 'Input'??
                        param_assignment = ParameterAssignment(name=param.name, value=value.name, value_type=1)
                    else:
                        param_assignment = ParameterAssignment(name=param.name, value=value, value_type=0)

                    if param.param_def.is_metadata_param:
                        module_node.module_metadata_parameters.append(param_assignment)
                    else:
                        module_node.module_parameters.append(param_assignment)

                graph_entity.module_nodes.append(module_node)

            elif node._datasource is not None:
                datasource_node = GraphDatasetNode(id=node_id, dataset_id=node._datasource.id)
                graph_entity.dataset_nodes.append(datasource_node)

        for edge in graph.edges:
            source = PortInfo(node_id=edge.source_port.node.node_id, port_name=edge.source_port.name)
            dest = PortInfo(node_id=edge.dest_port.node.node_id, port_name=edge.dest_port.name)
            graph_entity.edges.append(GraphEdge(source_output_port=source, destination_input_port=dest))

        return graph_entity

    @staticmethod
    def _get_backend_param_type_code(param_value):
        # ParameterType enum in the backend is Int=0, Double=1, Bool=2, String=3, Unidentified=4
        param_type_code = 4
        if isinstance(param_value, int):
            param_type_code = 0
        elif isinstance(param_value, float):
            param_type_code = 1
        elif isinstance(param_value, bool):
            param_type_code = 2
        elif isinstance(param_value, str):
            param_type_code = 3

        return param_type_code

    @staticmethod
    def _get_sdk_param_type_name(backend_param_type_code):
        # ParameterType enum in the backend is Int=0, Double=1, Bool=2, String=3, Unidentified=4
        param_type_code = 'Unidentified'
        if backend_param_type_code == 0:
            return int.__name__
        elif backend_param_type_code == 1:
            return float.__name__
        elif backend_param_type_code == 2:
            return bool.__name__
        elif backend_param_type_code == 3:
            return str.__name__

        return param_type_code

    @staticmethod
    def _get_graph_interface(graph):
        parameters = []
        for param_name, pipeline_param_value in graph.params.items():  # param is of type PipelineParameter
            param_type_code = _AevaGraphProvider._get_backend_param_type_code(pipeline_param_value.default_value)
            parameters.append(Parameter(name=param_name, default_value=pipeline_param_value.default_value,
                                        is_optional=True, type=param_type_code))
        return EntityInterface(parameters=parameters)


class _AevaPipelineRunProvider(_PipelineRunProvider):
    """
    _AevaPipelineRunProvider.
    """

    def __init__(self, service_caller, step_run_provider):
        """Initialize _AevaPipelineRunProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        :param step_run_provider: step run provider object
        :type step_run_provider: _AevaStepRunProvider
        """
        self._service_caller = service_caller
        self._step_run_provider = step_run_provider

    def get_status(self, pipeline_run_id):
        """
        Get the current status of the run
        :return current status
        :rtype str
        """
        result = self._service_caller.get_experiment_async(pipeline_run_id)

        if result.status is None:
            status_id = '0'
        else:
            status_id = result.status.status_code

        if status_id == '0':
            return "NotStarted"
        elif status_id == '1':
            return "Running"
        elif status_id == '2':
            return "Failed"
        elif status_id == '3':
            return "Finished"
        elif status_id == '4':
            return "Canceled"
        else:
            return "Unknown"

    def cancel(self, pipeline_run_id):
        """Cancel the run.
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        """
        self._service_caller.cancel_experiment_async(pipeline_run_id)

    def get_node_statuses(self, pipeline_run_id):
        """Gets the status of the node.
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        """
        return self._service_caller.get_all_nodes_in_level_status_async(pipeline_run_id)

    def get_pipeline_experiment_name(self, pipeline_run_id):
        """Gets experiment name.
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        """
        return self._service_caller.get_experiment_async(pipeline_run_id).run_history_experiment_name

    def get_runs_by_pipeline_id(self, pipeline_id):
        """Gets pipeline runs for a published pipeline ID.
        :param pipeline_id: published pipeline id
        :type pipeline_id: str
        :return List of tuples of (run id, experiment name)
        :rtype List
        """
        experiment_entities = self._service_caller.get_experiments_by_pipeline_id_async(pipeline_id)
        return [(experiment.id, experiment.run_history_experiment_name) for experiment in experiment_entities]


class _AevaStepRunProvider(_StepRunProvider):
    """
    _AevaStepRunProvider.
    """

    def __init__(self, service_caller):
        """Initialize _AevaStepRunProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        """
        self._service_caller = service_caller

    def get_status(self, pipeline_run_id, node_id):
        """
        Get the current status of the node run
        :return current status
        :rtype str
        """
        result = self._service_caller.get_node_status_code_async(pipeline_run_id, node_id)

        if result is None:
            status_id = '0'
        else:
            status_id = result

        # TODO: Can we make the status_ids of step_run and pipeline_run have same meaning?
        # For example, for Graph Run:
        # 0 = NotStarted, 1 = Running, 2 = Failed, 3 = Finished, and 4 = Canceled.
        # We could skip 1 for Graph Run and use 0, 2, 3, 4, and 5 for
        # NotStarted, Running, Failed, Finished, and Canceled.

        if status_id == '0':
            return "NotStarted"
        elif status_id == '1':
            return "Queued"
        elif status_id == '2':
            return "Running"
        elif status_id == '3':
            return "Failed"
        elif status_id == '4':
            return "Finished"
        elif status_id == '5':
            return "Canceled"
        elif status_id == '6':
            return "PartiallyExecuted"
        elif status_id == '7':
            return "Bypassed"
        else:
            return "Unknown"

    def get_run_id(self, pipeline_run_id, node_id):
        """Gets run id.
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        :param node_id: node id
        :type node_id: str
        """
        return self._service_caller.get_node_status_async(pipeline_run_id, node_id).run_id

    def get_job_log(self, pipeline_run_id, node_id):
        """Gets job log.
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        :param node_id: node id
        :type node_id: str
        """
        return self._service_caller.get_node_job_log_async(pipeline_run_id, node_id)

    def get_stdout_log(self, pipeline_run_id, node_id):
        """Gets stdout log.
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        :param node_id: node id
        :type node_id: str
        """
        return self._service_caller.get_node_stdout_log_async(pipeline_run_id, node_id)

    def get_stderr_log(self, pipeline_run_id, node_id):
        """Gets stderr log.
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        :param node_id: node id
        :type node_id: str
        """
        return self._service_caller.get_node_stderr_log_async(pipeline_run_id, node_id)

    def get_outputs(self, step_run, context, pipeline_run_id, node_id):
        """Gets outputs of experiment.
        :param step_run: step run object
        :type step_run: StepRun
        :param context: context object
        :type context: _GraphContext
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        :param node_id: node id
        :type node_id: str
        """
        node_outputs = self._service_caller.get_node_outputs_async(pipeline_run_id, node_id)

        output_port_runs = {}
        # remove fake completion output
        for node_output_name in node_outputs.keys():
            if node_output_name != ModuleDef.fake_output_name:
                output_port_runs[node_output_name] = StepRunOutput(context, pipeline_run_id, step_run,
                                                                   node_output_name, node_outputs[node_output_name])

        return output_port_runs

    def get_output(self, step_run, context, pipeline_run_id, node_id, name):
        """Gets an output of experiment.
        :param step_run: step run object
        :type step_run: StepRun
        :param context: context object
        :type context: _GraphContext
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        :param node_id: node id
        :type node_id: str
        :param name: name
        :type name: str
        """
        node_outputs = self._service_caller.get_node_outputs_async(pipeline_run_id, node_id)
        return StepRunOutput(context, pipeline_run_id, step_run, name, node_outputs[name])


class _AevaPublishedPipelineProvider(_PublishedPipelineProvider):
    """
    _AevaPublishedPipelineProvider.
    """

    def __init__(self, service_caller):
        """Initialize _AevaPublishedPipelineProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        """
        self._service_caller = service_caller

    def create_from_pipeline_run(self, name, description, version, pipeline_run_id):
        """Create a published pipeline from a run.
        :param name: name
        :type name: str
        :param description: description
        :type description: str
        :param version: version
        :type version: str
        :param pipeline_run_id: pipeline run id
        :type pipeline_run_id: str
        """
        creation_info = TemplateCreationInfo(name=name,
                                             description=description,
                                             experiment_id=pipeline_run_id,
                                             version=version)

        template_entity = self._service_caller.create_template_async(template_creation_info=creation_info)
        return _AevaPublishedPipelineProvider.from_template_entity(template_entity, self)

    def get_published_pipeline(self, published_pipeline_id):
        """Gets a published pipeline with a given published pipeline id.
        :param published_pipeline_id: published pipeline id
        :type published_pipeline_id: str
        """
        template_entity = self._service_caller.get_template_async(template_id=published_pipeline_id)
        return _AevaPublishedPipelineProvider.from_template_entity(template_entity, self)

    def submit(self, published_pipeline_id, experiment_name, parameter_assignment=None):
        """Submits an experiment with a given published pipeline id.
        :param published_pipeline_id: published pipeline id
        :type published_pipeline_id: str
        :param experiment_name: The experiment name
        :type experiment_name: str
        :param parameter_assignment: parameter assignment
        :type parameter_assignment: {str: str}
        """
        created_experiment = self._service_caller.submit_experiment_from_template_async(
            template_id=published_pipeline_id, experiment_name=experiment_name,
            parameter_assignment=parameter_assignment)
        return created_experiment.id

    def get_all(self, active_only=True):
        """
        Get all published pipelines in the current workspace

        :param workspace: The workspace the published pipeline was created on.
        :type workspace: azureml.core.Workspace
        :param active_only: If true, only return published pipelines which are currently active.
        :type active_only Bool
        :param _service_endpoint: The service endpoint.
        :type _service_endpoint: str

        :return: a list of :class:`azureml.pipeline.core.graph.PublishedPipeline`
        :rtype: list
        """
        entities = self._service_caller.get_all_published_pipelines(active_only=active_only)
        return [_AevaPublishedPipelineProvider.from_template_entity(entity, self) for entity in entities]

    @staticmethod
    def from_template_entity(template_entity, _pipeline_provider=None):
        """Returns a PublishedPipeline.
        :param template_entity: template entity
        :type template_entity: TemplateEntity
        :param _pipeline_provider: The published pipeline provider.
        :type _pipeline_provider: _PublishedPipelineProvider
        """
        status = AE3PServiceCaller.entity_status_from_enum(template_entity.entity_status)
        return PublishedPipeline(name=template_entity.name,
                                 description=template_entity.description,
                                 pipeline_run_id=template_entity.experiment_id,
                                 version=template_entity.version,
                                 published_pipeline_id=template_entity.id,
                                 status=status,
                                 _pipeline_provider=_pipeline_provider)

    def set_status(self, pipeline_id, new_status):
        """Set the status of the published pipeline ('Active', 'Deprecated', or 'Disabled').
        :param pipeline_id: published pipeline id
        :type pipeline_id: str
        :param new_status: The status to set
        :type new_status: str
        """
        self._service_caller.update_published_pipeline_status_async(pipeline_id=pipeline_id, new_status=new_status)


class _AevaPortDataReferenceProvider(_PortDataReferenceProvider):
    """
    _AevaPortDataReferenceProvider.
    """

    def __init__(self, workspace):
        """Initializes _AevaPortDataReferenceProvider.
        :param workspace: workspace
        :type workspace: Workspace
        """
        self._workspace = workspace

    def create_port_data_reference(self, output_run):
        """Creates a port data reference.
        :param output_run: output run
        :type output_run: output run
        """
        data_reference = None
        step_output = output_run.step_output

        if step_output.data_location is not None and step_output.data_location.data_reference is not None:
            type = step_output.data_location.data_reference.type
            if type == '1':
                data_location = step_output.data_location.data_reference.azure_blob_reference
            elif type == '2':
                data_location = step_output.data_location.data_reference.azure_data_lake_reference
            elif type == '3':
                data_location = step_output.data_location.data_reference.azure_files_reference
            else:
                raise ValueError("Unsupported output data reference type")
            datastore = Datastore(self._workspace, data_location.aml_data_store_name)
            data_reference = DataReference(datastore=datastore,
                                           data_reference_name=output_run.name,
                                           path_on_datastore=data_location.relative_path)

        return PortDataReference(context=output_run.context, pipeline_run_id=output_run.pipeline_run_id,
                                 data_reference=data_reference)

    def download(self, datastore_name, path_on_datastore, local_path, overwrite, show_progress):
        """download from datastore.
        :param datastore_name: datastore name
        :type datastore_name: str
        :param path_on_datastore: path on datastore
        :type path_on_datastore: str
        :param local_path: local path
        :type local_path: str
        :param overwrite: overwrite existing file
        :type overwrite: bool
        :param show_progress: show progress of download
        :type show_progress: bool
        """
        datastore = Datastore(self._workspace, datastore_name)

        return datastore.download(target_path=local_path, prefix=path_on_datastore, overwrite=overwrite,
                                  show_progress=show_progress)


class _AevaDataTypeProvider(_DataTypeProvider):
    """
    _AevaDataTypeProvider.
    """
    def __init__(self, service_caller):
        """Initialize _AevaDataTypeProvider.
        :param service_caller: service caller object
        :type service_caller: ServiceCaller
        """
        self._service_caller = service_caller

    def get_all_datatypes(self):
        """Get all data types."""
        entities = self._service_caller.get_all_datatypes_async()
        datatypes = [_AevaDataTypeProvider.from_datatype_entity(entity) for entity in entities]
        return datatypes

    def create_datatype(self, id, name, description, is_directory=False, parent_datatype_ids=[]):
        """Create a datatype.
        :param id: id
        :type id: str
        :param name: name
        :type name: str
        :param description: description
        :type description: str
        :param is_directory: is directory
        :type is_directory: bool
        :param parent_datatype_ids: parent datatype ids
        :type parent_datatype_ids: list[str]
        """
        creation_info = DataTypeCreationInfo(id=id, name=name, description=description,
                                             is_directory=is_directory,
                                             parent_data_type_ids=parent_datatype_ids)
        entity = self._service_caller.create_datatype_async(creation_info)
        return _AevaDataTypeProvider.from_datatype_entity(entity)

    def ensure_default_datatypes(self):
        """Checks if the datatype exists or not.  Creates one if not."""
        ids = [datatype.id for datatype in self.get_all_datatypes()]

        required_file_types = ['AnyFile', 'AzureBlobReference', 'AzureDataLakeReference']
        required_directory_types = ['AnyDirectory']

        for file_type in required_file_types:
            if file_type not in ids:
                self.create_datatype(id=file_type, name=file_type, description=file_type, is_directory=False)
        for dir_type in required_directory_types:
            if dir_type not in ids:
                self.create_datatype(id=dir_type, name=dir_type, description=dir_type, is_directory=True)

    @staticmethod
    def from_datatype_entity(datatype_entity):
        """Create a datatype.
        :param datatype_entity: datatype entity
        :type datatype_entity: DataTypeEntity
        """
        return DataType(id=datatype_entity.id, name=datatype_entity.name,
                        description=datatype_entity.description, is_directory=datatype_entity.is_directory,
                        parent_datatype_ids=datatype_entity.parent_data_type_ids)
