# Project Continuity Memory

**Resume the project, not the conversation.**

[简体中文](README.zh-CN.md)

Project Continuity Memory is a local-first, repo-native handoff protocol that lets
AI agents resume long-running work from verified project state instead of
reconstructing it from chat history.

It uses two small files:

- `PROJECT_MEMORY.md` stores stable project knowledge.
- `HANDOFF.md` stores the current objective, verified progress, blockers, evidence,
  and exact next action.

The bundled Agent Skill teaches compatible agents when to read them, how to resolve
stale state, and what to write back. The bundled validator keeps the files compact
and rejects incomplete handoffs.

## Why this exists

Every long-running agent workflow eventually hits a cold start: a new task, a new
window, a different model, a compacted context, or a human taking over.

Conversation persistence and project-state continuity are different problems. A
restored transcript may contain everything that happened while still leaving the
next agent unable to answer:

- What is true now?
- Which decisions are still binding?
- What was actually verified?
- Where is the evidence?
- What is the next executable action?

Project Continuity Memory turns those questions into a small, version-controlled
contract.

## The advantage

- **State, not recollection:** it records the verified current project state, not
  everything anyone said.
- **Two-speed memory:** durable knowledge and the live handoff evolve separately,
  so one file does not become either bloated or forgetful.
- **Evidence before memory:** current instructions, files, tests, and external state
  outrank stale notes.
- **Low-context recovery:** read two concise files, then open only the few sources
  needed for the current objective.
- **An executable handoff:** blockers, validation evidence, and the exact next action
  are first-class fields.
- **Auditable by default:** plain Markdown lives beside the work and can be reviewed
  with normal repository history.
- **Private by architecture:** no hosted service, telemetry, account, database,
  embeddings, or network access.
- **Portable and lightweight:** one open Agent Skill, one dependency-free Python
  utility, and no framework lock-in.

## How it compares

These approaches are complementary. Project Continuity Memory is deliberately
narrower: it owns the **verified project handoff**, while other systems keep doing
the jobs they are good at.

| Approach | Primary job | What it does well | What Project Continuity Memory adds |
|---|---|---|---|
| Conversation and user memory, such as [Mem0](https://github.com/mem0ai/mem0) or [Letta](https://github.com/letta-ai/letta) | Remember users, conversations, and agent experience | Personalization and long-term agent behavior | A compact statement of current project truth, evidence, binding decisions, and the next action |
| Runtime checkpointing, such as [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Resume graph execution state | Fault tolerance, replay, and thread-level checkpoints | Human-readable, framework-neutral continuity for the whole repository |
| Semantic knowledge systems, such as [Basic Memory](https://github.com/basicmachines-co/basic-memory) | Store and retrieve a broad body of knowledge | Search, discovery, and connected notes | A fixed recovery contract that resists stale or irrelevant retrieval |
| Task trackers, such as [GitHub Projects](https://docs.github.com/issues/planning-and-tracking-with-projects) | Track planned work, issues, and ownership | Priorities, views, assignments, and progress tracking | Why the current state is believed, what was verified, and how to resume safely |
| A single ad-hoc handoff note | Leave a quick message for the next worker | Simple to start | Stable knowledge separated from volatile status, plus conflict rules and validation |

The shortest mental model:

> Chat history tells the story. A task tracker tells the plan. A memory system
> retrieves the past. Project Continuity Memory tells the next agent what is true
> now, why, and what to do next.

## When it fits

Use it when:

- work continues across tasks, windows, models, agents, or people;
- the repository outlives any one conversation;
- resuming from the wrong or stale state would be costly;
- humans need to inspect, correct, and version the handoff;
- a database or hosted memory service would be unnecessary infrastructure.

Skip it for one-off questions, disposable experiments, pure conversation memory, or
projects that already have an equivalent verified-state handoff protocol.

## Design goals

- **Repo-native:** plain Markdown beside the work.
- **Local-first:** no account, server, database, embeddings, or network access.
- **Evidence-first:** project files and current state outrank memory notes.
- **Low-context:** start from two concise files, then open only relevant sources.
- **Auditable:** decisions, progress, and next actions point back to evidence.
- **Agent-portable:** packaged using the open
  [Agent Skills specification](https://github.com/agentskills/agentskills).

## What it is not

- A personal-memory system
- A transcript archive
- A vector database or RAG service
- A replacement for source code, ADRs, plans, tests, or task trackers
- A promise that an agent will remember everything

It is the continuity layer between those systems.

## Repository layout

```text
project-continuity-memory/
├── SKILL.md
├── agents/
├── assets/
├── references/
└── scripts/
```

The repository root contains only public documentation, tests, CI, and release
governance. Real project continuity files are deliberately excluded from the
public repository.

## Privacy boundary

This repository is extracted from the generalized Skill, never from a user's
actual project memory.

The public release must not contain:

- global or project-local `AGENTS.md`;
- real `PROJECT_MEMORY.md` or `HANDOFF.md`;
- novel-writing handoffs, backups, transcripts, or private project artifacts;
- user home-directory paths, personal email addresses, or other identifying data;
- symlinks that resolve outside the repository.

All templates and test fixtures are fictional. CI runs
`scripts/check_public_release.py` to enforce this boundary on every push and pull
request.

## Install

Install with the Agent Skills installer:

```bash
npx skills add YSjandj-design/project-continuity-memory
```

Or install the Skill directory from a local clone:

```bash
# Codex
cp -R project-continuity-memory ~/.codex/skills/

# Claude Code
cp -R project-continuity-memory ~/.claude/skills/
```

Installed Skills are normally discovered at the start of a new agent task or
session; do not assume a running session hot-loads a newly installed Skill.

## Use

Ask the agent to continue an existing project, or invoke the Skill explicitly:

```text
Use project-continuity-memory to resume this project from its verified current
state and update the handoff when done.
```

For a project that does not have continuity files yet:

```bash
python3 project-continuity-memory/scripts/pcm.py init \
  --root /path/to/project \
  --project-name "My Project"
```

Fill the generated files with verified facts, then validate them:

```bash
python3 project-continuity-memory/scripts/pcm.py check \
  --root /path/to/project \
  --strict
```

## The recovery chain

1. Read `PROJECT_MEMORY.md` and `HANDOFF.md` completely.
2. Open only the 1–5 fact sources relevant to the current objective.
3. Resolve conflicts using current instructions and verifiable state first.
4. Perform the work.
5. Promote only durable, verified knowledge to `PROJECT_MEMORY.md`.
6. Rewrite `HANDOFF.md` to the true current handoff instead of appending a diary.
7. Run the strict validator.

This follows the broader agent-engineering principle of giving agents a map to the
repository rather than a giant always-loaded manual, as described in OpenAI's
[harness engineering](https://openai.com/index/harness-engineering/) write-up.

## Status

Version 0.1.0 is a validated release candidate, published at
[YSjandj-design/project-continuity-memory](https://github.com/YSjandj-design/project-continuity-memory).

See [CHANGELOG.md](CHANGELOG.md) for release notes and
[CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

Apache License 2.0. See [LICENSE](LICENSE).
