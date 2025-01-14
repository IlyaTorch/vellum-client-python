# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class ProcessingStateEnum(str, enum.Enum):
    """
    * `QUEUED` - Queued
    * `PROCESSING` - Processing
    * `PROCESSED` - Processed
    * `FAILED` - Failed
    """

    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

    def visit(
        self,
        queued: typing.Callable[[], T_Result],
        processing: typing.Callable[[], T_Result],
        processed: typing.Callable[[], T_Result],
        failed: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ProcessingStateEnum.QUEUED:
            return queued()
        if self is ProcessingStateEnum.PROCESSING:
            return processing()
        if self is ProcessingStateEnum.PROCESSED:
            return processed()
        if self is ProcessingStateEnum.FAILED:
            return failed()
