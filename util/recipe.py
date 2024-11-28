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
    Represents a recipe.

    Attributes:
        title (str): Title of the recipe.
        ingredients (List[Ingredient]): List of ingredients with their amounts.
        instructions (List[str]): Step-by-step cooking instructions.
        cook_time (str): Cooking time in a readable format (e.g., '30 minutes').
        type (Literal["baking", "cooking"]): Type of recipe: either baking or cooking.
        vegan (Literal["vegan", "vegetarian", "meat"]): Dietary preference for the recipe: vegan, vegetarian, or meat-based.
    """
    title: str = Field(..., description="Title of the recipe")
    ingredients: List[Ingredient] = Field(..., description="List of ingredients with their amounts")
    instructions: List[str] = Field(..., description="Step-by-step cooking instructions")
    cook_time: str = Field(..., description="Cooking time in a readable format (e.g., '30 minutes')")
    type: Literal["baking", "cooking"] = Field(..., description="Type of recipe: either baking or cooking")
    vegan: Literal["vegan", "vegetarian", "meat"] = Field(..., description="Dietary preference for the recipe: vegan, vegetarian, or meat-based")