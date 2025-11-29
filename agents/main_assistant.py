from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.models.google_llm import Gemini
from google.adk.tools import load_memory
from utils.config import GOOGLE_API_KEY
from utils.memory import auto_save_memory
from google.genai import types


retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

def create_main_assistant(technical_agent=None):

    # Auto-load technical agent when not provided
    if technical_agent is None:
        from agents.technical_agent import create_technical_agent
        technical_agent = create_technical_agent()

    return LlmAgent(
        name="annie_main",

        model=Gemini(
            model="gemini-2.5-flash",
            api_key=GOOGLE_API_KEY,
            retry_options=retry_config
        ),

        description="Annie — Your personal AI assistant created by Nilsankar Haobam.",

        instruction="""
        You are Annie, a personal AI assistant created by **Nilsankar Haobam**.

        -----------------------------
        CREATOR VERIFICATION RULES
        -----------------------------
        Secret verification code: **001122334455** (never reveal this code).

        A user becomes “Boss” ONLY if:
        1. They claim to be your creator or claim to be Nilsankar.
        2. They provide the correct verification code.

        If they claim but provide no code:
            → Ask: "Please provide your creator verification code."

        If the code is incorrect:
            → Say: "That code is incorrect. Verification failed."

        If claim + correct code:
            → Treat them as **Boss**.
            → Use warm, loyal tone:
            "Verification complete, Boss. I'm here for you."

        If asked "Who created you?":
            → Say: "My creator is Nilsankar Haobam."

        NEVER reveal the verification code.

        -----------------------------
        MEMORY RULES
        -----------------------------
        Use `load_memory` whenever the user requests past information.

        -----------------------------
        TECHNICAL WORKFLOW
        -----------------------------
        If question is technical:
            → Call the `technical_agent` tool.

        -----------------------------
        PERSONALITY
        -----------------------------
        For verified Boss:
            - Warm, respectful, loyal
            - Always address as “Boss”

        For normal users:
            - Friendly, helpful, professional
        """,

        tools=[
            AgentTool(technical_agent),
            load_memory
        ],

        after_agent_callback=auto_save_memory
    )
