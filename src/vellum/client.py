# This file was auto-generated by Fern from our API Definition.

import json
import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx

from .core.api_error import ApiError
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .core.jsonable_encoder import jsonable_encoder
from .environment import VellumEnvironment
from .errors.bad_request_error import BadRequestError
from .errors.forbidden_error import ForbiddenError
from .errors.internal_server_error import InternalServerError
from .errors.not_found_error import NotFoundError
from .resources.deployments.client import AsyncDeploymentsClient, DeploymentsClient
from .resources.document_indexes.client import AsyncDocumentIndexesClient, DocumentIndexesClient
from .resources.documents.client import AsyncDocumentsClient, DocumentsClient
from .resources.model_versions.client import AsyncModelVersionsClient, ModelVersionsClient
from .resources.registered_prompts.client import AsyncRegisteredPromptsClient, RegisteredPromptsClient
from .resources.sandboxes.client import AsyncSandboxesClient, SandboxesClient
from .resources.test_suites.client import AsyncTestSuitesClient, TestSuitesClient
from .types.generate_error_response import GenerateErrorResponse
from .types.generate_options_request import GenerateOptionsRequest
from .types.generate_request import GenerateRequest
from .types.generate_response import GenerateResponse
from .types.generate_stream_response import GenerateStreamResponse
from .types.search_request_options_request import SearchRequestOptionsRequest
from .types.search_response import SearchResponse
from .types.submit_completion_actual_request import SubmitCompletionActualRequest
from .types.submit_workflow_execution_actual_request import SubmitWorkflowExecutionActualRequest
from .types.workflow_execution_event_type import WorkflowExecutionEventType
from .types.workflow_request_input_request import WorkflowRequestInputRequest
from .types.workflow_stream_event import WorkflowStreamEvent

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class Vellum:
    def __init__(
        self,
        *,
        environment: VellumEnvironment = VellumEnvironment.PRODUCTION,
        api_key: str,
        timeout: typing.Optional[float] = None,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        self._client_wrapper = SyncClientWrapper(
            environment=environment,
            api_key=api_key,
            httpx_client=httpx.Client(timeout=timeout) if httpx_client is None else httpx_client,
        )
        self.deployments = DeploymentsClient(client_wrapper=self._client_wrapper)
        self.document_indexes = DocumentIndexesClient(client_wrapper=self._client_wrapper)
        self.documents = DocumentsClient(client_wrapper=self._client_wrapper)
        self.model_versions = ModelVersionsClient(client_wrapper=self._client_wrapper)
        self.registered_prompts = RegisteredPromptsClient(client_wrapper=self._client_wrapper)
        self.sandboxes = SandboxesClient(client_wrapper=self._client_wrapper)
        self.test_suites = TestSuitesClient(client_wrapper=self._client_wrapper)

    def execute_workflow_stream(
        self,
        *,
        workflow_deployment_id: typing.Optional[str] = OMIT,
        workflow_deployment_name: typing.Optional[str] = OMIT,
        release_tag: typing.Optional[str] = OMIT,
        inputs: typing.List[WorkflowRequestInputRequest],
        external_id: typing.Optional[str] = OMIT,
        event_types: typing.Optional[typing.List[WorkflowExecutionEventType]] = OMIT,
    ) -> typing.Iterator[WorkflowStreamEvent]:
        """
        Executes a deployed Workflow and streams back its results.

        Parameters:
            - workflow_deployment_id: typing.Optional[str]. The ID of the Workflow Deployment. Must provide either this or workflow_deployment_name.

            - workflow_deployment_name: typing.Optional[str]. The name of the Workflow Deployment. Must provide either this or workflow_deployment_id.

            - release_tag: typing.Optional[str]. Optionally specify a release tag if you want to pin to a specific release of the Workflow Deployment

            - inputs: typing.List[WorkflowRequestInputRequest].

            - external_id: typing.Optional[str]. Optionally include a unique identifier for tracking purposes.

            - event_types: typing.Optional[typing.List[WorkflowExecutionEventType]]. Optionally specify which events you want to receive. Defaults to only WORKFLOW events. Note that the schema of non-WORKFLOW events is unstable and should be used with caution.
        """
        _request: typing.Dict[str, typing.Any] = {"inputs": inputs}
        if workflow_deployment_id is not OMIT:
            _request["workflow_deployment_id"] = workflow_deployment_id
        if workflow_deployment_name is not OMIT:
            _request["workflow_deployment_name"] = workflow_deployment_name
        if release_tag is not OMIT:
            _request["release_tag"] = release_tag
        if external_id is not OMIT:
            _request["external_id"] = external_id
        if event_types is not OMIT:
            _request["event_types"] = event_types
        with self._client_wrapper.httpx_client.stream(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/execute-workflow-stream"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        ) as _response:
            if 200 <= _response.status_code < 300:
                for _text in _response.iter_lines():
                    if len(_text) == 0:
                        continue
                    yield pydantic.parse_obj_as(WorkflowStreamEvent, json.loads(_text))  # type: ignore
                return
            _response.read()
            if _response.status_code == 400:
                raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 500:
                raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> GenerateResponse:
        """
        Generate a completion using a previously defined deployment.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - deployment_id: typing.Optional[str]. The ID of the deployment. Must provide either this or deployment_name.

            - deployment_name: typing.Optional[str]. The name of the deployment. Must provide either this or deployment_id.

            - requests: typing.List[GenerateRequest]. The generation request to make. Bulk requests are no longer supported, this field must be an array of length 1.

            - options: typing.Optional[GenerateOptionsRequest]. Additional configuration that can be used to control what's included in the response.
        ---
        from vellum import GenerateOptionsRequest, GenerateRequest, LogprobsEnum
        from vellum.client import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.generate(
            requests=[
                GenerateRequest(
                    input_values={},
                )
            ],
            options=GenerateOptionsRequest(
                logprobs=LogprobsEnum.ALL,
            ),
        )
        """
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/generate"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GenerateResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 403:
            raise ForbiddenError(pydantic.parse_obj_as(GenerateErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate_stream(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> typing.Iterator[GenerateStreamResponse]:
        """
        Generate a stream of completions using a previously defined deployment.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - deployment_id: typing.Optional[str]. The ID of the deployment. Must provide either this or deployment_name.

            - deployment_name: typing.Optional[str]. The name of the deployment. Must provide either this or deployment_id.

            - requests: typing.List[GenerateRequest]. The generation request to make. Bulk requests are no longer supported, this field must be an array of length 1.

            - options: typing.Optional[GenerateOptionsRequest]. Additional configuration that can be used to control what's included in the response.
        """
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        with self._client_wrapper.httpx_client.stream(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/generate-stream"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        ) as _response:
            if 200 <= _response.status_code < 300:
                for _text in _response.iter_lines():
                    if len(_text) == 0:
                        continue
                    yield pydantic.parse_obj_as(GenerateStreamResponse, json.loads(_text))  # type: ignore
                return
            _response.read()
            if _response.status_code == 400:
                raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 403:
                raise ForbiddenError(pydantic.parse_obj_as(GenerateErrorResponse, _response.json()))  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 500:
                raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def search(
        self,
        *,
        index_id: typing.Optional[str] = OMIT,
        index_name: typing.Optional[str] = OMIT,
        query: str,
        options: typing.Optional[SearchRequestOptionsRequest] = OMIT,
    ) -> SearchResponse:
        """
        Perform a search against a document index.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - index_id: typing.Optional[str]. The ID of the index to search against. Must provide either this or index_name.

            - index_name: typing.Optional[str]. The name of the index to search against. Must provide either this or index_id.

            - query: str. The query to search for.

            - options: typing.Optional[SearchRequestOptionsRequest]. Configuration options for the search.
        """
        _request: typing.Dict[str, typing.Any] = {"query": query}
        if index_id is not OMIT:
            _request["index_id"] = index_id
        if index_name is not OMIT:
            _request["index_name"] = index_name
        if options is not OMIT:
            _request["options"] = options
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/search"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SearchResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def submit_completion_actuals(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        actuals: typing.List[SubmitCompletionActualRequest],
    ) -> None:
        """
        Used to submit feedback regarding the quality of previously generated completions.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - deployment_id: typing.Optional[str]. The ID of the deployment. Must provide either this or deployment_name.

            - deployment_name: typing.Optional[str]. The name of the deployment. Must provide either this or deployment_id.

            - actuals: typing.List[SubmitCompletionActualRequest]. Feedback regarding the quality of previously generated completions
        ---
        from vellum.client import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.submit_completion_actuals(
            actuals=[],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/submit-completion-actuals"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def submit_workflow_execution_actuals(
        self,
        *,
        actuals: typing.List[SubmitWorkflowExecutionActualRequest],
        execution_id: typing.Optional[str] = OMIT,
        external_id: typing.Optional[str] = OMIT,
    ) -> None:
        """
            Used to submit feedback regarding the quality of previous workflow execution and its outputs.

            **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - actuals: typing.List[SubmitWorkflowExecutionActualRequest]. Feedback regarding the quality of an output on a previously executed workflow.

            - execution_id: typing.Optional[str]. The Vellum-generated ID of a previously executed workflow. Must provide either this or external_id.

            - external_id: typing.Optional[str]. The external ID that was originally provided by when executing the workflow, if applicable, that you'd now like to submit actuals for. Must provide either this or execution_id.
        ---
        from vellum.client import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.submit_workflow_execution_actuals(
            actuals=[],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if execution_id is not OMIT:
            _request["execution_id"] = execution_id
        if external_id is not OMIT:
            _request["external_id"] = external_id
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_environment().predict}/", "v1/submit-workflow-execution-actuals"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncVellum:
    def __init__(
        self,
        *,
        environment: VellumEnvironment = VellumEnvironment.PRODUCTION,
        api_key: str,
        timeout: typing.Optional[float] = None,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        self._client_wrapper = AsyncClientWrapper(
            environment=environment,
            api_key=api_key,
            httpx_client=httpx.AsyncClient(timeout=timeout) if httpx_client is None else httpx_client,
        )
        self.deployments = AsyncDeploymentsClient(client_wrapper=self._client_wrapper)
        self.document_indexes = AsyncDocumentIndexesClient(client_wrapper=self._client_wrapper)
        self.documents = AsyncDocumentsClient(client_wrapper=self._client_wrapper)
        self.model_versions = AsyncModelVersionsClient(client_wrapper=self._client_wrapper)
        self.registered_prompts = AsyncRegisteredPromptsClient(client_wrapper=self._client_wrapper)
        self.sandboxes = AsyncSandboxesClient(client_wrapper=self._client_wrapper)
        self.test_suites = AsyncTestSuitesClient(client_wrapper=self._client_wrapper)

    async def execute_workflow_stream(
        self,
        *,
        workflow_deployment_id: typing.Optional[str] = OMIT,
        workflow_deployment_name: typing.Optional[str] = OMIT,
        release_tag: typing.Optional[str] = OMIT,
        inputs: typing.List[WorkflowRequestInputRequest],
        external_id: typing.Optional[str] = OMIT,
        event_types: typing.Optional[typing.List[WorkflowExecutionEventType]] = OMIT,
    ) -> typing.AsyncIterator[WorkflowStreamEvent]:
        """
        Executes a deployed Workflow and streams back its results.

        Parameters:
            - workflow_deployment_id: typing.Optional[str]. The ID of the Workflow Deployment. Must provide either this or workflow_deployment_name.

            - workflow_deployment_name: typing.Optional[str]. The name of the Workflow Deployment. Must provide either this or workflow_deployment_id.

            - release_tag: typing.Optional[str]. Optionally specify a release tag if you want to pin to a specific release of the Workflow Deployment

            - inputs: typing.List[WorkflowRequestInputRequest].

            - external_id: typing.Optional[str]. Optionally include a unique identifier for tracking purposes.

            - event_types: typing.Optional[typing.List[WorkflowExecutionEventType]]. Optionally specify which events you want to receive. Defaults to only WORKFLOW events. Note that the schema of non-WORKFLOW events is unstable and should be used with caution.
        """
        _request: typing.Dict[str, typing.Any] = {"inputs": inputs}
        if workflow_deployment_id is not OMIT:
            _request["workflow_deployment_id"] = workflow_deployment_id
        if workflow_deployment_name is not OMIT:
            _request["workflow_deployment_name"] = workflow_deployment_name
        if release_tag is not OMIT:
            _request["release_tag"] = release_tag
        if external_id is not OMIT:
            _request["external_id"] = external_id
        if event_types is not OMIT:
            _request["event_types"] = event_types
        async with self._client_wrapper.httpx_client.stream(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/execute-workflow-stream"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        ) as _response:
            if 200 <= _response.status_code < 300:
                async for _text in _response.aiter_lines():
                    if len(_text) == 0:
                        continue
                    yield pydantic.parse_obj_as(WorkflowStreamEvent, json.loads(_text))  # type: ignore
                return
            await _response.aread()
            if _response.status_code == 400:
                raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 500:
                raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> GenerateResponse:
        """
        Generate a completion using a previously defined deployment.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - deployment_id: typing.Optional[str]. The ID of the deployment. Must provide either this or deployment_name.

            - deployment_name: typing.Optional[str]. The name of the deployment. Must provide either this or deployment_id.

            - requests: typing.List[GenerateRequest]. The generation request to make. Bulk requests are no longer supported, this field must be an array of length 1.

            - options: typing.Optional[GenerateOptionsRequest]. Additional configuration that can be used to control what's included in the response.
        ---
        from vellum import GenerateOptionsRequest, GenerateRequest, LogprobsEnum
        from vellum.client import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )
        await client.generate(
            requests=[
                GenerateRequest(
                    input_values={},
                )
            ],
            options=GenerateOptionsRequest(
                logprobs=LogprobsEnum.ALL,
            ),
        )
        """
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/generate"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GenerateResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 403:
            raise ForbiddenError(pydantic.parse_obj_as(GenerateErrorResponse, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate_stream(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> typing.AsyncIterator[GenerateStreamResponse]:
        """
        Generate a stream of completions using a previously defined deployment.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - deployment_id: typing.Optional[str]. The ID of the deployment. Must provide either this or deployment_name.

            - deployment_name: typing.Optional[str]. The name of the deployment. Must provide either this or deployment_id.

            - requests: typing.List[GenerateRequest]. The generation request to make. Bulk requests are no longer supported, this field must be an array of length 1.

            - options: typing.Optional[GenerateOptionsRequest]. Additional configuration that can be used to control what's included in the response.
        """
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        async with self._client_wrapper.httpx_client.stream(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/generate-stream"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        ) as _response:
            if 200 <= _response.status_code < 300:
                async for _text in _response.aiter_lines():
                    if len(_text) == 0:
                        continue
                    yield pydantic.parse_obj_as(GenerateStreamResponse, json.loads(_text))  # type: ignore
                return
            await _response.aread()
            if _response.status_code == 400:
                raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 403:
                raise ForbiddenError(pydantic.parse_obj_as(GenerateErrorResponse, _response.json()))  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 500:
                raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def search(
        self,
        *,
        index_id: typing.Optional[str] = OMIT,
        index_name: typing.Optional[str] = OMIT,
        query: str,
        options: typing.Optional[SearchRequestOptionsRequest] = OMIT,
    ) -> SearchResponse:
        """
        Perform a search against a document index.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - index_id: typing.Optional[str]. The ID of the index to search against. Must provide either this or index_name.

            - index_name: typing.Optional[str]. The name of the index to search against. Must provide either this or index_id.

            - query: str. The query to search for.

            - options: typing.Optional[SearchRequestOptionsRequest]. Configuration options for the search.
        """
        _request: typing.Dict[str, typing.Any] = {"query": query}
        if index_id is not OMIT:
            _request["index_id"] = index_id
        if index_name is not OMIT:
            _request["index_name"] = index_name
        if options is not OMIT:
            _request["options"] = options
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/search"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SearchResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def submit_completion_actuals(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        actuals: typing.List[SubmitCompletionActualRequest],
    ) -> None:
        """
        Used to submit feedback regarding the quality of previously generated completions.

        **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - deployment_id: typing.Optional[str]. The ID of the deployment. Must provide either this or deployment_name.

            - deployment_name: typing.Optional[str]. The name of the deployment. Must provide either this or deployment_id.

            - actuals: typing.List[SubmitCompletionActualRequest]. Feedback regarding the quality of previously generated completions
        ---
        from vellum.client import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )
        await client.submit_completion_actuals(
            actuals=[],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._client_wrapper.get_environment().predict}/", "v1/submit-completion-actuals"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def submit_workflow_execution_actuals(
        self,
        *,
        actuals: typing.List[SubmitWorkflowExecutionActualRequest],
        execution_id: typing.Optional[str] = OMIT,
        external_id: typing.Optional[str] = OMIT,
    ) -> None:
        """
            Used to submit feedback regarding the quality of previous workflow execution and its outputs.

            **Note:** Uses a base url of `https://predict.vellum.ai`.

        Parameters:
            - actuals: typing.List[SubmitWorkflowExecutionActualRequest]. Feedback regarding the quality of an output on a previously executed workflow.

            - execution_id: typing.Optional[str]. The Vellum-generated ID of a previously executed workflow. Must provide either this or external_id.

            - external_id: typing.Optional[str]. The external ID that was originally provided by when executing the workflow, if applicable, that you'd now like to submit actuals for. Must provide either this or execution_id.
        ---
        from vellum.client import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )
        await client.submit_workflow_execution_actuals(
            actuals=[],
        )
        """
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if execution_id is not OMIT:
            _request["execution_id"] = execution_id
        if external_id is not OMIT:
            _request["external_id"] = external_id
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(
                f"{self._client_wrapper.get_environment().predict}/", "v1/submit-workflow-execution-actuals"
            ),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
