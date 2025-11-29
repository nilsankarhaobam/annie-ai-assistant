from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from utils.config import GOOGLE_API_KEY
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

def create_technical_agent():
    return LlmAgent(
        name="technical_agent",

        description="Handles coding, debugging, architecture, MERN, Python, OOP, and AI basics.",

        model=Gemini(
            model="gemini-2.5-flash",
            api_key=GOOGLE_API_KEY,
            retry_options=retry_config
        ),

        instruction="""
You are a technical specialist.

Your responsibilities:
- Understand and debug code
- Explain what went wrong
- Provide corrected versions
- Use clear steps

When fixing code:
1. Identify the problem and explicitly mention the word "error".
2. Explain why the error occurs.
3. Provide the corrected code block.
4. Offer a short explanation.

Example format:
"There is an error because ... The corrected code is: ..."
""",

        tools=[google_search],
    )
