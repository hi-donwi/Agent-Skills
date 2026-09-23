# Fluid type and spacing

Load when sizing text or space across widths. The failure this prevents is subtle: stepped
type is correct at the breakpoints and slightly wrong everywhere else, which is most of the
time.

## The clamp() formula

```css
font-size: clamp(MIN, PREFERRED, MAX);
```

`PREFERRED` carries a viewport or container unit so the value scales; `MIN` and `MAX` stop
it. To scale from `MIN` at width `W1` to `MAX` at width `W2`:

```
slope      = (MAX - MIN) / (W2 - W1)
intercept  = MIN - W1 * slope
PREFERRED  = intercept + 100vw * slope     /* or 100cqi inside a container */
```

Worked: 1rem at 320px up to 1.5rem at 1280px, with a 16px root —

```
slope     = (24 - 16) / (1280 - 320) = 0.00833
intercept = 16 - 320 * 0.00833 = 13.33px = 0.833rem
```

```css
font-size: clamp(1rem, 0.833rem + 0.833vw, 1.5rem);
```

Keep a `rem` term in `PREFERRED`. That is what preserves the zoom trap fix below.

## The zoom trap

```css
font-size: clamp(1rem, 2.5vw, 2rem);   /* wrong */
```

`vw` does not change when the reader zooms, so between the bounds the text does not grow —
the page fails WCAG 1.4.4 (resize text to 200%) for the readers who most need it. Including
a `rem` term, as the formula does, keeps zoom working because `rem` responds to it.

## A scale, not per-element values

Define fluid steps once as tokens, then use the steps:

```css
:root {
  --text-sm:   clamp(0.875rem, 0.85rem + 0.12vw, 0.95rem);
  --text-base: clamp(1rem,     0.95rem + 0.25vw, 1.125rem);
  --text-lg:   clamp(1.25rem,  1.15rem + 0.5vw,  1.5rem);
  --text-xl:   clamp(1.5rem,   1.3rem  + 1vw,    2.25rem);
  --text-2xl:  clamp(2rem,     1.6rem  + 2vw,    3.5rem);
}
```

Headings can scale harder than body text — a display size doubling is fine, body text
doubling is not, because measure and line length stop working. Body text belongs in a narrow
band; most of the fluidity belongs at the top of the scale.

## Fluid space

The same technique applies to gutters and section rhythm, and matters more than it looks:
fixed 4rem section padding is generous on a phone and mean on a desktop.

```css
:root {
  --space-gutter:  clamp(1rem, 0.75rem + 1.5vw, 2rem);
  --space-section: clamp(3rem, 2rem + 5vw, 8rem);
}
```

Keep small, functional spacing fixed. The gap between a label and its input is a fixed
relationship, not a fluid one — scaling it just makes forms loose on wide screens.

## Inside a component

Swap `vw` for `cqi` so the value tracks the container rather than the window. A card in a
narrow sidebar then gets small type even on a wide monitor, which is the whole point.

```css
.card { container-type: inline-size; }
.card__title { font-size: clamp(1rem, 0.9rem + 2cqi, 1.5rem); }
```

## Line length and leading

Fluid size without a measure constraint produces very long lines on wide screens. Cap it:

```css
.prose { inline-size: min(65ch, 100%); }
```

Leading should loosen as size drops, not stay constant — `line-height: 1.5` on body and
`1.1`–`1.2` on display sizes. A unitless value inherits proportionally, which is why it is
the right form.
