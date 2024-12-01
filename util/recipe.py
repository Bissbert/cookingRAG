from pydantic import BaseModel, Field
from typing import List, Literal


class Ingredient(BaseModel):
    """
    Represents an ingredient in a recipe.

    Attributes:
        ingredient (str): Name of the ingredient.
        amount (str): Amount of the ingredient.
    """
    ingredient: str = Field(..., description="Name of the ingredient")
    amount: str = Field(..., description="Amount of the ingredient")


class Recipe(BaseModel):
    """
    Attributes:
        title (str): Title of the recipe.
        ingredients (List[str]): List of ingredients with their amounts.
        instructionsAsString (str): Step-by-step cooking instructions.
        cook_time (str): Cooking time in a readable format (e.g., '30 minutes').
        type (Literal["baking", "cooking"]): Type of recipe: either baking or cooking.
        dietary_preference (Literal["vegan", "vegetarian", "meat"]): Dietary preference for the recipe: vegan, vegetarian, or meat-based.
    """
    title: str = Field(..., description="Title of the recipe")
    ingredients: List[str] = Field(..., description="List of ingredients with their amounts")
    instructionsAsString: str = Field(..., description="Step-by-step cooking instructions")
    cook_time: str = Field(..., description="Total cooking time in a readable format (e.g., '30 minutes')")
    type: Literal["baking", "cooking", "undefined"] = Field(..., description="Type of recipe: either baking or cooking")
    dietary_preference: str = Field(..., description="Dietary preference for the recipe: vegan, vegetarian, or meat-based")