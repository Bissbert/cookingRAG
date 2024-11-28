import json
from typing import List
from util.recipe import Recipe


def recipes_to_json(recipes: List[Recipe]) -> str:
    """
    Converts a list of Recipe objects to a JSON string.
    
    Args:
        recipes (List[Recipe]): List of Recipe objects.
        
    Returns:
        str: JSON string representation of the recipes.
    """
    return json.dumps([recipe.dict() for recipe in recipes], indent=4)