# Generated by CodiumAI
from ..app import EmbeddingsProcessor
import chromadb
from langchain.vectorstores import Chroma


import pytest


class TestEmbeddingsProcessor:
    # EmbeddingsProcessor initializes successfully with default parameters
    def test_initialize_with_default_parameters(self):
        embeddings_processor = EmbeddingsProcessor()
        assert isinstance(embeddings_processor, EmbeddingsProcessor)

    # create_chroma_database method successfully creates a Chroma database from a list of documents with metadata
    def test_create_chroma_database_success_with_metadata(self):
        embeddings_processor = EmbeddingsProcessor()
        docs = [
            type("Document", (object,), {"page_content": "document 1", "metadata": {}}),
            type("Document", (object,), {"page_content": "document 2", "metadata": {}}),
            type("Document", (object,), {"page_content": "document 3", "metadata": {}}),
        ]
        db = embeddings_processor.create_chroma_database(docs)
        assert isinstance(db, Chroma)

    # Error is raised if Chroma.from_documents fails to create a database
    def test_error_if_chroma_from_documents_fails_to_create_database(self):
        embeddings_processor = EmbeddingsProcessor()
        with pytest.raises(Exception):
            embeddings_processor.create_chroma_database([])

    # The similarity_search method should not raise an exception when called with an empty query or a valid query
    def test_similarity_search_called_with_empty_query_or_database(self):
        embeddings_processor = EmbeddingsProcessor()
        docs = [
            type("Document", (object,), {"page_content": "document 1", "metadata": {}}),
            type("Document", (object,), {"page_content": "document 2", "metadata": {}}),
            type("Document", (object,), {"page_content": "document 3", "metadata": {}}),
        ]
        db = embeddings_processor.create_chroma_database(docs)
        try:
            db.similarity_search("")
            db.similarity_search("query")
        except Exception as e:
            pytest.fail(f"An error occurred: {str(e)}")
