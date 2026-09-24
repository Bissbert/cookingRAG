"""Issue #5: the query path must use the local models, not OpenAI."""

import pytest
from llama_index.core import Settings


class StopBeforeQuery(Exception):
    pass


def run_query_main(monkeypatch, argv):
    """Run query_recipes.main() up to the point where the index is opened.

    The vector store is replaced with an in-memory one and the index is
    intercepted, so this checks only what main() configures, not the database.
    """
    import query_recipes
    from llama_index.core import StorageContext

    seen = {}

    def from_vector_store(vector_store, **kwargs):
        seen["embed_model"] = Settings._embed_model
        seen["llm"] = Settings._llm
        raise StopBeforeQuery

    monkeypatch.setattr(query_recipes, "setup_vector_store", StorageContext.from_defaults)
    monkeypatch.setattr(query_recipes.VectorStoreIndex, "from_vector_store", from_vector_store)
    monkeypatch.setattr("sys.argv", ["query_recipes.py"] + argv)
    with pytest.raises(StopBeforeQuery):
        query_recipes.main()
    return seen


def test_query_embeds_with_the_ingest_model(monkeypatch):
    from util.embedding_util import ollama_embedding

    seen = run_query_main(monkeypatch, ["lentils"])
    assert seen["embed_model"] is ollama_embedding
    assert seen["embed_model"].model_name == "bge-m3"


def test_query_answers_with_the_local_llm(monkeypatch):
    from llama_index.llms.ollama import Ollama
    from util.ingestion_model_interaction import language_model

    seen = run_query_main(monkeypatch, ["lentils"])
    assert isinstance(seen["llm"], Ollama)
    assert seen["llm"] is language_model
    assert seen["llm"].model == "qwq"


def test_query_does_not_need_an_openai_key(monkeypatch):
    """Resolving the configured models must not reach for the OpenAI default."""
    run_query_main(monkeypatch, ["lentils"])
    # These properties fall back to OpenAI (and raise without a key) when unset.
    assert type(Settings.embed_model).__name__ == "OllamaEmbedding"
    assert type(Settings.llm).__name__ == "Ollama"


def test_query_uses_the_shared_store_setup():
    """One setup_vector_store(), so the query path cannot drift from ingest."""
    import query_recipes
    import util.database_conection as dbc

    assert query_recipes.setup_vector_store is dbc.setup_vector_store
