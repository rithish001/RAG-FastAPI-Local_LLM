import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)
from config.settings import settings

client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH,)

ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url=settings.OLLAMA_URL,
)

collection = client.get_or_create_collection(
    name=settings.COLLECTION_NAME,
    embedding_function=ef,
)