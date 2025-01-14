# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class ModelVersionExecConfigParameters(pydantic.BaseModel):
    temperature: typing.Optional[float]
    max_tokens: typing.Optional[int]
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    logit_bias: typing.Optional[typing.Dict[str, typing.Optional[float]]]
    stop: typing.Optional[typing.List[str]]
    top_k: typing.Optional[float]

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
