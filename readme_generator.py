class ReadmeGenerator:
    def __init__(self, data):
        self.data = data
        self.content = ""
        # Generate license badge if license is provided(Private Method)
    def _generate_license_badge(self):
        license_name = self.data['license']
        # Format the license for a badge URL (replace spaces with _, remove dots, etc.)
        badge_license = license_name.replace(' ', '_').replace('-', '__').replace('.', '')
        license_url = f"https://choosealicense.com/licenses/{license_name.lower().split(' ')[0]}/"
        return f"[![License: {license_name}](https://img.shields.io/badge/License-{badge_license}-blue.svg)]({license_url})"



    def generate_markdown(self):
        # Get data for easy access
        title = self.data.get('title', 'My Awesome Project')
        description = self.data.get('description', 'A brief description of the project.')
        installation = self.data.get('installation', 'No installation instructions provided.')
        author = self.data.get('author', 'Unknown')
        license_badge = self._generate_license_badge()

        # Title Section
        self.content += f"# {title}\n\n"

        # Add the license badge below the title
        self.content += f"{license_badge}\n\n"

        # Description Section
        self.content += "## Description\n\n"
        self.content += '---\n'
        self.content += f"{description}\n"
      
        # Installation Section
        self.content += "---\n\n"
        self.content += "## Installation\n\n"
        self.content += "To get this project running, follow these steps:\n\n"
        self.content += "```bash\n"
        self.content += f"{installation}\n"
        self.content += "```\n\n"


        # Author/Contact Section
        self.content += "---\n\n"
        self.content += "## Author and Contact\n\n"
        self.content += f"**Author:** {author}\n\n"
        
        return self.content

    def write_file(self, filename="README.md"):
        if not self.content:
            self.generate_markdown()

        try:
            with open(filename, "w") as file:
                file.write(self.content)
            print(f"the content has been written to {filename}.")

        except:
            print(f"Error: Could not write to file {filename}.")()
            
        