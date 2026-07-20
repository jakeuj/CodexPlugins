#!/usr/bin/env python3
"""Inspect local marketplace plugins and copy a skill without overwriting conflicts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


IGNORED_NAMES = {".DS_Store", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)


class PackageError(RuntimeError):
    """Raised for safe, user-actionable packaging failures."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory marketplace plugins or safely copy a skill into a plugin."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser(
        "inventory", help="Print writable local marketplace plugin metadata as JSON."
    )
    inventory.add_argument("--repo-root", default=".")
    inventory.add_argument("--marketplace")
    inventory.add_argument("--skill")

    copy = subparsers.add_parser(
        "copy", help="Copy a complete skill tree without overwriting different content."
    )
    copy.add_argument("--source", required=True)
    copy.add_argument("--plugin-root", required=True)

    return parser.parse_args()


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PackageError(f"{label} does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PackageError(f"{label} is not valid JSON: {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PackageError(f"{label} must contain a JSON object: {path}")
    return payload


def parse_skill_frontmatter(skill_dir: Path) -> dict[str, str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise PackageError(f"skill directory is missing SKILL.md: {skill_dir}")
    text = skill_md.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise PackageError(f"SKILL.md is missing YAML frontmatter: {skill_md}")
    try:
        payload = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise PackageError(f"SKILL.md frontmatter is invalid YAML: {skill_md}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PackageError(f"SKILL.md frontmatter must be an object: {skill_md}")
    fields = {key: payload.get(key) for key in ("name", "description")}
    if not all(isinstance(value, str) and value.strip() for value in fields.values()):
        raise PackageError(f"SKILL.md requires name and description: {skill_md}")
    return {key: value.strip() for key, value in fields.items() if isinstance(value, str)}


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def local_source_path(entry: dict[str, Any]) -> str | None:
    source = entry.get("source")
    if isinstance(source, str):
        return source
    if isinstance(source, dict) and source.get("source") == "local":
        raw_path = source.get("path")
        return raw_path if isinstance(raw_path, str) else None
    return None


def inspect_plugin(entry: dict[str, Any], repo_root: Path) -> tuple[dict[str, Any] | None, str | None]:
    name = entry.get("name")
    if not isinstance(name, str) or not name.strip():
        return None, "marketplace entry has no valid name"
    raw_path = local_source_path(entry)
    if raw_path is None:
        return None, "plugin source is not local"
    if not raw_path.startswith("./"):
        return None, "local source.path must start with ./"

    plugin_root = (repo_root / raw_path).resolve()
    if not inside(plugin_root, repo_root):
        return None, "local source.path escapes the repository root"
    if not plugin_root.is_dir():
        return None, "local plugin directory is missing"

    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    try:
        manifest = load_json_object(manifest_path, "plugin manifest")
    except PackageError as exc:
        return None, str(exc)

    skill_rows: list[dict[str, str]] = []
    skills_root = plugin_root / "skills"
    if skills_root.is_dir():
        for child in sorted(skills_root.iterdir()):
            if not child.is_dir() or not (child / "SKILL.md").is_file():
                continue
            try:
                metadata = parse_skill_frontmatter(child)
            except PackageError as exc:
                skill_rows.append({"path": str(child), "error": str(exc)})
            else:
                skill_rows.append(
                    {
                        "name": metadata["name"],
                        "description": metadata["description"],
                        "path": str(child),
                    }
                )

    interface = manifest.get("interface")
    return (
        {
            "name": name,
            "category": entry.get("category"),
            "source_path": raw_path,
            "plugin_root": str(plugin_root),
            "writable": os.access(plugin_root, os.W_OK),
            "manifest": {
                "name": manifest.get("name"),
                "description": manifest.get("description"),
                "keywords": manifest.get("keywords", []),
                "display_name": interface.get("displayName")
                if isinstance(interface, dict)
                else None,
            },
            "skills": skill_rows,
        },
        None,
    )


def inventory(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.is_dir():
        raise PackageError(f"repository root does not exist: {repo_root}")
    if args.marketplace:
        raw_marketplace = Path(args.marketplace).expanduser()
        marketplace_path = (
            raw_marketplace.resolve()
            if raw_marketplace.is_absolute()
            else (repo_root / raw_marketplace).resolve()
        )
    else:
        marketplace_path = repo_root / ".agents" / "plugins" / "marketplace.json"
    if not inside(marketplace_path, repo_root):
        raise PackageError(f"marketplace path escapes the selected root: {marketplace_path}")
    marketplace = load_json_object(marketplace_path, "marketplace")
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        raise PackageError(f"marketplace plugins must be an array: {marketplace_path}")

    plugins: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            skipped.append({"name": "<invalid>", "reason": "entry is not an object"})
            continue
        row, reason = inspect_plugin(entry, repo_root)
        if row is None:
            skipped.append(
                {
                    "name": str(entry.get("name", "<invalid>")),
                    "reason": reason or "unknown reason",
                }
            )
        elif row["writable"]:
            plugins.append(row)
        else:
            skipped.append({"name": row["name"], "reason": "plugin is not writable"})

    result: dict[str, Any] = {
        "repo_root": str(repo_root),
        "marketplace_path": str(marketplace_path),
        "marketplace_name": marketplace.get("name"),
        "plugins": plugins,
        "skipped": skipped,
    }
    if args.skill:
        skill_dir = Path(args.skill).expanduser().resolve()
        metadata = parse_skill_frontmatter(skill_dir)
        result["source_skill"] = {**metadata, "path": str(skill_dir)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def ignored(relative_path: Path) -> bool:
    return any(part in IGNORED_NAMES for part in relative_path.parts) or (
        relative_path.suffix in IGNORED_SUFFIXES
    )


def skill_fingerprint(root: Path) -> dict[str, str]:
    fingerprint: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ignored(relative):
            continue
        if path.is_symlink():
            raise PackageError(f"skill contains a symbolic link, which is not copied: {path}")
        if path.is_file():
            fingerprint[relative.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return fingerprint


def copy_ignore(directory: str, names: list[str]) -> set[str]:
    base = Path(directory)
    ignored_names: set[str] = set()
    for name in names:
        relative = Path(name)
        path = base / name
        if name in IGNORED_NAMES or path.suffix in IGNORED_SUFFIXES or ignored(relative):
            ignored_names.add(name)
    return ignored_names


def copy_skill(args: argparse.Namespace) -> int:
    source = Path(args.source).expanduser().resolve()
    plugin_root = Path(args.plugin_root).expanduser().resolve()
    metadata = parse_skill_frontmatter(source)
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        raise PackageError(f"plugin root is missing .codex-plugin/plugin.json: {plugin_root}")

    skill_name = metadata["name"]
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name) is None:
        raise PackageError(f"skill name must be lowercase hyphen-case: {skill_name}")
    source_fingerprint = skill_fingerprint(source)
    skills_root = plugin_root / "skills"
    destination = skills_root / skill_name

    if destination.is_symlink():
        raise PackageError(f"destination skill is a symbolic link: {destination}")
    if destination.exists():
        destination_metadata = parse_skill_frontmatter(destination)
        destination_fingerprint = skill_fingerprint(destination)
        if destination_metadata["name"] == skill_name and destination_fingerprint == source_fingerprint:
            print(
                json.dumps(
                    {
                        "status": "unchanged",
                        "skill": skill_name,
                        "destination": str(destination),
                        "files": len(source_fingerprint),
                    },
                    indent=2,
                )
            )
            return 0
        raise PackageError(
            f"destination skill already exists with different content: {destination}"
        )

    skills_root.mkdir(parents=True, exist_ok=True)
    temporary_parent = Path(tempfile.mkdtemp(prefix=f".{skill_name}-", dir=skills_root))
    temporary_skill = temporary_parent / skill_name
    try:
        shutil.copytree(source, temporary_skill, ignore=copy_ignore)
        copied_fingerprint = skill_fingerprint(temporary_skill)
        if copied_fingerprint != source_fingerprint:
            raise PackageError("copied skill fingerprint does not match the source")
        os.replace(temporary_skill, destination)
    finally:
        shutil.rmtree(temporary_parent, ignore_errors=True)

    print(
        json.dumps(
            {
                "status": "copied",
                "skill": skill_name,
                "destination": str(destination),
                "files": len(source_fingerprint),
            },
            indent=2,
        )
    )
    return 0


def main() -> None:
    args = parse_args()
    try:
        if args.command == "inventory":
            raise SystemExit(inventory(args))
        raise SystemExit(copy_skill(args))
    except PackageError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(3) from exc


if __name__ == "__main__":
    main()
