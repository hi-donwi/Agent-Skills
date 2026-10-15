# Layout quality for hand-built and declarative UI

## Define relationships before implementation

Reuse an existing page contract, or record its purpose, title hierarchy, content
width, field/section groups, action placement, density, and narrow-screen behavior.
Use the same review criteria for JSX, generated pages, and UIDL documents.

| Relationship | Starting design value |
|---|---|
| Label to control | 4-8 px |
| Icon to button text | 8 px |
| Related actions | 8-12 px |
| Field groups | 16-24 px |
| Last field to actions | 24 px |
| Sections | 24-32 px |
| Page gutter | 16 px narrow; 24-32 px wide |
| Single-column form width | 36-42 rem maximum, bounded by its parent |

These values are defaults for a neutral administration surface, not universal
requirements. Use the project's semantic spacing roles and supported rendering API.
Avoid full-width desktop action buttons unless the page contract calls for them.
Wrap an action group with a real gap; do not stack touching buttons.

## Control anatomy

Separate icon dimensions, label typography, internal padding, and pointer target.
A pager icon can be 16px while its target is square and at least 24px per side.
WCAG AA permits specific target-size exceptions; 44px is a useful primary-touch
policy, not the AA minimum. Density must not silently shrink hit targets.

Align pager buttons and page status vertically. Test zero records, one page, many
pages, page boundaries, long totals, and page-size changes. Keep lookup pagination
inside the lookup field/group rather than between unrelated form fields.

Read-only usage counts normally read as summaries. Use meaningful section titles;
generic numbered sections are a fallback for missing metadata.

## Diagnose CSS before patching it

1. Inspect computed display, gap, dimensions, min/max constraints, and box sizing.
2. Verify the stylesheet contains the utility class the renderer actually emitted.
3. Inspect cascade layers, specificity, inheritance, inline styles, and token scope.
4. Check that theme mode, root class/attribute, and foreground/background tokens agree.
5. Fix the owner: shared control, shared recipe, or host integration. Broad rules
   such as styling every descendant button can deform internal pagination.

## Completion evidence

Render the actual target artifact at narrow and wide widths; include 320/390,
768, and 1440px where relevant. Check long text, empty/loading/error states,
keyboard focus, zoom/reflow, actual theme contrast, and wrapping actions.

Use geometry assertions for overlapping/touching controls and distorted targets.
Use screenshots to inspect hierarchy, rhythm, and typography. Review snapshot
changes before accepting them. Functional checks and valid JSON cannot replace
this evidence. If a browser is unavailable, report visual verification as unrun.

Sources: [W3C target sizing](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html),
[W3C contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html),
[MDN cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Introduction).
