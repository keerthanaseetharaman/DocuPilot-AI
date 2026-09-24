from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from app.pdf_service import extract_text_from_pdf
from app.text_chunker import create_chunks
from app.embedding_service import create_embeddings
from app.chroma_service import store_chunks
from app.search_service import search_documents
from app.gemini_service import generate_answer, generate_summary


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="DocuPilot AI",
    description="AI-Powered Document Intelligence & Knowledge Assistant",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Upload Folder
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# --------------------------------------------------
# Home Route
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "DocuPilot AI Backend is running!"
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # Check file type
    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files are allowed."
        }

    # Create file path
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    # Save uploaded PDF
    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # --------------------------------------------------
    # Extract PDF Text
    # --------------------------------------------------

    pages = extract_text_from_pdf(
        file_path
    )

    # --------------------------------------------------
    # Create Text Chunks
    # --------------------------------------------------

    chunks = create_chunks(
        pages
    )

    # --------------------------------------------------
    # Create Embeddings
    # --------------------------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = create_embeddings(
        texts
    )

    # --------------------------------------------------
    # Store in ChromaDB
    # --------------------------------------------------

    stored_chunks = store_chunks(
        chunks,
        embeddings,
        file.filename
    )

    # --------------------------------------------------
    # Document Statistics
    # --------------------------------------------------

    total_pages = len(
        pages
    )

    total_characters = sum(
        len(page["text"])
        for page in pages
    )

    total_chunks = len(
        chunks
    )

    # --------------------------------------------------
    # Response
    # --------------------------------------------------

    return {
        "success": True,
        "message": "PDF uploaded and stored successfully!",
        "filename": file.filename,
        "total_pages": total_pages,
        "total_characters": total_characters,
        "total_chunks": total_chunks,
        "stored_chunks": stored_chunks
    }


# --------------------------------------------------
# Search Document
# --------------------------------------------------

@app.get("/search")
def search_pdf(
    query: str,
    top_k: int = 3
):

    results = search_documents(
        query,
        top_k
    )

    return {
        "success": True,
        "query": query,
        "results": results
    }


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

@app.get("/ask")
def ask_question(
    query: str,
    top_k: int = 3
):

    # Search relevant document chunks
    search_results = search_documents(
        query,
        top_k
    )

    # Combine retrieved chunks
    context = "\n\n".join(
        result["text"]
        for result in search_results
    )

    # Generate AI answer
    answer = generate_answer(
        query,
        context
    )

    # Prepare source information
    sources = []

    for result in search_results:

        sources.append({
            "document": result["document"],
            "page": result["page"]
        })

    return {
        "success": True,
        "question": query,
        "answer": answer,
        "sources": sources
    }


# --------------------------------------------------
# Summarize Document
# --------------------------------------------------

@app.get("/summarize")
def summarize_document(
    document_name: str,
    top_k: int = 10
):

    # Search document content
    search_results = search_documents(
        document_name,
        top_k
    )

    # Combine document chunks
    context = "\n\n".join(
        result["text"]
        for result in search_results
    )

    # Generate AI summary
    summary = generate_summary(
        context
    )

    # Prepare source information
    sources = []

    for result in search_results:

        sources.append({
            "document": result["document"],
            "page": result["page"]
        })

    return {
        "success": True,
        "document": document_name,
        "summary": summary,
        "sources": sources
    }