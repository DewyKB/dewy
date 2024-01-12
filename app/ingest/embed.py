from llama_index.embeddings import resolve_embed_model

EMBED_MODEL = resolve_embed_model("local")  # use the default local embedding

# Determine the dimension of the embeddings. There isn't an easy API for this,
# so we just perform an embedding and see the dimensions we get back.
EMBEDDING_DIMENSIONS = len(EMBED_MODEL.get_text_embedding("test embedding"))
