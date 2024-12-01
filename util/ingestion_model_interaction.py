
import logging
import time
from llama_index.core import Settings, SimpleDirectoryReader
from llama_index.core.async_utils import run_jobs
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from llama_index.llms.ollama import Ollama
from ollama._types import ResponseError
from util.recipe import Recipe

# Initialize the Ollama Multimodal Model
multimodal_model = OllamaMultiModal(model="llama3.2-vision:90b", request_timeout=600.0)

# Initialize the Ollama Language Model
language_model = Ollama(model="qwq", request_timeout=600.0)

image_extraction_prompt = """\
Extract the recipe from the provided image.
Ensure the instructions are clear by naming all ingredients involved.\
If the document is in a language other than English, translate all ingredients and instructions into English.\
Use the listed ingredients to deduce the dietary preference (e.g., vegetarian, vegan, gluten-free, etc.).\
Do not assume the dietary preference is explicitly stated; instead, infer it logically. Keep the dietary preferences short and precice.

"""
print("image_extraction_prompt is: ", image_extraction_prompt)

recipe_to_json_template = """
Input Recipe:
{recipe}

Objective:
Transform the provided recipe string into a structured format compliant with the specified Pydantic model below. Each field in the model should be accurately populated based on the information provided in the recipe. Ensure all necessary parsing and formatting is done correctly. Any ambiguous or missing information should be handled gracefully, with fields left as `None` where appropriate.

Expected Output:
Return a Python dictionary representing the data, formatted to match the Pydantic model structure.

Pydantic Model Definition:
"""
print("recipe_to_json_template is: ", recipe_to_json_template)



def initModel():
    """
    Initialize the model settings.

    This function sets the global LLM settings to use the initialized Ollama LLM.
    """
    #Settings.llm = llm

def pydantic_llm(output_class, image_documents, image_extraction_prompt, recipe_to_json_template, retries=3, delay=5):
    """
    Run the LLM program with the given output class, image documents, and prompt template.

    Args:
        output_class (Type): The Pydantic model class to parse the output.
        image_documents (List[Document]): List of image documents to process.
        prompt_template_str (str): The prompt template string to use.
        retries (int): Number of retries for the request.
        delay (int): Delay between retries in seconds.

    Returns:
        Any: The response from the LLM program.
    """
    for attempt in range(retries):
        try:
            recipe = multimodal_model.complete(
                prompt=image_extraction_prompt,
                image_documents=image_documents,
            )
            logging.info("Recipe extraction successful.")
            logging.info(recipe)
            break
        except ResponseError as e:
            logging.error(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise
    

    llm_program = LLMTextCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(output_class),
        prompt_template_str=recipe_to_json_template,
        llm=language_model,
        verbose=True,
    )

    for attempt in range(retries):
        try:
            logging.info("Running LLM program with extracted recipe:")
            logging.info(recipe)
            raw_output = llm_program(recipe=recipe)
            logging.info(f"Raw output from LLM program: {raw_output}")
            output = raw_output
            break
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

    return output

def aprocess_image_file(image_file):
    """
    Process a single image file to extract recipe information.

    Args:
        image_file (str): Path to the image file.

    Returns:
        Any: The extracted recipe information.
    """
    # should load one file
    print(f"Image file: {image_file}")
    img_docs = SimpleDirectoryReader(input_files=[image_file]).load_data()
    output = pydantic_llm(Recipe, img_docs, image_extraction_prompt, recipe_to_json_template)
    return output

async def aprocess_image_files(image_files):
    """
    Process metadata on multiple image files.

    Args:
        image_files (List[str]): List of paths to image files.

    Returns:
        List[Any]: List of extracted recipe information for each image file.
    """
    outputs = []
    for image_file in image_files:
        output = aprocess_image_file(image_file)
        outputs.append(output)

    print("created all tasks, now running processing")
    #outputs = await run_jobs(tasks, show_progress=True, workers=5)
    return outputs