# Visual polish and feedback states

Load when the component exists and the question is whether it looks and behaves like
production work. Three neighbouring skills own the rest: `design-tokens` for the palette,
type scale and theming; `responsive-layout` for sizing and breakpoints;
`accessibility-audit` for verifying the result.

## Avoid the AI aesthetic

AI-generated UI has recognizable patterns. Avoid all of them:

| AI Default | Why It Is a Problem | Production Quality |
|---|---|---|
| Purple/indigo everything | Models default to visually "safe" palettes, making every app look identical | Use the project's actual color palette |
| Excessive gradients | Gradients add visual noise and clash with most design systems | Flat or subtle gradients matching the design system |
| Rounded everything (rounded-2xl) | Maximum rounding signals "friendly" but ignores the hierarchy of corner radii in real designs | Consistent border-radius from the design system |
| Generic hero sections | Template-driven layout with no connection to the actual content or user need | Content-first layouts |
| Lorem ipsum-style copy | Placeholder text hides layout problems that real content reveals (length, wrapping, overflow) | Realistic placeholder content |
| Oversized padding everywhere | Equal generous padding destroys visual hierarchy and wastes screen space | Consistent spacing scale |
| Stock card grids | Uniform grids are a layout shortcut that ignores information priority and scanning patterns | Purpose-driven layouts |
| Shadow-heavy design | Layered shadows add depth that competes with content and slows rendering on low-end devices | Subtle or no shadows unless the design system specifies |
| Emojis in enterprise controls | Casual emojis look unprofessional, degrade visual density, and disrupt enterprise credibility | Strictly zero emojis: use semantic SVG icons, typed badges, and clean tabular indicators |
| Cramped element spacing (<16px) | Squeezing inputs and action buttons together leads to misclicks and touch targeting errors | Maintain minimum 16px vertical element spacing across form inputs, actions, and sections |
| Arbitrary corner radii mixing | Randomly mixing sharp, subtle, and oversized radii destroys layout rhythm | Enforce uniform radius hierarchy: control radius (4-6px) and card radius (8-12px) |
| Harsh black / dark solid borders | Harsh black lines overpower content, break visual flow, and signal broken CSS fallbacks (e.g. Tailwind v4 currentColor fallback) | Strictly enforce whisper-soft borders (#e8ecf1, #f1f5f9, or rgba(255,255,255,0.08) in dark mode). Never let borders default to black currentColor. Use subtle card elevation (0 1px 3px rgba(0,0,0,0.04)) over heavy solid strokes |

## Adopt 2026 aesthetics deliberately, not by default

Current web-design trends are legitimate vocabulary, but each fits only some products.
Adopt with a reason recorded in the design declaration; drop without one.

| Trend | Adopt when | Reject when |
|---|---|---|
| Dopamine / high-chroma colour | Brand-led consumer surfaces; used as accent on a controlled token | Any data-dense or compliance surface; as the default palette |
| Neo-brutalism | Brand personality that owns it (dev tools, creative studios) | Professional or enterprise products; mixed into an otherwise neutral system |
| 3D / WebGL scenes | One hero moment on a marketing or creative surface; loaded lazily, reduced-motion aware | Dashboards, applications, anything above-the-fold on a utility screen |
| Experimental navigation | Exploratory or artistic sites | Applications; discoverability and keyboard support are non-negotiable |
| Dark mode | Ships only at full parity: checked pairs, tonal surfaces, updated imagery and charts | Inverted with naive filters, or pairs never re-checked |
| Soft / organic shapes and oversized radii | Consumer-friendly products with the radius scale declared first | When radius values start being chosen per component |
| AI-driven interfaces (agentic chat, voice, adaptive smart forms) | When the task genuinely benefits from delegation or capture speed | Bolted on as a widget; voice without a visible transcript and an exit |

Aesthetic-Usability (Law of UX): users judge a beautiful interface as more usable even when
it is not. That is a risk to manage — never accept a hand-test failure because the surface
looks good — and never an excuse to ship unpolished work either.

## Loading and transitions

```tsx
function TaskListSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading tasks">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-12 bg-muted animate-pulse rounded" />
      ))}
    </div>
  );
}

function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previous = queryClient.getQueryData(['tasks']);

      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map(t => t.id === taskId ? { ...t, done: !t.done } : t)
      );

      return { previous };
    },
    onError: (_err, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context?.previous);
    },
  });
}
```

Skeleton loading for content, not spinners. Optimistic updates for perceived speed; roll back on error.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "Accessibility is a nice-to-have" | It's a legal requirement in many jurisdictions and an engineering quality standard. |
| "We'll make it responsive later" | Retrofitting responsive design is 3x harder than building it from the start. |
| "The design isn't final, so I'll skip styling" | Use the design system defaults. Unstyled UI creates a broken first impression for reviewers. |
| "This is just a prototype" | Prototypes become production code. Build the foundation right. |
| "The AI aesthetic is fine for now" | It signals low quality. Use the project's actual design system from the start. |
