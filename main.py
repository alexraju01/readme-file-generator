import questionary
from readme_generator import ReadmeGenerator

def ask_questions():
    answers = {}
    try:
        answers['title'] = questionary.text("Project Title (e.g., Python README Generator):").ask()
        answers['description'] = questionary.text(
            "Project Description (Press Esc+Enter when done):",
            multiline=True
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