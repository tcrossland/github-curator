# Working on github-curator

These notes are for changing the plugin. They stay out of the zip that `scripts/package.sh` builds, so the [README](../README.md) that ships with the plugin links nothing here.

- [`design.md`](design.md): why the skills work the way they do. Read it before changing a rule.
- [`github-facts.md`](github-facts.md): the GitHub and Claude behaviours the skills rely on, each with its source and the date it was checked.
- [`backlog.md`](backlog.md): what to build next.

The tests run the skills' code as it stands (the quote checker, the timing script, the reply counts and `stargazers`' repo listings), check that every relative link in a shipped file points to a file the zip holds, and render the scorecard template's three modes:

```sh
python3 -m unittest discover tests
node --test tests/*.test.mjs
```
