from sentence_transformers import SentenceTransformer

from src.qdrant_db import get_qdrant_client, COLLECTION_NAME


# Same embedding model used during ingestion
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def retrieve_chunks(question, top_k=5):
    """
    Finds the most relevant chunks from Qdrant
    for the given question.
    """

    # Load embedding model
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Convert question into an embedding
    question_embedding = model.encode(question).tolist()

    # Connect to Qdrant
    client = get_qdrant_client()

    # Search for similar vectors
    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=top_k,
    ).points

    # Extract useful information
    results = []

    for result in search_results:
        results.append({
            "text": result.payload["text"],
            "page": result.payload["page"],
            "score": result.score
        })

    client.close()

    return results


if __name__ == "__main__":

    question = input("Enter your question: ")

    results = retrieve_chunks(question)

    print("\nRelevant chunks:\n")

    for i, result in enumerate(results, start=1):
        print(f"--- Result {i} ---")
        print(f"Page: {result['page']}")
        print(f"Score: {result['score']:.4f}")
        print(result["text"][:500])
        print()