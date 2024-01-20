-- Apply the base schema.

CREATE TABLE collection (
    id SERIAL NOT NULL,
    name VARCHAR NOT NULL,

    PRIMARY KEY (id)
);

CREATE TYPE ingest_state AS ENUM ('pending', 'ingested', 'failed');
CREATE TABLE document(
    id SERIAL NOT NULL,
    collection_id INTEGER,
    url VARCHAR NOT NULL,

    -- The state of the most recent ingestion of this document.
    -- TODO: Should we have a separate `ingestion` table and associate
    -- many ingestions with each document ID?
    ingest_state ingest_state,
    -- The error (if any) resulting from the most recent ingestion.
    ingest_error VARCHAR,

    PRIMARY KEY (id),
    UNIQUE (collection_id, url),
    FOREIGN KEY(collection_id) REFERENCES collection (id)
);

CREATE TYPE chunk_kind AS ENUM (
    -- This is a chunk representing text.
    'text'
);
CREATE TABLE chunk(
    id SERIAL NOT NULL,

    -- The document containing this chunk.
    --
    -- TODO: We may want to allow chunks to be associated with
    -- multiple documents.
    document_id INTEGER,

    -- The kind of chunk.
    kind chunk_kind NULL,

    -- The text associated with the chunk, if any.
    --
    -- The existance of text does not imply the chunk is textual. For instance,
    -- image chunks may set the text to a description of the image.
    text VARCHAR,

    PRIMARY KEY (id),
    FOREIGN KEY(document_id) REFERENCES document (id)
);

-- CREATE TABLE ingestion(
--     id SERIAL NOT NULL,
--     -- The document ID this ingestion is associated with.
--     document_id INTEGER,
--     -- The state of this ingestion.
--     --
--     -- NULL indicates unknown.
--     state ingest_state,
--     -- Concatetaned errors reported by this ingestion.
--     error VARCHAR,

--     FOREIGN KEY(document_id) REFERENCES document (id)
-- )

CREATE TYPE embedding_kind AS ENUM (
    -- This is an embedding of the original text of the chunk.
    --
    -- `key_text` will be NULL -- see the `text` of the original chunk.
    'text',
    -- This is an embedding of the computed summary of the chunk.
    --
    -- `key_text` will contain the computed summary.
    'computed_summary',
    -- This is an embedding of the computed title.
    --
    -- `key_text` will contain the computed summary.
    'computed_title'
);
CREATE TABLE embedding(
    id SERIAL NOT NULL,

    chunk_id INTEGER,

    key_text VARCHAR,

    PRIMARY KEY (id),
    FOREIGN KEY(chunk_id) REFERENCES chunk (id)
);