# Production UI Checklist

Use this for review mode or as a self-check before delivery.

## Product Fit

- The screen's primary job is obvious within a few seconds.
- Visual direction matches audience, industry, and brand context.
- One primary action per view; secondary and destructive actions are clearly
  subordinate.
- Realistic copy/data is used for layout validation.

## Design System

- Semantic color tokens exist for background, surface, text, border, primary,
  danger, success, warning, and muted states.
- Typography has a clear scale and one page-level heading.
- Spacing follows the project scale; no arbitrary visual one-offs.
- Radius, elevation, border, and icon stroke choices are consistent.
- Dark mode values are designed, not just inverted.

## Component Architecture

- Components are focused and composable.
- Data fetching and mutation logic is separated from presentational components.
- State is kept as local as possible; URL state is used for shareable filters or
  pagination.
- New dependencies are justified and consistent with the stack.

## States and Feedback

- Default, hover, active, focus, disabled, loading, empty, error, success, and
  validation states are handled where relevant.
- Forms have visible labels, helper text for complex fields, and inline errors.
- Async actions show progress and prevent accidental duplicate submission.
- Destructive actions have confirmation or undo where appropriate.

## Accessibility

- Interactive elements are semantic buttons/links or have equivalent keyboard
  behavior.
- Focus order matches visual order and focus states are visible.
- Icon-only controls have accessible names.
- Normal text contrast is at least 4.5:1; large text and UI glyphs meet their
  relevant contrast targets.
- Status is not communicated by color alone.
- Route changes, dialogs, menus, and toasts manage focus/announcements correctly.

## Responsive Layout

- Verified at 320/375, 768, 1024, and 1440px where practical.
- No horizontal scroll on mobile.
- Text wraps cleanly without overlapping controls.
- Fixed headers, bottom bars, and safe areas do not cover content.
- Tables, charts, and dense grids have mobile-specific layouts.

## Performance and Polish

- Images have dimensions or aspect ratios to prevent layout shift.
- Fonts use sensible loading behavior and avoid excessive variants.
- Long lists are virtualized or paginated.
- Animations use transform/opacity where possible and respect reduced motion.
- Browser console is clean.
