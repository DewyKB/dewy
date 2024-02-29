# Experiments

## RAG Configuration

This experiment plays with some of the standard configuration options available in LangChain.
It runs a variety of extraction, splitting, and retrieval configurations on the AlexNet PDF and Q/A set.

To execute:

```sh
python rag_configuration.py run       # --help to see options for filtering configurations

python rag_configuration.py clear     # to clear Tru DB
python rag_configuration.py dashboard # to display dashboard
python rag_configuration.py sreve     # to serve the browser dashboard
```