#!/bin/sh
# Run the behaviour evals in evals/: known cases, each with its input and the
# call the skill should make. Each run is a child Claude session on your own
# account, so the suite costs real tokens. Extra arguments go to
# `claude plugin eval`, for example `--case triage-*`, `--runs 1` or
# `--ablation none` (skip the arm without the plugin).
set -eu

root=$(cd "$(dirname "$0")/.." && pwd)
# A run may read only its own workspace, so grant Read on the skills folder:
# repo-review's mode files (triage.md, portfolio.md, quick.md) are read on demand.
exec claude plugin eval "$root" --no-publish --trust-plugin \
  --allow-tools "Read(/$root/skills/**)" "$@"
