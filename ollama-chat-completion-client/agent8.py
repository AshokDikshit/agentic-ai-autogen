import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient

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

async def main():
    researcher = AssistantAgent(
        name = "ResearcherAgent",
        model_client = ollama_model_client,
        system_message="You are a geological researcher fellow, your job is to gater information, provide research finding and clarify if there is any query."
                       "Do not write article or create content, just provide data and facts."
    )
    contentWriter = AssistantAgent(
        name = "ContentWriter",
        model_client = ollama_model_client,
        system_message="You are a content writer, your job is to write article or blog on the basis of research data, facts and critic input given."
                       "Do not add any data which is not relevant to the data provided by researcher, just create article."
    )

    criticAgent = AssistantAgent(
        name = "CriticAgent",
        model_client = ollama_model_client,
        system_message="You are a critic, review the article and provide the feedback if any?"
                       "Say 'TERMINATE' when you are satisfied with research result."
    )

    maxMessageTermination = MaxMessageTermination(max_messages=10)
    textMentionTermination = TextMentionTermination(text='TERMINATE')
    terminationCondition = maxMessageTermination | textMentionTermination

    selectorGroupChat = SelectorGroupChat(participants=[criticAgent, researcher, contentWriter], model_client=ollama_model_client, termination_condition=terminationCondition, allow_repeated_speaker=True)
    await Console(selectorGroupChat.run_stream(task = "What is your future of Test Automation in time of Agentic AI?"))
    await ollama_model_client.close()

asyncio.run(main())
