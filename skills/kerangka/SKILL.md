---
name: kerangka
description: >-
  Author, validate, compile, and project Kerangka models — declarative JSON app logic, workflows, DDL, OpenAPI, MCP tools, and UIDL frontends.
metadata:
  pack: core
  keywords: kerangka, json skeleton, kir, compiler, projection, ddl, openapi, graphql, mcp, sidecar, durable session, workflow, business rules, uidl projection, declarative ui
---

# Kerangka

## Overview

Kerangka turns a declarative JSON model (`.kerangka.json`) into production application logic (validation, computed fields, business rules, state workflows, actions, permissions) and multi-target projections (SQL DDL, OpenAPI 3.1, GraphQL SDL, MCP tools, and UIDL frontend screens) with identical semantics across platforms.

## When to use
- Authoring, editing, or validating `.kerangka.json` application models.
- Compiling models to Canonical Intermediate Representation (KIR).
- Generating database DDL (PostgreSQL, SQLite), OpenAPI contracts, or MCP tool declarations.
- Projecting declarative dashboard, list, and form screens into UIDL for `uidl-runtime`.
- Operating the deterministic sidecar engine with durable SQLite sessions and transactional outboxes.

## Hand off when
| Need | Skill |
|---|---|
| Hand-coding freeform UI outside a schema | `frontend-ui-engineering` |
| Rendering or styling raw UIDL documents in React/Flutter | `uidl-runtime` |
| Custom token palettes, contrast, and themes | `design-tokens` |
| Designing non-modelled public REST APIs | `rest-api-contract` |

## Process

1. **Declare the JSON skeleton first.** Define entities, primitive types, defaults, and invariant rules in `.kerangka.json`. Keep data semantics pure without coupling to databases or UI frameworks.
2. **Model business rules and workflows declaratively.** Define computed fields, DMN-style decision tables (`decisions`), and state transitions with role guards (`workflow.transitions`).
3. **Validate syntax and types.** Run `kerangka check <model.json>`. Ensure all types resolve, expressions parse, and effective-date ranges do not overlap.
4. **Lint boundary invariants.** Run `kerangka lint <model.json>`. Verify entity naming rules, relation depths, and modular boundaries before compilation.
5. **Compile to Canonical Intermediate Representation.** Run `kerangka build <model.json> -o build/app.kir.json`. KIR is the verified input for all downstream projections.
6. **Project backend contracts.** Generate SQL DDL (`kerangka ddl`), OpenAPI 3.1 (`kerangka openapi`), and Model Context Protocol tools (`kerangka mcp`) directly from the model.
7. **Project declarative UI screens.** Run `kerangka uidl <model.json> -o uidl-screens/`. This generates production-ready UIDL documents (dashboards, data tables, forms, navbars) rendered by `uidl-runtime`.
8. **Execute sidecar runtime.** Use `kerangka serve --stdio --session app.db` for transactional execution. State changes, CloudEvents, and host effects commit atomically.

## Red flags
- Writing business rules or workflow logic inside page components instead of the model.
- Hand-crafting REST APIs or CRUD endpoints that can be projected deterministically.
- Inventing unmapped widget types in views that the UIDL reference registry cannot render.
- Modifying emitted KIR or projection files by hand instead of updating the source model.
- Performing side effects during pure evaluation runs instead of queueing host effects.

## Verification
- [ ] `kerangka check` exits 0 with no syntax or expression errors.
- [ ] `kerangka lint` reports zero boundary or complexity violations.
- [ ] Generated SQL DDL applies cleanly against target database (PostgreSQL/SQLite).
- [ ] Generated UIDL documents validate successfully against `uidl-validate`.
- [ ] Generated MCP tools expose correct parameter schemas and action permissions.

## References
- `references/model-specification.md` — entity fields, expressions, rules, workflows, and decisions
- `references/compiler-and-projections.md` — CLI commands, KIR compilation, OpenAPI, DDL, MCP, and sidecar runtime
- `references/declarative-ui-design.md` — designing dashboards, lists, and forms via Kerangka UIDL projections
