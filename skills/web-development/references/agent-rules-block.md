# Agent rules block

Copy this into the project's own rules file — `AGENTS.md`, `.cursor/rules/*.mdc`,
`.kilocode/rules/` — so the agent reads it on every turn instead of being told once.

## Agent rules block (copy into the project's rules file)

```
## Stack rules
- Use Next.js App Router with TypeScript.
- Prefer Server Components unless interactivity clearly requires a Client Component.
- Use Tailwind CSS for layout and tokens.
- Keep WebGL code inside components/scene/*.

## Quality gates
- pnpm lint
- pnpm test
- pnpm test:e2e
- pnpm lhci

## Performance budgets
- Keep route JS lean.
- LCP < 2.5s.  INP < 200ms.  CLS < 0.1.

## Accessibility
- Respect prefers-reduced-motion.
- Every 3D scene needs equivalent text and a static fallback image.

## Reusability standards
Four layers, each with one job:
- Components = UI rendering only; no business logic, no API calls.
- Hooks = reusable state/effect logic (`use` prefix, `hooks/` directory).
- Utilities = stateless pure functions (`utils/` or `helpers/`).
- Services = business workflows, API integrations (`services/`).
- Never inline API calls in components; never duplicate hook logic in pages.

## Review expectations
- Do not add new dependencies without justification.
- Prefer editing existing components over creating new abstractions.
- Include tests for interaction changes.
```
