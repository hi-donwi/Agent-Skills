// BAD: the same card done wrong. Each numbered comment marks a violation of
// ../docs/coding-standards.md. Use this as a "what not to do" reference.

"use client"; // (1) Needless client component — this content is static.

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

export function ArticleCard({ id }: { id: any }) {
  // (2) `any` prop type — strict TypeScript forbids this.
  const [article, setArticle] = useState<any>(null); // (3) `any` again.

  useEffect(() => {
    // (4) Client-side fetch with no caching, no error handling — waterfalls and
    //     ships secrets/keys to the browser if you're not careful. Fetch on the server.
    fetch("https://api.example.com/articles/" + id)
      .then((r) => r.json())
      .then(setArticle);
  }, [id]);

  if (!article) return <div>Loading...</div>; // (5) Layout shift (CLS) on every load.

  return (
    // (6) Non-semantic <div> instead of <article>; no heading hierarchy.
    <motion.div
      // (7) Animation ignores prefers-reduced-motion — accessibility failure.
      animate={{ opacity: [0, 1], y: [20, 0] }}
      className="card" // (8) Bespoke CSS class instead of Tailwind tokens.
    >
      <div className="title">{article.title}</div>
      <div>{article.excerpt}</div>
      <button onClick={() => alert("liked")}>♥</button>
      {/* (9) Icon-only button with no accessible label. */}
    </motion.div>
  );
}
