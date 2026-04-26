import asyncio
from pyexpat.errors import messages

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

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

async def main():
    assistant = AssistantAgent(name = "MultiModelAssistant", model_client = model_client)
    image = Image.from_file("/Users/ashdiksh/Downloads/WhatsAppImage.jpeg")
    multimodelmessage = MultiModalMessage(
        content = ["What do you see in this image?", image], source="user"
    )
    await Console(assistant.run_stream(task = multimodelmessage))
    await model_client.close()

asyncio.run(main())
