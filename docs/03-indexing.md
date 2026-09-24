# 3 — Indexing: `util/recipe.py` and `util/embedding_util.py`

[← back to the overview](../README.md) · sources:
[`util/recipe.py`](../util/recipe.py) (32 lines) ·
[`util/embedding_util.py`](../util/embedding_util.py) (51 lines)

Between extraction and storage sits a flattening step: each `Recipe` object is
rendered into one plain-text string, wrapped in a `TextNode` with two metadata
keys, and handed to the embedding model. This is the step that decides what the
vector store can actually match on.

## The schema

```mermaid
erDiagram
    RECIPE {
        str title
        list_str ingredients
        str instructionsAsString
        str cook_time
        literal type "baking | cooking | undefined"
        str dietary_preference
    }
    INGREDIENT {
        str ingredient
        str amount
    }
    RECIPE ||..|| INGREDIENT : "declared, never used"
```

`Ingredient` is defined in `util/recipe.py` and is **never imported,
instantiated or referenced** anywhere in the repository — `grep -rn Ingredient`
over the Python sources returns only its own class statement and an unrelated
`"Ingredients:\n"` literal. `Recipe.ingredients` is `List[str]`, not
`List[Ingredient]`.

The class docstring matches the fields. One `Field` description lags behind:
`type` is a `Literal["baking", "cooking", "undefined"]`, but its description
still says "either baking or cooking". That text is part of the schema the
structuring model is shown, so it may make `undefined` less likely to be
chosen; that effect was not measured.

## The flattening

`get_nodes_from_objs()` builds the node text from the fields `Recipe` has:

```python
recipe_text = f"Title: {getattr(recipe, 'title', 'Unknown Title')}\n"
recipe_text += f"\nCook Time: {getattr(recipe, 'cook_time', 'N/A')}\n"
recipe_text += f"Ingredients:\n"
for item in getattr(recipe, 'ingredients', []):
    recipe_text += f"- {item}\n"
recipe_text += "\nInstructions:\n"
recipe_text += f"{getattr(recipe, 'instructionsAsString', '')}\n"
```

```mermaid
flowchart LR
    R["Recipe<br/>title · 4 ingredients<br/>instruction text"] --> G["get_nodes_from_objs"]
    G --> T["TextNode.text<br/>title · cook time<br/>ingredients · instructions"]
    G --> M["TextNode.metadata<br/>type · dietary_preference"]
    T --> E["OllamaEmbedding<br/>bge-m3"]
    M --> E
    E --> S["pgvector"]

    style R fill:#1f6feb,stroke:#58a6ff,color:#fff
    style T fill:#238636,stroke:#3fb950,color:#fff
    style S fill:#238636,stroke:#3fb950,color:#fff
```

`tools/node_preview.py` feeds it a fully populated `Recipe` and prints the
result. Run in a Linux container
([`media/captures/linux-run.txt`](../media/captures/linux-run.txt)):

```
Title: Pariser Zwiebelsuppe

Cook Time: 45 minutes
Ingredients:
- 375 g Zwiebeln
- 50 g Butter
- 40 g Mehl
- 1 l Bruehe

Instructions:
1. Zwiebeln in feine Scheiben hobeln. 2. In Butter glasig duensten. 3. Mehl aufstreuen und aufkochen lassen.
```

```
Ingredient names reached the node text: True
Instruction text reached the node text: True
Characters in: 172 (title + ingredients + instructions)
Characters out: 244
```

Everything the recipe says is in the embedded text, so a question such as
"something vegetarian with lentils" can match on "lentils" through the
embedding. The `vegetarian` half is also a metadata value, but the default
query path does not filter on metadata unless asked to.

Until commit `13980e08` this function read `instructions` and
`Ingredient`-shaped elements, the shape of the older export described in
[02 — Extraction](02-extraction.md), and embedded only the title and cook time
([BUG-01](BUGS-FOUND.md#bug-01)).

## The embedding model

```python
ollama_embedding = OllamaEmbedding(
    model_name="bge-m3",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
)
```

Three things worth knowing:

- `base_url` is **hard-coded**. Unlike the database settings, there is no
  environment variable; an Ollama daemon on another host or port requires a
  source edit.
- `initEmbeddingModel()` assigns this to `Settings.embed_model`, the global
  `llama_index` setting. That is what makes `VectorStoreIndex(...)` in
  `ingest_recipes.py` embed with bge-m3 rather than with the OpenAI default.
- `bge-m3` is a third required model, and the README's quick start does not
  mention pulling it. Ingestion fails without it.

`get_nodes_from_objs` is annotated `-> TextNode` but returns `List[TextNode]`.

## Metadata

```python
metadata={
    "type": getattr(recipe, 'type', 'Unknown Type'),
    "dietary_preference": getattr(recipe, 'dietary_preference', 'None'),
}
```

These two keys do exist on `Recipe`, so they are populated correctly. They land
in the `metadata_` JSON column. Note that by default `llama_index` includes
metadata in the embedded text as well, which is why the logging call in
`ingest_recipes.py` uses `node.get_content(metadata_mode="all")`.

Neither `cook_time` nor `title` is stored as metadata, so they cannot be used as
a filter — only as embedded prose.

## Next

[04 — Storage](04-storage.md): what lands in PostgreSQL.
