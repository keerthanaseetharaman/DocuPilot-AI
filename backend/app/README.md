# DocuPilot AI

## AI-Powered Document Intelligence & Knowledge Assistant

DocuPilot AI is an AI-powered document intelligence application that allows users to upload PDF documents, search document content, ask questions, and generate document summaries.

The system combines PDF text extraction, semantic search, vector embeddings, ChromaDB, FastAPI, React, and Google Gemini to create an intelligent document assistant.

---

## Features

- 📄 PDF document upload
- 🔍 Automatic PDF text extraction
- ✂️ Intelligent text chunking
- 🧠 Sentence Transformer embeddings
- 🗄️ ChromaDB vector database
- 🔎 Semantic document search
- 💬 AI-powered document question answering
- 📝 AI-generated document summaries
- 📚 Source document and page references
- ⚡ FastAPI backend
- ⚛️ React frontend
- 🔐 Environment-based API key configuration
- 📱 Responsive user interface

---

## System Architecture

```text
User
  │
  ▼
React Frontend
  │
  ▼
FastAPI Backend
  │
  ├── PDF Upload
  │
  ├── PDF Text Extraction
  │
  ├── Text Chunking
  │
  ├── Sentence Transformer
  │
  ▼
ChromaDB
  │
  ▼
Semantic Search
  │
  ▼
Relevant Document Context
  │
  ▼
Google Gemini
  │
  ▼
AI Answer / Summary