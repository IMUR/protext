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
python3 ../skills-validator/scripts/validate_skill.py .

# Test standard init
python3 scripts/init_protext.py /path/to/project --tier advanced

# Test parent init (requires children with .protext/)
python3 scripts/init_protext.py /path/to/parent-project --parent

# Test parent refresh
python3 scripts/protext_refresh.py /path/to/parent-project --children

# Check status
python3 scripts/protext_status.py /path/to/project
```

### Deploying Updates

This repo is a dev project containing non-skill files (docs/, .protext/, CLAUDE.md, .archive/). Deploy only the skill subset:

```bash
# Copy skill files only to local skills directory
rsync -av --include='SKILL.md' --include='scripts/***' --include='references/***' --exclude='*' . ~/.agent/skills/local/protext/

# Or package from the clean deploy copy
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ~/.agent/skills/local/protext/
```

---

## Key Constraints

| Constraint | Value | Reason |
|-----------|-------|--------|
| PROTEXT.md target | ~500 tokens | Quick orientation |
| Max scopes | 5 per project | Prevent fragmentation |
| Max lateral links | 5 per project | Keep peer/sibling/reference list concise |
| Max child links | Unlimited | Structure dictates count |
| Max extractions | 20 per project | Index stays scannable |
| Token budget default | 2000 per session | Cost control |
| Handoff TTL | 48h (legacy) | No longer enforced (v2.1) |
| Hierarchy depth | 1 level | Parent → children only |
| SKILL.md max | ~500 lines | Skill creator guideline |

---

## File Map

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition (frontmatter + instructions) |
| `scripts/init_protext.py` | Bootstrap protext (standard or parent mode) |
| `scripts/protext_status.py` | Display protext state for a project |
| `scripts/protext_refresh.py` | Refresh parent protext from children |
| `references/formats.md` | Format specs (PROTEXT.md, markers, parent mode) |
| `references/commands.md` | Command reference with examples |
| `docs/DESIGN.md` | Design decisions and lineage (v1 → v2 → v2.1) |
| `NEXT-FEATURES.md` | v2.1 feature spec (markers, parent, handoff redesign) |
| `.archive/` | Earlier v1 domain-specific injectors |
