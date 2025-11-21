#!/usr/bin/env python3
"""
Update an existing Claude skill or create it if it doesn't exist.
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
Claude Skills Updater

USAGE:
    python update_skill.py <path-to-skill-folder>
    python update_skill.py --help

EXAMPLES:
    python update_skill.py ./skills/java-unit-testing
    python update_skill.py /absolute/path/to/skill
    python update_skill.py ../relative/path/to/skill
    """)

def main():
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    if len(sys.argv) != 2:
        print("❌ Error: Usage: python update_skill.py <path-to-skill-folder>")
        sys.exit(1)

    skill_path = sys.argv[1]
    skill_md_path = find_skill_path(skill_path)
    
    if not skill_md_path:
        print(f"❌ Error: Skill not found at '{skill_path}'")
        print(f"💡 Create the skill folder and SKILL.md file first")
        sys.exit(1)

    client = get_anthropic_client()
    display_title = get_skill_display_title(skill_path)

    print(f"🔍 Looking for existing skill '{display_title}'...")
    print(f"📁 Source: {skill_md_path}")
    
    def list_skills():
        return client.beta.skills.list(betas=[BETA_VERSION])
    
    skills = handle_anthropic_errors(list_skills)
    
    target_skill = None
    for skill in skills.data:
        if skill.display_title == display_title:
            target_skill = skill
            break
    
    skill_dir = os.path.dirname(skill_md_path)
    
    if target_skill:
        print(f"📝 Updating existing skill (ID: {target_skill.id})...")
        
        def update_skill():
            return client.beta.skills.versions.create(
                skill_id=target_skill.id,
                files=files_from_dir(skill_dir),
                betas=[BETA_VERSION]
            )
        
        updated_skill = handle_anthropic_errors(update_skill)
        
        print(f"✅ Successfully updated existing skill!")
        print(f"🆔 Skill ID: {target_skill.id}")
        print(f"📝 Display Title: {display_title}")
        print(f"📁 Source Path: {skill_path}")
        print(f"🔄 New Version: {updated_skill.version}")
    else:
        print(f"🚀 Skill not found, creating new skill...")
        
        def create_skill():
            return client.beta.skills.create(
                display_title=display_title,
                files=files_from_dir(skill_dir),
                betas=[BETA_VERSION]
            )
        
        new_skill = handle_anthropic_errors(create_skill)
        
        print(f"✅ Successfully created new skill!")
        print(f"🆔 Skill ID: {new_skill.id}")
        print(f"📝 Display Title: {display_title}")
        print(f"📁 Source Path: {skill_path}")
        print(f"🔄 Version: {new_skill.latest_version}")

if __name__ == "__main__":
    main()