#!python

import os
import sys
import uuid
import random
import logging
import asyncio
import argparse
import itertools
from pathlib import Path
from typing import Optional
from llama_index.core import VectorStoreIndex
from util.json_util import recipes_to_json
from util.ingestion_model_interaction import initModel, aprocess_image_files
from util.embedding_util import initEmbeddingModel, get_nodes_from_objs
from util.database_conection import setup_database, setup_vector_store

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_image_files(
    dir_path, sample: Optional[int] = 10, shuffle: bool = False
) -> list:
    """
    Get a list of image files from the specified directory.

    Args:
        dir_path (str): Path to the directory containing image files.
        sample (Optional[int]): Number of image files to sample. Defaults to 10.
        shuffle (bool): Whether to shuffle the image files. Defaults to False.

    Returns:
        list: List of image file paths.
    """
    dir_path = Path(dir_path)
    image_paths = []
    for image_path in itertools.chain(dir_path.glob("*.jpg"), dir_path.glob("*.jpeg"), dir_path.glob("*.png")):
        image_paths.append(image_path)

    random.shuffle(image_paths)
    if sample:
        return image_paths[:sample]
    else:
        return image_paths
    
def save_data_objects_to_json(dataObjects):
    """
    Save the dataObjects as a JSON array using the recipes_to_json method.

    Args:
        dataObjects (List[Recipe]): List of Recipe objects to save.

    Returns:
        None
    """
    json_data = recipes_to_json(dataObjects)
    filename = f"recipeExport-{uuid.uuid4()}.json"
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, 'w') as json_file:
        json_file.write(json_data)
    print(f"Data objects saved to {filepath}")

async def process_recipe_images(folder_path: str, storage_context):
    """
    Process recipe images from the specified folder and store them in the vector store.

    Args:
        folder_path (str): Path to the folder containing recipe images.
        storage_context (StorageContext): The storage context for the vector store.

    Returns:
        None
    """
    imageFiles = get_image_files(folder_path)

    if not imageFiles:
        print(f"No image files found in the specified folder: {folder_path}")
        return
    
    dataObjects = await aprocess_image_files(imageFiles)
    save_data_objects_to_json(dataObjects)
    nodes = get_nodes_from_objs(dataObjects)

    #log first 5 nodes
    for i, node in enumerate(nodes[:5]):
        print(f"Node {i+1}:")
        print(node.get_content(metadata_mode="all"))
        print()
    
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
    )

async def main():
    """
    Main function to process a folder of recipe images and store them in the database.

    This function initializes the necessary components, parses command-line arguments,
    and processes the recipe images in the specified folder.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Process a folder of recipe images and store them in the database.')
    parser.add_argument('folder', type=str, help='Path to the folder containing recipe images')
    args = parser.parse_args()

    folder_path = args.folder

    if not os.path.isdir(folder_path):
        print(f"The specified folder does not exist: {folder_path}")
        sys.exit(1)

    # init components
    initModel()
    initEmbeddingModel()
    setup_database()
    storage_context = setup_vector_store()

    # Process the recipe images in the folder
    await process_recipe_images(folder_path, storage_context)

if __name__ == "__main__":
    asyncio.run(main())
