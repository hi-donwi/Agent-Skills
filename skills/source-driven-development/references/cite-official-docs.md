# Cite official documentation

Load this when detecting stack, fetching sources, or writing citations.

## Detect stack and versions

```
package.json    → Node/React/Vue/Angular/Svelte
composer.json   → PHP/Symfony/Laravel
requirements.txt / pyproject.toml → Python/Django/Flask
go.mod          → Go
Cargo.toml      → Rust
Gemfile         → Ruby/Rails
```

State what you found:

```
STACK DETECTED:
- React 19.1.0 (from package.json)
- Vite 6.2.0
- Tailwind CSS 4.0.3
→ Fetching official docs for the relevant patterns.
```

If versions are missing or ambiguous, **ask**. Don't guess.

## Source hierarchy

| Priority | Source | Example |
|----------|--------|---------|
| 1 | Official documentation | react.dev, docs.djangoproject.com |
| 2 | Official blog / changelog | react.dev/blog |
| 3 | Web standards references | MDN, web.dev, html.spec.whatwg.org |
| 4 | Browser/runtime compatibility | caniuse.com, node.green |

Never cite as primary: Stack Overflow, blog posts/tutorials, AI-generated docs, training data.

```
BAD:  Fetch the React homepage
GOOD: Fetch react.dev/reference/react/useActionState

BAD:  Search "django authentication best practices"
GOOD: Fetch docs.djangoproject.com/en/6.0/topics/auth/
```

When official sources conflict, surface the discrepancy and verify against the detected version.

## Docs vs existing code

```
CONFLICT DETECTED:
The existing codebase uses useState for form loading state,
but React 19 docs recommend useActionState for this pattern.
(Source: react.dev/reference/react/useActionState)

Options:
A) Use the modern pattern — consistent with current docs
B) Match existing code — consistent with the codebase
→ Which approach do you prefer?
```

Don't silently pick one.

## Citation rules

- Full URLs, not shortened
- Prefer deep links with anchors
- Quote the relevant passage for non-obvious decisions
- Include browser/runtime support data when recommending platform features
- If you cannot find documentation:

```
UNVERIFIED: I could not find official documentation for this
pattern. This is based on training data and may be outdated.
Verify before using in production.
```

Honesty about what you couldn't verify is more valuable than false confidence.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "I'm confident about this API" | Confidence is not evidence. Verify. |
| "Fetching docs wastes tokens" | Hallucinating an API wastes more. |
| "The docs won't have what I need" | If they don't cover it, the pattern may not be officially recommended. |
| "I'll just mention it might be outdated" | Either verify and cite, or flag unverified. Hedging is the worst option. |
| "This is a simple task, no need to check" | Simple tasks with wrong patterns become templates. |
