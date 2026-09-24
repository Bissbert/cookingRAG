#!python

import argparse
from llama_index.core import Settings, VectorStoreIndex
from util.embedding_util import initEmbeddingModel
from util.ingestion_model_interaction import language_model
from util.database_conection import setup_vector_store

def init_query_models():
    """
    Configure the models used to answer a query.

    The question is embedded with the same model the recipes were ingested
    with, and the answer is written by the same local LLM that structures the
    recipes during ingestion, so no query falls back to a hosted default.
    """
    initEmbeddingModel()
    Settings.llm = language_model

def search_recipes(query, storage_context):
    # Create a query engine
    index = VectorStoreIndex.from_vector_store(
        vector_store=storage_context.vector_store,
    )
    query_engine = index.as_query_engine(similarity_top_k=5)  # Adjust top_k as needed

    # Query the index
    response = query_engine.query(query)
    print("Search Results:")
    print(response)

def main():
    parser = argparse.ArgumentParser(description='Query the recipe database using natural language.')
    parser.add_argument('query', type=str, nargs='+', help='Your search query in natural language')
    args = parser.parse_args()

    search_query = ' '.join(args.query)

    init_query_models()
    storage_context = setup_vector_store()
    search_recipes(search_query, storage_context)

if __name__ == "__main__":
    main()
