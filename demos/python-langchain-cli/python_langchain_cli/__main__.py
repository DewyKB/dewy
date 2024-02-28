import os
import sys

import click
from dewy_client import Client


@click.group()
@click.option("--collection", default="main")
@click.option("--base_url", default="http://localhost:8000")
@click.pass_context
def cli(ctx, collection, base_url):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj["base_url"] = base_url
    ctx.obj["collection"] = collection


@cli.command()
@click.pass_context
@click.argument("url_or_file")
def add_file(ctx, url_or_file):
    from dewy_client.api.kb import add_document, upload_document_content
    from dewy_client.models import AddDocumentRequest, BodyUploadDocumentContent
    from dewy_client.types import File

    client = Client(ctx.obj["base_url"])
    if os.path.isfile(url_or_file):
        document = add_document.sync(
            client=client,
            body=AddDocumentRequest(
                collection=ctx.obj["collection"],
            ),
        )
        print(f"Added document {document.id}. Uploading content.")

        with open(url_or_file, "rb") as file:
            payload = file.read()
            upload_document_content.sync(
                document.id,
                client=client,
                body=BodyUploadDocumentContent(
                    content=File(
                        payload=payload,
                        file_name=os.path.basename(url_or_file),
                    ),
                ),
            )
        print(f"Uploaded content for document {document.id}.")

    else:
        document = add_document.sync(
            client=client,
            body=AddDocumentRequest(collection=ctx.obj["collection"], url=url_or_file),
        )
        print(f"Added document {document.id} from URL '{url_or_file}'")


@cli.command()
@click.pass_context
@click.argument("query", type=click.File("r"), default=sys.stdin)
def query(ctx, query):
    from dewy_langchain import DewyRetriever
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai import ChatOpenAI

    retriever = DewyRetriever.for_collection(
        collection=ctx.obj["collection"], base_url=ctx.obj["base_url"]
    )

    prompt = ChatPromptTemplate.from_template(
        """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    )

    model = ChatOpenAI()

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    query_str = query.read()
    print(f"Invoking chain for:\n{query_str}")
    result = chain.invoke(query_str)
    print(f"\n\nAnswer:\n{result}")


if __name__ == "__main__":
    cli()
