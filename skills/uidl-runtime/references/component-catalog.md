# UIDL Component Catalog and Layout Registry

## Overview

UIDL documents reference component widgets through standard registry strings. Components map directly to the `uidl-runtime` component registry, which provides accessibility attributes, keyboard navigation, and theme bindings out of the box.

## 1. Structural and Layout Nodes

| Component Type | Role and Purpose | Common Props and Style Keys |
|---|---|---|
| `Container` | Main page shell or layout wrapper | `maxWidth`, `padding`, `margin: "0 auto"` |
| `Card` | Tonal elevated surface container | `padding`, `borderRadius`, `background`, `shadow` |
| `Column` | Vertical flexbox stack | `gap`, `alignItems`, `justifyContent` |
| `Row` | Horizontal flexbox arrangement | `gap`, `alignItems`, `justifyContent`, `flexWrap` |
| `Grid` | CSS Grid multi-column layout | `gridTemplateColumns`, `gap` |
| `Divider` | Structural separating line | `orientation: "horizontal" \| "vertical"` |

## 2. Data Display and Typography Nodes

| Component Type | Role and Purpose | Common Props and Bindings |
|---|---|---|
| `Text` | Standard body or label copy | `value: string`, `style: { fontSize, fontWeight, color }` |
| `Heading` | Section or page title | `level: 1..6`, `value: string` |
| `Badge` | Status indicator pill | `value`, `variant: "neutral" \| "success" \| "warning" \| "danger"` |
| `Metric` | Key Performance Indicator card | `label`, `value`, `change`, `trend: "up" \| "down"` |
| `Icon` | Vector symbol | `name`, `size: 16 \| 20 \| 24`, `color` |

## 3. Form and Interactive Widgets

| Component Type | Role and Purpose | State Binding Pattern |
|---|---|---|
| `TextField` | Text and email input | `props: { value: { "$bind": "state.form.field" } }` |
| `NumberField` | Numeric and currency input | `props: { min, max, step, value: { "$bind": "..." } }` |
| `Select` | Dropdown picker | `props: { options: [{ label, value }], value: { "$bind": "..." } }` |
| `Checkbox` | Boolean toggle | `props: { checked: { "$bind": "state.form.agree" } }` |
| `Switch` | Instantaneous toggle | `props: { checked: { "$bind": "state.settings.active" } }` |
| `DatePicker` | Calendar date picker | `props: { format: "YYYY-MM-DD", value: { "$bind": "..." } }` |
| `Button` | Interactive trigger | `props: { label, variant: "primary" \| "secondary" \| "danger" }` |

## 4. Collections and Data Grids

### `DataTable` Node Specification

```json
{
  "id": "invoices-grid",
  "type": "DataTable",
  "props": {
    "data": { "$query": { "from": "Invoice", "sort": [{ "field": "date", "dir": "desc" }] } },
    "columns": [
      { "field": "invoiceNumber", "header": "Invoice #" },
      { "field": "clientName", "header": "Client" },
      { "field": "amount", "header": "Amount", "format": "currency", "align": "right" },
      { "field": "status", "header": "Status", "widget": "Badge" }
    ],
    "pagination": { "pageSize": 15 },
    "density": "comfortable"
  }
}
```

## 5. Event and Action Arrays Invariant

In UIDL 1.x, event handlers must always provide an **array** of action descriptors. Single action objects are skipped by the interpreter:

```json
{
  "id": "submit-button",
  "type": "Button",
  "props": { "label": "Save Changes" },
  "events": {
    "press": [
      {
        "action": "mutate",
        "operation": "updateInvoice",
        "payload": { "$bind": "state.form" }
      },
      {
        "action": "toast",
        "message": "Invoice updated successfully",
        "type": "success"
      },
      {
        "action": "navigate",
        "path": "/invoices"
      }
    ]
  }
}
```
