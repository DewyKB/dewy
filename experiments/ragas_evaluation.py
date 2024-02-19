from functools import lru_cache
import json
from operator import itemgetter
import os
import random
import string
from typing import Any, Dict, List, Literal
import uuid
from attr import dataclass
import click
from dotenv import load_dotenv
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from datasets import Dataset
from pydantic import BaseModel, Field
from tqdm import tqdm

# Load environment variables from `.env`
load_dotenv()

@dataclass
class QAExample:
    query: str
    ground_truth: str


def load_examples() -> List[QAExample]:
    import json
    dataset = []
    with open('./datasets/history_of_alexnet/rag_dataset.json') as f:
        data = json.load(f)
        for example in data["examples"]:
            dataset.append(QAExample(
                query = example["query"],
                ground_truth = example["reference_answer"]
            ))

    return dataset

from langchain_community.document_loaders.base import BaseLoader
from langchain_core.embeddings import Embeddings
from langchain_community.document_loaders import PyPDFLoader, UnstructuredFileLoader, PyMuPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings, HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.retrievers import BaseRetriever
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever, MultiVectorRetriever
from langchain_core.documents import Document

def _indexing_recursive(collection_name: str, loader: BaseLoader, embedding: Embeddings, search_type: Literal["similarity", "mmr"]) -> BaseRetriever:
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    splits = loader.load_and_split(text_splitter=text_splitter)
    vectorstore = Chroma.from_documents(collection_name=collection_name,
                                        documents=splits,
                                        embedding=embedding)

    return vectorstore.as_retriever(search_type=search_type)

def _indexing_semantic(collection_name: str, loader: BaseLoader, embedding: Embeddings, search_type: Literal["similarity", "mmr"]) -> BaseRetriever:
    text_splitter = SemanticChunker(embedding)
    splits = loader.load_and_split(text_splitter=text_splitter)
    vectorstore = Chroma.from_documents(collection_name=collection_name,
                                        documents=splits,
                                        embedding=embedding)

    return vectorstore.as_retriever(search_type=search_type)

def _indexing_parent(collection_name: str, loader: BaseLoader, embedding: Embeddings, search_type: Literal["similarity", "mmr"]) -> BaseRetriever:
    vectorstore = Chroma(collection_name=collection_name, embedding_function=embedding)
    docstore = InMemoryStore()

    child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)

    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=docstore,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
        search_type=search_type,
    )
    retriever.add_documents(loader.load(), ids=None)
    return retriever

class HypotheticalQuestions(BaseModel):
    """Return hypothetical questions."""

    questions: List[str] = Field(description="hypothetical questions")

@lru_cache
def _questions_chain() -> Runnable:
    from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
    functions = [
        {
            "name": "hypothetical_questions",
            "description": "Generate hypothetical questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["questions"],
            },
        }
    ]

    chain = (
        {"doc": lambda x: x.page_content}
        | ChatPromptTemplate.from_template(
            "Generate a list of exactly 3 hypothetical questions that the below document could be used to answer:\n\n{doc}"
        )
        | QUESTION_GENERATION_LLM.bind(
            functions=functions,
            function_call={"name": "hypothetical_questions"}
        )
        | JsonKeyOutputFunctionsParser(key_name="questions")
    )
    return chain


def _indexing_questions(collection_name: str,
                        text_splitter: TextSplitter,
                        loader: BaseLoader,
                        embedding: Embeddings,
                        search_type: Literal["similarity", "mmr"]) -> BaseRetriever:
    docs = loader.load_and_split(text_splitter=text_splitter)

    vectorstore = Chroma(collection_name=collection_name, embedding_function=embedding)
    docstore = InMemoryStore()
    id_key = "doc_id"

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        byte_store=docstore,
        id_key=id_key,
        search_type=search_type,
    )

    doc_ids = [str(uuid.uuid4()) for _ in docs]

    hypothetical_questions = _questions_chain().batch(docs, {"max_concurrency": 5})
    question_docs = []
    for i, question_list in enumerate(hypothetical_questions):
        question_docs.extend(
            [Document(page_content=s, metadata={id_key: doc_ids[i]}) for s in question_list]
        )

    retriever.vectorstore.add_documents(question_docs)
    retriever.docstore.mset(list(zip(doc_ids, docs)))

    return retriever

def _indexing_questions_semantic(collection_name: str, loader: BaseLoader, embedding: Embeddings, search_type: Literal["similarity", "mmr"]) -> BaseRetriever:
    text_splitter = SemanticChunker(embedding)
    return _indexing_questions(collection_name, text_splitter, loader, embedding, search_type)

def _indexing_questions_recursive(collection_name: str, loader: BaseLoader, embedding: Embeddings, search_type: Literal["similarity", "mmr"]) -> BaseRetriever:
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    return _indexing_questions(collection_name, text_splitter, loader, embedding, search_type)

# To run:
# - [x] unstructured+semantic+bge-small+*
# - [ ] unstructured+parent+{*}+{*}

# TODO:
#
# - [ ] Persist net evaluation results (or reload) to update final results.

SUPPORTED_LOADER = {
    # "pypdf": PyPDFLoader,
    # "pymupdf": PyMuPDFLoader,
    "unstructured": UnstructuredFileLoader,
}
SUPPORTED_INDEXING = {
    # "recursive": _indexing_recursive,
    # "semantic": _indexing_semantic,
    "parent": _indexing_parent,
    # "questions-semantic": _indexing_questions_semantic,
    # "questions-recursive": _indexing_questions_recursive,
}
SUPPORTED_EMBEDDING = [
    "openai-2",
    # "openai-3-s",
    # "openai-3-l",
    # "bge-small-bad",
    "bge-small",
    # "bge-large-bad",
    # "bge-large",
]
SUPPORTED_SEARCH = ["similarity", "mmr"]

def create_embedding(embedding: str):
    match embedding:
        case "openai-2":
            return OpenAIEmbeddings(model="text-embedding-ada-002")
        case "openai-3-s":
            return OpenAIEmbeddings(model="text-embedding-3-small")
        case "openai-3-l":
            return OpenAIEmbeddings(model="text-embedding-3-large")
        case "bge-small-bad":
            return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        case "bge-small":
            return HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        case "bge-large-bad":
            return HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
        case "bge-large":
            return HuggingFaceBgeEmbeddings(model_name="BAAI/bge-large-en-v1.5")
        case _:
            raise ValueError(f"Unsupported embedding {embedding}")

@dataclass(repr=False)
class Experiment():
    loader: str
    indexing: str
    embedding: str
    search: str

    def __repr__(self):
        return "+".join((self.loader, self.indexing, self.embedding, self.search))

PRIMARY_QA_LLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
QUESTION_GENERATION_LLM = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
EVALUATION_LLM = ChatOpenAI(model_name= "gpt-3.5-turbo-0125")

PROMPT_TEMPLATE = """Answer the question based only on the following context. If you cannot answer the question with the context, please respond with 'I don't know':

Context:
{context}

Question:
{question}
"""

PROMPT = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

def _chain(experiment: Experiment) -> Runnable:
    embedding = create_embedding(experiment.embedding)

    loader = DirectoryLoader(
        './datasets/history_of_alexnet/source_documents',
        glob="*.pdf",
        use_multithreading=True,
        loader_cls=SUPPORTED_LOADER[experiment.loader],
        show_progress=True,
    )
    alphanumeric = string.ascii_letters + string.digits
    collection_name = ''.join(random.choices(alphanumeric, k=16))
    print(f"Using collection name: {collection_name} for {experiment!r}")
    retriever = SUPPORTED_INDEXING[experiment.indexing](
        collection_name = collection_name,
        loader = loader,
        embedding = embedding,
        search_type = experiment.search
    )

    rag_qa_chain = (
        # INVOKE CHAIN WITH: {"question" : "<<SOME USER QUESTION>>"}
        # "question" : populated by getting the value of the "question" key
        # "context"  : populated by getting the value of the "question" key and chaining it into the base_retriever
        {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
        # "context"  : is assigned to a RunnablePassthrough object (will not be called or considered in the next step)
        #              by getting the value of the "context" key from the previous step
        | RunnablePassthrough.assign(context=itemgetter("context"))
        # "response" : the "context" and "question" values are used to format our prompt object and then piped
        #              into the LLM and stored in a key called "response"
        # "context"  : populated by getting the value of the "context" key from the previous step
        | {"response": PROMPT | PRIMARY_QA_LLM, "context": itemgetter("context")}
    )

    return rag_qa_chain

def _run_experiment(result_path: str, experiment: Experiment):
    # Create the chain for the experiment.
    chain = _chain(experiment)

    print(f"Running chain for experiment {experiment}")
    results = []

    for example in tqdm(load_examples()):
        response = chain.invoke({"question" : example.query})
        results.append({
            "question": example.query,
            "answer": response["response"].content,
            "contexts": [context.page_content for context in response["context"]],
            "ground_truth": example.ground_truth
        })
    dataset = Dataset.from_list(results)

    path = f"{result_path}/{experiment!r}"
    print(f"Saving dataset for {experiment} to {path}")
    dataset.save_to_disk(path)

class ExperimentParam(click.ParamType):
    name = "experiment"

    def convert(self, value: Any, param: click.Parameter | None, ctx: click.Context | None) -> Any:
        if isinstance(value, Experiment):
            return Experiment
        elif isinstance(value, str):
            parts = value.split("+", 5)
            if len(parts) != 4:
                self.fail("Expected experiment of form <loader>+<indexing>+<embedding>+<search>",
                          param, ctx)

            loader, indexing, embedding, search = parts
            if loader not in SUPPORTED_LOADER:
                self.fail(f"Unsupported loader '{loader}', expected one of {SUPPORTED_LOADER.keys()}")
            if indexing not in SUPPORTED_INDEXING:
                self.fail(f"Unsupported indexing '{indexing}', expected one of {SUPPORTED_INDEXING}")
            if embedding not in SUPPORTED_EMBEDDING:
                self.fail(f"Unsupported embedding '{embedding}', expected one of {SUPPORTED_EMBEDDING}")
            if search not in SUPPORTED_SEARCH:
                self.fail(f"Unsupported search '{search}', expected one of {SUPPORTED_SEARCH}")
            return Experiment(
                loader=loader,
                indexing=indexing,
                embedding=embedding,
                search=search
            )
        else:
            self.fail(f"Unable to convert from {value!r} to experiment")

@click.group()
def cli():
    pass


@cli.command()
@click.option("--result-path",
              default="results",
              type=click.Path(file_okay=False, writable=True))
@click.argument('experiments', nargs=-1, type=ExperimentParam())
def run(result_path: str, experiments: List[Experiment]):
    experiments = experiments or [
        Experiment(loader_cls, indexing, embedding, search)
        for loader_cls in SUPPORTED_LOADER
        for indexing in SUPPORTED_INDEXING
        for embedding in SUPPORTED_EMBEDDING
        for search in SUPPORTED_SEARCH
    ]

    os.makedirs(result_path, exist_ok=True)
    for e in experiments:
        _run_experiment(result_path, e)

def _evaluate_dataset(path: str) -> Dict[str, Any]:
    from ragas import evaluate
    from ragas.metrics import (
        context_recall,
        context_precision,
        context_relevancy,
    )

    metrics = [
        context_recall,
        context_precision,
        context_relevancy,
    ]

    response_dataset = Dataset.load_from_disk(path)
    results = evaluate(response_dataset,
                       metrics,
                       llm=EVALUATION_LLM,
                       raise_exceptions=False)
    print(f"Results for {path}:\n{results}")

    # Write the complete result set.
    results_df = results.to_pandas()
    results_df.to_parquet(f"{path}.parquet")
    print(f"Per-Example Results in {path}.parquet")

    metrics = dict(results.items())
    metrics['experiment'] = os.path.basename(path)

    # Write metrics dictionary as JSON
    with open(f"{path}.json", "w") as f:
        print(f"Results written to {path}.json")
        json.dump(metrics, f)

    return metrics

def _is_experiment_results(result_path, e) -> bool:
        # Use presence of the dataset_info.json to verify it's an experiment.
        return (os.path.isdir(f"{result_path}/{e}")
                and os.path.isfile(f"{result_path}/{e}/dataset_info.json"))

def _validate_experiments_to_evaluate(ctx, param, experiments):
    result_path = ctx.params["result_path"]
    for e in experiments:
        if not _is_experiment_results(result_path, e):
            raise click.BadParameter(f"{e} is not an experiment in {result_path}")

@cli.command()
@click.option("--result-path",
              default="results",
              type=click.Path(exists=True, file_okay=False, writable=True))
@click.argument('experiments', nargs=-1)
def evaluate(result_path: str, experiments: List[str]):
    # If experiments aren't listed, discover them.
    experiments = (experiments
                   or [e for e in os.listdir(result_path) if _is_experiment_results(result_path, e)])

    results = []
    for experiment in experiments:
        experiment_path = f"{result_path}/{experiment}"

        if os.path.isfile(f"{experiment_path}.json"):
            print(f"{experiment_path}.json already exists")
            with open(f"{experiment_path}.json", "r") as f:
                metrics = json.load(f)
                print(f"Loaded metrics: {metrics}")
                results.append(metrics)
        else:
            print(f"Evaluating {experiment_path}")
            metrics = _evaluate_dataset(experiment_path)
            results.append(metrics)

    import pandas as pd
    results_df = pd.DataFrame.from_records(results)
    print(results_df)

    results_df.to_csv(f"{result_path}/results.csv")
    print(f"Wrote results to {result_path}/results.csv")

    results_df.to_parquet(f"{result_path}/results.parquet")
    print(f"Wrote results to {result_path}/results.parquet")

if __name__ == '__main__':
    cli()