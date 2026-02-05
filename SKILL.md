---
name: protext
description: Dynamic context management for AI agents. Invoke /protext at session
  start to load token-efficient project orientation. Use when (1) Starting a session
  and need quick orientation, (2) Handing off between sessions, (3) Managing context
  for multi-scope projects (dev/ops/security), (4) Reducing token usage while
  maintaining awareness. Primary command is /protext to load context. Other commands
  include protext init, status, scope, handoff, extract.
---

# Protext: Dynamic Context Management

Protext provides a three-layer context hierarchy for token-efficient AI agent orientation.

## Core Concept

```
PROTEXT.md (Layer 0)  →  .protext/index.yaml (Layer 1)  →  Deep Context (Layer 2)
     ~500 tokens              Signposts only                 Full docs/memory
     Always loaded            On-demand hints                Explicit extraction
```

**Separation of Concerns:**
- `CLAUDE.md` = Agent behavior (how to act) — stable, rarely changes
- `PROTEXT.md` = Project state (what's happening) — dynamic, session-aware

## File Structure

```
project-root/
├── PROTEXT.md                  # Layer 0: Orientation (~500 tokens)
├── CLAUDE.md                   # Existing: Behavior instructions
└── .protext/
    ├── index.yaml              # Layer 1: Extraction signposts
    ├── handoff.md              # Session continuity
    ├── scopes/
    │   ├── ops.md              # Operations context
    │   ├── dev.md              # Development context
    │   └── security.md         # Security context
    └── config.yaml             # Protext settings
```

## PROTEXT.md Format

```markdown
# Protext: [Project Name]
> Generated: YYYY-MM-DD | Scope: [active-scope] | Tokens: ~XXX

## Identity
[1-2 sentences: What is this project/system?]

## Current State
Active: [current work] | Blocked: [blockers] | Recent: [last completed]

## Hot Context
- [Critical point 1]
- [Critical point 2]
- [Critical point 3]

## Scope Signals
- `@ops` → .protext/scopes/ops.md
- `@security` → .protext/scopes/security.md
- `@deep:[name]` → Extract from index

## Handoff
Last: [summary] | Next: [suggested] | Caution: [warnings]
```

## Commands

### `/protext` (Primary - Session Start)

**Load project orientation.** This is the main entry point - invoke at session start.

```bash
/protext              # Load PROTEXT.md + active scope + handoff status
/protext @security    # Load with security scope
/protext --full       # Include available extractions list
```

**What it does:**
1. Reads and displays PROTEXT.md (orientation layer)
2. Shows handoff status (FRESH/AGING/STALE)
3. Loads active scope context
4. Lists available deep extractions (with `--full`)

**Cross-platform:** Works as slash command on Claude Code, or natural language on other platforms:
- "Load protext"
- "Show me the project context"
- "What's the current state?"

**If no PROTEXT.md exists:** Inform the user and offer to run `protext init` to bootstrap one. Do not fail silently.

---

### `protext init`

Initialize protext in a project. Reads existing CLAUDE.md to bootstrap.

```bash
# In conversation
"Initialize protext for this project"
"Set up protext here"
```

Creates: PROTEXT.md, .protext/ directory with full structure.

### `protext status`

Display current protext state.

```bash
"Show protext status"
"What's the current context state?"
```

Shows: Tier, active scope, handoff age, token budget, available extractions.

### `protext scope [name]`

Switch active scope context.

```bash
"Switch to ops scope"
"Focus on security context"
"@security"  # Shorthand
```

### `protext handoff`

Capture or display session handoff.

```bash
"Capture handoff: stopped mid-refactor, next step is testing"
"What was the last handoff?"
```

Handoff auto-stales after 48h (marked `[STALE]`).

### `protext extract [name]`

Pull deep context from index.

```bash
"Extract network context"
"@deep:services"  # Shorthand
```

Agent receives extraction suggestion; confirm to load.

## Extraction Modes

Configure in `.protext/config.yaml`:

```yaml
extraction_mode: suggest  # suggest | auto | confirm
token_budget: 2000        # Max extraction tokens per session
```

- **suggest** (default): Agent sees "context available: X" but doesn't auto-load
- **auto**: Keyword triggers load (opt-in, risky for token budget)
- **confirm**: Agent proposes extraction, user must approve

## Index Schema

`.protext/index.yaml`:

```yaml
extractions:
  network:
    source: docs/NETWORK.md
    triggers: [dns, ip, tailscale, mesh, routing]
    summary: "IPs, DNS config, mesh nodes"
    tokens: ~600

  services:
    source: docs/SERVICES.md
    triggers: [docker, container, service, port]
    summary: "Docker services, ports, domains"
    tokens: ~800

  secrets:
    source: docs/SECRETS.md
    triggers: [secret, credential, infisical, auth]
    summary: "Secrets management, auth patterns"
    tokens: ~400
```

**Limits:** Max 20 extractions per project.

## Scopes

Scopes provide domain-specific orientation. Max 5 per project.

Default scopes:
- `ops` — Infrastructure, deployment, monitoring
- `dev` — Development workflow, code patterns
- `security` — Auth, secrets, vulnerabilities
- `project` — Project-specific context (custom)

Scope file format (`.protext/scopes/ops.md`):

```markdown
# Scope: Operations

## Focus
Infrastructure management, service health, deployment.

## Key Resources
- [Service config paths]
- [Key infrastructure locations]

## Current Priorities
1. [Priority 1]
2. [Priority 2]

## Cautions
- [Ops-specific warnings]
```

## Handoff Protocol

`.protext/handoff.md`:

```markdown
# Session Handoff
> Updated: YYYY-MM-DDTHH:MM | TTL: 48h | Status: FRESH|STALE

## Last Session
**Completed:**
- [Task 1]
- [Task 2]

**In Progress:**
- [Task] (stopped at: [point])

**Deferred:**
- [Task] (blocked by: [reason])

## Cautions
- [Warning 1]
- [Warning 2]

## Agent Notes
[Observations that might help next session]
```

TTL enforcement:
- **FRESH** (< 24h): Full trust
- **AGING** (24-48h): Note the age
- **STALE** (> 48h): Warn user, suggest refresh

## Progressive Tiers

### Beginner
- PROTEXT.md only
- No scopes, extractions, or handoff
- Direct editing

### Intermediate
- PROTEXT.md + handoff.md
- Session continuity
- No extraction index

### Advanced (Default)
- Full feature set
- Scopes, extractions, token budgets
- Config-driven behavior

## Constraints

| Limit | Value | Rationale |
|-------|-------|-----------|
| Max scopes | 5 | Prevent fragmentation |
| Max extractions | 20 | Index stays scannable |
| Token budget | 2000 | Default per-session limit |
| Handoff TTL | 48h | Prevent stale guidance |
| PROTEXT.md size | ~500 tokens | Quick orientation |

## Integration Patterns

### With CLAUDE.md

CLAUDE.md provides behavioral instructions (stable):
```markdown
# CLAUDE.md
## How to Work
- Validate Caddy config before reloading
- Never hardcode secrets
```

PROTEXT.md provides state orientation (dynamic):
```markdown
# PROTEXT.md
## Current State
Active: Caddy refactor | Recent: Pi-hole v6 migration
```

### With Memory Systems

Protext complements but doesn't replace:
- **memory/** — Long-term learnings, patterns
- **PROTEXT.md** — Current session orientation

## Scripts

Requires **Python 3.8+**. No external packages needed (yaml parsed with fallback).

- `scripts/init_protext.py` — Bootstrap protext in a project
- `scripts/protext_status.py` — Display current state

## Reference Files

Consult these only when deeper detail is needed:

- `references/formats.md` — Read when creating or editing PROTEXT.md, index.yaml, handoff.md, or scope files. Contains complete templates and field guidelines.
- `references/commands.md` — Read when implementing command handling or troubleshooting. Contains full syntax, flags, error messages, and natural language alternatives.
