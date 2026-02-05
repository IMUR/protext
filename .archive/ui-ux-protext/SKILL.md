---
name: ui-ux-protext
description: Injects high-signal, project-specific UI/UX context into the current session. Use this to reinforcing your prompts with distilled design systems, component patterns, and stack rules.
---

# UI/UX Protext Injection

## Purpose

To instantly load the "Protext" (Project Context) for UI/UX work, ensuring the agent aligns with the project's established design system and frontend architecture without needing a full file exploration.

## Trigger

Use this skill when:

* The user asks to "reinforce with ui protext".
* You are starting a frontend task and want to ensure adherence to standards (e.g. "Svelte 5 Runes").
* You need to recall specific CSS variables or component patterns.

## Instructions

1. **Check for Source:** Look for `.protext/ui-ux.md` in the project root.
2. **Missing Source Handler:**
    * If the file does not exist, STOP and recommend running `extract-protext` first.
    * *Optional:* If authorized, run `extract-protext` automatically.
3. **Read & Absorb:**
    * Read the content of `.protext/ui-ux.md`.
    * Adopt the constraints found therein (e.g., "Do not use Ark UI").
    * Load the CSS variables and Design Tokens into your "working memory".
4. **Confirmation:**
    * Acknowledge context load: "UI/UX Protext loaded. Aligned to [Design System Name] and [Stack Version]."

## Output

Do not output the full text of the file unless asked. Simply confirm alignment and proceed with the user's request using this sharpened context.
