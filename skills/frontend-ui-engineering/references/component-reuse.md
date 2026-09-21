# Reusability Standards (workspace pattern)

Applies to **all projects**. See `AGENTS.md` → _Architecture Conventions — Reusability Standards_
for the full specification. This reference covers implementation patterns for each of the four
classifications.

## The Four Classifications

| Category | Implementation | Directory |
|---|---|---|
| Reusable UI / presentation | Component | `components/` |
| Reusable logic (state, effects) | Custom Hook | `hooks/` |
| Stateless pure function | Utility / Helper | `utils/` or `helpers/` |
| Business workflow / API integration | Service | `services/` |

## 1. Component Reuse

### Workflow

1. **Discover** — grep / glob `components/ui`, `page-kit`, `design-system`, Storybook.
2. **Reuse** — import existing primitive; pass props / variants.
3. **Extend** — add variant, density, or prop to the primitive when multiple pages need the same change.
4. **Wrap** — domain-specific tab/nav config in a thin wrapper (no duplicate CSS).

### Anti-patterns

- Inline `border-b-2` / `role="tablist"` tab strips in page components
- Copy-paste nav markup across pages
- New `*SettingsTabs.tsx` files that reimplement link/button styling
- Per-page padding overrides when `density` or `variant` on the primitive would suffice

### Decomposing a reusable component

Reusable components can be decomposed into smaller reusable or private subcomponents. Review a
component for decomposition when it approaches or exceeds roughly 200 lines, but make the
decision based on responsibilities rather than line count alone.

Extract a subcomponent when it represents a coherent visual region, owns meaningful conditional
rendering or interaction, is independently testable, repeats, or can change without requiring
knowledge of the entire parent. Extract state/effects to a Hook, pure transformations to a
Utility, and business/API work to a Service.

Keep extracted subcomponents at the narrowest valid scope:

| Reuse scope | Placement |
|---|---|
| Used only by one component family | Colocate under that component's directory; keep private |
| Used by several components in one feature | `features/<feature>/components/` |
| Domain-agnostic and used across features | Shared component library such as `components/ui/` |

Use a component directory once a component has meaningful subcomponents or supporting files.
Keep the directory shallow, use one extracted component per file, and expose only intentional
public APIs through `index.ts`. Do not create tiny wrapper components merely to reduce line count,
and do not promote feature-specific components into the global UI library prematurely.

### Tab / sub-navigation pattern

| Need | Approach |
|---|---|
| Route-based tabs | Shared primitive + `href` on items (or framework `Link`) |
| In-page section tabs | Shared primitive + `onChange` |
| Form sections (top/bottom) | Shared form tab bar wrapping the same primitive |
| Many tabs (6+) | `density="comfortable"` (or project equivalent) on the primitive |
| Pill / icon tabs | `variant="pill"` (+ optional `icon` per item) |

Adjust spacing **once** on the primitive; pages only pass `items`, `active`, `variant`, `density`.

## 2. Custom Hook Reuse

### Rules

- Every custom hook **must start with `use`**.
- Hooks encapsulate state, side effects, and reusable behaviors.
- Components consume hooks; hooks never render UI.
- Shared hooks live under `hooks/` (or `components/*/use-*.ts` for tightly scoped hooks).

### Example pattern

```typescript
// hooks/use-auth.ts
export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  // ... state logic, side effects, return values
  return { user, login, logout, isLoading };
}

// Component consumes the hook
function ProfilePage() {
  const { user, logout } = useAuth();
  // ...
}
```

## 3. Utility / Helper Reuse

### Rules

- Utilities are **framework-independent** pure functions.
- They must not manage React state or perform UI rendering.
- Group by domain: `utils/date.ts`, `utils/format.ts`, `utils/validation.ts`.

### Example pattern

```typescript
// utils/format.ts — stateless, framework-independent
export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}
```

## 4. Service Reuse

### Rules

- Services contain **business rules and domain workflows**.
- They handle communication with APIs, databases, and external systems.
- Components and Hooks delegate business operations to Services.
- Shared services live under `services/`.

### Example pattern

```typescript
// services/user-service.ts
export class UserService {
  async fetchProfile(userId: string): Promise<UserProfile> {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) throw new ApiError('Failed to fetch profile');
    return response.json();
  }
}

// Component delegates to Service via Hook
function ProfilePage() {
  const { profile, isLoading } = useUserProfile(userId);  // Hook calls UserService
}
```

## Layer Enforcement

```
UI Layer         → Components         (render, no business logic)
State & Behavior → Custom Hooks        (state, effects, delegate to services)
Shared Functions → Utilities / Helpers (pure, framework-independent)
Business Logic   → Services            (APIs, domain workflows)
```

## Project-specific documentation

Each repo should document its kit paths, service patterns, and named wrappers in the
nearest nested `AGENTS.md`, so an agent finds them without searching. The shape:

| Primitive | Path |
|---|---|
| `PageTabs` | `src/components/ui/page-kit.tsx` |
| Setup tabs wrapper | `SetupSettingsTabs` → `PageTabs` (`density="comfortable"`) |
| Form tabs wrapper | `FormBottomTabBar` → `PageTabs` |

A table like this is what stops an agent from inventing a fourth tab component. Pair it
with an enforcement rule in the project's agent rules file.
