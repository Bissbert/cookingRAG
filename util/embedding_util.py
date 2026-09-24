import os
from typing import List
from llama_index.core import Settings
from llama_index.core.schema import TextNode
from llama_index.embeddings.ollama import OllamaEmbedding
from util.recipe import Recipe



# The embedding model used on both the ingest and the query path. The vector
# column is created with this model's width, so changing it requires a reindex.
EMBED_MODEL = os.environ.get('EMBED_MODEL', 'bge-m3')
OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')

# Dense output width of known embedding models, so no embedding call is needed
# at startup. Other models are measured with one probe embedding.
KNOWN_EMBED_DIMS = {
    'bge-m3': 1024,
}

ollama_embedding = OllamaEmbedding(
    model_name=EMBED_MODEL,
    base_url=OLLAMA_BASE_URL,
    ollama_additional_kwargs={"mirostat": 0},
)

def initEmbeddingModel():
    """
    Initialize the embedding model settings.

    This function sets the global embedding model settings to use the initialized Ollama embedding model.
    """
    Settings.embed_model = ollama_embedding

def embedding_dim() -> int:
    """
    Return the vector width of the configured embedding model.

    EMBED_DIM in the environment takes precedence. Otherwise the width of a
    known model is returned, and an unknown model is measured with one probe
    embedding.

    Returns:
        int: Number of dimensions the embedding model produces.
    """
    override = os.environ.get('EMBED_DIM')
    if override:
        return int(override)
    name = EMBED_MODEL.split(':')[0]
    if name in KNOWN_EMBED_DIMS:
        return KNOWN_EMBED_DIMS[name]
    return len(ollama_embedding.get_text_embedding("dimension probe"))

def get_nodes_from_objs(recipe_list: List[Recipe]) -> TextNode:
    """
    Convert a list of Recipe objects into a list of TextNode objects.

    Args:
        recipe_list (List[Recipe]): List of Recipe objects to convert.

    Returns:
        List[TextNode]: List of TextNode objects created from the Recipe objects.
    """
    nodes = []
    for recipe in recipe_list:
        recipe_text = f"Title: {getattr(recipe, 'title', 'Unknown Title')}\n"
        recipe_text += f"\nCook Time: {getattr(recipe, 'cook_time', 'N/A')}\n"
        recipe_text += f"Ingredients:\n"
        for item in getattr(recipe, 'ingredients', []):
            recipe_text += f"- {item}\n"
        recipe_text += "\nInstructions:\n"
        recipe_text += f"{getattr(recipe, 'instructionsAsString', '')}\n"

        node = TextNode(
            text=recipe_text,
            metadata={
                "type": getattr(recipe, 'type', 'Unknown Type'),
                "dietary_preference": getattr(recipe, 'dietary_preference', 'None'),
            },
        )
        nodes.append(node)
    return nodes
