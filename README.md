# Protext

Dynamic context management for AI coding agents. Provides token-efficient project orientation via a three-layer hierarchy so agents can quickly understand a project without loading everything into context.

## What it does

```
PROTEXT.md (L0)      .protext/index.yaml (L1)     Deep Context (L2)
  ~500 tokens            Signposts only              Full docs/memory
  Always loaded          On-demand hints              Explicit extraction
```

**Key idea:** `CLAUDE.md` defines agent *behavior* (stable). `PROTEXT.md` defines project *state* (dynamic, session-aware). Protext manages the state layer.

## Install

Copy the skill to your agent skills directory:

```bash
# Claude Code
cp -r protext/ ~/.claude/skills/protext/

# Or use rsync to copy only skill files (no dev artifacts)
rsync -av --include='SKILL.md' --include='scripts/***' --include='references/***' \
  --exclude='*' protext/ ~/.claude/skills/protext/
```

Also works with Gemini CLI (`~/.gemini/skills/`), Codex CLI (`~/.agents/skills/`), Cursor (`~/.cursor/skills/`), and OpenCode (`~/.config/opencode/skills/`).

## Usage

### Initialize protext in a project

```bash
python3 scripts/init_protext.py /path/to/project --tier advanced
```

This reads the project's `CLAUDE.md`, creates `PROTEXT.md` and the `.protext/` directory with config, extraction index, handoff state, and scope files.

**Tiers:** `beginner` (PROTEXT.md only), `intermediate` (+handoff), `advanced` (full: config, index, scopes).

### Re-initialize existing projects

When `PROTEXT.md` or `.protext/` already exist, use `--existing`:

```bash
# Date-stamp and archive existing artifacts, then init fresh
python3 scripts/init_protext.py /path/to/project --existing archive

# Delete existing (preserve archive history), then init fresh
python3 scripts/init_protext.py /path/to/project --existing replace

# Regenerate PROTEXT.md + index.yaml only, keep config/scopes/handoff
python3 scripts/init_protext.py /path/to/project --existing update
```

Without `--existing`, the script prints a conflict message and exits non-zero. No interactive prompts.

### Check protext state

```bash
python3 scripts/protext_status.py /path/to/project
```

### In-session (slash command)

Once installed as a skill, invoke `/protext` at session start to load orientation context.

## Project structure

```
protext/
├── SKILL.md              Skill definition (loaded by AI platforms)
├── scripts/
│   ├── init_protext.py   Bootstrap protext in any project
│   └── protext_status.py Display protext state
└── references/
    ├── formats.md        Format specs for all protext files
    └── commands.md        Command reference with examples
```

## Constraints

- Python 3.8+, zero external dependencies
- PROTEXT.md target: ~500 tokens
- Max 5 scopes, 20 extractions, 2000-token budget per session
- Handoff TTL: 48h (FRESH / AGING / STALE)

## License

See repository root for license information.
