# Declarative Design Systems and Theming in UIDL-Runtime

## Overview

In the UIDL ecosystem, UI/UX design rules are not hand-coded with ad-hoc CSS classes or inline style strings. Design systems are declared as structured token themes and applied to UIDL document nodes via semantic tokens, `StyleIntent` objects, and responsive value maps.

## 1. Token Architecture and Themes

UIDL-Runtime separates token values across primitive and semantic layers:

```tsx
import type { Theme, PrimitiveTokens, SemanticTokens } from "uidl-runtime";

export const customBrandTheme: Theme = {
  id: "brand-dark",
  name: "Brand Dark Theme",
  colorScheme: "dark",
  primitives: {
    color: {
      canvas: "#09090b",
      surface: "#18181b",
      "surface-elevated": "#27272a",
      border: "#3f3f46",
      primary: "#3b82f6",
      "text-primary": "#f4f4f5",
      "text-muted": "#a1a1aa",
      danger: "#ef4444",
      success: "#22c55e",
      warning: "#f59e0b"
    },
    radius: {
      none: "0px",
      sm: "4px",
      md: "8px",
      lg: "12px",
      full: "9999px"
    },
    spacing: {
      1: "4px",
      2: "8px",
      3: "12px",
      4: "16px",
      6: "24px",
      8: "32px"
    }
  },
  semantics: {
    color: {
      "surface.canvas": "{primitives.color.canvas}",
      "surface.card": "{primitives.color.surface}",
      "border.subtle": "{primitives.color.border}",
      "interactive.primary": "{primitives.color.primary}"
    }
  }
};
```

Documents reference tokens symbolically using bracketed paths (`{primitives.color.surface}`), allowing the runtime to switch from light to dark or branded themes with zero node modifications.

## 2. StyleIntent and Responsive Layouts

Nodes control layout and spatial geometry using structured `StyleIntent` objects instead of string concatenation.

### Multi-Breakpoint Values

Every dimension in `StyleIntent` supports responsive breakpoint maps (`base`, `sm`, `md`, `lg`, `xl`):

```json
{
  "id": "content-container",
  "type": "Container",
  "style": {
    "display": "flex",
    "flexDirection": {
      "base": "column",
      "md": "row"
    },
    "gap": {
      "base": "16px",
      "md": "24px"
    },
    "padding": {
      "base": "16px",
      "md": "24px",
      "lg": "32px"
    },
    "maxWidth": "1280px",
    "margin": "0 auto"
  }
}
```

## 3. Implementing Layout Constraints in UIDL

When authoring UIDL documents, enforce the design system's spatial bounds:

1. **Form Max-Width**: Never allow single-column form containers to expand across wide screens. Set `style: { maxWidth: "36rem", width: "100%" }` (576px limit).
2. **Reading Line Length**: Constrain text or article blocks to `style: { maxWidth: "68ch" }` to guarantee 60–75 characters per line.
3. **Screen Edge Margins**: Shell containers use responsive padding (`base: "16px"`, `md: "24px"`).
4. **Touch Target Sizing**: Primary interactive buttons and inputs default to minimum 44px hit heights via standard component registry styling.
5. **Card Insets**: Apply 16px padding on mobile (`base`) and 20px–24px on desktop (`md`).

## 4. Density Modes in UIDL Components

Data-dense widgets (like `DataTable` and grid cards) support explicit density configurations matching the design system tiers:

```json
{
  "id": "orders-table",
  "type": "DataTable",
  "props": {
    "density": "compact",
    "columns": [
      { "field": "id", "header": "Order ID", "width": "120px" },
      { "field": "customer", "header": "Customer Name" },
      { "field": "amount", "header": "Total Amount", "align": "right" },
      { "field": "status", "header": "Status", "widget": "Badge" }
    ]
  }
}
```

- `compact`: 32px row heights, 6px vertical cell padding (enterprise financial and logistics surfaces).
- `comfortable`: 48px row heights, 12px vertical padding (default administration).
- `relaxed`: 60px row heights, 18px vertical padding (touch tablets and consumer dashboards).
