# Declarative UI Design via Kerangka Projections

## Overview

Rather than hand-crafting repetitive React, Vue, or Flutter page templates for enterprise applications, developers declare UI views directly inside the Kerangka model. The compiler projects these declarations into production-grade UIDL documents that adhere to the 8pt spatial grid, ergonomic hit targets, and accessible contrast standards when rendered by `uidl-runtime`.

## 1. Declaring Views in the Model

Views are declared under the `views` key of `.kerangka.json`:

```json
{
  "views": {
    "executive-dashboard": {
      "type": "dashboard",
      "title": "Operations Dashboard",
      "dashboard": [
        { "kpi": "Active Orders", "query": "count(Order.status == 'open')", "trend": "+12%" },
        { "kpi": "Pending Approvals", "query": "count(Order.status == 'pending_approval')" },
        { "kpi": "Gross Revenue", "query": "sum(Order.totalAmount)", "format": "currency" }
      ]
    },
    "orders-list": {
      "type": "list",
      "entity": "Order",
      "title": "Order Management",
      "columns": ["orderNumber", "customerName", "totalAmount", "status", "orderDate"],
      "filters": ["status", "orderDate"],
      "sort": { "field": "orderDate", "direction": "desc" }
    },
    "order-form": {
      "type": "form",
      "entity": "Order",
      "title": "New Sales Order",
      "layout": "two-column",
      "fields": ["customerName", "orderDate", "deliveryDate", "totalAmount", "notes"]
    }
  }
}
```

## 2. Projection to UIDL Surfaces

Running `kerangka uidl <model.json> -o uidl-screens/` projects these view declarations into canonical UIDL 1.x documents:

### A. Dashboard Projections
- Generates responsive metric cards using `Column` and `Card` nodes.
- Attaches declarative `$query` data sources to aggregate metrics.
- Formats currency, percentages, and numeric counts with proper typography hierarchy (Display/Title tokens).

### B. List View Projections
- Generates a `DataTable` widget with built-in server pagination (`page: { number, size }`), multi-column sorting, and full-text search.
- Maps enum fields (such as `status`) to visual status pills/badges.
- Injects row actions matching the entity's declared workflow transitions (e.g., `Approve`, `Reject`, `Cancel`).

### C. Form View Projections
- Inspects entity field types and constraints to select the appropriate input widget:
  - `string` -> `TextField`
  - `enum` -> `Select`
  - `bool` -> `Checkbox`
  - `date` -> `DatePicker`
- Wraps controls in a container capped at `max-inline-size: 36rem` (following the 480px–600px form max-width rule).
- Generates reactive bindings (`props: { value: { "$bind": "state.form.customerName" } }`).
- Generates submit actions executing the model's create or transition mutation.

### D. Application Navigation (Navbar)
- When multiple views exist, the compiler synthesizes a `Navbar` node linking each view route.
- The navbar renders at the top of the root container and highlights the currently active route based on the `$bind: "route.path"` state.

## 3. Design System Alignment

Because the generated UIDL documents consume the semantic token registry of `uidl-runtime`:
1. **Spatial Grid**: All generated containers, forms, and cards use the 8pt/4pt spatial scale tokens (`p-4` = 16px, `gap-4` = 16px, `gap-2` = 8px).
2. **Accessible Form Controls**: Input fields receive full hit targets (minimum 44px height on touch devices) and clear focus rings.
3. **Contrast and Themes**: Switching the host theme (e.g. to a dark or high-contrast preset) recolors all projected dashboards and data tables automatically without regenerating the UIDL files.
