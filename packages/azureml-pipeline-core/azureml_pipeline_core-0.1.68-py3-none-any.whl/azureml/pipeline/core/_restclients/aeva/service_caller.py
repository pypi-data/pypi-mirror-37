# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""service_calller.py, module for interacting with the AzureML service."""

from .ae3_pservice_api10 import AE3PServiceAPI10
from .service_caller_base import AE3PServiceCallerBase
from .models import ErrorResponseException


class AE3PServiceCaller(AE3PServiceCallerBase):
    """AE3PServiceCaller.
    :param base_url: base url
    :type base_url: Service URL
    :param subscription_id: subscription id
    :type subscription_id: str
    :param resource_group_name: resource group name
    :type resource_group_name: str
    :param workspace_name: workspace name
    :type workspace_name: str
    """
    def __init__(self, base_url, workspace):
        """Initializes AE3PServiceCaller."""
        self._service_endpoint = base_url
        self._caller = AE3PServiceAPI10(base_url=base_url)
        self._subscription_id = workspace.subscription_id
        self._resource_group_name = workspace.resource_group
        self._workspace_name = workspace.name
        self.auth = workspace._auth_object

    def _get_custom_headers(self):
        return self.auth.get_authentication_header()

    def create_datasource_async(self, creation_info):
        """CreateDataSourceAsync.

        :param creation_info: The datasource creation info
        :type creation_info: ~swaggerfixed.models.DataSourceCreationInfo
        :return: DatasetEntity
        :rtype: ~swaggerfixed.models.DatasetEntity
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_data_sources_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(), creation_info=creation_info)

        return result

    def update_datasource_async(self, id, updated):
        """UpdateDataSourceAsync.

        :param id: The datasource id
        :type id: str
        :param updated: The updated datasource
        :type updated: ~swaggerfixed.models.DataSourceEntity
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """

        self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_data_sources_by_data_source_id_put(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            data_source_id=id, updated=updated)

    def get_datasource_async(self, id):
        """GetDataSourceAsync.

        :param id: The datasource id
        :type id: str
        :return: DatasetEntity
        :rtype: ~swaggerfixed.models.DatasetEntity
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_data_sources_by_id_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            id=id)

        return result

    def get_module_async(self, id):
        """GetModuleAsync.

        :param id: The module id
        :type id: str
        :return: Module
        :rtype: ~swaggerfixed.models.Module
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_modules_by_id_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(), id=id)

        return result

    def create_module_async(self, creation_info):
        """CreateModuleAsync.

        :param creation_info: The module creation info
        :type creation_info: ~swaggerfixed.models.ModuleCreationInfo
        :return: ModuleEntity
        :rtype: ~swaggerfixed.models.ModuleEntity
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_modules_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(), creation_info=creation_info)

        return result

    def update_module_async(self, id, updated):
        """UpdateModuleAsync.

        :param id: The module id
        :type id: str
        :param updated: The updated module
        :type updated: ~swaggerfixed.models.ModuleEntity
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_modules_by_id_put(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, id=id, updated=updated, custom_headers=self._get_custom_headers())

        return result

    def create_unsubmitted_experiment_async(self, creation_info_with_graph):
        """CreateUnsubmittedExperimentWithGraphAsync.

        :param creation_info_with_graph: The experiment creation info
        :type creation_info_with_graph:
         ~swaggerfixed.models.ExperimentCreationInfoWithGraph
        :return: ExperimentEntity
        :rtype: ~swaggerfixed.models.ExperimentEntity
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_unsubmitted_creation_info_with_graph_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            creation_info_with_graph=creation_info_with_graph, experiment_name=creation_info_with_graph.creation_info.experiment_name)

        return result

    def submit_saved_experiment_async(self, experiment_id):
        """SubmitSavedExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """

        self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_submit_by_experiment_id_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(), experiment_id=experiment_id)

    def get_experiment_async(self, experiment_id):
        """GetExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: ExperimentEntity
        :rtype: ~swaggerfixed.models.ExperimentEntity
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(), experiment_id=experiment_id)

        return result

    def cancel_experiment_async(self, experiment_id):
        """CencelExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_execution_delete(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, custom_headers=self._get_custom_headers())

    def get_graph_async(self, graph_id):
        """GetGraphAsync

        :param graph_id: The graph id
        :type graph_id: str
        :return: GraphEntity
        :rtype: ~swaggerfixed.models.GraphEntity
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_graphs_by_graph_id_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, graph_id=graph_id, custom_headers=self._get_custom_headers())

        return result

    def get_node_status_code_async(self, experiment_id, node_id):
        """GetNodeStatusCodeAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node status code
        :rtype: StatusCode
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_graph_node_status_code_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, node_id_path=[node_id],
            custom_headers=self._get_custom_headers())

        return result

    def get_node_status_async(self, experiment_id, node_id):
        """GetNodeStatusAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node status
        :rtype: TaskStatus
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_graph_node_status_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, node_id_path=[node_id],
            custom_headers=self._get_custom_headers())

        return result

    def get_all_nodes_in_level_status_async(self, experiment_id):
        """GetAllNodesInLevelStatusAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: dict
        :rtype: dict[str: TaskStatus]
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_graph_all_nodes_status_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, node_id_path=[],
            custom_headers=self._get_custom_headers())

        return result

    def get_node_outputs_async(self, experiment_id, node_id):
        """GetNodeOutputsAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node outputs dictionary
        :rtype: dict
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_outputs_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, node_id_path=[node_id],
            custom_headers=self._get_custom_headers())

        return result

    def get_node_job_log_async(self, experiment_id, node_id):
        """GetNodeJobLogAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node job log
        :rtype: str
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_graph_shareable_job_log_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, node_id_path=[node_id],
            custom_headers=self._get_custom_headers())

        return result

    def get_node_stdout_log_async(self, experiment_id, node_id):
        """GetNodeStdOutAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node stdout
        :rtype: str
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_graph_shareable_stdout_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, node_id_path=[node_id],
            custom_headers=self._get_custom_headers())

        return result

    def get_node_stderr_log_async(self, experiment_id, node_id):
        """GetNodeStdErrAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :param node_id: The node id
        :type node_id: str
        :return: node stderr
        :rtype: str
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_by_experiment_id_graph_shareable_stderr_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, experiment_id=experiment_id, node_id_path=[node_id],
            custom_headers=self._get_custom_headers())

        return result

    def create_template_async(self, template_creation_info):
        """CreateTemplateAsync.

        :param template_creation_info: The template creation info
        :type template_creation_info: ~swaggerfixed.models.TemplateCreationInfo
        :return: TemplateEntity
        :rtype: ~swaggerfixed.models.TemplateEntity
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_templates_create_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            template_creation_info=template_creation_info)

        return result

    def get_template_async(self, template_id):
        """GetTemplateAsync.

        :param template_id: The template id
        :type template_id: str
        :return: TemplateEntity
        :rtype: ~swaggerfixed.models.TemplateEntity
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_templates_by_template_id_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(), template_id=template_id)

        return result

    def submit_experiment_from_template_async(self, template_id, experiment_name, parameter_assignment=None):
        """SubmitExperimentFromTemplateAsync.

        :param template_id: The template id
        :type template_id: str
        :param experiment_name: The experiment name
        :type experiment_name: str
        :param parameter_assignment: Parameter assignment.
         If null, it will use defaults from the base experiment.
        :type parameter_assignment: dict[str, str]
        :return: ExperimentEntity
        :rtype: ~swaggerfixed.models.ExperimentEntity
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_template_submit_by_template_id_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            template_id=template_id, experiment_name=experiment_name,
            parameter_assignment=parameter_assignment)

        return result

    def try_get_module_by_hash_async(self, identifier_hash):
        """GetModuleByHashAsync.

        :param identifier_hash: The module identifierHash
        :type identifier_hash: str
        :return: Module that was found, or None if not found
        :rtype: ~swagger.models.Module
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        try:
            result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_modules_hash_by_identifier_hash_get(
                subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                custom_headers=self._get_custom_headers(),
                identifier_hash=identifier_hash)
        except ErrorResponseException:
            # If the module was not found, return None
            return None

        return result

    def try_get_datasource_by_hash_async(self, identifier_hash):
        """GetDataSourceByHashAsync.

        :param identifier_hash: The datasource identifierHash
        :type identifier_hash: str
        :return: DataSourceEntity that was found, or None if not found
        :rtype: ~swagger.models.DataSourceEntity or
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        try:
            result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_data_sources_hash_by_hash_get(
                subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
                workspace_name=self._workspace_name,
                custom_headers=self._get_custom_headers(),
                hash=identifier_hash)
        except ErrorResponseException:
            # If the module was not found, return None
            return None

        return result

    def get_all_datatypes_async(self):
        """GetAllDataTypesAsync.

        :return: list
        :rtype: list[~swagger.models.DataTypeEntity]
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_data_types_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers())

        return result

    def create_datatype_async(self, creation_info):
        """CreateNewDataTypeAsync.

        :param creation_info: The DataTypeEntity creation info
        :type creation_info: ~swagger.models.DataTypeCreationInfo
        :return: DataTypeEntity
        :rtype: ~swagger.models.DataTypeEntity
        :raises:
         :class:`ErrorResponseException`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_data_types_post(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            creation_info=creation_info)

        return result

    def get_experiments_by_pipeline_id_async(self, pipeline_id):
        """GetExperimentsByPipelineIdAsync.

        :param pipeline_id: The published pipeline id
        :type pipeline_id: str
        :return: list
        :rtype: list[~swagger.models.ExperimentEntity]
        :raises:
         :class:`ErrorResponseException`
        """

        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_experiments_pipeline_by_pipeline_id_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            pipeline_id=pipeline_id)

        return result

    def get_all_published_pipelines(self, active_only=True):
        """GetPublishedPipelinesAsync.

        :param active_only: Indicate whether to load active only
        :type active_only: bool
        :return: list
        :rtype: list[~swagger.models.TemplateEntity]
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        result = self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_published_pipelines_get(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            active_only=active_only)

        return result

    def update_published_pipeline_status_async(self, pipeline_id, new_status):
        """UpdateStatusAsync.

        :param pipeline_id: The published pipeline id
        :type pipeline_id: str
        :param new_status: New status for the template ('Active', 'Deprecated', or 'Disabled')
        :type new_status: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """

        self._caller.api_v10_subscriptions_by_subscription_id_resource_groups_by_resource_group_name_providers_microsoft_machine_learning_services_workspaces_by_workspace_name_templates_by_template_id_status_put(
            subscription_id=self._subscription_id, resource_group_name=self._resource_group_name,
            workspace_name=self._workspace_name, custom_headers=self._get_custom_headers(),
            template_id=pipeline_id, new_status=new_status)
