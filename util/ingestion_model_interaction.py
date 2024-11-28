
from llama_index.core import Settings, SimpleDirectoryReader, run_jobs
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from util.recipe import Recipe

# Initialize the Ollama LLM with the LLaVA model
llm = OllamaMultiModal(model="llava:13b", request_timeout=120.0)

prompt_template_str = """\
    Can you extract the recipe from the image and return a response \
    with the following JSON format: \
"""

def initModel():
    Settings.llm = llm

async def pydantic_llm(output_class, image_documents, prompt_template_str):

    llm_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(output_class),
        image_documents=image_documents,
        prompt_template_str=prompt_template_str,
        multi_modal_llm=llm,
        verbose=True,
    )

    response = await llm_program.acall()
    return response

async def aprocess_image_file(image_file):
    # should load one file
    print(f"Image file: {image_file}")
    img_docs = SimpleDirectoryReader(input_files=[image_file]).load_data()
    output = await pydantic_llm(Recipe, img_docs, prompt_template_str)
    return output

async def aprocess_image_files(image_files):
    """Process metadata on image files."""
    tasks = []
    for image_file in image_files:
        task = aprocess_image_file(image_file)
        tasks.append(task)

    outputs = await run_jobs(tasks, show_progress=True, workers=5)
    return outputs