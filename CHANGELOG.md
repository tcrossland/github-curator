# Changelog

What changed for someone using the plugin, newest first. A Claude Code session keeps the version it started with, so start a new session after installing an update.

## Unreleased

- On claude.ai, where the pins come from a summary of your profile page that can leave some out, a repo the summary doesn't name shows as "pin unknown" rather than "not pinned now", and the feature call asks you to check your profile. The scorecard lists the pins it read as "may be incomplete".
- In Claude Code, where the artifact listing can stop at your 50 most recently updated artifacts, a review that finds no previous page there says in its footer that an older one may exist. `traffic` asks for the Traffic history page's link rather than start a second page, and a scheduled run that can't ask keeps the snapshot as a file instead.
- Triage writes every repo's reason and question anew on each run, taking only the forks' parents from the last triage, so a rule change since shows in its calls rather than being hidden behind last run's words.
- Triage counts only other people's stars: a repo you starred yourself shows it ("3 stars, one yours"), and your own star no longer counts as interest in its reasons or keeps a fork from a clear delete. It reads your stars once, at one call per 100 repos you've starred. On claude.ai, where that list may be refused, a single star it can't place says "possibly yours".
- Getting started asks whether the page says the project's status, maintained, experimental or finished, and is flagged when nothing says it, with a fix that adds the line for you to confirm. Commit dates and version numbers don't count, and an archived repo's banner does. Tone for `for:users` no longer asks the same thing. The quick review leaves it out.
- `repo-review` takes `for:users` or `for:researchers` in a full review or a portfolio, to judge a repo for people deciding whether to depend on it, or for others in its field, rather than for potential employers and collaborators, still the default. It changes what Tone, Jargon and Evidence look for: for users, whether it says its status, what it supports and where to get help, with the field's standard terms taken as known; for researchers, how it relates to earlier work and how to cite it, with every result reproducible. The scorecard says which readers a review used, and a re-run's reply names a change of readers first.
- A review's Contributors list counts the people named as co-authors in commits' `Co-authored-by` trailers, as GitHub's own Contributors sidebar does, and Tone's check on credit counts their work as shared. Coding assistants such as Claude and Copilot, and bots, are left out.
- Tone's check on credit says when it applies: the README claims something as yours, in the first person or under your name, and someone else's commits made a share of it. Tone is then flagged every time, never passed or failed for credit alone, where runs on the same repo had sometimes left it unflagged.

## 0.7.0 (2026-11-22)

- `repo-review overview` is now `repo-review portfolio`, after the page it publishes, since it's the costliest mode: a full review of every repo, then a ranking. `overview` still runs it. Triage's and the quick review's `next` commands use the new name.
- `repo-review` takes a repo as `OWNER/REPO` as well as its URL, as `stargazers` and `forks` already did, in every mode.
- `repo-review`'s hint in Claude Code's autocomplete says what each mode is for: quick is a glance, triage sorts by action, portfolio reviews each in full.
- `contributions` takes the organisations to count as yours with `orgs:ORG`, since `own` means repos that aren't forks in `triage own`. `own:ORG` still works.
- Three of the seven questions have labels that say what they check: Defensible is now Evidence, Context is Jargon and Way in is Getting started. The questions themselves are unchanged, and a re-run compares with a scorecard that has the old labels question by question.
- `repo-review` with no arguments asks what to review: the repo in the current folder, when it's in a git clone, a quick review of all your repos, or a triage. When no one can answer, as in a scheduled task, it runs the quick review.
- A review prints one line as each step starts, such as `Questions (4 of 7)`, and a portfolio run one as each repo starts, such as `Repo 3 of 10: OWNER/REPO`, so a long run shows where it is.
- A review's timings are more often true to each step: Timing now says which work belongs to each step, where runs had put some of it before the step's line.
- On claude.ai a review no longer asks GitHub for a similar repo's own page, which was refused for every repo not attached to the chat; the search results already hold what the Similar repos panel shows.
- A portfolio run of more than 10 repos says first what it will take, at about five minutes a repo and on claude.ai one approval each, and offers a quick review of them or a full review of the first 10 instead. A triage on claude.ai says how long attaching its repos will take as well as how many approvals.
- On the quick review and triage pages, each repo with a fail or flag, or marked for review, has its own review command with a copy button, so you can pick which to review in full rather than take the page's `next` command for ten.
- A re-run's reply starts with what changed since the last run, such as `Since 2026-11-21: Hook fail → pass; action archive → keep`, printed by the same script as the counts from this run's page and the last one's.

## 0.6.0 (2026-11-22)

- A new mode, `repo-review quick`, gives an at-a-glance review of your repos, or of the ones you name: Hook, Findable and Way in for each, from GitHub's search and each README alone, with a likely action and the most important fix, on one page titled "Quick review". It takes seconds a repo where a full review takes minutes, and its calls are provisional. It leaves out forks, archived repos and your profile README repo unless you name them, and ends with the command for a full review of the repos that need one.
- A review's Similar repos panel says how each similar repo relates to yours, rather than describing it in one line or judging it: whether it does the same job, what yours adds, whether it's maintained, the search words it's found by that yours lacks, one thing worth borrowing, and whether your README should name it.
- A review of a repo no one else has starred says so in both Stargazers lists, in the same words every time: "None: no stargazers besides you".
- Before suggesting a history written in the first person, a review checks who made a repo's commits from its Contributors list, which covers the whole history, rather than from its own shallow copy of the repo.
- A review that recommends making a repo private, or deleting it, no longer ties its most important fix to a question number. For a repo that's already private, make-private means leaving it private for good, and keep means it stays private only until it's ready to publish.
- `repo-review` given several repo URLs and no mode asks whether you want a quick review of them all or an overview, rather than reviewing each in full on its own. When no one can answer, as in a scheduled task, it runs the quick review.
- The README has a diagram of how `repo-review`'s modes hand on to each other, and which skills feed a scorecard's Outcomes panel.

## 0.5.0 (2026-11-21)

- A scorecard shows the fix prompt straight after the questions' strip, before the Outcomes panel and Similar repos. Those two, the changes since the last check, the recommendation's signals and its before-lists start closed, each with a summary of what's inside, such as how many items are to do. Triage's changes since the last triage start closed too.

## 0.4.0 (2026-11-21)

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
