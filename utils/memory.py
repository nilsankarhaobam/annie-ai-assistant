from google.adk.memory import InMemoryMemoryService
from google.adk.agents.callback_context import CallbackContext

memory_service = InMemoryMemoryService()

async def auto_save_memory(callback_context: CallbackContext):
    mem = callback_context._invocation_context.memory_service
    session = callback_context._invocation_context.session
    await mem.add_session_to_memory(session)
