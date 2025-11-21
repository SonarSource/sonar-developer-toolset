#!/usr/bin/env python3
"""
Utility functions for managing Claude skills from multiple sources.

This module provides functions to locate and manage skills from both:
1. Local user skills in ~/.claude/skills/
2. Shared repo skills in <script-location>/../lib/
"""

import os
import sys
from typing import Tuple, Optional, List, Dict

def get_script_directory():
    """Get the directory where the current script is located"""
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def get_repo_skills_directory():
    """Get the shared skills directory in the repo"""
    script_dir = get_script_directory()
    # New structure: scripts are in 'scripts/' and skills are in 'lib/'
    possible_paths = [
        os.path.join(script_dir, "..", "lib"),      # scripts/ -> lib/
        os.path.join(script_dir, "..", "skills"),  # legacy: scripts/ -> skills/
        os.path.join(script_dir, "lib"),           # same level as scripts/
        os.path.join(script_dir, "skills"),        # legacy: same directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    return None

def get_local_skills_directory():
    """Get the user's local skills directory"""
    return os.path.expanduser("~/.claude/skills")

def parse_skill_reference(skill_ref: str) -> Tuple[str, str]:
    """
    Parse skill reference - now pure path only.
    
    Args:
        skill_ref: Path to skill folder (relative or absolute)
        
    Returns:
        Tuple of ('path', skill_path) - always path mode
    """
    return 'path', skill_ref

def find_skill_path(skill_path: str, source: str = 'path') -> Tuple[Optional[str], Optional[str]]:
    """
    Find the path to a skill's SKILL.md file - pure path mode.
    
    Args:
        skill_path: Path to skill folder
        source: Always 'path' (parameter kept for compatibility)
        
    Returns:
        Tuple of (skill_md_path, 'path') or (None, None) if not found
    """
    # Expand and resolve the path
    skill_folder = os.path.abspath(os.path.expanduser(skill_path))
    skill_md_path = os.path.join(skill_folder, "SKILL.md")
    
    if os.path.exists(skill_md_path):
        return skill_md_path, 'path'
    
    return None, None

def list_all_skills() -> Dict[str, List[Dict]]:
    """
    List all available skills from both sources.
    
    Returns:
        Dict with 'local' and 'repo' keys, each containing list of skill info dicts
    """
    skills = {'local': [], 'repo': []}
    
    # Local skills
    local_dir = get_local_skills_directory()
    if os.path.exists(local_dir):
        for item in os.listdir(local_dir):
            skill_dir = os.path.join(local_dir, item)
            skill_file = os.path.join(skill_dir, "SKILL.md")
            if os.path.isdir(skill_dir) and os.path.exists(skill_file):
                skills['local'].append({
                    'name': item,
                    'path': skill_file,
                    'source': 'local'
                })
    
    # Repo skills
    repo_dir = get_repo_skills_directory()
    if repo_dir and os.path.exists(repo_dir):
        for item in os.listdir(repo_dir):
            skill_dir = os.path.join(repo_dir, item)
            skill_file = os.path.join(skill_dir, "SKILL.md")
            if os.path.isdir(skill_dir) and os.path.exists(skill_file):
                skills['repo'].append({
                    'name': item,
                    'path': skill_file,
                    'source': 'repo'
                })
    
    return skills

def get_skill_display_title(skill_path: str) -> str:
    """Extract skill folder name to use as display title"""
    # Extract just the folder name from the path - use it directly for better matching
    skill_name = os.path.basename(skill_path.rstrip('/\\'))
    return skill_name

def extract_skill_name(skill_md_path: str) -> str:
    """Extract name from SKILL.md file YAML front matter"""
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for YAML front matter first
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                yaml_section = parts[1]
                for line in yaml_section.split('\n'):
                    line = line.strip()
                    if line.startswith('name:'):
                        name = line.replace('name:', '').strip()
                        return name
                        
        # Fallback: use folder name
        folder_name = os.path.basename(os.path.dirname(skill_md_path))
        return folder_name
        
    except Exception:
        folder_name = os.path.basename(os.path.dirname(skill_md_path))
        return folder_name

def extract_skill_description(skill_md_path: str) -> str:
    """Extract description from SKILL.md file"""
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for YAML front matter first
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 2:
                yaml_section = parts[1]
                for line in yaml_section.split('\n'):
                    line = line.strip()
                    if line.startswith('description:'):
                        desc = line.replace('description:', '').strip()
                        if len(desc) > 120:
                            desc = desc[:117] + "..."
                        return desc
                        
        lines = content.split('\n')
        description_lines = []
        found_description = False
        in_yaml = False
        
        for line in lines:
            line = line.strip()
            
            # Skip YAML front matter
            if line == '---':
                in_yaml = not in_yaml
                continue
            if in_yaml:
                continue
                
            # Skip headers, @DisplayName, and empty lines
            if (line.startswith('#') or 
                line.startswith('@') or 
                not line):
                continue
                
            # Look for description-like content
            if not found_description:
                if (line.startswith('You are') or 
                    line.startswith('This skill') or
                    line.startswith('An expert') or
                    line.startswith('A comprehensive') or
                    ('expert' in line.lower() and ('specializ' in line.lower() or 
                                                   'focus' in line.lower() or
                                                   'help' in line.lower()))):
                    found_description = True
                    description_lines.append(line)
                continue
            
            # Stop at next major section marker or bullet points
            if (line.startswith('##') or 
                line.startswith('###') or
                line.startswith('-') or 
                line.startswith('*') or
                line.startswith('1.') or
                line.startswith('```')):
                break
                
            # Continue collecting description lines
            if line:
                description_lines.append(line)
        
        # Join and clean up
        description = ' '.join(description_lines).strip()
        
        # Remove common prefixes and clean up
        description = description.replace('@DisplayName', '').strip()
        
        # Truncate if too long
        if len(description) > 120:
            description = description[:117] + "..."
            
        return description if description else "Expert skill for specialized assistance"
        
    except Exception:
        return "Description unavailable"

