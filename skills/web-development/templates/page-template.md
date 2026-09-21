# Page Template (Next.js App Router)

Copy into `app/<route>/page.tsx`. Server Component by default; exports metadata for SEO.

```tsx
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "TITLE",
  description: "DESCRIPTION",
};

export default function Page() {
  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <h1 className="text-4xl font-bold tracking-tight text-zinc-50">TITLE</h1>
      <p className="mt-4 text-zinc-400">DESCRIPTION</p>
      {/* sections */}
    </main>
  );
}
```

Checklist:
- [ ] `metadata` filled in (title + description).
- [ ] One `<h1>` per page; logical heading order.
- [ ] No `"use client"` unless the page itself needs interactivity (push it into a child island).
- [ ] Data fetched on the server with caching (`fetch(..., { next: { revalidate } })`).
