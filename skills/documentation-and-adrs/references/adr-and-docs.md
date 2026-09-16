# ADR and documentation patterns

Load this when writing an ADR, comments, API docs, or a README.

## When to write an ADR

- Choosing a framework, library, or major dependency
- Designing a data model or database schema
- Selecting an authentication strategy
- Deciding on an API architecture (REST vs GraphQL vs RPC)
- Choosing between build tools, hosting platforms, or infrastructure
- Any decision that would be expensive to reverse

Store ADRs in `docs/decisions/` with sequential numbering.

```markdown
# ADR-001: Use PostgreSQL for primary database

## Status
Accepted | Superseded by ADR-XXX | Deprecated

## Date
2026-01-15

## Context
We need a primary database. Key requirements:
- Relational data model with ACID transactions
- Full-text search
- Managed hosting available

## Decision
Use PostgreSQL with the project's chosen ORM.

## Alternatives Considered

### Document store
- Pros: Flexible schema
- Cons: Data is inherently relational
- Rejected: Relationships would be manual or duplicated

### Embedded SQL
- Pros: Zero configuration
- Cons: Limited concurrent writes, no managed production hosting
- Rejected: Not suitable for a multi-user web application

## Consequences
- Type-safe access and migrations
- Team needs PostgreSQL knowledge (standard skill)
- Hosting on a managed service
```

Lifecycle: `PROPOSED → ACCEPTED → (SUPERSEDED or DEPRECATED)`. Don't delete old ADRs. When a decision changes, write a new ADR that supersedes the old one.

## Inline comments

Comment the *why*, not the *what*:

```typescript
// BAD: Restates the code
// Increment counter by 1
counter += 1;

// GOOD: Explains non-obvious intent
// Rate limit uses a sliding window — reset at the window boundary,
// not on a fixed schedule, to prevent burst attacks at window edges
if (now - windowStart > WINDOW_SIZE_MS) {
  counter = 0;
  windowStart = now;
}
```

Do not comment self-explanatory code. Do not leave TODOs you could do now. Do not leave commented-out code — git has history.

Document known gotchas next to the trap:

```typescript
/**
 * IMPORTANT: Call before the first render. After hydration this causes
 * a flash of unstyled content because the theme context is missing during SSR.
 *
 * See ADR-003 for the full design rationale.
 */
export function initializeTheme(theme: Theme): void {
  // ...
}
```

## API documentation

Prefer types for libraries:

```typescript
/**
 * Creates a new task.
 *
 * @param input - Task creation data (title required, description optional)
 * @returns The created task with server-generated ID and timestamps
 * @throws {ValidationError} If title is empty or exceeds 200 characters
 */
export async function createTask(input: CreateTaskInput): Promise<Task> {
  // ...
}
```

For HTTP, commit OpenAPI. Adding an error means adding an `ErrorCode`, not a new response shape. See `rest-api-contract`.

## README

Every project README covers: one-paragraph purpose, quick start, commands table, architecture (link ADRs), contributing.

## Changelog

Shipped features: Added / Fixed / Changed under a dated version heading. Generation of that file is `changelog-generator`; this skill is the shape, not the git mining.

## Documentation for agents

- Rules files (CLAUDE.md etc.) — conventions
- Spec files — what to build
- ADRs — why past decisions were made
- Inline gotchas — traps not to repeat

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "The code is self-documenting" | Code shows what. It doesn't show why, what alternatives were rejected, or what constraints apply. |
| "We'll write docs when the API stabilizes" | APIs stabilize faster when you document them. The doc is the first test of the design. |
| "Nobody reads docs" | Agents do. Future engineers do. Your 3-months-later self does. |
| "ADRs are overhead" | A 10-minute ADR prevents a 2-hour debate about the same decision six months later. |
| "Comments get outdated" | Comments on *why* are stable. Comments on *what* get outdated — that's why you only write the former. |
