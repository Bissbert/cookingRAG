#!python

import os
import argparse
from llama_index import StorageContext, VectorStoreIndex
from llama_index.vector_stores import PGVectorStore

# === Configuration ===

# Database connection details
PG_HOST = os.environ.get('PG_HOST', 'localhost')
PG_PORT = os.environ.get('PG_PORT', '5432')
PG_USER = os.environ.get('PG_USER', 'postgres')
PG_PASSWORD = os.environ.get('PG_PASSWORD', 'your_database_password')  # Replace with your password or use environment variable
PG_DB_NAME = os.environ.get('PG_DB_NAME', 'recipe_db')

def setup_vector_store():
    vector_store = PGVectorStore.from_params(
        database=PG_DB_NAME,
        host=PG_HOST,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        table_name="recipes",
        embed_dim=1536,  # Adjust based on your embedding model
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return storage_context

def search_recipes(query, storage_context):
    # Create a query engine
    index = VectorStoreIndex(storage_context=storage_context)
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

    storage_context = setup_vector_store()
    search_recipes(search_query, storage_context)

if __name__ == "__main__":
    main()
