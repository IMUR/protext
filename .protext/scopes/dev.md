# Scope: Dev

## Focus
Development workflow, code patterns, testing, debugging.

## Key Resources
- `scripts/init_protext.py` — Bootstrap protext in any project
- `scripts/protext_status.py` — Display protext state
- `references/formats.md` — Format specs for all protext files
- `references/commands.md` — Command reference with examples

## Current Priorities
1. Validate: `python3 /mnt/ops/prj/skills/skills-validator/scripts/validate_skill.py /mnt/ops/prj/skills/protext`
2. Deploy: `rsync -av --include='SKILL.md' --include='scripts/***' --include='references/***' --exclude='*' /mnt/ops/prj/skills/protext/ ~/.agent/skills/local/protext/`

## Cautions
- `extract_project_info` pulls first heading from CLAUDE.md as project name — often wrong (e.g. "CLAUDE.md")
- No automated test suite — validation via skills-validator is the quality gate
