import sys
import os
import json
import asyncio

# ------------------------------------------------------------
# Adds project root folder (Annie/) to PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# ------------------------------------------------------------
# IMPORTS FROM ANNIE PROJECT
# ------------------------------------------------------------
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.main_assistant import create_main_assistant
from utils.memory import memory_service

APP_NAME = "agents"  

# ------------------------------------------------------------
# EVALUATION QUERIES
# ------------------------------------------------------------
evaluation_tests = {
    "creator_test_correct": {
        "input": [
            "I am your creator",
            "001122334455"
        ],
        "expected_keywords": ["Boss", "Verification complete"]
    },
    "creator_test_wrong_code": {
        "input": [
            "I am your creator",
            "999999"
        ],
        "expected_keywords": ["incorrect", "failed"]
    },
    "memory_test_basic": {
        "input": [
            "My favorite color is blue.",
            "What is my favorite color?"
        ],
        "expected_keywords": ["blue"]
    },
    "technical_test": {
        "input": [
            "Fix this code:\nprin('hello')"
        ],
        "expected_keywords": ["print", "error"]
    }
}

# ------------------------------------------------------------
# RUN SINGLE TEST
# ------------------------------------------------------------
async def run_test(test_name, test_data):

    print(f"\n🔎 Running Test: {test_name}")

    # Build agent fresh for each test
    annie = create_main_assistant()

    session_service = InMemorySessionService()

    runner = Runner(
        agent=annie,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service
    )

    session_id = f"session_eval_{test_name}"
    user_id = "eval_user"

    # FIXED: keyword-only arguments
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    output_text = ""

    for message in test_data["input"]:
        content = types.Content(role="user", parts=[types.Part(text=message)])

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        output_text += part.text + "\n"

    print("Output:")
    print(output_text)

    # ------------------------------------------------------------
    # CHECK EXPECTED KEYWORDS
    # ------------------------------------------------------------
    success = all(keyword.lower() in output_text.lower()
                  for keyword in test_data["expected_keywords"])

    if success:
        print(f"Test Passed: {test_name}")
    else:
        print(f"Test Failed: {test_name}")

    return {
        "test": test_name,
        "passed": success,
        "output": output_text
    }

# ------------------------------------------------------------
# RUN ALL TESTS
# ------------------------------------------------------------
async def run_all_tests():

    print("\n Running Annie Agent Evaluation Suite...\n")

    results = {}

    for test_name, test_data in evaluation_tests.items():
        result = await run_test(test_name, test_data)
        results[test_name] = result

    # Save evaluation results
    output_path = os.path.join(ROOT_DIR, "evaluation", "eval_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print("\n Evaluation complete!")
    print(f"Results saved to: evaluation/eval_results.json\n")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
