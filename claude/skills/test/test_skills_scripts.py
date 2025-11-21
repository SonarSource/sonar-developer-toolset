#!/usr/bin/env python3
"""
Test script for Claude Skills management scripts.

This script validates that all four skill management scripts work correctly:
- create_skill.py
- update_skill.py  
- list_skills.py
- delete_skill.py

The test is idempotent - it cleans up after itself.
"""

import subprocess
import sys
import os
import time
import re

def run_command(command, description):
    """Run a command and return success status and output"""
    print(f"\n🧪 Testing: {description}")
    print(f"💻 Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        print(f"📤 Return code: {result.returncode}")
        if result.stdout:
            print(f"📄 Output:\n{result.stdout}")
        if result.stderr:
            print(f"❌ Error:\n{result.stderr}")
            
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False, "", "Command timed out"
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False, "", str(e)

def extract_skill_id(output):
    """Extract skill ID from create/list output"""
    # Look for pattern like "🆔 Skill ID: skill_abc123xyz"
    id_match = re.search(r'Skill ID:\s*(skill_\w+)', output)
    if id_match:
        return id_match.group(1)
    
    # Also look for just "ID: skill_abc123xyz" pattern
    id_match = re.search(r'ID:\s*(skill_\w+)', output)
    if id_match:
        return id_match.group(1)
        
    return None

def main():
    print("🚀 Starting Claude Skills Scripts Test")
    print("=" * 50)
    
    # Check if we're in the right directory
    scripts_dir = os.path.join(os.getcwd(), "claude", "skills", "scripts")
    test_skill_path = os.path.join(os.getcwd(), "claude", "skills", "test", "test-skill")
    
    if not os.path.exists(scripts_dir):
        print("❌ Error: scripts directory not found. Run from repository root.")
        sys.exit(1)
    
    if not os.path.exists(test_skill_path):
        print("❌ Error: test skill not found. Create test skill first.")
        sys.exit(1)
    
    print(f"📁 Scripts directory: {scripts_dir}")
    print(f"📁 Test skill path: {test_skill_path}")
    
    # Change to scripts directory for running commands
    original_dir = os.getcwd()
    os.chdir(scripts_dir)
    
    test_results = []
    created_skill_id = None
    
    try:
        # Test 1: List skills (before creation)
        success, output, error = run_command(
            ["python", "list_skills.py"],
            "List skills before creation"
        )
        test_results.append(("List skills (initial)", success))
        
        # Test 2: Create skill
        success, output, error = run_command(
            ["python", "create_skill.py", test_skill_path],
            "Create test skill"
        )
        test_results.append(("Create skill", success))
        
        if success:
            created_skill_id = extract_skill_id(output)
            print(f"✅ Created skill with ID: {created_skill_id}")
        else:
            print("❌ Failed to create skill - aborting remaining tests")
            return test_results
        
        # Small delay to ensure skill is fully created
        time.sleep(2)
        
        # Test 3: List skills (after creation)
        success, output, error = run_command(
            ["python", "list_skills.py"],
            "List skills after creation"
        )
        test_results.append(("List skills (after create)", success))
        
        if success and "Test Skill for Validation" in output:
            print("✅ Test skill found in skills list")
        else:
            print("⚠️  Test skill not found in skills list")
        
        # Test 4: Update skill (modify the SKILL.md first)
        print("\n📝 Modifying test skill for update test...")
        skill_md_path = os.path.join(test_skill_path, "SKILL.md")
        
        # Read current content
        with open(skill_md_path, 'r') as f:
            content = f.read()
        
        # Modify description
        updated_content = content.replace(
            "description: A test skill used to validate the Claude Skills scripts functionality",
            "description: UPDATED - A test skill used to validate the Claude Skills scripts functionality"
        )
        
        # Write updated content
        with open(skill_md_path, 'w') as f:
            f.write(updated_content)
        
        success, output, error = run_command(
            ["python", "update_skill.py", test_skill_path],
            "Update test skill"
        )
        test_results.append(("Update skill", success))
        
        # Restore original content
        with open(skill_md_path, 'w') as f:
            f.write(content)
        
        # Small delay to ensure update is processed
        time.sleep(2)
        
        # Test 5: List skills (after update)
        success, output, error = run_command(
            ["python", "list_skills.py"],
            "List skills after update"
        )
        test_results.append(("List skills (after update)", success))
        
    finally:
        # Test 6: Delete skill (cleanup)
        if created_skill_id:
            print(f"\n🧹 Cleaning up: Deleting skill {created_skill_id}")
            
            # Use expect to handle the confirmation prompt
            delete_command = f"echo 'yes' | python delete_skill.py {created_skill_id}"
            success, output, error = run_command(
                ["bash", "-c", delete_command],
                "Delete test skill (cleanup)"
            )
            test_results.append(("Delete skill (cleanup)", success))
            
            if success:
                print("✅ Test skill deleted successfully")
            else:
                print("⚠️  Failed to delete test skill - manual cleanup may be needed")
                print(f"   Skill ID: {created_skill_id}")
        
        # Return to original directory
        os.chdir(original_dir)
    
    # Print test summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Claude Skills scripts are working correctly.")
        return True
    else:
        print("💥 Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)