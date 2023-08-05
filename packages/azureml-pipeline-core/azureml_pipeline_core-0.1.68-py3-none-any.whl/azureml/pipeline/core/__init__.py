# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This package contains the core functionality for AzureMl Pipelines."""
from .builder import PipelineStep, PipelineData, StepSequence
from .pipeline import Pipeline
from .graph import PublishedPipeline, PortDataReference, OutputPortBinding, InputPortBinding
from .run import PipelineRun, StepRun, StepRunOutput
from azureml.core import Run

__all__ = ["PipelineRun",
           "StepRun",
           "StepRunOutput",
           "PipelineStep",
           "PipelineData",
           "Pipeline",
           "PublishedPipeline",
           "PortDataReference",
           "OutputPortBinding",
           "InputPortBinding",
           "StepSequence"
           ]


Run.add_type_provider('azureml.PipelineRun', PipelineRun._from_dto)
Run.add_type_provider('azureml.StepRun', StepRun._from_dto)
Run.add_type_provider('azureml.ReusedStepRun', StepRun._from_reused_dto)
