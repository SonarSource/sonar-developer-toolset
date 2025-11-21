#!/usr/bin/env python3
"""
List all Claude skills in your account.

This script lists all skills in your Anthropic Skills account with details
like display title, ID, version, creation date, and last updated date.

Requirements:
- ANTHROPIC_API_KEY environment variable must be set
"""

import anthropic
import os
import sys
from datetime import datetime

# Add script directory to path to import skill_utils
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from skill_utils import list_all_skills, extract_skill_description, extract_skill_name
except ImportError as e:
    print(f"❌ Error: Cannot import skill_utils module: {e}")
    print(f"💡 Ensure skill_utils.py is in the same directory as this script")
    sys.exit(1)

def show_help():
    """Display help information"""
    help_text = """
Claude Skills Lister

DESCRIPTION:
    Lists all Claude skills in your Anthropic account.
    Shows skill details including ID, display title, version, creation date, and last updated date.
    Also shows available local skills in ~/.claude/skills/ and repo skills in <script-dir>/../skills/.

USAGE:
    python list_skills.py
    python list_skills.py --help

OPTIONS:
    --help, -h          Show this help message

EXAMPLES:
    python list_skills.py

REQUIREMENTS:
    - ANTHROPIC_API_KEY environment variable must be set

ENVIRONMENT:
    ANTHROPIC_API_KEY    Your Anthropic API key (required)

OUTPUT FORMAT:
    Skills are displayed in a table format with:
    - Skill ID
    - Display Title
    - Latest Version
    - Created Date
    - Updated Date
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

def format_date(iso_string):
    """Format ISO date string to readable format"""
    if not iso_string:
        return "N/A"
    try:
        # Handle different ISO formats
        if 'T' in iso_string:
            # Standard ISO format with T separator
            dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        else:
            # Handle timestamp-like strings by converting to readable date
            if iso_string.isdigit() and len(iso_string) > 10:
                # Looks like a timestamp, try to parse as seconds or milliseconds
                timestamp = int(iso_string)
                if timestamp > 1e12:  # Likely milliseconds
                    timestamp = timestamp / 1000
                dt = datetime.fromtimestamp(timestamp)
            else:
                # Try parsing as ISO date string
                dt = datetime.fromisoformat(str(iso_string).replace('Z', '+00:00'))
        
        return dt.strftime('%Y-%m-%d %H:%M')
    except (ValueError, TypeError, OverflowError):
        # Fallback for unparseable dates
        return str(iso_string)[:16] if len(str(iso_string)) > 16 else str(iso_string)

def format_version(version):
    """Format version number for better display"""
    version_str = str(version)
    if len(version_str) > 10:
        # Handle very long version numbers by truncating
        return version_str[:8] + ".."
    return version_str

def main():
    # Handle help flag
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    # Validate arguments
    if len(sys.argv) > 1:
        print("❌ Error: This script takes no arguments")
        print("Usage: python list_skills.py")
        print("       python list_skills.py --help")
        sys.exit(1)

    # Validate environment
    api_key = validate_environment()

    # Initialize Anthropic client
    try:
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        print(f"❌ Error: Failed to initialize Anthropic client")
        print(f"💡 Please check your ANTHROPIC_API_KEY is valid")
        print(f"📝 Details: {e}")
        sys.exit(1)

    try:
        print("🔍 Fetching skills from your account...")
        
        # List all skills
        skills = client.beta.skills.list(betas=["skills-2025-10-02"])
        
        if not skills.data:
            print("📭 No skills found in your account")
            print("💡 Use create_skill.py to create your first skill")
            return

        print(f"\n✅ Found {len(skills.data)} skill(s):\n")
        
        # Header
        print(f"{'Display Title':<25} {'Version':<12} {'Created':<18} {'Updated':<18}")
        print(f"{'Skill ID':<50}")
        print("-" * 74)  # 25 + 12 + 18 + 18 + 1 = 74
        
        # List skills
        for skill in skills.data:
            title = skill.display_title[:23] + ".." if len(skill.display_title) > 23 else skill.display_title
            version = format_version(skill.latest_version)
            created = format_date(skill.created_at)
            updated = format_date(skill.updated_at)
            
            # Print the main row with title, version, and dates
            print(f"{title:<25} {version:<12} {created:<18} {updated:<18}")
            # Print the full skill ID on the next line with indentation
            print(f"  ID: {skill.id}")
            print()  # Empty line for better separation

        print(f"\n📊 Total: {len(skills.data)} skills deployed to Anthropic")

        # Show available skills that could be deployed
        print(f"\n" + "="*90)
        print(f"📁 AVAILABLE SKILLS TO DEPLOY:")
        print(f"="*90)
        
        available_skills = list_all_skills()
        repo_skills = available_skills['repo']
        
        if not repo_skills:
            print("📭 No skills found in lib directory")
            print("💡 Create skills in lib/<skill-name>/SKILL.md")
        else:
            print(f"\n✅ Found {len(repo_skills)} available skill(s):\n")
            
            # Show each skill with name, path, and description
            for skill in repo_skills:
                folder_name = skill['name']
                skill_name = extract_skill_name(skill['path'])
                description = extract_skill_description(skill['path'])
                
                # Format as: Name, Path, Description (multiline)
                print(f"📚 Name: {skill_name}")
                print(f"   Path: lib/{folder_name}")
                print(f"   Description: {description}")
                print(f"   Deploy: python scripts/create_skill.py lib/{folder_name}")
                print()

    except anthropic.AuthenticationError:
        print(f"❌ Error: Invalid API key")
        print(f"💡 Please check your ANTHROPIC_API_KEY is correct")
        sys.exit(1)
    except anthropic.PermissionDeniedError:
        print(f"❌ Error: Permission denied")
        print(f"💡 Please check your API key has skills permissions")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error listing skills: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
