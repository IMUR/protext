# Scope: Development

## Focus
Protext skill development — SKILL.md, Python scripts, reference docs, testing.

## Key Resources
- Skill definition: `SKILL.md`
- Init script: `scripts/init_protext.py`
- Status script: `scripts/protext_status.py`
- Format specs: `references/formats.md`
- Command reference: `references/commands.md`
- Skill creator tools: `~/.claude/skills/skill-creator/scripts/`

## Current Priorities
1. Iterate based on real-world usage feedback
2. Improve init script project name detection
3. Add tests for scripts

## Cautions
- Keep SKILL.md under 500 lines (skill creator guideline)
- After changes, always re-validate with quick_validate.py
- Deploy changes to `~/.agent/skills/local/protext/` after testing
