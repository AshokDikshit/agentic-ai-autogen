import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient

ollama_model_client = OllamaChatCompletionClient(
    model="gemma3:4b",
    model_info={
        "family": "llama",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True
    }
)

async def main():
    response = await ollama_model_client.create([UserMessage(content="What is 5+7?", source="user")])
    print(response)
    await ollama_model_client.close()

asyncio.run(main())
