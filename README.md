# Recipe Processing and Querying Tools

This repository contains two command-line interface (CLI) tools for processing and querying recipe data using AI models:

1. **`ingest_recipes.py`**: Processes a folder of recipe images, extracts structured information using the LLaVA model via Ollama, creates vector embeddings, and uploads them to a PostgreSQL database with `pgvector` for efficient searching.

2. **`query_recipes.py`**: Allows you to query the recipe database using natural language, retrieving relevant recipes based on vector similarity.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
  - [Ollama and LLaVA Model](#ollama-and-llava-model)
- [Usage](#usage)
  - [Ingestion Tool (`ingest_recipes.py`)](#ingestion-tool-ingest_recipespy)
  - [Querying Tool (`query_recipes.py`)](#querying-tool-query_recipespy)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Automated Data Extraction**: Extracts ingredients, instructions, cook time, and total time from recipe images.
- **Vector Embeddings with `pgvector`**: Stores recipes as vector embeddings in PostgreSQL for efficient similarity searches.
- **Natural Language Querying**: Search for recipes using natural language queries.
- **CLI Tools**: Easy-to-use command-line interfaces for both ingestion and querying.

---

## Prerequisites

- **Python 3.7+**
- **PostgreSQL** with the `pgvector` extension
- **Ollama**: A platform for running AI language models locally
- **LLaVA Model**: Large Language and Vision Assistant model pulled via Ollama
- **Required Python Packages** (see [Installation](#installation))

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/recipe-tools.git
   cd recipe-tools
   ```

2. **Create a Virtual Environment (Optional but Recommended)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Python Packages**:

   ```bash
   pip install llama-index
   pip install llama-index-llms-ollama
   pip install llama-index-vector-stores-postgres
   pip install psycopg2-binary
   pip install Pillow
   pip install tqdm
   ```

---

## Setup

### Environment Variables

Set up environment variables for sensitive information like database credentials:

```bash
export PG_HOST='localhost'
export PG_PORT='5432'
export PG_USER='postgres'
export PG_PASSWORD='your_database_password'  # Replace with your actual password
export PG_DB_NAME='recipe_db'
```

### Database Setup

1. **Install PostgreSQL**:

   - Follow instructions at the [official PostgreSQL website](https://www.postgresql.org/download/).

2. **Install `pgvector` Extension**:

   - Follow instructions at the [`pgvector` GitHub repository](https://github.com/pgvector/pgvector#installation).

3. **Ensure PostgreSQL Server is Running**:

   ```bash
   sudo service postgresql start  # On Linux
   # On Windows, use the Services panel to start PostgreSQL service
   ```

### Ollama and LLaVA Model

1. **Install Ollama**:

   - Follow instructions at the [Ollama Documentation](https://ollama.ai/docs/installation).

2. **Start the Ollama Server**:

   ```bash
   ollama serve
   ```

3. **Pull the LLaVA Model**:

   ```bash
   ollama pull llava
   ```

---

## Usage

### Ingestion Tool (`ingest_recipes.py`)

Processes a folder of recipe images and stores the extracted data in the database.

#### **Usage**

```bash
python ingest_recipes.py /path/to/your/image/folder
```

#### **Options**

- `/path/to/your/image/folder`: Replace with the actual path to the folder containing your recipe images.

#### **Example**

```bash
python ingest_recipes.py ./recipe_images
```

### Querying Tool (`query_recipes.py`)

Allows you to query the recipe database using natural language.

#### **Usage**

```bash
python query_recipes.py "Your search query here"
```

#### **Options**

- `"Your search query here"`: Replace with your natural language query enclosed in quotes.

#### **Example**

```bash
python query_recipes.py "Find recipes that include tomatoes and take less than 30 minutes to cook."
```

---

## Configuration

Both scripts have configuration sections where you can adjust settings:

- **Database Connection Details**: Modify the database connection parameters if needed.
- **Embedding Dimensions**: Ensure the `embed_dim` parameter matches your embedding model's output dimensions.
- **Prompt Customization**: Adjust the prompt in `extract_recipe_info` to extract additional information if required.

---

## Examples

### Ingesting Recipes

Assuming you have a folder named `recipe_images` containing recipe images:

```bash
python ingest_recipes.py ./recipe_images
```

### Querying Recipes

To find quick recipes with chicken:

```bash
python query_recipes.py "Find quick recipes that include chicken."
```

---

## Troubleshooting

### Common Issues

- **Database Connection Errors**:

  - Ensure PostgreSQL is running and accessible.
  - Check that the `pgvector` extension is installed and enabled.

- **Ollama Model Issues**:

  - Verify that the LLaVA model is correctly pulled.
  - Ensure the Ollama server is running.

- **Missing Dependencies**:

  - Install any missing packages using `pip install`.

- **Image Processing Errors**:

  - Ensure the image files are in supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`.

### Contact

If you encounter issues not covered here, please open an issue on the [GitHub repository](https://github.com/yourusername/recipe-tools/issues).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **LLaVA**: [LLaVA GitHub Repository](https://github.com/haotian-liu/LLaVA)
- **Ollama**: [Ollama Documentation](https://ollama.ai/docs)
- **LlamaIndex**: [LlamaIndex Documentation](https://gpt-index.readthedocs.io/)
- **pgvector**: [pgvector GitHub Repository](https://github.com/pgvector/pgvector)

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## Notes

- **Security**: Remember to handle your database credentials securely. Do not hardcode sensitive information in scripts or share them publicly.
- **Extensibility**: Feel free to extend the scripts to extract more information from recipes or improve the querying capabilities.

---