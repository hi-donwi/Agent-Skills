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

## Overview
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

## Audit evidence and exceptions
- Inventory manifests, lockfiles, build toolchains, CI actions, and executable
  skill resources. Record what the chosen scanner covers and what it omits.
- Use the repository's pinned gate when available; inspect its configuration and
  installed CLI help instead of inventing flags. Record revision, command, scanner
  version, database freshness when exposed, exit status, and sanitized report location.
- Separate a complete scan with no findings from findings, scanner failure, and
  incomplete coverage. A timeout or unreachable advisory database is not a pass.
- Confirm advisory details and fixed versions from primary sources at audit time.
  Distinguish affected package presence from demonstrated reachability or exploitation.
  Development dependencies still execute in build and CI environments.
- Scope exceptions to the advisory and affected artifact with a reason, responsible
  owner, expiry date, and compensating control. Apply the gate's supported schema;
  keep additional approval records in private context. Do not hide scanner failures.
- Verify artifact checksums and immutable references when upgrading executable
  tooling. A matching checksum proves integrity against that checksum source, not trust.

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
- Scope, failures, unscanned components, and expiring exceptions are explicit.
