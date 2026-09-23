# cookingRAG

![GitHub last commit](https://img.shields.io/github/last-commit/Bissbert/cookingRAG)

**Reads recipes out of photographs with a local vision model and makes them
searchable in natural language.** Point it at a folder of cookbook scans or
handwritten recipe cards; it extracts each one into a structured object, embeds
it, and stores it in PostgreSQL with pgvector. Nothing leaves the machine — the
vision model, the structuring model and the embedding model all run under
Ollama.

It is a small experiment, not a product. Ten of the fifteen defects this
documentation describes have since been fixed on the default branch; the
[known limitations](#known-limitations) separate what is still open from what
was repaired, and are worth reading before you try to use it.

## The pipeline

```mermaid
flowchart TD
    IMG["recipe photos<br/>jpg · jpeg · png"] --> SEL["get_image_files<br/><i>shuffle, take 10</i>"]
    SEL --> RD["SimpleDirectoryReader<br/>→ ImageDocument"]
    RD --> VIS["<b>llama3.2-vision:90b</b><br/>photo → free-text recipe<br/><i>translate, infer diet</i>"]
    VIS --> STR["<b>qwq</b> + PydanticOutputParser<br/>free text → Recipe object"]
    STR --> JSON["recipeExport-UUID.json<br/><i>written to CWD, never read back</i>"]
    STR --> NODE["get_nodes_from_objs<br/>Recipe → TextNode"]
    NODE --> EMB["<b>bge-m3</b><br/>text → vector"]
    EMB --> PG[("PostgreSQL + pgvector<br/>public.data_recipes")]

    Q["natural-language question"] --> QEMB["embed the question"]
    QEMB --> PG
    PG --> TOP["top-5 by cosine distance"]
    TOP --> GEN["response LLM<br/>→ prose answer"]

    style VIS fill:#8250df,stroke:#bc8cff,color:#fff
    style STR fill:#8250df,stroke:#bc8cff,color:#fff
    style EMB fill:#1f6feb,stroke:#58a6ff,color:#fff
    style QEMB fill:#1f6feb,stroke:#58a6ff,color:#fff
    style PG fill:#238636,stroke:#3fb950,color:#fff
    style NODE fill:#da3633,stroke:#f85149,color:#fff
    style GEN fill:#9e6a03,stroke:#d29922,color:#fff
```

Three models, one database, no chunking — a recipe is one row. Red marks the
step that loses data ([why](docs/03-indexing.md)); amber marks the step with no
model configured ([why](docs/05-query.md)).

## Quick start

**This quick start has not been run end to end.** No machine available while
writing it had the models and a pgvector server at the same time; the commands
below are derived from the source, and the two places where the previous README
did not match the code are corrected. See
[docs/measurement.md](docs/measurement.md).

```sh
git clone https://github.com/Bissbert/cookingRAG.git
cd cookingRAG

python3 -m venv venv && . venv/bin/activate

pip install -r requirements.txt

# All three models are required. The vision model is a ~55 GB download.
ollama pull llama3.2-vision:90b
ollama pull qwq
ollama pull bge-m3

# PostgreSQL with pgvector, and a role that may CREATE DATABASE
export PG_PASSWORD=yourpassword

python ingest_recipes.py ./testRecipes
python query_recipes.py something vegetarian with onions
```

Two corrections to the previous instructions:

- `bge-m3` must be pulled as well. It was not listed, and ingestion cannot
  embed without it.
- `query_recipes.py` takes the query as a **required** positional argument
  (`nargs='+'`). `python query_recipes.py` with no arguments is an argparse
  error.

At the time of this pass `pip install -r requirements.txt` failed as committed:

```
ERROR: Cannot install -r requirements.txt (line 8) and pydantic==1.10.17
because these package versions have conflicting dependencies.
    The user requested pydantic==1.10.17
    llama-index-core 0.12.2 depends on pydantic<2.10.0 and >=2.7.0
ERROR: ResolutionImpossible
```

The pin has since been changed to `pydantic==2.9.2`, which satisfies
`llama-index-core` 0.12.2. A full install was not run to confirm the whole set
resolves.

## Requirements

| | Needed | Notes |
|---|---|---|
| Python | 3.11 tested | The conflicting pydantic pin has been corrected to `2.9.2`. |
| Ollama | daemon on `localhost:11434` | Hard-coded; `OLLAMA_HOST` is not honoured. |
| `llama3.2-vision:90b` | image → text | ~55 GB. `:11b` is a one-line substitution, unevaluated here. |
| `qwq` | text → structured `Recipe` | |
| `bge-m3` | embeddings | Not mentioned in the previous README. |
| PostgreSQL | with `pgvector` | Needs `CREATEDB` and permission to `CREATE EXTENSION`. |

`python3 tools/envcheck.py` checks all of these and tells you which are missing.

## What it was tested on

`testRecipes/` holds the five images the author ingested, shown here at 260 px
wide:

![The five test images in testRecipes/](media/corpus.jpg)

Four handwritten German cursive pages from a ring binder, one printed cookbook
page. The repository also contains
`recipeExport-3889e5c2-fd85-4e50-8a61-024a12744127.json`, committed after a real
ingest of exactly these five images — the only surviving output of a working
run. Comparing it against the pictures:

| Image | Recipe on the page | Title extracted |
|---|---|---|
| `IMG_3092` | Spargel im Blätterteig | Spaetzle im Brei |
| `IMG_3093` | Spargel in Pfannkuchen | Spaetzle im Brei |
| `IMG_3094` | Zwiebelkuchen | Spaetzle im Brei |
| `IMG_3095` | Pariser Zwiebelsuppe | Spaetzle im Brei |
| `IMG_4952` | Mehlsuppe *(printed)* | Mehlsuppe mit Brötchen und Eier |

The printed page came through recognisably. All four handwritten pages collapsed
onto one title that appears nowhere in the corpus. The output was also entirely
in German despite the prompt demanding English, and the soup built on veal stock
was labelled `vegetarian`.

This is **one run, n = 5, unknown model build, unknown date** — evidence about
that run, not a benchmark. No accuracy score was computed from it. It is here
because it is the only empirical thing the repository contains, and because the
failure is silent: schema-valid JSON, well-formed, wrong.
[Details](docs/02-extraction.md).

## Repository layout

```
ingest_recipes.py     entry point: folder of images → vector store
query_recipes.py      entry point: natural-language question → answer
util/                 the five modules the pipeline is built from
testRecipes/          five real recipe photographs
recipeExport-*.json   output of one real ingest run, committed
docs/                 a write-up per pipeline stage, plus methodology
tools/                the scripts that produced every number in the docs
media/                generated figures
```

| File | Lines | Bytes |
| --- | ---: | ---: |
| `ingest_recipes.py` | 126 | 3,843 |
| `query_recipes.py` | 51 | 1,683 |
| `util/recipe.py` | 31 | 1,567 |
| `util/json_util.py` | 15 | 411 |
| `util/embedding_util.py` | 55 | 1,842 |
| `util/database_conection.py` | 62 | 2,254 |
| `util/ingestion_model_interaction.py` | 140 | 5,100 |
| **total** | **480** | **16,700** |

→ [Full documentation](docs/README.md) ·
[how this was measured](docs/measurement.md) ·
[bugs found](docs/BUGS-FOUND.md)

## What lands in PostgreSQL

One row per recipe, in `public.data_recipes` — note the `data_` prefix that
`llama_index` adds to the configured name `recipes`:

```sql
CREATE TABLE public.data_recipes (
	id BIGSERIAL NOT NULL,
	text VARCHAR NOT NULL,
	metadata_ JSON,
	node_id VARCHAR,
	embedding VECTOR(1536),
	PRIMARY KEY (id)
)
```

No HNSW or IVFFlat index is created, so similarity search is a sequential scan
with cosine distance — sensible at this scale, but worth knowing.
[Details](docs/04-storage.md).

## Known limitations

Each defect below is written up in full in
[docs/BUGS-FOUND.md](docs/BUGS-FOUND.md) — file and line, how to reproduce it,
and the fix as a diff. An independent adjudication of those fifteen entries
confirmed twelve and rejected three; ten of the twelve have since been fixed on
the default branch. What is left is listed first.

### Still open

- **No LLM and no embedding model are configured for the query path**
  ([BUG-04](docs/BUGS-FOUND.md#bug-04)). `query_recipes.py` imports and builds
  its index correctly now, but without a configured response model
  `llama_index` falls back to OpenAI, which contradicts the local-only premise.
  Choosing the supported local query model — and an embedding identity that
  matches the historical vectors — is a product decision, so nothing was
  guessed. [Details](docs/05-query.md).
- **`embed_dim=1536` is hard-coded** while the embedding model is `bge-m3`
  ([BUG-09](docs/BUGS-FOUND.md#bug-09)). 1536 is the OpenAI/`PGVectorStore`
  default; the Ollama metadata for `bge-m3` reports 1024. Changing the width is
  not a patch — it needs a canonical embedding model and a reindex plan for the
  existing vector column. [Details](docs/04-storage.md).
- **At most 10 images per run.** `sample=10` is hard-coded with no CLI flag.
  The order is now the discovered order unless `shuffle=True` is passed.
- **Extraction on handwriting was not reliable** in the one recorded run: four
  of five images produced the same wrong title. Not quantified beyond that.
- **The vision prompt's translation instruction was not followed** in the
  recorded run; all output stayed in German.
- **Dietary inference is unverified and was wrong at least once** — a veal-stock
  soup was labelled `vegetarian`. Do not rely on this field for anything that
  matters.
- **Configuration is read at import time** and duplicated verbatim between
  `util/database_conection.py` and `query_recipes.py`. The two copies are
  byte-identical, so nothing has diverged yet — but any change has to be made
  twice, by hand.
- **A cloned repository is ~78 MiB for 17 files.** A virtualenv was committed in
  the initial commit and deleted in `7e9c095f`; the blobs remain in history and
  account for **99.3 %** of all object bytes. Deleting files does not shrink
  history — only a rewrite would. `python3 tools/repo_size.py` shows the
  breakdown.

### Recorded, then rejected on review

- **`initModel()` is an empty function** ([BUG-06](docs/BUGS-FOUND.md#bug-06)).
  It is a no-op, but ingestion passes its model explicitly and the query entry
  point never calls it, so no runtime defect follows. Dead scaffolding, not a
  broken initialization path.
- **`recipe.dict()` is removed in pydantic 3**
  ([BUG-10](docs/BUGS-FOUND.md#bug-10)). A future-major removal, not a present
  failure of the pinned dependency set.
- **Ingestion is sequential despite the async scaffolding**
  ([BUG-12](docs/BUGS-FOUND.md#bug-12)). Accurate as a description, but nothing
  in the contract or in a measurement promises parallel execution, and the
  proposed change still wraps blocking model calls. An optimization proposal,
  not a functional bug.

### Fixed on the default branch since this pass

- **Ingredients and instructions were never embedded**
  ([BUG-01](docs/BUGS-FOUND.md#bug-01)). `get_nodes_from_objs()` read fields the
  `Recipe` does not have, so the stored text was title and cook time only. It
  now renders the string ingredients and `instructionsAsString`.
  [Details](docs/03-indexing.md).
- **`query_recipes.py` did not import**
  ([BUG-02](docs/BUGS-FOUND.md#bug-02)). It used the pre-0.10 flat
  `llama_index` layout against the pinned 0.12.2; the imports now match the
  pinned package layout.
- **The query index was built with no nodes and no vector store**
  ([BUG-03](docs/BUGS-FOUND.md#bug-03)). It is now constructed with
  `VectorStoreIndex.from_vector_store`, so it reads the persisted vectors.
- **`requirements.txt` did not resolve**
  ([BUG-05](docs/BUGS-FOUND.md#bug-05)). The `pydantic` pin is now `2.9.2`.
- **The `shuffle` parameter was declared and never read**
  ([BUG-07](docs/BUGS-FOUND.md#bug-07)). `random.shuffle` is now called only
  when `shuffle=True`.
- **`PG_DB_NAME` was interpolated unquoted** into SQL
  ([BUG-08](docs/BUGS-FOUND.md#bug-08)). The existence check binds the name as
  a parameter and creation uses `psycopg2.sql.Identifier`.
- **Both prompts were printed on import**
  ([BUG-11](docs/BUGS-FOUND.md#bug-11)). They are now `logging.debug` calls.
- **One failure lost the whole run**
  ([BUG-13](docs/BUGS-FOUND.md#bug-13)). Batch extraction now catches failures
  per image, logs them, and returns the successful results. A durable
  checkpoint was deliberately not invented.
- **The vision-model retry loop caught only `ResponseError`**
  ([BUG-14](docs/BUGS-FOUND.md#bug-14)). Both retry loops now cover transport
  failures, timeouts and connection failures, and no longer retry validation or
  programming errors.
- **The `Recipe` docstring contradicted its own fields**
  ([BUG-15](docs/BUGS-FOUND.md#bug-15)). It now documents the `undefined` type
  option and the unconstrained string dietary preference.

## Configuration

| Variable | Default | If unset |
|---|---|---|
| `PG_HOST` | `localhost` | fine |
| `PG_PORT` | `5432` | fine |
| `PG_USER` | `postgres` | fine; needs `CREATEDB` |
| `PG_PASSWORD` | `your_database_password` | **breaks** — the literal default is sent and authentication fails |
| `PG_DB_NAME` | `recipe_db` | fine |

Model names, the Ollama URL, the table name, `embed_dim`, timeouts, retry counts
and `similarity_top_k` are all hard-coded.
[Full table, with line numbers](docs/06-configuration.md).

## Status

Experimental. Ingestion runs end to end when the models and the database are
present, the query entry point imports and reads the persisted vectors, and the
indexing step now embeds ingredients and instructions. The query path still has
no configured local response or embedding model, and the hard-coded `embed_dim`
still does not match `bge-m3`. Treat it as a working sketch of a local RAG
pipeline rather than something to put recipes into and trust.

## License

MIT — see [LICENSE](LICENSE).
