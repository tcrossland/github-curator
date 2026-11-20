# github-curator

A Claude plugin for keeping a public GitHub portfolio in shape. It holds three skills:

- [`repo-review`](skills/repo-review/SKILL.md): recommends what to do with a repo (keep, publish, archive, make private or delete), whether to feature it among the profile's pinned repos, and the work worth doing first; finds similar repos; checks it, or a README draft, against seven questions; and publishes a scorecard as an artifact, with a fix prompt for Claude Code. `repo-review triage` makes a quick first pass over all of an account's repos from the API, settles the clear deletes and names the repos worth a full review; `repo-review overview` reviews several repos and ranks them. `triage org:NAME` triages an organisation's repos instead, and `no-publish` in any mode saves the page as a file rather than publishing it.

  The seven questions, most important first, each marked pass, fail or flagged:
  - **Hook**: would someone outside the niche understand what it is, why it's interesting and what it found?
  - **Findable**: is it public, with a description and topics in the words people search for?
  - **Facts**: does every result, status, version, command, link and tag match its source?
  - **Defensible**: does each strong claim point to the test, report or file that proves it?
  - **Context**: are the field's terms defined or linked where they first appear?
  - **Way in**: can a visitor run it, reuse part of it or join in, under a licence that lets them?
  - **Tone**: does it read as finished work that shows the author's judgement, rather than internal notes?
- [`stargazers`](skills/stargazers/SKILL.md): lists who starred a repo and when, and picks out the stargazers whose own work is in the same field. With no repo given it covers every public repo of yours that has stars; `since:YYYY-MM-DD` keeps only recent stars, and `all` reads every stargazer, not only the 30 most recent. GitHub lists stargazers only to a repo's owner, so it works on your own repos. The repo review runs its Steps 1 to 3 for the scorecard's Outcomes panel.
- [`contributions`](skills/contributions/SKILL.md): lists your merged pull requests to repos you don't own, in three groups: your own organisations' (counted), your employers' (listed apart, once you name them with `employers:OWNER`) and other people's projects, one row per repo with its stars, the dates and what you did. Pull requests to private repos are counted, never named.

All three read GitHub through `gh api`. Before publishing a private repo, the review also scans its full history for keys and tokens with [betterleaks](https://github.com/betterleaks/betterleaks), if it's installed (`brew install betterleaks`); it only detects, and never sends a secret anywhere. None follows, stars, comments on or messages anyone, and none archives, deletes or changes the visibility of a repo: the review only recommends.

## Install and update

The plugin is installed by uploading a zip of it to claude.ai (Plugins in the left sidebar > Add > Upload plugin). Edits here don't reach Claude until the plugin is uploaded again. Changes collect under Unreleased in [CHANGELOG.md](CHANGELOG.md); to release them, give that section the new version and date, raise `version` in `.claude-plugin/plugin.json` to match, then build the zip and upload it:

```sh
scripts/package.sh
```

It validates the manifest and writes `dist/github-curator-VERSION.zip`, holding only the manifest, the skills, this README, the changelog and the licence.

A Claude Code session that was already open keeps the version it started with, even after the new one reaches its disk: a skill invoked again returns the text it loaded first. Start a new session to use the new version. Typing `/reload-plugins` in the session applies plugin updates, but whether it picks up an upload to claude.ai isn't tested yet.

The skills run as `/github-curator:repo-review`, `/github-curator:stargazers` and `/github-curator:contributions`.

## Working on it

Notes for changing the plugin, and how to run its tests, are in `docs/README.md` in its repository. They don't ship in the zip.

## Licence

Apache License 2.0: see [LICENSE](LICENSE) and [NOTICE](NOTICE).
