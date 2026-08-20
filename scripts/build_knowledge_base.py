from app.db.chroma_client import collection
from app.utils.chunking import chunk_text
import uuid

# Load file
with open("data/coverletter.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Chunk text
chunks = chunk_text(text)

print(f"Loaded {len(chunks)} chunks")

# Generate unique IDs
ids = [str(uuid.uuid4()) for _ in chunks]

# Store in DB
collection.add(
    ids=ids,
    documents=chunks,
    metadatas=[
        {
            "source": "coverletter.txt",
            "user_name": "Rithish",
            "chunk_index": i,
        }
        for i in range(len(chunks))
    ],
)

print("Knowledge base built successfully!")