---
name: "repo-review"
description: "Review the user's GitHub repo or a README draft: recommend keep, publish, archive, make private or delete, and whether to feature it; check it and publish a scorecard. Modes: quick, triage, portfolio."
argument-hint: "[repo | folder | file] · quick [repos…]: a glance · triage [public|private|own|forks|archived|org:NAME]: sort by action · portfolio [repos…]: full review of each · no-publish"
---

# Repo review

The work product is a public GitHub repo, published as a portfolio piece to attract potential employers and collaborators. A great one draws traffic, stars and a community. These usually go wrong by being so niche that few people find them or see why they matter. Use this review on any draft, whoever wrote it: the user, Claude, or both together.

For a repo, the review also recommends what to do with it, whether to feature it on the user's profile, and the work worth doing before each. Not every repo should stay as it is: some are finished and should be archived with a proper account of what they were, some aren't worth showing, some private ones are ready to publish, and a few deserve one of the six pinned places on the user's profile. It also finds similar repos, so the review can say what this one adds and where readers who want a maintained tool should go.

There are four ways to run it:
- **One draft**: the arguments are a repo, a local clone's folder, a file, a doc link or pasted text. Run Steps 1 to 6.
- **Portfolio**: the arguments start with `portfolio`, or `overview`, its old name, optionally followed by repos. Run Steps 1 to 4 for each repo, one repo at a time (publishing each repo's scorecard as usual), then Step 7. Step 7 and how a portfolio run logs its time are in [portfolio.md](portfolio.md) beside this file: read it before starting, and only in this mode.
- **Triage**: the arguments start with `triage`, optionally followed by filters (`public`, `private`, `own`, `forks`, `archived`, or `org:NAME` for an organisation's repos). Run Step 8 only, from [triage.md](triage.md) beside this file, read only in this mode: a quick pass over many repos from GitHub's API, without cloning or the seven questions, that sorts out the clear cases and names the repos worth a full review.
- **Quick**: the arguments start with `quick`, optionally followed by repos. Run Step 9 only, from [quick.md](quick.md) beside this file, read only in this mode: an at-a-glance review of many repos from GitHub's search and each README, answering Hook, Findable and Way in, on one page with a row per repo.

A repo is given as its URL or as `OWNER/REPO`. A word of that form is a repo unless it names a folder or file that exists in the working folder.

Several repos with no mode word name no mode: before anything else, ask the user whether to run a quick review of them all (offered first) or a portfolio review, which reviews each in full, and run the one chosen with those repos. When no one can answer, as in a scheduled task, run the quick review and say why in its footer.

In any mode, `no-publish` as a separate word in the arguments saves each page as a file instead of publishing it: write it to the scratchpad, or a working folder outside any clone, and create or republish no artifact. A previous run is still read for comparison. It's for trying a change to a rule or the template without touching the live page.

**In Claude Code.** The steps name claude.ai's tools. In Claude Code, use these in their place:
- `add_repo`: none needed. Claude Code's `gh` uses the account it's signed in with, so read the repo directly.
- `git` reads a private repo over HTTPS only with a credential, and Claude Code's shell can't answer git's prompt for one. Give every clone and fetch of a private repo `gh`'s login, which changes no setting: `git -c credential.helper='!gh auth git-credential' clone ...`, and the same before `-C` in a fetch.
- `list_repos`: `gh api --paginate 'user/repos?affiliation=owner&per_page=100'`.
- `device_request_folder_access`, `device_bash` and `device_stage_files`: none needed. A local clone is on the same computer, so read it in the shell, still read only.
- `list_artifacts`, `read_artifact`, `get_artifact` and `publish_files`: the Artifact tool's `list`, `read` and `publish` actions. `list` takes no query, so look for the title among the artifacts it lists, paging on until it's found or the list ends. Read an existing artifact before republishing to it, and republish by passing its `url`.
- With no artifact tool, work as with `no-publish`, and say in the reply that the page wasn't published and the previous run couldn't be looked for.

## The questions

Run all seven, in this order. Question 1 matters most.

1. **Hook.** Would someone outside this niche understand, from the title, the repo description and the opening of the README, what this is, why it's interesting and what the answer turned out to be?
2. **Findable.** Is the repo set up so people can find and share it: public, with a description and topics in the words people search for?
3. **Facts.** Does every fact on the page (results, statuses, versions, commands, links, tags) match the file, report or setting it comes from?
4. **Defensible.** Could the author defend every strong claim on the page if a sceptical reader challenged it, and does the page point to the test, report or file that proves it?
5. **Context.** Are the field's terms and yardsticks defined or linked where they first appear, so a capable engineer from outside the field can follow?
6. **Way in.** Can a visitor do something with it (run it, reuse a piece of it or join in), and does the page tell them how?
7. **Tone.** Will it land with a potential employer or collaborator? Does it read as finished work that shows the author's judgement and what they learned, rather than internal notes?

Statuses:
- **pass**: the draft meets the question.
- **fail**: it plainly doesn't.
- **flagged**: it partly does, or the call needs the user's judgement or information the draft doesn't hold (for example repo settings when only README text was pasted).

**Private repos** are checked as they would read once public: the review is there to say whether they're worth publishing and what to do first, and making one public is the user's call. On a private repo, flag Findable rather than failing it when visibility is its only gap, and still check the description and topics as they would read once public.

Don't add numbers, thresholds or rules beyond these questions.

## The recommendation

For a GitHub repo, recommend one action:
- **keep**: leave it public (or private, if it's still being built) and keep working on it. The scorecard's fixes are the work.
- **publish**: a private repo that is worth showing. Make it public once the work before publishing is done.
- **archive**: finished or stopped work that is still worth showing. Do the work before archiving, then archive it, so the page tells the story of what it was and why it stopped. If it's private, publishing it is the last step before archiving.
- **make-private**: work worth keeping for the user but not worth showing, or that shouldn't be public. For a repo that is already private, it means leaving it private for good, where keep means it stays private only until it's ready to publish.
- **delete**: nothing worth keeping anywhere: an empty repo, a fork with no commits beyond its parent, a tutorial copy, or a duplicate of another repo.

Decide from what the repo shows, not from a rule: whether it's the user's own work (`fork`, and for a fork how many commits it has that its parent doesn't), when it last changed (`pushed_at` and the latest commit), whether its README says it's maintained, how it does on the seven questions (Hook, Defensible and Tone say most about whether it's worth showing), and whether other people rely on it (stars, forks, open issues and pull requests from others). Prefer the action that loses least: archive over make-private when anyone else has starred, forked or opened an issue, and make-private over delete whenever there is anything of the user's own in it. When the evidence points two ways (for example, recent commits but a README that says it's unmaintained), recommend the likelier action and say what the user should confirm.

An already archived repo gets **archive** again when that is still right, with the work-before list showing what's done; any remaining item needs the repo unarchived first (`gh repo unarchive`), which is the user's call.

Write down the signals as short facts ("last commit 2017-05-04", "14 stars, 0 open issues", "fork, 0 commits ahead of its parent"), then a one- or two-sentence reason that ties them to the action.

What each action costs, from GitHub's own documentation (say the relevant line in the recommendation's `caveat`):
- Changing visibility, in either direction, erases the repo's stars and watchers. Making a public repo private also detaches its public forks, which stay public.
- Archiving makes issues, pull requests, comments, code, releases and the rest read-only; GitHub recommends closing issues and pull requests and updating the README and description first. It can be undone with `gh repo unarchive`.
- Deleting a repo can be undone within 90 days only if it isn't part of a fork network with other repos in it. Deleting a public repo doesn't delete its forks.

Never archive, unarchive, delete or change the visibility of a repo, or close an issue or pull request: each is the user's call. The review only recommends.

### Work before the action

For **archive**, **publish** and **delete**, list the work worth doing first, each item marked `done`, `todo` or `n/a` from what the repo shows now, with a short note naming the evidence (a file and line, a setting, a command's result). Mark an item `todo` only when it applies to this repo; skip what doesn't, rather than padding the list.

Before archiving:
1. **Notice**: the first line of the README says the project is no longer maintained and the repo is archived, linking to the status section.
2. **Opening**: the README opens with what it was and what it set out to explore (this is Hook; mark it from the question's status).
3. **Status and history**: a section, in the first person, that says when it was written, how far it got, why it stopped and what the author would do differently now. Any later, better-known project in the same space is mentioned once, in a sentence that says which came first, with a pointer to maintained tools for readers who want one (from Similar repos).
4. **Still runs, or says it doesn't**: it builds and its tests pass on a current runtime, with the commands and results recorded in a pull request the README links to, or the README says plainly that it no longer runs.
5. **Old dependencies**: if its dependencies are old enough to have known vulnerabilities, the README says so and says to run it locally only.
6. **Licence and notices**: a licence file, and a notice for every file copied from another project.
7. **Third-party data and models**: every dataset, model weight or other file from an outside source names that source, and its terms allow redistribution; anything whose terms don't, or whose source is unknown, is removed from the history, not only the working tree. An archived repo keeps serving them.
8. **Picture**: a screenshot or sample output, when there is a UI or a result to show.
9. **Description and topics**: set, since archived repos still appear in search.
10. **Issues and pull requests**: each open one answered, merged or closed, since archiving makes them read-only.

Before publishing:
1. **Secrets and private data**: no keys, tokens or passwords anywhere in the full history, every branch included, by the secrets scan below; and no internal hostnames or personal data, which the scan doesn't look for, so search the history for those yourself. Anything ever committed becomes public with the repo.
2. **Licence**: a licence file, and notices for copied files.
3. **Third-party data and models**: every dataset, model weight or other file from an outside source names that source, and its terms allow redistribution; anything whose terms don't, or whose source is unknown, is removed from the history, not only the working tree.
4. **The seven questions**: every fail fixed; publishing is the moment it gets the most attention.
5. **Description and topics**: set before it goes public.

**The secrets scan.** Run betterleaks over the full clone from Step 1 (never a `--depth 1` one), in the shell that holds the clone (`device_bash` for a local clone), with `CLONE` as its path, from a folder outside it so the report isn't written inside it. Both of its major versions are in use and take different flags, so the script picks by version. It scans locally: never add `--validate`, `--analyze` or `--validation`, which send each secret found to its provider to test it.

On claude.ai, when the clone is in the session's own Linux VM (not on the user's computer through `device_bash`) and `command -v betterleaks` finds nothing, fetch the release this review was checked with first, in that VM's shell. It goes into a folder of its own and runs only if it matches the release's checksums:
```sh
[ "$(uname -s)" = Linux ] || { echo "fetch betterleaks only in the claude.ai VM" >&2; false; } &&
case $(uname -m) in x86_64|amd64) f=betterleaks_1.10.1_linux_x64.tar.gz ;; aarch64|arm64) f=betterleaks_1.10.1_linux_arm64.tar.gz ;; *) echo "no betterleaks build for $(uname -m)" >&2; false ;; esac &&
mkdir -p "$HOME/betterleaks-1.10.1" && cd "$HOME/betterleaks-1.10.1" &&
curl -fsSLO "https://github.com/betterleaks/betterleaks/releases/download/v1.10.1/$f" &&
curl -fsSLO https://github.com/betterleaks/betterleaks/releases/download/v1.10.1/checksums.txt &&
grep "  $f\$" checksums.txt | sha256sum -c - &&
tar -xzf "$f" betterleaks && ./betterleaks version
```
It prints `OK` and `1.10.1` when it worked; the scan below then finds it there. Never fetch it anywhere else: on the user's computer, in Claude Code or through `device_bash`, the review installs nothing.

```sh
bl=$(command -v betterleaks || command -v betterleaks-v1 || echo "$HOME/betterleaks-1.10.1/betterleaks")
v=$("$bl" version 2>/dev/null)
case $v in
  1.*) "$bl" git CLONE --no-banner --redact --exit-code 0 --report-format json --report-path secrets.json ;;
  2.*) "$bl" git CLONE --no-banner --silent --redact --exit-code 0 --validate=false --analyze=false --output secrets.json ;;
  *) echo "betterleaks not found or not version 1 or 2: $v" >&2; false ;;
esac &&
jq -r '(if type == "array" then . else .findings end)[] | (.attributes // .Attributes) as $a | [$a["git.sha"][:7], (.location.path // .File), (.location.start_line // .StartLine), (.rule_id // .RuleID), $a["git.date"][:10]] | @tsv' secrets.json
```
Each line is a finding: commit, file, line, rule and date. With `--exit-code 0` a clean scan and one with findings both exit 0, so any other exit means the scan failed. Mark item 1 `done` only when the scan ran and found nothing, and the search for hostnames and personal data found nothing either. Otherwise mark it `todo`, with the note listing each finding as `COMMIT FILE:LINE (RULE, DATE)`. You may read a finding's line to judge it (a test fixture's fake key is still a finding, since the scan can't tell), but never copy a secret's value into the scorecard, the fix prompt or the reply. A finding is the user's to act on, so keep it out of the fix prompt: revoke the key at its provider first, since removing it from the history doesn't make it safe once it has been seen. If betterleaks isn't there (and, on claude.ai, the fetch above failed), or the scan fails, never install it any other way: search the history yourself as well as you can, mark item 1 `todo` whatever that finds, and say in the note that the scan didn't run and why, with `brew install betterleaks` as the way to run it.

Before deleting:
1. **Nothing of the user's own**: no commits, notes or results that exist only here. For a fork, judge it from Step 1's commits on every branch, not the default branch alone, and name each other branch that holds any of the user's.
2. **A copy**: a local mirror (`git clone --mirror`) if there's any doubt.
3. **Nothing links to it**: the user's profile, other repos' READMEs and any site or CV.

**keep** and **make-private** have no list: for keep, the scorecard's fixes are the work; for make-private, the caveat says what is lost. If the repo is pinned on the user's profile, add **Unpin** to the list for make-private and delete (and make a list for make-private to hold it).

### Feature

Whether to feature the repo is a separate yes or no, alongside the action: an archived repo can still be a showcase piece. Only a repo that is or will be public can be featured: keep (when it's public), publish and archive.

Feature a repo when it is among the best evidence of the user's judgement and skill: it passes or nearly passes Hook, Defensible and Tone, it has an answer or a result worth telling, and it adds something the similar repos don't. Say why in one or two sentences, and say so when it's a close call.

A profile holds up to six pinned repositories and gists combined, so featuring is a choice across all the user's repos. Name the current pins (from Step 1). If all six places are taken, say which current pin this one should replace and why, or that it shouldn't displace any of them. A repo that's pinned but shouldn't be featured gets "unpin" as a recommendation, with the reason.

Before featuring:
1. **The seven questions**: all pass. A featured repo gets the most visitors, so a fail costs most here.
2. **Licence**: a licence file, so the visitors it draws may reuse what they find, and a notice for every file copied from another project.
3. **Description, topics and a link**: description and topics set, and the homepage field pointing to a demo, report or write-up when there is one.
4. **A release**: a tagged release, when it's software people would install or run.
5. **Pinned**: pinned on the user's profile. Pinning is the user's call; the review only recommends.

Leave the recommendation and the feature call out for pasted text, a file, or a local clone with no GitHub remote.

## Timing

Every run logs how long each step takes and how many GitHub API requests it makes, and the page shows them. Keep the log in the working folder where Step 5 fills the template, outside any clone, one per page: `REPO-NAME-timings.log`, `portfolio-timings.log`, `triage-timings.log` or `quick-timings.log`. Run every timing line in that folder's shell, never through `device_bash`, so the log has one file and one clock. Write its first line, named `start`, with `>` as the run begins, so a log left from an earlier run is replaced. Then, as each step below finishes, append a line named for that step with `>>`, in a command of its own: send it as soon as the step's work is done, and write none of the next step's work into the same command.

```sh
printf '%s\t%s\t%s\n' 'NAME' "$(date -u +%s)" "$(r=$(gh api rate_limit --jq '"\(.resources.core.used)\t\(.resources.core.reset)"' 2>/dev/null) && printf %s "$r")" >> "LOG"
```

Reading `rate_limit` costs no request, and `core.used` counts nearly every REST request, each page of a paginated call included. It leaves out three kinds, so say so rather than guess:
- **Search requests** have their own count, which resets every minute, so it can't be read across a step. Count the `search/` requests each step makes yourself, as `searches`.
- **GraphQL requests** have their own limit and aren't counted.
- **Traffic requests** (`traffic/views`, `traffic/clones` and `traffic/popular/...`) aren't counted, so a review's `Outcomes` row leaves out its four.

The count is the GitHub account's, not the run's: requests made at the same time by anything else on the account (the user's own `gh`, another session) are counted too, and so are this run's requests through `device_bash`.

Log a line only for a step that ran. The steps, in order (portfolio, triage and quick name theirs in their own files):
- **One draft**: `Get the draft` (Step 1 up to the outcomes), `Outcomes`, `Similar repos`, `Questions` (Step 2), `Compare` (Step 3), `Verify and recommend` (Step 4, which starts the run's JSON with the questions) and `Build` (adding the rest of the JSON in Step 5).

The page needs its timings before the template is filled, so for every page, in this order: finish the JSON, append the `Build` line, turn the log into rows with the script below (`python3 timings.py LOG`), add `searches` to the rows that made any, put the rows in the JSON as `timings`, then fill the template. Filling and publishing come after the last line, so the page doesn't time them.

```python
import json, sys
rows, prev = [], None
for line in open(sys.argv[1], encoding='utf-8'):
    f = line.rstrip('\n').split('\t')
    try:
        t = int(f[1])
    except (IndexError, ValueError):
        continue
    ok = len(f) == 4 and f[2].isdigit() and f[3].isdigit()
    cur = {'t': t, 'used': int(f[2]) if ok else None, 'reset': int(f[3]) if ok else None}
    if prev:
        same = ok and prev['used'] is not None and abs(cur['reset'] - prev['reset']) <= 60 and cur['used'] >= prev['used']
        rows.append({'step': f[0], 'seconds': t - prev['t'], 'calls': cur['used'] - prev['used'] if same else None})
    prev = cur
print(json.dumps(rows))
```

A step's `calls` is null when the rate limit couldn't be read at its start or its end (so one failed read blanks two rows), when GitHub's hourly window reset during it, or when its two reads disagree. Reads within one window can give resets a second apart, so resets up to a minute apart count as one window; a real reset moves it by an hour or more. A read can also give a `used` lower than the read before it, with a reset in a later window, while the next read is back in the earlier one: that read blanks two rows, as a failed read does. A line that can't be read at all is skipped, and its time goes to the next row. If `gh` isn't available, still log the times.

## Step 1: get the draft

Accept any of these:
- **Pasted text**: use it as given. Questions 2 and 3 can only be partly checked without the repo, so flag what can't be seen.
- **A file** (attached, or in a connected folder on the user's computer): read it. If it's a README inside a repo folder, also read the files it links to.
- **A GitHub repo or file link**: attach the repo with `add_repo` and `access: "push"` before anything else, so the GitHub API (settings, outcomes, traffic) works. Then clone it with `--depth 1` into a new, empty directory, or fetch and check out the latest default branch if a clone already exists. If push access is refused, fall back to a read-only clone, and take settings from the repo page with WebFetch. A WebFetch result is a summary, not the page, so label any quote taken from it "repo page summary, may not be verbatim".
  Read `README.md`, every file it links to that bears on a claim, the manifest (`pyproject.toml` or equivalent), the CI workflow and the license. Read settings with `gh api repos/OWNER/REPO` (description, topics, visibility, homepage, has_issues, `license`, and for the recommendation `fork`, `archived` and `pushed_at`) and tags with `gh api repos/OWNER/REPO/tags`. For a fork, count the commits it has that its parent doesn't with the git commands below, taking the parent's name from `.parent.full_name` in the settings. For a private repo, clone the full history instead of `--depth 1`, so the secrets check before publishing can read it. Use REST for everything but the pins.
  Read the fork's commits with git, not the compare API. In the working folder, clone the fork without its files, every branch, and fetch the parent's branches and tags into it the same way (a public parent needs no attaching on claude.ai):
  ```sh
  d="forks/REPO.git" && { [ -d "$d" ] && git -C "$d" fetch -q --prune origin '+refs/heads/*:refs/heads/*' || git clone -q --bare --filter=tree:0 "https://github.com/OWNER/REPO.git" "$d"; } &&
  git -C "$d" fetch -q --prune --no-tags --filter=tree:0 "https://github.com/PARENT-OWNER/PARENT-REPO.git" '+refs/heads/*:refs/parent/heads/*' '+refs/tags/*:refs/parent/tags/*' &&
  git -C "$d" symbolic-ref --short HEAD &&
  git -C "$d" rev-list --count --branches --not --glob='refs/parent/*' &&
  git -C "$d" log --source --branches --not --glob='refs/parent/*' --format='%S%x09%an%x09%ae%x09%ad%x09%s' --date=short | awk -F'\t' -v OFS='\t' -v branch=1 -v email=3 '{sub(/^refs\/heads\//, "", $branch); sub(/.*@/, "", $email); print}'
  ```
  The first line is the fork's default branch, and the second the count of commits on any of its branches that no branch or tag of the parent holds. Then comes one line per commit, newest first: a branch it's on, the author's name, their email's domain (never the address), the date and the subject. A commit on a branch other than the default is easy to miss on GitHub, so name those branches wherever the commits are reported. If the parent can't be cloned (deleted, or private and not attached), say so and leave the count out.
  Read the repos pinned on the user's profile. REST doesn't list them; GraphQL does. GraphQL works in a shell on the user's computer (Claude Code's own, or `device_bash` on claude.ai), and a claude.ai session's own shell refuses it, both `gh api graphql` and `gh repo view --json`. Where it works, use `gh api graphql -f query='{user(login:"OWNER"){pinnedItems(first:6){nodes{... on Repository{nameWithOwner}}}}}'`. Otherwise take them from the profile page (`https://github.com/OWNER`) with WebFetch, asking for the pinned repositories as `owner/name` (the page shows the owner only for repos owned by someone else, so ask for it from each link's path), and label them "profile page summary, may not be complete". If neither works, say the pins couldn't be read and make the feature call without them.
  If `private` is true in that response, check it as set out under Private repos above, and add "private" to the scorecard's `subject`. If `gh api repos/OWNER/REPO` returns 404, the repo either doesn't exist or is private and not shared with this account, and the WebFetch fallback can't see a private repo either. Say so in one line and ask the user for access, a local clone or the pasted README.
- **A local clone** (a folder on the user's computer that holds a `.git` directory): this is the pre-push check, so review the working copy exactly as it is.
  - Work through the device bridge, read only: never check out, fetch, pull, stash, commit or write anything inside the folder. If the folder isn't connected yet, ask for it with `device_request_folder_access`.
  - With `device_bash` in the folder, read the branch (`git rev-parse --abbrev-ref HEAD`), the commit (`git rev-parse --short HEAD`), uncommitted changes (`git status --porcelain`) and the remote (`git remote get-url origin`). Read `README.md`, every file it links to that bears on a claim, the manifest, the CI workflow and the license from the working copy, and check links and anchors on disk.
  - Run Step 4's `verify_run.py` in that shell, from a copy written to a scratch file outside the connected folders, with the folder as `REPO-ROOT`. If `device_bash` isn't available, stage the README and the files it quotes or links to with `device_stage_files` and run everything in the workspace.
  - Settings and outcomes come from GitHub: if `origin` points to a GitHub repo, attach it with `add_repo` as in the bullet above and read them through the API, including whether the repo is private. They describe what's live, not the working copy, so say so in the Findable finding when the branch isn't the default branch. With no GitHub remote, flag Findable as not checkable and leave the outcomes panel out.
  - In the scorecard's `subject`, say "working copy at PATH, branch BRANCH at commit COMMIT", adding "with uncommitted changes in N files" when `git status` lists any. A quote from a file with uncommitted changes gets "(working copy)" after its line number.
  - Find the previous run by the repo name from `origin` (or the folder name with no remote), so a local check and a GitHub check of the same repo share one scorecard and the Since last check panel compares them.
- **A Google Doc**: use the Google Drive connector if one is connected.
- **A claude.ai artifact or doc**: use `read_artifact`, or the Claude Docs read tool.
- **Anything else**: WebFetch.
- If the draft can't be read, say so in one line and ask the user to paste it. Don't guess at its contents.

Note the commit hash or version you checked. It goes in the scorecard's subject line.

**House style.** Look for the repo's own writing rules: CLAUDE.md, CONTRIBUTING.md, a style guide, or a writing section in the docs. Every replacement line the scorecard suggests, and the whole fix prompt, must follow them (for example British English and no em-dashes), so a fix can be pasted in as it is. If there are none, match the README's own spelling and voice. In every case, when you write new README text:
- Write a sole author's history, motives and lessons in the first person ("I stopped work on it"), not impersonally ("Work stopped"), so the page shows whose work it is. Check whose commits they are first, from Contributors under Outcomes, never from `git shortlog` on a `--depth 1` clone, which holds one commit; with no GitHub remote, run `git shortlog -sn` on the local clone, which has its full history.
- State an interest or a claim directly ("My interest was in X"), not by contrast with what it wasn't ("less in Y than in X").
- Don't set the repo's dates beside someone else's product in a list or timeline: it reads as a claim of priority or copying. Say once, in a sentence, that one came before the other, then point readers to the other.
- Don't repeat the same noun or opening ("It was a prototype", "It is a prototype") across neighbouring paragraphs.

**The previous run.** Look for this repo's existing scorecard with `list_artifacts` and the query "Repo review: REPO-NAME", or, failing that, "Portfolio repo check: REPO-NAME" (its title before the skill was renamed). If there is one, read it with `read_artifact` and parse the JSON inside `<script type="application/json" id="data">`. Use it only to compare against in Step 3. Never copy its text into this run.

### Outcomes (context only)

When the draft is a GitHub repo, also gather how the repo is doing, to show beside the check. These figures never change a status or the verdict, and get no pass or fail: there is no bar for them.

- **Repo stats**: stars, forks and watchers from `gh api repos/OWNER/REPO` (`stargazers_count`, `forks_count`, `subscribers_count`); open issues by counting every page of `gh api --paginate 'repos/OWNER/REPO/issues?state=open&per_page=100' --jq '.[] | select(has("pull_request") | not) | .number' | wc -l` (the issues endpoint also returns pull requests, which the filter leaves out); and open pull requests with `gh api --paginate 'repos/OWNER/REPO/pulls?state=open&per_page=100' --jq '.[].number' | wc -l`. If `gh api` can't reach the repo, take stars, forks and watchers from the repo page with WebFetch, and mark issues and pull requests "Not available".
- **Traffic** for the last 14 days: `gh api repos/OWNER/REPO/traffic/views`, `.../traffic/clones`, `.../traffic/popular/referrers` and `.../traffic/popular/paths`. Report total views and unique visitors, total clones and unique cloners, and the top three referrers and most-viewed pages. GitHub shows traffic only to accounts with push access; if that was refused in Step 1, show each traffic figure as "Not available" with the reason.
- **Traffic history**: for a public repo, look for the page the `traffic` skill keeps, with `list_artifacts` and the query "Traffic history", and if there is one, give its link as `history` in Step 5. Don't read it: it holds every repo's traffic since the first snapshot, and the link is all the scorecard needs.
- **Stargazers**: run Steps 1 to 3 of the `stargazers` skill for this repo, under its rules. It lists who starred the repo and when, reads each stargazer's public profile, and picks the ones whose work is in the same field. Its Step 4 reply doesn't apply here: the results go in the two Stargazers lists in Step 5. In this check, never follow, star, message or open an issue for anyone. If the `stargazers` skill isn't available, or its Step 1 stops because GitHub doesn't list the stargazers to the user (the repo isn't the user's own), leave both Stargazers lists out and add an `items` entry labelled "Stargazers", valued "Not available", with the note "stargazers skill not loaded" or "GitHub lists stargazers only to the repo's owner", so the gap shows on the scorecard. When the list was read but no stargazer's profile could be, no pick was made: the "Stargazers worth a look" list says "Not available" with the reason, never "None in the same field".
- **Forks**: when `forks_count` is above 0, run Steps 1 to 3 of the `forks` skill for this repo, under its rules. It lists the forks that hold commits the repo doesn't, what those commits change and who made them. Its Step 4 reply doesn't apply here: the results go in the "Forks with commits" list in Step 5. In this check, never star, follow, message, or open an issue or pull request on a fork. If the `forks` skill isn't available, leave the list out and add an `items` entry labelled "Forks with commits", valued "Not available", with the note "forks skill not loaded".
- **Contributors**: everyone else with commits on the default branch, and how many and when, with each person's login where GitHub links one and the name on their commits otherwise, never an email address. List the commits, then group them with the script below (`python3 people.py commits.tsv OWNER`), not by hand:
  ```sh
  gh api --paginate 'repos/OWNER/REPO/commits?per_page=100' --jq '.[] | [(.author.login // ""), .commit.author.name, .commit.author.date[:10]] | @tsv' > commits.tsv
  ```
  A commit with no login was made under an email not linked to any account; it counts as the user's when its name appears on any commit carrying the user's login. Name a bot or a scheduled job as what it is, not as a person.
- **Waiting on you**: open issues and pull requests opened by someone else, each with its age and whether the user has replied:
  ```sh
  gh api --paginate 'repos/OWNER/REPO/issues?state=open&per_page=100' --jq '.[] | select(.user.login != "OWNER") | [.number, (if .pull_request then "pull request" else "issue" end), .user.login, .created_at[:10], (now - (.created_at | fromdateiso8601) | ./86400 | floor), .comments, .title] | @tsv'
  ```
  For each with comments, the user's last reply is the latest of their comments, `gh api --paginate 'repos/OWNER/REPO/issues/N/comments?per_page=100' --jq '.[] | select(.user.login == "OWNER") | .created_at[:10]' | tail -1`, and for a pull request also their reviews, from `.../pulls/N/reviews` with the same filter on `.submitted_at`. No comment or review from the user means no reply.
- **Pasted text** with no repo: leave the panel out.
- **A private repo**: leave the panel out and don't list stargazers or forks. Only people with access can star, view or clone it, so the figures say nothing about how it will do once public. Still read Contributors and Waiting on you: Tone, Way in and the fix prompt use them.
- Note the date the figures were read.

The Contributors script, `people.py`, which prints the user's count and each other person's, most commits first:

```python
import json, sys
user = sys.argv[2].lower()
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1], encoding='utf-8')]
rows = [r for r in rows if len(r) >= 3]
mine = {name.lower() for login, name, _ in rows if login.lower() == user}
people, own = {}, 0
for login, name, date in rows:
    if login.lower() == user or (not login and name.lower() in mine):
        own += 1
        continue
    key = login.lower() if login else 'name:' + name.lower()
    p = people.setdefault(key, {'who': login or name, 'login': bool(login), 'commits': 0, 'last': date})
    p['commits'] += 1
    p['last'] = max(p['last'], date)
others = sorted(people.values(), key=lambda p: (-p['commits'], p['who'].lower()))
print(json.dumps({'commits': len(rows), 'user': own, 'others': others}, indent=1))
```

### Similar repos (context only)

Find up to five popular repos that do much the same thing, for any draft whose subject is clear (private repos and pasted drafts included). Like the outcomes, they get no pass or fail.

1. Search by the repo's most specific topics, two at a time: `gh api 'search/repositories?q=topic:A+topic:B&sort=stars&per_page=10'`. Skip generic topics such as a language name. When the repo has no specific topics, skip this search: never make topics up.
2. Then search by the words that say what it does, from the description or the README's opening: `gh api 'search/repositories?q=WORD+WORD+in:name,description,topics&sort=stars&per_page=10'`.
3. Read every description before keeping a result: in both kinds of search the most-starred results are often only loosely related. Keep those that do much the same job, leaving out the repo itself and its forks, and leaving out curated lists, course notes and collections unless this repo is one. Order them most-starred first. Record each one's `full_name`, `html_url`, `stargazers_count`, `created_at` and `pushed_at` (dates only), `archived`, `description` and `topics`, and read its README opening.
4. Add any project the README itself names as related or as an alternative, with its link, even when it isn't on GitHub. GitHub search can't find tools hosted elsewhere.

**A README's opening**, here and in triage, comes from a clone that checks out the README and nothing else, in the working folder, not from the API or WebFetch. A public repo needs no attaching for it on claude.ai:
```sh
d="readmes/OWNER--REPO" && { [ -d "$d" ] || { git clone -q --depth 1 --filter=blob:none --sparse "https://github.com/OWNER/REPO.git" "$d" &&
  git -C "$d" sparse-checkout set --no-cone '/[Rr][Ee][Aa][Dd][Mm][Ee]*' '/.github/[Rr][Ee][Aa][Dd][Mm][Ee]*' '/docs/[Rr][Ee][Aa][Dd][Mm][Ee]*'; }; } &&
{ f=; for p in .github . docs; do f=$(cd "$d" && find "$p" -maxdepth 1 -iname 'readme*' ! -type d 2>/dev/null | while IFS= read -r x; do echo "${#x} ${x#./}"; done | sort -n | head -1 | cut -d' ' -f2-); [ -n "$f" ] && break; done
  if [ -n "$f" ]; then echo "== $f"; head -20 "$d/$f"; else echo "no README"; fi; }
```
It prints the README's path and its first 20 lines, or `no README`. A private repo needs attaching first on claude.ai.

The search API has a tighter rate limit than the rest; if a search is refused, say so in the panel's `note` and use what was found.

**How each relates.** The user doesn't maintain these repos, so don't judge them: answer, for each, how it bears on the repo under review, from its search result, its README opening and this repo's own files as Step 1 read them. Make no other request.
- **Overlap**: `same` (the same job), `partial` (part of it, or more besides) or `adjacent` (a neighbouring job). Keep an `adjacent` one only when this repo's README names it.
- **Difference**: one line on what this repo does that the other doesn't, said of this repo alone ("Counts every trial against a deflated Sharpe ratio"), or "nothing clear". Never remark on the other repo's README, results or quality, and never list what this repo lacks: those are not what it adds.
- **Alive**: `maintained` (pushed in the last year and not archived), `quiet` (not archived, but not pushed in the last year) or `archived`.
- **Found by**: the topics, and words in its description, that people would search for and that appear nowhere in this repo's description, topics or README opening, or none.
- **Worth borrowing**: one thing on its README this repo could adopt, named exactly (a one-line result at the top, a quickstart block, a picture of the output), or none.
- **Mention**: whether this repo's README should name it, from how the two relate, whatever the recommended action. The first that fits: `named` (the README already names it), `builds-on` (this repo uses or extends it), `alternative` (it's `maintained` and its Overlap is `same` or `partial`: a tool for readers who want one), `earlier` (it does the `same` job and was created before this repo; say once, in a sentence, which came first), or `no`.

For a project the README names that isn't on GitHub, answer Overlap, Difference and Mention (`named`) from the README's own words, and leave the rest out.

Describe each repo from what its own page says. Never say one copied, influenced or was influenced by another, and don't set dates side by side as if they were a race (see House style).

The questions and the recommendation use them:
- **Hook**: does the opening say what this repo adds, the Difference? A Difference of "nothing clear" for a `same` repo is the Hook's hardest test.
- **Findable**: Found by gives the topics and words to consider adding.
- **Fixes**: a Worth borrowing item goes into a question's fix only when it fixes that question's fail or flag.
- **Archive**: the status and history section points readers to the `maintained` repos marked `alternative`, and names those marked `earlier`.
- **Feature**: what visitors will compare it with; a `same` repo that is `maintained` with a Difference of "nothing clear" counts against featuring.

## Step 2: run every question

Write every field fresh, from the files as they are now, even when a previous run exists.

For each question, in order:
1. Decide the status.
2. Quote the exact line or lines from the draft that decide it: one or two, copied character for character, each with its source (file and line number, or "GitHub repo description, read via the API", "GitHub repo settings, read via the API (summarised, not a verbatim line)", "pasted text, paragraph N"). If the deciding evidence is that something is missing, quote the nearest relevant line and say in the finding what's absent.
3. Write a one- or two-sentence finding in plain words.
4. Write one concrete fix: an edit the user could make today, ideally the actual replacement line or sentence, in the repo's house style. For a pass, say "No change" and, only if there's one, the event that should prompt a re-check.

A repo description the review suggests, in a fix or the fix prompt, is at most 350 characters, the most GitHub accepts: count it with code. When the text it would reuse, such as a manifest's description, is longer, write a shorter one from it rather than a command that copies it.

Checking facts (question 3) means comparing claims against their sources: every relative link and anchor resolves, versions match the manifest, statuses match tags, releases and each other wherever the page states them twice, and numbers match the report they come from. Checking claims (question 4) means finding the test, report or file that backs each strong claim ("reproducible", "no look-ahead", "every trial counted", "works with no keys") and noting any claim the repo's own docs hedge or contradict. Checking the way in (question 6) includes the licence, since without one nobody else has permission to reuse the code: a repo with no licence file (`license` is null in the API, or no `LICENSE`, `COPYING` or similar in the working copy) fails Way in, as does one whose README or manifest names a licence that no file holds, or whose licence file still has a template's placeholders in its copyright line (such as `[year] [fullname]`; the appendix at the end of the Apache-2.0 text keeps its placeholders on purpose, so they don't count). The fix says to add or complete one and leaves the choice of licence to the user; when the repo is mostly writing rather than code, it says a Creative Commons licence fits that better than a software one. Before suggesting a licence be added, check who else has commits (`gh api --paginate 'repos/OWNER/REPO/contributors?anon=1&per_page=100'`; entries without a login are commits under an unlinked email, so say which names they carry, not the addresses): code that others contributed with no licence can be licensed only with their agreement, so when anyone besides the user has commits, the fix names them and says so. For a fork, its code is under its parent's licence: when the parent has none, the fix says only the parent's owner can license it. Judge a private repo as it would read once public. For pasted text or a file with no repo to read, flag Way in when the licence can't be seen. Way in also covers whether the repo says if it wants contributions, and whether its settings agree: flag it (a flag, not a fail) when the README asks for issues while issues are turned off (`has_issues` false), invites pull requests on an archived repo, or says nothing either way while someone else's issue or pull request is waiting (Waiting on you). A repo that doesn't want contributions meets this once it says so.

Checking tone (question 7) includes credit: flag Tone when the README presents work as the user's alone that others share, such as a first-person history over a repo whose commits are mostly someone else's, or a feature described as the user's that another contributor's commits added (Contributors). Count people, not bots or scheduled jobs. The fix credits them by name: their login, or the name on their commits.

## Step 3: compare with the previous run

If Step 1 found a previous run, write a short list of what changed since it: the commit (old → new, with what merged, in a few words), each question whose status moved (old → new, and why in one clause), the fixes that landed, the failing or flagged questions that are unchanged, a change of recommended action or feature call (old → new, and why), work-before items that are now done, similar repos that are new to the list, and any stargazers who are new since the previous run's Stargazers list (by login). If nothing changed, say so in one item. Leave this out on a first run.

## Step 4: verify, then recommend and pick the verdict

Verify before building the page:
- **Quotes**: start the run's JSON in the working folder Step 5 uses, with only `questions`, in the shape Step 5 gives. Copy [verify_run.py](verify_run.py), which sits beside this file, into that folder, as Step 5 does the template, and run it as `python3 verify_run.py RUN.json REPO-ROOT`, where `REPO-ROOT` is the clone in the workspace, or the local clone's folder when it runs in the shell on the user's computer. Every file quote must appear verbatim, on the line its source names. Fix or replace any that fails.
- **Numbers in your own prose**: list every number or count you wrote in the verdict, findings, fixes, signals and work-before notes ("seven phase notes", "30 links", "three commands"), and recount each one from the source with code, not from memory or the previous run. Rewrite any that don't match, or drop the number if a recount isn't possible.

With the questions settled, decide the recommendation, the feature call and their work-before lists, as set out in The recommendation above.

The verdict names the single most important fix. Take the earliest failing question. If none fails, take the earliest flagged one, passing over a private repo's Findable flag when visibility is its only gap. If that flag is all that's left, the verdict is to make the repo public when the user judges it ready. If everything passes, say so. When the recommendation is make-private or delete, the page isn't worth fixing: the verdict's fix is the first `todo` item before the action, or the action itself ("Leave it private" for a repo that already is), and comes from no question. Write the fix as one direct sentence a reader could act on, then one or two sentences on why it matters most for this repo.

## Step 5: build and publish the scorecard

1. Copy [scorecard-template.html](scorecard-template.html), which sits beside this file, into a working folder outside any cloned repo. Fill the copy as below; don't retype or edit the template.
2. Add the rest of the run to the JSON Step 4 started, so it has this shape:
   - `title`: "Repo review: REPO-NAME"
   - `subject`: what was checked, including the commit or version
   - `link`, `linkText`: the repo URL and its owner/name (omit both for pasted text)
   - `date`: ISO 8601
   - `rerun`: the command that runs this check again, `/github-curator:repo-review` followed by the repo URL, the local clone's folder path or the file path that was checked (leave it out for pasted text)
   - `changes` (only when there was a previous run): `since` (its date and commit) and `items` (the list from Step 3)
   - `recommendation` (repos only): `action` (`keep`, `publish`, `archive`, `make-private` or `delete`), `why` (the one- or two-sentence reason), `signals` (the short facts it rests on), `confirm` (what the user should confirm, only when the evidence points two ways), `caveat` (what the action costs, from the list above; omit for keep), and `before` (for archive, publish and delete): `title` ("Before archiving", "Before publishing" or "Before deleting") and `items`, a list of `{text, status, note}` with `status` `done`, `todo` or `n/a`, and `feature`: `recommended` (`true` or `false`), `why`, `pinned` (`true`, `false`, or `null` when the pins couldn't be read), `pins` (the current pins, as `owner/name` strings, with the source in `pinsSource`), `replace` (the pin it should replace, when all six places are taken; omit otherwise) and, when recommended, `before` with `title` "Before featuring" and `items` as above
   - `similar` (any draft whose subject is clear): `asOf` (ISO 8601 date), `note` (optional, such as a refused search), and `items`, a list of `{name, link, stars, pushed, archived, description, overlap, difference, alive, foundBy, borrow, mention}`, most-starred first, from How each relates: `foundBy` a list of strings (empty for none), `borrow` omitted for none; for a project the README names that isn't on GitHub, give `name`, `link`, `overlap`, `difference` and `mention` only
   - `verdict`: `question` (the number as a string, or an empty string when the fix comes from no question: make-private, delete, or everything passes), `fix`, `why`
   - `questions`: seven objects, in order, each with `short` (the bold label above), `status` (`pass`, `fail` or `flagged`), `question` (the full question text), `finding`, `quotes` (a list of `{text, source}`), and `fix`
   - `outcomes` (repos only): `asOf` (ISO 8601 date), `source` (one line, such as "GitHub API"), `history` (the "Traffic history" page's link, when there is one; omit otherwise), `items` (a list of `{label, value, note}`, with `note` optional, such as "Not available: no push access"), in this order: Stars, Forks, Watchers, Open issues, Open pull requests, Views (14 days), Unique visitors, Clones (14 days), Unique cloners; and `lists` (a list of `{label, entries, empty}` for "Top referrers", "Most-viewed pages", "Stargazers worth a look", "Stargazers", "Forks with commits", "Contributors" and "Waiting on you", each entry a string such as "news.ycombinator.com · 40 views, 31 unique", with an empty list when there are none; `empty` is the line shown in place of an empty list: "None in the last 14 days" for the two traffic lists, "None: no stargazers besides you" for both Stargazers lists when no one else has starred it, "None in the same field" for "Stargazers worth a look" when profiles were read and none is in the field (when no profile could be read, "Not available: " and the reason, such as "Not available: GitHub refused the profile pages"), "Only you" for "Contributors", "None: no fork has commits of its own" for "Forks with commits" when there are forks (when none could be read, "Not available: " and the reason), and "None" for "Forks with commits" with no forks and for "Waiting on you"). A "Stargazers worth a look" entry is "`LOGIN` · the one line from the `stargazers` skill"; a "Stargazers" entry is "DATE STARRED · `LOGIN` · name, company, location (whichever the profile has) · N followers · active DATE (or no recent activity, or activity not available)", with " · profile page summary" at the end of an entry read from the profile page, oldest first, opening with "N earlier stargazers not listed" when only the 30 most recent were read; a "Forks with commits" entry is "`OWNER/REPO` · N commits (on BRANCH, when not only the default) · by NAMES · last DATE · what they change", with " · worth a look: " and the reason when the `forks` skill picked it, most recently pushed first, ending with "N more not read" when the limit of 30 left some out; a "Contributors" entry is "`LOGIN` · N commits · last DATE", or "NAME (no linked account) · N commits · last DATE", most commits first, from `people.py`; a "Waiting on you" entry is "#N issue (or pull request) · `LOGIN` · opened DATE, N days ago · you replied DATE (or no reply from you) · TITLE", oldest first
   - `fixPrompt` (when anything fails or is flagged, or someone is waiting on a reply): a prompt for Claude Code, in the repo's house style, as `header`, `items` and `footer`. The `header` says where the edits go. When the repo's own rules (CLAUDE.md, CONTRIBUTING.md or a working agreement) say how changes land, it follows them. Otherwise, for a public repo or one with commits from anyone besides the user, it names a new branch and says to open a pull request and not merge it; for a private repo only the user commits to, it says to commit on the current branch and not push, so the user reviews the commits before they leave the machine. Either way, the user's own instructions on branching take precedence. The `header` also restates the repo's own rules that matter for the edits, and says to check every statement against the repo and never invent a figure. `items` has one entry per failed or flagged question, `{question, status, text}`, where `text` is a short section: the question's name and location, the finding, the quoted line, the fix, what to verify first, and a Conventional Commits message if the repo uses them. Leave out a private repo's Findable flag when visibility is its only gap. For archive and publish, and for a recommended feature, add one item per `todo` work-before item that a commit can do, with `question` set to the list's title ("Before archiving", "Before featuring") and `status` `before`; the `header` then also says not to do the action itself, since the user does that once the changes have landed. For keep and archive, add one item per Waiting on you entry, with `question` "Waiting on you" and `status` `reply`: its link and title, what it asks, and a draft reply in the repo's house style that answers it, for the user to post; for archive, the drafts are the work of the "Issues and pull requests" item before archiving. When there are any, the `header` says that Claude Code doesn't post replies: they're the user's to post, edit or drop. Steps only the user can take (pinning, releases, unpinning) stay on the scorecard and out of the prompt. For make-private and delete, leave the fix prompt out. Leave `fixPrompt` out too if no items remain. Settings changes go through `gh repo edit`; the prompt never archives, deletes or changes a repo's visibility, and never closes an issue or pull request: each is the user's call, so an item about open issues says what to write in reply and leaves the closing to the user. The `footer` lists the repo's own checks from its CI workflow, link checking, and what the pull request description (or, with no pull request, the closing reply) must report.
   - `timings`: the rows from the log, as set out under Timing, each `{step, seconds, calls, searches}`, with `searches` only when the step made any
   - `footer`: the status definitions in one or two sentences
   Text fields may use `backticks` for code.
3. Append the `Build` line to the log and add `timings` to the JSON, as set out under Timing. Then fill the template: replace `__TITLE__` with the title, and `__DATA__` with the JSON, escaping every `</` as `<\/`. Save the result as `REPO-NAME-scorecard.html`.
4. With `no-publish`, stop here: the saved file is the result. Otherwise, publish it with `publish_files`, titled "Repo review: REPO-NAME", with the icon `checklist`. If Step 1 found an existing scorecard, under either title, republish to it (`get_artifact` gives the `base_version`) instead of creating a new one, so a re-run updates the same page.

## Step 6: reply

Reply in exactly three lines (two when there is no recommendation), and nothing else:
1. The recommendation: the action and whether to feature it, with the reason, in one sentence, and the number of `todo` items before them when there are any.
2. The verdict: the most important fix, in one sentence.
3. The counts, in the form `N pass · N fail · N flagged`, exactly as the script below prints them from the run's JSON (`python3 counts.py RUN.json`). Don't count by hand. If it prints `cannot count` instead, fix the JSON's `questions` and rebuild the page before replying. Step 7 runs the same script on the portfolio page's JSON, and Step 9 on the quick review's.

```python
import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
statuses = ('pass', 'fail', 'flagged')

def counts(name, items):
    got = [s for _, s in items]
    odd = [str(label) for label, s in items if s not in statuses]
    if len(items) != 7 or odd:
        sys.exit(f"cannot count {name}: {len(items)} questions, expected 7; unknown status in: {', '.join(odd) or 'none'}")
    return f"{got.count('pass')} pass · {got.count('fail')} fail · {got.count('flagged')} flagged"

if d.get('quick'):
    names = ['Hook', 'Findable', 'Way in']
    for r in d['repos']:
        qs = r.get('questions') or []
        if [q.get('short') for q in qs] != names or any(q.get('status') not in statuses for q in qs):
            sys.exit(f"cannot count {r.get('name')}: expected Hook, Findable and Way in, in that order, each pass, fail or flagged")
    parts = []
    for i, n in enumerate(names):
        got = [r['questions'][i]['status'] for r in d['repos']]
        parts.append(f"{n} {got.count('pass')} pass · {got.count('fail')} fail · {got.count('flagged')} flagged")
    print(f"{len(d['repos'])} repos; " + '; '.join(parts))
elif d.get('overview'):
    print('; '.join(f"{r['name']}: {r['action']}{' (featured)' if r.get('feature') else ''}, "
                    + counts(r['name'], list(enumerate(r['statuses'], 1))) for r in d['repos']))
else:
    print(counts('the run', [(q.get('short'), q.get('status')) for q in d['questions']]))
```

The artifact card carries the link, so don't repeat it. With `no-publish` there is no card: add a last line with the saved file's full path.
