def chunk_documents(documents, chunk_size=800, overlap=100):
    """
    Splits PDF text into smaller chunks.

    Each chunk keeps the page number from the original PDF.
    """

    chunks = []

    for document in documents:
        text = document["text"]
        page = document["page"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page
                })

            start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    from pdf_loader import load_pdf

    documents = load_pdf()
    chunks = chunk_documents(documents)

    print("Number of chunks:", len(chunks))

    print("\nFirst chunk:\n")
    print(chunks[0]["text"])

    print("\nPage number:", chunks[0]["page"])