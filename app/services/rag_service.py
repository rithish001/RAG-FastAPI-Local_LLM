from app.db.chroma_client import collection
import ollama


def ask_question(question: str, user: str = None):
    # Step 1: Build query
    query_params = {
        "query_texts": [question],
        "n_results": 3,
    }

    # Optional filtering
    if user:
        query_params["where"] = {"user_name": user}

    # Step 2: Retrieve documents
    results = collection.query(**query_params)

    # Handle empty results
    if not results.get("documents") or not results["documents"][0]:
        return {
            "answer": "No relevant information found.",
            "context": [],
        }

    context = "\n\n".join(results["documents"][0])

    # Step 3: Build prompt
    prompt = f"""Use the following context to answer the question.
If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {question}
"""

    # Step 4: Call LLM
    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[{"role": "user", "content": prompt}],
    )

    return {
        "answer": response["message"]["content"],
        "context": results["documents"][0],
    }