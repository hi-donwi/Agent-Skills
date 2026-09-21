# Coding Standards

These are enforceable rules, not preferences. They convert "good taste" into policy and
prevent the main failure mode of agentic front-end work: impressive-looking output with
inconsistent structure, weak performance discipline, and missing tests.

## Stack rules
- Use **Next.js App Router** with **TypeScript** (strict mode, no `any`).
- Prefer **Server Components**; use a Client Component only when interactivity requires it.
- Use **Tailwind CSS** for layout and design tokens.
- Keep all **WebGL/3D code inside `components/scene/*`**.
- Default rendering posture: **server-first rendering + selective enhancement** — add
  client motion/3D only where it materially improves the experience.

## Recommended default stack
| Layer | Default |
|---|---|
| Framework | Next.js (App Router) + TypeScript |
| Content-heavy / editorial | Astro (HTML-first, selective islands) |
| Styling | Tailwind CSS |
| 3D / immersive | React Three Fiber + Drei (`<model-viewer>` for simple product viewers) |
| Motion | Framer Motion or GSAP (GSAP ScrollTrigger for scroll-driven 3D) |
| Deploy | Vercel or Cloudflare Workers |
| CI / quality | Playwright + Lighthouse CI + GitHub Actions |

## Quality gates (must pass in CI)
```
pnpm lint
pnpm test
pnpm test:e2e
pnpm lhci
```

## Performance budgets
- Keep route JS lean.
- **LCP < 2.5s · INP < 200ms · CLS < 0.1.**

## Accessibility
- Respect `prefers-reduced-motion`.
- Every 3D scene needs equivalent text and a static fallback image.

## Review expectations
- Do not add new dependencies without justification.
- Prefer editing existing components over creating new abstractions.
- Include tests for interaction changes.
- Enforce strict TypeScript; add JSDoc to non-obvious functions.

Run `node scripts/check-project.js` to verify a project against these rules.
