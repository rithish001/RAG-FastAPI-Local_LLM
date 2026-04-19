# 🧠 RAG-based Local LLM Application (FastAPI + ChromaDB + Ollama)

A Retrieval-Augmented Generation (RAG) system that allows users to
upload documents and ask questions based on their content using a local
LLM.

------------------------------------------------------------------------

![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00.svg?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-000000.svg?style=for-the-badge)

## 🚀 Features

-   📂 Upload TXT and PDF files
-   ✂️ Text chunking
-   🔎 Semantic search using vector embeddings
-   🧠 Context-aware answers using local LLM (Ollama)
-   👤 User-specific document filtering
-   ⚡ FastAPI-based backend

------------------------------------------------------------------------

## 🧠 How It Works

1.  Upload Document via `/upload`
2.  Extract text and split into chunks
3.  Generate embeddings
4.  Store in ChromaDB
5.  Query via `/ask` to retrieve relevant chunks and generate answer

------------------------------------------------------------------------

## 🏗️ Tech Stack

| Layer           | Technology                  |
|----------------|-----------------------------|
| Framework       | FastAPI                     |
| Vector DB       | ChromaDB (Persistent)       |
| Embeddings      | nomic-embed-text (Ollama)   |
| LLM             | Qwen2.5 0.5B / Any Ollama model |
| Document Parser | PyPDF                       |
| Validation      | Pydantic v2                 |

------------------------------------------------------------------------

## 📁 Project Structure

    app/
    ├── api/routes.py
    ├── services/rag_service.py
    ├── utils/chunking.py
    ├── db/chroma_client.py
    ├── schemas/schemas.py
    main.py

------------------------------------------------------------------------

## ⚙️ Setup

    git clone https://github.com/rithish001/RAG-FastAPI-Local_LLM.git
    cd RAG-FastAPI-Local_LLM
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ollama run qwen2.5:0.5b
    uv run uvicorn app.main:app --reload
    API will be live at: http://localhost:8000

------------------------------------------------------------------------

## 📬 API

POST /upload\
POST /documents\
GET /ask

------------------------------------------------------------------------

## 💡 Future Improvements

-   UI
-   Authentication
-   Deployment

------------------------------------------------------------------------

## 👨‍💻 Author

Rithish Reddy
