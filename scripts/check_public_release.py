#!/usr/bin/env python3
"""Fail when tracked public-release files cross the repository privacy boundary."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


FORBIDDEN_BASENAMES = {"AGENTS.md", "PROJECT_MEMORY.md", "HANDOFF.md"}
FORBIDDEN_DIRECTORY_NAMES = {".project-memory", "backup", "backups"}
FORBIDDEN_SUFFIXES = {".bak", ".backup"}
SELF = Path("scripts/check_public_release.py")

CONTENT_PATTERNS = (
    ("macOS user-home path", re.compile(rb"/Users/[A-Za-z0-9._-]+")),
    ("Linux user-home path", re.compile(rb"/home/[A-Za-z0-9._-]+")),
    (
        "Windows user-home path",
        re.compile(rb"[A-Za-z]:\\\\Users\\\\[^\\s\\\\]+", re.IGNORECASE),
    ),
    (
        "email address",
        re.compile(
            rb"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@"
            rb"[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z0-9.-])"
        ),
    ),
    ("private-name marker", re.compile(rb"\bPRIVATE_NAME\b", re.IGNORECASE)),
    (
        "private-key material",
        re.compile(rb"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    ),
)


def tracked_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [
        Path(raw.decode("utf-8"))
        for raw in result.stdout.split(b"\0")
        if raw
    ]


def scan_repository(root: Path, paths: list[Path]) -> list[str]:
    findings: list[str] = []
    resolved_root = root.resolve()

    for relative in paths:
        parts = set(relative.parts)
        if relative.name in FORBIDDEN_BASENAMES:
            findings.append(f"{relative}: forbidden private filename")
        if parts & FORBIDDEN_DIRECTORY_NAMES:
            findings.append(f"{relative}: forbidden private directory")
        if relative.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"{relative}: forbidden backup suffix")

        target = root / relative
        if target.is_symlink():
            resolved_target = target.resolve(strict=False)
            if not resolved_target.is_relative_to(resolved_root):
                findings.append(f"{relative}: symlink resolves outside repository")
            continue

        if not target.is_file() or relative == SELF:
            continue

        data = target.read_bytes()
        for label, pattern in CONTENT_PATTERNS:
            if pattern.search(data):
                findings.append(f"{relative}: contains {label}")

    return findings


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Check tracked files for private project-state leakage."
    )
    result.add_argument(
        "--root",
        default=".",
        help="Git repository root. Defaults to the current directory.",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    root = Path(args.root).resolve()
    findings = scan_repository(root, tracked_paths(root))
    if findings:
        print("PUBLIC_RELEASE_CHECK_FAILED")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("PUBLIC_RELEASE_CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
