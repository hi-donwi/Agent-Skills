# Adaptive Layout Archetypes and Window Classes

## Overview

Responsive layout reflows content fluidly within an established arrangement. Adaptive layout fundamentally restructures the interface—transforming navigation, multi-pane relationships, and information density—based on discrete window size classes.

## 1. Window Size Classes

Categorize viewport width into three standardized window classes to govern macro layout architecture:

| Window Class | Width Range | Form Factor Context | Navigation & Shell Strategy |
|---|---|---|---|
| **Compact** | `< 600px` | Phones, narrow portrait panes | Bottom navigation bar, modal slide-over drawers, single-column stacks |
| **Medium** | `600px - 840px` | Small tablets, split-screen desktop windows | Compact navigation rail, collapsible side drawers, two-pane layouts |
| **Expanded** | `> 840px` | Large tablets, laptops, widescreen monitors | Permanent navigation sidebar, persistent multi-pane workspaces |

## 2. Canonical Multi-Pane Archetypes

Most enterprise and productivity applications map to three canonical structural archetypes:

### A. List-Detail Archetype

Presents an indexed collection alongside the active record's full contents.

- **Compact Viewport**: Display list and detail as sequential screens. Selecting an item navigates forward to the detail screen; a prominent back button returns to the list.
- **Medium / Expanded Viewport**: Display list and detail simultaneously side-by-side. The list occupies a fixed width (e.g., 320px–360px) while the detail pane fills remaining space.

```css
/* Responsive List-Detail Layout */
.list-detail-container {
  display: flex;
  height: 100%;
}

.list-pane {
  width: 100%;
}

.detail-pane {
  display: none;
}

@media (min-width: 840px) {
  .list-pane {
    width: 360px;
    border-inline-end: 1px solid var(--color-border-subtle);
    flex-shrink: 0;
  }

  .detail-pane {
    display: block;
    flex: 1;
    overflow-y: auto;
  }
}
```

### B. Supporting Pane Archetype

Focuses attention on a primary canvas while providing a contextual inspector or secondary tool pane (e.g., document editors, code inspection, issue trackers).

- **Compact Viewport**: Supporting pane opens as an overlay bottom sheet or full-width modal.
- **Medium Viewport**: Supporting pane docks as a slide-over drawer that overlays secondary content.
- **Expanded Viewport**: Supporting pane embeds persistently on the trailing edge (e.g., 300px width), reflowing canvas content without occlusion.

### C. Bento Grid and Dashboard Cards

Arranges modular content cards across an adaptable grid. Rather than forcing uniform squares, cards span variable rows and columns based on information priority.

```css
.bento-grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

@media (min-width: 840px) {
  .bento-grid {
    grid-template-columns: repeat(12, 1fr);
  }

  .card-featured {
    grid-column: span 8;
    grid-row: span 2;
  }

  .card-metric {
    grid-column: span 4;
  }
}
```

## 3. Shell vs. Component Responsibility Boundary

Maintain a strict boundary between viewport queries and container queries:

1. **Page Shell (Viewport-aware)**: The root layout shell handles top-level navigation, sidebar collapse state, and window margins using viewport media queries (`@media (min-width: ...)`).
2. **Inner Components (Container-aware)**: Reusable components (feed cards, user summaries, comment lists) must never inspect viewport width. They must declare `@container` contexts and adapt strictly to the width of their assigned layout column.

```css
/* Shell provides container context */
.main-content-column {
  container-type: inline-size;
  container-name: content-area;
}

/* Reusable card adapts to available column space */
@container content-area (min-width: 480px) {
  .article-card {
    display: flex;
    flex-direction: row;
    gap: var(--space-4);
  }

  .article-card-thumb {
    width: 160px;
    height: 100%;
  }
}
```
