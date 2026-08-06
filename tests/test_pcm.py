from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY / "project-continuity-memory" / "scripts" / "pcm.py"

COMPLETE_PROJECT_MEMORY = """# Project Memory

## Project identity
- Project: Example

## Long-term goal and boundaries
- Goal: Ship a verified example.

## Active workstreams
| Workstream | Status | Current focus | Source of truth |
|---|---|---|---|
| Core | Active | Validation | `src/` |

## Durable decisions
- Keep the core local.

## Key sources of truth
| Path | Purpose | Read when |
|---|---|---|
| `src/` | Implementation | Editing behavior |

## Project conventions
- Run tests before handoff.

## Known pitfalls
- Static checks do not prove facts.

## Maintenance rules
- Keep this file compact.
"""

COMPLETE_HANDOFF = """# Current Handoff

## Handoff status
- Project: Example

## Current objective
- Verify the release.

## Start here
1. Run the test suite.

## Verified current state
- The fixture is complete.

## Decisions this session
- No new decisions.

## Recent changes and evidence
- Tests cover strict validation.

## Blockers and open questions
- None.

## Next step
1. Publish the verified result.

## Protection and recovery
- Preserve existing project files.

## Integrity rules
- Correct stale state before continuing.
"""


class PcmCliTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        return result, payload

    def write_scope_pair(self, root: Path, kind: str) -> None:
        memory = COMPLETE_PROJECT_MEMORY.replace(
            "## Project identity\n- Project: Example",
            (
                "## Project identity\n"
                f"- Project: Example\n- Root: `{root.resolve()}`\n"
                f"- Project kind: {kind}"
            ),
        )
        (root / "PROJECT_MEMORY.md").write_text(memory, encoding="utf-8")
        (root / "HANDOFF.md").write_text(COMPLETE_HANDOFF, encoding="utf-8")

    def test_init_creates_both_files(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            result, payload = self.run_cli(
                "init", "--root", root, "--project-name", "Example"
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(
                payload["created"], ["PROJECT_MEMORY.md", "HANDOFF.md"]
            )
            self.assertNotIn(
                "{{",
                (Path(root) / "PROJECT_MEMORY.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "- Project kind: single-project",
                (Path(root) / "PROJECT_MEMORY.md").read_text(encoding="utf-8"),
            )

    def test_init_never_overwrites_existing_files(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            self.run_cli("init", "--root", root, "--project-name", "Example")
            memory = Path(root) / "PROJECT_MEMORY.md"
            original = memory.read_text(encoding="utf-8") + "\nSENTINEL\n"
            memory.write_text(original, encoding="utf-8")

            result, payload = self.run_cli(
                "init", "--root", root, "--project-name", "Changed"
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["created"], [])
            self.assertEqual(
                payload["skipped_existing"], ["PROJECT_MEMORY.md", "HANDOFF.md"]
            )
            self.assertEqual(memory.read_text(encoding="utf-8"), original)

    def test_strict_check_rejects_unfilled_templates(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            self.run_cli("init", "--root", root, "--project-name", "Example")
            result, payload = self.run_cli("check", "--root", root, "--strict")
            self.assertEqual(result.returncode, 1)
            self.assertFalse(payload["ok"])
            errors = [
                error
                for item in payload["files"]
                for error in item.get("errors", [])
            ]
            self.assertTrue(
                any("empty template fields" in error for error in errors)
            )

    def test_strict_check_accepts_complete_files(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            Path(root, "PROJECT_MEMORY.md").write_text(
                COMPLETE_PROJECT_MEMORY, encoding="utf-8"
            )
            Path(root, "HANDOFF.md").write_text(
                COMPLETE_HANDOFF, encoding="utf-8"
            )
            result, payload = self.run_cli("check", "--root", root, "--strict")
            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])

    def test_check_rejects_missing_file(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            Path(root, "PROJECT_MEMORY.md").write_text(
                COMPLETE_PROJECT_MEMORY, encoding="utf-8"
            )
            result, payload = self.run_cli("check", "--root", root)
            self.assertEqual(result.returncode, 1)
            self.assertFalse(payload["ok"])
            handoff = next(
                item for item in payload["files"] if item["file"] == "HANDOFF.md"
            )
            self.assertEqual(handoff["errors"], ["missing"])

    def test_scope_resolves_single_project_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_scope_pair(root, "single-project")
            child = root / "docs"
            child.mkdir()

            result, payload = self.run_cli("scope", "--path", str(child))

            self.assertEqual(result.returncode, 0)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["status"], "resolved")
            self.assertEqual(payload["scope"], str(root.resolve()))

    def test_scope_blocks_orphaned_parent_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "HANDOFF.md").write_text(COMPLETE_HANDOFF, encoding="utf-8")
            child = root / "story-a"
            child.mkdir()

            result, payload = self.run_cli("scope", "--path", str(child))

            self.assertEqual(result.returncode, 1)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["status"], "blocked_by_orphan")
            self.assertIn(str(root.resolve()), payload["orphan_scopes"])

    def test_scope_prefers_child_pair_over_orphan_parent_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "HANDOFF.md").write_text(COMPLETE_HANDOFF, encoding="utf-8")
            child = root / "story-a"
            child.mkdir()
            self.write_scope_pair(child, "single-project")

            result, payload = self.run_cli("scope", "--path", str(child))

            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["status"], "resolved")
            self.assertEqual(payload["scope"], str(child.resolve()))

    def test_scope_requires_child_pair_under_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_scope_pair(root, "workspace")
            child = root / "story-a"
            child.mkdir()

            result, payload = self.run_cli("scope", "--path", str(child))

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["status"], "workspace_requires_child_scope")

            self.write_scope_pair(child, "single-project")
            result, payload = self.run_cli("scope", "--path", str(child))

            self.assertEqual(result.returncode, 0)
            self.assertEqual(payload["scope"], str(child.resolve()))

    def test_scope_rejects_mismatched_declared_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_scope_pair(root, "single-project")
            memory = root / "PROJECT_MEMORY.md"
            memory.write_text(
                memory.read_text(encoding="utf-8").replace(
                    f"- Root: `{root.resolve()}`", "- Root: `/workspace/other`"
                ),
                encoding="utf-8",
            )

            result, payload = self.run_cli("scope", "--path", str(root))

            self.assertEqual(result.returncode, 1)
            self.assertEqual(payload["status"], "declared_root_mismatch")


if __name__ == "__main__":
    unittest.main()
