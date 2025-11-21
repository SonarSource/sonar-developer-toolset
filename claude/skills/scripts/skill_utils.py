#!/usr/bin/env python3
"""
Utility functions for managing Claude skills.
"""

import anthropic
import os
import sys
from datetime import datetime
from typing import Tuple, Optional, List, Dict, Any

BETA_VERSION = "skills-2025-10-02"
SKILL_FILENAME = "SKILL.md"



def find_skill_path(skill_path: str) -> Optional[str]:
    """Find the path to a skill's SKILL.md file"""
    skill_folder = os.path.abspath(os.path.expanduser(skill_path))
    skill_md_path = os.path.join(skill_folder, SKILL_FILENAME)
    
    if os.path.exists(skill_md_path):
        return skill_md_path
    
    return None

def list_skills_in_directory(directory_path: str) -> List[Dict]:
    """List all skills in a given directory"""
    skills = []
    if os.path.exists(directory_path):
        for item in os.listdir(directory_path):
            skill_dir = os.path.join(directory_path, item)
            skill_file = os.path.join(skill_dir, SKILL_FILENAME)
            if os.path.isdir(skill_dir) and os.path.exists(skill_file):
                skills.append({
                    'name': item,
                    'path': skill_file
                })
    return skills

def get_skill_display_title(skill_path: str) -> str:
    """Extract skill folder name to use as display title"""
    return os.path.basename(skill_path.rstrip('/\\'))

def extract_skill_name(skill_md_path: str) -> str:
    """Extract name from SKILL.md file YAML frontmatter"""
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                for line in parts[1].split('\n'):
                    line = line.strip()
                    if line.startswith('name:'):
                        return line.replace('name:', '').strip()
        
        return "Unnamed Skill"
        
    except Exception:
        return "Unnamed Skill"

def extract_skill_description(skill_md_path: str) -> str:
    """Extract description from SKILL.md file YAML frontmatter"""
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                for line in parts[1].split('\n'):
                    line = line.strip()
                    if line.startswith('description:'):
                        desc = line.replace('description:', '').strip()
                        return desc[:117] + "..." if len(desc) > 120 else desc
        
        return "No description available"
        
    except Exception:
        return "No description available"

def get_anthropic_client() -> anthropic.Anthropic:
    """Initialize and return Anthropic client with proper error handling"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY environment variable is not set")
        print("💡 Please set your API key: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)
    
    try:
        return anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        print(f"❌ Error: Failed to initialize Anthropic client")
        print(f"💡 Please check your ANTHROPIC_API_KEY is valid")
        print(f"📝 Details: {e}")
        sys.exit(1)

def handle_anthropic_errors(func, *args, **kwargs):
    """Common error handling for Anthropic API calls"""
    try:
        return func(*args, **kwargs)
    except anthropic.AuthenticationError:
        print("❌ Error: Invalid API key")
        print("💡 Please check your ANTHROPIC_API_KEY is correct")
        sys.exit(1)
    except anthropic.PermissionDeniedError:
        print("❌ Error: Permission denied")
        print("💡 Please check your API key has skills permissions")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def format_date(iso_string: Any) -> str:
    """Format ISO date string to readable format"""
    if not iso_string:
        return "N/A"
    try:
        dt = datetime.fromisoformat(str(iso_string).replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except (ValueError, TypeError):
        return str(iso_string)[:16]

def find_skill_by_id_or_title(client: anthropic.Anthropic, identifier: str) -> Tuple[Optional[Any], Optional[str]]:
    """Find skill by ID or display title"""
    skills = client.beta.skills.list(betas=[BETA_VERSION])
    
    for skill in skills.data:
        if skill.id == identifier:
            return skill, "id"
    
    for skill in skills.data:
        if skill.display_title == identifier:
            return skill, "title"
    
    title_from_folder = identifier.replace("-", " ").title()
    for skill in skills.data:
        if skill.display_title == title_from_folder:
            return skill, "converted_title"
            
    return None, None

