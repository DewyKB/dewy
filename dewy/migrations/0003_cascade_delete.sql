-- Update foreign key constraints to cascade deletion

ALTER TABLE document
DROP CONSTRAINT document_collection_id_fkey,
ADD CONSTRAINT document_collection_id_fkey
   FOREIGN KEY (collection_id)
   REFERENCES collection (id)
   ON DELETE CASCADE;

ALTER TABLE chunk
DROP CONSTRAINT chunk_document_id_fkey,
ADD CONSTRAINT chunk_document_id_fkey
   FOREIGN KEY (document_id)
   REFERENCES document (id)
   ON DELETE CASCADE;

ALTER TABLE embedding
DROP CONSTRAINT embedding_chunk_id_fkey,
ADD CONSTRAINT embedding_chunk_id_fkey
   FOREIGN KEY (chunk_id)
   REFERENCES chunk (id)
   ON DELETE CASCADE;