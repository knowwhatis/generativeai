"""Retriever wrapper for Google Cloud Enterprise Search."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from google.protobuf.json_format import MessageToDict
from google.cloud.discoveryengine_v1beta  import SearchServiceClient, SearchRequest

from pydantic import BaseModel, Extra, root_validator

from langchain.schema import BaseRetriever, Document
from langchain.utils import get_from_dict_or_env

class EnterpriseSearchRetriever(BaseRetriever, BaseModel):
    """Wrapper around Google Cloud Enterprise Search."""
    client: Any = None #: :meta private:
    serving_config: Any = None #: :meta private:Any
    content_search_spec: Any = None #: :meta private:Any
    project_id: str = None
    search_engine_id: str = None
    serving_config_id: str = 'default_config'
    location_id: str = 'global'
    max_snippet_count: int = 3
    credentials: Any = None
    "The default custom credentials (google.auth.credentials.Credentials) to use "
    "when making API calls. If not provided, credentials will be ascertained from "
    "the environment."


    class Config:
        """Configuration for this pydantic object."""
        extra = Extra.forbid
        arbitrary_types_allowed = True

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        try:
            from google.cloud import discoveryengine_v1beta
        except ImportError:
            raise ImportError(
                "google.cloud.discoveryengine is not installed. "
                "Please install it with pip install google-cloud-discoveryengine"
            )

        project_id = get_from_dict_or_env(values, "project_id", "PROJECT_ID")
        values["project_id"] = project_id
        search_engine_id = get_from_dict_or_env(values, "search_engine_id", "SEARCH_ENGINE_ID")
        values["search_engine_id"] = search_engine_id
        location_id = get_from_dict_or_env(values, "location_id", "LOCATION_ID")
        values["location_id"] = location_id
        max_snippet_count = get_from_dict_or_env(values, "max_snippet_count", "MAX_SNIPPET_COUNT")
        values["max_snippet_count"] = max_snippet_count

        client = SearchServiceClient(credentials=values['credentials'])
        values["client"] = client

        serving_config = client.serving_config_path(
            project=project_id,
            location=location_id,
            data_store=search_engine_id,
            serving_config=values['serving_config_id'],
        )
        values["serving_config"] = serving_config

        content_search_spec = {
            'snippet_spec': {
                'max_snippet_count': max_snippet_count, 
            } 
        }
        values["content_search_spec"] = content_search_spec

        return values

    def _convert_search_response(self, search_results):
        """Converts search response to a list of LangChain documents."""
        documents = []
        for result in search_results:
            doc_info = MessageToDict(result.document._pb)
            if doc_info.get('derivedStructData'):
                for snippet in doc_info.get('derivedStructData', {}).get('snippets', []):
                    if snippet.get('snippet') is not None:
                        document = Document(
                            page_content=snippet.get('snippet'),
                            metadata={
                                'source': f"{doc_info.get('derivedStructData').get('link')}:{snippet.get('pageNumber')}",
                                'id': doc_info.get('id')
                            }
                        )
                        documents.append(document)

        return documents

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get documents relevant for a query."""
        request = SearchRequest(
            query=query,
            serving_config=self.serving_config,
            content_search_spec=self.content_search_spec,
        )
        response = self.client.search(request)
        documents = self._convert_search_response(response.results)

        return documents

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        raise NotImplementedError("Async interface to GDELT not implemented")