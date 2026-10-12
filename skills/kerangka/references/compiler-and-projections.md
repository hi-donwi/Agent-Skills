# Kerangka Compiler, Projections, and Sidecar Runtime

## Overview

The Kerangka toolchain validates declarative application models, compiles them into a Canonical Intermediate Representation (KIR), and projects them into database schemas, API contracts, AI tool definitions, and frontend documents.

## 1. The Canonical Intermediate Representation (KIR)

When Kerangka compiles a `.kerangka.json` file, it normalizes shorthand types, validates expressions, resolves cross-entity references, and verifies decision tables into a canonical KIR document. All downstream code generators, DDL emitters, and API synthesizers consume KIR rather than parsing raw source JSON.

```
.kerangka.json  -->  [ Compiler (L0 Check & Validation) ]  -->  KIR Document (.kir.json)
                                                                     |
       +--------------------+---------------------+------------------+------------------+
       |                    |                     |                  |                  |
   SQL DDL             OpenAPI 3.1           GraphQL SDL          MCP Tools         UIDL Screens
 (PostgreSQL/SQLite)   (REST contracts)      (Query/Mutation)    (AI Tool APIs)   (uidl-runtime)
```

## 2. CLI Toolchain Commands

### Validation and Quality Gates

- `kerangka check <model.json>`: Verifies JSON structure, validates expression syntax, and checks that effective-date ranges do not overlap.
- `kerangka lint <model.json>`: Enforces architectural boundary rules, entity naming standards, and complexity budgets.

### Compilation and Schema Projections

- `kerangka build <model.json> -o build/app.kir.json`: Compiles the source model into canonical KIR.
- `kerangka ddl <model.json> --dialect postgres -o schema.sql`: Emits relational DDL with primary keys, foreign key constraints, indexes, and nullability checks.
- `kerangka openapi <model.json> -o openapi.json`: Generates an OpenAPI 3.1 contract complete with request/response schemas and RFC 9457 error formats.
- `kerangka graphql <model.json> -o schema.graphql`: Generates GraphQL query types, mutation inputs, and entity definitions.
- `kerangka mcp <model.json> -o mcp-tools.json`: Synthesizes Model Context Protocol tool declarations (`list_*`, `get_*`, `create_*`, `update_*`, `transition_*`) so AI coding agents can interact directly with model-backed actions.
- `kerangka uidl <model.json> -o uidl-screens/`: Generates valid UIDL documents for dashboards, data tables, and forms consumed by `uidl-runtime`.

### Polyglot Code Generation

- `kerangka codegen <model.json> --target ts -o models.ts`: TypeScript interfaces and Zod schemas.
- `kerangka codegen <model.json> --target java -o models/`: Java 21 records and Jakarta validation annotations.
- `kerangka codegen <model.json> --target python -o models.py`: Python dataclasses and Pydantic v2 schemas.
- `kerangka codegen <model.json> --target go -o models.go`: Go structs with JSON and validation tags.

## 3. Sidecar Host Runtime Architecture

For local execution, testing, and microservice deployment, Kerangka provides a zero-overhead runtime sidecar (`kerangka serve`).

### Architectural Invariants

1. **Durable SQLite Sessions**: Running with `--session <file>` persists session state in SQLite. If the process restarts, pending events and unperformed host effects remain intact.
2. **Pre-Dispatch Delivery Queue**: Events and host effects are queued in the durable store *before* network dispatch begins, preventing lost events if a crash occurs during third-party connector execution.
3. **Transactional Outbox**: Business events are formatted as CloudEvents and stored in an append-only outbox table. Subscribers acknowledge events via `/api/events/{id}/ack` or `/nack`.
4. **Separation of Logic and I/O**: The Kerangka evaluation kernel executes purely in memory with zero direct network I/O. Outbound operations (emails, webhooks, timers) are emitted as declarative host effect requests for the host runtime to execute.
