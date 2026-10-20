from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY / "scripts" / "check_public_release.py"
SPEC = importlib.util.spec_from_file_location("check_public_release", SCRIPT)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class PublicReleaseBoundaryTests(unittest.TestCase):
    def scan(
        self, files: dict[str, bytes | str], private_names: list[str] | None = None
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths: list[Path] = []
            for relative_raw, content in files.items():
                relative = Path(relative_raw)
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                if isinstance(content, bytes):
                    target.write_bytes(content)
                else:
                    target.write_text(content, encoding="utf-8")
                paths.append(relative)
            return CHECKER.scan_repository(root, paths, private_names)

    def test_fictional_public_fixture_passes(self) -> None:
        findings = self.scan(
            {
                "examples/example.md": (
                    "# Example\n\nProject: Atlas\nRoot: /workspace/atlas\n"
                )
            }
        )
        self.assertEqual(findings, [])

    def test_real_continuity_filename_is_rejected(self) -> None:
        findings = self.scan({"PROJECT_MEMORY.md": "# Private state"})
        self.assertTrue(any("forbidden private filename" in item for item in findings))

    def test_user_home_path_is_rejected(self) -> None:
        private_path = "Root: /" + "Users/example/private"
        findings = self.scan({"example.md": private_path})
        self.assertTrue(any("macOS user-home path" in item for item in findings))

    def test_email_and_configured_private_name_are_rejected(self) -> None:
        private_marker = "Morgan <person" + "@example.com>"
        findings = self.scan(
            {"example.md": private_marker}, private_names=["Morgan"]
        )
        self.assertTrue(any("email address" in item for item in findings))
        self.assertTrue(
            any("configured private-name marker" in item for item in findings)
        )

    def test_checker_source_is_not_exempt_from_content_scanning(self) -> None:
        private_path = "Root: /" + "Users/example/private"
        findings = self.scan({"scripts/check_public_release.py": private_path})
        self.assertTrue(any("macOS user-home path" in item for item in findings))

    def test_external_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            link = root / "outside-link"
            link.symlink_to("/private/tmp/outside")
            findings = CHECKER.scan_repository(root, [Path("outside-link")])
            self.assertTrue(
                any("symlink resolves outside repository" in item for item in findings)
            )


if __name__ == "__main__":
    unittest.main()
