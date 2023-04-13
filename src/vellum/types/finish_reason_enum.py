# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class FinishReasonEnum(str, enum.Enum):
    LENGTH = "LENGTH"
    STOP = "STOP"
    UNKNOWN = "UNKNOWN"

    def visit(
        self,
        length: typing.Callable[[], T_Result],
        stop: typing.Callable[[], T_Result],
        unknown: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is FinishReasonEnum.LENGTH:
            return length()
        if self is FinishReasonEnum.STOP:
            return stop()
        if self is FinishReasonEnum.UNKNOWN:
            return unknown()