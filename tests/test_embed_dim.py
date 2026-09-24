"""Issue #6: the vector column width must match the embedding model."""

import pytest

import util.embedding_util as eu
import util.database_conection as dbc
from conftest import BGE_M3_DIM


@pytest.fixture
def no_probe(monkeypatch):
    """Fail if the width is measured with a model call."""
    from llama_index.embeddings.ollama import OllamaEmbedding

    def refuse(self, text):
        raise AssertionError("embedding model called")

    monkeypatch.setattr(OllamaEmbedding, "get_text_embedding", refuse)


def capture_store_kwargs(monkeypatch):
    captured = {}

    def from_params(**kwargs):
        captured.update(kwargs)
        raise RuntimeError("stop")

    monkeypatch.setattr(dbc.PGVectorStore, "from_params", from_params)
    with pytest.raises(RuntimeError, match="stop"):
        dbc.setup_vector_store()
    return captured


def test_default_model_is_bge_m3():
    assert eu.EMBED_MODEL == "bge-m3"
    assert eu.ollama_embedding.model_name == "bge-m3"


def test_bge_m3_width_is_known_without_a_model_call(monkeypatch, no_probe):
    monkeypatch.delenv("EMBED_DIM", raising=False)
    assert eu.embedding_dim() == BGE_M3_DIM


def test_store_is_created_with_the_model_width(monkeypatch, no_probe):
    monkeypatch.delenv("EMBED_DIM", raising=False)
    kwargs = capture_store_kwargs(monkeypatch)
    assert kwargs["embed_dim"] == BGE_M3_DIM
    assert kwargs["embed_dim"] != 1536


def test_embed_dim_override(monkeypatch, no_probe):
    monkeypatch.setenv("EMBED_DIM", "768")
    assert eu.embedding_dim() == 768
    assert capture_store_kwargs(monkeypatch)["embed_dim"] == 768


def test_tagged_model_name_uses_the_known_width(monkeypatch, no_probe):
    monkeypatch.delenv("EMBED_DIM", raising=False)
    monkeypatch.setattr(eu, "EMBED_MODEL", "bge-m3:latest")
    assert eu.embedding_dim() == BGE_M3_DIM


def test_unknown_model_is_measured_once(monkeypatch):
    from llama_index.embeddings.ollama import OllamaEmbedding

    calls = []

    def probe(self, text):
        calls.append(text)
        return [0.0] * 384

    monkeypatch.delenv("EMBED_DIM", raising=False)
    monkeypatch.setattr(eu, "EMBED_MODEL", "all-minilm")
    monkeypatch.setattr(OllamaEmbedding, "get_text_embedding", probe)
    assert eu.embedding_dim() == 384
    assert len(calls) == 1
