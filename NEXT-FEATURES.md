# Protext: Next Features

Planning document for upcoming protext enhancements.

## Table of Contents

1. [Parent Protext & Hierarchical Context](#parent-protext--hierarchical-context)
2. [Machine-Readable Markers](#machine-readable-markers)
3. [Handoff Redesign](#handoff-redesign)
4. [Bidirectional Awareness](#bidirectional-awareness)
5. [Conversational Command Interface](#conversational-command-interface)
6. [Zero Auto-Execution Principle](#zero-auto-execution-principle)
7. [Implementation Roadmap](#implementation-roadmap)

---

## Parent Protext & Hierarchical Context

**Goal:** Support meta-projects that aggregate multiple child protext-enabled projects.

**Use Case:** `/mnt/ops/prj/` contains `skills/`, `homelab/`, `infra/` — each with its own PROTEXT.md. Parent protext at `/mnt/ops/prj/PROTEXT.md` provides bird's-eye view of all children.

### Parent PROTEXT.md Structure

```markdown
# Protext: Projects Root

## Identity
Meta-project containing AI agent tooling: skills catalog, protext context system, validator.

## Current State
Active: 2/3 children active | Blocked: None | Recent: Protext links feature

## Child Projects
- `./protext/` → **active** | Dynamic context management | Recent: Links feature
- `./skills-validator/` → **active** | 44-point validation | Recent: Platform updates
- `./.agent/skills/` → **idle** | Canonical skills clone | Recent: Synced from remote

## Hot Context
- Protext now supports cross-project linking with 6 relationship types
- Validator covers 8 AI platforms (Claude, Codex, OpenCode, Cursor, etc.)
- Skills-sync deploys from .agent/skills/ to platform-native paths

## Links
- `./protext` → child | context management
- `./skills-validator` → child | quality gate

## Handoff
[User-captured notes, if any]
```

### Commands

```bash
# Initialize parent protext (scans for children)
protext init --parent

# Re-aggregate child status (explicit user action)
protext refresh --children
```

### Key Features

- **Discovery:** Scans for child `.protext/` directories, reads each child's PROTEXT.md
- **Aggregation:** Extracts identity, state, hot context from children into parent's `## Child Projects` section
- **Scope signals:** Parent scopes can map to children: `@skills → skills/PROTEXT.md`
- **Depth limit:** Parent only sees immediate children, not grandchildren (prevent recursion complexity)
- **No extractions at parent level:** Extractions live in children only

---

## Machine-Readable Markers

**Goal:** Make PROTEXT.md sections extractable by parent protext for aggregation, while keeping them human-readable.

### Marker Syntax (HTML Comments)

```markdown
## Identity
<!-- marker:identity -->
Monorepo for AI agent skills management and validation tools.
<!-- /marker:identity -->

## Current State
<!-- marker:state -->
Active: Links feature implementation | Blocked: None | Recent: Validator platform updates
<!-- /marker:state -->

## Hot Context
<!-- marker:hot -->
- Links system adds cross-project signposting
- Skills-validator updated with Claude Code extension fields
- Protext and validator both self-validate cleanly
<!-- /marker:hot -->

## Links
<!-- marker:links -->
- `../skills-validator` → peer | quality gate for SKILL.md format
- `./protext` → child | dynamic context management system
<!-- /marker:links -->

## Handoff
<!-- marker:handoff -->
[User-captured notes, if any]
<!-- /marker:handoff -->
```

### Why HTML Comments?

- Invisible to non-parent readers (standard protext usage unaffected)
- Parseable by parent aggregation logic
- No new syntax to learn
- Works with existing markdown renderers

### Marker Blocks

All sections get markers:
- `<!-- marker:identity -->`
- `<!-- marker:state -->`
- `<!-- marker:hot -->`
- `<!-- marker:links -->`
- `<!-- marker:handoff -->`

Parent's `protext refresh --children` extracts these blocks from each child and composes the `## Child Projects` section.

---

## Handoff Redesign

**Current behavior:** Agents encouraged to auto-update handoff at session end (48h TTL with FRESH/AGING/STALE warnings).

**New behavior:** Handoff is **user-initiated only**, becomes an optional scratchpad rather than mandatory protocol.

### Changes

1. **Explicit capture only:**
   ```bash
   "protext handoff capture: stopped mid-refactor, next is testing"
   "Capture handoff: completed DNS migration, next step is certs"
   ```

2. **No auto-capture:** Remove guidance for agents to auto-update at session end

3. **No TTL warnings:** Handoff age doesn't trigger warnings (it's just notes, not state)

4. **Optional file:** `.protext/handoff.md` is created only if user captures a handoff

5. **Read-only by default:**
   ```bash
   "Show the handoff"
   "What was the last handoff?"
   ```

### Why This Change?

- Handoff was too prescriptive (not all projects need session continuity)
- TTL warnings were noise for projects with long gaps between sessions
- User-initiated makes it opt-in rather than core mechanic
- Aligns with zero auto-execution principle

---

## Bidirectional Awareness

**Goal:** Children know their parent, parent knows its children.

### Config Schema Update

`.protext/config.yaml` gains hierarchy fields:

```yaml
# Protext Configuration

# Extraction behavior
extraction_mode: suggest
token_budget: 2000

# Handoff settings
handoff_ttl_hours: 48

# Active scope
active_scope: ops

# Hierarchy (new)
parent: ../                # Relative path to parent protext (optional)
children:                  # List of child protext paths (optional, parent only)
  - ./protext
  - ./skills-validator
  - ./.agent/skills

# Feature flags
features:
  auto_handoff_capture: false   # Now defaults to false
  token_warnings: true
  scope_switching: true
```

### Initialization Behavior

**Parent initialization:**
```bash
protext init --parent
```

1. Scans for child `.protext/` directories
2. Creates parent PROTEXT.md with `## Child Projects` section (extracted from child markers)
3. Writes parent config with `children: []` list
4. **Optionally** updates each child's config with `parent: ../` (requires user confirmation)

**Agent prompt:**
```
"Found 3 child protext projects. Update their configs with parent reference?"
Options: yes (update all) | no (skip) | ask (prompt per child)
```

### Link Types Extended

Add two new relationship types for hierarchy:

| Type | Meaning | Example |
|------|---------|---------|
| `child` | This is a child project | parent → child |
| `parent` | This is a parent project | child → parent |
| `sibling` | Same role, different node/environment | crtr homelab ↔ drtr homelab |
| `peer` | Different role, same system | protext ↔ skills-validator |
| `dependency` | This project depends on that one | app → shared-lib |
| `consumer` | That project uses this one | homelab → protext |
| `reference` | Not connected, contextually useful | project → upstream docs |

**Total: 7 relationship types**

---

## Conversational Command Interface

**Goal:** Make protext commands discoverable through inline prompts rather than requiring flag memorization.

### Current (Flag-Based)

```bash
protext init --tier advanced --parent --existing replace
/protext --full
protext refresh --children
```

User must know syntax.

### New (Conversational)

```
User: "protext init"

Agent: "Initialize protext. I'll ask a few questions:

  1. Tier? (beginner | intermediate | advanced)
     Default: advanced

  2. Parent mode? (scan for children)
     Default: no

  3. Existing PROTEXT.md found. Handle how?
     - archive (move to .protext/archive/)
     - replace (overwrite)
     - update (merge)

  You can answer all at once or one by one."

User: "advanced, yes parent, replace"

Agent: [proceeds with parent initialization]
```

Or shorthand still works:

```
User: "protext init --tier advanced --parent --existing replace"
Agent: [executes directly, no prompts]
```

### Implementation

**In SKILL.md, add guidance:**

```markdown
## Conversational Command Pattern

When the user invokes a protext command without specifying all options:

1. **Check for missing options** — Does this command have flags/choices?
2. **Present as questions** — Show available options with defaults
3. **Accept flexible input** — User can answer all at once or one-by-one
4. **Skip if flags provided** — `protext init --tier advanced` bypasses prompts

Example commands with prompts:
- `protext init` → asks tier, parent mode, existing handling
- `/protext` → asks standard/minimal/full/scope
- `protext link [path]` → asks relationship type, note (already implemented)
- `protext refresh` → asks children refresh? (if parent)
```

### Benefits

- **Discoverability:** Users don't need to memorize flags
- **Flexibility:** Power users can still use flags
- **Consistency:** All commands follow same pattern
- **Natural language friendly:** "load protext with full context" → agent infers `--full`

---

## Zero Auto-Execution Principle

**Core constraint:** No protext operation executes without explicit user request.

### What This Means

**Never auto-execute:**
- ❌ Auto-refresh parent on load (stale child info is fine, user refreshes manually)
- ❌ Auto-aggregation when parent is opened
- ❌ Auto-handoff capture at session end
- ❌ Background scanning or updates
- ❌ Smart suggestions that auto-trigger file reads
- ❌ Cascading loads (opening parent doesn't auto-load children)

**Always explicit:**
- ✅ `/protext` to load orientation
- ✅ `protext refresh` to update PROTEXT.md
- ✅ `protext refresh --children` to re-aggregate from children
- ✅ `protext handoff capture` to save state
- ✅ `protext link` to add connections
- ✅ `protext extract` to pull deep context

### Example: Parent Load Behavior

```
User: "/protext"

Agent loads parent PROTEXT.md as-is (potentially stale).

If children modified since last refresh:
  Agent: "Child projects modified since last refresh (2 days ago).
          Run 'protext refresh --children' to update."

User must explicitly: "protext refresh --children"

Then agent:
  1. Scans for child .protext/ directories
  2. Reads each child's PROTEXT.md
  3. Extracts marker blocks
  4. Updates parent's ## Child Projects section
  5. Writes updated parent PROTEXT.md
```

### Why This Matters

- **Predictable:** No surprise file reads, no token budget ambushes
- **Transparent:** User always knows what's happening
- **Controllable:** Every action is deliberate
- **Fast:** No cascading operations slowing down simple commands

---

## Implementation Roadmap

### Phase 1: Markers & Handoff Redesign

**Files to update:**
- `references/formats.md` — Add marker syntax to all section templates
- `references/commands.md` — Update handoff command (user-initiated only), remove TTL warnings
- `SKILL.md` — Update handoff description, remove auto-capture language
- `scripts/init_protext.py` — Inject markers into generated PROTEXT.md template

**Changes:**
- All PROTEXT.md sections wrapped in `<!-- marker:section -->` comments
- Handoff becomes opt-in, no TTL enforcement
- `features.auto_handoff_capture: false` as default in config

**Validation:** Existing protexts work unchanged (markers are additive)

---

### Phase 2: Link Types Extended

**Files to update:**
- `references/formats.md` — Add `child` and `parent` to relationship types table (now 7 types)
- `references/commands.md` — Update `protext link` guided flow with new types
- `SKILL.md` — Update relationship types list
- `.agent/skills/protext/` — Sync updated skill

**Changes:**
- Relationship types: `sibling | peer | dependency | consumer | reference | child | parent`
- Examples in formats.md show parent→child and child→parent links

**Validation:** Existing links unaffected, new types available

---

### Phase 3: Parent Protext & Bidirectional Awareness

**Files to update:**
- `scripts/init_protext.py` — Add `--parent` flag, child discovery, aggregation logic
- `scripts/protext_refresh.py` — NEW script for `protext refresh --children`
- `references/formats.md` — Add parent PROTEXT.md template, `## Child Projects` section spec
- `references/commands.md` — Add `protext init --parent`, `protext refresh --children`
- `.protext/config.yaml` schema — Add `parent:` and `children:` fields
- `SKILL.md` — Document parent mode, child aggregation

**New functionality:**
- `protext init --parent` discovers children, creates aggregated parent PROTEXT.md
- `protext refresh --children` re-aggregates from child markers
- Parent config tracks `children: []` list
- Optional: update child configs with `parent: ../` (user confirms)

**Validation:** Parent and child protexts both validate cleanly, no recursion issues

---

### Phase 4: Conversational Interface

**Files to update:**
- `SKILL.md` — Add "Conversational Command Pattern" section with prompt guidance
- `references/commands.md` — Add prompt templates for each command (init, load, refresh, link)

**Changes:**
- Commands accept full flags OR prompt for missing options
- Flexible input parsing (all-at-once or one-by-one answers)
- Natural language alternatives trigger prompts

**Validation:** Both `protext init` and `protext init --tier advanced --parent` work correctly

---

## Design Decisions (Finalized 2026-02-10)

### 1. Marker Syntax: HTML Comments ✓
**Decision:** HTML comments (`<!-- marker:section -->`)

**Rationale:**
- Standard markdown syntax, no new conventions
- Invisible to human readers
- Parseable by parent aggregation logic
- Works with all markdown renderers

---

### 2. Parent Depth: One Level Only ✓
**Decision:** Parent → children only, no multi-level nesting

**Rationale:**
- Avoids recursion complexity
- Simpler mental model
- Sufficient for vast majority of use cases
- Can be extended later if genuine need emerges

---

### 3. Child Status Detection: Modification Time ✓
**Decision:** Detect status via PROTEXT.md modification timestamp

**Logic:**
- `**active**` if modified < 7 days
- `**idle**` if modified ≥ 7 days
- `**stale**` if PROTEXT.md missing (child initialized but never updated)

**Rationale:**
- Automatic, no manual tagging required
- Simple implementation
- "Active" matches typical sprint/iteration cycles

---

### 4. Link Type Precedence: Hierarchy Wins ✓
**Decision:** Hierarchy types (`child`, `parent`) take precedence over lateral types

**Behavior:**
- If both `child` and `peer` links to same target exist, `child` wins
- Validator should WARN on conflicting types (e.g., both `child` and `peer` to same path)

**Rationale:**
- Hierarchy is structural, lateral is contextual
- Parent/child relationships are more fundamental

---

### 5. Backward Compatibility: Best-Effort Extraction ✓
**Decision:** Fallback to heading-based parsing when markers absent

**Behavior:**
- If child has markers: use them (precise extraction)
- If child lacks markers: parse by `## Heading` (lenient fallback)
- Log note: "Child `./foo` has no markers. Consider refreshing with `protext init --existing update`"

**Rationale:**
- Pragmatic migration path
- Doesn't break existing protexts
- Encourages adoption without forcing it

---

## Design Principles

These guide all implementation decisions:

1. **Zero auto-execution** — No protext operation runs without explicit user request
2. **Markers are additive** — Existing protexts work unchanged, markers enhance but don't break
3. **User-initiated handoff** — Handoff is opt-in, not mandatory
4. **Hierarchy is optional** — Parent mode is a feature, not a requirement
5. **Conversational by default** — Commands prompt for missing options, but flags still work
6. **Single source of truth** — PROTEXT.md is the primary artifact, config is secondary
7. **No magic** — Predictable, transparent, controllable

---

## Related Documents

- `SKILL.md` — Current protext specification
- `references/formats.md` — Format specs for all protext files
- `references/commands.md` — Command reference with syntax and examples
- `TODO.md` — Issue tracking for all projects
- `CLAUDE.md` — Root project instructions

---

---

## Status

**Current State:** Design validated, ready for implementation
**Last Updated:** 2026-02-10
**Approved By:** User (all key design decisions finalized)
**Next Step:** Begin Phase 1 (Markers & Handoff Redesign)

### Implementation Priority

**High confidence, proceed immediately:**
- Phase 1: Markers & handoff redesign
- Phase 2: Extended link types
- Phase 3: Parent protext (core feature)

**Lower priority, polish phase:**
- Phase 4: Conversational interface (UX enhancement, not blocking)
