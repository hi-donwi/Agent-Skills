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

## Translate a design-system decision into the actual vocabulary

A document carries design decisions only if they fit the real reference vocabulary
(`StyleIntent` in `packages/core/src/types/theme.ts`) and the installed theme engine.
Supported dimensions include gap, padding/margin per side and shorthand, width and
min/max-sizes, flex direction/justify/align, display, positioning (relative through
sticky, inset, z-index), background, color, fontSize/fontWeight/lineHeight/letterSpacing,
borderRadius, borderWidth/borderColor, shadow, opacity, and a single typography token
reference. Anything else is not a decision the document can state.

1. **Values are intent values, not literal CSS.** Structural fields take the engine's
   utility-class values (`gap-4`, `max-w-xl`) and colour/typography may take token
   references (`{primitives.color.primary}`, `{semantics.typography.headline-medium}`).
   A raw `16px` in `gap` renders nothing — the design decision died in translation.
2. **Responsive decisions use the object form.** `{ "base": "p-4", "md": "p-6" }` is how
   a window-class or breakpoint decision lands. Use the host's declared breakpoints —
   check `theme.breakpoints` instead of assuming Tailwind's.
3. **A design system lands in three places, nowhere else.**
   - Colour roles and pairing -> `primitives.color` / semantic colour tokens on the Theme.
   - Type scale -> semantic `typography` tokens applied with the `typography` field.
   - Spatial rhythm -> spacing `primitives` referenced through `gap`/`padding` values.
   Elevation by surface tint or tonal level must be expressed with the supported
   `background`/`shadow` fields; inventing an `elevation` key renders nothing.
4. **Trends and system conventions stop at the boundary.** Something Apple HIG or M3
   "says" only applies if the installed StyleIntent/theme can state it. Record the delta
   in the design declaration instead of sneaking CSS into documents. Context-level
   system choice lives in `uiux-design-systems`; token tiers live in `design-tokens`.

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


## Whisper-soft borders and border-color safety

Never allow borders to default to browser or `currentColor` fallbacks. In Tailwind v4,
`--tw-border-style: solid` is registered globally; omitting a paired `border-color`
causes cards, dividers, and tables to fall back to `currentColor` (harsh solid black).
The upgraded `uidl-runtime/style.css` enforces universal whisper-soft defaults
(`border-color: var(--color-gray-200, #e8ecf1)` in light mode, and `#262626` in dark mode)
across shadow roots and document contexts. Host implementations should leverage
subtle card elevation (`shadow-sm`, `0 1px 3px rgba(0,0,0,0.04)`) alongside soft borders
rather than heavy outlines.
