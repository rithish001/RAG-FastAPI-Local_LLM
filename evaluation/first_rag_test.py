from deepeval.test_case import LLMTestCase
from app.services.rag_service import ask_question
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import FaithfulnessMetric
from deepeval.models import OllamaModel




question = "Which backend framework is mentioned?"

result = ask_question(question, user="Rithish")

judge_model = OllamaModel(
    model="qwen2.5:0.5b",
    base_url="http://localhost:11434",
    temperature=0
)

# metric = AnswerRelevancyMetric(
#     threshold=0.7,
#     model=judge_model
# )

metric = FaithfulnessMetric(
     threshold=0.7,
     model=judge_model
)

test_case = LLMTestCase(
    input=question,
    actual_output=result["answer"],
    expected_output="The backend framework mentioned in the document is FastAPI",
    retrieval_context=result["context"],

)

metric.measure(test_case)


print(test_case)
print('\n')
print(metric.score)
print('\n')
print(metric.reason)
print('\n')
print(metric.success)
