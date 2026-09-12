# Prompt Examples

Modular prompting beats one giant prompt. Scaffold → iterate → integrate, one concern at a time.

For the full template library (all phases, tools, checklists), see
[`prompts.md`](./prompts.md).

## Structured format (default for agent mode)

```
Goal: Add pricing section with 3 tiers and Stripe checkout CTA.
Constraints: Use existing design tokens in tailwind.config.ts. No new dependencies.
Scope: @components/landing/* only. Do not touch API routes.
Verification: pnpm lint && pnpm test && screenshot hero-to-pricing scroll.
```

## Scaffolding
> Initialize a Next.js App Router project (TypeScript, strict) with Tailwind and shadcn/ui.
> Add a top navigation bar and a hero section. Server Components by default.

## Iterating on UI
> Update the hero to include a staggered fade-in using Framer Motion. Respect
> `prefers-reduced-motion`: disable the animation when the user prefers reduced motion.

## Integrating backend
> Create a Supabase schema for user profiles (id, handle, avatar_url, bio). Generate the
> API route handlers and a typed client. Keep secrets server-side only.

## Few-shot for a specific look
> Match this layout (link/screenshot). Use our tokens: dark surfaces, neon-green accent,
> bold display type with a monospace label above each section.

## Debugging
> I got this error running the build (full stack trace below). Analyze the trace and fix the
> underlying issue — don't just silence the symptom.

## Enforcing quality
> Write clean, modular code. Strict TypeScript, no `any`. Add JSDoc to non-obvious functions.
> Include a Playwright test for the new interaction. Don't add new dependencies without
> justification.

## Immersive 3D
> In `components/scene/`, build a React Three Fiber canvas with a product model that rotates
> on scroll (GSAP ScrollTrigger). Provide a static fallback image and a text description, and
> disable the scene under reduced motion.

## Production (spec-driven)
> Write a Gherkin BDD spec for the pricing checkout flow (successful payment, declined card,
> cancel mid-flow). Save to specs/pricing.feature. Do not generate implementation yet.
