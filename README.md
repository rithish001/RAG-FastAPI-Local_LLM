# 🧠 RAG-based Local LLM Application (FastAPI + ChromaDB + Ollama)

A Retrieval-Augmented Generation (RAG) system that allows users to
upload documents and ask questions based on their content using a local
LLM.

------------------------------------------------------------------------

## 🚀 Features

-   📂 Upload TXT and PDF files
-   ✂️ Automatic text chunking
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

-   FastAPI\
-   ChromaDB\
-   Ollama (qwen2.5:0.5b)\
-   mxbai-embed-large\
-   PyPDF

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

    git clone <your-repo>
    cd <your-repo>
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ollama run qwen2.5:0.5b
    uv run uvicorn app.main:app --reload

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
