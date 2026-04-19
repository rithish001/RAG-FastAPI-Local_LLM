from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag_service import ask_question
from app.schemas.schemas import DocumentSubmission
from app.utils.chunking import chunk_text
from app.db.chroma_client import collection

from pypdf import PdfReader
import uuid

router = APIRouter()


@router.post("/documents")
def add_document(submission: DocumentSubmission):

    if not submission.user_name.strip():
        raise HTTPException(status_code=400, detail="User name cannot be empty")

    if not submission.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")

    # Chunk text
    chunks = chunk_text(submission.content)

    # Store in DB
    collection.add(
        ids=[f"{submission.user_name}-chunk{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[
            {"source": "profile", "user_name": submission.user_name, "chunk_index": i}
            for i in range(len(chunks))
        ],
    )

    return {
        "message": f"Added {len(chunks)} chunks for user '{submission.user_name}'.",
        "user_name": submission.user_name,
        "chunks_added": len(chunks),
    }


def extract_text_from_file(file: UploadFile):
    if file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")

    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    else:
        raise HTTPException(
            status_code=400,
            detail="Only TXT and PDF files are supported"
        )


@router.post("/upload")
def upload_file(user_name: str, file: UploadFile = File(...)):

    if not user_name.strip():
        raise HTTPException(status_code=400, detail="User name is required")

    # Extract text
    text = extract_text_from_file(file)

    if not text.strip():
        raise HTTPException(status_code=400, detail="File is empty or unreadable")

    # Chunk text
    chunks = chunk_text(text)

    # Generate unique IDs
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Store in DB
    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=[
            {
                "source": file.filename,
                "user_name": user_name,
                "chunk_index": i,
            }
            for i in range(len(chunks))
        ],
    )

    return {
        "message": f"{file.filename} uploaded successfully",
        "chunks_added": len(chunks),
        "user": user_name,
    }


@router.get("/ask")
def ask(question: str, user: str = None):
    return ask_question(question, user)