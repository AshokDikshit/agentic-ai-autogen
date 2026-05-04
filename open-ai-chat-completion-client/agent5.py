import asyncio
from pyexpat.errors import messages

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMessageTermination, MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

gemma_model_client = OpenAIChatCompletionClient(
    model="deepseek-v4",  # DeepSeek-V4 backend
    api_key="sk-a4b6e6beaae74ddfb59f46ba507e48b1",
    base_url="https://api.deepseek.com",
    model_info = {
        "family": "llama",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True
    }
)

async def main():
    math_teacher = AssistantAgent(
        name = "MathTeacher",
        model_client = gemma_model_client,
        system_message="Behave like a teacher, explain concept clearly and ask followup questions if needed."
                        "When user looks satisfied with conversation, acknowledge that and say 'LESSION COMPLETED' to end session"
    )
    student_proxy = UserProxyAgent(name="Student")
    math_class = RoundRobinGroupChat(name="MathClass_HumanInLoop", participants=[student_proxy, math_teacher], termination_condition = TextMentionTermination("LESSION COMPLETED"))
    await Console(math_class.run_stream(task = "Start your math conversation:"))
    await gemma_model_client.close()

asyncio.run(main())
