# CLAUDE.md

AI agent context for the Protext development project.

---

## Project Purpose

Protext is a dynamic, user-involved context management system for AI agents. It provides token-efficient "jumping-off point" summaries with controlled depth extraction, balancing detailed emergent context with concise orientation information.

**This repo contains:**
- The protext skill (`SKILL.md`, `scripts/`, `references/`)
- Design documentation (`docs/`)
- Earlier iterations (`.archive/`)

**This repo does NOT contain:**
- Deployed skill packages (those go to `~/.agent/skills/local/protext/`)
- Per-project protext instances (those live in each project's own `.protext/`)

---

## Architecture

Three-layer context hierarchy:
```
PROTEXT.md (L0) → .protext/index.yaml (L1) → Deep Context (L2)
  ~500 tokens        Signposts only            Full docs
  Always loaded      On-demand hints            Explicit extraction
```

Key separation: `CLAUDE.md` = behavior (stable), `PROTEXT.md` = state (dynamic).

---

## Development Workflow

### Testing the Skill

```bash
# Validate skill structure
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py .

# Test init on a target project
python3 scripts/init_protext.py /path/to/project --tier advanced

# Check status
python3 scripts/protext_status.py /path/to/project
```

### Deploying Updates

```bash
# Copy to local skills directory
cp -r . ~/.agent/skills/local/protext/

# Or package for distribution
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py .
```

---

## Key Constraints

| Constraint | Value | Reason |
|-----------|-------|--------|
| PROTEXT.md target | ~500 tokens | Quick orientation |
| Max scopes | 5 per project | Prevent fragmentation |
| Max extractions | 20 per project | Index stays scannable |
| Token budget default | 2000 per session | Cost control |
| Handoff TTL | 48h | Prevent stale guidance |
| SKILL.md max | ~500 lines | Skill creator guideline |

---

## File Map

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition (frontmatter + instructions) |
| `scripts/init_protext.py` | Bootstrap protext in any project |
| `scripts/protext_status.py` | Display protext state for a project |
| `references/formats.md` | Format specs for all protext files |
| `references/commands.md` | Command reference with examples |
| `docs/` | Design docs and architecture decisions |
| `.archive/` | Earlier v1 domain-specific injectors |
