from app.db.chroma_client import collection
from fastapi.concurrency import run_in_threadpool
import ollama
import time
from app.utils.logger import logger
from config.settings import settings


async def ask_question(question: str, user: str = None, source: str = None):
    start_time = time.perf_counter()
    logger.info(f"Received question: {question}")
    # Step 1: Build query
    query_params = {
        "query_texts": [question],
        "n_results": settings.TOP_K_RESULTS,
    }

    filters = []

    # Optional filtering
    if user:
        query_params["where"] = {"user_name": user}

    if source:
        filters.append({"source": source})

    if len(filters) == 1:
        query_params["where"] = filters[0]

    elif len(filters) > 1:
        query_params["where"] = {
            "$and": filters
        }

    logger.info("Querying ChromaDB...")

    # Step 2: Retrieve documents
    try:
        results = await run_in_threadpool(
            collection.query,
            **query_params,
        )
    except Exception:
        logger.exception("Failed while querying ChromaDB.")
        raise

    # logger.info(
    #     f"Retrieved {len(results['documents'][0])} document(s)"
    # )

    # Handle empty results
    # if not results.get("documents") or not results["documents"][0]:
    #     return {
    #         "answer": "No relevant information found.",
    #         "context": [],
    #     }
    #
    # context = "\n\n".join(results["documents"][0])

    if not results.get("documents") or not results["documents"][0]:
        logger.warning("No relevant documents found.")

        elapsed = time.perf_counter() - start_time
        logger.info(f"Request completed in {elapsed:.2f} seconds")

        return {
            "answer": "No relevant information found.",
            "context": [],
        }

    documents = results["documents"][0]

    logger.info(f"Retrieved {len(documents)} document(s)")

    context = "\n\n".join(documents)



    prompt = f"""You are a helpful AI assistant answering questions from a knowledge base.

            Instructions:
            - Answer ONLY using the provided context.
            - Do NOT use outside knowledge.
            - If the answer is not present in the context, reply exactly:
              "The provided context does not contain enough information to answer this question."
            - Keep the answer concise (1-3 sentences).
            - Do not make assumptions or hallucinate information.
            
            Context:
            {context}
            
            Question: {question}
            """

    # Step 4: Call LLM
    logger.info("Sending request to Ollama...")

    try:
        response = await run_in_threadpool(
            ollama.chat,
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
    except Exception:
        logger.exception("Failed while generating LLM response.")
        raise

    logger.info("Response generated successfully.")

    elapsed = time.perf_counter() - start_time

    logger.info(f"Request completed in {elapsed:.2f} seconds")

    return {
        "answer": response["message"]["content"],
        "context": results["documents"][0],
    }