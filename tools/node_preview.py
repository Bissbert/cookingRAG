#!/usr/bin/env python3
"""Show the text that get_nodes_from_objs() actually produces for a Recipe.

util/embedding_util.py builds the string that gets embedded and stored. This
script feeds it a fully populated Recipe built from util/recipe.py and prints
the result verbatim, so the text that reaches the vector store can be compared
against the recipe that went in.

    python3 tools/node_preview.py

Requires the project dependencies (llama_index, pydantic).
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)


def main():
    from util.recipe import Recipe
    from util.embedding_util import get_nodes_from_objs

    recipe = Recipe(
        title="Pariser Zwiebelsuppe",
        ingredients=["375 g Zwiebeln", "50 g Butter", "40 g Mehl", "1 l Bruehe"],
        instructionsAsString=(
            "1. Zwiebeln in feine Scheiben hobeln. "
            "2. In Butter glasig duensten. "
            "3. Mehl aufstreuen und aufkochen lassen."
        ),
        cook_time="45 minutes",
        type="cooking",
        dietary_preference="vegetarian",
    )

    print("Input Recipe")
    print("------------")
    for name in type(recipe).model_fields:
        print("  %-22s %r" % (name, getattr(recipe, name)))

    node = get_nodes_from_objs([recipe])[0]

    print()
    print("Node text handed to the embedding model")
    print("---------------------------------------")
    print(repr(node.text))
    print()
    print("Rendered:")
    for line in node.text.splitlines():
        print("  | %s" % line)
    print()
    print("Node metadata")
    print("-------------")
    print("  %r" % (node.metadata,))
    print()

    ing_lost = all(i not in node.text for i in recipe.ingredients)
    ins_lost = recipe.instructionsAsString not in node.text
    print("Ingredient names reached the node text: %s" % (not ing_lost))
    print("Instruction text reached the node text: %s" % (not ins_lost))
    print()
    print("Characters in: %d (title + ingredients + instructions)"
          % (len(recipe.title) + sum(len(i) for i in recipe.ingredients)
             + len(recipe.instructionsAsString)))
    print("Characters out: %d" % len(node.text))


if __name__ == "__main__":
    main()
