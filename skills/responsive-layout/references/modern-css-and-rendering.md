# Modern CSS Architecture and Rendering Performance

## Overview

Modern web browsers support native CSS nesting, cascade layers, container queries, and subgrid without requiring heavy preprocessors. Structuring stylesheets around these capabilities prevents specificity conflicts and guarantees high-performance rendering (eliminating layout shift and interaction latency).

## 1. Native CSS Nesting Architecture

Browser-native nesting allows co-locating element selectors, pseudo-classes, and state attributes cleanly:

```css
.profile-card {
  background-color: var(--color-surface-container);
  border-radius: var(--radius-md);
  padding: var(--space-4);

  /* Direct child nesting */
  & > .header {
    display: flex;
    align-items: center;
    gap: var(--space-3);
  }

  /* State attribute selectors */
  &[data-state="active"] {
    border-color: var(--color-interactive-primary);
  }

  /* Interaction states */
  &:hover {
    box-shadow: var(--shadow-sm);
  }
}
```

### Nesting Discipline

- **Maximum Nesting Depth**: Keep nesting to at most 3 levels. Deeper nesting bloats selector specificity and tightly couples styles to ephemeral DOM markup.
- **Avoid Tag-Level Selectors in Nesting**: Prefer class and data-attribute selectors (`& > .action-button`) over bare element selectors (`& > div > button`) to maintain refactoring resilience.

## 2. Cascade Layers (`@layer`)

Cascade layers eliminate CSS specificity wars by explicitly defining the precedence of style layers independent of individual selector weights.

### Standard Layer Order

Declare the layer hierarchy at the very top of the root stylesheet:

```css
@layer reset, base, tokens, components, utilities;

@layer reset {
  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
  }
}

@layer components {
  /* Complex component selector with high internal specificity */
  .button.btn-primary:not(:disabled) {
    background-color: var(--color-interactive-primary);
    color: var(--color-foreground-inverse);
  }
}

@layer utilities {
  /* Utility rule with single-class specificity wins over components layer */
  .u-hidden {
    display: none !important;
  }

  .u-text-danger {
    color: var(--color-feedback-danger);
  }
}
```

## 3. Subgrid for Multi-Card Alignment

Cards in a grid often have variable headline lengths, causing action buttons and footers to misalign vertically across rows. Use CSS Subgrid to participate directly in the parent grid's row tracks:

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  grid-auto-rows: auto auto 1fr auto; /* Title, metadata, body, actions */
  gap: var(--space-4);
}

.card-item {
  display: grid;
  grid-row: span 4;
  grid-template-rows: subgrid;
  background-color: var(--color-surface-container);
  padding: var(--space-4);
  border-radius: var(--radius-md);
}
```

## 4. Rendering Stability and Web Vitals

Ensure stylesheet architecture actively prevents layout instability and interaction delays:

### Cumulative Layout Shift (CLS) Prevention

1. **Aspect Ratio Reservation**: Always declare explicit dimensions or `aspect-ratio` on images, videos, and embed frames:
   ```css
   .hero-image {
     width: 100%;
     aspect-ratio: 16 / 9;
     object-fit: cover;
   }
   ```
2. **Min-Height on Async Containers**: Apply minimum height placeholders to containers that load async third-party widgets or dynamic feeds to prevent content jumping when data resolves.
3. **Font Metrics Matching**: When loading web fonts, declare fallback font metric overrides (`size-adjust`, `ascent-override`) to avoid reflow when the primary web font swaps in.

### Interaction to Next Paint (INP) Optimization

1. **Avoid Layout Thrashing**: Never alternate DOM geometry reads (such as `element.offsetWidth` or `getBoundingClientRect()`) with DOM style mutations inside interaction handlers. Batch reads first, then batch writes.
2. **Content Visibility for Long Lists**: For lengthy off-screen lists, apply `content-visibility: auto` to defer layout and rendering until items approach the viewport:
   ```css
   .feed-item {
     content-visibility: auto;
     contain-intrinsic-size: 0 120px; /* Estimated height placeholder */
   }
   ```
