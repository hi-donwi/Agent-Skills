# Web Development — Aider Conventions

Use with Aider:  `aider --read .agents/skills/web-development/adapters/aider-conventions.md`
(or add it under `read:` in `.aider.conf.yml`). Full skill: `.agents/skills/web-development/SKILL.md`.

## Conventions
- Stack: Next.js App Router + TypeScript (strict, no `any`) + Tailwind CSS.
- Server Components by default; add `"use client"` only for genuine interactivity, in the
  smallest island possible.
- Keep WebGL/3D code under `components/scene/`.
- Fetch data on the server with caching; never expose secrets to the client.
- Accessibility: respect `prefers-reduced-motion`; 3D scenes need a text equivalent + static
  fallback; label interactive elements; one logical heading order.
- Performance budgets: LCP < 2.5s, INP < 200ms, CLS < 0.1.
- Don't add dependencies without justification; prefer editing existing components; add tests
  for interaction changes.
- Make changes in small, reviewable steps.
