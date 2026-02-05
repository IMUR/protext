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

### 5. Max 5 Scopes, 20 Extractions

**Decision:** Hard limits on both.
**Alternatives:** Unlimited, Lower limits (3/10)
**Rationale:** Prevents complexity explosion while allowing real project needs. Scopes must be orthogonal.

### 6. 48h Handoff TTL

**Decision:** FRESH (<24h) → AGING (24-48h) → STALE (>48h)
**Alternatives:** No TTL, 24h TTL, 72h TTL
**Rationale:** 48h balances freshness with weekend coverage. Three states give graduated trust levels.

### 7. User-Invoked `/protext` as Primary Entry

**Decision:** User triggers context injection via slash command, not auto-loaded.
**Alternatives:** Auto-inject on session start, Hook-based injection
**Rationale:** Maximum cross-platform compatibility. Works as slash command or natural language on any AI platform.

### 8. Advanced Tier as Default

**Decision:** New projects get full features (scopes, extractions, handoff).
**Alternatives:** Beginner default with opt-in, Intermediate default
**Rationale:** User preference. Power users want full capability immediately. Simpler tiers remain available for lightweight use cases.

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
