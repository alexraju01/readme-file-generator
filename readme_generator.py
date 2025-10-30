class ReadmeGenerator:
    def __init__(self, data):
        self.data = data
        self.content = ""


        # Generate license badge if license is provided (Private Method)
    def _generate_license_badge(self):
        license_name = self.data['license']
        # Format the license for a badge URL (replace spaces with _, remove dots, etc.)
        badge_license = license_name.replace(' ', '_').replace('-', '__').replace('.', '')
        license_url = f"https://choosealicense.com/licenses/{license_name.lower().split(' ')[0]}/"
        return f"[![License: {license_name}](https://img.shields.io/badge/License-{badge_license}-blue.svg)]({license_url})"

    # Generate tech stack badge (Private Method)
    def _generate_tech_stack_badge(self):
        tech_stack_input = self.data.get('tech_stack', '').strip()
        
        if not tech_stack_input:
            return ""

        keywords_str = tech_stack_input.replace('\n', ',')
        keywords_str = keywords_str.replace(' ', ',')

        cleaned_keywords = [
            word.strip().lower() 
            for word in keywords_str.split(',') 
            if word.strip() # Ensures non-empty strings are kept
        ]

        # Format for the skillicons URL: 'keyword1,keyword2,keyword3'
        formatted_keywords = ','.join(cleaned_keywords)
        
        if not formatted_keywords:
            return ""
        
        # Returns the markdown for the skillicons badge set
        return f"![My Skills](https://skillicons.dev/icons?i={formatted_keywords})"
    def generate_markdown(self):
        # Get data for easy access
        title = self.data.get('title', 'My Awesome Project')
        description = self.data.get('description', 'A brief description of the project.')
        installation = self.data.get('installation', 'No installation instructions provided.')
        author = self.data.get('author', 'Unknown')
        license_badge = self._generate_license_badge()
        tech_stack = self._generate_tech_stack_badge()
        contact = self.data.get("contact")

        # Title Section
        self.content += f"# {title}\n\n"

        # Add the license badge below the title
        self.content += f"{license_badge}\n\n"

        # Description Section
        self.content += "## Description\n\n"
        self.content += f"{description}\n"

        # Tech Stack Section 
        self.content += "---\n\n"
        self.content += "## Tech Stack\n\n"
        self.content += f"{tech_stack}\n"

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
        self.content += f"**Contact:** {contact}\n\n"

        
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
            
        