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
        self.content += "## Description\n"
        self.content += '---'
        self.content += f"{description}\n"
      
        return self.content

    def write_file(self, filename="README.md"):
        if not self.content:
            self.generate_markdown()

        try:
            with open(filename, "w") as file:
                file.write(self.content)
            print(f"the content has been written to {filename}.")

        except:
            print(f"Error: Could not write to file {filename}.")
            
        