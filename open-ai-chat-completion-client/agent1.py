import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

gemma_model_client = OpenAIChatCompletionClient(
    model="gemma3:4b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "family": "llama"
    }
)

async def main():
    assistant = AssistantAgent(name = "assistant", model_client = gemma_model_client)
    await Console(assistant.run_stream(task = "What is 4+8 ?"))
    await gemma_model_client.close()

asyncio.run(main())
