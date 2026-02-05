# Protext: Protext Dev

> Generated: 2026-02-05 | Scope: dev | Tokens: ~400

## Identity

Context management skill for AI agents. Three-layer hierarchy (orientation → index → deep context) with user-invoked `/protext` injection, scopes, handoff, and token budgets.

## Current State

Active: v2 initial build | Blocked: None | Recent: Skill created, validated, tested on crtr-config

## Hot Context

- Skill source lives here; deployed copy at `~/.agent/skills/local/protext/`
- Validate with: `python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py .`
- v1 archive in `.archive/` — 5 domain-specific injectors (superseded)
- Primary UX: `/protext` slash command for cross-platform injection
- Key limits: 5 scopes, 20 extractions, 2000 token budget, 48h handoff TTL

## Scope Signals

- `@dev` → .protext/scopes/dev.md
- `@ops` → .protext/scopes/ops.md
- `@deep:design` → docs/DESIGN.md

## Handoff

Last: v2 skill built and validated | Next: Iterate based on real usage, refine init script project name extraction | Caution: First real deployment — expect rough edges
