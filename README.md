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
- ✂️ Text chunking with LangChain's `RecursiveCharacterTextSplitter`
- 🔎 Semantic search using vector embeddings (Ollama `nomic-embed-text`)
- 🧠 Context-aware answers using a local LLM (Ollama)
- 👤 User- and source-specific document filtering
- 📊 Built-in RAG evaluation pipeline (DeepEval: answer relevancy, faithfulness, contextual precision/recall)
- 🪵 Structured logging with request timing
- ⚡ FastAPI-based backend, async end-to-end

---

## 🧠 How It Works

1. Add content via `/upload` (TXT/PDF file) or `/documents` (raw text)
2. Text is split into overlapping chunks (`app/utils/chunking.py`)
3. Chunks are embedded and stored in ChromaDB, tagged with `source`, `user_name`, and `chunk_index` metadata
4. Query via `/ask` — the service embeds the question, retrieves the top-`k` matching chunks (optionally filtered by `user`, and by `source` if calling the service directly), and passes them as context to the local LLM
5. The LLM is instructed to answer **only** from the retrieved context, and to say so explicitly if the context doesn't contain the answer

---

## 🏗️ Tech Stack

| Layer             | Technology                              |
|-------------------|-------------------------------------------|
| Framework         | FastAPI (async)                            |
| Vector DB         | ChromaDB (Persistent)                      |
| Embeddings        | nomic-embed-text (Ollama)                  |
| LLM               | Qwen2.5 0.5B / Any Ollama model            |
| Text Splitting    | LangChain (`RecursiveCharacterTextSplitter`) |
| Config Management | Pydantic Settings (`.env`-based)           |
| Evaluation        | DeepEval (LLM-as-judge via Ollama)         |
| Validation        | Pydantic v2                                |

---

## 📁 Project Structure

```
RAG-FastAPI-Local_LLM/
├── app/
│   ├── api/routes.py            # FastAPI route definitions
│   ├── services/rag_service.py  # Core RAG logic: retrieval + LLM answer generation
│   ├── utils/chunking.py        # Text chunking (LangChain RecursiveCharacterTextSplitter)
│   ├── utils/logger.py          # Logging configuration
│   ├── db/chroma_client.py      # ChromaDB client + Ollama embedding function
│   ├── schemas/schemas.py       # Pydantic request/response models
│   └── main.py                  # FastAPI app entrypoint
├── config/
│   └── settings.py              # Pydantic Settings (reads from .env)
├── data/                        # Source documents (e.g. coverletter.txt) + persistent Chroma store
├── evaluation/
│   ├── dataset/                 # CSV test cases (question, expected_answer, ...)
│   ├── results/                 # Evaluation output CSVs
│   └── evaluate_dataset.py      # Runs DeepEval metrics against the RAG pipeline
├── scripts/
│   └── build_knowledge_base.py  # One-off script to chunk + embed a doc into ChromaDB
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone and install

```bash
git clone https://github.com/rithish001/RAG-FastAPI-Local_LLM.git
cd RAG-FastAPI-Local_LLM

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:0.5b
CHROMA_DB_PATH=./data/chroma
COLLECTION_NAME=documents
TOP_K_RESULTS=3
LOG_LEVEL=INFO
```

### 3. Pull the local models via Ollama

```bash
ollama pull nomic-embed-text
ollama pull qwen2.5:0.5b
ollama run qwen2.5:0.5b
```

### 4. Build the knowledge base (optional, for a quick test)

Place a document at `data/coverletter.txt` (or point the script at your own file), then run:

```bash
python -m scripts.build_knowledge_base
```

This chunks the document and stores the embeddings in your persistent ChromaDB collection.

### 5. Start the API server

```bash
uvicorn app.main:app --reload
```

The API will be live at: `http://localhost:8000`

---

## 📬 API

| Method | Endpoint     | Params                                          | Description                                                                          |
|--------|--------------|--------------------------------------------------|-----------------------------------------------------------------------------------------|
| POST   | `/documents` | Body: `user_name`, `content`                      | Submit raw text for a user; chunks it and stores it in ChromaDB (`source: "profile"`)   |
| POST   | `/upload`    | Query: `user_name` · Form: `file` (TXT or PDF)    | Upload a TXT or PDF file, extract its text, chunk it, and store it in ChromaDB (`source: <filename>`) |
| GET    | `/ask`       | Query: `question`, `user` (optional)              | Ask a question, optionally filtered by `user`, and get a context-aware answer           |

`/ask` returns `{ "answer": ..., "context": [...] }`.

> Note: `ask_question()` in `rag_service.py` also supports filtering by `source`, but the `/ask` route doesn't currently expose it as a query parameter. There's also no `GET /documents` listing endpoint yet — only `POST /documents` (add raw text) exists.

---

## 📊 Evaluation

`evaluation/evaluate_dataset.py` runs the RAG pipeline against a labeled test set (e.g. `evaluation/dataset/coverletter_testcases.csv`, with `id`, `question`, `expected_answer`, `category`, `difficulty`, `source_document` columns) and scores each response with [DeepEval](https://github.com/confident-ai/deepeval), using a local Ollama model as the judge:

- **Answer Relevancy** – does the answer address the question?
- **Faithfulness** – is the answer grounded in the retrieved context?
- **Contextual Precision / Recall** – how well did retrieval surface the right chunks?

Run it with:

```bash
python -m evaluation.evaluate_dataset
```

Results (per-question scores and pass/fail flags) are written to `evaluation/results/evaluation_results.csv`.

> **Current benchmark status:** on the sample cover-letter dataset (20 questions), most cases score `0.5` on both answer relevancy and faithfulness against a `0.6` threshold — i.e. they currently fail with the tiny `qwen2.5:0.5b` model acting as both generator and judge. This is expected for a 0.5B-parameter model; swapping in a larger Ollama model (e.g. `qwen2.5:7b` or `llama3.1`) for generation and/or judging should improve scores meaningfully.

---

## 💡 Future Improvements

- UI
- Authentication
- Deployment

---

## 👨‍💻 Author

Rithish Reddy
