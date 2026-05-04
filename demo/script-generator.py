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
        "function_calling": True,
        "structured_output": True,
        "json_output": True,
        "multiple_system_messages": True
    }
)

async def generate_bdd_with_step_library(
        step_def_folder: str,
        acceptance_criteria: str,
        test_scenario_variations: str,
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
    """

    # Load step definitions from folder
    # print("📂 Loading step definitions from folder...")
    print("Loading step definitions from folder...")
    step_library = get_step_library_for_agent(step_def_folder)

    # Create BDD agent
    bdd_agent = AssistantAgent(
        name="BDD_Feature_Writer",
        system_message="""
You are an expert BDD test automation engineer.
Create comprehensive Gherkin feature files using ONLY the provided step definitions.
Break down actions into atomic steps. Create multiple scenario variations.
Never invent new steps - use only what's provided in the step library.
""",
        model_client=ollama_chat_completion_model
    )

    user_proxy = UserProxyAgent(
        name="QA_Lead"
    )

    # Create task with step library
    task = f"""
TASK: Create BDD feature file from acceptance criteria using ONLY the steps below.

{'=' * 80}
AVAILABLE STEP DEFINITIONS:
{'=' * 80}

{step_library}

{'=' * 80}
ACCEPTANCE CRITERIA:
{'=' * 80}
{acceptance_criteria}
{'=' * 80}
REQUIREMENTS:
{'=' * 80}
1. Use ONLY steps from the library above
2. Break actions into atomic steps
3. Include proper synchronization (waits, scrolls)
4. Add appropriate tags (@smoke, @regression, @mobile, etc.)

{test_scenario_variations}
"""
    feature_file_creator = RoundRobinGroupChat(name = "Create_Executable_Gherkin", participants = [user_proxy, bdd_agent],
                                               termination_condition = TextMentionTermination("Executable Gherkin files created"))
    await Console(feature_file_creator.run_stream(task = task))
    await ollama_chat_completion_model.close()
    return "Executable Gherkin files created."


# Example Usage
async def main():
    print(project_root)
    step_definitions = project_root + "/tests/step-definitions"

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

    test_scenario_variations = """
Create test scenario variations:
   - Basic happy path
   - Negative Scenarios - Invalid Email
   - Negative Scenarios - Invalid Password
    """

    # Generate feature file using step definitions from folder
    feature = await generate_bdd_with_step_library(
        step_def_folder=step_definitions,
        acceptance_criteria=acceptance_criteria,
        test_scenario_variations=test_scenario_variations,
        output_file="registration.feature"
    )

    print("\n" + "=" * 80)
    print("GENERATED FEATURE FILE:")
    print("=" * 80)
    print(feature)

asyncio.run(main())
