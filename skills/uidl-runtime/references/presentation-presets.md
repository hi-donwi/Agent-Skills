# Presentation Presets Across Repositories

Use a presentation preset when several hosts need the same UIDL composition and token decisions
without sharing a domain model or a concrete data adapter.

## Ownership

Keep one source of truth per concern:

| Boundary | Owns | Must not own |
|---|---|---|
| Reference app | Synthetic fixtures, screenshots, browser journeys, and visual evidence | Shared runtime contracts or business-model compilers |
| UIDL Runtime | Manifest, catalog, semantic themes, widget requirements, and neutral recipes | Business entities, tenant data, HTTP, SQL, or branded domain names |
| Domain projection | Business semantics, permissions, workflows, and UIDL screen references | CSS, JSX, concrete React state, or theme values |
| Builder | Catalog discovery, preview, authoring, application, and export | A second preset definition or renderer semantics |
| Host | Trusted adapter, command/mutation/download handlers, capabilities, tenancy, and composition | A renderer fork or an untrusted adapter supplied by a document |
| Skill library | Portable extraction, boundary-review, routing, and conformance guidance | Product implementation or materialised consumer copies |

## Manifest contract

A manifest is a discoverable contract, not a theme dump. At minimum declare:

```json
{
  "id": "dense-business",
  "version": "0.1.0",
  "kind": "presentation-preset",
  "targets": ["react"],
  "themes": ["light", "dark"],
  "recipes": ["shell", "list", "form", "report", "print"],
  "requiredWidgets": ["Column", "Row", "TextField", "DataTable", "Button"],
  "capabilities": ["data-adapter", "host-actions"],
  "provenance": { "source": "uidl-runtime" }
}
```

Pin the preset and version in a consuming document or export. Do not infer target support from
the React catalog: Flutter and Android may expose fewer widgets and different layout behavior.

## Extraction workflow

1. Freeze the reference route, screenshot, and test inventory before changing shared code.
2. Classify each asset as token, recipe, widget, host interaction, domain fixture, or evidence.
3. Move only neutral presentation decisions into the runtime catalog.
4. Keep reads behind `DataAdapter` and writes behind allowlisted host handlers; fail closed.
5. Have projection and builder consumers reference the catalog rather than copy definitions.
6. Let the host supply trust, tenancy, capabilities, and handlers; never let a document select them.

## Conformance matrix

Run one synthetic list, form, report, and print journey through every available boundary. Compare:

- schema validation and pinned preset resolution;
- accessible names, keyboard focus, and error announcements;
- loading, empty, error, pagination, responsive, and dark-mode states;
- route and host-action intent without network or database references in UIDL;
- screenshots and computed geometry at narrow and wide widths.

Record unavailable targets as explicit gaps. A passing JSON schema check is necessary, not visual
acceptance.
