import asyncio
import uuid
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agents.main_assistant import create_main_assistant
from agents.technical_agent import create_technical_agent
from utils.memory import memory_service

from google.adk.plugins.logging_plugin import LoggingPlugin




APP_NAME = "agents"


async def chat_demo():

    # Build both agents
    tech_agent = create_technical_agent()
    annie = create_main_assistant(tech_agent)

    # Create session + runner
    session_service = InMemorySessionService()

    runner = Runner(
        agent=annie,
        app_name=APP_NAME,      
        session_service=session_service,
        memory_service=memory_service,
        plugins=[LoggingPlugin()]
    )

    # Create new session (use keyword arguments)
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    user_id = "local_user"

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    print("Annie online. Type 'exit' to quit.")

    # Chat loop
    while True:
        user_input = input("\nYou> ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("Annie> Goodbye, See you again !!")
            break

        content = types.Content(role="user", parts=[types.Part(text=user_input)])

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if part.text:
                        print("\nAnnie>", part.text)


if __name__ == "__main__":
    asyncio.run(chat_demo())
