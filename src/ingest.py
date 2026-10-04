from sentence_transformers import SentenceTransformer
from qdrant_client.models import Distance, VectorParams, PointStruct

from pdf_loader import load_pdf
from chunking import chunk_documents
from qdrant_db import get_qdrant_client, COLLECTION_NAME


# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def ingest_documents():
    print("Loading PDF...")

    # Step 1: Load PDF
    documents = load_pdf()

    print(f"Loaded {len(documents)} pages.")

    # Step 2: Create chunks
    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # Step 3: Load embedding model
    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print("Embedding model loaded.")

    # Step 4: Convert chunks into embeddings
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    print("Embeddings created.")

    # Step 5: Connect to Qdrant
    client = get_qdrant_client()

    # Step 6: Create collection
    vector_size = len(embeddings[0])

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )

    print("Qdrant collection created.")

    # Step 7: Prepare points
    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

        points.append(
            PointStruct(
                id=index,
                vector=embedding.tolist(),
                payload={
                    "text": chunk["text"],
                    "page": chunk["page"]
                }
            )
        )

    # Step 8: Store vectors in Qdrant
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Successfully stored {len(points)} vectors in Qdrant.")

    client.close()

    print("Qdrant client closed.")
    print("Ingestion completed successfully!")


if __name__ == "__main__":
    ingest_documents()