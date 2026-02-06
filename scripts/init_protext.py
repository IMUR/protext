#!/usr/bin/env python3
"""
init_protext.py - Initialize Protext in a project

Bootstraps the protext context management system by reading existing
CLAUDE.md and creating PROTEXT.md with the full .protext/ structure.

Usage:
    python init_protext.py <project-path> [--tier beginner|intermediate|advanced]
                                          [--existing archive|replace|update]

Default tier: advanced (full features)

When PROTEXT.md or .protext/ already exist, the --existing flag is required:
    archive  - Date-stamp existing artifacts to .protext/archive/YYYY-MM-DD/,
               then generate fresh
    replace  - Delete existing artifacts (preserving .protext/archive/),
               then generate fresh
    update   - Regenerate PROTEXT.md and index.yaml only; preserve config.yaml,
               scopes/, and handoff.md

Without --existing, the script prints a conflict message and exits non-zero.
No interactive prompts are used.
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
import re


def extract_project_info(claude_md_path: Path, project_path: Path = None) -> dict:
    """Extract key information from existing CLAUDE.md."""
    info = {
        "name": "Unknown Project",
        "identity": "",
        "key_services": [],
        "key_paths": [],
    }

    # Primary: directory name (most reliable, avoids "CLAUDE.md" heading bug)
    if project_path:
        info["name"] = project_path.name.replace("-", " ").replace("_", " ").title()

    if not claude_md_path.exists():
        return info

    content = claude_md_path.read_text()

    # Override with CLAUDE.md heading only if it looks like a real project name
    skip_names = {"claude.md", "readme.md", "readme", "overview", "about", "introduction"}
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        candidate = title_match.group(1).strip()
        if candidate.lower() not in skip_names:
            info["name"] = candidate

    # Extract identity/purpose
    purpose_match = re.search(
        r'(?:purpose|about|overview)[:\s]*\n+(.+?)(?=\n#|\n\n---|\Z)',
        content, re.IGNORECASE | re.DOTALL
    )
    if purpose_match:
        info["identity"] = purpose_match.group(1).strip()[:200]

    # Extract service locations
    service_matches = re.findall(
        r'\|\s*([^|]+)\s*\|\s*([/\w.-]+(?:docker-compose\.yml|config\.yaml|Caddyfile)[^|]*)\s*\|',
        content
    )
    info["key_services"] = [(m[0].strip(), m[1].strip()) for m in service_matches[:5]]

    # Extract key paths
    path_matches = re.findall(r'`(/[^`]+)`', content)
    info["key_paths"] = list(set(path_matches))[:10]

    return info


def detect_docs_structure(project_path: Path) -> list:
    """Detect existing documentation files for extraction index."""
    docs_dir = project_path / "docs"
    extractions = []

    if docs_dir.exists():
        for doc_file in docs_dir.glob("*.md"):
            name = doc_file.stem.lower()
            extractions.append({
                "name": name,
                "source": f"docs/{doc_file.name}",
                "summary": f"{doc_file.stem} documentation",
            })

    return extractions[:20]  # Max 20 extractions


def create_protext_md(project_path: Path, info: dict) -> str:
    """Generate PROTEXT.md content."""
    today = datetime.now().strftime("%Y-%m-%d")

    identity = info.get("identity") or f"Project at {project_path.name}"
    if len(identity) > 200:
        identity = identity[:197] + "..."

    return f"""# Protext: {info['name']}

> Generated: {today} | Scope: ops | Tokens: ~400

## Identity

{identity}

## Current State

Active: Initial setup | Blocked: None | Recent: Protext initialized

## Hot Context

- Protext just initialized - review and customize
- Check `.protext/index.yaml` for extraction triggers
- Update scope files in `.protext/scopes/`

## Scope Signals

- `@ops` → .protext/scopes/ops.md
- `@dev` → .protext/scopes/dev.md
- `@security` → .protext/scopes/security.md

## Handoff

Last: Protext initialized | Next: Customize hot context | Caution: Review auto-generated content
"""


def create_index_yaml(extractions: list) -> str:
    """Generate .protext/index.yaml content."""
    content = """# Protext Extraction Index
# Max 20 extractions. Triggers are keyword hints (suggest-mode default).

extractions:
"""

    # Default triggers by common doc names
    default_triggers = {
        "network": ["dns", "ip", "tailscale", "mesh", "routing", "network"],
        "services": ["docker", "container", "service", "port", "compose"],
        "secrets": ["secret", "credential", "infisical", "auth", "password"],
        "architecture": ["design", "diagram", "pattern", "architecture"],
        "system": ["hardware", "storage", "resources", "memory", "cpu"],
        "router": ["mikrotik", "gateway", "dhcp", "firewall", "forward"],
    }

    for ext in extractions:
        name = ext["name"]
        triggers = default_triggers.get(name, [name])
        content += f"""
  {name}:
    source: {ext['source']}
    triggers: {triggers}
    summary: "{ext['summary']}"
    tokens: ~500
"""

    if not extractions:
        content += """
  # Example extraction (uncomment and customize):
  # docs:
  #   source: docs/README.md
  #   triggers: [documentation, readme, overview]
  #   summary: "Project documentation"
  #   tokens: ~500
"""

    return content


def create_config_yaml() -> str:
    """Generate .protext/config.yaml content."""
    return """# Protext Configuration

# Extraction behavior
extraction_mode: suggest  # suggest | auto | confirm
token_budget: 2000        # Max tokens per session

# Handoff settings
handoff_ttl_hours: 48     # Time-to-live before staleness warning

# Active scope (updated by protext scope command)
active_scope: ops

# Feature flags
features:
  auto_handoff_capture: true
  token_warnings: true
  scope_switching: true
"""


def create_handoff_md() -> str:
    """Generate .protext/handoff.md content."""
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return f"""# Session Handoff
> Updated: {now} | TTL: 48h | Status: FRESH

## Last Session
**Completed:**
- Protext initialization

**In Progress:**
- None

**Deferred:**
- None

## Cautions
- Review auto-generated PROTEXT.md content
- Customize extraction triggers in index.yaml

## Agent Notes
Initial protext setup. Customize scopes and hot context for your workflow.
"""


def create_scope_file(scope_name: str, focus: str) -> str:
    """Generate a scope file."""
    return f"""# Scope: {scope_name.title()}

## Focus
{focus}

## Key Resources
- [Add key paths and resources]

## Current Priorities
1. [Define priorities]
2. [Add more as needed]

## Cautions
- [Add scope-specific warnings]
"""


SCOPE_DEFAULTS = {
    "ops": "Infrastructure management, service health, deployment, monitoring.",
    "dev": "Development workflow, code patterns, testing, debugging.",
    "security": "Authentication, secrets management, vulnerabilities, access control.",
}


def _archive_dir_for_today(protext_dir: Path) -> Path:
    """Return a unique archive directory for today's date."""
    today = datetime.now().strftime("%Y-%m-%d")
    archive_base = protext_dir / "archive"
    archive_base.mkdir(parents=True, exist_ok=True)
    candidate = archive_base / today
    if not candidate.exists():
        return candidate
    # Append -N suffix if date dir already exists
    n = 1
    while True:
        candidate = archive_base / f"{today}-{n}"
        if not candidate.exists():
            return candidate
        n += 1


def handle_existing_archive(project_path: Path) -> None:
    """Move existing protext artifacts into a dated archive directory."""
    protext_md = project_path / "PROTEXT.md"
    protext_dir = project_path / ".protext"

    archive_dir = _archive_dir_for_today(protext_dir)
    archive_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Archiving existing artifacts to {archive_dir.relative_to(project_path)}/")

    # Move PROTEXT.md
    if protext_md.exists():
        shutil.move(str(protext_md), str(archive_dir / "PROTEXT.md"))

    # Move .protext/ contents (except archive/ itself)
    if protext_dir.exists():
        for item in protext_dir.iterdir():
            if item.name == "archive":
                continue
            dest = archive_dir / item.name
            shutil.move(str(item), str(dest))


def handle_existing_replace(project_path: Path) -> None:
    """Delete existing protext artifacts, preserving .protext/archive/."""
    protext_md = project_path / "PROTEXT.md"
    protext_dir = project_path / ".protext"

    print("  Replacing existing artifacts (preserving archive/)...")

    if protext_md.exists():
        protext_md.unlink()

    if protext_dir.exists():
        for item in protext_dir.iterdir():
            if item.name == "archive":
                continue
            if item.is_dir():
                shutil.rmtree(str(item))
            else:
                item.unlink()


def handle_existing_update(project_path: Path, tier: str) -> bool:
    """Regenerate PROTEXT.md and index.yaml; preserve user-customized files."""
    claude_md = project_path / "CLAUDE.md"
    protext_md = project_path / "PROTEXT.md"
    protext_dir = project_path / ".protext"

    info = extract_project_info(claude_md, project_path)
    extractions = detect_docs_structure(project_path)

    print(f"Updating protext (tier: {tier})...")
    print(f"  Project: {info['name']}")

    updated = []
    preserved = []

    # Always regenerate PROTEXT.md
    protext_content = create_protext_md(project_path, info)
    protext_md.write_text(protext_content)
    updated.append("PROTEXT.md")

    if tier == "advanced" and protext_dir.exists():
        # Regenerate index.yaml
        index_path = protext_dir / "index.yaml"
        index_path.write_text(create_index_yaml(extractions))
        updated.append(".protext/index.yaml")

        # Preserve user-customized files
        if (protext_dir / "config.yaml").exists():
            preserved.append(".protext/config.yaml")
        if (protext_dir / "handoff.md").exists():
            preserved.append(".protext/handoff.md")
        scopes_dir = protext_dir / "scopes"
        if scopes_dir.exists():
            for scope_file in scopes_dir.iterdir():
                preserved.append(f".protext/scopes/{scope_file.name}")

    print(f"\n  Updated:   {', '.join(updated)}")
    if preserved:
        print(f"  Preserved: {', '.join(preserved)}")

    print("\nProtext updated successfully!")
    return True


def init_protext(project_path: Path, tier: str = "advanced",
                 existing: str = None) -> bool:
    """Initialize protext in the given project."""

    # Validate project path
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        return False

    if not project_path.is_dir():
        print(f"Error: Not a directory: {project_path}")
        return False

    # Check for existing protext
    protext_md = project_path / "PROTEXT.md"
    protext_dir = project_path / ".protext"
    has_existing = protext_md.exists() or protext_dir.exists()

    if has_existing and existing is None:
        found = []
        if protext_md.exists():
            found.append("PROTEXT.md")
        if protext_dir.exists():
            found.append(".protext/")
        print(f"Error: Protext already exists in this project.")
        print(f"  Found: {', '.join(found)}")
        print()
        print("Use --existing to specify how to handle existing artifacts:")
        print("  --existing archive  - Archive to .protext/archive/YYYY-MM-DD/, then init fresh")
        print("  --existing replace  - Delete existing (preserve archive/), then init fresh")
        print("  --existing update   - Regenerate PROTEXT.md + index.yaml, keep config/scopes/handoff")
        return False

    if has_existing:
        if existing == "update":
            return handle_existing_update(project_path, tier)
        elif existing == "archive":
            handle_existing_archive(project_path)
        elif existing == "replace":
            handle_existing_replace(project_path)

    # Extract info from existing CLAUDE.md
    claude_md = project_path / "CLAUDE.md"
    info = extract_project_info(claude_md, project_path)

    # Detect docs for extraction index
    extractions = detect_docs_structure(project_path)

    print(f"Initializing protext (tier: {tier})...")
    print(f"  Project: {info['name']}")
    print(f"  Found {len(extractions)} docs for extraction index")

    # Create PROTEXT.md (all tiers)
    protext_content = create_protext_md(project_path, info)
    protext_md.write_text(protext_content)
    print(f"  Created: PROTEXT.md")

    if tier in ("intermediate", "advanced"):
        # Create .protext directory
        protext_dir.mkdir(exist_ok=True)

        # Create handoff.md
        handoff_path = protext_dir / "handoff.md"
        handoff_path.write_text(create_handoff_md())
        print(f"  Created: .protext/handoff.md")

    if tier == "advanced":
        # Create config.yaml
        config_path = protext_dir / "config.yaml"
        config_path.write_text(create_config_yaml())
        print(f"  Created: .protext/config.yaml")

        # Create index.yaml
        index_path = protext_dir / "index.yaml"
        index_path.write_text(create_index_yaml(extractions))
        print(f"  Created: .protext/index.yaml")

        # Create scopes directory
        scopes_dir = protext_dir / "scopes"
        scopes_dir.mkdir(exist_ok=True)

        for scope_name, focus in SCOPE_DEFAULTS.items():
            scope_file = scopes_dir / f"{scope_name}.md"
            scope_file.write_text(create_scope_file(scope_name, focus))
            print(f"  Created: .protext/scopes/{scope_name}.md")

    print("\nProtext initialized successfully!")
    print("\nNext steps:")
    print("  1. Review and customize PROTEXT.md")
    if tier == "advanced":
        print("  2. Adjust extraction triggers in .protext/index.yaml")
        print("  3. Customize scope files in .protext/scopes/")
    print(f"\nTip: Run 'protext status' to see current state.")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Initialize Protext context management in a project"
    )
    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to the project directory"
    )
    parser.add_argument(
        "--tier",
        choices=["beginner", "intermediate", "advanced"],
        default="advanced",
        help="Feature tier (default: advanced)"
    )
    parser.add_argument(
        "--existing",
        choices=["archive", "replace", "update"],
        default=None,
        help="How to handle existing protext artifacts: "
             "archive (move to dated backup), "
             "replace (delete and regenerate), "
             "update (regenerate PROTEXT.md + index.yaml only)"
    )

    args = parser.parse_args()

    project_path = args.project_path.resolve()
    success = init_protext(project_path, args.tier, args.existing)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
