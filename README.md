# cookingRAG

![GitHub last commit](https://img.shields.io/github/last-commit/Bissbert/cookingRAG)

> Ingests recipe photos using a local multimodal LLM, stores extracted recipes in a PostgreSQL vector store, and retrieves them by natural-language query.

## Why

Recipe collections often live in photos — screenshots, cookbook scans, handwritten cards — not in machine-readable formats. cookingRAG uses a locally-running vision model (LLaVA via Ollama) to extract structured recipe data from images, embeds the text into a PostgreSQL vector store, and then answers free-text queries like "something vegetarian with lentils" without sending data to an external API.

## Quick start

```bash
git clone https://github.com/Bissbert/cookingRAG.git
cd cookingRAG
pip install -r requirements.txt

# Start Ollama and pull the required models
ollama pull llama3.2-vision:90b
ollama pull qwq

# Set database connection environment variables (see Configuration below)
export PG_PASSWORD=yourpassword

# Ingest a folder of recipe images
python ingest_recipes.py /path/to/recipe/photos

# Query the vector store
python query_recipes.py
```

## How it works

- `ingest_recipes.py` — entry point for ingestion. Collects JPEG/PNG files from a directory (samples up to 10 by default), runs them through the multimodal pipeline, serializes extracted recipes to a JSON export file, converts them to `llama_index` `TextNode` objects, and upserts them into the vector store.
- `util/ingestion_model_interaction.py` — drives two Ollama models in sequence: `llama3.2-vision:90b` extracts raw recipe text from an image; `qwq` converts that text into a structured `Recipe` Pydantic object. Both calls retry up to 3 times with a 5-second delay.
- `util/recipe.py` — `Ingredient` and `Recipe` Pydantic models that define the structured output.
- `util/embedding_util.py` — initialises the `OllamaEmbedding` model and converts `Recipe` objects into `TextNode` objects with metadata attached.
- `util/database_conection.py` — connects to PostgreSQL, creates the `recipe_db` database if absent, and sets up `PGVectorStore` (embedding dimension 1536) via `llama_index`.
- `query_recipes.py` — loads the vector index from PostgreSQL and runs a similarity search against a user-supplied natural-language query.

The entire pipeline runs locally — no OpenAI key required.

## Configuration

Environment variables read by `util/database_conection.py`:

| Variable | Default | Description |
|---|---|---|
| `PG_HOST` | `localhost` | PostgreSQL host |
| `PG_PORT` | `5432` | PostgreSQL port |
| `PG_USER` | `postgres` | PostgreSQL user |
| `PG_PASSWORD` | *(required)* | PostgreSQL password |
| `PG_DB_NAME` | `recipe_db` | Database name |

Ollama must be running locally with `llama3.2-vision:90b` and `qwq` available.

## Status

Experimental. Ingestion runs end-to-end; query functionality is implemented but the project is not yet packaged for production use. See the project roadmap in the repository for planned features (web app, mobile UI, model fine-tuning).

## License

MIT
