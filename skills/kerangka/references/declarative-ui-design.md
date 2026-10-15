# Kerangka views and presentation ownership

## Read the projection path first

Identify whether the host consumes static `kerangka uidl` documents or per-request
screens from `RecipeProjector` / `GET /screens/{viewId}`. They have different record,
version, query, and action contracts. Follow ADR-0043 and ADR-0045 in the Kerangka
repository: business presets belong to Kerangka; presentation recipes and CSS
belong to UIDL Runtime. Do not create another copy of a layout library.

## Declare views using the compiler's vocabulary

Views name their kind as a key, not `type: "list"` plus `entity`:

```json
{
  "kerangka": "0.1",
  "app": "record-management",
  "entities": {
    "Record": { "fields": { "name": "string!", "email": "email", "status": "enum(active, suspended) = active" } }
  },
  "views": {
    "records": { "list": "Record", "columns": ["name", "email", "status"], "open": "record" },
    "record": { "form": "Record", "sections": [["name", "email"], ["status"]] }
  }
}
```

Check and compile the exact example against the pinned compiler. Where the upgraded
compiler supports `sectionTitles`, add an array parallel to `sections`, for example
`["Identity", "Lifecycle"]`. Titles must be nonempty and unique. An older compiler
rejects this new key; upgrade it before adding the metadata.

## Static documents

`kerangka uidl <model.json> -o uidl-screens/` generates lists and forms. Static
form sections use registered Column/Text/Form widgets and supported spacing
utilities. The upgraded projector emits shared `uidl-admin-*` presentation hooks,
bounded width, and field groups. Older runtimes still need explicit layout and
cannot be assumed to implement the new hooks.

A static dashboard is refused with `DASHBOARD_NOT_STATIC`; aggregate values must be
computed for the actual actor by the dynamic screen path. Do not document static
dashboards as production-ready or bind the first record as an aggregate.

## Per-request screens

The recipe projector uses `uidl-runtime/recipes`, which must remain React-free.
Forms take record data and version; lists carry paging/query state; dashboards
compute authorized aggregates. Preserve those host seams when changing presentation.
Do not switch static documents to dynamic recipes just to fix a margin.

## Layout contract and verification

Before authoring a view, identify its title, content width, meaningful sections,
field order, action hierarchy, lookup boundary, and narrow-screen behavior.
Presentation recipes own exact geometry; model metadata owns labels and grouping.
Do not invent Card, Grid, DatePicker, or other unregistered widget names.

Generated JSON validity is only the first gate. Render the emitted document with
the exact host runtime and stylesheet. Check field/section gaps, bounded form
width, wrapping actions, readable helper text, pagination geometry, focus, and
loading/error/empty states at narrow and wide widths. Capture reviewed screenshots.
