from src.rag_pipeline import answer_question


print("=" * 60)
print("Programming Languages RAG Assistant")
print("=" * 60)

print("\nAsk questions about the programming languages in your PDF.")
print("Type 'exit' to stop.\n")


while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("\nGoodbye!")
        break

    if not question.strip():
        print("Please enter a question.\n")
        continue

    print("\nSearching documents...\n")

    answer, results = answer_question(question)

    print("Assistant:")
    print(answer)

    print("\nSources:")

    for result in results:
        print(
            f"- Page {result['page']} "
            f"(rerank score: {result['rerank_score']:.4f})"
        )

    print("\n" + "-" * 60 + "\n")