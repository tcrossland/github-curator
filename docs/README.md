# Working on github-curator

These notes are for changing the plugin. They stay out of the zip that `scripts/package.sh` builds, so the [README](../README.md) that ships with the plugin links nothing here.

- [`design.md`](design.md): why the skills work the way they do. Read it before changing a rule.
- [`github-facts.md`](github-facts.md): the GitHub and Claude behaviours the skills rely on, each with its source and the date it was checked.
- [`backlog.md`](backlog.md): what to build next.

## Building and releasing

The plugin is installed by uploading a zip of it to claude.ai (Plugins in the left sidebar > Add > Upload plugin), so edits here don't reach Claude until the plugin is uploaded again. Changes collect under Unreleased in [CHANGELOG.md](../CHANGELOG.md); to release them, give that section the new version and date, raise `version` in `.claude-plugin/plugin.json` to match, then build the zip and upload it:

```sh
scripts/package.sh
```

It validates the manifest when the `claude` CLI is installed, and writes `dist/github-curator-VERSION.zip`, holding only the manifest, the skills, the README, the changelog and the licence.

To try changes before a release, build a test zip with a pre-release version, which goes only into the zip's manifest:

```sh
scripts/package.sh --dev 0.3.1-dev.1
```

Typing `/reload-plugins` in a Claude Code session applies plugin updates, but whether it picks up an upload to claude.ai isn't tested yet.

## Tests

The tests run the skills' code as it stands (the quote checker and quick mode's quote check, the timing script, the reply counts, the review's Contributors and Waiting on you, its secrets scan and check of GitHub's secret scanning, the profile review's commands, `stargazers`' repo listings, `forks`' listing and git commands, `contributions`' searches and grouping script, and `traffic`'s repo listings and snapshot script), check that every relative link in a shipped file points to a file the zip holds, and render the scorecard template's five modes:

```sh
python3 -m unittest discover tests
node --test tests/*.test.mjs
```

They also run on GitHub on every push and pull request, on Ubuntu and macOS, from `.github/workflows/tests.yml`. macOS is there for the zsh tests, which skip wherever zsh isn't installed. The test of the real betterleaks skips unless the runner has it, since the workflow installs nothing.

The secrets scan's tests use a stand-in betterleaks, and one test also runs the real one over a repo with fake keys planted in its history. It runs when betterleaks is on `PATH`, or with `BETTERLEAKS` naming one or more binaries separated by `:`, so both major versions can be checked at once. The tests of its fetch on claude.ai use a stand-in `curl` and `uname` serving a made-up release.

The behaviour evals in `evals/` check the skills' calls rather than their code: each case gives one repo, offline, and the call the skill should make (`design.md` says why). Each run is a child Claude session on the CLI's own sign-in, so run `claude auth login` first if `claude auth status` says you aren't signed in. They cost real tokens (the full suite, 30 runs with and without the plugin, came to about $8 and six minutes on 2026-11-20), so a change to a rule runs only the cases that guard it, once each, and before a release, the cases whose rules changed since the last one run once each (`CLAUDE.md` has the rule):

```sh
scripts/evals.sh --case other-people --runs 1 --ablation none
scripts/evals.sh
```

Extra arguments go to `claude plugin eval`: `--case` takes one glob, such as `triage-*`; `--runs 1` runs each case once (leave it out for a case tagged `repeat`); `--ablation none` skips the runs without the plugin. Results go to `evals/results/`, which git ignores.
