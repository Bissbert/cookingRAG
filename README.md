<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">COOKINGRAG</h1>
</p>
<p align="center">
    <em>Find Recipes, One Ingredient at a Time"This slogan captures the essence of cookingRAGs purpose, emphasizing the idea of discovering recipes through a modular and efficient system that integrates with various utility modules. It is concise, memorable, and engaging, inviting users to explore the project's capabilities. The phrase also hints at the AI-powered aspect of the project, using one ingredient as a metaphor for the data ingestion and processing process.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/Bissbert/cookingRAG?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=#4CAF50" alt="license">
	<img src="https://img.shields.io/github/last-commit/Bissbert/cookingRAG?style=for-the-badge&logo=git&logoColor=white&color=#4CAF50" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Bissbert/cookingRAG?style=for-the-badge&color=#4CAF50" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Bissbert/cookingRAG?style=for-the-badge&color=#4CAF50" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python">
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [📍 Overview](#-overview)
- [🧩 Features](#-features)
- [🗂️ Repository Structure](#️-repository-structure)
- [📦 Modules](#-modules)
- [🚀 Getting Started](#-getting-started)
  - [⚙️ Installation](#️-installation)
  - [🤖 Usage](#-usage)
  - [🧪 Tests](#-tests)
- [🛠 Project Roadmap](#-project-roadmap)
- [🤝 Contributing](#-contributing)
- [🎗 License](#-license)
- [🔗 Acknowledgments](#-acknowledgments)
</details>
<hr>

## 📍 Overview

CookingRAG is an open-source software project that enables users to discover and explore recipes through natural language queries. The system ingest images from specific folders, store them in vector stores, and connect to database connections for efficient search and retrieval of recipes. It facilitates the creation of a standardized way to represent culinary data through its Recipe model, ensuring consistency in data storage and querying. CookingRAG provides value by allowing users to easily query and retrieve recipe information using natural language queries, making it an effective tool for those seeking cooking inspiration or looking to discover new recipes.

---

## 🧩 Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The architecture is modular, with multiple utility modules (e.g., `util/embedding_util.py`, `util/database_conection.py`) that work together to achieve the project's goals. Each module is designed to be reusable and can be easily integrated into other parts of the project. |
| 🔩 | **Code Quality**  | The code has good readability, with clear and concise comments throughout. The use of a standardized structure for recipes (e.g., `util/recipe.py`) and well-organized files contribute to maintainable code quality. However, some minor improvements could be made in terms of naming conventions and documentation consistency. |
| 📄 | **Documentation**  | Although the project has some basic documentation, it is somewhat limited in its scope. Better documentation would help new users understand how to use the project effectively and would provide more context for developers working on the codebase. Some examples could include API documentation for utility modules or explanations of specific algorithms used in the project. |
| 🔌 | **Integrations**  | The project integrates with various external dependencies, including:
	+ `py`: Python library
	+ `python`: Python framework ( likely a custom implementation)
	+ PostgreSQL: database connection through `util/database_conection.py`
	*   Ollama MultiModal LLM: for image processing and recipe embeddings
	+ `json` module: for transforming data into JSON format |
| 🧩 | **Modularity**    | The codebase is designed to be modular, with separate utility modules (e.g., `util/embedding_util.py`, `util/database_conection.py`) that can be easily reused and integrated into other parts of the project. This modularity contributes to maintainability and scalability. |
| 🧪 | **Testing**       | Although there is no explicit testing information provided, it is likely that unit tests are included in the codebase to verify individual modules' functionality. The use of clear naming conventions (e.g., `util/recipe.py`) also suggests a focus on maintainability and testability. |
| ⚡️  | **Performance**   | Without specific performance metrics or benchmarks, it is difficult to assess efficiency and speed. However, the project's design, which separates concerns into multiple utility modules, could help improve performance by allowing each module to optimize for its specific task. |
| 🛡️ | **Security**      | The codebase does not appear to have any explicitly stated security measures or protections. However, the use of environment variables for database credentials in `util/database_conection.py` suggests that some basic access control and data protection are being taken. More comprehensive security measures (e.g., authentication, encryption) might be necessary depending on the project's specific requirements |
| 📦 | **Dependencies**  | The project has a few external dependencies:
	+ `py`: Python library

---

## 🗂️ Repository Structure

```sh
└── cookingRAG/
    ├── LICENSE
    ├── ingest_recipes.py
    ├── query_recipes.py
    └── util
        ├── database_conection.py
        ├── embedding_util.py
        ├── ingestion_model_interaction.py
        ├── json_util
        └── recipe.py
```

---

## 📦 Modules

<details closed><summary>.</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                                                                       |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                                                           |
| [ingest_recipes.py](https://github.com/Bissbert/cookingRAG/blob/master/ingest_recipes.py) | Process recipe images from specified folders and store them in vector stores, integrating with database connections and embedding models. Achieves image data ingestion and storage for cooking recipes, utilizing a modular architecture across multiple utility modules within the repository.                                              |
| [query_recipes.py](https://github.com/Bissbert/cookingRAG/blob/master/query_recipes.py)   | Describe Retrieves Recipes from Database Using Natural Language Query. This script enables users to query the recipe database using natural language queries, leveraging an embedding model for efficient search and retrieval of recipes. It sets up a vector store index, performs searches, and prints results in a human-readable format. |

</details>

<details closed><summary>util</summary>

| File                                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                |
| ---                                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                    |
| [embedding_util.py](https://github.com/Bissbert/cookingRAG/blob/master/util/embedding_util.py)                           | The embedding_util.py file plays a crucial role in initializing the Ollama embedding model settings for the cookingRAG repositorys architecture. It enables the utilization of this model for recipe embeddings, contributing to the overall functionality and data representation within the parent recipes repository structure.                     |
| [database_conection.py](https://github.com/Bissbert/cookingRAG/blob/master/util/database_conection.py)                   | Connects to a PostgreSQL database using environment variables for credentials, checks if the database exists, and creates it if necessary. Initializes a PGVectorStore and StorageContext, which are used to interact with the vector store in the repositorys architecture. Establishes a connection to the database for data retrieval.              |
| [ingestion_model_interaction.py](https://github.com/Bissbert/cookingRAG/blob/master/util/ingestion_model_interaction.py) | Extracts recipe information from image files using an AI-powered LLM model. Establishes a connection with the Ollama MultiModal LLM, processes images, and returns extracted recipes in JSON format. Facilitates batch processing of multiple image files. Acts as a utility function for ingesting recipe data into the cookingRAG repository.        |
| [json_util](https://github.com/Bissbert/cookingRAG/blob/master/util/json_util)                                           | Transforms a list of Recipe objects into a JSON string, utilizing the `json` module and dictionary methods to create a formatted output. Achieves its purpose by converting complex data structures into a human-readable format suitable for storage or transfer in the parent repositorys architecture, facilitating data exchange between modules.  |
| [recipe.py](https://github.com/Bissbert/cookingRAG/blob/master/util/recipe.py)                                           | Defines recipes structure with Ingredient and Recipe models, providing a standardized way to represent culinary data. Validates recipe attributes using Pydantics BaseModel and Field, ensuring consistency across the repositorys ingest_recipes.py and query_recipes.py files. Establishes a foundation for database ingestion and querying recipes. |

</details>

---

## 🚀 Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

### ⚙️ Installation

<h4>From <code>source</code></h4>

> 1. Clone the cookingRAG repository:
>
> ```console
> $ git clone https://github.com/Bissbert/cookingRAG
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd cookingRAG
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

### 🤖 Usage

<h4>From <code>source</code></h4>

> Run cookingRAG using the command below:
> ```console
> $ python main.py
> ```

### 🧪 Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

## 🛠 Project Roadmap
- [ ] `► ensure ingestion runnable`
- [ ] `► collect data for ingestion`
- [ ] `► add query functionality`
- [ ] `► create webapp for serving functionality`
- [ ] `► create UI for mobile`
- [ ] `► add submission of new recipe`
- [ ] `► finetuning of models for better results and speed`
  - [ ]  `► embedding model`
  - [ ]  `► image detection model`
  - [ ]  `► query model`

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/Bissbert/cookingRAG/issues)**: Submit bugs found or log feature requests for the `cookingRAG` project.
- **[Submit Pull Requests](https://github.com/Bissbert/cookingRAG/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Bissbert/cookingRAG/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/Bissbert/cookingRAG
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/Bissbert/cookingRAG/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Bissbert/cookingRAG">
   </a>
</p>
</details>

---

## 🎗 License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## 🔗 Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
