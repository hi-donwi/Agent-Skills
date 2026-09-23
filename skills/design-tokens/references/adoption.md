# Introducing tokens into a codebase that already has values

Load when the system is being added to existing code rather than started with it. The
failure mode here is not writing the tokens — it is ending up with two systems running at
once, indefinitely.

## Find what is already there

```bash
# raw colours in component code
rg -n '#[0-9a-fA-F]{3,8}\b' --glob '!*.test.*' src/
# off-scale spacing
rg -n '\b\d+px\b' src/ | rg -v '1px|0px'
# what a theme config already declares
rg -n 'colors|spacing|borderRadius|fontSize' tailwind.config.* theme.* 2>/dev/null
```

Cluster the results before naming anything. Four greys within a few percent of each other
are one token and three mistakes; two greens that differ visibly are two roles. The cluster
count is the size of the real system, which is almost always smaller than the file suggests.

## Convert in the order that makes the next step cheaper

1. **Colour first.** It is the most duplicated, the most visible, and the prerequisite for
   theming.
2. **Spacing second.** Usually already near a scale; the work is rounding to it.
3. **Radius, elevation, type last.** Fewer values, lower risk, and by then the pattern is
   established.

Convert by surface, not by token. Finishing one page means it can be reviewed and themed;
converting every `--color-text` across the app leaves nothing demonstrably done.

## Do not migrate what is being deleted

A screen scheduled for replacement gets no conversion. Note it and move on. This is the
cheapest decision available and the one most often skipped.

## Close the door

A migration with no gate regresses, because the next contributor has no signal. Add the rule
as soon as the first surface is converted, not when the last one is:

```jsonc
// stylelint
{
  "rules": {
    "declaration-property-value-disallowed-list": {
      "/^(color|background|border-color)/": ["/^#/", "/^rgb/"]
    }
  }
}
```

ESLint equivalents exist for inline styles and for Tailwind arbitrary values
(`bg-[#0b7a3b]`), which are the usual way a raw value re-enters a tokenised codebase.

Allow the primitive tier's own file, and nothing else.

## When the design changes mid-migration

Change the primitive, not the call sites. If changing a brand colour requires touching
components, the tiers are not one-directional yet — find the component reading a primitive
and fix that instead of doing the rename.
