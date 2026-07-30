# Project Continuity Memory Protocol

## 1. Memory layers

### Global instructions

Global instruction files contain rules that apply across projects: when to look
for project continuity, how to read it, and when to write it back. Do not place
individual project state there.

### Stable project layer

`PROJECT_MEMORY.md` contains low-churn information:

- purpose, scope, and non-goals;
- long-lived workstreams and priorities;
- authoritative sources and when to read them;
- confirmed decisions that remain binding across tasks;
- project-specific conventions, acceptance methods, and recurring pitfalls.

### Active handoff layer

`HANDOFF.md` contains high-churn information:

- current objective and scope;
- verified progress;
- decisions and actual changes from the current phase;
- acceptance evidence;
- blockers, open questions, and exact next actions;
- protected files, backups, and recovery entry points.

### Fact and evidence layer

Source code, documents, data, tests, task systems, ADRs, plans, exports, and
external state are the project facts. Read them only when the current objective
requires them.

## 2. Root selection

Choose one root using this precedence:

1. The project path explicitly specified by the user.
2. The nearest parent containing `PROJECT_MEMORY.md` or `HANDOFF.md`.
3. A root declared by project-local agent instructions.
4. A Git root, project manifest, or clear workspace marker.
5. The current working directory.

In a large workspace, the nearest independent project's continuity files win.
Do not inject parent-workspace state into a child project that has its own state.

## 3. Recovery chain

Expand context progressively:

1. L0: global rules and durable user preferences already supplied by the agent
   runtime.
2. L1: read `PROJECT_MEMORY.md` and `HANDOFF.md` completely.
3. L2: read the 1–5 sources directly relevant to the current objective.
4. L3: read history, backups, and detailed evidence only for conflict,
   traceability, audit, or acceptance.

Before work, distinguish:

- verified facts;
- state that still needs verification;
- decisions already made by the user;
- the direct next action.

Do not read or repeat unrelated history to perform familiarity.

## 4. Creation and promotion

Create both continuity files when a continuing project first gains any of:

- a substantive result that later tasks must continue;
- a decision that changes future work;
- work spanning multiple steps, dates, or tasks;
- a paused state with verified progress, blockers, or a next action;
- an explicit request for durable project continuity.

Do not create them for one-off answers or trivial operations with no future state.

Promote information to `PROJECT_MEMORY.md` only when it:

- is explicitly confirmed by the user or verifiable from project facts;
- will likely affect multiple future tasks;
- is not merely a temporary handoff detail;
- does not duplicate a more authoritative document.

Rewrite `HANDOFF.md` after substantive work. Remove completed temporary details
that no longer affect resumption.

## 5. Conflict and stale state

Resolve conflicts in this order:

1. The user's latest explicit instruction.
2. Verifiable current disk or external state.
3. Authoritative project plans, tasks, or decisions.
4. `PROJECT_MEMORY.md`.
5. `HANDOFF.md`.
6. Conversation summaries or model recollection.

If a conflict changes task direction, state the conflict and the evidence used.
Fix stale continuity when safe. If evidence cannot decide, preserve both
possibilities as open questions instead of silently choosing.

## 6. Size budgets

| File | Target | Warning threshold | Hard limit |
|---|---:|---:|---:|
| `PROJECT_MEMORY.md` | up to 120 lines | 160 lines or 8,000 characters | 240 lines or 12,000 characters |
| `HANDOFF.md` | up to 80 lines | 100 lines or 4,000 characters | 140 lines or 6,000 characters |

When over target, remove duplication, completed temporary details, and content
that can be replaced by a link. Never meet a budget by removing binding decisions,
boundaries, blockers, or the next action.

## 7. Archive policy

Create `.project-memory/history/YYYY-MM-DD_<slug>.md` only when:

- a phase or milestone is complete;
- project direction changes materially;
- the handoff will be fully replaced but retains audit value;
- the user explicitly requests a snapshot.

History is evidence, not default recovery context. Do not archive every ordinary
conversation.

## 8. Hard failures

Continuity acceptance fails when any of these occurs:

- an agent claims to resume without reading existing continuity files;
- continuity conflicts with project facts and is not verified;
- a guess or model preference is recorded as a user decision;
- `HANDOFF.md` lacks an executable next action;
- a key artifact has no path or evidence;
- existing memory, backups, or another workstream are silently overwritten;
- credentials, secrets, or large unrelated transcripts are stored;
- full-history reading is required for every resume;
- a file exceeds its hard size limit.

## 9. Dynamic acceptance

Given only a project path and a request to continue, a fresh agent should:

1. locate the correct project root;
2. read both continuity files;
3. open the minimum relevant fact sources;
4. accurately state the current position and next action;
5. detect and correct a deliberately stale handoff using current evidence.
