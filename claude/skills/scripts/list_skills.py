#!/usr/bin/env python3
"""
List all Claude skills in your account.
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from skill_utils import (
        get_anthropic_client, handle_anthropic_errors, list_skills_in_directory, 
        extract_skill_description, extract_skill_name, format_date, BETA_VERSION
    )
except ImportError as e:
    print(f"❌ Error: Cannot import skill_utils module: {e}")
    sys.exit(1)

def show_help():
    """Display help information"""
    print("""
Claude Skills Lister

USAGE:
    python list_skills.py
    python list_skills.py --help

Shows deployed skills with details including ID, display title, version, creation and update dates.
    """)

def format_version(version):
    """Format version number for better display"""
    version_str = str(version)
    return version_str[:8] + ".." if len(version_str) > 10 else version_str

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    if len(sys.argv) > 1:
        print("❌ Error: This script takes no arguments")
        sys.exit(1)

    client = get_anthropic_client()

    print("🔍 Fetching skills from your account...")
    
    def list_remote_skills():
        return client.beta.skills.list(betas=[BETA_VERSION])
    
    skills = handle_anthropic_errors(list_remote_skills)
    
    if not skills.data:
        print("📭 No skills found in your account")
        print("💡 Use create_skill.py to create your first skill")
        return

    print(f"\n✅ Found {len(skills.data)} skill(s):\n")
    
    print(f"{'Display Title':<25} {'Version':<12} {'Created':<18} {'Updated':<18}")
    print(f"{'Skill ID':<50}")
    print("-" * 74)
    
    for skill in skills.data:
        title = skill.display_title[:23] + ".." if len(skill.display_title) > 23 else skill.display_title
        version = format_version(skill.latest_version)
        created = format_date(skill.created_at)
        updated = format_date(skill.updated_at)
        
        print(f"{title:<25} {version:<12} {created:<18} {updated:<18}")
        print(f"  ID: {skill.id}")
        print()

    print(f"\n📊 Total: {len(skills.data)} skills deployed to Anthropic")

if __name__ == "__main__":
    main()