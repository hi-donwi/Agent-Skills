---
name: dependency-audit
pack: core
description: >-
  Audit, upgrade, or rationalize third-party dependencies for security,
  licensing, maintenance, bundle/runtime impact, and supply-chain risk. Use when
  adding dependencies, fixing audit findings, upgrading packages, or reducing
  dependency surface. Do not use for application logic bugs unrelated to external
  packages.
---

# Dependency Audit

Dependencies are code you ship and operate. Add and upgrade them deliberately.

## When to Use

- Adding a new production dependency.
- Handling `npm audit`, `pnpm audit`, `cargo audit`, Dependabot, Snyk, OSV, or
  GitHub security alerts.
- Upgrading packages, SDKs, lockfiles, or transitive dependency chains.
- Reducing bundle size or supply-chain exposure.

## Process

1. **Classify the dependency.** Runtime, dev-only, optional, peer, transitive,
   build tool, SDK, or platform adapter.
2. **Check necessity.** Prefer standard library or existing project packages when
   they satisfy the need.
3. **Assess risk.** Security advisory, license, maintenance activity, download
   trust signals, install scripts, native code, network behavior, and package
   ownership.
4. **Plan upgrade path.** Read changelog/release notes for breaking changes and
   migration steps; use `source-driven-development` for current docs.
5. **Apply minimally.** Update only required packages/lockfiles unless a broader
   upgrade is intentional.
6. **Verify.** Run relevant tests, build, typecheck, audit, and bundle/perf
   checks for user-facing packages.

## Red Flags

- Adding a dependency for a trivial helper.
- Ignoring lockfile changes.
- Auto-upgrading major versions without reading release notes.
- Treating dev dependencies as harmless in build/deploy environments.
- Suppressing audit alerts without documenting exploitability and mitigation.

## Verification

- Reason for adding/upgrading/removing is documented.
- Security/license/maintenance risk is acceptable or bounded.
- Tests/build/audit checks relevant to the package passed.
