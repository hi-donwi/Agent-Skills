# Kerangka Model Specification

## Overview

A Kerangka application model (`.kerangka.json`) is a declarative specification defining entities, types, invariants, computed values, decision tables, state machines, and view projections. The model is completely decoupled from database engines, transport protocols, and UI frameworks.

## 1. Document Root Structure

```json
{
  "kerangka": "0.1",
  "app": "order-management",
  "meta": {
    "title": "Order Management System",
    "description": "B2B order lifecycle, approval rules, and fulfillment",
    "timezone": "UTC"
  },
  "roles": ["customer", "sales-rep", "manager", "admin"],
  "decisions": { /* DMN-style decision tables */ },
  "entities": { /* Data models, rules, workflows */ },
  "views": { /* Declarative dashboard, list, and form projections */ },
  "examples": [ /* Executable scenario tests */ ]
}
```

## 2. Type System and Field Definitions

Fields use concise shorthand notation or expanded definition objects:

| Shorthand Syntax | Type | Constraints / Meaning |
|---|---|---|
| `string!` | String | Required (non-null) string |
| `string(max=120)` | String | Maximum length 120 characters |
| `int! >= 0` | Integer | Required non-negative integer |
| `decimal(10,2)` | Decimal | Fixed-point financial currency amount |
| `bool = false` | Boolean | Defaults to `false` if omitted |
| `date!` | Date | ISO-8601 date (`YYYY-MM-DD`) |
| `datetime` | DateTime | ISO-8601 timestamp with timezone |
| `uuid` | UUID | Universally unique identifier |
| `enum(draft, open, closed)! = draft` | Enum | Enumerated string set with default |

### Expanded Field Object

```json
"totalAmount": {
  "type": "decimal(12,2)",
  "required": true,
  "compute": "subtotal + taxAmount - discountAmount",
  "readOnly": true
}
```

## 3. Invariant Rules and Validation

Rules define business assertions that must hold true before a record can be persisted or transitioned.

```json
"rules": [
  {
    "id": "valid-quantity",
    "check": "quantity > 0",
    "field": "quantity",
    "message": "Order quantity must be at least 1 unit"
  },
  {
    "id": "end-after-start",
    "check": "deliveryDate >= orderDate",
    "field": "deliveryDate",
    "message": "Delivery date cannot precede the order creation date"
  }
]
```

## 4. Decision Tables

Decisions encapsulate complex branching logic as tabular rules, avoiding convoluted nested conditionals:

```json
"decisions": {
  "discountTier": {
    "hitPolicy": "first",
    "inputs": [{ "name": "orderTotal", "type": "decimal" }],
    "outputs": [{ "name": "discountPercent", "type": "decimal" }],
    "rows": [
      { "orderTotal": ">= 50000", "discountPercent": 15.0 },
      { "orderTotal": ">= 10000", "discountPercent": 10.0 },
      { "orderTotal": ">= 2000",  "discountPercent": 5.0 },
      { "orderTotal": "< 2000",   "discountPercent": 0.0 }
    ]
  }
}
```

## 5. Workflows and State Machines

Workflows govern state transitions, permitted roles, and automated escalation:

```json
"workflow": {
  "field": "status",
  "tasks": {
    "managerApproval": {
      "state": "pending_approval",
      "assign": { "role": "manager" },
      "actions": ["approve", "reject"],
      "due": "P2D",
      "onOverdue": "escalate"
    }
  },
  "transitions": {
    "submit": {
      "from": "draft",
      "to": "pending_approval",
      "roles": ["sales-rep"]
    },
    "approve": {
      "from": ["pending_approval", "escalated"],
      "to": "approved",
      "roles": ["manager", "admin"],
      "when": "totalAmount <= 100000 || actor.role == 'admin'"
    },
    "reject": {
      "from": "pending_approval",
      "to": "rejected",
      "roles": ["manager"]
    }
  }
}
```

## 6. Executable Scenario Examples

Models embed executable tests to verify business logic during compilation:

```json
"examples": [
  {
    "name": "approval within manager threshold",
    "run": "Order.approve",
    "actor": { "role": "manager" },
    "record": { "status": "pending_approval", "totalAmount": 45000 },
    "expect": {
      "ok": true,
      "record": { "status": "approved" }
    }
  }
]
```
