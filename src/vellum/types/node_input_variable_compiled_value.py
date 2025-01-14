# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .node_input_compiled_chat_history_value import NodeInputCompiledChatHistoryValue
from .node_input_compiled_error_value import NodeInputCompiledErrorValue
from .node_input_compiled_json_value import NodeInputCompiledJsonValue
from .node_input_compiled_number_value import NodeInputCompiledNumberValue
from .node_input_compiled_search_results_value import NodeInputCompiledSearchResultsValue
from .node_input_compiled_string_value import NodeInputCompiledStringValue


class NodeInputVariableCompiledValue_String(NodeInputCompiledStringValue):
    type: typing_extensions.Literal["STRING"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class NodeInputVariableCompiledValue_Number(NodeInputCompiledNumberValue):
    type: typing_extensions.Literal["NUMBER"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class NodeInputVariableCompiledValue_Json(NodeInputCompiledJsonValue):
    type: typing_extensions.Literal["JSON"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class NodeInputVariableCompiledValue_ChatHistory(NodeInputCompiledChatHistoryValue):
    type: typing_extensions.Literal["CHAT_HISTORY"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class NodeInputVariableCompiledValue_SearchResults(NodeInputCompiledSearchResultsValue):
    type: typing_extensions.Literal["SEARCH_RESULTS"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class NodeInputVariableCompiledValue_Error(NodeInputCompiledErrorValue):
    type: typing_extensions.Literal["ERROR"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


NodeInputVariableCompiledValue = typing.Union[
    NodeInputVariableCompiledValue_String,
    NodeInputVariableCompiledValue_Number,
    NodeInputVariableCompiledValue_Json,
    NodeInputVariableCompiledValue_ChatHistory,
    NodeInputVariableCompiledValue_SearchResults,
    NodeInputVariableCompiledValue_Error,
]
