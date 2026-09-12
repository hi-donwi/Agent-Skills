#!/usr/bin/env node
/**
 * check-project.js — verify a web project against the web-development skill's
 * coding standards (see ../docs/coding-standards.md).
 *
 * Usage:  node check-project.js [projectDir]   (defaults to current directory)
 * Exit:   0 if no failures, 1 if any rule fails. Warnings never fail the build.
 *
 * Zero dependencies — Node built-ins only.
 */

const fs = require("fs");
const path = require("path");

const root = path.resolve(process.argv[2] || ".");
const results = [];
const add = (level, msg) => results.push({ level, msg });

function readJson(file) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
  } catch {
    return null;
  }
}

function exists(rel) {
  return fs.existsSync(path.join(root, rel));
}

// --- package.json: deps + quality-gate scripts ---------------------------------
const pkg = readJson("package.json");
if (!pkg) {
  add("fail", "package.json not found or unreadable.");
} else {
  const deps = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
  if (!deps.next) add("warn", "`next` not in dependencies (skill defaults to Next.js App Router).");
  if (!deps.typescript) add("fail", "`typescript` not installed (strict TS is required).");
  if (!deps.tailwindcss) add("warn", "`tailwindcss` not installed (skill default for styling).");

  const scripts = pkg.scripts || {};
  for (const gate of ["lint", "test"]) {
    if (!scripts[gate]) add("fail", `Missing quality gate: "${gate}" script in package.json.`);
  }
  if (!scripts["test:e2e"]) add("warn", 'No "test:e2e" script (Playwright e2e recommended).');
  if (!scripts.lhci) add("warn", 'No "lhci" script (Lighthouse CI recommended for perf budgets).');
}

// --- tsconfig: strict mode ------------------------------------------------------
const tsconfig = readJson("tsconfig.json");
if (!tsconfig) {
  add("fail", "tsconfig.json not found.");
} else if (!tsconfig.compilerOptions || tsconfig.compilerOptions.strict !== true) {
  add("fail", 'tsconfig.json must set compilerOptions.strict = true.');
}

// --- structure: 3D code is isolated --------------------------------------------
if (exists("components") && !exists("components/scene") && exists("public")) {
  add("info", "Tip: keep any WebGL/3D code under components/scene/ (none found yet).");
}

// --- report ---------------------------------------------------------------------
const icon = { fail: "✗", warn: "!", info: "·" };
const order = { fail: 0, warn: 1, info: 2 };
results.sort((a, b) => order[a.level] - order[b.level]);

console.log(`\ncheck-project: ${root}\n`);
if (results.length === 0) console.log("  ✓ all checks passed");
for (const r of results) console.log(`  ${icon[r.level]} [${r.level}] ${r.msg}`);

const failures = results.filter((r) => r.level === "fail").length;
console.log(`\n${failures} failure(s).\n`);
process.exit(failures > 0 ? 1 : 0);
