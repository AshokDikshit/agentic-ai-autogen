from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

# Configuration
config_list = [
    {
        "model": "gpt-4",  # or your preferred model
        "api_key": "your-api-key"
    }
]

# System message for BDD Feature Writer Agent
bdd_agent_system_message = """
You are an expert BDD (Behavior-Driven Development) test automation engineer specializing in creating Gherkin feature files.

YOUR ROLE:
- Convert acceptance criteria and user stories into comprehensive, granular BDD feature files
- Use ONLY the pre-defined step definitions provided to you
- Break down user actions into the smallest possible atomic steps
- Create multiple test scenarios covering different testing approaches

CORE PRINCIPLES:
1. **Granularity**: Break down each action into individual steps
2. **Step Reusability**: Use ONLY steps from the provided step definition library
3. **Multiple Scenarios**: Create variations for different test approaches
4. **Explicit Waits**: Include synchronization before critical actions
5. **Realistic Flow**: Simulate actual user behavior patterns

STEP MATCHING RULES:
- Match step patterns exactly as defined in the step definition file
- Respect regex patterns: (button|link|element|radio button)
- Use correct parameter format: "elementName" in quotes
- Never invent new steps - decompose into existing ones

SCENARIO COVERAGE (create 3-5 scenarios minimum):
1. Basic happy path - simplest success flow
2. Keyboard navigation - Tab, Enter, accessibility focus
3. Mobile-specific - scroll, hide keyboard, touch interactions
4. Data-driven - Scenario Outline with Examples table
5. Explicit waits - for handling timing issues

OUTPUT: Valid Gherkin feature files with proper tags, structure, and atomic steps.
"""

# Create the BDD Feature Writer Agent
bdd_feature_writer = AssistantAgent(
    name="BDD_Feature_Writer",
    system_message=bdd_agent_system_message,
    llm_config={
        "config_list": config_list,
        "temperature": 0.3,  # Lower temperature for more consistent output
        "timeout": 120,
    }
)

# Create User Proxy Agent (represents you)
user_proxy = UserProxyAgent(
    name="QA_Lead",
    human_input_mode="NEVER",  # Set to "ALWAYS" if you want to review before execution
    max_consecutive_auto_reply=1,
    code_execution_config=False,
)


# Function to read step definitions
def read_step_definitions(file_path: str) -> str:
    """Read the step definition file content"""
    with open(file_path, 'r') as file:
        return file.read()


# Function to generate BDD feature file
def generate_bdd_feature(
        step_definitions_path: str,
        acceptance_criteria: str,
        output_file: str = None
) -> str:
    """
    Generate BDD feature file from acceptance criteria

    Args:
        step_definitions_path: Path to step definition file
        acceptance_criteria: The acceptance criteria text
        output_file: Optional output file path to save the feature

    Returns:
        Generated feature file content
    """

    # Read step definitions
    step_definitions = read_step_definitions(step_definitions_path)

    # Create the detailed task prompt
    task = f"""
TASK: Create comprehensive BDD feature file from the acceptance criteria below.

═══════════════════════════════════════════════════════════════
STEP DEFINITION LIBRARY (USE ONLY THESE STEPS):
═══════════════════════════════════════════════════════════════

{step_definitions}

═══════════════════════════════════════════════════════════════
ACCEPTANCE CRITERIA TO IMPLEMENT:
═══════════════════════════════════════════════════════════════

{acceptance_criteria}

═══════════════════════════════════════════════════════════════
REQUIREMENTS:
═══════════════════════════════════════════════════════════════

1. Analyze the acceptance criteria and identify:
   - All user actions required
   - All input fields and their values
   - All validations and expected outcomes
   - Any conditional flows or variations

2. Create AT LEAST 5 different scenario variations:
   a) Basic Happy Path - simplest successful flow
   b) Keyboard Navigation - using Tab, Enter, Space keys
   c) Mobile Flow - with scroll, hide keyboard, touch gestures
   d) Scenario Outline - data-driven with Examples table
   e) Explicit Waits - with wait conditions for stability

3. Break down EVERY action into atomic steps:
   ❌ DON'T: "When I fill the registration form"
   ✅ DO: 
      When I type "John" into "First Name" field
      And I press Tab key
      And I type "Doe" into "Last Name" field

4. Include proper synchronization:
   - Add "wait for visible" before interacting with elements
   - Add "wait for clickable" before clicking buttons
   - Add "scroll to" when elements might be off-screen
   - Add "wait for page to load" after navigation

5. Use ONLY steps from the library above - match patterns exactly:
   - Respect regex alternations: (button|link|element)
   - Use quoted parameters: "Element Name"
   - Match step keywords: Given/When/Then/And

6. Add appropriate tags:
   - @smoke - for critical happy path
   - @regression - for comprehensive coverage
   - @positive - for success scenarios
   - @negative - for error scenarios
   - @mobile - for mobile-specific tests
   - @accessibility - for keyboard navigation

7. Include realistic test data in examples

DELIVER: Complete Gherkin feature file ready for immediate execution.
"""

    # Initiate the conversation
    user_proxy.initiate_chat(
        bdd_feature_writer,
        message=task
    )

    # Get the generated feature file from the last message
    feature_content = bdd_feature_writer.last_message()["content"]

    # Optionally save to file
    if output_file:
        with open(output_file, 'w') as f:
            f.write(feature_content)
        print(f"✅ Feature file saved to: {output_file}")

    return feature_content


# Example usage
if __name__ == "__main__":
    # Your acceptance criteria
    acceptance_criteria = """
AC2: Successful Registration with Mandatory Fields

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

    # Generate the feature file
    feature_content = generate_bdd_feature(
        step_definitions_path="path/to/ui-actions.steps.ts",
        acceptance_criteria=acceptance_criteria,
        output_file="registration.feature"
    )

    print("\n" + "=" * 60)
    print("GENERATED BDD FEATURE FILE:")
    print("=" * 60)
    print(feature_content)