# Contributing

github-curator is a personal project with one author. It doesn't take outside contributions yet. If you've been given access, this is how changes are made. The plugin's own `repo-review` reads this file for a repo's house style and for how its changes land, so the rules below are also the ones its fix prompts follow here.

## Reporting a problem

Open an issue that says:
- the plugin version, from `.claude-plugin/plugin.json` or the top of [CHANGELOG.md](CHANGELOG.md);
- where it ran: claude.ai, or Claude Code on your own computer. A claude.ai session reaches much less of GitHub, so the same command can work in one and be refused in the other;
- the command you gave, and what came back, with any error quoted word for word.

Leave out other people's details, and the names of private repos, unless they're needed to show the problem.

A security problem goes to private vulnerability reporting instead, not an issue: [SECURITY.md](SECURITY.md) says how.

## Before changing a rule

- Read [docs/design.md](docs/design.md). It says why each rule is the way it is, so a change doesn't quietly undo one.
- The skills only recommend. A change mustn't make any of the skills archive, delete, pin or unpin a repo, change its visibility, close an issue or pull request, or contact anyone.
- A behaviour of GitHub or Claude that a skill relies on goes in [docs/github-facts.md](docs/github-facts.md), with its source and the date it was checked. Mark anything not checked **unverified**. Check the claude.ai section before relying on something that works in a local shell.
- Keep anything about a specific person or private repo out of the files that ship (the manifest, `skills/`, the README and the changelog).

## Making a change

1. Branch from `main`, one change per branch.
2. Make the change. `SKILL.md` loads in full on every run, so it holds instructions only; the reasons go in `docs/design.md`.
3. Try it with `no-publish`, so the live scorecards aren't republished.
4. If it changes how a skill reaches GitHub, check it on claude.ai as well as in Claude Code.
5. Run the tests:

   ```sh
   python3 -m unittest discover tests
   node --test tests/*.test.mjs
   ```

   The Python tests run code blocks from `SKILL.md` as they stand, so a change to a block is tested as written.
6. If a user of the plugin would notice the change, add an entry under `## Unreleased` in `CHANGELOG.md` in the same commit, saying what changed from their side. Leave `version` alone: it's raised only when a release is cut.
7. Update [docs/backlog.md](docs/backlog.md) in the same commit when the change advances or finishes an item.

## How changes land

Commit on your branch. The owner reviews it and fast-forwards `main` to it, so keep the branch on top of `main` and don't add merge commits. Nothing is pushed without the owner's go-ahead.

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/): a `type(scope): subject` line in the imperative ("build: add a changelog and ship it in the zip", "fix(stargazers): tell a hidden stargazer list apart from a private repo"), a blank line, then a wrapped body that says what changed and why. The types are `feat`, `fix`, `docs`, `build`, `test`, `refactor` and `chore`; scopes name a skill (`repo-review`, `stargazers`) or a document (`backlog`, `facts` for `docs/github-facts.md`).

## Writing

British English, no em-dashes, and plain words. Say what something does rather than dressing it up. These rules cover this repo, the skills' own text included. What the skills write for another repo, such as a suggested README line or a fix prompt, follows that repo's house style instead.
