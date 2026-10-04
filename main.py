from fastapi import FastAPI
from pydantic import BaseModel

from src.rag_pipeline import answer_question


app = FastAPI(
    title="Programming Languages RAG API",
    description="RAG API for answering questions from programming language documents.",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Programming Languages RAG API is running."
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer, results = answer_question(request.question)

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            {
                "page": result["page"],
                "score": result["rerank_score"]
            }
            for result in results
        ]
    }