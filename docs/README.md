# Working on github-curator

These notes are for changing the plugin. They stay out of the zip that `scripts/package.sh` builds, so the [README](../README.md) that ships with the plugin links nothing here.

- [`design.md`](design.md): why the skills work the way they do. Read it before changing a rule.
- [`github-facts.md`](github-facts.md): the GitHub and Claude behaviours the skills rely on, each with its source and the date it was checked.
- [`backlog.md`](backlog.md): what to build next.

The tests run the skills' code as it stands (the quote checker, the timing script, the reply counts, `stargazers`' repo listings, and `contributions`' searches and grouping script), check that every relative link in a shipped file points to a file the zip holds, and render the scorecard template's three modes:

```sh
python3 -m unittest discover tests
node --test tests/*.test.mjs
```

The behaviour evals in `evals/` check the skills' calls rather than their code: each case gives one repo, offline, and the call the skill should make (`design.md` says why). Each run is a child Claude session on the CLI's own sign-in, so run `claude auth login` first if `claude auth status` says you aren't signed in. They cost real tokens (the full suite, 30 runs with and without the plugin, came to about $8 and six minutes on 2026-11-20), so run them when a change touches a rule:

```sh
scripts/evals.sh
```

Extra arguments go to `claude plugin eval`: `--case triage-*` for some cases, `--runs 1` for a quick pass, `--ablation none` to skip the runs without the plugin. Results go to `evals/results/`, which git ignores.
