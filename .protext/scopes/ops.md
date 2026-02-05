# Scope: Operations

## Focus
Deployment, packaging, distribution, and integration with skill infrastructure.

## Key Resources
- Package script: `~/.claude/skills/skill-creator/scripts/package_skill.py`
- Validate script: `~/.claude/skills/skill-creator/scripts/quick_validate.py`
- Deploy target: `~/.agent/skills/local/protext/`
- Test target: `/mnt/ops/configs/crtr-config/` (crtr-config project)

## Current Priorities
1. Establish deploy workflow (source → validate → copy → test)
2. Test on crtr-config as primary dogfood project

## Cautions
- Don't package before validating
- Test init_protext.py on a clean directory before releasing
