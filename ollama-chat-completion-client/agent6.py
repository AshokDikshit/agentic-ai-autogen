import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient

ollama_model_client = OllamaChatCompletionClient(
    model="llama3.2:3b",
    model_info={
        "family": "llama",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True
    }
)
    
async def main():
    assistant = AssistantAgent(name = "assistant", model_client = ollama_model_client)
    await Console(assistant.run_stream(task = "What is 4+8 ?"))
    await ollama_model_client.close()

asyncio.run(main())
