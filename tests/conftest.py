"""Shared fixtures for the cookingRAG test suite.

No Ollama daemon and no OpenAI key are available where the suite runs. The
Ollama embedding and LLM classes are patched to deterministic local fakes, so
the project's own objects and wiring are exercised without any model.
"""

import hashlib
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

# bge-m3 returns 1024-dimensional dense vectors.
BGE_M3_DIM = 1024
FAKE_ANSWER = "Try the lentil soup."


def fake_vector(text, dim=BGE_M3_DIM):
    """A deterministic unit-length vector derived from the text."""
    seed = hashlib.sha256(text.encode("utf-8")).digest()
    values = [((seed[i % len(seed)] + i) % 251) / 251.0 + 0.01 for i in range(dim)]
    norm = sum(v * v for v in values) ** 0.5
    return [v / norm for v in values]


@pytest.fixture(autouse=True)
def no_openai(monkeypatch):
    """Remove any OpenAI key and reset the global llama_index models."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    from llama_index.core import Settings
    Settings._embed_model = None
    Settings._llm = None
    yield
    Settings._embed_model = None
    Settings._llm = None


@pytest.fixture
def fake_ollama(monkeypatch):
    """Replace Ollama embedding and chat calls with local fakes.

    Returns a dict that records which model names were called.
    """
    from llama_index.core.base.llms.types import ChatMessage, ChatResponse
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.llms.ollama import Ollama

    calls = {"embed_models": [], "llm_models": []}

    def embed(self, text):
        calls["embed_models"].append(self.model_name)
        return fake_vector(text)

    def embed_many(self, texts):
        return [embed(self, t) for t in texts]

    def chat(self, messages, **kwargs):
        calls["llm_models"].append(self.model)
        return ChatResponse(message=ChatMessage(role="assistant", content=FAKE_ANSWER))

    monkeypatch.setattr(OllamaEmbedding, "get_general_text_embedding", embed)
    monkeypatch.setattr(OllamaEmbedding, "_get_text_embedding", embed)
    monkeypatch.setattr(OllamaEmbedding, "_get_query_embedding", embed)
    monkeypatch.setattr(OllamaEmbedding, "_get_text_embeddings", embed_many)
    monkeypatch.setattr(Ollama, "chat", chat)
    return calls
