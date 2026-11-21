# Changelog

What changed for someone using the plugin, newest first. A Claude Code session keeps the version it started with, so start a new session after installing an update.

## Unreleased

- The README's Try it section links to the latest release, where the zip is.
- A review that suggests a repo description keeps it to 350 characters, the most GitHub accepts, and writes a shorter one rather than copying a longer description from the manifest.
- The plugin's description is shorter, to fit GitHub's limit of 350 characters for a repo's description, so the repo can use the same words.
- The README opens with what the plugin decides and what sets it apart, and lists `repo-review`'s modes one to a line.
- The README says what a claude.ai chat can't do yet that Claude Code can, and that the no-changes promise is a rule in the skills' instructions.
- The README explains what a Claude plugin, a skill and an artifact are where they first appear.
- The README has a Try it section: what the plugin needs, where to get it and a first command, with what comes back.
- The README's install section is for people installing the plugin: the release routine and the notes on test builds moved to the repo's notes for working on it.
- A new skill, `forks`, lists the forks of one of your repos that hold commits of their own, on any branch, with what those commits change and who made them, and picks out the ones worth a look. It reads only forks pushed to after they were made, the 30 most recent unless you add `all`. A public repo's review lists them in its Outcomes panel as "Forks with commits".
- A new skill, `traffic`, saves the views, clones, stars and top referrers of every public repo you own to a page titled "Traffic history", one snapshot at a time, and charts them across snapshots, so they outlast GitHub's 14 days. `schedule` sets up a weekly task that saves the next ones. A public repo's review links to the page from its Outcomes panel.
- In Claude Code, the commands that read a fork's commits and a README's opening work as written: Claude Code put the skill's arguments in place of awk's `$0`, `$1` and `$2`, so triage's README listing broke, and an overview given repo URLs would have broken the fork commands too. The README listing also no longer prints errors in zsh, and the fork commands no longer fail there for every fork: zsh read part of the parent's branch name as a modifier.
- A fork's commits beyond its parent are counted on every branch of the fork, against every branch and tag of the parent, not on its default branch alone, and the review and triage name any other branch that holds your commits. Before, a fork whose only work of yours was on a branch such as `develop` could be marked clear to delete.
- In Claude Code, the review and triage clone private repos with `gh`'s login, since `git` alone can't answer its prompt for a password there.

## 0.3.0 (2026-11-21)

- The review's Outcomes panel shows the other people in a repo: everyone else with commits, by login or by the name on their commits (never an email address), and the open issues and pull requests other people opened, each with its age and whether you've replied.
- Tone is flagged when the README presents shared work as yours alone, and the fix credits the others by name. Way in is flagged when the README doesn't say whether the repo wants contributions while someone's issue waits, or asks for issues that are turned off, or invites pull requests on an archived repo.
- For keep and archive, the fix prompt drafts a reply to each issue or pull request waiting on you, for you to post. The review never posts it.
- The overview has a copy button on each repo that has something to fix, copying the fix prompt from that repo's scorecard, so you can act on the overview without opening each scorecard. Each prompt is for a Claude Code session in its own repo.
- Before publishing, the review scans the repo's full history for keys, tokens and passwords with betterleaks (version 1 or 2), on every branch, and lists each finding with its commit, file and line, never the secret itself. betterleaks isn't installed on your computer for you (`brew install betterleaks`); without it, the review says the scan didn't run and leaves the item to do. On claude.ai, whose session has no betterleaks, the review fetches release 1.10.1 into the session's own VM and runs it only if it matches the release's checksums.
- A new skill, `contributions`, lists your merged pull requests to repos you don't own: those to your own organisations counted, those to employers you name with `employers:` listed apart, and those to other people's projects one row per repo with its stars, dates and what you did. Pull requests to private repos are counted, never named. On claude.ai, where your organisations can't be read, it says which owners it counted as yours and that the private count may be short.
- Triage and the review read GitHub in ways that also work in a claude.ai chat, where most of GitHub's API is refused for repos not attached to the chat. A fork's commits beyond its parent come from git rather than GitHub's compare, which claude.ai refuses between a fork and its parent, and which listed at most 250. READMEs, in triage and for similar repos, come from a clone of the README alone.
- Triage records each fork's parent on its page and reads it from there next time. On claude.ai it attaches only the repos it can't do without, the private repos and the forks whose parent it doesn't know, asking once and asking you to switch the chat to Manual mode first, so each attach waits for your approval. Manual mode asks for each repo, so when a first triage would need more than 10 approvals it suggests running that one from Claude Code. A repo it can't attach goes to review. An organisation's triage on claude.ai says to run it from Claude Code.
- Triage finds your pull requests to the forks' parents in one search rather than one per fork, so an account with many forks no longer runs into GitHub's search limit.
- On claude.ai, `stargazers` reads each stargazer's profile page instead of the API, which is refused there, and says where it read it. When no profile can be read, it and the review's Stargazers lists say "Not available" with the reason, rather than that none are in the same field.

## 0.2.14 (2026-11-20)

- `repo-review` says what to use in Claude Code in place of each claude.ai tool, and saves the page as a file when there's no artifact tool to publish it with.
- Step 1 says where GraphQL works for reading the profile's pins, rather than calling it unavailable and then using it.
- The review's JSON starts in Step 4, with the questions the quote checker reads, and its timings count that writing in Step 4's row.

## 0.2.13 (2026-11-20)

- A single review loads less: the overview and triage steps are in files of their own, read only in those modes, so the review's instructions are about a fifth shorter.
- The quote checker ships as a file, `verify_run.py`, and is run as written rather than retyped from the instructions.

## 0.2.12 (2026-11-20)

- `stargazers` finds a stargazer's three most-starred repos, and their organisation's, among all of them. Before, it looked only at the first 100, so for someone with more it could miss their best-known work.

## 0.2.11 (2026-11-20)

- The README that comes with the plugin no longer links to notes that aren't in it.

## 0.2.10 (2026-11-20)

- Timings split a run's time between its steps more truly: each step's time is logged on its own as soon as the step ends. Before, the work of the next step could be counted to the one before it.

## 0.2.9 (2026-11-20)

- Timings give an API call count on more rows. GitHub's rate limit can give slightly different reset times, or now and then a stray count, within one hour, and each blanked the count on rows where GitHub's hourly window hadn't reset. Now only a stray count's two rows go without.

## 0.2.8 (2026-11-20)

- A review's Timings know that GitHub doesn't count traffic requests, so the Outcomes row's API calls leave out its four requests for views, clones, referrers and pages, and a run says so rather than guessing.

## 0.2.7 (2026-11-20)

- An overview reviews its repos one at a time, so each scorecard's Timings and the overview's time per repo are that repo's own. Before, reviews could run side by side, and their times and API calls ran together.

## 0.2.6 (2026-11-20)

- The reply to a review or an overview takes its pass, fail and flagged counts from the page's own data, so the reply and the page always agree. Before, they were counted by hand and could differ.

## 0.2.5 (2026-11-19)

- Every scorecard, overview and triage page has a Timings section at its foot: how long each step took and how many GitHub API calls it made, with totals. It's closed until opened.

## 0.2.4 (2026-11-19)

- `repo-review triage org:NAME` triages an organisation's repos, more strictly than your own, on a page of its own.
- `no-publish` in any `repo-review` mode saves each page as a file instead of publishing it.
- `stargazers` with no repo covers every public repo of yours that has stars. `since:YYYY-MM-DD` keeps only recent stars, and `all` reads every stargazer, not only the 30 most recent.
- Both skills show their arguments in Claude Code's autocomplete.

## 0.2.3 (2026-11-19)

- `stargazers` no longer mistakes someone else's public repo for a private one. GitHub lists stargazers only to a repo's owner, so for another owner's repo it now says the list is hidden and gives the public star count. The review's Outcomes panel shows the same gap.

## 0.2.2 (2026-11-19)

- The fix prompt follows the repo's own rules and your instructions on branches. Without either, a public repo, or one others commit to, still gets a branch and a pull request, and a private repo only you commit to gets unpushed commits on the current branch.

## 0.2.1 (2026-11-19)

- Way in fails a repo with no licence file, one whose README or manifest names a licence no file holds, and one whose licence still has a template's placeholder copyright line.
- Featuring now needs a licence. Archiving and publishing need a known source, with terms that allow redistribution, for any third-party data or model files.
- Triage marks your own repos that have no licence.

## 0.2.0 (2026-11-19)

- First release: `repo-review`, with its `overview` and `triage` modes, and `stargazers`.
