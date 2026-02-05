---
name: architecture-protext
description: Injects high-level Architecture context (Patterns, Flows, Decisions) into the session. reinforced by ARCHITECTURE.md scaffolding.
---

# Architecture Protext Injection

## Purpose

To load the high-level system design, patterns, and architectural decisions. This provides the "Zoomed Out" view of the project, ensuring alignment with the core metaphors (Molecule/Atom) and data flows.

## Trigger

Use when:

* Refactoring core logic.
* Making decisions about state management.
* Integrating new major features.
* User asks for "architecture context".

## Instructions

1. Read `.protext/architecture.md`.
2. If missing, run `extract-protext`.
3. Absorb:
    * Application Metaphors (e.g. "Molecule/Atom").
    * Data Flow patterns (Singleton Store? Signals?).
    * State Management strategy.

## Output

Confirm context load: "Architecture Protext loaded. Aligned to [Pattern Name] and [State Strategy]."
