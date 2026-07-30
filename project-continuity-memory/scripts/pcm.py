#!/usr/bin/env python3
"""Initialize and statically validate Project Continuity Memory files."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from datetime import date
from pathlib import Path


FILES = {
    "PROJECT_MEMORY.md": {
        "asset": "project-memory-template.md",
        "required": (
            "# Project Memory",
            "## Project identity",
            "## Long-term goal and boundaries",
            "## Active workstreams",
            "## Durable decisions",
            "## Key sources of truth",
            "## Project conventions",
            "## Known pitfalls",
            "## Maintenance rules",
        ),
        "warn_lines": 160,
        "max_lines": 240,
        "warn_chars": 8000,
        "max_chars": 12000,
    },
    "HANDOFF.md": {
        "asset": "handoff-template.md",
        "required": (
            "# Current Handoff",
            "## Handoff status",
            "## Current objective",
            "## Start here",
            "## Verified current state",
            "## Decisions this session",
            "## Recent changes and evidence",
            "## Blockers and open questions",
            "## Next step",
            "## Protection and recovery",
            "## Integrity rules",
        ),
        "warn_lines": 100,
        "max_lines": 140,
        "warn_chars": 4000,
        "max_chars": 6000,
    },
}

EMPTY_LABEL = re.compile(
    r"^-\s*(?:Goal|In scope|Out of scope|Current scope|Do not overwrite|"
    r"Backup or rollback entry):\s*$",
    re.IGNORECASE,
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Initialize or validate PROJECT_MEMORY.md and HANDOFF.md."
    )
    sub = result.add_subparsers(dest="command", required=True)

    init = sub.add_parser(
        "init", help="Create missing files without overwriting existing ones."
    )
    init.add_argument("--root", required=True, help="Existing project root directory.")
    init.add_argument(
        "--project-name", help="Project display name; defaults to directory name."
    )

    check = sub.add_parser(
        "check", help="Validate structure, fields, and size budgets."
    )
    check.add_argument("--root", required=True, help="Project root directory.")
    check.add_argument(
        "--strict",
        action="store_true",
        help="Treat unresolved or empty fields and size warnings as failures.",
    )
    return result


def resolve_root(raw: str) -> Path:
    root = Path(raw).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Project root does not exist or is not a directory: {root}")
    return root


def atomic_create(path: Path, content: str) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    handle, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temp_name, path)
        except FileExistsError:
            raise FileExistsError(
                f"Refusing to overwrite existing file: {path}"
            ) from None
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def init_files(root: Path, project_name: str) -> dict[str, object]:
    asset_dir = Path(__file__).resolve().parent.parent / "assets"
    created: list[str] = []
    skipped: list[str] = []
    values = {
        "{{PROJECT_NAME}}": project_name,
        "{{PROJECT_ROOT}}": str(root),
        "{{DATE}}": date.today().isoformat(),
    }

    for filename, rules in FILES.items():
        target = root / filename
        if target.exists():
            skipped.append(filename)
            continue
        template = (asset_dir / str(rules["asset"])).read_text(encoding="utf-8")
        for marker, value in values.items():
            template = template.replace(marker, value)
        atomic_create(target, template)
        created.append(filename)

    return {
        "ok": True,
        "root": str(root),
        "created": created,
        "skipped_existing": skipped,
        "next": (
            "Fill every empty field from verified project facts, then run "
            "check --strict."
        ),
    }


def find_empty_template_fields(lines: list[str]) -> list[int]:
    empty: list[int] = []
    for number, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if stripped in {"-", "1."} or EMPTY_LABEL.fullmatch(stripped):
            empty.append(number)
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if cells and all(not cell for cell in cells):
                empty.append(number)
    return empty


def validate_file(
    path: Path, rules: dict[str, object], strict: bool
) -> dict[str, object]:
    if not path.is_file():
        return {
            "file": path.name,
            "ok": False,
            "errors": ["missing"],
            "warnings": [],
        }

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors: list[str] = []
    warnings: list[str] = []

    for heading in rules["required"]:
        if heading not in lines:
            errors.append(f"missing heading: {heading}")

    if "{{" in content or "}}" in content:
        errors.append("unresolved template marker")

    empty_lines = find_empty_template_fields(lines)
    if empty_lines:
        preview = ",".join(str(number) for number in empty_lines[:12])
        suffix = "..." if len(empty_lines) > 12 else ""
        warnings.append(f"empty template fields at lines: {preview}{suffix}")

    line_count = len(lines)
    char_count = len(content)
    if line_count > int(rules["max_lines"]):
        errors.append(f"line hard limit exceeded: {line_count}>{rules['max_lines']}")
    elif line_count > int(rules["warn_lines"]):
        warnings.append(
            f"line budget exceeded: {line_count}>{rules['warn_lines']}"
        )

    if char_count > int(rules["max_chars"]):
        errors.append(
            f"character hard limit exceeded: {char_count}>{rules['max_chars']}"
        )
    elif char_count > int(rules["warn_chars"]):
        warnings.append(
            f"character budget exceeded: {char_count}>{rules['warn_chars']}"
        )

    if strict and warnings:
        errors.extend(f"strict: {warning}" for warning in warnings)

    return {
        "file": path.name,
        "ok": not errors,
        "lines": line_count,
        "characters": char_count,
        "errors": errors,
        "warnings": warnings,
    }


def check_files(root: Path, strict: bool) -> dict[str, object]:
    files = [
        validate_file(root / filename, rules, strict)
        for filename, rules in FILES.items()
    ]
    return {
        "ok": all(bool(item["ok"]) for item in files),
        "root": str(root),
        "strict": strict,
        "files": files,
        "scope": (
            "Static structure, fields, and size only; project facts require "
            "dynamic verification."
        ),
    }


def main() -> int:
    args = parser().parse_args()
    try:
        root = resolve_root(args.root)
        if args.command == "init":
            name = (args.project_name or root.name).strip()
            if not name:
                raise ValueError("Project name must not be empty.")
            result = init_files(root, name)
        else:
            result = check_files(root, args.strict)
    except (OSError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        return 2

    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
