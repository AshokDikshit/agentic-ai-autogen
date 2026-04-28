import asyncio
from pyexpat.errors import messages

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMessageTermination, MaxMessageTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_ext.models.openai import OpenAIChatCompletionClient

gemma_model_client = OpenAIChatCompletionClient(
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
    math_teacher = AssistantAgent(
        name = "MathTeacher",
        model_client = gemma_model_client,
        system_message="Behave like a teacher, explain concept clearly and ask followup questions if needed."
    )
    student = AssistantAgent(
        name = "Student",
        model_client = gemma_model_client,
        system_message="Behave like a student, ask math related questions to teacher till you satisfied."
    )

    math_class = RoundRobinGroupChat(name="RoundRobinGroupChat", participants=[math_teacher, student], termination_condition = MaxMessageTermination(max_messages = 6))
    await Console(math_class.run_stream(task = "Let's discuss what is addition and how it works? "))

    await gemma_model_client.close()

asyncio.run(main())
