# Web Development — Copilot Instructions

Drop into `.github/copilot-instructions.md` (or append to it) to apply these standards in
GitHub Copilot. Full skill: `.agents/skills/web-development/SKILL.md`.

When working on website/web-app code in this repo:

- Use **Next.js App Router** with **TypeScript** in strict mode. Never use `any`.
- Default to **Server Components**; only add `"use client"` when state, effects, or event
  handlers are required, and isolate that into the smallest possible island.
- Style with **Tailwind CSS** tokens. Keep all WebGL/3D code under `components/scene/`.
- Fetch data on the server with caching; never ship secrets to the client.
- Respect `prefers-reduced-motion`. Every 3D scene needs a text equivalent and a static
  fallback image.
- Honor performance budgets: LCP < 2.5s, INP < 200ms, CLS < 0.1.
- Don't introduce new dependencies without justification. Prefer editing existing components
  over new abstractions. Add tests for interaction changes.
- Provide accessible labels on interactive elements and a single logical heading order.
