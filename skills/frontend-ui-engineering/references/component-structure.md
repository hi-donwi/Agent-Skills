# Component structure

Load this when placing, splitting, or composing UI components. Layer rules live in
`component-reuse.md`.

## File structure

Colocate everything related to a component:

```
src/components/
  TaskList/
    index.ts              # Public exports for this component family
    TaskList.tsx          # Parent/orchestrating component
    TaskItem.tsx          # Private or family-level subcomponent
    TaskListEmpty.tsx     # Focused UI state
    TaskList.test.tsx     # Tests
    TaskList.stories.tsx  # Storybook stories (if using)
    use-task-list.ts      # Custom hook (if complex state)
    types.ts              # Component-specific types (if needed)
```

Keep small components in one file while they remain easy to understand. Create a component
directory when the component has supporting files, meaningful subcomponents, tests, stories,
types, or a scoped hook. Do not create deep directory nesting for trivial wrappers.

## Decomposing large components

A reusable component may itself be composed of smaller components. Split it when its size or
number of responsibilities makes the file difficult to understand, test, or safely change.
Treat **200 lines as a review threshold**, not a target and not the only reason to split.

Split a component when one or more of these signals apply:

- It exceeds roughly 200 lines and contains multiple meaningful UI regions.
- A JSX section has its own purpose, props, conditional states, or interaction behavior.
- Rendering, state orchestration, data adaptation, and event handling compete in one file.
- A section is repeated, independently testable, or likely to be reused.
- The component has deeply nested JSX or requires scrolling between related handlers and markup.
- A change to one visual region routinely risks unrelated regions.

Decompose by responsibility:

| Concern | Extract To |
|---|---|
| Distinct visual region | Focused subcomponent |
| Reusable visual pattern | Shared component or design-system primitive |
| State, effects, event orchestration | Custom Hook |
| Pure formatting, mapping, validation | Utility / Helper |
| Business workflow or API integration | Service |

The parent component should express composition and high-level orchestration. A subcomponent
should own one coherent visual responsibility and receive the smallest practical props. Avoid
passing a parent's entire state object merely to reduce the number of props.

```tsx
// TaskList/TaskList.tsx — composition stays easy to scan
export function TaskList({ tasks }: TaskListProps) {
  const list = useTaskList(tasks);

  return (
    <section>
      <TaskListHeader count={list.visibleTasks.length} />
      <TaskFilters value={list.filter} onChange={list.setFilter} />
      <TaskItems tasks={list.visibleTasks} onToggle={list.toggle} />
      {list.visibleTasks.length === 0 && <TaskListEmpty />}
    </section>
  );
}
```

Do not split mechanically into tiny one-use components that hide straightforward markup.
Extraction must improve at least one of: readability, cohesion, testability, reuse, or change
isolation.

## Subcomponent placement

Place a component at the narrowest scope where it is genuinely reusable:

```text
src/
  components/
    ui/                       # App-wide primitives: Button, Dialog, Tabs
    TaskList/                 # One component family
      index.ts                # Deliberate public API
      TaskList.tsx            # Public parent component
      TaskItem.tsx            # Family-level subcomponent
      TaskListEmpty.tsx
      use-task-list.ts
      types.ts
  features/
    tasks/
      components/             # Components reusable only inside the tasks feature
```

- Keep a subcomponent beside its parent when it is used only by that component family.
- Do not export private subcomponents from `index.ts`.
- Export family-level subcomponents only when consumers have a valid composition use case.
- Move a component to feature-level `components/` when multiple components in that feature use it.
- Move it to shared `components/ui/` only when it is domain-agnostic and reused across features.
- Use one component per file once extracted; use names that describe UI responsibility.
- Keep tests, stories, styles, types, and tightly scoped hooks next to their component family.
- Prefer shallow, predictable directories; avoid generic dumping grounds such as `misc/`,
  `common/`, or `shared/` without a clear scope.
- Follow the nearest project `AGENTS.md` and existing component-library conventions when their
  directory names differ from this example.

## Component patterns

**Prefer composition over configuration:**

```tsx
// Good: Composable
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// Avoid: Over-configured
<Card
  title="Tasks"
  headerVariant="large"
  bodyPadding="md"
  content={<TaskList tasks={tasks} />}
/>
```

**Keep components focused:**

```tsx
export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-center gap-3 p-3">
      <Checkbox checked={task.done} onChange={() => onToggle(task.id)} />
      <span className={task.done ? 'line-through text-muted' : ''}>{task.title}</span>
      <Button variant="ghost" size="sm" onClick={() => onDelete(task.id)}>
        <TrashIcon />
      </Button>
    </li>
  );
}
```

**Separate data fetching from presentation:**

```tsx
export function TaskListContainer() {
  const { tasks, isLoading, error } = useTasks();

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="Failed to load tasks" retry={refetch} />;
  if (tasks.length === 0) return <EmptyState message="No tasks yet" />;

  return <TaskList tasks={tasks} />;
}

export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul role="list" className="divide-y">
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
    </ul>
  );
}
```

## State management

Choose the simplest approach that works:

```
Local state (useState)           → Component-specific UI state
Lifted state                     → Shared between 2-3 sibling components
Context                          → Theme, auth, locale (read-heavy, write-rare)
URL state (searchParams)         → Filters, pagination, shareable UI state
Server state (React Query, SWR)  → Remote data with caching
Global store (Zustand, Redux)    → Complex client state shared app-wide
```

Avoid prop drilling deeper than 3 levels. If you're passing props through components that don't use them, introduce context or restructure the component tree.
