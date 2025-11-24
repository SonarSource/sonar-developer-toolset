# Claude Skills Management Scripts

A comprehensive set of Python scripts for managing Claude skills via the Anthropic Skills API. These scripts allow you to create, update, list, and delete skills from your Anthropic account.

**Important**: Skills created via the API are shared among all squad members using the same API key. Each squad typically has their own shared API key.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+** installed on your system
2. **Anthropic Python SDK** installed:
   ```bash
   pip install anthropic
   ```
3. **API Key**: Get your Anthropic API key from the [Anthropic Console](https://console.anthropic.com/)

### Setup

1. **Set your API key** as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```
   
   Or add it to your shell profile (`.bashrc`, `.zshrc`, etc.):
   ```bash
   echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

2. **Navigate to the skills directory**:
   ```bash
   cd claude/skills
   ```

**Note:** These scripts manage **API-based skills** which are shared among squad members using the same API key. This is different from **local filesystem skills** used in Claude Code, which are personal-only.

## 📋 Two Ways to Use Skills

### Option 1: Squad Skills (API-based) - Recommended
Use these scripts to upload skills and share them with your squad:
- Skills are uploaded to Anthropic's servers via API
- Accessible by all squad members using the same API key
- Managed centrally through these scripts

### Option 2: Personal Skills (Local filesystem) - Claude Code only  
Copy skill folders directly to your local directories for personal use in Claude Code:
- Copy `lib/skill-name/` to `~/.claude/skills/skill-name/`
- Only works in Claude Code (CLI/Desktop)
- Personal use only, not shared with team

## 📁 File Structure

```
claude/
└── skills/
    ├── scripts/            # Management scripts
    │   ├── create_skill.py     # Create new skills
    │   ├── update_skill.py     # Update existing skills
    │   ├── list_skills.py      # List all your skills
    │   ├── delete_skill.py     # Delete skills
    │   └── skill_utils.py      # Shared utility functions
    ├── lib/                # Shared skills library
    │   ├── java-unit-testing/
    │   │   └── SKILL.md
    │   └── logging-best-practices/
    │       └── SKILL.md
    └── README.md          # This file
```

## 🎯 Pure Path-Based System

This tool uses **direct paths only** for maximum clarity and flexibility. No magic search, no confusion - you specify exactly where your skill is located.

### Usage Patterns

```bash
# Deploy skills from lib/
python scripts/create_skill.py lib/java-unit-testing
python scripts/create_skill.py lib/logging-best-practices

# List deployed and available skills
python scripts/list_skills.py
```

### Benefits

- **🎯 Explicit**: Always know exactly which skill file is being used
- **🧹 Simple**: No complex search logic or precedence rules  
- **🔧 Flexible**: Works with any directory structure
- **🐛 Debuggable**: Clear error messages show exact paths checked

## 🚀 Quick Setup for Local Use (Claude Code)

If you just want to use these skills personally in Claude Code without API registration:

```bash
# Copy skills to your local directory
cp -r lib/java-unit-testing ~/.claude/skills/
cp -r lib/logging-best-practices ~/.claude/skills/

# Verify the structure
ls -la ~/.claude/skills/
```

Your skills will be automatically discovered by Claude Code.

## 🛠️ Script Usage (Team/API-based)

### 1. Create a New Skill

Creates a new Claude skill from a local SKILL.md file.

```bash
python create_skill.py <path-to-skill-folder>
```

**Examples:**
```bash
# Deploy skills from lib/
python scripts/create_skill.py lib/java-unit-testing
python scripts/create_skill.py lib/logging-best-practices
```

**What it does:**
- Takes direct path to skill folder containing SKILL.md
- Supports relative paths, absolute paths, and tilde expansion  
- Uses folder name as display title in kebab-case (e.g., "java-unit-testing")
- Creates the skill in your Anthropic account
- Returns skill ID, version, and source path information

### 2. Update an Existing Skill

Updates an existing skill or creates it if it doesn't exist.

```bash
python update_skill.py <skill-folder-name>
```

**Examples:**
```bash
python update_skill.py java-unit-testing
python update_skill.py my-custom-skill
```

**What it does:**
- Looks for existing skill by display title (kebab-case folder name)
- If found: creates a new version of the existing skill
- If not found: creates a new skill
- Skills are matched by display title

### 3. List All Skills

Lists all skills in your Anthropic account.

```bash
python list_skills.py
```

**Sample Output:**
```
✅ Found 1 skill(s):

Display Title             Version      Created            Updated           
Skill ID                                          
--------------------------------------------------------------------------
java-unit-testing         1            2024-01-15 10:30   2024-01-15 10:30  
  ID: skill_abc123xyz789

📊 Total: 1 skill(s) deployed to Anthropic

==========================================================================
📁 AVAILABLE SKILLS TO DEPLOY:
==========================================================================

✅ Found 2 available skill(s):

📚 Name: java-unit-testing
   Path: lib/java-unit-testing
   Description: Helps with creating comprehensive unit tests for Java code
   Deploy: python scripts/create_skill.py lib/java-unit-testing

📚 Name: logging-best-practices
   Path: lib/logging-best-practices
   Description: Guidelines for implementing effective logging in applications
   Deploy: python scripts/create_skill.py lib/logging-best-practices
```

### 4. Delete a Skill

Deletes a skill by ID or display title (with confirmation).

```bash
python delete_skill.py <skill-id-or-title>
```

**Examples:**
```bash
# Delete by skill ID
python delete_skill.py skill_abc123xyz789

# Delete by display title
python scripts/delete_skill.py "java-unit-testing"

# Delete by folder name
python scripts/delete_skill.py java-unit-testing
```

**Safety Features:**
- Asks for confirmation before deletion
- Shows skill details before confirming
- Supports multiple identification methods (ID, title, folder name)

## 🆘 Help and Documentation

All scripts support help flags:

```bash
python create_skill.py --help
python update_skill.py --help
python list_skills.py --help
python delete_skill.py --help
```

## 📝 Skill File Format

Your `SKILL.md` file should follow the Claude Skills format. Here's a basic template:

```markdown
---
name: my-skill-name
description: Brief description of what your skill does and when to use it
---

# My Skill Name

## Usage
How to use the skill.

## Examples
Example usage scenarios.
```

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | ✅ Yes |

## ⚠️ Error Handling

The scripts include comprehensive error handling for common issues:

### API Key Issues
- **Missing API key**: Clear error message with setup instructions
- **Invalid API key**: Authentication error with troubleshooting tips
- **Permission denied**: Guidance on API key permissions

### File Issues
- **Missing SKILL.md**: Clear path information and suggestions
- **File access errors**: Detailed error descriptions

### Network Issues
- **Connection problems**: Retry suggestions and troubleshooting
- **API rate limits**: Guidance on handling rate limits

## 🎯 Best Practices

### Folder Naming
- Use lowercase with dashes: `java-unit-testing`, `data-analysis`
- Avoid spaces and special characters
- Be descriptive but concise

### Skill Development Workflow
1. **Create** folder in `lib/`:
   ```bash
   mkdir -p lib/my-new-skill
   ```
2. **Write** your `SKILL.md` file with YAML frontmatter
3. **Deploy** the skill:
   ```bash
   python scripts/create_skill.py lib/my-new-skill
   ```
4. **Update** when ready:
   ```bash
   python scripts/update_skill.py lib/my-new-skill
   ```

### Version Management
- Each update creates a new version
- Old versions are preserved in the system
- Use descriptive commit-like messages in your skill updates

## 🔧 Troubleshooting

### Common Issues

**1. "ANTHROPIC_API_KEY environment variable is not set"**
```bash
# Set the API key
export ANTHROPIC_API_KEY='your-api-key-here'
# Verify it's set
echo $ANTHROPIC_API_KEY
```

**2. "Skill file not found"**
- Ensure the skill folder contains a `SKILL.md` file (exact spelling and case)
- Check the skill directory structure: `ls -la path/to/skill/`
- Verify the folder path matches what you're passing to the script

**3. "Permission denied"**
- Verify your API key has Skills API access
- Check that your API key is active and not expired
- Ensure you have the correct permissions in your Anthropic account

**4. "Failed to initialize Anthropic client"**
- Check your internet connection
- Verify the API key format is correct
- Try regenerating your API key if issues persist

### Getting Help

1. **Use the help flags** on any script: `--help`
2. **Check the API documentation**: [Anthropic Skills API](https://docs.anthropic.com/)
3. **Verify your setup** with `list_skills.py` first

## 📚 Managing Shared Skills

### Contributing to Team Library

1. **Create a new skill** in the repo's `lib/` directory:
   ```bash
   mkdir -p lib/my-new-skill
   vim lib/my-new-skill/SKILL.md
   ```

2. **Test the skill locally**:
   ```bash
   python create_skill.py lib/my-new-skill
   ```

3. **Commit to the repo**:
   ```bash
   git add lib/my-new-skill/
   git commit -m "Add new team skill: my-new-skill"
   git push
   ```

### Updating Shared Skills

```bash
# Edit the skill file
vim lib/java-unit-testing/SKILL.md

# Test the update
python update_skill.py lib/java-unit-testing

# Commit changes
git add lib/java-unit-testing/SKILL.md
git commit -m "Update java-unit-testing skill"
git push
```

### Best Practices for Shared Skills

- **Descriptive Names**: Use clear, descriptive folder names
- **Documentation**: Include comprehensive skill descriptions
- **Testing**: Test skills before committing
- **Versioning**: Use meaningful git commit messages
- **Review**: Have skills reviewed by team members

## 🤝 Sharing with Your Team

### For Team Distribution

1. **Share this repository** with your squad
2. **Skills are shared among squad members** using the same API key
3. **Standardize folder naming** conventions across squads
4. **Use version control** for your skill definitions

### Recommended Team Workflows

#### Option A: Squad Skills (API-based)
```bash
# Setup (once)
export ANTHROPIC_API_KEY='squad-shared-api-key'
cd claude/skills

# Deploy skills (shared with squad)
python scripts/create_skill.py lib/java-unit-testing
python scripts/list_skills.py
```

#### Option B: Personal Skills (Claude Code only)
```bash
# Copy skills to local directory
cp -r lib/* ~/.claude/skills/
```

## 📊 Script Features Summary

| Script | Purpose | Key Features |
|--------|---------|--------------|
| `create_skill.py` | Create new skills | ✅ Auto-title generation<br/>✅ File validation<br/>✅ Error handling |
| `update_skill.py` | Update/create skills | ✅ Auto-detection<br/>✅ Version management<br/>✅ Fallback creation |
| `list_skills.py` | View all skills | ✅ Formatted output<br/>✅ Date formatting<br/>✅ Summary stats |
| `delete_skill.py` | Remove skills | ✅ Confirmation prompts<br/>✅ Multi-ID support<br/>✅ Safety warnings |

## 🚀 Potential Next Steps

Based on team feedback and Anthropic's Skills API capabilities, we're considering adding:

### 🔍 Enhanced Validation & Safety
- **Skill Validation**: Validate SKILL.md format and required metadata before upload
- **Size Monitoring**: Check against the 8MB workspace upload limit
- **Dependency Checking**: Validate skills that depend on other skills or shared resources

### 📦 Bulk Operations & Templates  
- **Bulk Deployment**: Deploy/update multiple skills from a manifest file
- **Skill Templates**: Generate new skill scaffolding with standardized structure
- **Batch Updates**: Update multiple skills simultaneously with version control

### 🏢 Team Governance
- **Version Pinning**: Allow teams to pin to specific skill versions for stability
- **Approval Workflows**: Features for skill review and approval processes
- **Skill Composition**: Tools to help combine skills for complex workflows

### 📊 Monitoring & Analytics
- **Usage Tracking**: Monitor which skills are being used most frequently
- **Performance Metrics**: Track skill execution times and success rates
- **Team Dashboard**: Overview of workspace skills and their status

*Have ideas for other features? Open an issue or contribute to the project!*

## 🔄 Version History

- **v1.0**: Initial scripts with basic functionality
- **v2.0**: Added comprehensive error handling, help documentation, and team-sharing features

---

**Happy skill building! 🚀**

## 📚 Additional Resources

For more information about Claude Skills, check out the official documentation:

- **[Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** - Understanding skills and where they work
- **[Skills Quickstart](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart)** - Getting started with skills
- **[Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)** - Writing effective skills
- **[Skills API Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)** - Technical API reference

For questions or issues with these scripts, please refer to the help documentation in each script (`--help` flag) or open an issue in this repository.
