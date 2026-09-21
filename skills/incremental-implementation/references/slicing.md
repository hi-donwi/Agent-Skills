# Slicing and increment rules

Load this when choosing how to cut work or applying the implementation rules.

## Vertical slices (preferred)

One complete path through the stack:

```
Slice 1: Create a task (DB + API + basic UI)
    → Tests pass, user can create a task via the UI

Slice 2: List tasks (query + API + UI)
    → Tests pass, user can see their tasks

Slice 3: Edit a task (update + API + UI)
    → Tests pass, user can modify tasks

Slice 4: Delete a task (update + API + UI + confirmation)
    → Tests pass, full CRUD complete
```

## Contract-first slicing

When backend and frontend need to develop in parallel:

```
Slice 0: Define the API contract (types, interfaces, OpenAPI spec)
Slice 1a: Implement backend against the contract + API tests
Slice 1b: Implement frontend against mock data matching the contract
Slice 2: Integrate and test end-to-end
```

## Risk-first slicing

```
Slice 1: Prove the WebSocket connection works (highest risk)
Slice 2: Build real-time task updates on the proven connection
Slice 3: Add offline support and reconnection
```

If Slice 1 fails, you discover it before investing in Slices 2 and 3.

## Implementation rules

**Rule 0 — Simplicity first.** What is the simplest thing that could work? Three similar lines beat a premature abstraction. Optimize only after tests prove correctness.

```
SIMPLICITY CHECK:
✗ Generic EventBus with middleware pipeline for one notification
✓ Simple function call

✗ Abstract factory pattern for two similar components
✓ Two straightforward components with shared utilities

✗ Config-driven form builder for three forms
✓ Three form components
```

**Rule 0.5 — Scope discipline.** Touch only what the task requires. Note adjacent issues; do not fix them here.

**Rule 1 — One thing at a time.** Don't mix a new component, a refactor, and a build-config change in one increment.

**Rule 2 — Keep it compilable.** Existing tests pass between slices.

**Rule 3 — Feature flags for incomplete features.** Merge increments without exposing unfinished work.

**Rule 4 — Safe defaults.** New behaviour opt-in.

**Rule 5 — Rollback-friendly.** Additive changes; focused modifications; migrations with rollbacks. Don't delete and replace in the same commit.

## Directing an agent

```
Start with just the database schema change and the API endpoint.
Don't touch the UI yet — we'll do that in the next increment.
After implementing, run the test suite and the build.
```

## Increment checklist

- [ ] The change does one thing and does it completely
- [ ] All existing tests still pass
- [ ] The build succeeds
- [ ] Type checking and linting pass where the project has them
- [ ] The new functionality works as expected
- [ ] The change is committed with a descriptive message

Run each verification command after a change that could affect it. After a successful run, don't repeat the same command unless the code has changed.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "I'll test it all at the end" | Bugs compound. A bug in Slice 1 makes Slices 2-5 wrong. Test each slice. |
| "It's faster to do it all at once" | It *feels* faster until something breaks and you can't find which of 500 changed lines caused it. |
| "These changes are too small to commit separately" | Small commits are free. Large commits hide bugs and make rollbacks painful. |
| "I'll add the feature flag later" | If the feature isn't complete, it shouldn't be user-visible. Add the flag now. |
| "This refactor is small enough to include" | Refactors mixed with features make both harder to review and debug. Separate them. |
| "Let me run the build command again just to be sure" | After a successful run, repeating the same command adds nothing unless the code has changed. |
