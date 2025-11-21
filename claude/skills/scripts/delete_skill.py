#!/usr/bin/env python3
"""
Delete a Claude skill by ID or display title.

This script deletes a skill from your Anthropic Skills account.
You can specify the skill by either its ID or display title.

Requirements:
- ANTHROPIC_API_KEY environment variable must be set
"""

import anthropic
import os
import sys

def show_help():
    """Display help information"""
    help_text = """
Claude Skills Deleter

DESCRIPTION:
    Deletes a Claude skill from your Anthropic account.
    You can specify the skill by either its ID or display title.
    
    ⚠️  WARNING: This action is irreversible!

USAGE:
    python delete_skill.py <skill-id-or-title>
    python delete_skill.py --help

ARGUMENTS:
    skill-id-or-title    Either the skill ID or display title to delete

OPTIONS:
    --help, -h          Show this help message

EXAMPLES:
    python delete_skill.py skill_abc123xyz789
    python delete_skill.py "Java Unit Testing"
    python delete_skill.py java-unit-testing

REQUIREMENTS:
    - ANTHROPIC_API_KEY environment variable must be set

ENVIRONMENT:
    ANTHROPIC_API_KEY    Your Anthropic API key (required)

NOTES:
    - If you provide a folder name (e.g., "java-unit-testing"), it will be 
      converted to title case ("Java Unit Testing") for matching
    - Skill deletion is permanent and cannot be undone
    - The script will ask for confirmation before deleting
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

def find_skill_by_id_or_title(client, identifier):
    """Find skill by ID or display title"""
    try:
        skills = client.beta.skills.list(betas=["skills-2025-10-02"])
        
        # First try exact ID match
        for skill in skills.data:
            if skill.id == identifier:
                return skill, "id"
        
        # Then try exact title match
        for skill in skills.data:
            if skill.display_title == identifier:
                return skill, "title"
        
        # Finally try folder-name-to-title conversion
        title_from_folder = identifier.replace("-", " ").title()
        for skill in skills.data:
            if skill.display_title == title_from_folder:
                return skill, "converted_title"
                
        return None, None
    except Exception as e:
        raise e

def confirm_deletion(skill):
    """Ask user for confirmation before deletion"""
    print(f"\n⚠️  You are about to delete the following skill:")
    print(f"   🆔 ID: {skill.id}")
    print(f"   📝 Title: {skill.display_title}")
    print(f"   🔄 Version: {skill.latest_version}")
    print(f"\n❗ This action is IRREVERSIBLE and cannot be undone!")
    
    while True:
        response = input("\nAre you sure you want to delete this skill? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'")

def main():
    # Handle help flag
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    # Validate arguments
    if len(sys.argv) != 2:
        print("❌ Error: Invalid number of arguments")
        print("Usage: python delete_skill.py <skill-id-or-title>")
        print("       python delete_skill.py --help")
        sys.exit(1)

    # Validate environment
    api_key = validate_environment()
    
    identifier = sys.argv[1]

    # Initialize Anthropic client
    try:
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        print(f"❌ Error: Failed to initialize Anthropic client")
        print(f"💡 Please check your ANTHROPIC_API_KEY is valid")
        print(f"📝 Details: {e}")
        sys.exit(1)

    try:
        print(f"🔍 Looking for skill: {identifier}")
        
        # Find the skill
        skill, match_type = find_skill_by_id_or_title(client, identifier)
        
        if not skill:
            print(f"❌ Error: No skill found with ID or title: {identifier}")
            print("💡 Use list_skills.py to see all available skills")
            sys.exit(1)
        
        # Show what was found
        if match_type == "id":
            print(f"✅ Found skill by ID")
        elif match_type == "title":
            print(f"✅ Found skill by title")
        elif match_type == "converted_title":
            print(f"✅ Found skill by converted title (from folder name)")
        
        # Confirm deletion
        if not confirm_deletion(skill):
            print("❌ Deletion cancelled by user")
            sys.exit(0)
        
        # Delete the skill (need to delete all versions first)
        print(f"\n🗑️  Deleting skill...")
        
        # First, get all versions of this skill
        try:
            print("📋 Fetching skill versions...")
            versions = client.beta.skills.versions.list(skill_id=skill.id, betas=["skills-2025-10-02"])
            
            if versions.data:
                print(f"🔄 Found {len(versions.data)} version(s) to delete...")
                
                # Delete each version
                for version in versions.data:
                    print(f"   Deleting version {version.version}...")
                    client.beta.skills.versions.delete(
                        skill_id=skill.id, 
                        version=version.version, 
                        betas=["skills-2025-10-02"]
                    )
                    print(f"   ✅ Deleted version {version.version}")
                
                print("✅ All versions deleted successfully")
            else:
                print("📭 No versions found to delete")
        
        except Exception as version_error:
            print(f"❌ Error deleting skill versions: {version_error}")
            print("💡 Some versions may need to be deleted manually")
            # Continue trying to delete the skill itself
        
        # Now delete the skill itself
        print("🗑️  Deleting skill...")
        client.beta.skills.delete(skill_id=skill.id, betas=["skills-2025-10-02"])
        
        print(f"✅ Successfully deleted skill!")
        print(f"🆔 Deleted ID: {skill.id}")
        print(f"📝 Deleted Title: {skill.display_title}")

    except anthropic.AuthenticationError:
        print(f"❌ Error: Invalid API key")
        print(f"💡 Please check your ANTHROPIC_API_KEY is correct")
        sys.exit(1)
    except anthropic.PermissionDeniedError:
        print(f"❌ Error: Permission denied")
        print(f"💡 Please check your API key has skills permissions")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error deleting skill: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()