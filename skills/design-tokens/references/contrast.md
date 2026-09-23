# Contrast as a token constraint

Load when defining colour tokens. The point of this document is timing: contrast checked
while defining a token is a value change, contrast checked at review is a redesign.

## The ratios

| Content | Minimum | Why it is that number |
|---|---|---|
| Body text | 4.5:1 | WCAG 2.1 AA, 1.4.3 |
| Large text (≥24px, or ≥19px bold) | 3:1 | 1.4.3 — larger glyphs carry more signal per pixel |
| UI component boundaries, focus rings, icons that carry meaning | 3:1 | 1.4.11 |
| Decorative graphics, disabled controls | none | Exempt, but see below |

"Disabled is exempt" is true and still a trap: a disabled control nobody can read is a
control nobody can tell is disabled. Keep it distinguishable even though the rule does not
force it.

## Pair tokens, do not check colours

A colour has no contrast ratio. A *pair* does. So the declaration records pairs:

| Foreground token | Allowed on | Ratio |
|---|---|---|
| `--color-text` | `--color-surface`, `--color-surface-raised` | 14.8:1, 13.1:1 |
| `--color-text-muted` | `--color-surface` | 4.7:1 |
| `--color-on-accent` | `--color-accent` | 5.2:1 |
| `--color-danger` | `--color-surface` | 4.9:1 |

A foreground used on a background not in its row is a bug, whatever it looks like. This is
also what makes the check mechanical rather than aesthetic: there is a finite list of pairs,
and each one either passes or does not.

## Every theme, not the default one

A pair that passes in light frequently fails in dark, because the same hue against a dark
surface has a different relative luminance. Check each pair in each theme. Dark themes fail
most often on muted text and on accent-on-surface.

Pure `#000` backgrounds are the common dark-mode mistake: maximum contrast produces halation
around light text and reads as harsh. A very dark grey with a slight hue is easier to read
and still clears 4.5:1 comfortably.

## Non-colour signalling

Contrast solves legibility, not meaning. A reader who cannot distinguish red from green gets
nothing from a red border alone. Every state that colour conveys also carries a second
signal — an icon, a label, a shape, or text.

This is WCAG 1.4.1, and it is the failure most often found late, because the person writing
the component can see the colour.

## Checking

- In the browser: DevTools shows the ratio in the colour picker and flags failures in the
  accessibility pane.
- In CI: a script that walks the declared pairs and computes the ratio catches a token edit
  that breaks a pair nobody re-tested.
- The one that matters most costs nothing: define the pair, check it, write the ratio in the
  declaration. It is then a documented fact rather than an assumption.
