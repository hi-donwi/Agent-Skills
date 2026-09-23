# Default stack and choosing a tool

Load when picking the stack for a new project or deciding which tool to build it in.

Everything here is dated by nature — product names, capabilities and prices move faster
than this library does. Treat it as a starting point to verify, not as a fact.

## Recommended default stack

| Layer | Default | Notes |
|---|---|---|
| Framework | **Next.js (App Router) + TypeScript** | React 19; Server Components by default; Client only when interactivity needs it |
| Content-heavy / editorial | **Astro** | HTML-first with selective islands |
| Styling | **Tailwind CSS v4** | Layout + design tokens — shared language with the agent |
| UI kit | **shadcn/ui** | Component variants, a11y states |
| 3D / immersive | **React Three Fiber + Drei** | Keep all WebGL in `components/scene/*`; dynamic import, `ssr: false` |
| Motion | **Framer Motion** or **GSAP + ScrollTrigger** | GSAP/ScrollTrigger for scroll-driven 3D narratives |
| Deploy | **Vercel** or **Cloudflare Workers** | |
| CI / quality | **Playwright + Lighthouse CI + GitHub Actions** | Enforce budgets in CI |

Guiding principle for premium sites: **server-first rendering plus selective enhancement** —
add client-side motion and 3D only where it materially improves the experience.

## Choosing the right tool

| Goal | Tool | Typical time |
|---|---|---|
| UI demo / meeting tomorrow | **v0** (Vercel) | ~4 hours |
| MVP full-stack weekend | **Lovable**, **Bolt.new**, **Base44** | ~7–8 hours |
| Production codebase | **Cursor**, **Claude Code**, **Windsurf** | 5–12 hours |
| Award-style 3D portfolio | **Cursor** + manual R3F/GSAP | 2–5 days |
| 3D scene scaffolding | Three.js / R3F via coding agent | varies |

- **UI components / rapid prototyping:** v0 (Vercel).
- **Full-stack no/low-code, hosted iteration:** Bolt.new, Lovable, Replit Agent.
- **Deep, production codebase work:** Cursor, Windsurf, Claude Code (full architecture control).
- **3D scene generation:** Three.js / R3F via a coding agent; specialized tools (Omma, Emergent)
  for prompt-to-3D scaffolding.
