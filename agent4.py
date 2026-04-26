import asyncio
from pyexpat.errors import messages

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMessageTermination, MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
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
    math_teacher = AssistantAgent(
        name = "MathTeacher",
        model_client = model_client,
        system_message="Behave like a teacher, explain concept clearly and ask followup questions if needed."
                        "When user looks satisfied with conversation, acknowledge that and say 'LESSION COMPLETED' to end session"
    )
    student_proxy = UserProxyAgent(name="Student")
    math_class = RoundRobinGroupChat(name="MathClass", participants=[student_proxy, math_teacher], termination_condition = TextMentionTermination("LESSION COMPLETED"))
    await Console(math_class.run_stream(task = "Start your conversation regarding math:"))

    await model_client.close()

asyncio.run(main())
