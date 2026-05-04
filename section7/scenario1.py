import asyncio
import os
from email.policy import default

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ChatCompletionClient
from autogen_core.tools import Workbench
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

os.environ["JIRA_URL"] = ""
os.environ["JIRA_USERNAME"] = ""
os.environ["JIRA_API_TOKEN"] = ""

ollama_chat_completion_model = OllamaChatCompletionClient(
    model = "qwen2.5:7b",
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

mcp_server_playwright = StdioServerParams(
    command="npx",
    args= [
        "@playwright/mcp@latest"
    ]
)

workbench_playwright = McpWorkbench(
    server_params=mcp_server_playwright
)

async def main():

    async with workbench_playwright as wb_playwright:
        agent = AssistantAgent(
            name="Playwright_Agent",
            model_client=ollama_chat_completion_model,
            workbench=wb_playwright,
            system_message="You are a PlayWright Automation agent capable of browsing and retrieving data."
                           "When user looks happy, just say 'Execution Completed'"
        )
        engineer = UserProxyAgent(name="Engineer")
        team = SelectorGroupChat(
            participants=[agent, engineer],
            model_client=ollama_chat_completion_model,
            termination_condition=TextMentionTermination(text="Execution Completed")
        )
        result = team.run_stream(task="Just open google.com and then close the browser.")
        await Console(result)

asyncio.run(main())
