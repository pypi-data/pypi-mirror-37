# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""service_calller_base.py, module for interacting with the AzureML service."""

from abc import ABC, abstractmethod


class AE3PServiceCallerBase(ABC):
    """Handles interactions with the AzureML service for
    creating/updating datasources/modules, and submitting
    experiments.
    """

    @abstractmethod
    def create_datasource_async(self, creation_info):
        """CreateDataSourceAsync.

        :param creation_info: The datasource creation info
        :type creation_info: ~swaggerfixed.models.DataSourceCreationInfo
        :return: DatasetEntity
        :rtype: ~swaggerfixed.models.DatasetEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_datasource_async(self, id):
        """GetDataSourceAsync.

        :param id: The datasource id
        :type id: str
        :return: DatasetEntity
        :rtype: ~swaggerfixed.models.DatasetEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def get_module_async(self, id):
        """GetModuleAsync.

        :param id: The module id
        :type id: str
        :return: Module
        :rtype: ~swaggerfixed.models.Module
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def create_module_async(self, creation_info):
        """CreateModuleAsync.

        :param creation_info: The module creation info
        :type creation_info: ~swaggerfixed.models.ModuleCreationInfo
        :return: ModuleEntity
        :rtype: ~swaggerfixed.models.ModuleEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def submit_saved_experiment_async(self, experiment_id):
        """SubmitSavedExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def get_experiment_async(self, experiment_id):
        """GetExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: ExperimentEntity
        :rtype: ~swaggerfixed.models.ExperimentEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def cancel_experiment_async(self, experiment_id):
        """CencelExperimentAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: None
        :rtype: None
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def get_graph_async(self, graph_id):
        """GetGraphAsync

        :param graph_id: The graph id
        :type graph_id: str
        :return: GraphEntity
        :rtype: ~swaggerfixed.models.GraphEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_all_nodes_in_level_status_async(self, experiment_id):
        """GetAllNodesInLevelStatusAsync.

        :param experiment_id: The experiment id
        :type experiment_id: str
        :return: dict
        :rtype: dict[str: TaskStatus]
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def create_template_async(self, template_creation_info):
        """CreateTemplateAsync.

        :param template_creation_info: The template creation info
        :type template_creation_info: ~swaggerfixed.models.TemplateCreationInfo
        :return: TemplateEntity
        :rtype: ~swaggerfixed.models.TemplateEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def get_template_async(self, template_id):
        """GetTemplateAsync.

        :param template_id: The template id
        :type template_id: str
        :return: TemplateEntity
        :rtype: ~swaggerfixed.models.TemplateEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def try_get_module_by_hash_async(self, identifier_hash):
        """GetModuleByHashAsync.

        :param identifier_hash: The module identifierHash
        :type identifier_hash: str
        :return: Module that was found, or None if not found
        :rtype: ~swagger.models.Module
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        pass

    @abstractmethod
    def try_get_datasource_by_hash_async(self, identifier_hash):
        """GetDataSourceByHashAsync.

        :param identifier_hash: The datasource identifierHash
        :type identifier_hash: str
        :return: DataSourceEntity that was found, or None if not found
        :rtype: ~swagger.models.DataSourceEntity or
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        pass

    @abstractmethod
    def get_all_datatypes_async(self):
        """GetAllDataTypesAsync.

        :return: list
        :rtype: list[~swagger.models.DataTypeEntity]
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def create_datatype_async(self, creation_info):
        """CreateNewDataTypeAsync.

        :param creation_info: The DataTypeEntity creation info
        :type creation_info: ~swagger.models.DataTypeCreationInfo
        :return: DataTypeEntity
        :rtype: ~swagger.models.DataTypeEntity
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def get_experiments_by_pipeline_id_async(self, pipeline_id):
        """GetExperimentsByPipelineIdAsync.

        :param pipeline_id: The published pipeline id
        :type pipeline_id: str
        :return: list
        :rtype: list[~swagger.models.ExperimentEntity]
        :raises:
         :class:`ErrorResponseException`
        """
        pass

    @abstractmethod
    def get_all_published_pipelines(self, active_only=True):
        """GetPublishedPipelinesAsync.

        :param active_only: Indicate whether to load active only
        :type active_only: bool
        :return: list
        :rtype: list[~swagger.models.TemplateEntity]
        :raises:
         :class:`HttpOperationError<msrest.exceptions.HttpOperationError>`
        """
        pass

    @abstractmethod
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
        pass

    @staticmethod
    def entity_status_from_enum(status_enum):
        """Convert an enum entity status from the Aeva backend to a string

        :param status_enum: Entity status as from the Aeva enum ('0', '1', or '2')
        :type status_enum: str
        :return: Status value ('Active', 'Deprecated', or 'Disabled')
        :rtype: str
        """
        if status_enum == '0':
            return 'Active'
        elif status_enum == '1':
            return 'Deprecated'
        elif status_enum == '2':
            return 'Disabled'
        else:
            raise ValueError("Invalid entity status " + status_enum)

    @staticmethod
    def entity_status_to_enum(status):
        """Convert a string entity status to the Aeva backend enum

        :param status: Status value ('Active', 'Deprecated', or 'Disabled')
        :type status: str
        :return: Entity status as from the Aeva enum ('0', '1', or '2')
        :rtype: str
        """
        if status == 'Active':
            return '0'
        elif status == 'Deprecated':
            return '1'
        elif status == 'Disabled':
            return '2'
        else:
            raise ValueError("Invalid entity status " + status)
