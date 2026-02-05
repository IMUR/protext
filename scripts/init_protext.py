#!/usr/bin/env python3
"""
init_protext.py - Initialize Protext in a project

Bootstraps the protext context management system by reading existing
CLAUDE.md and creating PROTEXT.md with the full .protext/ structure.

Usage:
    python init_protext.py <project-path> [--tier beginner|intermediate|advanced]

Default tier: advanced (full features)
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
import re


def extract_project_info(claude_md_path: Path) -> dict:
    """Extract key information from existing CLAUDE.md."""
    info = {
        "name": "Unknown Project",
        "identity": "",
        "key_services": [],
        "key_paths": [],
    }

    if not claude_md_path.exists():
        return info

    content = claude_md_path.read_text()

    # Extract project name from first heading or title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        info["name"] = title_match.group(1).strip()

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


def init_protext(project_path: Path, tier: str = "advanced") -> bool:
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

    if protext_md.exists() or protext_dir.exists():
        print("Warning: Protext already exists in this project.")
        response = input("Overwrite? [y/N]: ").strip().lower()
        if response != 'y':
            print("Aborted.")
            return False

    # Extract info from existing CLAUDE.md
    claude_md = project_path / "CLAUDE.md"
    info = extract_project_info(claude_md)

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

    args = parser.parse_args()

    project_path = args.project_path.resolve()
    success = init_protext(project_path, args.tier)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
