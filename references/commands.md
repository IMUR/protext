# Protext Command Reference

All protext commands with syntax, examples, and natural language alternatives.

## Command Summary

| Command | Purpose | Shorthand |
|---------|---------|-----------|
| **`/protext`** | **Load orientation (primary)** | "Load protext" |
| `protext init` | Initialize protext in project | "Set up protext" |
| `protext status` | Show current state | "What's the context?" |
| `protext scope` | Switch active scope | `@scope-name` |
| `protext handoff` | Capture/show handoff | "Save session state" |
| `protext extract` | Pull deep context | `@deep:name` |
| `protext refresh` | Update PROTEXT.md | "Refresh the protext" |

---

## /protext (Primary Command)

**Load project orientation at session start.** This is the main entry point.

### Syntax

```
/protext                    # Load orientation + scope + handoff
/protext @[scope]           # Load with specific scope
/protext --full             # Include extraction list
/protext --minimal          # PROTEXT.md only, no scope/handoff
```

### Natural Language (Cross-Platform)

- "Load protext"
- "Show me the project context"
- "What's the current state of this project?"
- "Orient me to this codebase"
- "Load the context"

### What It Loads

1. **PROTEXT.md** - Project identity, current state, hot context
2. **Active scope** - Domain-specific orientation (ops/dev/security)
3. **Handoff status** - Session continuity with FRESH/AGING/STALE indicator
4. **(--full)** Available extractions from index.yaml

### Example Output

```
═══════════════════════════════════════════════════════
 PROTEXT: Cooperator Node (crtr-config)
 Scope: @ops | Handoff: FRESH (2h ago)
═══════════════════════════════════════════════════════

## Identity
Edge services and ingress node for Raspberry Pi home cluster.
Runs Caddy reverse proxy, Pi-hole v6 DNS, Headscale VPN.

## Current State
Active: Protext system design | Blocked: None | Recent: Docs consolidation

## Hot Context
• Caddy config: /etc/caddy/Caddyfile - validate before reload
• Pi-hole admin: https://dns.ism.la (Port 8080)
• All secrets via Infisical - never hardcode
• Split-horizon DNS: LAN=192.168.254.10, Mesh=100.64.0.1

## Handoff
Last: Protext initialized | Next: Test in sessions | Caution: First usage

───────────────────────────────────────────────────────
Extractions available: @deep:network, @deep:services, @deep:secrets...
Use @deep:[name] to load additional context.
═══════════════════════════════════════════════════════
```

### Flags

| Flag | Effect |
|------|--------|
| `@[scope]` | Override active scope for this load |
| `--full` | Show all available extractions |
| `--minimal` | Skip scope and handoff, just PROTEXT.md |
| `--json` | Output as JSON (for tooling integration) |

---

## protext init

Initialize protext in a project.

### Syntax

```
protext init [--tier beginner|intermediate|advanced]
```

Default: `--tier advanced`

### Natural Language

- "Initialize protext for this project"
- "Set up protext here"
- "Create protext context"
- "Bootstrap protext"

### What It Creates

**Beginner tier:**
- `PROTEXT.md` only

**Intermediate tier:**
- `PROTEXT.md`
- `.protext/handoff.md`

**Advanced tier (default):**
- `PROTEXT.md`
- `.protext/config.yaml`
- `.protext/index.yaml`
- `.protext/handoff.md`
- `.protext/scopes/ops.md`
- `.protext/scopes/dev.md`
- `.protext/scopes/security.md`

### Examples

```
# Initialize with all features (default)
"Initialize protext"

# Minimal setup
"Initialize protext with beginner tier"

# With handoff only
"Set up protext, intermediate tier"
```

### Script Usage

```bash
python scripts/init_protext.py /path/to/project
python scripts/init_protext.py /path/to/project --tier beginner
```

---

## protext status

Display current protext state.

### Syntax

```
protext status
```

### Natural Language

- "Show protext status"
- "What's the current context state?"
- "Protext info"
- "Context status"

### Output Includes

- Current tier (beginner/intermediate/advanced)
- Active scope
- Handoff status and age
- Token budget usage
- Available extractions count
- File modification times

### Example Output

```
==================================================
 Protext Status: crtr-config
==================================================

  Tier:           [A] Advanced
  Active Scope:   @ops (3/5 scopes)
  Handoff:        FRESH (age: 2.5h)
  Token Budget:   ~380/2000 (19%)
  Extractions:    5/20 defined

  Files:
    PROTEXT.md          (modified: 2026-02-05 14:30)
    .protext/handoff.md (modified: 2026-02-05 14:30)
    .protext/index.yaml
    .protext/config.yaml
```

### Script Usage

```bash
python scripts/protext_status.py /path/to/project
python scripts/protext_status.py  # Uses current directory
```

---

## protext scope

Switch active scope context.

### Syntax

```
protext scope [name]
protext scope list
```

### Shorthand

```
@ops
@dev
@security
@[scope-name]
```

### Natural Language

- "Switch to ops scope"
- "Focus on security context"
- "Change scope to development"
- "I'm working on security stuff"
- "List available scopes"

### Behavior

1. Updates `active_scope` in `.protext/config.yaml`
2. Loads corresponding scope file from `.protext/scopes/[name].md`
3. Updates scope indicator in PROTEXT.md header

### Examples

```
# Switch scope
"Switch to security scope"
"@security"
"Focus on ops"

# List scopes
"What scopes are available?"
"protext scope list"
```

### Scope Limits

- Maximum 5 scopes per project
- Default scopes: ops, dev, security
- Custom scopes: Create `.protext/scopes/[name].md`

---

## protext handoff

Capture or display session handoff.

### Syntax

```
protext handoff                    # Show current handoff
protext handoff capture [notes]    # Capture new handoff
protext handoff clear              # Clear handoff
```

### Natural Language

**View:**
- "What was the last handoff?"
- "Show handoff notes"
- "What did we do last time?"

**Capture:**
- "Capture handoff: stopped mid-refactor"
- "Save session state"
- "Remember this for next time: [notes]"

**Clear:**
- "Clear the handoff"
- "Reset session notes"

### Handoff Structure

```markdown
## Last Session
**Completed:** [list]
**In Progress:** [task] (stopped at: [point])
**Deferred:** [task] (blocked by: [reason])

## Cautions
[warnings for next session]

## Agent Notes
[observations]
```

### Status Markers

| Status | Age | Action |
|--------|-----|--------|
| FRESH | < 24h | Trust fully |
| AGING | 24-48h | Verify critical items |
| STALE | > 48h | Suggest refresh |

### Examples

```
# View
"Show the last handoff"

# Capture
"Capture handoff: completed the DNS migration, next step is testing certs"
"Save this: stopped at Caddy config, needs Cloudflare token from Infisical"

# With structure
"Capture handoff:
  Completed: Pi-hole upgrade
  In progress: Caddy wildcards (at DNS challenge)
  Caution: Don't restart Pi-hole during gravity update"
```

---

## protext extract

Pull deep context from extraction index.

### Syntax

```
protext extract [name]
protext extract list
```

### Shorthand

```
@deep:network
@deep:services
@deep:[extraction-name]
```

### Natural Language

- "Extract network context"
- "Load the services documentation"
- "I need details about the router config"
- "Pull in the architecture docs"
- "What extractions are available?"

### Extraction Modes

Configured in `.protext/config.yaml`:

| Mode | Behavior |
|------|----------|
| `suggest` | Shows "context available: X" - you confirm to load |
| `auto` | Loads automatically on keyword trigger |
| `confirm` | Always asks before loading |

### Examples

```
# List available
"What extractions are defined?"
"protext extract list"

# Extract specific
"@deep:network"
"Extract the services documentation"
"I need the secrets management context"

# Keyword trigger (suggest mode)
Agent: "I see there's DNS-related context available: network (~600 tokens). Load it?"
You: "Yes, load it"
```

### Budget Enforcement

- Default budget: 2000 tokens per session
- Warning at 80%: "Approaching context budget (1600/2000)"
- At 100%: "Budget reached. Use @force-extract to override."

---

## protext refresh

Update PROTEXT.md hot context.

### Syntax

```
protext refresh
protext refresh hot [new items]
protext refresh state [new state]
```

### Natural Language

- "Refresh the protext"
- "Update hot context"
- "Change current state to: working on tests"
- "Add to hot context: new priority item"

### Examples

```
# Full refresh
"Refresh protext based on current work"

# Update specific sections
"Update hot context: Caddy migration complete, now on DNS"
"Change state to: Active: Testing | Recent: Caddy config"

# Add item
"Add to hot context: Remember to check backup job"
```

---

## Error Messages

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| "Protext not initialized" | No PROTEXT.md found | Run `protext init` |
| "Scope not found: X" | Scope file doesn't exist | Create `.protext/scopes/X.md` |
| "Max scopes reached (5)" | Too many scopes | Merge or archive existing scopes |
| "Extraction not found: X" | Not in index.yaml | Add to `.protext/index.yaml` |
| "Token budget exceeded" | Over 2000 tokens loaded | Use `@force-extract` or increase budget |
| "Handoff is STALE" | > 48h since update | Capture new handoff |

### Recovery Commands

```
# Reset to defaults
"Reset protext config to defaults"

# Force operations
"@force-extract:network"  # Bypass budget
"Force scope switch even if over limit"

# Clear state
"Clear all protext state and reinitialize"
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│                 PROTEXT QUICK REF                   │
├─────────────────────────────────────────────────────┤
│ ▶ LOAD     /protext              ← START HERE       │
│            /protext @security    (with scope)       │
│            /protext --full       (show extractions) │
├─────────────────────────────────────────────────────┤
│ INIT       protext init [--tier X]                  │
│ STATUS     protext status                           │
│ SCOPE      @ops  @dev  @security                    │
│ EXTRACT    @deep:network  @deep:services            │
│ HANDOFF    "capture handoff: [notes]"               │
│ REFRESH    "refresh protext"                        │
├─────────────────────────────────────────────────────┤
│ LIMITS     5 scopes | 20 extractions | 2000 tokens  │
│ HANDOFF    FRESH <24h | AGING 24-48h | STALE >48h   │
└─────────────────────────────────────────────────────┘
```
