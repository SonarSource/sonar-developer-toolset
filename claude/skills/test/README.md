# Claude Skills Scripts Test Suite

This directory contains a test suite for validating the Claude Skills management scripts.

## Contents

- `test-skill/` - A fake skill used for testing with proper YAML frontmatter
- `test_skills_scripts.py` - Comprehensive test script that validates all operations
- `README.md` - This file

## Running the Tests

From the repository root directory, run:

```bash
python claude/skills/test/test_skills_scripts.py
```

Or make it executable and run directly:

```bash
chmod +x claude/skills/test/test_skills_scripts.py
./claude/skills/test/test_skills_scripts.py
```

## What the Test Does

The test script performs these operations in sequence:

1. **List skills** - Shows initial state
2. **Create skill** - Creates the test skill from `test-skill/`
3. **List skills** - Verifies the skill appears in the list
4. **Update skill** - Modifies the skill description and updates it
5. **List skills** - Verifies the update worked
6. **Delete skill** - Cleans up by deleting the test skill

## Requirements

- `ANTHROPIC_API_KEY` environment variable must be set
- Anthropic API key must have skills permissions
- Internet connection for API calls

## Test Skill Details

The test skill includes:
- Proper YAML frontmatter with `name` and `description`
- Realistic skill content for testing
- Safe content that won't cause API issues

## Idempotent Design

The test is designed to be idempotent:
- Always cleans up the test skill at the end
- Can be run multiple times safely
- Handles failures gracefully with cleanup

## Troubleshooting

If tests fail:
1. Check that `ANTHROPIC_API_KEY` is set correctly
2. Verify API key has skills permissions
3. Check internet connectivity
4. Look at the detailed output for specific error messages
5. Manually clean up any leftover test skills if needed

The test skill will have "Test Skill for Validation" as its display title.