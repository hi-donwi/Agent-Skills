# Component Template

Two shapes. Default to the Server Component. Reach for the client island only when you need
state, effects, or event handlers. `scripts/generate-component.js` scaffolds the first shape.

## Server Component (default)
```tsx
interface NameProps {
  className?: string;
}

export function Name({ className }: NameProps) {
  return (
    <section className={`text-zinc-50 ${className ?? ""}`}>
      <h2 className="text-2xl font-bold tracking-tight">Name</h2>
      {/* content */}
    </section>
  );
}
```

## Client island (only when interactive)
```tsx
"use client";

import { useState } from "react";

interface CounterProps {
  initial?: number;
}

export function Counter({ initial = 0 }: CounterProps) {
  const [count, setCount] = useState(initial);
  return (
    <button
      type="button"
      aria-label="Increment counter"
      onClick={() => setCount((c) => c + 1)}
      className="rounded-md bg-zinc-800 px-3 py-1 text-zinc-50"
    >
      {count}
    </button>
  );
}
```

Rules: strict types (no `any`), accessible labels on interactive elements, Tailwind tokens,
and respect `prefers-reduced-motion` for any animation.
