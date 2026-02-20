# Protext Design Decisions

Record of architectural decisions made during Protext development.

---

## Decision Log

### 1. Three-Layer Hierarchy over Monolith

**Decision:** PROTEXT.md (L0) → index.yaml (L1) → Deep Context (L2)
**Alternatives:** Single file, Two-layer
**Rationale:** Maps to cognitive "orient → find → dive" pattern. Each layer has distinct update frequency and token cost.

### 2. PROTEXT.md Separate from CLAUDE.md

**Decision:** Behavior (CLAUDE.md) and state (PROTEXT.md) are distinct files.
**Alternatives:** Merge into CLAUDE.md, Replace CLAUDE.md
**Rationale:** Different update frequencies. CLAUDE.md is stable (rules), PROTEXT.md is dynamic (session state). Reduces maintenance burden on both.

### 3. Suggest-Mode Extraction Default

**Decision:** Agents see "context available" hints but don't auto-load.
**Alternatives:** Auto-load on keyword trigger, Always require confirmation
**Rationale:** Balances discoverability with token cost control. User stays in control.

### 4. Hybrid Trigger System

**Decision:** Explicit (@scope) > keyword hints > agent request
**Alternatives:** Pure keyword matching, Pure explicit only
**Rationale:** Keywords alone are brittle (false positives). Explicit alone lacks discoverability. Hybrid provides reliability with progressive disclosure.

### 5. Max 5 Scopes, 5 Lateral Links, 20 Extractions **[updated v2.2]**

**Decision:** Hard limits on scopes and lateral links; child links unlimited.
**Alternatives:** Unlimited all, Lower limits (3/10), Hard limit on all links
**Rationale:** Scopes must be orthogonal — 5 prevents fragmentation. Lateral links (peer/sibling/reference) are editorial choices so 5 keeps orientation concise. Child links are structural — a parent project can't be told to have fewer children than it actually has. Extractions at 20 keeps the index scannable.

### 6. ~~48h Handoff TTL~~ **[DEPRECATED in v2.1]**

~~**Decision:** FRESH (<24h) → AGING (24-48h) → STALE (>48h)~~
~~**Alternatives:** No TTL, 24h TTL, 72h TTL~~
~~**Rationale:** 48h balances freshness with weekend coverage. Three states give graduated trust levels.~~

**Revised (v2.1 - Feb 2026):** User-initiated handoff only, no TTL enforcement.
**Rationale:** TTL warnings were noise for projects with long gaps between sessions. Handoff is now an optional scratchpad, not mandatory protocol. Zero auto-execution principle.

### 7. User-Invoked `/protext` as Primary Entry

**Decision:** User triggers context injection via slash command, not auto-loaded.
**Alternatives:** Auto-inject on session start, Hook-based injection
**Rationale:** Maximum cross-platform compatibility. Works as slash command or natural language on any AI platform.

### 8. Advanced Tier as Default

**Decision:** New projects get full features (scopes, extractions, handoff).
**Alternatives:** Beginner default with opt-in, Intermediate default
**Rationale:** User preference. Power users want full capability immediately. Simpler tiers remain available for lightweight use cases.

### 9. HTML Comment Markers for Aggregation **[v2.1]**

**Decision:** Wrap sections in `<!-- marker:name -->content<!-- /marker:name -->`
**Alternatives:** YAML front-matter per section, Custom fence syntax, No markers
**Rationale:** Invisible to humans, parseable by parent aggregation, standard markdown syntax. Enables parent protext without breaking existing projects. Fallback to heading-based parsing for backward compatibility.

### 10. One-Level Hierarchy for Parent Protext **[v2.1]**

**Decision:** Parent → children only, no multi-level nesting
**Alternatives:** Unlimited depth, Two-level (grandparent → parent → children)
**Rationale:** Avoids recursion complexity, simpler mental model, sufficient for 99% of use cases. Can be extended later if genuine need emerges.

### 11. Zero Auto-Execution Principle **[v2.1]**

**Decision:** No protext operation executes without explicit user request
**Alternatives:** Auto-refresh parent on load, Smart suggestions that auto-trigger
**Rationale:** Predictable behavior, no surprise token costs, transparent operations. Parent never auto-refreshes — user runs `protext refresh --children` explicitly.

### 12. Child Status via Modification Time **[v2.1]**

**Decision:** Active (<7 days), Idle (≥7 days), Stale (no PROTEXT.md)
**Alternatives:** Manual status tags, Presence of handoff, Explicit config field
**Rationale:** Automatic, no manual maintenance, simple implementation. 7-day window matches typical sprint/iteration cycles.

### 14. Command Block Fences: `text` not `bash` **[v2.2]**

**Decision:** Conversational command examples use `text` code fences, not `bash`.
**Alternatives:** `bash` fences, no language tag, prose-only
**Rationale:** On Gemini Antigravity and similar platforms, agents seeing a `bash` fence treat the content as a shell command and attempt to execute it. Confirmed in production: Antigravity tried to execute `~/.gemini/antigravity/skills/protext/bin/protext` after seeing `protext` in a `bash` block in SKILL.md. `text` fences are visually identical for humans but signal non-executable content to agents.

### 15. Relative Paths Preferred in Links **[v2.2]**

**Decision:** Link paths should use relative notation (`../sibling`, `./child`) over absolute paths.
**Alternatives:** Absolute paths only, No preference stated
**Rationale:** Absolute paths break on nodes with different mount prefixes (e.g., `/mnt/ops/` on Linux vs `/Volumes/ops/` on macOS trtr). Relative paths are portable across all nodes and OS environments. Confirmed issue in real deployment: PROTEXT.md links written on Linux with `/mnt/ops/configs/trtr-config` failed to resolve on macOS trtr.

### 13. Link Validation with Spatial Constraints **[v2.2]**

**Decision:** Reduce to 4 types (child/parent/sibling/peer) with path pattern validation
**Alternatives:** Keep 7 types, No validation, Manual review only
**Rationale:**
- Dependency/consumer/reference were ambiguous and redundant with peer
- Path patterns make relationships verifiable (child must be ./name, not ../foo)
- Prevents logical errors (can't claim ../sibling is a "child")
- Only child aggregates (ownership follows hierarchy, not association)
- Sibling is strictly lateral (../name only, not ../parent/cousin)
- Hierarchy lives in Links section, not config.yaml (single source of truth)

---

## Lineage

**v1 (Jan 2025):** Domain-specific injectors
- Individual skills per domain (backend, ui-ux, architecture, devops)
- Separate extraction skill to generate context files
- Problem: Fragmented, no unified orientation, no handoff

**v2 (Feb 2025):** Unified Protext system
- Single skill with three-layer hierarchy
- Scopes replace domain-specific skills
- Built-in handoff protocol
- User-invoked `/protext` command
- Token budgets and extraction controls

**v2.1 (Feb 2026):** Parent protext & refinements
- HTML comment markers for machine-readable sections
- Parent protext mode (hierarchical aggregation)
- Cross-project links (7 relationship types)
- User-initiated handoff only (no TTL enforcement)
- Zero auto-execution principle
- Backward-compatible marker extraction

**v2.2 (Feb 2026):** Link validation & spatial constraints
- Reduced link types from 7 to 4 (removed dependency/consumer/reference)
- Path pattern validation (child=./name, sibling=../name, parent=../, peer=any)
- Merged hierarchy into Links (removed config.yaml children field)
- Only child links aggregate status
- Spatial relationships enforce filesystem structure
