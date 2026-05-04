import os
import re
from typing import List, Dict, Set
from pathlib import Path
import json


class StepDefinitionReader:
    """
    Reads and parses step definition files to extract available BDD steps.
    Supports TypeScript (.ts), JavaScript (.js), Python (.py), and Java (.java) files.
    """

    def __init__(self, step_definitions_folder: str):
        """
        Initialize the reader with a folder path

        Args:
            step_definitions_folder: Path to folder containing step definition files
        """
        self.folder_path = Path(step_definitions_folder)
        self.step_definitions = []
        self.step_patterns = []
        self.step_types = {'Given': [], 'When': [], 'Then': []}
        self.raw_content = ""

    def read_all_files(self) -> Dict:
        """
        Read all step definition files from the folder

        Returns:
            Dictionary containing all extracted step information
        """
        if not self.folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {self.folder_path}")

        # Supported file extensions
        supported_extensions = ['.ts', '.js', '.py', '.java']

        # Find all step definition files
        step_files = []
        for ext in supported_extensions:
            step_files.extend(self.folder_path.glob(f'**/*{ext}'))

        print(f"📁 Found {len(step_files)} step definition files")

        # Read and parse each file
        for file_path in step_files:
            print(f"📄 Reading: {file_path.name}")
            self._parse_file(file_path)

        return self._compile_results()

    def _parse_file(self, file_path: Path):
        """Parse a single step definition file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.raw_content += f"\n\n{'=' * 60}\n"
                self.raw_content += f"FILE: {file_path.name}\n"
                self.raw_content += f"{'=' * 60}\n\n"
                self.raw_content += content

                # Detect file type and parse accordingly
                if file_path.suffix in ['.ts', '.js']:
                    self._parse_typescript_javascript(content, file_path.name)
                elif file_path.suffix == '.py':
                    self._parse_python(content, file_path.name)
                elif file_path.suffix == '.java':
                    self._parse_java(content, file_path.name)

        except Exception as e:
            print(f"⚠️  Error reading {file_path.name}: {str(e)}")

    def _parse_typescript_javascript(self, content: str, filename: str):
        """Parse TypeScript/JavaScript step definitions (WebdriverIO, Cucumber)"""

        # Pattern to match Given/When/Then step definitions
        # Matches: Given(/^pattern$/, async (params) => {
        # Also matches: When('pattern', async function() {
        patterns = [
            r"(Given|When|Then|And)\s*\(\s*\/([^\/]+)\/[^,]*,",  # Regex pattern
            r"(Given|When|Then|And)\s*\(\s*['\"]([^'\"]+)['\"]",  # String pattern
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                step_type = match.group(1)
                step_pattern = match.group(2)

                # Clean up the pattern
                step_pattern = self._clean_pattern(step_pattern)

                step_info = {
                    'type': step_type,
                    'pattern': step_pattern,
                    'regex': step_pattern,
                    'file': filename,
                    'example': self._generate_example(step_pattern)
                }

                self.step_definitions.append(step_info)
                self.step_patterns.append(step_pattern)
                self.step_types[step_type].append(step_pattern)

    def _parse_python(self, content: str, filename: str):
        """Parse Python step definitions (Behave, Pytest-BDD)"""

        # Pattern for @given, @when, @then decorators
        patterns = [
            r"@(given|when|then)\s*\(\s*['\"]([^'\"]+)['\"]",
            r"@(given|when|then)\s*\(\s*r['\"]([^'\"]+)['\"]",  # Raw strings
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                step_type = match.group(1).capitalize()
                step_pattern = match.group(2)

                step_pattern = self._clean_pattern(step_pattern)

                step_info = {
                    'type': step_type,
                    'pattern': step_pattern,
                    'regex': step_pattern,
                    'file': filename,
                    'example': self._generate_example(step_pattern)
                }

                self.step_definitions.append(step_info)
                self.step_patterns.append(step_pattern)

                if step_type in self.step_types:
                    self.step_types[step_type].append(step_pattern)

    def _parse_java(self, content: str, filename: str):
        """Parse Java step definitions (Cucumber-Java)"""

        # Pattern for @Given, @When, @Then annotations
        pattern = r"@(Given|When|Then)\s*\(\s*['\"]([^'\"]+)['\"]"

        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            step_type = match.group(1)
            step_pattern = match.group(2)

            step_pattern = self._clean_pattern(step_pattern)

            step_info = {
                'type': step_type,
                'pattern': step_pattern,
                'regex': step_pattern,
                'file': filename,
                'example': self._generate_example(step_pattern)
            }

            self.step_definitions.append(step_info)
            self.step_patterns.append(step_pattern)
            self.step_types[step_type].append(step_pattern)

    def _clean_pattern(self, pattern: str) -> str:
        """Clean and normalize step pattern"""
        # Remove leading/trailing special characters
        pattern = pattern.strip('^$')

        # Replace common regex patterns with readable placeholders
        replacements = [
            (r'\(\[\^"\]\*\)', '<text>'),  # ([^"]*) -> <text>
            (r'\(\[\\d\]\+\)', '<number>'),  # (\\d+) -> <number>
            (r'\(\.\*\)', '<any>'),  # (.*) -> <any>
            (r'\\d\+', '<number>'),
            (r'\(\?\:', '('),  # Non-capturing groups
        ]

        for regex, replacement in replacements:
            pattern = re.sub(regex, replacement, pattern)

        return pattern

    def _generate_example(self, pattern: str) -> str:
        """Generate a usage example from the pattern"""
        example = pattern

        # Replace regex groups with example values
        example = re.sub(r'\(\[\\w\s\]\+\)', '"Example Text"', example)
        example = re.sub(r'<text>', '"example"', example)
        example = re.sub(r'<number>', '5', example)
        example = re.sub(r'<any>', 'something', example)
        example = re.sub(r'\(([^|)]+)\|([^)]+)\)', r'\1', example)  # Take first option from alternation

        return example

    def _compile_results(self) -> Dict:
        """Compile all results into a structured dictionary"""
        return {
            'total_steps': len(self.step_definitions),
            'steps_by_type': {
                'Given': len(self.step_types['Given']),
                'When': len(self.step_types['When']),
                'Then': len(self.step_types['Then'])
            },
            'all_steps': self.step_definitions,
            'step_patterns': self.step_patterns,
            'steps_by_type_detailed': self.step_types,
            'raw_content': self.raw_content
        }

    def get_formatted_step_library(self) -> str:
        """
        Get a formatted string of all available steps for AI agent consumption

        Returns:
            Formatted string containing all step definitions
        """
        output = []
        output.append("=" * 80)
        output.append("AVAILABLE BDD STEP DEFINITIONS")
        output.append("=" * 80)
        output.append(f"\nTotal Steps: {len(self.step_definitions)}\n")

        # Group by type
        for step_type in ['Given', 'When', 'Then']:
            if self.step_types[step_type]:
                output.append(f"\n{'=' * 80}")
                output.append(f"{step_type.upper()} STEPS ({len(self.step_types[step_type])})")
                output.append(f"{'=' * 80}\n")

                for idx, step in enumerate(self.step_types[step_type], 1):
                    output.append(f"{idx}. {step_type} {step}")

        output.append(f"\n{'=' * 80}")
        output.append("USAGE EXAMPLES")
        output.append(f"{'=' * 80}\n")

        # Add some examples
        for step_info in self.step_definitions[:10]:  # First 10 examples
            output.append(f"{step_info['type']} {step_info['example']}")

        return "\n".join(output)

    def get_step_library_for_llm(self) -> str:
        """
        Get step library formatted specifically for LLM consumption
        Includes patterns, examples, and usage guidelines
        """
        output = []
        output.append("STEP DEFINITION LIBRARY - USE ONLY THESE STEPS")
        output.append("=" * 80)
        output.append(f"Total Available Steps: {len(self.step_definitions)}\n")

        # Categorize steps by action type
        categories = self._categorize_steps()

        for category, steps in categories.items():
            if steps:
                output.append(f"\n## {category}")
                output.append("-" * 60)
                for step in steps:
                    output.append(f"  {step['type']} {step['pattern']}")
                    if step['example'] != step['pattern']:
                        output.append(f"    Example: {step['type']} {step['example']}")
                output.append("")

        return "\n".join(output)

    def _categorize_steps(self) -> Dict[str, List]:
        """Categorize steps by their action type"""
        categories = {
            'NAVIGATION': [],
            'CLICK ACTIONS': [],
            'TEXT INPUT': [],
            'WAIT CONDITIONS': [],
            'FORM INTERACTIONS': [],
            'MOBILE GESTURES': [],
            'ASSERTIONS': [],
            'OTHER': []
        }

        keywords = {
            'NAVIGATION': ['navigate', 'go back', 'go forward', 'refresh', 'reload', 'switch', 'open', 'close'],
            'CLICK ACTIONS': ['click', 'double click', 'right click', 'hover'],
            'TEXT INPUT': ['type', 'enter', 'clear', 'select all'],
            'WAIT CONDITIONS': ['wait for', 'wait'],
            'FORM INTERACTIONS': ['check', 'uncheck', 'select', 'dropdown', 'upload', 'submit'],
            'MOBILE GESTURES': ['swipe', 'pinch', 'zoom', 'rotate', 'shake', 'lock'],
            'ASSERTIONS': ['should see', 'should be', 'should contain', 'verify', 'assert']
        }

        for step in self.step_definitions:
            pattern_lower = step['pattern'].lower()
            categorized = False

            for category, keys in keywords.items():
                if any(key in pattern_lower for key in keys):
                    categories[category].append(step)
                    categorized = True
                    break

            if not categorized:
                categories['OTHER'].append(step)

        return categories

    def export_to_json(self, output_file: str):
        """Export step definitions to JSON file"""
        results = self._compile_results()

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)

        print(f"✅ Step definitions exported to: {output_file}")

    def get_statistics(self) -> Dict:
        """Get statistics about the step definitions"""
        return {
            'total_steps': len(self.step_definitions),
            'given_steps': len(self.step_types['Given']),
            'when_steps': len(self.step_types['When']),
            'then_steps': len(self.step_types['Then']),
            'unique_patterns': len(set(self.step_patterns)),
            'files_processed': len(set(s['file'] for s in self.step_definitions))
        }


# ============================================================================
# USAGE FUNCTIONS
# ============================================================================

def load_step_definitions(folder_path: str) -> StepDefinitionReader:
    """
    Main function to load step definitions from a folder

    Args:
        folder_path: Path to the folder containing step definition files

    Returns:
        StepDefinitionReader instance with all loaded steps
    """
    reader = StepDefinitionReader(folder_path)
    reader.read_all_files()

    # Print statistics
    stats = reader.get_statistics()
    print("\n" + "=" * 60)
    print("STEP DEFINITION STATISTICS")
    print("=" * 60)
    print(f"Total Steps Found: {stats['total_steps']}")
    print(f"  - Given Steps: {stats['given_steps']}")
    print(f"  - When Steps: {stats['when_steps']}")
    print(f"  - Then Steps: {stats['then_steps']}")
    print(f"Unique Patterns: {stats['unique_patterns']}")
    print(f"Files Processed: {stats['files_processed']}")
    print("=" * 60 + "\n")

    return reader


def get_step_library_for_agent(folder_path: str) -> str:
    """
    Get formatted step library ready for AI agent consumption

    Args:
        folder_path: Path to step definitions folder

    Returns:
        Formatted string of all available steps
    """
    reader = load_step_definitions(folder_path)
    return reader.get_step_library_for_llm()


def get_raw_step_content(folder_path: str) -> str:
    """
    Get raw content of all step definition files
    Useful for giving complete context to AI agents

    Args:
        folder_path: Path to step definitions folder

    Returns:
        Raw content of all step definition files
    """
    reader = load_step_definitions(folder_path)
    return reader.raw_content

