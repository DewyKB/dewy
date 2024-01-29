<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/DewyKB/dewy">
    <img src="images/logo.png" alt="Logo" width="160" height="160">
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
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

Dewy helps you build AI agents and RAG applications by managing the extraction of knowledge from your documents and implementing semantic search over the extracted content.
Load your documents and Dewy takes care of parsing, chunking, summarizing, and indexing for retrieval
Dewy builds on the lessons of putting real Gen AI applications into production so you can focus on getting 💩 done, rather than comparing vector databases and building data extraction infrastructure.

Below is the typical architecture of an AI agent performing RAG.
Dewy handles all of the parts shown in brown, letting you focus on your application -- the parts in green.

<p align="center">
  <img src="images/app_architecture.png" alt="System architecture showing steps of RAG." width="600px">
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

1. (Optional) Start a `pgvector` instance to persist your data
    ```sh
    docker run -d \
      -p 5432:5432 \
      -e POSTGRES_DB=dewydb \
      -e POSTGRES_USER=dewydbuser \
      -e POSTGRES_PASSWORD=dewydbpwd \
      -e POSTGRES_HOST_AUTH_METHOD=trust \
      ankane/pgvector
    ```
1. Install Dewy
    ```
    pip install dewy
    ```
1. Fire up Dewy
    ```sh
    // Configure your OpenAI key (optional - local models will be used if not provided)
    export OPENAI_API_KEY=...

    // Configure your pgvector endpoint (this assumes you installed with Docker as shown previously)
    export DB=postgresql://dewydbuser:dewydbpwd@localhost/dewydb

    // Run the docker container
    dewy

    // Go to the management console to start creating resources!
    open http://localhost/admin
    ```
1. Install the API client library
    ```sh
    npm install dewy-ts
    ```
1. Add documents
    ```typescript
    import { Dewy } from 'dewy_ts';
    const dewy = new Dewy({endpoint: “localhost:3000”})

    await dewy.addDocument({url: “https://arxiv.org/abs/2005.11401”})
1. Retrieve document chunks for LLM prompting
    ```typescript
    import { Dewy } from 'dewy_ts';
    const dewy = new Dewy({endpoint: “localhost:3000”})

    const context = await dewy.retrieveChunks({query: "tell me about RAG", n: 10});

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

    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      stream: true,
      messages: [...prompt, [{role: 'user': content: 'Tell me about RAG'}]]
    })
    ```

Swagger docs at `http://localhost:8000/docs`.
Notebook `example_notebook.ipynb` uses the REST API from Python.

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

<!-- LICENSE -->
## License

Distributed under the Apache 2 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
