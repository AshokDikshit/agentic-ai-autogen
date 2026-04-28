import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import Workbench
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

os.environ["JIRA_URL"] = ""
os.environ["JIRA_USERNAME"] = ""
os.environ["JIRA_API_TOKEN"] = ""

ollama_chat_completion_model = OllamaChatCompletionClient(
    model = "mistral:7b",
    model_info = {
        "family": "llama",
        "vision": True,
        "function_calling": True,
        "structured_output": True,
        "json_output": True,
        "multiple_system_messages": True
    }
)

mcp_server_param = StdioServerParams(
    command="docker",
    args=[
        "run", "-i", "--rm",
        "-e", "JIRA_URL",
        "-e", "JIRA_USERNAME",
        "-e", "JIRA_API_TOKEN",
        "ghcr.io/sooperset/mcp-atlassian:latest"
    ]

)

mcp_workbench = McpWorkbench(
    server_params=mcp_server_param
)

async def main():
    agent = AssistantAgent(
        name="JIRA_Agent",
        model_client=ollama_chat_completion_model,
    )
    result = agent.run_stream(task="Name two cities in North America.")
    await Console(result)

asyncio.run(main())
