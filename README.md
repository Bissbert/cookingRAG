<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">COOKINGRAG</h1>
</p>
<p align="center">
    <em>Ingestion and processing of recipe images* Query functionality for natural language input* Efficient data management through vector store index* Retrieval of recipes via a user-friendly interfaceThe phrase One Bite at Time" conveys the idea that cookingRAG makes it easy to access and explore recipes, making it a relatable and engaging experience for users.</em>
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
- [🛠 Project Roadmap](#-project-roadmap)
- [🤝 Contributing](#-contributing)
- [🎗 License](#-license)
- [🔗 Acknowledgments](#-acknowledgments)
</details>
<hr>

## 📍 Overview

CookingRAG is an open-source software project designed to facilitate efficient data management and retrieval for cooking recipes. The platform enables users to ingest, process, and query recipe images and metadata through its robust architecture, which integrates various utility modules such as database connections, vector store indexing, and model initialization. CookingRAG provides a value proposition by offering a unified interface for data ingestion and processing, allowing users to easily search and retrieve recipes based on natural language inputs. This projects core functionalities cater to the needs of cooking enthusiasts and professionals alike, streamlining recipe discovery and management.

---

## 🧩 Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | The cookingRAG project appears to be built using a microservices architecture, with each module serving a specific purpose. The codebase is designed for modularity and reusability, allowing for efficient data management and scalability. |
| 🔩 | **Code Quality**   | The code quality is generally good, with clear and concise documentation and well-structured modules. However, there are some areas where the code could benefit from additional comments and error handling to improve maintainability. |
| 📄 | **Documentation**  | The project has extensive documentation, including repository contents, module descriptions, and usage examples. This makes it easy for users to understand how to integrate and use each component of the cookingRAG system. |
| 🔌 | **Integrations**    | The cookingRAG project integrates with various external dependencies, including Python, PostgreSQL, and OllamaEmbedding model. These integrations enable efficient data processing, storage, and retrieval. |
| 🧩 | **Modularity**      | The codebase is highly modular, allowing for easy maintenance and extension of individual components. This modularity also enables scalability, as new modules can be added or removed without affecting the entire system. |
| 🧪 | **Testing**         | Testing frameworks are not explicitly mentioned in the provided codebase details. No automated Testing is done, only hand tests up to this point|
| ⚡️  | **Performance**    | The cookingRAG system seems to be designed for performance, with optimized data processing, storage, and retrieval mechanisms. The use of the OllamaEmbedding model also improves efficiency in text data processing. |
| 🛡️ | **Security**        | Security measures are not explicitly mentioned in the provided codebase details. However, it is assumed that standard security best practices have been followed to protect user data and prevent unauthorized access. |
| 📦 | **Dependencies**    | The project has a small number of dependencies, including Python and an OllamaEmbedding model. This reduces the risk of security vulnerabilities and makes maintenance easier. |
| 🚀 | **Scalability**      | The cookingRAG system appears to be designed for scalability, with modular components that can be easily added or removed as needed. This enables efficient handling of increased traffic and load, making it suitable for large-scale applications. |

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
        ├── json_util.py
        └── recipe.py
```

---

## 📦 Modules

<details closed><summary>.</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [ingest_recipes.py](https://github.com/Bissbert/cookingRAG/blob/master/ingest_recipes.py) | The ingest_recipes.py file orchestrates the processing of recipe images, creating a vector store index for storage.Achieves: Organizes the ingestion of image files from a specified directory into the database, utilizing model initialization and embedding functionality for efficient data representation.Resolves: Key functionalities within the parent repositorys architecture by integrating with other utility modules, ensuring comprehensive data management. |
| [query_recipes.py](https://github.com/Bissbert/cookingRAG/blob/master/query_recipes.py)   | Activate functionality in query_recipes.py by querying the recipe database using natural language input. Achieves this through configuration-based setup of a vector store index and similarity search engine, ultimately providing search results for a given query. Facilitates data retrieval from the database via a user-friendly interface.                                                                                                                          |

</details>

<details closed><summary>util</summary>

| File                                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                                                        |
| [embedding_util.py](https://github.com/Bissbert/cookingRAG/blob/master/util/embedding_util.py)                           | Initiates the embedding model settings for the cooking recipe database, utilizing the OllamaEmbedding model to process text data. Converts a list of Recipe objects into a list of TextNode objects, incorporating metadata and formatting instructions. Enhances the repositorys architecture by providing a uniform interface for data ingestion and processing.                         |
| [database_conection.py](https://github.com/Bissbert/cookingRAG/blob/master/util/database_conection.py)                   | Establishes connections to a PostgreSQL database, creating it if necessary. Configures the PGVectorStore and StorageContext for vector storage, utilizing environment variables for connection details. Provides setup functions for database creation and initialization of the vector store and storage context.                                                                         |
| [ingestion_model_interaction.py](https://github.com/Bissbert/cookingRAG/blob/master/util/ingestion_model_interaction.py) | Process Recipe Information------------------------Extracts recipe information from image files using an LLaVA-based model, processing metadata on multiple images concurrently. This module orchestrates tasks to run the LLM program, handling loading image data and output parsing. It serves as a crucial component in the repositorys architecture for handling ingestions.           |
| [json_util](https://github.com/Bissbert/cookingRAG/blob/master/util/json_util)                                           | Converts a list of Recipe objects to a JSON string representation, enabling seamless data exchange between systems. Achieves this by serializing the recipe data into a structured format, facilitating efficient ingestion and querying of recipes within the cookingRAG repositorys architecture.                                                                                        |
| [recipe.py](https://github.com/Bissbert/cookingRAG/blob/master/util/recipe.py)                                           | A data model for recipes in the cookingRAG repository.Achieves: Defines two main classes, Ingredient and Recipe, to represent components of recipe data. These models ensure structured and consistent data storage and retrieval in the database.Relates to: Database connection implementation (database_conection.py) and ingestion model interaction (ingestion_model_interaction.py). |

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

Not runnable yet

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

This project is protected under the [MIT](./LICENSE) License.

---

## 🔗 Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
