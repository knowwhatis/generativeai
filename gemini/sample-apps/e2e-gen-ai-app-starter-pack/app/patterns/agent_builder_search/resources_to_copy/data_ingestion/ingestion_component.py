from kfp.dsl import component
from typing import Optional


@component(
    base_image="gcr.io/ml-pipeline/google-cloud-pipeline-components:2.0.0b5",
    packages_to_install=[
        "langchain",
        "langchain-community",
        "vertexai",
        "google-cloud-discoveryengine",
        "langchain-google-vertexai",
        "pypdf",
    ],
)
def ingest_into_datastore(
    project_id: str,
    region_vertex: str,
    region_search: str,
    input_bucket: str,
    data_store_id: str,
) -> str:
    import json
    import vertexai
    import uuid
    from google.api_core.client_options import ClientOptions
    from google.cloud import discoveryengine
    from google.cloud import storage
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_core.documents import Document
    from langchain_core.embeddings import Embeddings
    from langchain_google_vertexai import VertexAIEmbeddings
    from typing import List

    URL = "https://services.google.com/fh/files/misc/practitioners_guide_to_mlops_whitepaper.pdf"
    EMBEDDING_MODEL = "text-embedding-004"
    GCS_URI = "datastore_pre_processed_input.jsonl"
    EMBEDDING_COLUMN = "embedding"

    def pre_process_data(url: str) -> List[Document]:
        """Load and split documents from a given URL."""
        loader = PyPDFLoader(url)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        doc_splits = text_splitter.split_documents(documents)
        for document in doc_splits:
            document.metadata["title"] = "practitioners_guide_to_mlops_whitepaper"
            document.metadata["id"] = str(uuid.uuid4())

        return doc_splits

    def add_embeddings(docs: List[Document], embedding: Embeddings) -> List[Document]:
        embeddings = embedding.embed_documents(
            [
                f"{document.metadata['title']}\n{document.page_content}"
                for document in docs
            ]
        )

        documents_with_embeddings = []

        for index in range(len(docs)):
            current_document = docs[index]
            current_document.metadata["embedding"] = embeddings[index]
            documents_with_embeddings.append(current_document)

        return documents_with_embeddings

    def convert_docs_to_jsonl(
        docs: List[Document], bucket_name: str, file_name: str
    ) -> None:
        """Converts an array of documents to a jsonl file and stores it in GCS.

        Args:
            docs: An array of documents, where each document is a dictionary.
            bucket_name: The name of the GCS bucket.
            file_name: The name of the jsonl file to be created.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        with blob.open("w") as f:
            for doc in docs:
                json_data = doc.metadata
                json_data["content"] = doc.page_content
                dictionary = {
                    "id": doc.metadata["id"],
                    "json_data": json.dumps(json_data),
                }
                f.write(json.dumps(dictionary) + "\n")

    def update_schema_as_json(
        original_schema: str, field_name: Optional[str] = None
    ) -> str:

        original_schema_dict = json.loads(original_schema)

        if original_schema_dict.get("properties") is None:
            original_schema_dict["properties"] = {}

        if field_name:
            field_schema = {
                "type": "array",
                "keyPropertyMapping": "embedding_vector",
                "dimension": 768,
                "items": {"type": "number"},
            }
            original_schema_dict["properties"][field_name] = field_schema

        return json.dumps(original_schema_dict)

    def update_data_store_schema(
        project_id: str,
        location: str,
        data_store_id: str,
        embedding_column: Optional[str] = None,
        client_options: Optional[ClientOptions] = None,
    ) -> None:
        schemaClient = discoveryengine.SchemaServiceClient(
            client_options=client_options
        )
        collection = "default_collection"

        name = f"projects/{project_id}/locations/{location}/collections/{collection}/dataStores/{data_store_id}/schemas/default_schema"

        getSchemaRequest = discoveryengine.GetSchemaRequest(name=name)
        schema = schemaClient.get_schema(request=getSchemaRequest)
        new_schema_json = update_schema_as_json(schema.json_schema, embedding_column)
        new_schema = discoveryengine.Schema(json_schema=new_schema_json, name=name)

        updateSchemaRequest = discoveryengine.UpdateSchemaRequest(
            schema=new_schema, allow_missing=True
        )
        # Make the request
        operation = schemaClient.update_schema(request=updateSchemaRequest)
        print(f"Waiting for operation to complete: {operation.operation.name}")
        operation.result()

    def add_data_in_store(
        project_id: str,
        location: str,
        data_store_id: str,
        bucket_name: Optional[str] = None,
        gcs_uri: Optional[str] = None,
        client_options: Optional[ClientOptions] = None,
    ) -> None:
        client = discoveryengine.DocumentServiceClient(client_options=client_options)

        # The full resource name of the search engine branch.
        # e.g. projects/{project}/locations/{location}/dataStores/{data_store_id}/branches/{branch}
        parent = client.branch_path(
            project=project_id,
            location=location,
            data_store=data_store_id,
            branch="default_branch",
        )

        request = discoveryengine.ImportDocumentsRequest(
            parent=parent,
            gcs_source=discoveryengine.GcsSource(
                # Multiple URIs are supported
                input_uris=[f"gs://{bucket_name}/{gcs_uri}"],
                # Options:
                # - `content` - Unstructured documents (PDF, HTML, DOC, TXT, PPTX)
                # - `custom` - Unstructured documents with custom JSONL metadata
                # - `document` - Structured documents in the discoveryengine.Document format.
                # - `csv` - Unstructured documents with CSV metadata
                data_schema="document",
            ),
            # Options: `FULL`, `INCREMENTAL`
            reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.FULL,
        )

        # Make the request
        operation = client.import_documents(request=request)

        print(f"Waiting for operation to complete: {operation.operation.name}")
        operation.result()

    def main(
        project_id: str,
        region_vertex: str,
        region_search: str,
        input_bucket: str,
        data_store_id: str,
    ) -> str:
        # project_id = os.getenv("PROJECT_ID", 'No project id set')
        # region_vertex = os.getenv("SINGLE_REGION", 'No Vertex AI region set')
        # region_search = os.getenv("MULTI_REGION", 'No agent builder region set')
        # input_bucket = os.getenv("INPUT_BUCKET", 'No input bucket set')
        # data_store_id = os.getenv("DATA_STORE_ID", 'No agent builder data store id set')

        client_options = ClientOptions(
            api_endpoint=f"{region_search}-discoveryengine.googleapis.com"
        )
        vertexai.init(project=project_id, location=region_vertex)
        embedding = VertexAIEmbeddings(
            model_name=EMBEDDING_MODEL, location=region_vertex
        )
        docs = pre_process_data(URL)
        docs = add_embeddings(docs, embedding)
        convert_docs_to_jsonl(docs, input_bucket, GCS_URI)
        update_data_store_schema(
            project_id=project_id,
            location=region_search,
            data_store_id=data_store_id,
            embedding_column=EMBEDDING_COLUMN,
            client_options=client_options,
        )
        add_data_in_store(
            project_id=project_id,
            location=region_search,
            data_store_id=data_store_id,
            client_options=client_options,
            bucket_name=input_bucket,
            gcs_uri=GCS_URI,
        )
        return "Success"

    return main(project_id, region_vertex, region_search, input_bucket, data_store_id)
