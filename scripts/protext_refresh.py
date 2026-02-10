#!/usr/bin/env python3
"""
protext_refresh.py - Refresh parent protext from children

Re-aggregates child project status and updates parent PROTEXT.md.

Usage:
    python protext_refresh.py [project-path] [--children]

Without --children: Updates PROTEXT.md timestamp and scope (standard refresh)
With --children: Re-aggregates child status (parent protext only)
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Import parent functions from init_protext
from init_protext import (
    discover_children,
    extract_child_info,
    create_parent_protext_md,
    extract_project_info,
    extract_marker,
    extract_section_fallback
)


def is_parent_protext(project_path: Path) -> bool:
    """Check if this is a parent protext (has children in config)."""
    config_path = project_path / ".protext" / "config.yaml"
    if not config_path.exists():
        return False

    content = config_path.read_text()
    return "children:" in content


def refresh_parent(project_path: Path) -> bool:
    """Refresh parent PROTEXT.md by re-aggregating children."""
    print(f"Refreshing parent protext...")

    # Check for parent protext
    if not is_parent_protext(project_path):
        print(f"Error: Not a parent protext (no children in config)")
        print(f"  Run 'protext init --parent' to initialize as parent")
        return False

    # Discover children
    children = discover_children(project_path)
    if not children:
        print(f"Warning: No child protext projects found")
        print(f"  Looking for subdirectories with .protext/")
        return False

    print(f"  Found {len(children)} child projects: {', '.join(children)}")

    # Extract info from each child
    children_info = []
    for child_name in children:
        child_path = project_path / child_name
        child_info = extract_child_info(child_path)
        children_info.append(child_info)
        print(f"    - {child_name}: {child_info['status']}")

    # Extract parent project name from existing PROTEXT.md
    protext_md = project_path / "PROTEXT.md"
    if protext_md.exists():
        content = protext_md.read_text()
        # Extract project name from first heading
        import re
        name_match = re.search(r"^#\s+Protext:\s+(.+)$", content, re.MULTILINE)
        project_name = name_match.group(1) if name_match else project_path.name
    else:
        project_name = project_path.name

    info = {"name": project_name, "identity": f"Meta-project containing {len(children)} child projects"}

    # Generate updated parent PROTEXT.md
    protext_content = create_parent_protext_md(project_path, info, children_info)
    protext_md.write_text(protext_content)
    print(f"  Updated: PROTEXT.md")

    # Update config.yaml children list
    config_path = project_path / ".protext" / "config.yaml"
    if config_path.exists():
        config_content = config_path.read_text()
        # Simple replace: find children: section and update
        lines = config_content.split("\n")
        new_lines = []
        in_children_section = False
        for line in lines:
            if line.startswith("children:"):
                new_lines.append("children:  # Child protext projects")
                for child in children:
                    new_lines.append(f"  - {child}")
                in_children_section = True
            elif in_children_section and line.startswith("  - "):
                # Skip old children entries
                continue
            elif in_children_section and not line.startswith("  "):
                # End of children section
                new_lines.append(line)
                in_children_section = False
            else:
                new_lines.append(line)

        config_path.write_text("\n".join(new_lines))
        print(f"  Updated: .protext/config.yaml")

    print("\nParent protext refreshed successfully!")
    print(f"  {sum(1 for c in children_info if c['status'] == 'active')}/{len(children_info)} children active")
    return True


def refresh_standard(project_path: Path) -> bool:
    """Standard refresh: update timestamp and regenerate based on current state."""
    print("Standard refresh not yet implemented")
    print("For now, use 'protext init --existing update' to regenerate PROTEXT.md")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Refresh protext context"
    )
    parser.add_argument(
        "project_path",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Path to the project directory (default: current directory)"
    )
    parser.add_argument(
        "--children",
        action="store_true",
        help="Refresh parent by re-aggregating children"
    )

    args = parser.parse_args()

    project_path = args.project_path.resolve()

    # Validate project has protext
    protext_md = project_path / "PROTEXT.md"
    if not protext_md.exists():
        print(f"Error: No PROTEXT.md found in {project_path}")
        print(f"  Run 'protext init' to initialize")
        sys.exit(1)

    if args.children:
        success = refresh_parent(project_path)
    else:
        success = refresh_standard(project_path)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
