#!/usr/bin/env bash
# Refuse to publish a private or client name.
#
# Two sources, deliberately separated:
#
#   PRIVATE_IDENTIFIERS   a repository secret holding the names that must never
#                         be published. A list of those names, written into a
#                         published file, is the leak it exists to prevent, so
#                         the pattern never enters the repository.
#   .github/public-identifiers   names that are public anyway: this repository,
#                         its documented sibling projects, and the account they
#                         live under. A portable library is expected to name
#                         them; a stale secret that still contains them must not
#                         redden every build. Never add a private or client name
#                         to that file.
#
# Only file names are printed. A matched line, or the matched text itself, would
# put the name into a public build log, where secret masking does not reach it.
#
# Usage: bin/identifier-gate.sh [path ...]   (default: skills)
set -uo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
allowlist="${IDENTIFIER_ALLOWLIST:-$repo_root/.github/public-identifiers}"
pattern="${PRIVATE_IDENTIFIERS:-}"

targets=("$@")
if [ "${#targets[@]}" -eq 0 ]; then
  targets=("$repo_root/skills")
fi

fail=0

if [ -z "$pattern" ]; then
  echo "::warning::PRIVATE_IDENTIFIERS is unset - the name check did not run"
elif [ ! -r "$allowlist" ]; then
  echo "::error::the public identifier list is unreadable - the name check cannot run"
  fail=1
else
  while IFS= read -r file; do
    [ -n "$file" ] || continue
    while IFS= read -r token; do
      [ -n "$token" ] || continue
      if ! grep -qxFi -- "$token" "$allowlist"; then
        echo "::error::a personal or client name reached a published file: $file"
        fail=1
        break
      fi
    done < <(grep -ioE -e "$pattern" "$file" | tr '[:upper:]' '[:lower:]' | sort -u)
  done < <(grep -rilE --include='*.md' -e "$pattern" "${targets[@]}")
fi

# Case-sensitive on purpose: `/api/users/` in an example must not match `/Users/`,
# or the check fails on nothing.
if home_paths="$(grep -rlE '/(Users|home)/[A-Za-z][A-Za-z0-9._-]*' --include='*.md' "${targets[@]}")"; then
  while IFS= read -r file; do
    [ -n "$file" ] || continue
    echo "::error::a home-directory path reached a published file: $file"
    fail=1
  done <<<"$home_paths"
fi

exit $fail