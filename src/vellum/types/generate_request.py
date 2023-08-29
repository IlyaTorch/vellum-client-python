# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .chat_message_request import ChatMessageRequest


class GenerateRequest(pydantic.BaseModel):
    input_values: typing.Dict[str, typing.Any] = pydantic.Field(
        description="Key/value pairs for each template variable defined in the deployment's prompt."
    )
    chat_history: typing.Optional[typing.List[ChatMessageRequest]] = pydantic.Field(
        description="Optionally provide a list of chat messages that'll be used in place of the special {$chat_history} variable, if included in the prompt."
    )
    external_ids: typing.Optional[typing.List[str]] = pydantic.Field(
        description="Optionally include a unique identifier for each generation, as represented outside of Vellum. Note that this should generally be a list of length one."
    )

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
