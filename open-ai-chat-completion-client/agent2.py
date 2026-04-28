import asyncio
from pathlib import Path
from pyexpat.errors import messages

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

gemma_model_client = OpenAIChatCompletionClient(
    model="gemma3:4b",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model_info={
        "vision": True,
        "function_calling": True,
        "json_output": True,
        "structured_output": True,
        "family": "llama"
    }
)

async def main():
    assistant = AssistantAgent(name = "MultiModelAssistant", model_client = gemma_model_client)
    image = Image.from_file(Path("/Users/ashdiksh/Downloads/WhatsAppImage.jpeg"))
    multi_model_message = MultiModalMessage(
        content = ["What do you see in this image?", image], source="user"
    )
    await Console(assistant.run_stream(task = multi_model_message))
    await gemma_model_client.close()

asyncio.run(main())
