# Protext Skill Evaluation

> Date: 2026-02-10 | Evaluator: Antigravity | Version Assessed: v2.2

---

## Executive Summary

Protext is in a **mature, production-deployed state**. It has evolved through 4 well-documented versions (v1 → v2 → v2.1 → v2.2) and has a real-world deployment across the `configs/` cluster hierarchy (parent + 5 children + 1 peer). The skill spec is solid, the scripts work, and there is a clear next-features roadmap. Minor hygiene issues remain — stale references to deprecated behavior and a stub function — but nothing that blocks usage.

**Overall Grade: A-**

---

## 1. Skill Architecture — A

The three-layer hierarchy (L0 → L1 → L2) is clean and well-reasoned:

```
PROTEXT.md (L0)  →  .protext/index.yaml (L1)  →  Deep Context (L2)
     ~500 tokens          Signposts only             Full docs/memory
     Always loaded        On-demand hints             Explicit extraction
```

Key architectural decisions:

- **CLAUDE.md / PROTEXT.md separation** — Behavior (stable) vs state (dynamic) in distinct files with different update frequencies.
- **Suggest-mode extraction** — Agents are aware of available context but don't auto-load, preserving token budget.
- **Zero auto-execution** — No protext operation runs without explicit user request.
- **HTML comment markers** — Machine-readable section delimiters invisible to humans, enabling parent aggregation.
- **One-level hierarchy** — Parent → children only, no multi-level nesting. Simple, sufficient.
- **4 link types with spatial validation** — child/parent/sibling/peer with regex pattern enforcement.

All of these are documented in `docs/DESIGN.md` with ADR-style decision records including alternatives considered and rationale.

---

## 2. Documentation Quality — A-

The documentation suite is thorough and internally consistent:

| File | Lines | Role | Quality |
|------|-------|------|---------|
| `SKILL.md` | 376 | Main skill spec | ✅ Comprehensive, well-structured |
| `references/commands.md` | 872 | Command reference | ✅ Extremely detailed with examples |
| `references/formats.md` | 578 | Format templates with markers | ✅ Complete, includes parent mode |
| `docs/DESIGN.md` | 126 | Decision log (13 entries) | ✅ Good ADR-style lineage |
| `CLAUDE.md` | 98 | Dev project context | ✅ Clear project orientation |
| `README.md` | 111 | Install & usage guide | ✅ Concise, functional |
| `NEXT-FEATURES.md` | 541 | Roadmap & design decisions | ✅ Detailed, design-finalized |

### Inconsistencies Found

1. **Quick Reference Card stale** — `commands.md:869` shows `HANDOFF FRESH <24h | AGING 24-48h | STALE >48h`. This was deprecated in v2.1 (user-initiated handoff, no TTL enforcement).

2. **formats.md stale handoff description** — `formats.md:346` says handoff.md "Auto-stales after 48h." This directly contradicts the v2.1 handoff redesign which made handoff user-initiated only with no TTL enforcement. The behavior section at `formats.md:373-378` contradicts its own header.

3. **NEXT-FEATURES.md internal contradiction** — Line 230 says "Total: 4 relationship types (reduced from 7 in v2.1, simplified in v2.2)" but Phase 2 at line 390 still describes 7 types as the target. The phases should reflect that they're already done.

4. **NEXT-FEATURES.md status is stale** — Line 527 says "Design validated, ready for implementation" and "Next Step: Begin Phase 1". In reality, Phases 1–3 are fully implemented and deployed. The document hasn't been updated to reflect completion.

---

## 3. Script Implementation — B+

| Script | Lines | Status | Notes |
|--------|-------|--------|-------|
| `init_protext.py` | 820 | ✅ Full | 25 functions. Standard/parent/existing modes, markers, spatial validation, child discovery |
| `protext_status.py` | 328 | ✅ Full | 15 functions. ANSI output, YAML fallback parser, tier detection |
| `protext_refresh.py` | 137 | ⚠️ Partial | 6 functions. Parent refresh works; `refresh_standard` is a stub |

### Issues

1. **`refresh_standard` is a stub** — `protext_refresh.py:92-96` contains:

   ```python
   def refresh_standard(project_path: Path) -> bool:
       """Standard refresh: update timestamp and regenerate based on current state."""
       print("Standard refresh not yet implemented")
       print("For now, use 'protext init --existing update' to regenerate PROTEXT.md")
       return False
   ```

   The `protext refresh` command (non-parent variant) is documented in `commands.md:785-816` but doesn't actually work. The documented workaround (`--existing update`) exists but isn't surfaced to users in the error message clearly.

2. **Import coupling** — `protext_refresh.py` imports from `init_protext` via bare module name (`from init_protext import ...`). This works only when both scripts are in the same directory. Not a problem for current usage but fragile for alternative packaging.

3. **Zero external dependencies** — All scripts use stdlib only (argparse, pathlib, datetime, re, shutil). YAML is parsed with a custom fallback when PyYAML isn't available. This is a genuine strength.

---

## 4. Real-World Deployment — A-

Protext is deployed across the configs/ cluster hierarchy, audited by the main Claude session:

```
configs/ (parent)
├── crtr-config (child) — edge services / ingress (192.168.254.10)
├── drtr-config (child) — ML/inference compute (192.168.254.124)
├── trtr-config (child) — macOS admin console (192.168.254.134)
├── prtr-config (child) — multi-GPU compute (192.168.254.20)
├── brtr-config (child) — ESP32-S3 power control (btr.ism.la)
└── dotfiles (peer)     — Chezmoi-managed cluster dotfiles
```

Additionally, dotfiles has 3 peer links back to crtr/drtr/trtr-config.

### Audit Scorecard (from main session)

| Category | Grade | Notes |
|----------|-------|-------|
| Marker integrity | A | All 30 marker pairs intact |
| Token budget | A | All files 311–558 tokens |
| Parent/child hierarchy | A- | Correct structure, missing reciprocal parent links |
| Sibling mesh | A | Complete bilateral mesh for 3 cluster nodes |
| Link spatial validity | A | All paths match declared type patterns |
| Path consistency | B- | Mixed absolute/relative paths for dotfiles |
| Config consistency | B | Minor variations in legacy fields and ignore patterns |
| Content quality | A | Genuinely useful, project-specific content |
| **Overall** | **A-** | Solid real-world deployment with minor consistency gaps |

### Deployment Notes

- `rrtr-config/` exists in configs/ as an empty directory with no PROTEXT.md. Parent handoff correctly notes "rrtr-config not linked." Handled properly.
- `brtr-config` was added as the 5th child. With dotfiles as a peer, configs/ has 6 total links (5 child + 1 peer). Child links are unlimited; the lateral link cap (5) applies to peer/sibling/reference only — configs/ is within limits.
- Children lack reciprocal `.. → parent` links back to configs/. The spec supports it but it wasn't done during deployment.

---

## 5. Dev Repo vs Installed Skill — A

The installed skill at `.agent/skills/protext/` contains:

```
.agent/skills/protext/
├── .gitignore
├── .skillignore
├── README.md
├── SKILL.md          ← matches dev repo
├── references/
│   ├── commands.md   ← matches dev repo
│   └── formats.md    ← matches dev repo
└── scripts/
    ├── init_protext.py      ← matches dev repo
    ├── protext_refresh.py   ← matches dev repo
    └── protext_status.py    ← matches dev repo
```

The `.skillignore` correctly excludes dev-only files: `docs/`, `CLAUDE.md`, `NEXT-FEATURES.md`, `.archive/`, `.protext/`.

---

## 6. Knowledge Items — Stale

### Antigravity KI (`antigravity_agent_skills/artifacts/implementation/protext.md`)

This KI describes **v2.0** state. It is missing:

- HTML comment markers (v2.1)
- Parent protext mode (v2.1)
- Cross-project links (v2.1)
- Spatial validation (v2.2)
- `protext_refresh.py` script (v2.1)
- User-initiated handoff redesign (v2.1)
- 4-type link system (v2.2)

Still references 48h TTL handoff as active behavior.

### SuggestionBox KI (`protext_methodology.md` + `protext_implementation_details.md`)

These describe **v1** architecture — domain-specific injectors (`ui-ux-protext`, `backend-protext`, `extract-protext`), sidecar patterns, table-driven high density. This was the original concept that evolved into the unified protext system. Archaeological value only — potentially misleading if read by an agent without v2 context.

---

## 7. Roadmap vs Current State

`NEXT-FEATURES.md` defines 4 phases. Implementation status:

| Phase | Feature | Status | Evidence |
|-------|---------|--------|----------|
| **1** | Machine-readable markers | ✅ Done | In `formats.md` templates, `init_protext.py` generates them, deployed in configs/ |
| **1** | Handoff redesign (user-initiated) | ✅ Done | `SKILL.md` and `commands.md` updated, `DESIGN.md` entry 6 deprecated |
| **2** | Extended link types | ✅ Done (then simplified) | v2.1 had 7 types, v2.2 reduced to 4 with spatial validation |
| **3** | Parent protext | ✅ Done | `init_protext.py --parent`, `protext_refresh.py --children`, deployed at configs/ |
| **3** | Bidirectional awareness | ⚠️ Partial | Config schema has `parent:` field, but children don't auto-link back. Audit notes "missing reciprocal parent links" |
| **4** | Conversational command interface | ❌ Not started | Described in NEXT-FEATURES.md but no implementation in SKILL.md or scripts |

---

## 8. Action Items

### High Priority

1. **Fix Quick Reference Card** — `commands.md:869`: Remove deprecated TTL handoff states from the card
2. **Fix handoff.md header** — `formats.md:346`: Change "Auto-stales after 48h" to match user-initiated behavior described in its own Behavior section
3. **Implement `refresh_standard`** — The documented `protext refresh` (non-parent) command is a stub

### Medium Priority

1. **Update NEXT-FEATURES.md status** — Reflect that Phases 1–3 are done; Phase 4 is the only remaining work
2. **Update Antigravity KI** — The protext artifact is stuck at v2.0, missing all v2.1/v2.2 features
3. **Add reciprocal parent links** — Children in configs/ should have `.. → parent` links back to the parent

### Low Priority

1. ~~**Address link budget**~~ — **Resolved (2026-02-20):** Child links now unlimited; lateral links capped at 5. configs/ (5 child + 1 peer) is within limits.
2. **Clean internal contradictions** — NEXT-FEATURES.md Phase 2 still describes 7 types (line 390) vs 4 types (line 230)
3. **SuggestionBox KI** — v1 architecture descriptions are harmless but could confuse agents

---

## 9. Post-Evaluation Fixes (2026-02-20)

Following this evaluation, a skill audit session on crtr identified and resolved additional issues:

| Fix | Detail |
|-----|--------|
| Code fence language | 8 command blocks changed `bash` → `text` in SKILL.md (both dev + deployed). Confirmed root cause: Antigravity tried to exec `~/.gemini/antigravity/skills/protext/bin/protext` |
| Link constraint split | "Max links: 5" split into "Max lateral links: 5 / Max child links: Unlimited" in SKILL.md, CLAUDE.md |
| Relative path guidance | Added explicit note to `protext link` section: prefer relative paths for cross-node portability |
| EVALUATION.md accuracy | Fixed "4 children" → "5 children", added prtr-config to diagram, updated link budget note |

See `docs/sessions/crtr-protext.md` for full session log.

---

## 10. Version Lineage

| Version | Date | Key Changes |
|---------|------|-------------|
| **v1** | Jan 2025 | Domain-specific injectors (ui-ux, backend, architecture, devops) |
| **v2** | Feb 2025 | Unified three-layer hierarchy, scopes, handoff protocol, /protext command |
| **v2.1** | Feb 2026 | HTML markers, parent protext, 7 link types, user-initiated handoff, zero auto-execution |
| **v2.2** | Feb 2026 | Reduced to 4 link types, spatial validation, hierarchy merged into Links section |

---

## 11. Summary Scorecard

| Dimension | Grade | Notes |
|-----------|-------|-------|
| Architecture & Design | **A** | Clean three-layer model, well-reasoned constraints |
| Documentation | **A-** | Thorough, minor stale references to deprecated TTL |
| Script Implementation | **B+** | 2 of 3 scripts complete; 1 has a stub function |
| Real-World Deployment | **A-** | 6 projects, validated parent/child/peer model |
| Dev/Install Sync | **A** | Packaged files match; .skillignore correct |
| Knowledge Items | **C+** | KI artifacts stuck at v2.0 / v1 |
| Roadmap Execution | **B+** | 3 of 4 phases complete |
| **Overall** | **A-** | Mature skill with minor hygiene gaps |
