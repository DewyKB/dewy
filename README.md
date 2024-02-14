<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DewyKB/dewy">
    <img src="https://github.com/DewyKB/dewy/raw/main/images/logo.png" alt="Logo" width="160" height="160">
  </a>

<h3 align="center">Dewy - The Knowledgebase for AI</h3>

  <p align="center">
    Opinionated knowledge extraction and semantic retrieval for Gen AI applications.
    <br />
    <a href="https://github.com/DewyKB/dewy"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/DewyKB/dewy/issues">Report Bug</a>
    ·
    <a href="https://github.com/DewyKB/dewy/issues">Request Feature</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

Dewy helps you build AI agents and RAG applications by managing the extraction of knowledge from your documents and implementing semantic search over the extracted content.
Load your documents and Dewy takes care of parsing, chunking, summarizing, and indexing for retrieval.
Dewy builds on the lessons of putting real Gen AI applications into production so you can focus on getting 💩 done, rather than comparing vector databases and building data extraction infrastructure.

Below is the typical architecture of an AI agent performing RAG.
Dewy handles all of the parts shown in brown so you can focus on your application -- the parts in green.

<p align="center">
  <img src="https://github.com/DewyKB/dewy/raw/main/images/app_architecture.png" alt="System architecture showing steps of RAG." width="600px">
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

1. (Optional) Start a `pgvector` instance to persist your data

    Dewy uses a vector database to store metadata about the documents you've loaded as well as embeddings used to provide semantic search results.

    ```sh
    docker run -d \
      -p 5432:5432 \
      -e POSTGRES_DB=dewydb \
      -e POSTGRES_USER=dewydbuser \
      -e POSTGRES_PASSWORD=dewydbpwd \
      -e POSTGRES_HOST_AUTH_METHOD=trust \
      ankane/pgvector
    ```
    If you already have an instance of `pgvector` you can create a database for Dewy and configure Dewy use it using the `DB` env var (see below).

1. Install Dewy
    ```
    pip install dewy
    ```

    This will install Dewy in your local Python environment.

1. Configure Dewy.
    Dewy will read env vars from an `.env` file if provided. You can also set these directly
    in the environment, for example when configuring an instance running in docker / kubernetes.

    ```sh
    # ~/.env
    ENVIRONMENT=LOCAL
    DB=postgresql://...
    OPENAI_API_KEY=...
    ```

1. Fire up Dewy
    ```sh
    dewy
    ```

    Dewy includes an admin console you can use to create collections, load documents, and run test queries.

    ```sh
    open http://localhost:8000/admin
    ```

### Using Dewy in Typescript / Javascript

1. Install the API client library
    ```sh
    npm install dewy-ts
    ```

1. Connect to an instance of Dewy
    ```typescript
    import { Dewy } from 'dewy_ts';
    const dewy = new Dewy()
    ```

1. Add documents
    ```typescript
    await dewy.kb.addDocument({
      collection_id: 1,
      url: “https://arxiv.org/abs/2005.11401”,
    })
    ```

1. Retrieve document chunks for LLM prompting
    ```typescript
    const context = await dewy.kb.retrieveChunks({
      collection_id: 1,
      query: "tell me about RAG",
      n: 10,
    });

    // Minimal prompt example
    const prompt = [
      {
        role: 'system',
        content: `You are a helpful assistant.
        You will take into account any CONTEXT BLOCK that is provided in a conversation.
        START CONTEXT BLOCK
        ${context.results.map((c: any) => c.chunk.text).join("\n")}
        END OF CONTEXT BLOCK
        `,
      },
    ]

    // Using OpenAI to generate responses
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      stream: true,
      messages: [...prompt, [{role: 'user': content: 'Tell me about RAG'}]]
    })
    ```

### Using Dewy in Python

1. Install the API client library
    ```sh
    pip install dewy-client
    ```

1. Connect to an instance of Dewy
    ```python
    from dewy_client import Client
    dewy = Client(base_url="http://localhost:8000")
    ```

1. Add documents
    ```python
    from dewy_client.api.kb import add_document
    from dewy_client.models import AddDocumentRequest
    await add_document.asyncio(client=dewy, body=AddDocumentRequest(
      collection_id = 1,
      url = “https://arxiv.org/abs/2005.11401”,
    ))
    ```

1. Retrieve document chunks for LLM prompting
    ```python
    from dewy_client.api.kb import retrieve_chunks
    from dewy_client.modles import RetrieveRequest
    chunks = await retrieve_chunks.asyncio(client=dewy, body=RetrieveRequest(
      collection_id = 1,
      query = "tell me about RAG",
      n = 10,
    ))

    # Minimal prompt example
    prompt = f"""
    You will take into account any CONTEXT BLOCK that is provided in a conversation.
      START CONTEXT BLOCK
      {"\n".join([chunk.text for chunk in chunks.text_results])}
      END OF CONTEXT BLOCK
    """
    ```

See [`python-langchain.ipynb'](demos/python-langchain-notebook/python-langchain.ipynb) for an example using Dewy in LangChain, including an implementation of LangChain's `BaseRetriever` backed by Dewy.

## Roadmap

Dewy is under active development.
This is an overview of our current roadmap - please 👍 issues that are important to you.
Don't see a feature that would make Dewy better for your application - [create a feature request](https://github.com/DewyKB/dewy/issues)!

* Support more document formats (ie [Markdown](https://github.com/DewyKB/dewy/issues/29), [DOCX](https://github.com/DewyKB/dewy/issues/28), [HTML](https://github.com/DewyKB/dewy/issues/27))
* Support more types of chunk extractors
* Multi-modal search over images, tables, audio, etc.
* Integrations with LangChain, LlamaIndex, Haystack, etc.
* Support flexible result ranking (ie rag-fusion, mmr, etc).
* Provide metrics around which chunks are used, relevance scores, etc.
* Query history and explorer in the UI.
* Multi-tenancy
* Hybrid search

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Installation

1. Clone the repo
    ```sh
    git clone https://github.com/DewyKB/dewy.git
    ```
1. Install Python packages
    ```sh
    poetry install
    ```
1. Configure Dewy.
    Dewy will read env vars from an `.env` file if provided. You can also set these directly
    in the environment, for example when configuring an instance running in docker / kubernetes.
    ```sh
    cat > .env << EOF
    ENVIRONMENT=LOCAL
    DB=postgresql://...
    OPENAI_API_KEY=...
    EOF
    ```
1. Build the frontend
    ```sh
    cd frontend && npm install && npm run build
    ```
1. Run the Dewy service
    ```sh
    poetry run dewy
    ```

### Practices

Some skeleton code based on best practices from https://github.com/zhanymkanov/fastapi-best-practices.

The following commands run tests and apply linting.
If you're in a `poetry shell`, you can omit the `poetry run`:

* Running tests: `poetry run pytest`
* Linting (and formatting): `poetry run ruff check --fix`
* Formatting: `poetry run ruff format`
* Type Checking: `poetry run mypy app`


<p align="right">(<a href="#readme-top">back to top</a>)</p

### Releasing

1. Look at the [draft release](https://github.com/DewyKB/dewy/releases) to determine the suggested next version.
2. Create a PR updating the following locations to that version:
  a. [`pyproject.toml`](https://github.com/DewyKB/dewy/blob/main/pyproject.toml#L3) for `dewy`
  b. [`pyproject.toml`](https://github.com/DewyKB/dewy/blob/main/dewy-client/pyproject.toml#L3) for `dewy-client`
  c. API version in [`config.py`](https://github.com/DewyKB/dewy/blob/main/dewy/config.py#L69)
  d. `openapi.yaml` and `dewy-client` by running `poe extract-openapi` and `poe update-client`.
3. Once that PR is in, edit the draft release, make sure the version and tag match what you selected in step 1 (and used in the PR), check "Set as a pre-release" (will be updated by the release automation) and choose to publish the release.
4. The release automation should kick in and work through the release steps. It will need approval for the pypi deployment environment to publish the `dewy` and `dewy-client` packages.

<p align="right">(<a href="#readme-top">back to top</a>)</p

<!-- LICENSE -->
## License

Distributed under the Apache 2 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
