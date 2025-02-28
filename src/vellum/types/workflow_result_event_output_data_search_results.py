# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .search_result import SearchResult
from .workflow_node_result_event_state import WorkflowNodeResultEventState

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class WorkflowResultEventOutputDataSearchResults(pydantic.BaseModel):
    id: typing.Optional[str]
    name: str
    state: WorkflowNodeResultEventState
    node_id: str
    delta: typing.Optional[str] = pydantic.Field(
        description="The newly output string value. Only relevant for string outputs with a state of STREAMING."
    )
    value: typing.Optional[typing.List[SearchResult]]

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
