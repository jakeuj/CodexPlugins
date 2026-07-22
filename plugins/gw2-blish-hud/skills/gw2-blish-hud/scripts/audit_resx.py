#!/usr/bin/env python3
"""Audit neutral and culture-specific .resx resources using only stdlib."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


PLACEHOLDER_RE = re.compile(r"\{\d+(?:,[^}:]+)?(?::[^}]+)?\}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare neutral .resx files with one localized culture."
    )
    parser.add_argument("strings_root", type=Path, help="Root containing .resx files")
    parser.add_argument("--culture", default="zh", help="Culture suffix, e.g. zh or zh-TW")
    parser.add_argument(
        "--show-keys", action="store_true", help="List keys for every detected issue"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 for missing files/keys, extra keys, empty values, or format drift",
    )
    return parser.parse_args()


def read_resx(path: Path) -> dict[str, str]:
    root = ET.parse(path).getroot()
    values: dict[str, str] = {}
    for node in root.findall("data"):
        key = node.attrib.get("name")
        if not key:
            continue
        value = node.find("value")
        values[key] = "" if value is None or value.text is None else value.text
    return values


def neutral_files(root: Path) -> list[Path]:
    files = set(root.rglob("*.resx"))
    localized: set[Path] = set()
    for path in files:
        stem = path.name[: -len(".resx")]
        if "." not in stem:
            continue
        candidate = path.with_name(stem.rsplit(".", 1)[0] + ".resx")
        if candidate in files:
            localized.add(path)
    return sorted(files - localized)


def placeholders(value: str) -> Counter[str]:
    return Counter(PLACEHOLDER_RE.findall(value))


def print_keys(label: str, keys: list[str], enabled: bool) -> None:
    if enabled and keys:
        print(f"    {label}: {', '.join(keys)}")


def main() -> int:
    args = parse_args()
    root = args.strings_root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: strings root is not a directory: {root}", file=sys.stderr)
        return 2

    bases = neutral_files(root)
    if not bases:
        print(f"ERROR: no neutral .resx files found under {root}", file=sys.stderr)
        return 2

    totals = Counter()
    strict_issues = 0
    parse_errors = 0

    print(f"RESX audit: root={root} culture={args.culture}")
    for base in bases:
        relative = base.relative_to(root)
        localized = base.with_name(f"{base.stem}.{args.culture}.resx")
        try:
            base_values = read_resx(base)
        except (ET.ParseError, OSError) as exc:
            print(f"[PARSE ERROR] {relative}: {exc}")
            parse_errors += 1
            continue

        totals["base_files"] += 1
        totals["base_keys"] += len(base_values)

        if not localized.exists():
            print(f"[MISSING FILE] {relative} -> {localized.name} ({len(base_values)} keys)")
            totals["missing_files"] += 1
            totals["missing_keys"] += len(base_values)
            strict_issues += 1
            continue

        try:
            localized_values = read_resx(localized)
        except (ET.ParseError, OSError) as exc:
            print(f"[PARSE ERROR] {localized.relative_to(root)}: {exc}")
            parse_errors += 1
            continue

        totals["localized_files"] += 1
        base_keys = set(base_values)
        localized_keys = set(localized_values)
        shared = base_keys & localized_keys
        missing = sorted(base_keys - localized_keys)
        extra = sorted(localized_keys - base_keys)
        empty = sorted(key for key in shared if not localized_values[key].strip())
        identical = sorted(
            key for key in shared if localized_values[key].strip() == base_values[key].strip()
        )
        placeholder_drift = sorted(
            key
            for key in shared
            if placeholders(base_values[key]) != placeholders(localized_values[key])
        )
        newline_drift = sorted(
            key
            for key in shared
            if base_values[key].count("\n") != localized_values[key].count("\n")
        )

        totals["present_keys"] += len(shared)
        totals["nonempty_keys"] += len(shared) - len(empty)
        totals["missing_keys"] += len(missing)
        totals["extra_keys"] += len(extra)
        totals["empty_keys"] += len(empty)
        totals["identical_values"] += len(identical)
        totals["placeholder_drift"] += len(placeholder_drift)
        totals["newline_drift"] += len(newline_drift)

        has_issue = bool(missing or extra or empty or placeholder_drift)
        needs_review = bool(newline_drift)
        status = "ISSUES" if has_issue else "REVIEW" if needs_review else "OK"
        print(
            f"[{status}] {relative}: base={len(base_values)} localized={len(localized_values)} "
            f"missing={len(missing)} extra={len(extra)} empty={len(empty)} "
            f"placeholders={len(placeholder_drift)} newlines={len(newline_drift)} "
            f"identical={len(identical)}"
        )
        print_keys("missing", missing, args.show_keys)
        print_keys("extra", extra, args.show_keys)
        print_keys("empty", empty, args.show_keys)
        print_keys("placeholder drift", placeholder_drift, args.show_keys)
        print_keys("newline drift", newline_drift, args.show_keys)
        print_keys("identical", identical, args.show_keys)
        strict_issues += int(has_issue)

    coverage = (
        100.0 * totals["present_keys"] / totals["base_keys"]
        if totals["base_keys"]
        else 0.0
    )
    print(
        "SUMMARY: "
        f"base_files={totals['base_files']} localized_files={totals['localized_files']} "
        f"base_keys={totals['base_keys']} present_keys={totals['present_keys']} "
        f"nonempty_keys={totals['nonempty_keys']} coverage={coverage:.1f}% "
        f"missing_files={totals['missing_files']} missing_keys={totals['missing_keys']} "
        f"extra_keys={totals['extra_keys']} empty_keys={totals['empty_keys']} "
        f"placeholder_drift={totals['placeholder_drift']} "
        f"newline_drift={totals['newline_drift']} identical={totals['identical_values']}"
    )

    if parse_errors:
        return 2
    if args.strict and strict_issues:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
