// GOOD: Server Component by default. Data fetched on the server, no client JS shipped
// for the static parts. Strict types, semantic HTML, accessible, Tailwind tokens.
//
// Follows ../docs/coding-standards.md:
//  - Server Component unless interactivity requires otherwise
//  - strict TypeScript (no `any`)
//  - interactivity isolated into a small client island
//  - respects prefers-reduced-motion

import { LikeButton } from "./like-button";

interface Article {
  id: string;
  title: string;
  excerpt: string;
  readingTimeMinutes: number;
}

async function getArticle(id: string): Promise<Article> {
  const res = await fetch(`https://api.example.com/articles/${id}`, {
    next: { revalidate: 3600 }, // cache + ISR, no client fetch
  });
  if (!res.ok) throw new Error(`Failed to load article ${id}`);
  return res.json();
}

export async function ArticleCard({ id }: { id: string }) {
  const article = await getArticle(id);

  return (
    <article className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
      <h2 className="text-xl font-bold tracking-tight text-zinc-50">
        {article.title}
      </h2>
      <p className="mt-2 text-zinc-400">{article.excerpt}</p>
      <footer className="mt-4 flex items-center justify-between text-sm text-zinc-500">
        <span>{article.readingTimeMinutes} min read</span>
        {/* Only the interactive bit is a client island */}
        <LikeButton articleId={article.id} />
      </footer>
    </article>
  );
}
