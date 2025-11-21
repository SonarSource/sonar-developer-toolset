#!/usr/bin/env python3
"""
Create a new Claude skill from a local SKILL.md file.
"""

from anthropic.lib import files_from_dir
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from skill_utils import find_skill_path, get_skill_display_title, get_anthropic_client, handle_anthropic_errors, BETA_VERSION
except ImportError as e:
    print(f"❌ Error: Cannot import skill_utils module: {e}")
    sys.exit(1)

def show_help():
    """Display help information"""
    print("""
Claude Skills Creator

USAGE:
    python create_skill.py <path-to-skill-folder>
    python create_skill.py --help

EXAMPLES:
    python create_skill.py ./skills/java-unit-testing
    python create_skill.py /absolute/path/to/skill
    python create_skill.py ../relative/path/to/skill
    """)

def main():
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    if len(sys.argv) != 2:
        print("❌ Error: Usage: python create_skill.py <path-to-skill-folder>")
        sys.exit(1)

    skill_path = sys.argv[1]
    skill_md_path = find_skill_path(skill_path)
    
    if not skill_md_path:
        print(f"❌ Error: Skill not found at '{skill_path}'")
        print(f"💡 Create the skill folder and SKILL.md file first")
        sys.exit(1)

    client = get_anthropic_client()
    display_title = get_skill_display_title(skill_path)

    def create_skill():
        skill_dir = os.path.dirname(skill_md_path)
        return client.beta.skills.create(
            display_title=display_title,
            files=files_from_dir(skill_dir),
            betas=[BETA_VERSION]
        )

    skill = handle_anthropic_errors(create_skill)
    
    print(f"✅ Successfully created skill!")
    print(f"🆔 Skill ID: {skill.id}")
    print(f"📝 Display Title: {display_title}")
    print(f"📁 Source Path: {skill_path}")
    print(f"🔄 Version: {skill.latest_version}")

if __name__ == "__main__":
    main()