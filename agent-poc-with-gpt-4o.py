import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    openai_client = OpenAIChatCompletionClient(
        model = "gpt-4o"
    )
    assistant = AssistantAgent(name = "assistant", model_client = openai_client)
    await Console(assistant.run_stream(task = "what is 2+2"))
    await openai_client.close()
asyncio.run(main())