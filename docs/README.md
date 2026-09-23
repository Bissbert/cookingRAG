# Documentation

One write-up per stage of the pipeline, in the order data flows through it, plus
the methodology. Each write-up links back to the overview and to the source it
describes.

| | Stage | Source | In one line |
|---|---|---|---|
| 1 | [Ingestion](01-ingestion.md) | [`ingest_recipes.py`](../ingest_recipes.py) | Picks ten random images and drives the whole run, sequentially. |
| 2 | [Extraction](02-extraction.md) | [`util/ingestion_model_interaction.py`](../util/ingestion_model_interaction.py) | Two Ollama models in series: photo → free text → `Recipe`. |
| 3 | [Indexing](03-indexing.md) | [`util/recipe.py`](../util/recipe.py), [`util/embedding_util.py`](../util/embedding_util.py) | Flattens a `Recipe` to text — and drops the ingredients and instructions doing it. |
| 4 | [Storage](04-storage.md) | [`util/database_conection.py`](../util/database_conection.py) | One row per recipe in `public.data_recipes`, no vector index. |
| 5 | [Query](05-query.md) | [`query_recipes.py`](../query_recipes.py) | The retrieval half. Does not currently import. |
| 6 | [Configuration](06-configuration.md) | — | Every environment variable, every hard-coded value. |
| — | [Measurement](measurement.md) | [`tools/`](../tools) | How every number here was produced, and what was not run. |
| — | [Bugs found](BUGS-FOUND.md) | — | Fifteen defects found while reading the source. None is fixed in this branch. |

## Reading order

If you only read one, read [03 — Indexing](03-indexing.md): it explains why the
text that reaches the vector store is not the text you would expect. For the
defects on their own, with a proposed diff each, see
[BUGS-FOUND.md](BUGS-FOUND.md).

```mermaid
flowchart LR
    A["images"] --> B["<b>1</b><br/>ingestion"]
    B --> C["<b>2</b><br/>extraction"]
    C --> D["<b>3</b><br/>indexing"]
    D --> E["<b>4</b><br/>storage"]
    E --> F["<b>5</b><br/>query"]

    style D fill:#da3633,stroke:#f85149,color:#fff
    style F fill:#da3633,stroke:#f85149,color:#fff
```

Red marks the two stages with defects serious enough to change what the system
does: indexing silently discards most of each recipe, and the query entry point
fails at import.

## Tools

Everything in [`tools/`](../tools) is runnable and produced something quoted in
these pages.

| Script | Produces | Needs |
|---|---|---|
| [`codestats.py`](../tools/codestats.py) | the source-size table | stdlib |
| [`repo_size.py`](../tools/repo_size.py) | the object-graph size breakdown | stdlib + `git` |
| [`envcheck.py`](../tools/envcheck.py) | the component-availability table | stdlib |
| [`inspect_export.py`](../tools/inspect_export.py) | the committed-export summary and schema check | stdlib (+ project deps for the check) |
| [`node_preview.py`](../tools/node_preview.py) | the node text in doc 03 | project deps |
| [`show_schema.py`](../tools/show_schema.py) | the `CREATE TABLE` in doc 04 | project deps |
| [`make_media.py`](../tools/make_media.py) | [`media/corpus.jpg`](../media/corpus.jpg) | Pillow |

[← back to the overview](../README.md)
