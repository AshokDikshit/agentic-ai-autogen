import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

ollama_model_client = OllamaChatCompletionClient(
    model="mistral:7b",
    model_info={
        "family": "llama",
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "structured_output": True
    }
)

current_dir = os.getcwd()
print(current_dir)

file_sys_stdio = StdioServerParams(command = "npx",
                                   args = [
                                       "-y",
                                       "@modelcontextprotocol/server-filesystem",
                                       ".",
                                   ],
                                   read_timeout_seconds = 300
                                   )

async def main():
    fs_mcp_workbench = McpWorkbench(file_sys_stdio)
    async with fs_mcp_workbench as fs_wb:
        math_teacher = AssistantAgent(
            name = "MathTeacher",
            model_client = ollama_model_client,
            workbench = fs_wb,
            system_message="Behave like a teacher and system admin role, explain concept clearly and ask followup questions if needed."
                           "When user looks satisfied with conversation, acknowledge that and say 'LESSON COMPLETED' to end session"
        )
        student_proxy = UserProxyAgent(name="Student")
        math_class = RoundRobinGroupChat(name="MathClass_HumanInLoop", participants=[student_proxy, math_teacher],
                                         termination_condition=TextMentionTermination("LESSON COMPLETED"))
        await Console(math_class.run_stream(task="Start your math conversation, refer allowed directory and write response in that file for further analysis."))
        await ollama_model_client.close()

asyncio.run(main())
