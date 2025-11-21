#!/usr/bin/env python3
"""
Create a new Claude skill from a local SKILL.md file.

This script creates a new skill in the Anthropic Skills API using a local markdown file.
The skill folder should contain a SKILL.md file with the skill definition.

Requirements:
- ANTHROPIC_API_KEY environment variable must be set
- Skill folder must exist and contain SKILL.md file
"""

import anthropic
from anthropic.lib import files_from_dir
import os
import sys

# Add script directory to path to import skill_utils
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from skill_utils import parse_skill_reference, find_skill_path, get_skill_display_title
except ImportError as e:
    print(f"❌ Error: Cannot import skill_utils module: {e}")
    print(f"💡 Ensure skill_utils.py is in the same directory as this script")
    sys.exit(1)

def show_help():
    """Display help information"""
    help_text = """
Claude Skills Creator

DESCRIPTION:
    Creates a new Claude skill from a SKILL.md file.
    Uses direct paths to skill folders for maximum clarity and flexibility.
    The display title is automatically generated from the folder name.

USAGE:
    python create_skill.py <path-to-skill-folder>
    python create_skill.py --help

ARGUMENTS:
    path-to-skill-folder    Path to folder containing SKILL.md file

EXAMPLES:
    python create_skill.py lib/java-unit-testing       # Repo skill
    python create_skill.py ~/.claude/skills/my-skill   # Local skill
    python create_skill.py ./custom-skills/tool        # Relative path
    python create_skill.py ../external/team-helper     # Relative path
    python create_skill.py /absolute/path/to/skill     # Absolute path

REQUIREMENTS:
    - ANTHROPIC_API_KEY environment variable must be set
    - Specified folder must contain SKILL.md file

ENVIRONMENT:
    ANTHROPIC_API_KEY    Your Anthropic API key (required)
    """
    print(help_text)

def validate_environment():
    """Validate required environment variables"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable is not set")
        print("💡 Please set your API key: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    return api_key

def main():
    # Handle help flag
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    # Validate arguments
    if len(sys.argv) != 2:
        print("❌ Error: Invalid number of arguments")
        print("Usage: python create_skill.py <skill-reference>")
        print("       python create_skill.py --help")
        sys.exit(1)

    # Validate environment
    api_key = validate_environment()
    
    skill_reference = sys.argv[1]
    
    # Parse skill reference (now always a path)
    source, skill_path = parse_skill_reference(skill_reference)
    
    # Find the skill file
    skill_md_path, actual_source = find_skill_path(skill_path, source)
    
    if not skill_md_path:
        print(f"❌ Error: Skill not found at '{skill_path}'")
        abs_path = os.path.abspath(os.path.expanduser(skill_path))
        print(f"💡 Checked: {abs_path}/SKILL.md")
        print(f"💡 Create the skill folder and SKILL.md file first")
        sys.exit(1)

    # Initialize Anthropic client
    try:
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        print(f"❌ Error: Failed to initialize Anthropic client")
        print(f"💡 Please check your ANTHROPIC_API_KEY is valid")
        print(f"📝 Details: {e}")
        sys.exit(1)

    # Extract display title from folder name
    display_title = get_skill_display_title(skill_path)

    try:
        print(f"🚀 Creating skill '{display_title}'...")
        print(f"📁 Source folder: {os.path.dirname(skill_md_path)}")
        
        # Get the skill directory path
        skill_dir = os.path.dirname(skill_md_path)
        
        skill = client.beta.skills.create(
            display_title=display_title,
            files=files_from_dir(skill_dir),
            betas=["skills-2025-10-02"]
        )

        print(f"✅ Successfully created skill!")
        print(f"🆔 Skill ID: {skill.id}")
        print(f"📝 Display Title: {display_title}")
        print(f"📁 Source Path: {skill_path}")
        print(f"🔄 Version: {skill.latest_version}")

    except anthropic.AuthenticationError:
        print(f"❌ Error: Invalid API key")
        print(f"💡 Please check your ANTHROPIC_API_KEY is correct")
        sys.exit(1)
    except anthropic.PermissionDeniedError:
        print(f"❌ Error: Permission denied")
        print(f"💡 Please check your API key has skills permissions")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
