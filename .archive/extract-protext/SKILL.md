---
name: extract-protext
description: Scans the current project state to extract and distill high-level, up-to-the-minute 'Protext' (Project Context) into persistent artifacts for UI/UX and Backend. Use this to rectify context files before difficult tasks.
---

# Extract Protext

## Purpose

To create or update the single-source-of-truth "Protext" files that serve as specific context injectors. This skill ensures the agent (you) has a distilled, high-signal summary of the project's *current reality*—architecture, design tokens, stack decisions, and recent refactors.

## Usage

Run this skill whenever:

1. Significant architectural changes have occurred.
2. You are about to start a complex session and want to ensure your context is "fresh".
3. The user explicitly triggers "extract protext".

## Instructions

### 1. Analysis Phase

Perform a deep but targeted scan of the project to gather "up to the minute" details.

* **Structure:** List root directories and key configuration files (`package.json`, `bun.lockb`, `vite.config.js`, etc.).
* **Tech Stack:** Identify frameworks (Svelte 5? React?), runtimes (Bun? Node?), and key libraries (Tailwind? Ark UI? None?).
* **Design System:** Locate design tokens (CSS variables), styling philosophy (Brutalist? Glassmorphism?), and component patterns.
* **Backend:** Identify server entry points, database schema (SQLite? Postgres?), API routes, and auth mechanisms.
* **Recent Changes:** Briefly check `findings.md`, `task_plan.md` or git history to spot "recent refactors" (e.g., "Removed Ark UI").

### 2. Protext Generation (Table Format Mandated)

Generate the following files in `.protext/` using **Markdown Tables** (`| Descriptor | Value |`) for maximum information density.

#### A. `ui-ux.md`

* **Stack:** Framework, Build, Styles.
* **Design System:** Radius, Shadows, Typography, Scale.
* **Component Architecture:** Molecules/Atoms.
* **Critical Rules:** A11y, Performance constraints.
* **Token Cheat-Sheet:** CSS Variables.

#### B. `backend.md`

* **Stack:** Runtime, Database, Server.
* **Schema:** Tables.
* **API:** Endpoints.
* **Auth:** Strategy.

#### C. `architecture.md` (System Patterns)

* **Meta:** App Type (SPA/MPA), Rendering (CSR/SSR).
* **Patterns:** State Management (Store/Signals), Data Flow.
* **Decisions:** Key architectural choices (e.g., "Polymorphic Components").

#### D. `devops.md` (Operations)

* **Build:** Bundlers (Vite/Bun), Commands.
* **Deploy:** Config, Ports, Static Files.
* **Security:** Headers, CORS, Rate Limiting.
* **Env:** Variable Schema.

### 3. Execution

1. Ensure `.protext/` directory exists.
2. Write the files.
3. Notify the user that Protext has been extracted and rectified.

## Example output structure (`.protext/architecture.md`)

```markdown
# Architecture Protext

## Meta
| Descriptor | Value |
| :--- | :--- |
| App Type | SPA |
| Rendering | CSR |

## Patterns
| Pattern | Implementation |
| :--- | :--- |
| State | Singleton Store (`store.svelte.js`) |
| Auth | Hybrid Cookie/Fingerprint |
```
