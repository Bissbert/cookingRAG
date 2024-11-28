#!python

import os
import sys
import random
import asyncio
import argparse
import itertools
from pathlib import Path
from typing import Optional
from tqdm import tqdm
from llama_index.core import VectorStoreIndex
from util.ingestion_model_interaction import initModel, aprocess_image_files
from util.embedding_util import initEmbeddingModel, get_nodes_from_objs
from util.database_conection import setup_database, setup_vector_store

def get_image_files(
    dir_path, sample: Optional[int] = 10, shuffle: bool = False
) -> list:
    dir_path = Path(dir_path)
    image_paths = []
    for image_path in itertools.chain(dir_path.glob("*.jpg"), dir_path.glob("*.jpeg"), dir_path.glob("*.png")):
        image_paths.append(image_path)

    random.shuffle(image_paths)
    if sample:
        return image_paths[:sample]
    else:
        return image_paths

async def process_recipe_images(folder_path: str, storage_context):
    imageFiles = get_image_files(folder_path)

    if not imageFiles:
        print(f"No image files found in the specified folder: {folder_path}")
        return
    
    dataObjects = await aprocess_image_files(imageFiles)
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
    process_recipe_images(folder_path, storage_context)

if __name__ == "__main__":
    asyncio.run(main())
