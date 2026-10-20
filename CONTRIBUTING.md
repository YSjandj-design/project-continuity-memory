# Contributing

Contributions are welcome when they keep Project Continuity Memory small,
auditable, and agent-portable.

## Principles

- Project facts remain the source of truth.
- Stable memory and active handoff have different lifetimes.
- Recovery begins with the smallest useful context.
- Memory files index evidence; they do not duplicate it.
- A strict check must be mechanically meaningful.
- No network service or external dependency is required for the core workflow.

## Development

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

Run the public-release privacy gate:

```bash
python3 scripts/check_public_release.py
```

## Pull requests

Please include:

- the failure mode or continuity problem being addressed;
- why the change belongs in the core protocol rather than an optional integration;
- tests for validator behavior changes;
- documentation updates for any user-visible behavior;
- confirmation that no private paths, credentials, or real project data were added.

Pull requests fail when they include real continuity files, agent instruction
files, backups, user paths, personal email addresses, configured private-name
markers, or external symlinks. Use fictional fixtures only.

Large additions such as databases, embeddings, hosted services, or automatic
transcript capture should be proposed as optional integrations, not added to the
dependency-free core by default.
