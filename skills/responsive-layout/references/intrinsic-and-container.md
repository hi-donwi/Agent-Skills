# Intrinsic sizing and container queries

Load when building the layout itself. The ordering here is the point: each section is only
reached when the one before it cannot do the job.

## 1. Intrinsic — no query at all

Most "responsive" layouts are a grid that wraps. This needs no breakpoint, works at every
width including ones nobody tested, and has nothing to maintain:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
  gap: var(--space-gutter);
}
```

`auto-fit` collapses empty tracks so the last row stretches; `auto-fill` keeps them, leaving
gaps. Prefer `auto-fit` unless you deliberately want a fixed column rhythm.

The `min(18rem, 100%)` matters: a bare `minmax(18rem, 1fr)` overflows below 18rem, which is
the most common cause of horizontal scroll at 320px.

Two more that remove queries:

```css
.sidebar-layout {            /* sidebar beside content, stacking when there is no room */
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-gutter);
}
.sidebar-layout > .sidebar { flex: 1 1 16rem; }
.sidebar-layout > .main    { flex: 999 1 30rem; }   /* wins the space until both cannot fit */

.prose { inline-size: min(65ch, 100%); }            /* readable measure, never overflowing */
```

## 2. Container queries — a component reading its own space

When the component genuinely must change shape, it should ask about the space it was given,
not about the window. This is what removes the `variant` prop:

```css
.card-host { container-type: inline-size; container-name: card; }

.card { display: grid; gap: var(--space-inline); }

@container card (inline-size > 30rem) {
  .card { grid-template-columns: 12rem 1fr; }
}
```

The same card is now correct in a sidebar, a three-column grid and a full-width modal, with
no prop and no knowledge of the page.

Two constraints worth knowing before you reach for it:

- A container cannot query itself. `container-type` goes on the parent; the query styles the
  child. This is why the example has a `.card-host`.
- `container-type: inline-size` makes the element a containment context, which removes its
  dependence on child inline size. On a block-level element that is usually what you want;
  on a grid or flex item it can change sizing, so check the result.

Container units (`cqi`, `cqb`) size against the container rather than the viewport, which is
the right unit inside a component:

```css
.card__title { font-size: clamp(1rem, 4cqi, 1.5rem); }
```

## 3. Media queries — the page shell only

The shell knows about the window; components do not. Keep viewport queries at that level:
the overall page frame, print styles, `prefers-reduced-motion`, `prefers-color-scheme`,
coarse-vs-fine pointer.

A media query inside a reusable component is the bug this whole ordering exists to prevent.

## Subgrid and `:has()`

`subgrid` lets a child align to its ancestor's tracks — the fix for cards in a row whose
titles and footers should line up despite different content lengths:

```css
.card-grid { display: grid; grid-template-rows: masonry; }  /* where supported */
.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;   /* title / body / footer align across all cards */
}
```

`:has()` lets a container react to its content, removing a class of wrapper components:

```css
.field:has(input:invalid)     { --field-border: var(--color-danger); }
.layout:has(> .sidebar)       { grid-template-columns: 16rem 1fr; }
.card:has(img)                { grid-template-rows: auto 1fr; }
```

Both are widely supported in current browsers. Check the project's stated support target
before relying on either as the only path, and make the fallback the simpler layout rather
than a broken one.
