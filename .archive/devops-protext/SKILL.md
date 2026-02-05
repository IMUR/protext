---
name: devops-protext
description: Injects DevOps context (Build, Deploy, Infrastructure, Env) into the session.
---

# DevOps Protext Injection

## Purpose

To load the operational context: how the app is built, served, and configured. Essential for debugging build issues, server config, or environment variable management.

## Trigger

Use when:

* Modifying `package.json`, `vite.config.js`, or `Dockerfile`.
* Debugging build failures.
* Changing server ports or environment variables.

## Instructions

1. Read `.protext/devops.md`.
2. If missing, run `extract-protext`.
3. Absorb:
    * Build commands.
    * Environment Variable schema.
    * Port allocations.
    * Deployment constraints (e.g. "Bun only").

## Output

Confirm context load: "DevOps Protext loaded. Aligned to [Build Tool] and [Deploy Target]."
