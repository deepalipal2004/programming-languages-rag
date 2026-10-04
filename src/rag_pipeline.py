from src.retriever import retrieve_chunks
from src.reranker import rerank_results
from src.llm import generate_answer


def build_context(results):
    """
    Combines the retrieved chunks into one context.
    """

    context_parts = []

    for result in results:
        context_parts.append(
            f"Page {result['page']}:\n{result['text']}"
        )

    return "\n\n".join(context_parts)


def answer_question(question):
    """
    Retrieves relevant chunks, reranks them,
    and asks the LLM to answer using the best results.
    """

    # Step 1: Retrieve initial results
    retrieved_results = retrieve_chunks(
        question,
        top_k=5
    )

    # Step 2: Rerank the retrieved results
    reranked_results = rerank_results(
        question,
        retrieved_results,
        top_k=3
    )

    # Step 3: Build context from the best results
    context = build_context(reranked_results)

    # Step 4: Create RAG prompt
    prompt = f"""
You are a helpful programming assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not make up information.

Context:
{context}

User Question:
{question}

Answer:
"""

    # Step 5: Send context + question to Nugen
    answer = generate_answer(prompt)

    return answer, reranked_results


if __name__ == "__main__":

    question = input("Enter your question: ")

    answer, results = answer_question(question)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources:\n")

    for result in results:
        print(
            f"- Page {result['page']} "
            f"(rerank score: {result['rerank_score']:.4f})"
        )