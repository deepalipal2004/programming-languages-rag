from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def rerank_results(question, results, top_k=3):
    """
    Re-ranks retrieved chunks based on their similarity
    to the user's question.
    """

    if not results:
        return []

    model = SentenceTransformer(EMBEDDING_MODEL)

    # Create embedding for the question
    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    # Create embeddings for retrieved chunks
    texts = [result["text"] for result in results]

    chunk_embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    # Calculate similarity using dot product
    scores = chunk_embeddings @ question_embedding

    # Add the new reranking score
    reranked_results = []

    for result, score in zip(results, scores):
        updated_result = result.copy()
        updated_result["rerank_score"] = float(score)
        reranked_results.append(updated_result)

    # Sort from highest score to lowest score
    reranked_results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    # Return only the best results
    return reranked_results[:top_k]


if __name__ == "__main__":
    from retriever import retrieve_chunks

    question = input("Enter your question: ")

    retrieved_results = retrieve_chunks(question, top_k=5)

    reranked_results = rerank_results(
        question,
        retrieved_results,
        top_k=3
    )

    print("\nReranked results:\n")

    for i, result in enumerate(reranked_results, start=1):
        print(f"--- Result {i} ---")
        print(f"Page: {result['page']}")
        print(f"Rerank score: {result['rerank_score']:.4f}")
        print(result["text"][:500])
        print()