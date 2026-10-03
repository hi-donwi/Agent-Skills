---
name: skill-evaluation
description: >-
  Evaluate whether a skill routes correctly and improves task outcomes. Use when adding or revising skills, investigating misfires, or comparing skill versions.
metadata:
  pack: agent
  keywords: skill evaluation, skill benchmark, harness, routing accuracy, eval, test skill
---

# Skill Evaluation

## Overview
Separate catalog validity from demonstrated behavior. A well-formed skill can still
misroute tasks, stall work, or perform unauthorized actions.

## When to use
- A skill is new, substantially revised, or repeatedly produces poor results.
- Comparing a candidate skill with the previous version.

## Process
1. Define observable success before running the candidate: correct artifact,
   necessary checks, permitted tool actions, and situations that should not trigger it.
   Identify the target skill and revision first. If they are unspecified, ask for
   that missing target; do not expand a draft evaluation into a whole-catalog review.
2. Select representative fixtures: a direct request, a paraphrase, a nearby
   non-match, and a failure or ambiguity case. Add an adversarial case when the
   skill handles untrusted input or external actions. Use synthetic data.
3. Validate structure, resource paths, naming, and catalog entries separately.
   In this library run ./bin/reindex and python3 bin/validate.py.
   For closed evaluator inputs, prefer exact file reads. Scope any necessary search
   to an allowed directory and filename filter; a file-shaped search path may not
   restrict the tool. Unexpected material is an input-boundary incident: record it
   and repeat affected evaluations from a fresh context before claiming isolation.
4. Exercise the fixtures using the available authorized evaluation mechanism.
   Give an evaluator only the request, candidate skill, and necessary artifacts;
   keep expected outcomes in a separate scoring record. Do not spawn agents,
   call another provider, or send private fixtures without authorization.
5. Record the skill revision or content hash, model/runtime when used, fixture,
   observed actions, artifact, and pass/fail/not-run result. A manual walkthrough
   is useful but must be labeled as such, not called an independent model test.
6. Compare against the previous version on the same fixtures when claiming an
   improvement. Repeat only cases affected by changes or observed variability.
   Fix the narrow cause of a failure; avoid growing universal rules from one example.
   Distinguish artifact defects from overspecified scoring. If an oracle contradicts
   the supplied contract, retain the old result, version the correction, and score
   both candidates again; changed-oracle scores are not a skill improvement claim.
7. Report structural checks, behavioral outcomes, and remaining uncertainty
   separately. Unrun cases never count as passes.

## Red flags
- Scoring only the final answer while ignoring unsafe tool calls.
- Tests that merely assert the skill repeats its own wording.
- Counting another reviewer agreeing as task execution evidence.
- Changing fixtures between versions and claiming a measured improvement.

## Verification
- Expected outcomes describe decisions and artifacts, not exact prose.
- Negative routing and failure handling have evidence or explicit not-run status.
- Claims of improvement match the evaluation method actually performed.

## References
- `references/scenarios.md` — synthetic routing and failure fixtures for this
  library's agent workflows; load when reviewing those skills or extending coverage.
- `references/business-behavior-protocol.md` - held-out artifact execution and
  decision evaluation for critical business workflows, with explicit evidence limits.
