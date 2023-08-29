# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime


class SubmitCompletionActualRequest(pydantic.BaseModel):
    id: typing.Optional[str] = pydantic.Field(
        description="The Vellum-generated ID of a previously generated completion. Must provide either this or external_id."
    )
    external_id: typing.Optional[str] = pydantic.Field(
        description="The external ID that was originally provided when generating the completion that you'd now like to submit actuals for. Must provide either this or id."
    )
    text: typing.Optional[str] = pydantic.Field(description="Text representing what the completion _should_ have been.")
    quality: typing.Optional[float] = pydantic.Field(
        description="A number between 0 and 1 representing the quality of the completion. 0 is the worst, 1 is the best."
    )
    timestamp: typing.Optional[str] = pydantic.Field(
        description="Optionally provide the timestamp representing when this feedback was collected. Used for reporting purposes."
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
