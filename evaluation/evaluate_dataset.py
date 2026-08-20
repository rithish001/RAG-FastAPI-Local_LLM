from app.services.rag_service import ask_question

from deepeval.test_case import LLMTestCase
from deepeval.models import OllamaModel
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualPrecisionMetric, ContextualRecallMetric

import csv
DATASET_PATH = "evaluation/dataset/coverletter_testcases.csv"
OUTPUT_PATH = "evaluation/results/evaluation_results.csv"

judge_model = OllamaModel(
        model="qwen2.5:0.5b",
        base_url="http://localhost:11434",
        temperature=0
    )


answer_metric = AnswerRelevancyMetric(
            threshold=0.6,
            model=judge_model
        )

faithfulness_metric = FaithfulnessMetric(
        threshold=0.6,
        model=judge_model
    )

context_precision = ContextualPrecisionMetric(
    threshold=0.7,
    model=judge_model
)

context_recall = ContextualRecallMetric(
    threshold=0.7,
    model=judge_model
)

results = []

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        # Ask RAG
        result = ask_question(
            question=row["question"],
            user="Rithish",  # or row["user"] if your CSV has this column
            source="coverletter.txt",
        )

        # Create DeepEval test case
        test_case = LLMTestCase(
            input=row["question"],
            actual_output=result["answer"],
            expected_output=row["expected_answer"],
            retrieval_context=result["context"],
            context=result["context"],
        )

        # Evaluate
        answer_metric.measure(test_case)
        faithfulness_metric.measure(test_case)

        context_precision.measure(test_case)
        context_recall.measure(test_case)

        results.append(
            {
                "id": row["id"],
                "question": row["question"],
                "expected": row["expected_answer"],
                "generated": result["answer"],
                "answer_relevancy": round(answer_metric.score, 2),
                "faithfulness": round(faithfulness_metric.score, 2),
                "answer_pass": answer_metric.success,
                "faithfulness_pass": faithfulness_metric.success,
            }
        )

        # Print Results
        print("=" * 70)
        print("ID :", row["id"])
        print()

        print("Question:")
        print(row["question"])
        print()

        print("Expected:")
        print(row["expected_answer"])
        print()

        print("Generated:")
        print(result["answer"])
        print()

        print("Answer Relevancy :", answer_metric.score)
        print(answer_metric.reason)
        print()

        print("Faithfulness :", faithfulness_metric.score)
        print(faithfulness_metric.reason)
        print()

        print("Context Precision :", context_precision.score)
        print(context_precision.reason)

        print()

        print("Context Recall :", context_recall.score)
        print(context_recall.reason)

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "id",
            "question",
            "expected",
            "generated",
            "answer_relevancy",
            "faithfulness",
            "answer_pass",
            "faithfulness_pass",
        ],
    )

    writer.writeheader()
    writer.writerows(results)

print(f"\nResults saved to {OUTPUT_PATH}")














