---
name: backend-protext
description: Injects high-signal, project-specific Backend context into the current session. Use this to reinforce your prompts with database schemas, API contracts, and server architecture.
---

# Backend Protext Injection

## Purpose

To instantly load the "Protext" (Project Context) for Backend work, ensuring the agent understands the data model, authentication flow, and server capabilities.

## Trigger

Use this skill when:

* The user asks to "reinforce with backend protext".
* You are starting a backend task (API endpoint, DB migration).
* You need to verify data relationships or auth constraints.

## Instructions

1. **Check for Source:** Look for `.protext/backend.md` in the project root.
2. **Missing Source Handler:**
    * If the file does not exist, STOP and recommend running `extract-protext` first.
    * *Optional:* If authorized, run `extract-protext` automatically.
3. **Read & Absorb:**
    * Read the content of `.protext/backend.md`.
    * Internalize the Schema definitions.
    * Note server entry points and router logic.
4. **Confirmation:**
    * Acknowledge context load: "Backend Protext loaded. Aligned to [Database Type] and [Server Runtime]."

## Output

Do not output the full text of the file unless asked. Simply confirm alignment and proceed with the user's request.
