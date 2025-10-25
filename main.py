import questionary
from questionary import Separator
from readme_generator import ReadmeGenerator


LICENSE_CHOICES = [
    'MIT License',
    'GNU GPLv3',
    'Apache License 2.0',
    'ISC License',
    Separator(), # Adds a visual divider in the list
    'Unlicensed'
]

def ask_questions():
    answers = {}
    try:
        answers['title'] = questionary.text("Project Title (e.g., Python README Generator):").ask()
        answers['description'] = questionary.text(
            "Project Description (Press Esc+Enter when done):",
            multiline=True
        ).ask()
        answers['installation'] = questionary.text(
            "Installation Instructions (Press Esc+Enter when done):",
            multiline=True
        ).ask()

        answers['tech_stack'] = questionary.text( 
            "Skill Icons Keywords (e.g., html,css,js,react,mongodb):",
            multiline=True
        ).ask()
        answers['license'] = questionary.select(
            "Choose a License:",
            choices=LICENSE_CHOICES
        ).ask()

        answers['author'] = questionary.text(
            "Author Name:"
        ).ask()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        return None

    return answers


def main():
    print("--- README.MD Generator CLI ---")
    results = ask_questions()
    generator = ReadmeGenerator(results)

    print(generator.write_file())
    print("\n--- Answers Received ---")
    print(results)


main()