# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .input_variable import InputVariable
from .model_version_exec_config_parameters import ModelVersionExecConfigParameters
from .prompt_template_block_data import PromptTemplateBlockData


class ModelVersionExecConfig(pydantic.BaseModel):
    parameters: ModelVersionExecConfigParameters = pydantic.Field(
        description="The generation parameters that are passed to the LLM provider at runtime."
    )
    input_variables: typing.List[InputVariable] = pydantic.Field(
        description="Input variables specified in the prompt template."
    )
    prompt_template: typing.Optional[str] = pydantic.Field(
        description="The template used to generate prompts for this model version."
    )
    prompt_block_data: typing.Optional[PromptTemplateBlockData]
    prompt_syntax_version: typing.Optional[int]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
