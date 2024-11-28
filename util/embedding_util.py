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
    Settings.embed_model = ollama_embedding

def get_nodes_from_objs(recipe_list: List[Recipe]) -> TextNode:
    """Get nodes from objects."""
    nodes = []
    for recipe in recipe_list:

        recipe_text = f"Title: {recipe.get('title', 'Unknown Title')}\n"
        recipe_text += f"Ingredients:\n"
        for item in recipe.get('ingredients', []):
            ingredient = item.get('ingredient', '')
            amount = item.get('amount', '')
            recipe_text += f"- {ingredient}: {amount}\n"
        recipe_text += "\nInstructions:\n"
        for idx, step in enumerate(recipe.get('instructions', []), 1):
            recipe_text += f"{idx}. {step}\n"
        recipe_text += f"\nCook Time: {recipe.get('cook_time', 'N/A')}"

        node = TextNode(
            text=recipe_text,
            metadata={
                "type": recipe.type,
                "dietary_preference": recipe.vegan,
            },
        )
        nodes.append(node)
    return nodes

