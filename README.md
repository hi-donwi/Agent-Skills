# Agent Skills

Portable, agent-agnostic **skills** in the open Agent Skills format: a `SKILL.md` entry
point with YAML frontmatter and concise instructions, plus a `references/` folder an agent
loads only when it needs the detail.

48 skills, grouped into packs. Nothing here names a company, a client, or a private
codebase. Skills may be specific to a **technology** — that is what a pack is: `java` is
Quarkus and Panache, `uidl-runtime` is the UIDL package and its spec. The line is whether
someone outside this organisation, using that technology, could pick the skill up
unchanged.

## Why a separate repository

A skill is knowledge about *how to do a kind of work*. It outlives any one project and it
is worth sharing between them — including work tied to a particular stack, which is why
some packs are named after one. Keeping skills in their own repository means one version,
one history, and one place to improve them — and lets a workspace pull **only the packs it
needs** rather than carrying all of them.

Consumed by [Agent-Workspace](https://github.com/hi-donwi/Agent-Workspace) via
`ws skills add <name>` / `ws skills sync`, which materialises the selected skills with a
sparse checkout pinned to a commit. It works standalone too — clone it and point your agent
at `skills/`.

## Packs

### `core` — engineering practice

Language-agnostic. How to plan, build, review, debug, ship, and keep a codebase healthy.

| Skill | Use it when |
|---|---|
| [`api-design`](skills/api-design/SKILL.md) | adding or changing an HTTP/RPC endpoint, a public library interface, or a service contract, or when reviewing an interface for consistency |
| [`changelog-generator`](skills/changelog-generator/SKILL.md) | Generate user-facing changelogs, release notes, upgrade notes, and internal change summaries from git history, PRs, issues, commits, or diff… |
| [`ci-cd`](skills/ci-cd/SKILL.md) | adding GitHub Actions (or similar), defining quality gates, fixing a failing pipeline, or designing a release/rollout |
| [`code-review`](skills/code-review/SKILL.md) | asked to review code, before merging a change, or to self-review a diff |
| [`code-simplification`](skills/code-simplification/SKILL.md) | refactoring code for clarity without changing behavior. code works but is harder to read, maintain, or extend than it should be. reviewing code… |
| [`codebase-onboarding`](skills/codebase-onboarding/SKILL.md) | starting work in an unknown or large codebase, before major refactors, or when asked to explain how a project works |
| [`debugging`](skills/debugging/SKILL.md) | facing a bug, stack trace, failing test, crash, or unexpected behavior, or when a fix attempt did not work |
| [`dependency-audit`](skills/dependency-audit/SKILL.md) | adding dependencies, fixing audit findings, upgrading packages, or reducing dependency surface |
| [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) | removing old systems, APIs, or features. migrating users from one implementation to another. deciding whether to maintain or sunset existing code |
| [`documentation-and-adrs`](skills/documentation-and-adrs/SKILL.md) | making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will… |
| [`doubt-driven-development`](skills/doubt-driven-development/SKILL.md) | challenging consequential technical decisions with evidence and bounded review |
| [`git-workflow`](skills/git-workflow/SKILL.md) | committing, branching, writing commit/PR messages, resolving conflicts, or structuring a change for review |
| [`incremental-implementation`](skills/incremental-implementation/SKILL.md) | implementing any feature or change that touches more than one file. you're about to write a large amount of code at once, or when a task feels too… |
| [`observability`](skills/observability/SKILL.md) | shipping production code, diagnosing runtime behavior, or making systems operable |
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | performance requirements exist, you suspect a regression, or profiling reveals a bottleneck that needs fixing |
| [`planning-and-task-breakdown`](skills/planning-and-task-breakdown/SKILL.md) | you have a spec or clear requirements and need to break work into implementable tasks. a task feels too large to start, when you need to estimate… |
| [`rest-api-contract`](skills/rest-api-contract/SKILL.md) | designing a new endpoint, aligning endpoints that have diverged, choosing a status code, shaping an error response, updating the OpenAPI spec, or… |
| [`security-hardening`](skills/security-hardening/SKILL.md) | reviewing code for vulnerabilities, handling auth/input/untrusted data, before shipping anything internet-facing, or when secrets/keys are involved |
| [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md) | preparing to deploy to production. you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a… |
| [`source-driven-development`](skills/source-driven-development/SKILL.md) | you want authoritative, source-cited code free from outdated patterns. building with any framework or library where correctness matters |
| [`spec-driven-development`](skills/spec-driven-development/SKILL.md) | starting a new project, feature, or significant change and no specification exists yet. requirements are unclear, ambiguous, or only exist as a… |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | implementing any logic, fixing any bug, or changing any behavior. you need to prove that code works, when a bug report arrives, or when you're… |

### `agent` — working with AI agents

Context, skills, and tool integration — the practice of directing agents well.

| Skill | Use it when |
|---|---|
| [`agent-handoff`](skills/agent-handoff/SKILL.md) | resuming another agent or teammate, preparing a handoff, or coordinating explicitly authorized parallel work |
| [`ai-tool-security`](skills/ai-tool-security/SKILL.md) | reviewing agent tool permissions, prompt injection boundaries, or outbound AI data |
| [`context-engineering`](skills/context-engineering/SKILL.md) | selecting and refreshing relevant context for the active task |
| [`context-privacy`](skills/context-privacy/SKILL.md) | deciding where multi-client context, team memory, local notes, and credentials belong |
| [`mcp-builder`](skills/mcp-builder/SKILL.md) | exposing external APIs/data/actions to agents |
| [`skill-creator`](skills/skill-creator/SKILL.md) | creating or upgrading reusable skills in the source library |
| [`skill-evaluation`](skills/skill-evaluation/SKILL.md) | checking skill routing, task outcomes, and behavior across versions |
| [`using-agent-skills`](skills/using-agent-skills/SKILL.md) | selecting the smallest useful set from the installed catalog |


### `web` — web and frontend

Browser-facing work: interface craft, the token system beneath it, layout that adapts to
its container, forms, schema-driven UI, page-load performance, and verification in a real
browser.

| Skill | Use it when |
|---|---|
| [`accessibility-audit`](skills/accessibility-audit/SKILL.md) | asked to check or fix accessibility, when a11y bugs or complaints arrive, before shipping a user-facing surface, or when an automated scan reports… |
| [`design-tokens`](skills/design-tokens/SKILL.md) | starting a UI with no declared design system, when hardcoded colours or pixel values are spreading, when adding dark mode or a second theme, or… |
| [`forms-and-validation`](skills/forms-and-validation/SKILL.md) | building or fixing any form, input, validation rule, or error display, when a submit can be fired twice, or when form errors are invisible to… |
| [`frontend-state`](skills/frontend-state/SKILL.md) | choosing between useState, context, a URL param, a query cache and a global store, when a component re-renders too much, when the same fact is… |
| [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | building or modifying user-facing interfaces, components, or stateful interactions |
| [`responsive-layout`](skills/responsive-layout/SKILL.md) | a component must work in more than one context, when a layout breaks at a width or at large text, when adding breakpoints, or when a design must… |
| [`uidl-runtime`](skills/uidl-runtime/SKILL.md) | creating or changing a UIDL document, the document schema, DataAdapter seam, $bind/$query/$expr/mutate behaviour, uidl-validate, or uidl-compile |
| [`web-development`](skills/web-development/SKILL.md) | the user wants to scaffold, design, or iterate on a website or web app with an AI agent, asks about vibe coding, AI-first IDEs (Cursor, Windsurf,… |
| [`web-perf`](skills/web-perf/SKILL.md) | asked to audit, profile, debug, or optimize page load performance, Lighthouse scores, or site speed |
| [`webapp-testing`](skills/webapp-testing/SKILL.md) | asked to verify a feature works in the browser, reproduce a UI bug, or add e2e coverage |

### `java` — Java and Quarkus

Concrete rules for a Java 21 / Quarkus / PostgreSQL stack.

| Skill | Use it when |
|---|---|
| [`bulk-reporting-export`](skills/bulk-reporting-export/SKILL.md) | an export is slow or runs out of memory, when building any endpoint in the reporting module, when a report exceeds a few thousand rows, or when… |
| [`java-code-standards`](skills/java-code-standards/SKILL.md) | writing a new Java class, reviewing a Java diff, cleaning up hard-to-read code, deciding on an exception shape or return type, or enforcing… |
| [`java-delivery`](skills/java-delivery/SKILL.md) | setting up or fixing a build, adding a CI stage, preparing a release, deploying to staging or production, writing a runbook, or planning a rollback |
| [`quarkus-observability`](skills/quarkus-observability/SKILL.md) | preparing a new service for production, adding metrics, diagnosing an issue that only appears in staging or production, designing alerts, or when… |
| [`quarkus-persistence`](skills/quarkus-persistence/SKILL.md) | creating or changing an entity, writing a migration, writing a query, fixing a slow request or N+1, deciding a transaction boundary, or designing… |
| [`quarkus-security`](skills/quarkus-security/SKILL.md) | touching login or sessions, adding an endpoint that needs a role, accepting user input or files, building dynamic sort/filter, reviewing a PR that… |
| [`quarkus-service`](skills/quarkus-service/SKILL.md) | adding a new endpoint, creating a new Quarkus module, untangling code that mixes layers, moving configuration to @ConfigMapping, or calling… |
| [`quarkus-testing`](skills/quarkus-testing/SKILL.md) | adding an endpoint or business rule, fixing a bug (failing test first), dealing with slow or flaky tests, setting up Testcontainers, or when… |

## Using a skill

An agent reads the `description` in the frontmatter first and loads the body only when the
task matches — progressive disclosure, so a large library costs little context.

```
skills/<name>/
├── SKILL.md            entry point: frontmatter + instructions
└── references/         loaded only when SKILL.md is not enough
```

**One shape, enforced.** `SKILL.md` is at most **100 lines**; the skills here sit at
40-80. It is a context budget rather than a style rule: the entry point is loaded in
full on every match, so depth kept there is paid for by every task that did not need
it. Anything conditional or worked-through belongs in `references/`, which an agent
opens only when it must. A skill that cannot state its process in 80 lines is usually
two skills, or one skill whose references have not been written yet.

Required frontmatter: `name` and `description`, plus this library's `metadata.pack`
(`core`, `agent`, `web`, or `java`). The description should say **when to use it**
and, where it helps, when *not* to — that sentence is what routing matches on.
`pack` is catalog grouping, stored under the spec's `metadata` map so a strict
[Agent Skills](https://agentskills.io/specification) consumer can load the skill.
The generated `index.json` still carries `pack` as a column so `ws skills sync`
can select packs without parsing every SKILL.md.

## Adding or changing a skill

1. Write or edit `skills/<name>/SKILL.md`.
2. Exercise representative requests and failure cases; label manual walkthroughs
   separately from actual model executions. See the
   [evaluation scenarios](skills/skill-evaluation/references/scenarios.md).
3. Run `./bin/reindex` and `python3 bin/validate.py`; update this catalog and count.
4. No personal, client, or company identifiers — CI fails the build on them.
5. Include the updated `index.json` when committing the reviewed change.

The `skill-creator` skill in this repository walks through writing a good one.

## Quality checks

Run these commands from this repository after a skill change:

```bash
./bin/reindex
python3 -B bin/validate.py
python3 -B -m unittest discover -s tests -v
```

The validator checks canonical metadata, name and description limits, known packs,
allowed spec fields, the 100-line entry-point ceiling, links and resource paths in
every reachable document, routes to skills the library does not ship, files that pose
as agent instructions for the surrounding project, bundled files nothing points at,
private-use characters left behind by another assistant, symlink escapes, nested
discovery leaks, and agreement between the source, index, and README catalog. The regression suite uses disposable catalogs; it needs no network,
credentials, or third-party packages.

Required metadata follows the reindex format: unquoted single-line `name`, a
plain single-line or folded (`>` / `>-`) `description`, and `metadata.pack` as a
block mapping. Optional spec fields (`license`, `compatibility`, `allowed-tools`,
extra string keys under `metadata`) are allowed in the same plain-text form.
The validator is not a general YAML parser; flow-style values are rejected.
Local links are checked in every `.md` and `.mdc` in a skill tree, outside fenced
examples, including inline Markdown links, reference definitions, and backtick
resource paths. A bare `references/x.md` resolves against the skill, not against the
document that names it. Remote links, Cursor's `mdc:` scheme, anchor existence, and
arbitrary CommonMark syntax are outside this check's coverage.

Behavioral evaluation is separate. Give an evaluator synthetic requests and the
minimum necessary artifacts, keep expected outcomes out of its input, and record
selected skills, actual tool actions, outputs, candidate hashes, and limitations.
Use a disposable fixture repository for Git tasks. A hypothetical response is
decision evidence, not a successful runtime security test. Re-run affected cases
after fixes and retain both original and replay results.

## Licence

MIT — see [LICENSE](LICENSE).
