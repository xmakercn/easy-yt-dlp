#!/usr/bin/env python3
"""Automatic version management based on PR labels."""
import re
import sys
from pathlib import Path


def get_current_version() -> tuple[int, int, int]:
    """Read current version from __init__.py."""
    init_file = Path("src/easy_ytdlp/__init__.py")
    content = init_file.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        raise ValueError("Version not found in __init__.py")
    return tuple(map(int, match.groups()))


def bump_version(version_type: str) -> tuple[int, int, int]:
    """Bump version based on type: major, minor, or patch."""
    major, minor, patch = get_current_version()
    
    if version_type == "major":
        return (major + 1, 0, 0)
    elif version_type == "minor":
        return (major, minor + 1, 0)
    elif version_type == "patch":
        return (major, minor, patch + 1)
    else:
        raise ValueError(f"Invalid version type: {version_type}")


def update_version_in_file(file_path: Path, old_version: str, new_version: str) -> bool:
    """Update version string in a file."""
    if not file_path.exists():
        return False
    
    content = file_path.read_text(encoding="utf-8")
    new_content = content.replace(old_version, new_version)
    
    if new_content != content:
        file_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def update_all_versions(new_version: str) -> None:
    """Update version in all relevant files."""
    old_version = ".".join(map(str, get_current_version()))
    
    files_to_update = [
        Path("src/easy_ytdlp/__init__.py"),
        Path("README.md"),
        Path("README-zh.md"),
    ]
    
    updated = []
    for file_path in files_to_update:
        if update_version_in_file(file_path, old_version, new_version):
            updated.append(str(file_path))
    
    print(f"Updated version from {old_version} to {new_version}")
    print(f"Files updated: {', '.join(updated)}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python bump_version.py <major|minor|patch>")
        sys.exit(1)
    
    version_type = sys.argv[1].lower()
    if version_type not in ("major", "minor", "patch"):
        print("Error: version type must be major, minor, or patch")
        sys.exit(1)
    
    new_version = ".".join(map(str, bump_version(version_type)))
    update_all_versions(new_version)
    
    # Output for GitHub Actions
    print(f"::set-output name=version::{new_version}")


if __name__ == "__main__":
    main()
