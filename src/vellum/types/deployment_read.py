# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .deployment_status import DeploymentStatus
from .environment_enum import EnvironmentEnum
from .vellum_variable import VellumVariable

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class DeploymentRead(pydantic.BaseModel):
    id: str
    created: dt.datetime
    label: str = pydantic.Field(description="A human-readable label for the deployment")
    name: str = pydantic.Field(description="A name that uniquely identifies this deployment within its workspace")
    status: typing.Optional[DeploymentStatus] = pydantic.Field(
        description=(
            "The current status of the deployment\n"
            "\n"
            "* `ACTIVE` - Active\n"
            "* `INACTIVE` - Inactive\n"
            "* `ARCHIVED` - Archived\n"
        )
    )
    environment: typing.Optional[EnvironmentEnum] = pydantic.Field(
        description=(
            "The environment this deployment is used in\n"
            "\n"
            "* `DEVELOPMENT` - Development\n"
            "* `STAGING` - Staging\n"
            "* `PRODUCTION` - Production\n"
        )
    )
    active_model_version_ids: typing.List[str]
    last_deployed_on: dt.datetime
    input_variables: typing.List[VellumVariable]

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
