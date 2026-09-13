# Agent Skills

Portable, agent-agnostic **skills** in the open Agent Skills format: a `SKILL.md` entry
point with YAML frontmatter and concise instructions, plus a `references/` folder an agent
loads only when it needs the detail.

42 skills, grouped into packs. Nothing here is specific to one company,
client, or codebase.

## Why a separate repository

A skill is knowledge about *how to do a kind of work*. It outlives any one project and it
is worth sharing between them. Keeping skills in their own repository means one version,
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
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | performance requirements exist, when you suspect performance regressions, or when Core Web Vitals or load times need improvement. profiling… |
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



| Skill | Use it when |
|---|---|
| [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | building or modifying user-facing interfaces, components, layouts, or stateful interactions |
| [`web-development`](skills/web-development/SKILL.md) | Build high-quality, modern websites with AI coding agents using the "vibe coding" workflow — including premium marketing sites, SaaS UIs, and… |
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

Required frontmatter: `name`, `pack`, `description`. The description should say **when to
use it** and, where it helps, when *not* to — that sentence is what routing matches on.
The required top-level `pack` field is a library extension. Strict consumers of the
[Agent Skills specification](https://agentskills.io/specification) may need an adapter;
the library and workspace currently depend on this field.

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
local entrypoint links, resource paths, symlink escapes, nested discovery leaks,
and agreement between the source, index, and README catalog. The regression suite
uses disposable catalogs; it needs no network, credentials, or third-party packages.

Required metadata follows the existing reindex format: unquoted single-line name
and pack, and a plain single-line or folded (`>` / `>-`) description. The validator
is not a general YAML parser; optional metadata needs separate YAML validation.
Local links are checked in SKILL.md outside fenced examples, including inline
Markdown links, reference definitions, and backtick resource paths. Remote links,
anchor existence, supporting-document links, and arbitrary CommonMark syntax are
outside this check's coverage.

Behavioral evaluation is separate. Give an evaluator synthetic requests and the
minimum necessary artifacts, keep expected outcomes out of its input, and record
selected skills, actual tool actions, outputs, candidate hashes, and limitations.
Use a disposable fixture repository for Git tasks. A hypothetical response is
decision evidence, not a successful runtime security test. Re-run affected cases
after fixes and retain both original and replay results.

## Licence

MIT — see [LICENSE](LICENSE).
