# 🧠 RAG-based Local LLM Application (FastAPI + ChromaDB + Ollama)

A Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions based on their content using a local LLM.

---

![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00.svg?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-000000.svg?style=for-the-badge)
![DeepEval](https://img.shields.io/badge/DeepEval-Evaluation-blue.svg?style=for-the-badge)

## 🚀 Features

- 📂 Upload TXT and PDF files
- ✂️ Text chunking
- 🔎 Semantic search using vector embeddings
- 🧠 Context-aware answers using a local LLM (Ollama)
- 👤 User-specific document filtering
- ⚡ FastAPI-based backend

---

## 🧠 How It Works

1. Upload a document via `/upload`
2. Extract text and split it into chunks
3. Generate embeddings
4. Store embeddings in ChromaDB
5. Query via `/ask` to retrieve relevant chunks and generate an answer

---

## 🏗️ Tech Stack

| Layer            | Technology                       |
|------------------|-----------------------------------|
| Framework        | FastAPI                           |
| Vector DB        | ChromaDB (Persistent)             |
| Embeddings       | nomic-embed-text (Ollama)         |
| LLM              | Qwen2.5 0.5B / Any Ollama model   |
| Document Parser  | PyPDF                             |
| Validation       | Pydantic v2                       |

---

## 📁 Project Structure

```
RAG-FastAPI-Local_LLM/
├── app/
│   ├── api/routes.py
│   ├── services/rag_service.py
│   ├── utils/chunking.py
│   ├── db/chroma_client.py
│   ├── schemas/schemas.py
│   └── main.py
├── config/          # App/environment configuration
├── data/            # Uploaded documents / persistent ChromaDB storage
├── evaluation/       # Scripts and notebooks for evaluating retrieval/answer quality
├── scripts/         # Utility and setup scripts
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
git clone https://github.com/rithish001/RAG-FastAPI-Local_LLM.git
cd RAG-FastAPI-Local_LLM

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Pull and run the local LLM via Ollama
ollama run qwen2.5:0.5b

# Start the API server
uvicorn app.main:app --reload
```

The API will be live at: `http://localhost:8000`

---

## 📬 API

| Method | Endpoint     | Description                                  |
|--------|--------------|-----------------------------------------------|
| POST   | `/upload`    | Upload a TXT or PDF document                  |
| GET    | `/documents` | List uploaded documents                       |
| POST   | `/ask`       | Ask a question and get a context-aware answer |

---

## 💡 Future Improvements

- UI
- Authentication
- Deployment

---
