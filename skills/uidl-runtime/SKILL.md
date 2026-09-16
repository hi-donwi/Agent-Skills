---
name: uidl-runtime
description: >-
  Author, validate, and render UIDL documents — schema-driven JSON UI for lists,
  forms, reports, dashboards, and settings — with the uidl-runtime package
  (React reference, Flutter and Android semantic cores, Java document builder).
  Use when creating or changing a UIDL document, the document schema, DataAdapter
  seam, $bind/$query/$expr/mutate behaviour, uidl-validate, or uidl-compile.
  Do not use for hand-built React/Flutter/Compose screens that are not UIDL
  documents (frontend-ui-engineering) or for ordinary REST work that does not
  produce UIDL (quarkus-service, rest-api-contract).
metadata:
  pack: web
---

# UIDL Runtime

## Overview

A UIDL document is JSON that describes layout, state, queries, bindings, events,
and actions. The runtime validates it and renders it through a component registry.
Documents must not name a data source, HTTP client, or database: reads go through
one `DataAdapter`; writes go through a host `mutationHandler` and fail closed
when none is permitted.

## When to use
- Authoring or editing a UIDL JSON document or page generator.
- Changing schema, bindings, expressions, queries, or actions.
- Wiring `UIDocumentRenderer` / `DocumentSchema` in a React host.
- Validating documents with `uidl-validate` or compiling with `uidl-compile`.
- Extending Flutter, Android, or the Java document builder against the same spec.

## Process
1. **Confirm it is UIDL.** If the screen is hand-built JSX/Compose/Widgets with
   no document, stop and use `frontend-ui-engineering`.
2. **Read the spec first.** `spec/README.md`, then the relevant file under
   `spec/semantics/` (`state`, `bindings`, `expressions`, `queries`, `mutations`,
   `actions`). Do not invent node types or action kinds.
3. **Keep the seams.** Documents and generators import no concrete adapter.
   Reads: `$query` → `DataAdapter`. Writes: `mutate` / `command` → host handler.
   Schema `$id` values are names, never fetch targets.
4. **Validate before render.** `DocumentSchema.parse` / `safeParse` in code, or
   `uidl-validate <file.json>`. Reject unknown document majors
   (`UNSUPPORTED_VERSION`); accept additive minors.
5. **Fail closed.** A `mutate` without a permitted host handler must fail, not
   invent a backend. API-backed actions are allowlisted.
6. **Pick the runtime honestly.** React (`packages/core`, npm `uidl-runtime`) is
   the full widget suite. Flutter and Android are semantic cores with smaller
   default catalogs — do not assume pixel parity with the React reference.
7. **Verify.** Unit/conformance tests for schema and actions; Playwright only for
   React surfaces. Load `webapp-testing` for browser journeys.

See `references/document-model.md` for the document shape and
`references/commands.md` for repo commands.

## Red flags
- HTTP, SQL, or a concrete adapter imported from a document or generator.
- `mutate` succeeding with no host handler.
- Hand-building a React page that should be a UIDL document.
- Assuming Flutter or Compose render the full React catalog.
- Fetching `https://uidl.dev/schema/...` — those `$id`s are not URLs to retrieve.
- Treating reference consoles as production-ready products.

## Verification
- `uidl-validate` (or `DocumentSchema.safeParse`) succeeds on the document.
- Nearby non-match: "add a settings button in JSX" does not use this skill.
- Failure case: missing mutation handler → closed failure, no invented API.
- Reads go through `DataAdapter`; writes through the host handler.
- Conformance fixtures under `conformance/cases/` still pass for the changed area.
