import questionary

def main():
    """
    Main function to run the README generator application.
    """
    print("--- Python README File Generator ---\n")

    questionary.text("What's your first name").ask()
    questionary.password("What's your secret?").ask()
    questionary.confirm("Are you amazed?").ask()

    questionary.select(
        "What do you want to do?",
        choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
    ).ask()


main()