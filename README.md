# Programming Languages RAG Assistant

A Retrieval-Augmented Generation (RAG) project that answers questions about programming languages using information stored in a PDF document.

## Project Overview

This project uses RAG to retrieve relevant information from a programming languages study guide and generate answers using the Nugen LLM.

Instead of asking the language model to answer from its general knowledge, the system first searches the provided document and then generates an answer using the retrieved information.

## RAG Pipeline

PDF Document
    ↓
PDF Loader
    ↓
Text Chunking
    ↓
Sentence Embeddings
    ↓
Qdrant Vector Database
    ↓
Retriever
    ↓
Reranker
    ↓
Relevant Context
    ↓
Nugen LLM
    ↓
Final Answer

## Technologies Used

- Python
- PyPDF
- Sentence Transformers
- Qdrant
- Nugen LLM API
- Python-dotenv
- Requests

## Project Structure

```text
rag_project/
│
├── documents/
│   └── programming_languages.pdf
│
├── qdrant_storage/
│
├── src/
│   ├── __init__.py
│   ├── pdf_loader.py
│   ├── chunking.py
│   ├── ingest.py
│   ├── qdrant_db.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── llm.py
│   └── rag_pipeline.py
│
├── .env
├── .gitignore
├── app.py
├── requirements.txt
├── sample_questions.txt
└── README.md