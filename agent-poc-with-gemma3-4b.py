import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
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
    assistant = AssistantAgent(
        name="assistant",
        model_client=model_client,
    )
    response = await assistant.on_messages(
        [TextMessage(content="What is AutoGen? Give one liner only", source="user")], CancellationToken()
    )
    print(response.chat_message.content)

asyncio.run(main())