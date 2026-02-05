# Cross-Platform Skills Checklist

Comprehensive checklist for building portable, cross-compatible AI agent skills based on the SKILL.md open standard (Anthropic, Dec 2025) and platform-specific conventions.

---

## Table of Contents

1. [Platform Compatibility Matrix](#platform-compatibility-matrix)
2. [SKILL.md Core Checklist](#skillmd-core-checklist)
3. [File Structure Checklist](#file-structure-checklist)
4. [Frontmatter & Metadata](#frontmatter--metadata)
5. [Trigger & Discovery](#trigger--discovery)
6. [Context Injection & Token Efficiency](#context-injection--token-efficiency)
7. [Progressive Disclosure](#progressive-disclosure)
8. [Cross-Platform Portability](#cross-platform-portability)
9. [Platform-Specific Conventions](#platform-specific-conventions)
10. [Testing & Validation](#testing--validation)
11. [Gotchas & Incompatibilities](#gotchas--incompatibilities)

---

## Platform Compatibility Matrix

| Platform | Skills Format | Trigger Mechanism | Custom Commands | Rules File |
|----------|--------------|-------------------|-----------------|------------|
| **Claude Code** | SKILL.md (native) | Auto-detect + `/slash` | Yes | CLAUDE.md |
| **Cursor** | SKILL.md (adopted) | Auto-detect + `@ref` | `.cursor/rules/` | .cursorrules |
| **GitHub Copilot** | SKILL.md (adopted) | Auto-detect | Extensions | .github/copilot-instructions.md |
| **Continue.dev** | config.json | `/slash` commands | Yes (JSON) | .continue/config.json |
| **Cline** | .clinerules | Auto-read on init | Memory bank keys | .clinerules |
| **Windsurf** | .windsurfrules | Auto-load on session | Workspace rules | .windsurfrules |
| **Aider** | CONVENTIONS.md | Auto-load on start | CLI flags | .aider.conf.yml |
| **Roo Code** | .roo/rules/ | `/mode` activation | Mode-specific | .roo/rules/*.md |

**Standard adoption status:**
- **Native SKILL.md**: Claude Code
- **Adopted SKILL.md**: Cursor, GitHub Copilot, Pulumi ecosystem
- **Own convention (compatible patterns)**: Continue.dev, Cline, Windsurf, Aider, Roo Code

---

## SKILL.md Core Checklist

### Required

- [ ] `SKILL.md` file exists at skill root (case-sensitive, exact name)
- [ ] YAML frontmatter present with opening and closing `---`
- [ ] `name` field: hyphen-case, lowercase, max 64 chars, no leading/trailing hyphens
- [ ] `description` field: max 1024 chars, no angle brackets (`<` or `>`)
- [ ] Description includes BOTH what the skill does AND when to use it
- [ ] Body contains actionable instructions in imperative form
- [ ] Body is under 500 lines (prevents context bloat)

### Frontmatter Schema

```yaml
---
name: skill-name                    # Required: hyphen-case identifier
description: >                      # Required: trigger text + purpose
  What it does and when to use it.
  Include specific trigger scenarios.
allowed-tools: [Bash, Read, Write]  # Optional: restrict tool access
metadata:                           # Optional: custom key-value pairs
  version: "2.0"
  author: "team"
---
```

**Allowed frontmatter fields:** `name`, `description`, `license`, `allowed-tools`, `metadata`

### Body Quality

- [ ] Opens with a concise purpose statement (1-2 lines)
- [ ] Uses imperative form ("Run tests" not "Running tests")
- [ ] Includes concrete examples, not just abstract instructions
- [ ] Avoids explaining things the model already knows
- [ ] Each paragraph justifies its token cost
- [ ] No README, CHANGELOG, or auxiliary docs created alongside

---

## File Structure Checklist

### Standard Layout

```
skill-name/
├── SKILL.md              # Required: definition + instructions
├── scripts/              # Optional: executable code
│   └── *.py, *.sh        # Deterministic, reusable operations
├── references/           # Optional: loaded into context as needed
│   └── *.md              # Domain docs, schemas, examples
└── assets/               # Optional: NOT loaded into context
    └── templates, images # Used in output, not read by agent
```

- [ ] Skill directory name matches `name` in frontmatter
- [ ] Only SKILL.md, scripts/, references/, assets/ present (no extras)
- [ ] No README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, or auxiliary docs
- [ ] Scripts are executable (`chmod +x`)
- [ ] Scripts tested by actually running them
- [ ] References are one level deep from SKILL.md (no nested references)
- [ ] References over 100 lines include table of contents
- [ ] All paths use forward slashes (`/`), never backslashes
- [ ] All paths are relative to skill root

---

## Frontmatter & Metadata

### Description Best Practices

- [ ] Description is the PRIMARY trigger mechanism (always in context)
- [ ] Includes numbered use cases: "(1) When X, (2) When Y, (3) When Z"
- [ ] Covers both positive triggers (when to use) and implicit scope
- [ ] All "when to use" info is in description, NOT in the body
- [ ] Under 1024 characters
- [ ] No angle brackets (breaks YAML parsing on some platforms)

### Example (Good)

```yaml
description: Dynamic context management for AI agents. Invoke /protext at
  session start to load token-efficient project orientation. Use when
  (1) Starting a session and need quick orientation, (2) Handing off
  between sessions, (3) Managing multi-scope projects (dev/ops/security).
```

### Example (Bad)

```yaml
description: A context management tool.  # Too vague, won't trigger
```

---

## Trigger & Discovery

### Cross-Platform Trigger Compatibility

| Trigger Type | Claude Code | Cursor | Copilot | Continue | Cline |
|-------------|-------------|--------|---------|----------|-------|
| Auto-detect (description match) | Yes | Yes | Yes | No | No |
| Slash command (`/skill`) | Yes | No | No | Yes | No |
| Natural language | Yes | Yes | Yes | Yes | Yes |
| Keyword in conversation | Yes | Yes | Yes | Partial | Partial |
| Manual invocation | Yes | Yes | Yes | Yes | Yes |

### Checklist

- [ ] Description contains enough keywords for auto-detection
- [ ] Skill works when invoked via natural language (most portable)
- [ ] Slash command defined for platforms that support it
- [ ] Body does NOT rely on slash commands as only trigger
- [ ] Natural language alternatives documented for each command
- [ ] Skill gracefully handles being triggered in wrong context

---

## Context Injection & Token Efficiency

### Token Budget Guidelines

| Component | Target | Max | Notes |
|-----------|--------|-----|-------|
| Frontmatter (always loaded) | ~100 tokens | 200 | Triggers skill detection |
| SKILL.md body (on trigger) | ~2000 tokens | 5000 | Core instructions |
| Single reference file | ~500 tokens | 2000 | Loaded as needed |
| Total skill footprint | ~3000 tokens | 8000 | All loaded content |

### Checklist

- [ ] Challenge each piece: "Does the model really need this?"
- [ ] Assume model capabilities — don't explain common knowledge
- [ ] Prefer concise examples over verbose explanations
- [ ] Use few-shot patterns (input → output pairs) for clarity
- [ ] Structure outputs strictly for APIs/data; flexibly for creative tasks
- [ ] Avoid excessive options ("use pypdf or pdfplumber" → pick one)
- [ ] List dependencies explicitly; don't assume availability
- [ ] Embed conversation-relevant context, not encyclopedic content

---

## Progressive Disclosure

### Three-Level Loading

```
Level 1: Frontmatter (always)  →  ~100 tokens  →  Triggers relevance check
Level 2: SKILL.md body (on trigger)  →  ~2000 tokens  →  Core instructions
Level 3: References/scripts (as needed)  →  Unlimited  →  Deep context
```

### Checklist

- [ ] Frontmatter alone is sufficient to decide relevance
- [ ] Body is self-contained for common use cases
- [ ] References clearly named and described in body
- [ ] Body tells agent WHEN to read each reference file
- [ ] Large references (>100 lines) include grep-friendly headings
- [ ] Scripts can execute without being read into context
- [ ] Assets are never loaded into context (templates, images, fonts)

### Pattern: High-Level Guide with References

```markdown
## Processing
Use the standard workflow for common cases.

**Advanced features:**
- Form handling: See [references/forms.md](references/forms.md)
- API details: See [references/api.md](references/api.md)
```

### Pattern: Conditional Loading

```markdown
**Creating new content?** → Follow creation workflow below
**Editing existing?** → See [references/editing.md](references/editing.md)
```

---

## Cross-Platform Portability

### Universal Compatibility Rules

- [ ] Use Markdown for all instruction content (every platform supports it)
- [ ] Use forward slashes (`/`) for all paths (Windows backslash breaks)
- [ ] Use relative paths from skill root (absolute paths are non-portable)
- [ ] List ALL dependencies explicitly (no assumed packages)
- [ ] Provide defaults with fallbacks: "Use X; if unavailable, do Y manually"
- [ ] Test with weaker models — what works for Haiku degrades gracefully on Opus
- [ ] Don't rely on platform-specific features as the only path
- [ ] Include natural language invocation as primary trigger (most portable)

### Graceful Degradation Strategy

```
Full support (Claude Code):
  SKILL.md → auto-triggers → scripts execute → references load

Partial support (Cursor, Copilot):
  SKILL.md → description-based discovery → manual reference loading

Minimal support (Aider, Cline):
  SKILL.md body read as instructions → manual workflow
```

- [ ] Skill provides value even if only SKILL.md body is read
- [ ] Scripts have clear manual equivalents documented
- [ ] No hard dependency on auto-detection or slash commands
- [ ] Works as a standalone Markdown document at minimum

### Companion Files for Multi-Platform

For maximum reach, consider generating platform-specific companions:

| Platform | Companion File | Derivable From |
|----------|---------------|----------------|
| Cursor | `.cursorrules` | SKILL.md body (subset) |
| Windsurf | `.windsurfrules` | SKILL.md body (subset) |
| Cline | `.clinerules` | SKILL.md body (subset) |
| Copilot | `.github/copilot-instructions.md` | SKILL.md body (subset) |
| Aider | `CONVENTIONS.md` | SKILL.md body (subset) |
| Roo Code | `.roo/rules/skill.md` | SKILL.md body (subset) |

- [ ] Skill content can be extracted into platform companions if needed
- [ ] Core instructions don't depend on SKILL.md-specific features

---

## Platform-Specific Conventions

### Claude Code

| Convention | Details |
|-----------|---------|
| Skills directory | `~/.claude/skills/` (global), `.claude/skills/` (project) |
| Rules file | `CLAUDE.md` at repo root (auto-loaded) |
| Trigger | Auto-detect via description + `/slash` commands |
| Tool restriction | `allowed-tools` in frontmatter |
| Subagents | Skills can spawn subagents with isolated context |
| Hooks | Pre/post tool execution hooks available |

### Cursor

| Convention | Details |
|-----------|---------|
| Rules file | `.cursorrules` (root) or `.cursor/rules/` (directory) |
| Trigger | `@reference` in chat, auto on workspace load |
| Rule types | Global, workspace, file-scoped |
| SKILL.md | Adopted — placed in project root or `.cursor/skills/` |

### GitHub Copilot

| Convention | Details |
|-----------|---------|
| Instructions | `.github/copilot-instructions.md` |
| SKILL.md | Adopted — auto-discovered in repo |
| Extensions | Copilot Extensions for deeper integration |

### Continue.dev

| Convention | Details |
|-----------|---------|
| Config | `.continue/config.json` or `~/.continue/config.json` |
| Custom commands | `slashCommands` array in config |
| Context providers | `contextProviders` array for injection |

### Cline

| Convention | Details |
|-----------|---------|
| Rules | `.clinerules` at repo root |
| Memory bank | Key-value persistent facts in rules file |
| Instructions | Auto-read on session init |

### Aider

| Convention | Details |
|-----------|---------|
| Config | `.aider.conf.yml` at repo root or global |
| Conventions | `CONVENTIONS.md` auto-loaded |
| Read files | `--read` flag for additional context files |

---

## Testing & Validation

### Pre-Release Checklist

- [ ] `quick_validate.py` passes (if using Claude Code skill creator)
- [ ] YAML frontmatter parses without errors
- [ ] Name is valid hyphen-case, max 64 chars
- [ ] Description is under 1024 chars, no angle brackets
- [ ] All scripts execute successfully
- [ ] All referenced files exist at stated paths
- [ ] No broken relative path references

### Cross-Platform Testing

- [ ] Test on Claude Code (native SKILL.md support)
- [ ] Test on Cursor (adopted SKILL.md support)
- [ ] Test body content as standalone instructions (Cline, Aider fallback)
- [ ] Test with multiple model tiers (Opus, Sonnet, Haiku)
- [ ] Test auto-detection triggers (does description match intent?)
- [ ] Test natural language invocation (no slash command)
- [ ] Test progressive disclosure (are references loaded only when needed?)

### Functional Testing

- [ ] Happy path: skill triggers correctly, produces expected output
- [ ] Error path: skill handles missing files, bad input gracefully
- [ ] Chaining: skill works when invoked by another skill
- [ ] Long context: skill doesn't bloat context window
- [ ] Feedback loop: skill improves based on iterative usage

### Validation Script Usage

```bash
# Claude Code skill validation
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py /path/to/skill

# Package for distribution
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py /path/to/skill
```

---

## Gotchas & Incompatibilities

### Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Windows backslashes | Paths break on non-Windows | Use `/` always |
| Angle brackets in description | YAML parsing fails | Use plain text |
| Options overload | "Use X or Y" confuses agent | Pick one, be decisive |
| Body "When to use" section | Never read (loaded after trigger) | Put triggers in description |
| Unlisted dependencies | Script fails on clean env | List all requirements |
| Platform-specific paths | Absolute paths non-portable | Use relative paths |
| Too verbose instructions | Token budget blown | Challenge every paragraph |
| Auxiliary docs | README.md, CHANGELOG clutter | Delete, keep only SKILL.md |
| Model-specific tuning | Opus-level detail too sparse for Haiku | Test across tiers |
| Case sensitivity | `skill.md` ≠ `SKILL.md` | Always `SKILL.md` exact |

### Platform Gaps

| Platform | Known Gap |
|----------|-----------|
| Windsurf | No confirmed SKILL.md adoption yet |
| Cline | No SKILL.md adoption; uses own .clinerules |
| Aider | No SKILL.md adoption; uses CONVENTIONS.md |
| Continue.dev | Uses JSON config, not SKILL.md |
| Roo Code | Own .roo/rules/ system, SKILL.md status unclear |

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│              SKILL CREATION QUICK CHECKLIST                 │
├─────────────────────────────────────────────────────────────┤
│ □ SKILL.md with valid YAML frontmatter                     │
│ □ name: hyphen-case, ≤64 chars                             │
│ □ description: triggers + purpose, ≤1024 chars, no < >     │
│ □ Body: imperative form, <500 lines, examples > prose      │
│ □ scripts/: tested, executable, explicit deps              │
│ □ references/: one level deep, TOC if >100 lines           │
│ □ assets/: never loaded into context                       │
│ □ All paths: relative, forward slashes only                │
│ □ No auxiliary docs (README, CHANGELOG, etc.)              │
│ □ Progressive disclosure: frontmatter → body → references  │
│ □ Natural language triggers (most portable)                │
│ □ Tested across platforms and model tiers                  │
│ □ Validates with quick_validate.py                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Sources

- Anthropic, "Equipping Agents for the Real World with Agent Skills" (Dec 2025)
- Anthropic, "The Complete Guide to Building Skills for Claude" (2025)
- Pulumi, "Pulumi Agent Skills" (2025) — Cross-platform SKILL.md adoption
- Platform documentation: Cursor, Continue.dev, Cline, Windsurf, Aider, Roo Code, GitHub Copilot
