# Design Principles

Because anyone can generate a functional site in minutes, the differentiator is **how it
feels**. Taste, typography, whitespace, and interaction design are the real value.

## The "coding vibe" look
Not just "dark mode." The convincing pattern combines:
- Dark or high-contrast surfaces.
- Bold typography with monospace accents.
- Visible grids and terminal-like microcopy.
- Controlled glow / glass effects (used sparingly).
- Experimental but legible navigation.
- Functional motion — motion that communicates, never decoration for its own sake.

## Set the tone explicitly
Tell the agent the aesthetic in concrete terms, e.g.:
> "Minimalist, brutalist, dark mode by default, neon-green accents, bold type, smooth
> micro-interactions, generous whitespace."

## Immersive 3D
- Describe spatial intent: camera sweep, lighting ("clustered lighting as studio softboxes").
- Tie 3D rotation / camera movement to scroll using GSAP ScrollTrigger or Framer Motion 3D.
- Generate `.glb`/`.gltf` assets, then have the agent import and render them.
- Keep it accessible: text equivalent + static fallback image, and respect reduced motion.

## When to use 3D / motion
Add it only where it materially improves the experience. Avoid putting motion and 3D
everywhere — it dilutes impact and wrecks performance budgets.

## Anti-patterns
- Prompting without a PRD / rules file → hallucinated structure, inconsistent output.
- "Impressive-looking" UI with no performance discipline or tests.
- Sparse-vs-busy mismatch: motion that fights the content rather than guiding the eye.
