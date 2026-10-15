# Layout and theming against the installed runtime

## Verify the artifact first

Read the host import, package exports, lockfile, widget manifest, and actual CSS
entry point. A local core checkout can differ from the published package used by
a server projector. Do not infer capabilities from release notes or a skill alone.

## Theme objects must satisfy the real type

Extend a complete preset rather than inventing an incomplete Theme object:

```tsx
import { meridianLightTheme, type Theme } from "uidl-runtime";

export const brandTheme: Theme = {
  ...meridianLightTheme,
  id: "brand-light",
  name: "Brand Light",
  mode: "light",
  primitives: {
    ...meridianLightTheme.primitives,
    color: {
      ...meridianLightTheme.primitives.color,
      primary: "#1d4ed8",
      "text-primary": "#172033",
      "text-secondary": "#475569"
    }
  }
};
```

The Theme contract uses `mode`, not `colorScheme`, and requires breakpoints,
primitive and semantic maps, and variants. Import the runtime stylesheet once.
A host's theme attribute, dark class, renderer theme, and token scope must agree.

## StyleIntent is not a plain CSS declaration

The React engine maps structural StyleIntent values to utility classes. Use
`gap: "gap-4"`, `padding: "p-4"`, `width: "w-full"`, and
`maxWidth: "max-w-xl"`. A value such as `gap: "16px"` becomes an ineffective class;
`maxWidth: "36rem"` and `margin: "0 auto"` have the same problem.

```json
{
  "id": "form-layout",
  "type": "Form",
  "style": {
    "display": "flex",
    "flexDirection": "column",
    "gap": "gap-4",
    "width": "w-full",
    "maxWidth": "max-w-xl",
    "padding": { "base": "p-4", "md": "p-6" }
  }
}
```

Use only utilities shipped by the installed stylesheet or explicitly compiled by
the host. Responsive class generation does not guarantee that CSS exists.
Primitive token references such as `{primitives.color.text-secondary}` can resolve
to inline CSS variables. Verify each property: do not assume every semantic token
reference or responsive token value is implemented. Node `props.style` is a React
CSS object escape hatch, not the same interface as node `style`; keep it in a
reviewed host or shared presentation recipe.

## Compose the page deliberately

Row, Column, and Form names alone supply no default flex layout or gap. Declare
layout explicitly or use a supported presentation composition. Scope internal
spacing to the parent: field group, form section, action group, and page gutter
are different relationships. A form normally has bounded width; a data table can
use the available content width.

Use `examples/admin-form.uidl.json` as a runtime-validated starting document. Keep
lookup search, loading/retry, selection, and paging in one field group. Put save
and return/reload controls in a wrapping action group. Display read-only counts as
summaries where users cannot edit them.

Administration composition helpers (`createAdminHeader`, `createAdminSection`,
`createAdminForm`, `createAdminActionBar`) and `uidl-admin-*` CSS hooks are additive
in the upgraded runtime source. Confirm exports before importing them; published
0.1.8 does not include these helpers. Generic widgets keep their original layout.

## Density and control geometry

The reference controls support their documented `small`/`large` size props.
Do not assume DataTable supports a `density` prop, arbitrary column widgets, or
32/48/60px density tiers unless its installed manifest and implementation do.

Keep an icon's size separate from its pointer target. Pagination needs square
controls, aligned status, correct empty/single/multiple-page behavior, and adequate
spacing. Never fix internal pagination by applying height or padding to every
button in the host. Prefer supported component hooks and theme tokens.

## Evidence before completion

Validate the document and registry, then render it. Inspect computed display,
gap, width, height, token values, and the CSS cascade. Test narrow and wide widths,
long text, loading/error/empty states, keyboard focus, and actual theme contrast.
Capture screenshots; do not accept a new snapshot merely because a tool created it.
