from pathlib import Path
from pypdf import PdfReader


# Path of our PDF file
PDF_PATH = Path(__file__).resolve().parent.parent / "documents" / "programming_languages.pdf"


def load_pdf(pdf_path=PDF_PATH):
    """
    Reads the PDF and returns the text page by page.
    """

    reader = PdfReader(str(pdf_path))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            documents.append({
                "page": page_number,
                "text": text
            })

    return documents


if __name__ == "__main__":
    documents = load_pdf()

    print("PDF loaded successfully!")
    print("Number of pages:", len(documents))

    if documents:
        print("\nFirst page text:\n")
        print(documents[0]["text"][:1000])