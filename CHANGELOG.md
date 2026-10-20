# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

- Explicit continuity-scope rules for multi-project workspaces and nested child
  projects.
- A `pcm.py scope` resolver that blocks orphaned parent handoffs, workspace
  fallback, and mismatched declared roots.
- Regression coverage for child-project isolation and safe parent inheritance.
- README comparison of the 1.0 and 2.0 protocol lines.

### Changed

- Continuity files are now treated as a co-located pair rather than selecting
  the nearest ancestor containing either file.
- Character-budget warnings and hard limits are now 6,000/8,000 for
  `HANDOFF.md` and 10,000/14,000 for `PROJECT_MEMORY.md`.

### Security

- The public-release privacy gate now scans its own source and accepts optional
  `--private-name` markers instead of embedding a real person's name.

## 0.1.0 - 2026-07-30

### Added

- Two-layer project continuity protocol using `PROJECT_MEMORY.md` and `HANDOFF.md`.
- Agent Skill workflow for cold-start recovery, evidence precedence, and writeback.
- Dependency-free Python initializer and strict static validator.
- English and Simplified Chinese project documentation.
- Standard-library regression test suite and GitHub Actions workflow.
- Public-release privacy gate that blocks real memory, handoff, agent instruction,
  backup, user-path, email, private-name, and external-symlink leakage.

### Changed

- The public edition uses English schema headings for cross-language portability.
- Strict validation now rejects unresolved and empty template fields.

### Security

- No network access, telemetry, credential access, command execution, or destructive
  file operations are used by the bundled validator.
- Real project continuity files and private development state are excluded from the
  public repository and its clean release history.
