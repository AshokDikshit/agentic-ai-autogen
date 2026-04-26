import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemma3:4b",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "structured_output": False,
            "family": "unknown"
        }
    )
    assistant = AssistantAgent(name = "assistant", model_client = model_client)
    await Console(assistant.run_stream(task = "What is 4+8 ?"))
    await model_client.close()

asyncio.run(main())
