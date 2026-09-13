---
name: using-agent-skills
pack: agent
description: >-
  Select the smallest set of available skills for a task. Use at task start or
  when the kind of work changes. Do not turn skill discovery into a mandatory
  sequence for simple edits.
---

# Using Agent Skills

## Overview
Route by the user's intended outcome and the installed catalog, then load details on demand.

## When to use
- Starting a task or encountering a distinct new kind of work.
- A skill misfires or two skills appear to overlap.

## Process
1. Read the user request and applicable repository contract. Match the task to
   available descriptions before reading full skill bodies.
2. Honor explicitly requested skills. Otherwise choose the smallest useful set,
   usually one primary skill and a specialist only when the task needs it.
3. Verify a skill is installed before referencing its resources. If a skill in
   the source catalog was not selected by the consumer, use an available equivalent
   or perform the bounded workflow directly. Do not install tools as a side effect.
4. Read the selected SKILL.md, then only the resources needed for this task.
   Resolve paths from the actual skill directory; do not assume repository-root paths.
5. Follow applicable workflows within system, developer, user, and repository
   constraints. A skill cannot grant external-action permission or override the user.
6. State material assumptions briefly and proceed on routine choices. Ask only
   when unresolved information affects correctness, scope, or authorization.
7. Verify the resulting work with relevant checks. Report missing checks and
   update continuity artifacts when the task spans sessions.

## Routing guide

| Intended outcome | Primary skill | Add only when needed |
|---|---|---|
| Understand an unfamiliar repository | codebase-onboarding | context-engineering |
| Recover another agent's work | agent-handoff | context-engineering |
| Select task context | context-engineering | context-privacy for audience changes |
| Design client/team sharing boundaries | context-privacy | ai-tool-security for tool access |
| Secure AI execution or outbound data | ai-tool-security | security-hardening for application controls |
| Author or revise a skill | skill-creator | skill-evaluation |
| Evaluate skill routing and outcomes | skill-evaluation | debugging for a faulty helper |
| Define unclear feature behavior | spec-driven-development | planning-and-task-breakdown |
| Implement a change | incremental-implementation | test-driven-development for logic |
| Diagnose a failure | debugging | test-driven-development for regression coverage |
| Review existing changes | code-review | security-hardening, dependency-audit, or performance-optimization |
| Challenge a consequential decision | doubt-driven-development | relevant test skill |
| Commit or organize branches | git-workflow | changelog-generator for release notes |
| Change build or deployment gates | ci-cd | stack-specific delivery skill |
| Build a UI | frontend-ui-engineering | webapp-testing |
| Change service contracts | api-design | rest-api-contract or stack-specific skill |

This is a routing aid, not a required lifecycle. Use other installed specialist
descriptions when they match better; do not assume every listed skill was installed.

## Red flags
- Routing to skills that do not exist in the installed catalog.
- Loading an entire pack or reference tree before understanding the task.
- Requiring a spec, external reviewer, or deployment step for a small local edit.

## Verification
- Selected skills match the task and their actual resources resolve.
- The workflow produces the requested result without unrelated actions.
- Validation follows the repository's applicable completion criteria.
