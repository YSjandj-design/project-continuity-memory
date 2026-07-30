---
name: project-continuity-memory
description: Maintain compact, verifiable continuity for long-running projects across agent tasks and sessions. Use when resuming, handing off, modifying, migrating, or pausing a project that has PROJECT_MEMORY.md or HANDOFF.md, or when substantive work first needs durable project state. Do not use for one-off questions, pure conversation, transcript storage, or global personal memory.
license: Apache-2.0
metadata:
  version: "0.1.0"
  source: "https://github.com/YSjandj-design/project-continuity-memory"
---

# Project Continuity Memory

Treat each agent task as one work session in the same project. Recover from a
small verified state, perform the work, then write back only the useful delta.

## Core files

- `PROJECT_MEMORY.md`: stable knowledge that remains useful across tasks.
- `HANDOFF.md`: the active objective, verified progress, evidence, blockers, and
  exact next action.
- `.project-memory/history/`: optional milestone snapshots that are not part of
  the default recovery chain.

These files are a map and handoff, not a second source of truth. Source code,
documents, data, ADRs, plans, tests, task systems, and external state remain
authoritative.

## Workflow

1. Locate one project root.
   - Prefer the path explicitly given by the user.
   - Otherwise use the nearest parent containing `PROJECT_MEMORY.md` or
     `HANDOFF.md`.
   - Otherwise use the clear repository or workspace root.
   - Ask only when different roots would materially change writes and current
     state cannot resolve the ambiguity.
2. Decide whether continuity applies.
   - Resume, handoff, modification, creation, migration, deployment, writing,
     validation, or paused multi-step work: use this workflow.
   - One-off answer, unrelated read-only query, or pure conversation: do not
     create or update continuity files.
3. Recover context.
   - Read `PROJECT_MEMORY.md` and `HANDOFF.md` completely.
   - Open only the 1–5 fact sources directly relevant to the current objective.
   - Verify paths, artifacts, task state, and cited evidence.
   - Correct stale continuity state before following it.
4. Perform the work.
   - Track completed, decided, unverified, and next-step deltas internally.
   - Preserve user files, backups, and unrelated work.
5. Close the session.
   - Promote only durable, verified knowledge to `PROJECT_MEMORY.md`.
   - Rewrite `HANDOFF.md` to the true current handoff; do not append a diary.
   - Run `scripts/pcm.py check --root <project-root> --strict`.
   - Report what changed, how it was verified, and what remains.

Read [references/protocol.md](references/protocol.md) when resolving conflicts,
managing size limits, archiving a handoff, or assessing a continuity failure.

## Initialize a project

When substantive project state now exists and both files are missing:

```bash
python3 <skill-dir>/scripts/pcm.py init \
  --root <project-root> \
  --project-name "<project-name>"
```

`init` creates only missing files and never overwrites existing ones. Replace all
empty template fields with verified project facts, then run:

```bash
python3 <skill-dir>/scripts/pcm.py check \
  --root <project-root> \
  --strict
```

The validator checks structure, unresolved fields, required active-state content,
and size budgets. It cannot prove that project claims are true; verify those
against the actual project.

Templates:

- [assets/project-memory-template.md](assets/project-memory-template.md)
- [assets/handoff-template.md](assets/handoff-template.md)

## Write boundaries

- Do not copy global identity, personality, or universal preferences into a
  project.
- Do not store passwords, tokens, private keys, credentials, or unrelated
  sensitive data.
- Do not write model guesses as user decisions.
- Do not paste full conversations, long documents, source code, or logs.
- Link to existing project systems rather than duplicating their content.
- Use Waggle or another audit mechanism for immutable cross-agent receipts when
  needed; it complements rather than replaces this protocol.

## Definition of done

- A fresh agent can identify the current project position from the two files and
  a few linked sources.
- Every important state can be traced to project evidence.
- `HANDOFF.md` contains an executable next action.
- Strict validation passes.
- Dynamic verification finds no material drift.
- Default recovery remains compact.
