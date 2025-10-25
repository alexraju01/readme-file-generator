class ReadmeGenerator:
    def __init__(self, data):
        self.data = data
        self.content = ""

    def generate_markdown(self):
        # Get data for easy access
        title = self.data.get('title', 'My Awesome Project')
        description = self.data.get('description', 'A brief description of the project.')

        self.content += f"# {title}\n\n"
        

        # Description Section
        self.content += "## Description\n\n"
        self.content += f"{description}\n"
        return self.content

