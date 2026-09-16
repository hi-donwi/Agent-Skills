# Task and plan templates

Load this when writing `tasks/plan.md` or `tasks/todo.md`.

## Dependency graph

Implementation order follows the graph bottom-up: foundations first (schema → types → endpoints → client → UI; plus seed/migrations).

## Vertical vs horizontal

**Bad (horizontal):** entire schema, then all API, then all UI, then connect.

**Good (vertical):** user can register (schema + API + UI); then log in; then create a task; then list tasks. Each slice is working and testable.

## Task card

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Tests pass: `npm test -- --grep "feature-name"`
- [ ] Build succeeds: `npm run build`
- [ ] Manual check: [description of what to verify]

**Dependencies:** [Task numbers this depends on, or "None"]

**Files likely touched:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [Small: 1-2 files | Medium: 3-5 files | Large: 5+ files]
```

## Checkpoints

```markdown
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Core user flow works end-to-end
- [ ] Review with human before proceeding
```

## Sizing

| Size | Files | Scope | Example |
|------|-------|-------|---------|
| **XS** | 1 | Single function or config change | Add a validation rule |
| **S** | 1-2 | One component or endpoint | Add a new API endpoint |
| **M** | 3-5 | One feature slice | User registration flow |
| **L** | 5-8 | Multi-component feature | Search with filtering and pagination |
| **XL** | 8+ | **Too large — break it down further** | — |

Break a task down when it would take more than one focused session, acceptance criteria need more than three bullets, it touches two independent subsystems, or the title contains "and".

## Output files

- Plan: `tasks/plan.md`
- Task list: `tasks/todo.md`

Create `tasks/` if needed. Downstream tooling (`/build`) expects these paths.

## Plan document

```markdown
# Implementation Plan: [Feature/Project Name]

## Overview
[One paragraph]

## Architecture Decisions
- [Key decision and rationale]

## Task List

### Phase 1: Foundation
- [ ] Task 1: ...

### Checkpoint: Foundation
- [ ] Tests pass, builds clean

### Phase 2: Core Features
- [ ] Task 3: ...

### Checkpoint: Core Features
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: ...

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```

## Parallelization

- **Safe:** independent feature slices, tests for already-implemented features, documentation
- **Sequential:** database migrations, shared state, dependency chains
- **Coordinate:** features that share an API contract — define the contract first

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | That's how you end up with a tangled mess and rework. 10 minutes of planning saves hours. |
| "The tasks are obvious" | Write them down anyway. Explicit tasks surface hidden dependencies and forgotten edge cases. |
| "Planning is overhead" | Planning is the task. Implementation without a plan is just typing. |
| "I can hold it all in my head" | Context windows are finite. Written plans survive session boundaries and compaction. |
