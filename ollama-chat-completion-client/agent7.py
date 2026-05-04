import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
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
    helperAgent = AssistantAgent(
        name = "Agent1_Helper",
        model_client = ollama_model_client
    )
    backupAgent = AssistantAgent(
        name = "Agent2_Backup",
        model_client = ollama_model_client
    )
    await Console(helperAgent.run_stream(task = "I come from Raipaty a small village somewhere in India. There is a lord Shiva temple near my village."))

    state = await helperAgent.save_state()
    await backupAgent.load_state(state)

    await Console(backupAgent.run_stream(task="What is my village name?"))

    await ollama_model_client.close()

asyncio.run(main())
