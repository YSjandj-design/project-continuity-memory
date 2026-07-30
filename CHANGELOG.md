# Changelog

All notable changes to this project will be documented in this file.

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
