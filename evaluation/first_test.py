from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is FastAPI?",
    actual_output="FastAPI is a Python web framework",
    expected_output="FastAPI is a modern Python web framework"
)

print(test_case)