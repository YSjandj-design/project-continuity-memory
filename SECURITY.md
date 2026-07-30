# Security Policy

Project Continuity Memory is designed to operate entirely on local, user-selected
project directories.

The core validator:

- does not use the network;
- does not read credentials or environment files;
- does not execute shell commands;
- does not delete project files;
- creates only missing continuity files during `init`;
- refuses to overwrite existing continuity files.

## Public-release boundary

The repository itself must never contain real user memory or private project
state. `scripts/check_public_release.py` rejects:

- `AGENTS.md`, `PROJECT_MEMORY.md`, and `HANDOFF.md`;
- backup directories and backup files;
- macOS, Linux, or Windows user-home paths;
- personal email addresses and private-name markers;
- private-key material;
- symlinks that resolve outside the repository.

Templates and fixtures must use fictional names, paths, and project facts.

## Reporting a vulnerability

Use the repository's
[private vulnerability reporting](https://github.com/YSjandj-design/project-continuity-memory/security/advisories/new)
channel when available.

Please do not include real credentials, private project data, or exploit payloads
that affect third-party systems in a public issue.
