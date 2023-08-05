# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""builder.py, module for building a pipeline graph."""
from abc import ABC, abstractmethod
from azureml.pipeline.core.graph import Graph, Node, InputPortBinding, OutputPortBinding, InputPortDef, OutputPortDef
from azureml.pipeline.core.graph import PortDataReference, ModuleDef, DataSourceDef, PipelineParameter
from azureml.pipeline.core.graph import Edge, _DataReferenceEdgeBuilder, _PipelineDataEdgeBuilder
from azureml.data.data_reference import DataReference
from azureml.pipeline.core._datasource_builder import _DataReferenceDatasourceBuilder
from msrest.exceptions import HttpOperationError

import os


class PipelineStep(ABC):
    """
    PipelineStep represents an execution step in a pipeline.

    A PipelineStep can have named inputs, outputs, and parameters. This is the base step class which the supported
    step types inherit from.


    :param name: The name of the pipeline step.
    :type name: str
    :param inputs: The list of step inputs.
    :type inputs: list
    :param outputs: The list of step outputs.
    :type outputs: list
    :param arguments: The list of step arguments.
    :type arguments: list
    :param fix_port_name_collisions: If true and an input and output have the same name, the input is prefixed with
        "INPUT_".
    :type fix_port_name_collisions: bool
    """

    def __init__(self, name, inputs, outputs, arguments=None, fix_port_name_collisions=False):
        """
        Initialize PipelineStep.

        :param name: The name of the pipeline step.
        :type name: str
        :param inputs: The list of step inputs.
        :type inputs: list
        :param outputs: The list of step outputs.
        :type outputs: list
        :param arguments: The list of step arguments.
        :type arguments: list
        :param fix_port_name_collisions: If true and an input and output have the same name, the input is prefixed with
            "INPUT_".
        :type fix_port_name_collisions: bool
        """
        self.name = name
        self.run_after_steps = []

        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []
        if arguments is None:
            arguments = []
        self._inputs = inputs
        self._outputs = outputs
        self._arguments = arguments

        input_port_names = []
        output_port_names = []
        for step_output in self._outputs:
            if not isinstance(step_output, PipelineData) and not isinstance(step_output, OutputPortBinding):
                raise ValueError("Unexpected output type: %s" % type(step_output))
            step_output._set_producer(self)
            output_port_names.append(step_output._output_name)

        step_inputs = {}
        for step_input in self._inputs:
            if not isinstance(step_input, PipelineData) and not isinstance(step_input, InputPortBinding) and \
                    not isinstance(step_input, DataReference) and not isinstance(step_input, PortDataReference):
                raise ValueError("Unexpected input type: %s" % type(step_input))
            if isinstance(step_input, DataReference) or isinstance(step_input, PortDataReference):
                input_port_names.append(step_input.data_reference_name)
                step_inputs[step_input.data_reference_name] = step_input
            else:
                input_port_names.append(step_input.name)
                step_inputs[step_input.name] = step_input

        self._inputs, self._arguments = self.assure_unique_port_names(input_port_names, output_port_names,
                                                                      step_inputs, arguments, fix_port_name_collisions)

        self.validate_arguments(self._arguments, self._inputs, self._outputs)

    def run_after(self, step):
        """
        Append this step after the provided step.

        :param step: The pipeline step to run before this step.
        :type step: azureml.pipeline.core.PipelineStep
        """
        self.run_after_steps.append(step)

    @abstractmethod
    def create_node(self, graph, default_datastore_name, context):
        """
        Create a node for the pipeline graph based on this step.

        :param graph: The graph to add the node to.
        :type graph: azureml.pipeline.core.graph.Graph
        :param default_datastore_name: Name of the default datastore to use.
        :type default_datastore_name: str
        :param context: The graph context object.
        :type context: _GraphContext

        :return: The created node.
        :rtype: azureml.pipeline.core.graph.Node
        """
        pass

    def assure_unique_port_names(self, input_port_names, output_port_names, step_inputs, step_arguments,
                                 fix_port_name_collisions):
        """
        Assure unique port names.

        :param input_port_names: List of the input port names.
        :type input_port_names: list
        :param output_port_names: List of the output port names.
        :type output_port_names: list
        :param step_inputs: Dictionary of step input names to step input objects.
        :type step_inputs: dict
        :param step_arguments: Dictionary of step output names to step output objects.
        :type step_arguments: list
        :param fix_port_name_collisions: if true and a port name collision exists, the input is prefixed with "INPUT_".
        :type fix_port_name_collisions: bool

        :return: Tuple of the inputs and arguments
        :rtype: list, list
        """
        import re
        invalid_name = re.compile('\\W')

        input_seen = set()
        for port_name in input_port_names:
            if invalid_name.search(port_name):
                raise ValueError("[%s] is not a valid input name. "
                                 "Input port names may only contain letters, digits, and underscores." % port_name)
            if port_name in input_seen:
                raise ValueError("[%s] is repeated. Input port names must be unique." % port_name)
            input_seen.add(port_name)

        output_seen = set()
        for port_name in output_port_names:
            if invalid_name.search(port_name):
                raise ValueError("[%s] is not a valid output name. "
                                 "Output port names may only contain letters, digits, and underscores." % port_name)
            if port_name in output_seen:
                raise ValueError("[%s] is repeated. Output port names must be unique." % port_name)
            output_seen.add(port_name)

        if not fix_port_name_collisions:
            for port_name in input_port_names:
                if port_name in output_seen:
                    raise ValueError("[%s] is repeated. Input and Output port names must be unique." % port_name)
            return step_inputs.values(), step_arguments

        else:
            new_inputs = []
            changed_inputs = {}
            for port_name in input_port_names:
                # check if any input port names are also output port names, if so append 'INPUT_'
                # prefix to data ref name
                step_input = step_inputs[port_name]
                if port_name in output_seen:
                    if isinstance(step_input, DataReference):
                        new_bind_object = self._create_input_bind_object(step_input, "INPUT_{0}".format(port_name))

                        new_input = InputPortBinding(name=port_name,
                                                     bind_object=new_bind_object,
                                                     bind_mode=step_input.mode,
                                                     path_on_compute=step_input.path_on_compute,
                                                     overwrite=step_input.overwrite)

                        changed_inputs[step_input] = new_bind_object
                    elif isinstance(step_input, PipelineData) or isinstance(step_input, PortDataReference):
                        new_bind_object = self._create_input_bind_object(step_input, "INPUT_{0}".format(port_name))
                        if isinstance(step_input, PipelineData):
                            new_bind_object._set_producer(step_input._producer)

                        new_input = InputPortBinding(name=port_name, bind_object=new_bind_object)

                        changed_inputs[step_input] = new_bind_object
                    else:
                        new_bind_object = self._create_input_bind_object(step_input.bind_object,
                                                                         "INPUT_{0}".format(port_name))

                        if isinstance(new_bind_object, PipelineData) or isinstance(new_bind_object, OutputPortBinding):
                            new_bind_object._set_producer(step_input.bind_object._producer)
                        new_input = InputPortBinding(name=port_name,
                                                     bind_object=new_bind_object,
                                                     bind_mode=step_input.bind_mode,
                                                     path_on_compute=step_input.path_on_compute,
                                                     overwrite=step_input.overwrite)
                        changed_inputs[step_input.bind_object] = new_bind_object
                        changed_inputs[step_input] = new_input
                    new_inputs.append(new_input)
                elif isinstance(step_input, InputPortBinding):
                    bind_object_name = step_input.get_bind_object_name()

                    if bind_object_name in output_seen:
                        new_bind_object = self._create_input_bind_object(step_input.bind_object, port_name)
                        if isinstance(new_bind_object, PipelineData) or isinstance(new_bind_object, OutputPortBinding):
                            new_bind_object._set_producer(step_input.bind_object._producer)
                        new_input = InputPortBinding(name=step_input.name,
                                                     bind_object=new_bind_object,
                                                     bind_mode=step_input.bind_mode,
                                                     path_on_compute=step_input.path_on_compute,
                                                     overwrite=step_input.overwrite)

                        changed_inputs[step_input] = new_input
                        changed_inputs[step_input.bind_object] = new_bind_object
                        new_inputs.append(new_input)
                    else:
                        new_inputs.append(step_input)
                else:
                    new_inputs.append(step_input)

            new_arguments = []
            for argument in step_arguments:
                if argument in changed_inputs.keys():
                    new_arguments.append(changed_inputs[argument])
                else:
                    new_arguments.append(argument)

            return new_inputs, new_arguments

    @staticmethod
    def _configure_pipeline_parameters(graph, node, pipeline_params_in_step_params=None,
                                       pipeline_params_implicit=None):
        if pipeline_params_in_step_params is not None:
            graph._add_pipeline_params(list(pipeline_params_in_step_params.values()))
        if pipeline_params_implicit is not None:
            graph._add_pipeline_params(list(pipeline_params_implicit.values()))
        node._attach_pipeline_parameters(pipeline_params_implicit, pipeline_params_in_step_params)

    @staticmethod
    def _get_pipeline_parameters_implicit(arguments=None, inputs=None, outputs=None):
        pipeline_params = {}
        if arguments is not None:
            PipelineStep._process_pipeline_parameters(arguments, pipeline_params)
        # TODO add inputs and outputs
        # if inputs is not None:
        #    PipelineStep._process_pipeline_parameters(inputs, pipeline_params)
        # if outputs is not None:
        #    PipelineStep._process_pipeline_parameters(outputs, pipeline_params)
        return pipeline_params

    @staticmethod
    def _get_pipeline_parameters_step_params(params):
        pipeline_params = {}
        if params is not None:
            for param_name, param_value in params.items():
                if isinstance(param_value, PipelineParameter):
                    if param_name not in pipeline_params:
                        pipeline_params[param_name] = param_value
                    else:
                        if pipeline_params[param_name].default_value != param_value.default_value:
                            raise Exception('Pipeline parameters with same name {0} '
                                            'but different values {1}, {2} used'
                                            .format(param_name,
                                                    pipeline_params[param_name].default_value,
                                                    param_value.default_value))
        return pipeline_params

    @staticmethod
    def _process_pipeline_parameters(parameterizable_list, pipeline_params):
        if parameterizable_list is not None:
            for item in parameterizable_list:
                if isinstance(item, PipelineParameter):
                    if item.name not in pipeline_params:
                        pipeline_params[item.name] = item
                    else:
                        if pipeline_params[item.name].default_value != item.default_value:
                            raise Exception('Pipeline parameters with same name {0} '
                                            'but different values {1}, {2} used'
                                            .format(item.name,
                                                    pipeline_params[item.name].default_value,
                                                    item.default_value))

    @staticmethod
    def _create_input_bind_object(step_input, new_name):
        """
        Create input bind object with the new given name.

        :param step_input: The step input object to recreate.
        :type step_input: PipelineData, DataReference, PortDataReference
        :param new_name: The new name for the input.
        :type new_name: str

        :return: The new step input.
        :rtype: DataReference or PortDataReference or PipelineData or OutputPortBinding
        """
        if isinstance(step_input, DataReference):
            return DataReference(datastore=step_input.datastore,
                                 data_reference_name=new_name,
                                 path_on_datastore=step_input.path_on_datastore,
                                 mode=step_input.mode,
                                 path_on_compute=step_input.path_on_compute,
                                 overwrite=step_input.overwrite)
        elif isinstance(step_input, PortDataReference):
            new_data_ref = DataReference(datastore=step_input._data_reference.datastore,
                                         data_reference_name=new_name,
                                         path_on_datastore=step_input.path_on_datastore,
                                         mode=step_input._data_reference.mode,
                                         path_on_compute=step_input._data_reference.path_on_compute,
                                         overwrite=step_input._data_reference.overwrite)

            return PortDataReference(context=step_input._context,
                                     pipeline_run_id=step_input.pipeline_run_id,
                                     data_reference=new_data_ref)
        elif isinstance(step_input, PipelineData):
            return PipelineData(name=new_name,
                                datastore_name=step_input.datastore_name,
                                output_mode=step_input._output_mode,
                                output_path_on_compute=step_input._output_path_on_compute,
                                output_overwrite=step_input._output_overwrite,
                                output_name=step_input._output_name)
        elif isinstance(step_input, OutputPortBinding):
            return OutputPortBinding(name=new_name,
                                     datastore_name=step_input.datastore_name,
                                     output_name=step_input._output_name,
                                     bind_mode=step_input.bind_mode,
                                     path_on_compute=step_input.path_on_compute,
                                     overwrite=step_input.overwrite)

    @staticmethod
    def validate_arguments(arguments, inputs, outputs):
        """
        Validate the step inputs and outputs in the arguments list are in the input and output lists.

        :param arguments: List of step arguments.
        :type arguments: list
        :param inputs: List of step inputs.
        :type inputs: list
        :param outputs: List of step outputs.
        :type outputs: list
        """
        if arguments is not None:
            for argument in arguments:
                valid = False
                if isinstance(argument, InputPortBinding):
                    for input in inputs:
                        if input == argument or argument.bind_object == input:
                            valid = True
                            break
                    if not valid:
                        raise ValueError(
                            "Input %s appears in arguments list but is not in the input list" % (
                                argument.name))
                elif isinstance(argument, PipelineData):
                    for output in outputs:
                        if output == argument:
                            valid = True
                            break
                    if not valid:
                        for input in inputs:
                            if argument == input or isinstance(input, InputPortBinding) and \
                                    input.bind_object == argument:
                                valid = True
                                break
                    if not valid:
                        raise ValueError(
                            "Input/Output %s appears in arguments list but is not in the input/output lists" % (
                                argument.name))
                elif isinstance(argument, DataReference):
                    for input in inputs:
                        if input == argument or (isinstance(input, InputPortBinding) and
                                                 input.bind_object == argument):
                            valid = True
                            break
                    if not valid:
                        raise ValueError(
                            "Input %s appears in arguments list but is not in the input list" % (
                                argument.data_reference_name))
                elif isinstance(argument, PortDataReference):
                    for input in inputs:
                        if input == argument or (isinstance(input, InputPortBinding) and
                                                 input.bind_object == argument):
                            valid = True
                            break
                    if not valid:
                        raise ValueError(
                            "Input %s appears in arguments list but is not in the input list" % (
                                argument.data_reference_name))
                elif isinstance(argument, OutputPortBinding):
                    for output in outputs:
                        if output == argument:
                            valid = True
                            break
                    if not valid:
                        raise ValueError(
                            "Output %s appears in arguments list but is not in the output list" % (
                                argument.name))

    @staticmethod
    def resolve_input_arguments(arguments, inputs, outputs, params):
        """
        Match inputs and outputs to arguments so argument string is produced correctly.

        :param arguments: List of step arguments.
        :type arguments: list
        :param inputs: List of step inputs.
        :type inputs: list
        :param outputs: List of step outputs.
        :type outputs: list
        :param params: List of step parameters.
        :type params: list

        :return: The resolved arguments list.
        :rtype: list
        """
        resolved_arguments = []
        for argument in arguments:
            if isinstance(argument, InputPortBinding):
                for input in inputs:
                    if input == argument:
                        resolved_arguments.append(input)
                        break
                    elif argument.bind_object == input:
                        resolved_arguments.append(input)
                        break
            elif isinstance(argument, PipelineData):
                found_input = False
                for input in inputs:
                    if input == argument:
                        resolved_arguments.append(input)
                        found_input = True
                        break
                    elif isinstance(input, InputPortBinding) and argument == input.bind_object:
                        resolved_arguments.append(input)
                        found_input = True
                        break
                if not found_input:
                    for output in outputs:
                        if output == argument:
                            resolved_arguments.append(output)
            elif isinstance(argument, PortDataReference):
                for input in inputs:
                    if input == argument:
                        resolved_arguments.append(input)
                        break
                    elif isinstance(input, InputPortBinding) and argument == input.bind_object:
                        resolved_arguments.append(input)
                        break
            elif isinstance(argument, DataReference):
                for input in inputs:
                    if input == argument:
                        resolved_arguments.append(input)
                        break
                    elif isinstance(input, InputPortBinding) and argument == input.bind_object:
                        resolved_arguments.append(input)
                        break
            elif isinstance(argument, PipelineParameter):
                resolved_arguments.append("$AML_PARAMETER_{0}".format(argument.name))
            elif isinstance(argument, str):
                found = False
                for param_name in params:
                    if param_name == argument:
                        resolved_arguments.append("$AML_PARAMETER_{0}".format(argument))
                        found = True
                if not found:
                    resolved_arguments.append(argument)
            else:
                resolved_arguments.append(argument)

        return resolved_arguments

    def create_module_def(self, execution_type, input_bindings, output_bindings, param_defs=None,
                          create_sequencing_ports=True, allow_reuse=True, version=None):
        """
        Create the module definition object that describes the step.

        :param execution_type: The execution type of the module.
        :type execution_type: str
        :param input_bindings: The step input bindings.
        :type input_bindings: list
        :param output_bindings: The step output bindings.
        :type output_bindings: list
        :param param_defs: The step param definitions.
        :type param_defs: list
        :param create_sequencing_ports: If true sequencing ports will be created for the module.
        :type create_sequencing_ports: bool
        :param allow_reuse: If true the module will be available to be reused in future Pipelines.
        :type allow_reuse: bool
        :param version: The version of the module.
        :type version: str

        :return: The module def object.
        :rtype: azureml.pipeline.core.graph.ModuleDef
        """
        # TODO: Use specific datatypes for inputs/outputs
        all_datatypes = ["AnyFile", "AnyDirectory"]
        input_port_defs = []
        for input_binding in input_bindings:
            input_port_defs.append(InputPortDef(name=input_binding.name,
                                                datatypes=all_datatypes,
                                                default_datastore_mode=input_binding.bind_mode,
                                                default_path_on_compute=input_binding.path_on_compute,
                                                default_overwrite=input_binding.overwrite,
                                                default_data_reference_name=input_binding.data_reference_name))

        output_port_defs = []
        for output_binding in output_bindings:
            output_port_defs.append(OutputPortDef(name=output_binding._output_name,
                                                  default_datastore_name=output_binding.datastore_name,
                                                  default_datastore_mode=output_binding.bind_mode,
                                                  default_path_on_compute=output_binding.path_on_compute,
                                                  default_overwrite=output_binding.overwrite))

        module_def = ModuleDef(
            name=self.name,
            description=self.name,
            input_port_defs=input_port_defs,
            output_port_defs=output_port_defs,
            param_defs=param_defs,
            module_execution_type=execution_type,
            create_sequencing_ports=create_sequencing_ports,
            allow_reuse=allow_reuse,
            version=version)

        return module_def

    def create_input_output_bindings(self, inputs, outputs, default_datastore_name):
        """
        Create input and output bindings from the step inputs and outputs.

        :param inputs: The list of step inputs.
        :type inputs: list
        :param outputs: The list of step outputs.
        :type outputs: list
        :param default_datastore_name: The default datastore name.
        :type default_datastore_name: str

        :return: Tuple of the input bindings and output bindings.
        :rtype: list, list
        """
        input_bindings = []
        for step_input in inputs:
            input_binding = step_input
            if not isinstance(step_input, InputPortBinding):
                if isinstance(step_input, DataReference):
                    input_binding = InputPortBinding(name=step_input.data_reference_name,
                                                     bind_object=step_input,
                                                     bind_mode=step_input.mode,
                                                     path_on_compute=step_input.path_on_compute,
                                                     overwrite=step_input.overwrite)
                else:
                    input_binding = step_input.create_input_binding()

            input_bindings.append(input_binding)

        output_bindings = []
        for step_output in outputs:
            output_binding = step_output
            if step_output._producer != self:
                raise ValueError("Step output %s can not be used as an output for step %s, as it is already an "
                                 "output of step %s." % (step_output.name, self.name, step_output._producer.name))
            if isinstance(step_output, PipelineData):
                output_binding = OutputPortBinding(name=step_output.name,
                                                   datastore_name=step_output.datastore_name,
                                                   output_name=step_output._output_name,
                                                   bind_mode=step_output._output_mode,
                                                   path_on_compute=step_output._output_path_on_compute,
                                                   overwrite=step_output._output_overwrite)

            if output_binding.datastore_name is None:
                output_binding.datastore_name = default_datastore_name
                if default_datastore_name is None:
                    raise ValueError("DataStore name not provided for output: %s" % step_output.name)
            output_bindings.append(output_binding)

        return input_bindings, output_bindings

    def get_source_directory_and_hash_paths(self, context, source_directory, script_name, hash_paths):
        """
        Get source directory and hash paths for the step.

        :param context: The graph context object.
        :type context: _GraphContext
        :param source_directory: The source directory for the step.
        :type source_directory: str
        :param script_name: The script name for the step.
        :type script_name: str
        :param hash_paths: The hash paths to use when determining the module fingerprint.
        :type hash_paths: list

        :return: The source directory and hash paths.
        :rtype: str, list
        """
        source_directory = source_directory
        if source_directory is None:
            source_directory = context.default_source_directory

        script_path = os.path.join(source_directory, script_name)
        if not os.path.isfile(script_path):
            abs_path = os.path.abspath(script_path)
            raise ValueError("Step [%s]: script not found at: %s. Make sure to specify an appropriate "
                             "source_directory on the Step or default_source_directory on the Pipeline."
                             % (self.name, abs_path))

        fq_hash_paths = []
        for hash_path in hash_paths:
            if not os.path.isabs(hash_path):
                hash_path = os.path.join(source_directory, hash_path)
                fq_hash_paths.append(hash_path)
                if not os.path.isfile(hash_path) and not os.path.isdir(hash_path):
                    raise ValueError("step [%s]: hash_path does not exist: %s" % (self.name, hash_path))

        return source_directory, fq_hash_paths


class PipelineData(object):
    """
    PipelineData represents a piece of intermediate data in a pipeline.

    PipelineData can be produced by one step and consumed in another step by providing the PipelineData object as an
    output of one step and the input of one or more steps.


    :param name: Name of the PipelineData object.
    :type name: str
    :param datastore_name: Name of the Datastore the PipelineData will reside on.
    :type datastore_name: str
    :param output_name: Name of the output, if None name is used.
    :type output_name: str
    :param output_mode: Specifies whether the producing step will use "upload" or "mount" method to access the data.
    :type output_mode: str
    :param output_path_on_compute: For "upload" mode, the path the module writes the output to.
    :type output_path_on_compute: str
    :param output_overwrite: For "upload" mode, whether to overwrite existing data.
    :type output_overwrite: bool
    """

    def __init__(self, name, datastore_name=None, output_name=None, output_mode="mount", output_path_on_compute=None,
                 output_overwrite=None):
        """
        Initialize PipelineData.

        :param name: Name of the PipelineData object.
        :type name: str
        :param datastore_name: Name of the Datastore the PipelineData will reside on.
        :type datastore_name: str
        :param output_name: Name of the output, if None name is used.
        :type output_name: str
        :param output_mode: Specifies whether the producing step will use "upload" or "mount"
            method to access the data.
        :type output_mode: str
        :param output_path_on_compute: For "upload" mode, the path the module writes the output to.
        :type output_path_on_compute: str
        :param output_overwrite: For "upload" mode, whether to overwrite existing data.
        :type output_overwrite: bool
        """
        self._name = name
        self._datastore_name = datastore_name
        self._producer = None
        self._output_mode = output_mode
        self._output_path_on_compute = output_path_on_compute
        self._output_overwrite = output_overwrite
        if output_name is None:
            output_name = name
        self._output_name = output_name

        if self._output_mode not in ["mount", "upload"]:
            raise ValueError("Invalid output mode [%s]" % self._output_mode)

    def _set_producer(self, step):
        self._producer = step

    def as_download(self, input_name=None, path_on_compute=None, overwrite=None):
        """
        Consume the PipelineData as download.

        :param input_name: Use to specify a name for this input.
        :type input_name: str
        :param path_on_compute: The path on the compute to download to.
        :type path_on_compute: str
        :param overwrite: Use to indicate whether to overwrite existing data.
        :type overwrite: bool

        :return: The InputPortBinding with this PipelineData as the source.
        :rtype: azureml.pipeline.core.graph.InputPortBinding
        """
        return self.create_input_binding(input_name=input_name, mode="download", path_on_compute=path_on_compute,
                                         overwrite=overwrite)

    def as_mount(self, input_name=None):
        """
        Consume the PipelineData as mount.

        :param input_name: Use to specify a name for this input.
        :type input_name: str

        :return: The InputPortBinding with this PipelineData as the source.
        :rtype: azureml.pipeline.core.graph.InputPortBinding
        """
        return self.create_input_binding(input_name=input_name, mode="mount")

    def as_input(self, input_name):
        """
        Create an InputPortBinding and specify an input name (but use default mode).

        :param input_name: Use to specify a name for this input.
        :type input_name: str

        :return: The InputPortBinding with this PipelineData as the source.
        :rtype: azureml.pipeline.core.graph.InputPortBinding
        """
        return self.create_input_binding(input_name=input_name)

    def create_input_binding(self, input_name=None, mode=None, path_on_compute=None, overwrite=None):
        """
        Create input binding.

        :param input_name: The name of the input.
        :type input_name: str
        :param mode: The mode to access the PipelineData ("mount" or "download").
        :type mode: str
        :param path_on_compute: For "download" mode, the path on the compute the data will reside.
        :type path_on_compute: str
        :param overwrite: For "download" mode, whether to overwrite existing data.
        :type overwrite: bool

        :return: The InputPortBinding with this PipelineData as the source.
        :rtype: azureml.pipeline.core.graph.InputPortBinding
        """
        if input_name is None:
            input_name = self._name

        # TODO: currently defaulting to mount, but what if the compute doesnt support it?
        # should be getting default value from somewhere else? should default be passthrough??
        if mode is None:
            mode = "mount"

        if mode not in ["mount", "download"]:
            raise ValueError("Input [%s] has an invalid mode [%s]" % (input_name, mode))

        input_binding = InputPortBinding(
            name=input_name,
            bind_object=self,
            bind_mode=mode,
            path_on_compute=path_on_compute,
            overwrite=overwrite,
        )

        return input_binding

    @property
    def name(self):
        """
        Name of the PipelineData object.

        :return: Name.
        :rtype: str
        """
        return self._name

    @property
    def datastore_name(self):
        """
        Name of the Datastore the PipelineData will reside on.

        :return: The Datastore name.
        :rtype: str
        """
        return self._datastore_name

    def __str__(self):
        """
        __str__ override.

        :return: str representation of the PipelineData
        :rtype: str
        """
        return "$AZUREML_DATAREFERENCE_{0}".format(self.name)

    def __repr__(self):
        """
        Return __str__.

        :return: str representation of the PipelineData
        :rtype: str
        """
        return self.__str__()


class _PipelineGraphBuilder(object):
    """_PipelineGraphBuilder."""

    _registered_builders = {}

    @staticmethod
    def register(collection_name, builder):
        """
        Register builders.

        :param collection_name: collection name
        :type collection_name: str
        :param builder: builder
        :type builder: _SequentialPipelineGraphBuilder, _ParallelPipelineGraphBuilder
        """
        _PipelineGraphBuilder._registered_builders[collection_name] = builder

    def __init__(self, builders=None, resolve_closure=True, default_datastore_name=None, context=None):
        """
        Initialize _PipelineGraphBuilder.

        :param builders: builders
        :type builders: dict
        :param resolve_closure: whether to resolve closure
        :type resolve_closure: bool
        :param default_datastore_name: default datastore name
        :type default_datastore_name: str
        :param context: graph context object
        :type context: _GraphContext
        """
        if context is None:
            raise ValueError("a valid graph context is required")

        self._context = context
        self._default_datastore_name = default_datastore_name

        if builders is None:
            builders = _PipelineGraphBuilder._registered_builders

        self._builders = builders
        self._resolve_closure = resolve_closure

    def build(self, name, steps, finalize=True, regenerate_outputs=False):
        """
        Build a graph that executes the required pipeline steps and produces any required pipeline data.

        :param name: a friendly name for the graph, this is useful for tracking
        :type name: str
        :param steps: pipeline steps and/or data that the graph is required to include
        :type steps: Union[PipelineData, PipelineStep, list]
        :param finalize: call finalize on the graph after construction
        :type finalize: bool
        :param regenerate_outputs: set True to force a new run during finalization (disallows module/datasource reuse)
        :type regenerate_outputs: bool

        :return: the constructed graph
        :rtype: Graph
        """
        if (self._default_datastore_name is None and self._context._workspace is not None):
            try:
                # Attempt to find the default datastore of the workspace if the user has not specified one
                default_datastore = self._context._workspace.get_default_datastore()
                if default_datastore is not None:
                    self._default_datastore_name = default_datastore.name
            except HttpOperationError:
                # If the workspace does not have a default datastore, keep default_datastore_name unset
                pass

        graph = self.construct(name, steps)
        if finalize:
            graph.finalize(regenerate_outputs=regenerate_outputs)
        return graph

    def construct(self, name, steps):
        """
        Construct a graph but does not upload modules.

        :param name: a friendly name for the graph, this is useful for tracking
        :type name: str
        :param steps: pipeline steps and/or data that the graph is required to include
        :type steps: Union[PipelineData, PipelineStep, list]

        :return: the constructed graph
        :rtype: Graph
        """
        self._builderStack = []
        self._nodeStack = []
        self._step2node = {}
        self._graph = Graph(name, self._context)
        self._nodeStack.append([])
        self.process_collection(steps)
        for builder in self._builderStack[::-1]:
            builder.apply_rules()

        return self._graph

    def validate(self):
        """Validate inputs."""
        # check for dangling inputs
        pass

    def process_collection(self, collection):
        """
        Process collection.

        :param collection: collection
        :type collection: list

        :return: list of added nodes.
        :rtype: list
        """
        # for outputs, just include the producer step?
        if isinstance(collection, PipelineData):
            if collection._producer is None:
                raise ValueError("Cannot build graph as step output [%s] does not have a producer. "
                                 "Please add to the outputs list of the step that produces it" % collection._name)
            collection = collection._producer

        # just a step?
        if isinstance(collection, PipelineStep):
            return self.process_step(collection)

        # delegate to correct builder
        builder = self.create_builder(collection)
        self._nodeStack.append([])
        self._builderStack.append(builder)
        builder.process_collection(collection)
        added_nodes = self._nodeStack.pop()
        self._nodeStack[-1].extend(added_nodes)
        return added_nodes

    def assert_node_valid(self, step, graph, node):
        """
        Raise an assert when node is invalid.

        :param step: step
        :type step: pipeline step
        :param graph: graph
        :type graph: Graph
        :param node: node
        :type node: Node
        """
        if node is None:
            raise ValueError("step %s type %s: create_node needs to return a valid Node (got None)"
                             % (step.name, type(step)))
        if not isinstance(node, Node):
            raise ValueError("step %s type %s: create_node needs to return a valid Node (got %s)"
                             % (step.name, type(step), type(node)))
        # TODO: validate node is on correct graph
        # TODO: do deeper node validation e.g. ports etc

    def process_step(self, step):
        """
        Process a step.

        :param step: step
        :type step: PipelineStep

        :return: list of added steps.
        :rtype: list
        """
        if step in self._step2node:
            return self._step2node[step]

        node = step.create_node(self._graph, self._default_datastore_name, self._context)
        self.assert_node_valid(step, self._graph, node)

        self._step2node[step] = node
        self._nodeStack[-1].append(node)

        resolved_nodes = self.resolve_references([node])

        # resolve run_after's
        for predecessor_step in step.run_after_steps:
            if predecessor_step in self._step2node:
                predecessor_node = self._step2node[predecessor_step]
                node.run_after(predecessor_node)
            elif self._resolve_closure:
                resolved_nodes.append(self.process_step(predecessor_step))
                node.run_after(self._step2node[predecessor_step])
            else:
                raise ValueError

        return resolved_nodes

    def create_builder(self, collection):
        """
        Create a builder.

        :param collection: collection
        :type collection: list

        :return: Builder for the collection.
        :rtype: _PipelineGraphBuilder
        """
        key = type(collection).__name__
        if key not in self._builders:
            raise NotImplementedError(key)
        return self._builders[key](self)

    def resolve_references(self, node_list):
        """
        Resolve node references.

        :param node_list: node_list
        :type node_list: list

        :return: list of resolved nodes.
        :rtype: list
        """
        added_nodes = []
        for node in node_list:
            for input_port in node.inputs:
                edge = input_port.incoming_edge
                if edge is not None and not isinstance(edge, Edge) and edge.source is not None:
                    resolved_node = None
                    if isinstance(edge, _PipelineDataEdgeBuilder):
                        peer = edge.source._producer

                        if not isinstance(peer, PipelineStep):
                            raise ValueError('PipelineData or OutputPortBinding producer has invalid type.')

                        if peer not in self._step2node:
                            if self._resolve_closure:
                                added_nodes.extend(self.process_step(peer))
                            else:
                                raise ValueError

                        resolved_node = self._step2node[peer]

                    elif isinstance(edge, _DataReferenceEdgeBuilder):
                        peer = edge.source
                        datasource_def = DataSourceDef(peer.data_reference_name, description=None, data_type_id=None,
                                                       datastore_name=peer.datastore.name,
                                                       path_on_datastore=peer.path_on_datastore)

                        datasource_builder = _DataReferenceDatasourceBuilder(context=self._context,
                                                                             datasource_def=datasource_def)

                        resolved_node = self._graph.add_datasource_node(name=peer.data_reference_name,
                                                                        datasource_builder=datasource_builder)

                    edge.create_edge(resolved_node)

        if len(added_nodes) > 0:
            node_list.extend(self.resolve_references(added_nodes))

        return node_list


class _SequentialPipelineGraphBuilder(object):
    """_SequentialPipelineGraphBuilder."""

    def __init__(self, base_builder):
        """
        Initialize _SequentialPipelineGraphBuilder.

        :param base_builder: base builder
        :type base_builder: _PipelineGraphBuilder
        """
        self._base_builder = base_builder
        self._nodes = []

    def process_collection(self, collection):
        """
        Process list of nodes.

        :param collection: collection
        :type collection: list
        """
        for item in collection:
            nodes = self._base_builder.process_collection(item)
            self._nodes.append(nodes)

    def apply_rules(self):
        """Apply sequential rules."""
        if len(self._nodes) < 2:
            return
        predecessors = []
        for successors in self._nodes:
            if not isinstance(successors, list):
                successors = [successors]
            for successor in successors:
                for predecessor in predecessors:
                    successor.run_after(predecessor)
            predecessors = successors


class _ParallelPipelineGraphBuilder(object):
    """_ParallelPipelineGraphBuilder."""

    def __init__(self, base_builder):
        """
        Initialize _ParallelPipelineGraphBuilder.

        :param base_builder: base builder
        :type base_builder: _PipelineGraphBuilder
        """
        self._base_builder = base_builder

    def process_collection(self, collection):
        """
        Process collection.

        :param collection: collection
        :type collection: list
        """
        for item in collection:
            self._base_builder.process_collection(item)

    def apply_rules(self):
        """Apply rules."""
        pass


class StepSequence(object):
    """
    Creates a list of steps which will be executed in order.

    Use the StepSequence when initializing a Pipeline to create a workflow that contains the steps in the StepSequence.


    :param steps: steps for StepSequence.
    :type steps: list
    """

    def __init__(self, steps=None):
        """
        Initialize StepSequence.

        :param steps: steps for StepSequence.
        :type steps: list
        """
        if steps is None:
            steps = []

        self._steps = steps

    def __iter__(self):
        """
        Iterate over the steps.

        :return: iterator.
        :rtype: iter
        """
        return self._steps.__iter__()


_PipelineGraphBuilder.register(StepSequence.__name__, _SequentialPipelineGraphBuilder)
_PipelineGraphBuilder.register(list.__name__, _ParallelPipelineGraphBuilder)
