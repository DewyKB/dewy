---
title: Installation
sidebar_position: 1
--- 

# Installation

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