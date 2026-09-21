# Spec template

Load this in the Specify phase.

## Assumptions first

```
ASSUMPTIONS I'M MAKING:
1. This is a web application (not native mobile)
2. Authentication uses session-based cookies (not JWT)
3. The database is PostgreSQL (based on the existing schema)
4. We're targeting modern browsers only
→ Correct me now or I'll proceed with these.
```

Don't silently fill in ambiguous requirements.

## Six core areas

1. **Objective** — What are we building and why? Who is the user? What does success look like?
2. **Commands** — Full executable commands with flags, not just tool names.
3. **Project Structure** — Where source, tests, and docs live.
4. **Code Style** — One real snippet beats three paragraphs. Naming, formatting, good output.
5. **Testing Strategy** — Framework, locations, coverage, which level for which concern.
6. **Boundaries**
   - **Always do:** tests before commits, naming conventions, validate inputs
   - **Ask first:** schema changes, new dependencies, CI config
   - **Never do:** commit secrets, edit vendor directories, remove failing tests without approval

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions]

## Commands
[Build, test, lint, dev — full commands]

## Project Structure
[Directory layout with descriptions]

## Code Style
[Example snippet + key conventions]

## Testing Strategy
[Framework, test locations, coverage requirements, test levels]

## Boundaries
- Always: [...]
- Ask first: [...]
- Never: [...]

## Success Criteria
[How we'll know this is done — specific, testable conditions]

## Open Questions
[Anything unresolved that needs human input]
```

## Reframe instructions as success criteria

```
REQUIREMENT: "Make the dashboard faster"

REFRAMED SUCCESS CRITERIA:
- Dashboard LCP < 2.5s on 4G connection
- Initial data load completes in < 500ms
- No layout shift during load (CLS < 0.1)
→ Are these the right targets?
```

## Keep the spec alive

Update when decisions or scope change. Commit it. Link the spec section each PR implements.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | Simple tasks don't need *long* specs, but they still need acceptance criteria. A two-line spec is fine. |
| "I'll write the spec after I code it" | That's documentation, not specification. The spec's value is in forcing clarity *before* code. |
| "The spec will slow us down" | A 15-minute spec prevents hours of rework. |
| "Requirements will change anyway" | That's why the spec is a living document. An outdated spec is still better than no spec. |
| "The user knows what they want" | Even clear requests have implicit assumptions. The spec surfaces those assumptions. |
