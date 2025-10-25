"""
Streamlit Modern README Generator

This file includes a helper for automatic dependency installation.
If the user runs this file without Streamlit installed, the script
will detect the missing import and automatically install packages
listed in `requirements.txt` inside the virtual environment (if any)
or globally.

Run:
    python streamlit_readme_generator.py
    # It will auto-install requirements if missing.

Or manually:
    pip install -r requirements.txt
    streamlit run streamlit_readme_generator.py
"""

from textwrap import dedent
import datetime
import os
import subprocess
import sys
import uuid # For unique keys in Streamlit

# --- Dependency auto-installer ---

def ensure_requirements():
    """Ensure all required packages from requirements.txt are installed."""
    # Create a minimal requirements.txt if it doesn't exist
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if not os.path.exists(req_file):
        with open(req_file, 'w') as f:
            f.write("streamlit\n")

    try:
        import streamlit  # noqa: F401
    except ImportError:
        print("📦 Installing dependencies from requirements.txt...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_file])
        except Exception as e:
             print(f"Error installing dependencies: {e}")
             print("Please ensure you have pip installed or install Streamlit manually.")
             sys.exit(1)

# Call before imports that might fail
ensure_requirements()

import streamlit as st  # noqa: E402

# ---------- Helpers ----------

def get_markdown_sections(data: dict, template_type: str):
    """Generates the main content sections for the README based on data and flags."""
    
    features_md = "\n".join([f"- {f.strip()}" for f in data.get("features", []) if f.strip()])
    
    sections = []
    toc = [] # Only used for Classic template

    # --- Standard Sections (Installation, Features, Contributing are always included) ---
    
    # Installation
    sections.append({
        "title": "Installation",
        "content": f"```bash\n{data['install_command']}\n```",
        "id": "installation"
    })
    toc.append("Installation")
    
    # Features
    sections.append({
        "title": "Features",
        "content": features_md or "- No features listed yet.",
        "id": "features"
    })
    toc.append("Features")

    # --- Conditional Sections (Usage) ---
    if data.get('include_usage', True):
        usage_content = f"```bash\n{data['usage_example']}\n```" if data.get('usage_example', '').strip() else "*No usage example provided yet.*"
        sections.append({
            "title": "Usage",
            "content": usage_content,
            "id": "usage"
        })
        toc.append("Usage")

    # --- Custom Sections ---
    for section in data.get('custom_sections', []):
        if section.get('title', '').strip():
            # Use a slugified version of the title for the ID
            section_id = section['title'].strip().lower().replace(' ', '-')
            sections.append({
                "title": section['title'].strip(),
                "content": section['content'].strip(),
                "id": section_id
            })
            toc.append(section['title'].strip())

    # --- Standard Section (Contributing is always included) ---
    sections.append({
        "title": "Contributing",
        "content": data['contributing'] or 'Contributions welcome — open an issue or a PR.',
        "id": "contributing"
    })
    toc.append("Contributing")

    # --- Conditional Sections (Author) ---
    if data.get('include_author', True):
        author_md = f"**{data['author_name']}**\n"
        if data.get('github_username'):
            author_md += f"- GitHub: [{data['github_username']}](https://github.com/{data['github_username']})\n"
        if data.get('website'):
            author_md += f"- Website: [{data['website']}]({data['website']})\n"
        
        sections.append({
            "title": "Author",
            "content": author_md.strip(),
            "id": "author"
        })
        toc.append("Author")

    return sections, toc


def build_readme_template(data: dict, template_choice: str) -> str:
    """Builds the complete README markdown based on the chosen template and data."""
    sections, toc = get_markdown_sections(data, template_choice)
    badges_md = " ".join([b.strip() for b in data.get("badges", []) if b.strip()])
    
    # --- Header ---
    md_parts = [
        f"# {data['project_name']} {data.get('emoji', '')}",
        data['description'],
        badges_md
    ]
    
    if template_choice == "Classic":
        # Dynamic Table of Contents for Classic Template
        toc_md = "\n".join([f"- [{title}](#{title.lower().replace(' ', '-')})" for title in toc])
        md_parts.append("## Table of contents\n" + toc_md)

    # --- Sections ---
    for section in sections:
        md_parts.append(f"## {section['title']}\n\n{section['content']}\n")

    # --- Footer ---
    footer = f"_Generated with Streamlit README Generator on {datetime.date.today().isoformat()}_"
    if template_choice == "Classic":
        md_parts.append("---\n" + footer)
    else:
        md_parts.append(footer)

    return dedent("\n\n".join(filter(None, md_parts))).strip()


def get_default_data() -> dict:
    """Returns the default initial data for the editor."""
    return {
        "project_name": "My Streamlit Project",
        "emoji": "🚀",
        "description": "A short, one-line description of the project.",
        "install_command": "pip install -r requirements.txt",
        "usage_example": "streamlit run app.py",
        "features": ["Easy to use", "Fast deployment", "Highly configurable"],
        "contributing": "Open issues and PRs are welcome.",
        "author_name": "Your Name",
        "github_username": "",
        "website": "",
        "badges": ["[![PyPI version](https://badge.fury.io/py/your-package.svg)](https://badge.fury.io/py/your-package)"],
        "include_usage": True,
        "include_author": True,
        "custom_sections": [],
    }


def main():
    st.set_page_config(page_title="Dynamic README Generator", layout="wide")
    st.title("Dynamic README Generator — Live Preview")
    st.caption("Build a clean README.md using a visual editor. Select which sections to include.")

    # Initialize data if not present in session state
    if "data" not in st.session_state:
        st.session_state.data = get_default_data()
    
    # Initialize unique keys for custom sections
    if "custom_section_keys" not in st.session_state:
        st.session_state.custom_section_keys = {}

    data = st.session_state.data
    
    # Split the layout into two columns
    cols = st.columns((1, 1))

    with cols[0]:
        st.header("Editor")

        # --- Core Project Info ---
        with st.container(border=True):
            st.markdown("### Core Info")
            data['project_name'] = st.text_input("Project name", value=data.get('project_name', ''))
            data['emoji'] = st.text_input("Emoji (optional)", value=data.get('emoji', ''))
            data['description'] = st.text_area("Short description", value=data.get('description', ''), height=80)
            
            template_choice = st.selectbox("Template Style", ["Minimal", "Classic"], index=0)

            badges_text = st.text_area("Badges (one per line, enter full Markdown)", 
                                        value="\n".join(data.get('badges', [])), height=80)
            data['badges'] = [line for line in badges_text.splitlines() if line.strip()]

        # --- Standard Content ---
        with st.container(border=True):
            st.markdown("### Standard Content")
            data['install_command'] = st.text_input("Installation Command (`Installation` section)", 
                                                    value=data.get('install_command', ''))
            
            features_text = st.text_area("Features (one per line, for `Features` section)", 
                                         value="\n".join(data.get('features', [])), height=120)
            data['features'] = [line for line in features_text.splitlines() if line.strip()]

            data['contributing'] = st.text_area("Contributing Notes (`Contributing` section)", 
                                                value=data.get('contributing', ''), height=60)

        # --- Section Visibility and Conditional Content ---
        with st.container(border=True):
            st.markdown("### Section Control")
            
            # Usage Control
            data['include_usage'] = st.checkbox("Include Usage Section", value=data.get('include_usage', True))
            if data['include_usage']:
                data['usage_example'] = st.text_area("Usage Example / Snippet", 
                                                    value=data.get('usage_example', ''), height=80)
            
            st.markdown("---")

            # Author Control
            data['include_author'] = st.checkbox("Include Author Section", value=data.get('include_author', True))
            if data['include_author']:
                data['author_name'] = st.text_input("Author Name", value=data.get('author_name', ''))
                data['github_username'] = st.text_input("GitHub Username (optional)", 
                                                        value=data.get('github_username', ''))
                data['website'] = st.text_input("Website (optional)", value=data.get('website', ''))


        # --- Custom Sections (New Feature) ---
        st.subheader("Custom Sections")
        if 'custom_sections' not in data:
            data['custom_sections'] = []
            
        # Use an expander for custom sections to keep the main UI clean
        with st.expander(f"Manage Custom Sections ({len(data['custom_sections'])})"):
            
            sections_to_remove = []
            for i, section in enumerate(data['custom_sections']):
                # Ensure each custom section has a unique key for Streamlit to track it
                if i not in st.session_state.custom_section_keys:
                    st.session_state.custom_section_keys[i] = str(uuid.uuid4())
                
                key_prefix = st.session_state.custom_section_keys[i]

                st.markdown(f"**Section {i + 1}**")
                cols_c = st.columns([4, 1])
                section['title'] = cols_c[0].text_input(f"Title (e.g., License, Roadmap)", 
                                                        value=section['title'], key=f"title_{key_prefix}")
                
                section['content'] = st.text_area(f"Content (Full Markdown)", 
                                                value=section['content'], height=100, key=f"content_{key_prefix}")
                
                if cols_c[1].button("Remove", key=f"remove_{key_prefix}"):
                    sections_to_remove.append(i)
                st.markdown("---")

            # Perform removal outside of the loop
            for index in sorted(sections_to_remove, reverse=True):
                st.session_state.data['custom_sections'].pop(index)
                del st.session_state.custom_section_keys[index]
            
            if sections_to_remove:
                st.experimental_rerun()
            
            if st.button("Add New Section"):
                st.session_state.data['custom_sections'].append({'title': '', 'content': ''})
                # Need to regenerate keys and rerun if adding a section
                keys = list(st.session_state.custom_section_keys.keys())
                max_key = max(keys) if keys else -1
                st.session_state.custom_section_keys[max_key + 1] = str(uuid.uuid4())
                st.experimental_rerun()


        # --- Action Buttons ---
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Reset to defaults"):
                st.session_state.data = get_default_data()
                st.session_state.custom_section_keys = {}
                st.experimental_rerun()

    # --- Live Preview Column ---
    with cols[1]:
        st.header("Live Preview")
        
        # Build the Markdown content using the updated logic
        md = build_readme_template(data, template_choice)
        
        st.subheader("Rendered README")
        st.markdown(md)
        
        st.subheader("Markdown Source")
        st.code(md, language='markdown')
        
        # Download button for the generated file
        b = md.encode('utf-8')
        st.download_button("Download README.md", data=b, file_name="README.md", mime="text/markdown")

    st.markdown("---")
    st.caption("Tip: Streamlit automatically re-runs whenever you change any input — that’s what makes the preview live.")


if __name__ == '__main__':
    main()
