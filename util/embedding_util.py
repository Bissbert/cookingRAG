from typing import List
from llama_index.core import Settings
from llama_index.core.schema import TextNode
from llama_index.embeddings.ollama import OllamaEmbedding
from util.recipe import Recipe



ollama_embedding = OllamaEmbedding(
    model_name="bge-m3",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)

def initEmbeddingModel():
    """
    Initialize the embedding model settings.

    This function sets the global embedding model settings to use the initialized Ollama embedding model.
    """
    Settings.embed_model = ollama_embedding

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
            ingredient = getattr(item, 'ingredient', '')
            amount = getattr(item, 'amount', '')
            recipe_text += f"- {ingredient}: {amount}\n"
        recipe_text += "\nInstructions:\n"
        for idx, step in enumerate(getattr(recipe, 'instructions', []), 1):
            recipe_text += f"{idx}. {step}\n"

        node = TextNode(
            text=recipe_text,
            metadata={
                "type": getattr(recipe, 'type', 'Unknown Type'),
                "dietary_preference": getattr(recipe, 'dietary_preference', 'None'),
            },
        )
        nodes.append(node)
    return nodes

