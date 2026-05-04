import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.ollama import OllamaChatCompletionClient
from demo.StepDefinitionReader import get_step_library_for_agent

project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))

ollama_chat_completion_model = OllamaChatCompletionClient(
    model = "qwen2.5:7b",
    model_info = {
        "family": "llama",
        "vision": True,
        "json_output": True,
        "function_calling": True,
        "structured_output": True,
        "multiple_system_messages": True
    }
)

async def generate_bdd_with_step_library(
        step_def_folder: str,
        acceptance_criteria: str,
        scenario_requirement: str,
        output_file: str = "generated_feature.feature"
) -> str:
    """
    Generate BDD feature file using step definitions from a folder
    Args:
        step_def_folder: Path to folder containing step definition files
        acceptance_criteria: Acceptance criteria text
        output_file: Output feature file path

    Returns:
        Generated feature file content
        :param output_file:
        :param step_def_folder:
        :param acceptance_criteria:
        :param scenario_requirement:
    """

    # Load step definitions from folder
    # print("📂 Loading step definitions from folder...")
    print("Loading step definitions from folder...")
    step_library = get_step_library_for_agent(step_def_folder)

    # Create BDD agent
    bdd_agent = AssistantAgent(
        name="BDD_Feature_Writer",
        model_client=ollama_chat_completion_model,
        system_message=f"""
        You are an expert BDD test automation engineer. Your ONLY task is to map Acceptance Criteria to a specific Gherkin Step Library.

        ### STRICT RULES:
        1. USE ONLY the provided Step Definitions. 
        2. Include proper synchronization (waits, scrolls)        
        3. ATOMICITY: Break down every Acceptance Criterion into the smallest possible actions.
        4. SYNTAX: Follow the Gherkin standard (Feature, Scenario, Given, When, Then, And).
        5. FORMATTING: Output the Feature file content ONLY. Do not provide explanations or chat.
        6. BDD TAGS: Add appropriate tags (@smoke, @regression, @mobile, etc.)
        
        ### EXECUTION EXAMPLE:
        Follow the exact pattern of the provided step library. Wrap element name and value in double quotes as given example below.
        Example pattern: 
            When I type "text" into "element" field
            Then "expected_text" should be visible

        ### AVAILABLE STEP DEFINITIONS:
        {step_library}
        """
    )

    user_proxy = UserProxyAgent(
        name="QA_Lead"
    )

    # Create task with step library
    task = f"""
    {'=' * 80}
    ACCEPTANCE CRITERIA:
    {'=' * 80}
    {acceptance_criteria}
    {'=' * 80}
    REQUIREMENTS:
    {'=' * 80}
    {scenario_requirement}
    {'=' * 80}
    \nTASK: Create BDD feature file from acceptance criteria using ONLY the steps below.   
    """

    feature_file_creator = RoundRobinGroupChat(name = "Create_Executable_Gherkin", participants = [user_proxy, bdd_agent],
                                               termination_condition = TextMentionTermination("Feature files created"))

    await Console(feature_file_creator.run_stream(task = task))
    await ollama_chat_completion_model.close()
    return "Feature files created"

# Example Usage
async def main():

    step_definitions = project_root + "/tests/step-definitions"

    scenario_requirement = """
    Create test scenario variations:
       - Basic happy path
       - Negative Scenarios - Invalid Email
       - Negative Scenarios - Invalid Password
    """

    acceptance_criteria = """
    AC1: Successful Registration with Mandatory Fields
    * Given I am on the registration page
    * When I enter valid data in all mandatory fields:
       * First Name
       * Last Name
       * Email Address
       * Password
       * Confirm Password
       * Mobile Number
       * Accept Terms & Conditions checkbox
    * And I click "Create Account" button
    * Then I should see a success message "Account created successfully"
    * And I should receive a verification email
    * And I should be redirected to the email verification page
    """

    # Generate feature file using step definitions from folder
    feature = await generate_bdd_with_step_library(
        step_def_folder=step_definitions,
        acceptance_criteria=acceptance_criteria,
        scenario_requirement=scenario_requirement,
        output_file="registration.feature"
    )

    print("\n" + "=" * 80)
    print("GENERATED FEATURE FILE:")
    print("=" * 80)
    print(feature)

asyncio.run(main())
