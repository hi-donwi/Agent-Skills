# Agent Skills

Portable, agent-agnostic **skills** in the open Agent Skills format: a `SKILL.md` entry
point with YAML frontmatter and concise instructions, plus a `references/` folder an agent
loads only when it needs the detail.

65 skills, grouped into packs. Nothing here names a company, a client, or a private
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

Language-agnostic engineering practice and business application workflows. How to
plan, build, review, debug, ship, and preserve SaaS, ERP, and membership invariants.

| Skill | Use it when |
|---|---|
| [`api-design`](skills/api-design/SKILL.md) | adding or changing an HTTP/RPC endpoint, a public library interface, or a service contract, or when reviewing an interface for consistency |
| [`audit-logging`](skills/audit-logging/SKILL.md) | recording attributable business mutations with durable audit history, redaction, and retention |
| [`background-jobs`](skills/background-jobs/SKILL.md) | building durable workers, outboxes, scheduling, retries, leases, and crash recovery |
| [`changelog-generator`](skills/changelog-generator/SKILL.md) | Generate user-facing changelogs, release notes, upgrade notes, and internal change summaries from git history, PRs, issues, commits, or diff… |
| [`ci-cd`](skills/ci-cd/SKILL.md) | adding GitHub Actions (or similar), defining quality gates, fixing a failing pipeline, or designing a release/rollout |
| [`code-review`](skills/code-review/SKILL.md) | asked to review code, before merging a change, or to self-review a diff |
| [`code-simplification`](skills/code-simplification/SKILL.md) | refactoring code for clarity without changing behavior. code works but is harder to read, maintain, or extend than it should be. reviewing code… |
| [`codebase-onboarding`](skills/codebase-onboarding/SKILL.md) | starting work in an unknown or large codebase, before major refactors, or when asked to explain how a project works |
| [`data-import-export`](skills/data-import-export/SKILL.md) | exchanging typed data with staging, dry runs, mapping, row errors, resumability, and reconciliation |
| [`debugging`](skills/debugging/SKILL.md) | facing a bug, stack trace, failing test, crash, or unexpected behavior, or when a fix attempt did not work |
| [`dependency-audit`](skills/dependency-audit/SKILL.md) | adding dependencies, fixing audit findings, upgrading packages, or reducing dependency surface |
| [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) | removing old systems, APIs, or features. migrating users from one implementation to another. deciding whether to maintain or sunset existing code |
| [`documentation-and-adrs`](skills/documentation-and-adrs/SKILL.md) | making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will… |
| [`doubt-driven-development`](skills/doubt-driven-development/SKILL.md) | challenging consequential technical decisions with evidence and bounded review |
| [`erp-accounting`](skills/erp-accounting/SKILL.md) | posting balanced journals, locking fiscal periods, reversing entries, and reconciling open items |
| [`erp-domain-design`](skills/erp-domain-design/SKILL.md) | defining ERP modules, master-data ownership, company boundaries, and business document lifecycles |
| [`erp-inventory`](skills/erp-inventory/SKILL.md) | preserving stock movements, reservations, warehouse transfers, lots/serials, and valuation handoffs |
| [`erp-procurement`](skills/erp-procurement/SKILL.md) | building requisitions, purchase orders, receiving, supplier invoices, and cumulative three-way matching |
| [`erp-sales`](skills/erp-sales/SKILL.md) | implementing quote-to-cash orders, fulfillment, invoicing, credit controls, returns, and credit notes |
| [`feature-flags`](skills/feature-flags/SKILL.md) | managing deterministic exposure, release toggles, kill switches, and flag retirement |
| [`git-workflow`](skills/git-workflow/SKILL.md) | committing, branching, writing commit/PR messages, resolving conflicts, or structuring a change for review |
| [`identity-access-management`](skills/identity-access-management/SKILL.md) | designing tenant-scoped permissions, SSO/MFA, directory provisioning, and access revocation |
| [`incremental-implementation`](skills/incremental-implementation/SKILL.md) | implementing any feature or change that touches more than one file. you're about to write a large amount of code at once, or when a task feels too… |
| [`membership-management`](skills/membership-management/SKILL.md) | handling invitations, eligibility, renewals, expiry, benefits, suspension, and ownership transfer |
| [`observability`](skills/observability/SKILL.md) | shipping production code, diagnosing runtime behavior, or making systems operable |
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | performance requirements exist, you suspect a regression, or profiling reveals a bottleneck that needs fixing |
| [`planning-and-task-breakdown`](skills/planning-and-task-breakdown/SKILL.md) | you have a spec or clear requirements and need to break work into implementable tasks. a task feels too large to start, when you need to estimate… |
| [`product-analytics`](skills/product-analytics/SKILL.md) | defining privacy-aware behavioral events, activation funnels, retention cohorts, and experiment metrics |
| [`rest-api-contract`](skills/rest-api-contract/SKILL.md) | designing a new endpoint, aligning endpoints that have diverged, choosing a status code, shaping an error response, updating the OpenAPI spec, or… |
| [`saas-billing`](skills/saas-billing/SKILL.md) | implementing subscriptions, payment reconciliation, pricing, atomic metering, and paid entitlements |
| [`saas-multitenancy`](skills/saas-multitenancy/SKILL.md) | enforcing trusted tenant scope, row-level security, storage isolation, and noisy-neighbor controls |
| [`saas-onboarding`](skills/saas-onboarding/SKILL.md) | provisioning, activating, suspending, recovering, exporting, or retiring tenant organizations |
| [`security-hardening`](skills/security-hardening/SKILL.md) | reviewing code for vulnerabilities, handling auth/input/untrusted data, before shipping anything internet-facing, or when secrets/keys are involved |
| [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md) | preparing to deploy to production. you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a… |
| [`source-driven-development`](skills/source-driven-development/SKILL.md) | you want authoritative, source-cited code free from outdated patterns. building with any framework or library where correctness matters |
| [`spec-driven-development`](skills/spec-driven-development/SKILL.md) | starting a new project, feature, or significant change and no specification exists yet. requirements are unclear, ambiguous, or only exist as a… |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | implementing any logic, fixing any bug, or changing any behavior. you need to prove that code works, when a bug report arrives, or when you're… |
| [`webhook-integrations`](skills/webhook-integrations/SKILL.md) | authenticating partner events and delivering signed webhooks with safe endpoints, retries, and replay |
| [`workflow-approvals`](skills/workflow-approvals/SKILL.md) | authorizing document revisions with maker-checker, delegation, quorum, and atomic transitions |

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

## Business application routing

Business workflows stay in `core`; no new pack or consumer configuration is required.
Choose by the invariant being changed, not simply because an application is SaaS or ERP.

| Responsibility | Primary skill | Boundary |
|---|---|---|
| Customer infrastructure isolation | `saas-multitenancy` | Tenant scope is not legal-entity scope or membership eligibility |
| Organization provisioning and retirement | `saas-onboarding` | Separate from repository orientation and member renewals |
| Identity and action permissions | `identity-access-management` | Authentication does not imply active membership or paid access |
| Membership eligibility and benefits | `membership-management` | Payment processing remains in `saas-billing` |
| Commercial capability and usage | `saas-billing` | Paid entitlement does not replace authorization or release configuration |
| Exposure and product measurement | `feature-flags`, `product-analytics` | Flags are not access policy; analytics is not an audit ledger |
| ERP ownership and company boundaries | `erp-domain-design` | Companies and branches are distinct from SaaS tenants |
| Financial, physical, purchasing, and sales facts | `erp-accounting`, `erp-inventory`, `erp-procurement`, `erp-sales` | Preserve independent document states and source links |
| Revision-specific human decisions | `workflow-approvals` | Current actor eligibility is rechecked under a versioned policy |
| Durable effects, integrations, evidence, and exchange | `background-jobs`, `webhook-integrations`, `audit-logging`, `data-import-export` | Retries, transport acceptance, and business completion are distinct |

Detailed tax, payroll, manufacturing, and industry rules require an approved domain
contract. These portable workflows do not supply jurisdiction-specific professional advice.

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
python3 -B bin/harness.py benchmark
python3 -B bin/harness.py budget
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

`tests/scenarios.json` includes direct, paraphrased, neighboring-task, and failure
requests for the business workflows. The regression suite requires their expected
skill in Top-3 and primary routes for direct, paraphrased, and boundary requests.
Failure-case `expected_decision` fields are behavioral rubrics, not executed security
assertions. The lexical benchmark and approximate token budgets do not prove model
execution, database isolation, provider correctness, or production compliance.

For held-out code execution, decision-only cases, input-boundary incidents, and oracle
corrections, use the [business behavior evaluation protocol](skills/skill-evaluation/references/business-behavior-protocol.md).

## Licence

MIT — see [LICENSE](LICENSE).
