#!/usr/bin/env python3
"""
Delete a Claude skill by ID or display title.
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

try:
    from skill_utils import get_anthropic_client, handle_anthropic_errors, find_skill_by_id_or_title, BETA_VERSION
except ImportError as e:
    print(f"❌ Error: Cannot import skill_utils module: {e}")
    sys.exit(1)

def show_help():
    """Display help information"""
    print("""
Claude Skills Deleter

USAGE:
    python delete_skill.py <skill-id-or-title>
    python delete_skill.py --help

EXAMPLES:
    python delete_skill.py skill_abc123xyz789
    python delete_skill.py "Java Unit Testing"
    python delete_skill.py "My Custom Skill"
    """)

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
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help", "help"]:
        show_help()
        sys.exit(0)
    
    if len(sys.argv) != 2:
        print("❌ Error: Usage: python delete_skill.py <skill-id-or-title>")
        sys.exit(1)

    identifier = sys.argv[1]
    client = get_anthropic_client()

    print(f"🔍 Looking for skill: {identifier}")
    
    skill, match_type = find_skill_by_id_or_title(client, identifier)
    
    if not skill:
        print(f"❌ Error: No skill found with ID or title: {identifier}")
        print("💡 Use list_skills.py to see all available skills")
        sys.exit(1)
    
    if match_type == "id":
        print(f"✅ Found skill by ID")
    elif match_type == "title":
        print(f"✅ Found skill by title")
    elif match_type == "converted_title":
        print(f"✅ Found skill by converted title (from folder name)")
    
    if not confirm_deletion(skill):
        print("❌ Deletion cancelled by user")
        sys.exit(0)
    
    print(f"\n🗑️  Deleting skill...")
    
    def delete_versions():
        versions = client.beta.skills.versions.list(skill_id=skill.id, betas=[BETA_VERSION])
        
        if versions.data:
            print(f"🔄 Found {len(versions.data)} version(s) to delete...")
            
            for version in versions.data:
                print(f"   Deleting version {version.version}...")
                client.beta.skills.versions.delete(
                    skill_id=skill.id, 
                    version=version.version, 
                    betas=[BETA_VERSION]
                )
                print(f"   ✅ Deleted version {version.version}")
            
            print("✅ All versions deleted successfully")

    try:
        handle_anthropic_errors(delete_versions)
    except Exception as version_error:
        print(f"❌ Error deleting skill versions: {version_error}")
        print("💡 Some versions may need to be deleted manually")
    
    def delete_skill():
        return client.beta.skills.delete(skill_id=skill.id, betas=[BETA_VERSION])
    
    handle_anthropic_errors(delete_skill)
    
    print(f"✅ Successfully deleted skill!")
    print(f"🆔 Deleted ID: {skill.id}")
    print(f"📝 Deleted Title: {skill.display_title}")

if __name__ == "__main__":
    main()