---
name: "repo-review"
description: "Review the user's GitHub repo or a README draft: recommend keep, publish, archive, make private or delete, and whether to feature it; check it and publish a scorecard. Modes: overview, triage."
---

# Repo review

The work product is a public GitHub repo, published as a portfolio piece to attract potential employers and collaborators. A great one draws traffic, stars and a community. These usually go wrong by being so niche that few people find them or see why they matter. Use this review on any draft, whoever wrote it: the user, Claude, or both together.

For a repo, the review also recommends what to do with it, whether to feature it on the user's profile, and the work worth doing before each. Not every repo should stay as it is: some are finished and should be archived with a proper account of what they were, some aren't worth showing, some private ones are ready to publish, and a few deserve one of the six pinned places on the user's profile. It also finds similar repos, so the review can say what this one adds and where readers who want a maintained tool should go.

There are three ways to run it:
- **One draft**: the arguments are a repo URL, a local clone's folder, a file, a doc link or pasted text. Run Steps 1 to 6.
- **Overview**: the arguments start with `overview`, optionally followed by repo URLs. Run Steps 1 to 4 for each repo (publishing each repo's scorecard as usual), then Step 7.
- **Triage**: the arguments start with `triage`, optionally followed by filters (`public`, `private`, `own`, `forks`, `archived`). Run Step 8 only: a quick pass over many repos from GitHub's API, without cloning or the seven questions, that sorts out the clear cases and names the repos worth a full review.

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
- **make-private**: work worth keeping for the user but not worth showing, or that shouldn't be public.
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
1. **Secrets and private data**: search the full history, not only the working tree, for keys, tokens, passwords, internal hostnames and personal data (a full clone, not `--depth 1`). Anything ever committed becomes public with the repo.
2. **Licence**: a licence file, and notices for copied files.
3. **Third-party data and models**: every dataset, model weight or other file from an outside source names that source, and its terms allow redistribution; anything whose terms don't, or whose source is unknown, is removed from the history, not only the working tree.
4. **The seven questions**: every fail fixed; publishing is the moment it gets the most attention.
5. **Description and topics**: set before it goes public.

Before deleting:
1. **Nothing of the user's own**: no commits, notes or results that exist only here.
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

## Step 1: get the draft

Accept any of these:
- **Pasted text**: use it as given. Questions 2 and 3 can only be partly checked without the repo, so flag what can't be seen.
- **A file** (attached, or in a connected folder on the user's computer): read it. If it's a README inside a repo folder, also read the files it links to.
- **A GitHub repo or file link**: attach the repo with `add_repo` and `access: "push"` before anything else, so the GitHub API (settings, outcomes, traffic) works. Then clone it with `--depth 1` into a new, empty directory, or fetch and check out the latest default branch if a clone already exists. If push access is refused, fall back to a read-only clone, and take settings from the repo page with WebFetch. A WebFetch result is a summary, not the page, so label any quote taken from it "repo page summary, may not be verbatim".
  Read `README.md`, every file it links to that bears on a claim, the manifest (`pyproject.toml` or equivalent), the CI workflow and the license. Read settings with `gh api repos/OWNER/REPO` (description, topics, visibility, homepage, has_issues, `license`, and for the recommendation `fork`, `archived` and `pushed_at`) and tags with `gh api repos/OWNER/REPO/tags`. For a fork, count the commits it has that its parent doesn't with `gh api 'repos/PARENT-OWNER/PARENT-REPO/compare/PARENT-BRANCH...OWNER:BRANCH' --jq .ahead_by`, taking the parent's name and default branch from `.parent` in the settings and the fork's branch from `default_branch`. For a private repo, clone the full history instead of `--depth 1`, so the secrets check before publishing can read it. GraphQL (`gh repo view --json`) is not available; use REST.
  Read the repos pinned on the user's profile. REST doesn't list them, so take them from the profile page (`https://github.com/OWNER`) with WebFetch, asking for the pinned repositories as `owner/name` (the page shows the owner only for repos owned by someone else, so ask for it from each link's path), and label them "profile page summary, may not be complete". Where `gh api graphql` does work (in the shell on the user's computer), use `gh api graphql -f query='{user(login:"OWNER"){pinnedItems(first:6){nodes{... on Repository{nameWithOwner}}}}}'` instead. If neither works, say the pins couldn't be read and make the feature call without them.
  If `private` is true in that response, check it as set out under Private repos above, and add "private" to the scorecard's `subject`. If `gh api repos/OWNER/REPO` returns 404, the repo either doesn't exist or is private and not shared with this account, and the WebFetch fallback can't see a private repo either. Say so in one line and ask the user for access, a local clone or the pasted README.
- **A local clone** (a folder on the user's computer that holds a `.git` directory): this is the pre-push check, so review the working copy exactly as it is.
  - Work through the device bridge, read only: never check out, fetch, pull, stash, commit or write anything inside the folder. If the folder isn't connected yet, ask for it with `device_request_folder_access`.
  - With `device_bash` in the folder, read the branch (`git rev-parse --abbrev-ref HEAD`), the commit (`git rev-parse --short HEAD`), uncommitted changes (`git status --porcelain`) and the remote (`git remote get-url origin`). Read `README.md`, every file it links to that bears on a claim, the manifest, the CI workflow and the license from the working copy, and check links and anchors on disk.
  - Run the verify script from Step 4 in that shell, from a scratch file outside the connected folders, with the folder as `REPO-ROOT`. If `device_bash` isn't available, stage the README and the files it quotes or links to with `device_stage_files` and run everything in the workspace.
  - Settings and outcomes come from GitHub: if `origin` points to a GitHub repo, attach it with `add_repo` as in the bullet above and read them through the API, including whether the repo is private. They describe what's live, not the working copy, so say so in the Findable finding when the branch isn't the default branch. With no GitHub remote, flag Findable as not checkable and leave the outcomes panel out.
  - In the scorecard's `subject`, say "working copy at PATH, branch BRANCH at commit COMMIT", adding "with uncommitted changes in N files" when `git status` lists any. A quote from a file with uncommitted changes gets "(working copy)" after its line number.
  - Find the previous run by the repo name from `origin` (or the folder name with no remote), so a local check and a GitHub check of the same repo share one scorecard and the Since last check panel compares them.
- **A Google Doc**: use the Google Drive connector if one is connected.
- **A claude.ai artifact or doc**: use `read_artifact`, or the Claude Docs read tool.
- **Anything else**: WebFetch.
- If the draft can't be read, say so in one line and ask the user to paste it. Don't guess at its contents.

Note the commit hash or version you checked. It goes in the scorecard's subject line.

**House style.** Look for the repo's own writing rules: CLAUDE.md, CONTRIBUTING.md, a style guide, or a writing section in the docs. Every replacement line the scorecard suggests, and the whole fix prompt, must follow them (for example British English and no em-dashes), so a fix can be pasted in as it is. If there are none, match the README's own spelling and voice. In every case, when you write new README text:
- Write a sole author's history, motives and lessons in the first person ("I stopped work on it"), not impersonally ("Work stopped"), so the page shows whose work it is. Check `git shortlog -sn` first.
- State an interest or a claim directly ("My interest was in X"), not by contrast with what it wasn't ("less in Y than in X").
- Don't set the repo's dates beside someone else's product in a list or timeline: it reads as a claim of priority or copying. Say once, in a sentence, that one came before the other, then point readers to the other.
- Don't repeat the same noun or opening ("It was a prototype", "It is a prototype") across neighbouring paragraphs.

**The previous run.** Look for this repo's existing scorecard with `list_artifacts` and the query "Repo review: REPO-NAME", or, failing that, "Portfolio repo check: REPO-NAME" (its title before the skill was renamed). If there is one, read it with `read_artifact` and parse the JSON inside `<script type="application/json" id="data">`. Use it only to compare against in Step 3. Never copy its text into this run.

### Outcomes (context only)

When the draft is a GitHub repo, also gather how the repo is doing, to show beside the check. These figures never change a status or the verdict, and get no pass or fail: there is no bar for them.

- **Repo stats**: stars, forks and watchers from `gh api repos/OWNER/REPO` (`stargazers_count`, `forks_count`, `subscribers_count`); open issues by counting every page of `gh api --paginate 'repos/OWNER/REPO/issues?state=open&per_page=100' --jq '.[] | select(has("pull_request") | not) | .number' | wc -l` (the issues endpoint also returns pull requests, which the filter leaves out); and open pull requests with `gh api --paginate 'repos/OWNER/REPO/pulls?state=open&per_page=100' --jq '.[].number' | wc -l`. If `gh api` can't reach the repo, take stars, forks and watchers from the repo page with WebFetch, and mark issues and pull requests "Not available".
- **Traffic** for the last 14 days: `gh api repos/OWNER/REPO/traffic/views`, `.../traffic/clones`, `.../traffic/popular/referrers` and `.../traffic/popular/paths`. Report total views and unique visitors, total clones and unique cloners, and the top three referrers and most-viewed pages. GitHub shows traffic only to accounts with push access; if that was refused in Step 1, show each traffic figure as "Not available" with the reason.
- **Stargazers**: run Steps 1 to 3 of the `stargazers` skill for this repo, under its rules. It lists who starred the repo and when, reads each stargazer's public profile, and picks the ones whose work is in the same field. Its Step 4 reply doesn't apply here: the results go in the two Stargazers lists in Step 5. In this check, never follow, star, message or open an issue for anyone. If the `stargazers` skill isn't available, leave both Stargazers lists out and add an `items` entry labelled "Stargazers", valued "Not available", with the note "stargazers skill not loaded", so the gap shows on the scorecard.
- **Pasted text** with no repo: leave the panel out.
- **A private repo**: leave the panel out and don't list stargazers. Only people with access can star, view or clone it, so the figures say nothing about how it will do once public.
- Note the date the figures were read.

### Similar repos (context only)

Find up to five popular repos that do much the same thing, for any draft whose subject is clear (private repos and pasted drafts included). Like the outcomes, they get no pass or fail.

1. Search by the repo's most specific topics, two at a time: `gh api 'search/repositories?q=topic:A+topic:B&sort=stars&per_page=10'`. Skip generic topics such as a language name.
2. Then search by the words that say what it does, from the description or the README's opening: `gh api 'search/repositories?q=WORD+WORD+in:name,description,topics&sort=stars&per_page=10'`.
3. Read every description before keeping a result: in both kinds of search the most-starred results are often only loosely related. Keep those that do much the same job, leaving out the repo itself and its forks, and leaving out curated lists, course notes and collections unless this repo is one. Order them most-starred first. Record each one's `full_name`, `html_url`, `stargazers_count`, `pushed_at` (date only), `archived` and `description`, and write one line on how it relates to this repo, from its description and README opening.
4. Add any project the README itself names as related or as an alternative, with its link, even when it isn't on GitHub. GitHub search can't find tools hosted elsewhere.

The search API has a tighter rate limit than the rest; if a search is refused, say so in the panel's `note` and use what was found.

Describe each repo from what its own page says. Never say one copied, influenced or was influenced by another, and don't set dates side by side as if they were a race (see House style).

The questions and the recommendation use them:
- **Hook**: does the opening make clear what this repo adds that the popular ones don't?
- **Findable**: do the popular ones use topics or words that this repo lacks?
- **Archive**: the maintained tools that the status and history section points readers to come from this list (those not archived and recently pushed).
- **Feature**: what visitors will compare it with.

## Step 2: run every question

Write every field fresh, from the files as they are now, even when a previous run exists.

For each question, in order:
1. Decide the status.
2. Quote the exact line or lines from the draft that decide it: one or two, copied character for character, each with its source (file and line number, or "GitHub repo description, read via the API", "GitHub repo settings, read via the API (summarised, not a verbatim line)", "pasted text, paragraph N"). If the deciding evidence is that something is missing, quote the nearest relevant line and say in the finding what's absent.
3. Write a one- or two-sentence finding in plain words.
4. Write one concrete fix: an edit the user could make today, ideally the actual replacement line or sentence, in the repo's house style. For a pass, say "No change" and, only if there's one, the event that should prompt a re-check.

Checking facts (question 3) means comparing claims against their sources: every relative link and anchor resolves, versions match the manifest, statuses match tags, releases and each other wherever the page states them twice, and numbers match the report they come from. Checking claims (question 4) means finding the test, report or file that backs each strong claim ("reproducible", "no look-ahead", "every trial counted", "works with no keys") and noting any claim the repo's own docs hedge or contradict. Checking the way in (question 6) includes the licence, since without one nobody else has permission to reuse the code: a repo with no licence file (`license` is null in the API, or no `LICENSE`, `COPYING` or similar in the working copy) fails Way in, as does one whose README or manifest names a licence that no file holds, or whose licence file still has a template's placeholders in its copyright line (such as `[year] [fullname]`; the appendix at the end of the Apache-2.0 text keeps its placeholders on purpose, so they don't count). The fix says to add or complete one and leaves the choice of licence to the user; when the repo is mostly writing rather than code, it says a Creative Commons licence fits that better than a software one. Before suggesting a licence be added, check who else has commits (`gh api --paginate 'repos/OWNER/REPO/contributors?anon=1&per_page=100'`; entries without a login are commits under an unlinked email, so say which names they carry, not the addresses): code that others contributed with no licence can be licensed only with their agreement, so when anyone besides the user has commits, the fix names them and says so. For a fork, its code is under its parent's licence: when the parent has none, the fix says only the parent's owner can license it. Judge a private repo as it would read once public. For pasted text or a file with no repo to read, flag Way in when the licence can't be seen.

## Step 3: compare with the previous run

If Step 1 found a previous run, write a short list of what changed since it: the commit (old → new, with what merged, in a few words), each question whose status moved (old → new, and why in one clause), the fixes that landed, the failing or flagged questions that are unchanged, a change of recommended action or feature call (old → new, and why), work-before items that are now done, similar repos that are new to the list, and any stargazers who are new since the previous run's Stargazers list (by login). If nothing changed, say so in one item. Leave this out on a first run.

## Step 4: verify, then recommend and pick the verdict

Verify before building the page:
- **Quotes**: run the script below on the run's JSON. Every file quote must appear verbatim, on the line its source names. Fix or replace any that fails.
- **Numbers in your own prose**: list every number or count you wrote in the verdict, findings, fixes, signals and work-before notes ("seven phase notes", "30 links", "three commands"), and recount each one from the source with code, not from memory or the previous run. Rewrite any that don't match, or drop the number if a recount isn't possible.

```python
import json, re, sys, os
run, root = sys.argv[1], sys.argv[2]
d = json.load(open(run)); bad = 0
for q in d['questions']:
    for x in q['quotes']:
        src = x['source']
        m = re.match(r'([\w./-]+)(?::(\d+)|,?\s+lines?\s+(\d+))?', src)
        name = m.group(1) if m else ''
        path = os.path.join(root, name)
        if not name or not os.path.isfile(path):
            if '.' in name or '/' in name: print(f"{q['short']}: MISSING FILE {name}"); bad += 1
            else: print(f"{q['short']}: not a file quote, skipped ({src[:40]})")
            continue
        ln = m.group(2) or m.group(3)
        if not ln and re.search(r'\blines?\b', src, re.I):
            print(f"{q['short']}: line number in an unreadable form ({src[:40]})"); bad += 1; continue
        text = open(path, encoding='utf-8').read()
        if x['text'] not in text: print(f"{q['short']}: NOT VERBATIM in {name}"); bad += 1; continue
        if ln:
            ln = int(ln); lines = text.splitlines()
            if ln > len(lines) or (x['text'] not in lines[ln-1] and x['text'].splitlines()[0] not in lines[ln-1]):
                print(f"{q['short']}: not on line {ln} of {name}"); bad += 1; continue
        print(f"{q['short']}: ok ({name}{', line '+str(ln) if ln else ''})")
print('problems:', bad)
```

Run it as `python3 verify_run.py RUN.json REPO-ROOT`, where `REPO-ROOT` is the clone in the workspace, or the local clone's folder when it runs in the shell on the user's computer.

With the questions settled, decide the recommendation, the feature call and their work-before lists, as set out in The recommendation above.

The verdict names the single most important fix. Take the earliest failing question. If none fails, take the earliest flagged one, passing over a private repo's Findable flag when visibility is its only gap. If that flag is all that's left, the verdict is to make the repo public when the user judges it ready. If everything passes, say so. When the recommendation is make-private or delete, the page isn't worth fixing: the verdict's fix is the first `todo` item before the action, or the action itself. Write the fix as one direct sentence a reader could act on, then one or two sentences on why it matters most for this repo.

## Step 5: build and publish the scorecard

1. Copy [scorecard-template.html](scorecard-template.html), which sits beside this file, into a working folder outside any cloned repo. Fill the copy as below; don't retype or edit the template.
2. Write the run as JSON with this shape:
   - `title`: "Repo review: REPO-NAME"
   - `subject`: what was checked, including the commit or version
   - `link`, `linkText`: the repo URL and its owner/name (omit both for pasted text)
   - `date`: ISO 8601
   - `rerun`: the command that runs this check again, `/github-curator:repo-review` followed by the repo URL, the local clone's folder path or the file path that was checked (leave it out for pasted text)
   - `changes` (only when there was a previous run): `since` (its date and commit) and `items` (the list from Step 3)
   - `recommendation` (repos only): `action` (`keep`, `publish`, `archive`, `make-private` or `delete`), `why` (the one- or two-sentence reason), `signals` (the short facts it rests on), `confirm` (what the user should confirm, only when the evidence points two ways), `caveat` (what the action costs, from the list above; omit for keep), and `before` (for archive, publish and delete): `title` ("Before archiving", "Before publishing" or "Before deleting") and `items`, a list of `{text, status, note}` with `status` `done`, `todo` or `n/a`, and `feature`: `recommended` (`true` or `false`), `why`, `pinned` (`true`, `false`, or `null` when the pins couldn't be read), `pins` (the current pins, as `owner/name` strings, with the source in `pinsSource`), `replace` (the pin it should replace, when all six places are taken; omit otherwise) and, when recommended, `before` with `title` "Before featuring" and `items` as above
   - `similar` (any draft whose subject is clear): `asOf` (ISO 8601 date), `note` (optional, such as a refused search), and `items`, a list of `{name, link, stars, pushed, archived, description, relation}`, most-starred first; for a project the README names that isn't on GitHub, give `name`, `link` and `relation` only
   - `verdict`: `question` (the number as a string), `fix`, `why`
   - `questions`: seven objects, in order, each with `short` (the bold label above), `status` (`pass`, `fail` or `flagged`), `question` (the full question text), `finding`, `quotes` (a list of `{text, source}`), and `fix`
   - `outcomes` (repos only): `asOf` (ISO 8601 date), `source` (one line, such as "GitHub API"), `items` (a list of `{label, value, note}`, with `note` optional, such as "Not available: no push access"), in this order: Stars, Forks, Watchers, Open issues, Open pull requests, Views (14 days), Unique visitors, Clones (14 days), Unique cloners; and `lists` (a list of `{label, entries, empty}` for "Top referrers", "Most-viewed pages", "Stargazers worth a look" and "Stargazers", each entry a string such as "news.ycombinator.com · 40 views, 31 unique", with an empty list when there are none; `empty` is the line shown in place of an empty list: "None in the last 14 days" for the two traffic lists, "None in the same field" for "Stargazers worth a look", and "None" for "Stargazers"). A "Stargazers worth a look" entry is "`LOGIN` · the one line from the `stargazers` skill"; a "Stargazers" entry is "DATE STARRED · `LOGIN` · name, company, location (whichever the profile has) · N followers · active DATE (or no recent activity)", oldest first, opening with "N earlier stargazers not listed" when only the 30 most recent were read
   - `fixPrompt` (when anything fails or is flagged): a prompt for Claude Code, in the repo's house style, as `header`, `items` and `footer`. The `header` says where the edits go. When the repo's own rules (CLAUDE.md, CONTRIBUTING.md or a working agreement) say how changes land, it follows them. Otherwise, for a public repo or one with commits from anyone besides the user, it names a new branch and says to open a pull request and not merge it; for a private repo only the user commits to, it says to commit on the current branch and not push, so the user reviews the commits before they leave the machine. Either way, the user's own instructions on branching take precedence. The `header` also restates the repo's own rules that matter for the edits, and says to check every statement against the repo and never invent a figure. `items` has one entry per failed or flagged question, `{question, status, text}`, where `text` is a short section: the question's name and location, the finding, the quoted line, the fix, what to verify first, and a Conventional Commits message if the repo uses them. Leave out a private repo's Findable flag when visibility is its only gap. For archive and publish, and for a recommended feature, add one item per `todo` work-before item that a commit can do, with `question` set to the list's title ("Before archiving", "Before featuring") and `status` `before`; the `header` then also says not to do the action itself, since the user does that once the changes have landed. Steps only the user can take (pinning, releases, unpinning) stay on the scorecard and out of the prompt. For make-private and delete, leave the fix prompt out. Leave `fixPrompt` out too if no items remain. Settings changes go through `gh repo edit`; the prompt never archives, deletes or changes a repo's visibility, and never closes an issue or pull request: each is the user's call, so an item about open issues says what to write in reply and leaves the closing to the user. The `footer` lists the repo's own checks from its CI workflow, link checking, and what the pull request description (or, with no pull request, the closing reply) must report.
   - `footer`: the status definitions in one or two sentences
   Text fields may use `backticks` for code.
3. Fill the template: replace `__TITLE__` with the title, and `__DATA__` with the JSON, escaping every `</` as `<\/`. Save the result as `REPO-NAME-scorecard.html`.
4. Publish it with `publish_files`, titled "Repo review: REPO-NAME", with the icon `checklist`. If Step 1 found an existing scorecard, under either title, republish to it (`get_artifact` gives the `base_version`) instead of creating a new one, so a re-run updates the same page.

## Step 6: reply

Reply in exactly three lines (two when there is no recommendation), and nothing else:
1. The recommendation: the action and whether to feature it, with the reason, in one sentence, and the number of `todo` items before them when there are any.
2. The verdict: the most important fix, in one sentence.
3. The counts, in the form `N pass · N fail · N flagged`.

The artifact card carries the link, so don't repeat it.

## Step 7: overview

An overview runs the full review on every repo, so with more than a handful, run `triage` first and pass the repos it names to `overview`.

For `overview`, use the repo URLs given. If none are given, list the user's repos with `list_repos`, keep the ones the user owns, public and private, forks included, leaving out those already archived, and say in the overview's footer which repos were included and how they were chosen.

After each repo's scorecard is published, publish one more page from the same template, titled "Portfolio overview", with the icon `checklist`. Republish to an existing "Portfolio overview" artifact if `list_artifacts` finds one. Its JSON:
- `overview`: `true`
- `title`: "Portfolio overview"; `subject`: how many repos and which commits; `date`
- `verdict`: `fix` (the repo that needs attention first, and its most important fix) and `why` (one or two sentences). Pick the repo whose earliest failing question comes first; break ties by the most fails.
- `pins`: `current` (the pinned repos and gists now, as `owner/name` strings), `recommended` (up to six, in the order to pin them, chosen across every repo reviewed and the current pins that weren't), `source` (where the current pins came from) and `why` (one or two sentences on what changes and why). Rank the repos whose feature call is yes, and keep a current pin that wasn't reviewed unless something reviewed is clearly stronger.
- `repos`: one object per repo with `name` (owner/name), `link`, `action` (its recommended action), `feature` (`true` or `false`), `todo` (the number of `todo` items before the action and featuring, or 0), `statuses` (the seven statuses in order), `fix` (that repo's verdict fix), `stars`, `views` (14-day views, or "Not available") and `scorecard` (the scorecard's claude.ai URL)
- `footer`: which repos were included and how they were chosen

Reply in three lines: the repo that needs attention first with its fix; the recommended pins, in order; then one `name: ACTION (featured), N pass · N fail · N flagged` entry per repo, with "(featured)" only when its feature call is yes, separated by semicolons.

## Step 8: triage

Triage is a first pass over many repos, from GitHub's API alone. It settles the cases the API makes plain, gives every other repo a provisional action, and names the ones worth a full review. It never clones, runs the seven questions, lists stargazers or searches for similar repos, and, like the rest of this skill, it only recommends.

### Which repos

List the repos the user owns with `gh api --paginate 'user/repos?affiliation=owner&per_page=100'`. If that fails or plainly misses repos, use `list_repos`, and say in the footer which source was used. Then apply the filters given: `public` or `private` (visibility), `own` or `forks`, and `archived` (archived repos are left out unless it's given). With no filters, take every repo that isn't archived. Read the pinned repos as in Step 1.

### Signals

From the listing, for each repo: `private`, `fork`, `archived`, `pushed_at`, `stargazers_count`, `forks_count`, `open_issues_count`, `description`, `topics`, `size`, `default_branch` and `license`. Then:
- **Each fork**: read its parent from `gh api repos/OWNER/REPO` (`.parent`), and count the commits the fork has that its parent doesn't, as in Step 1. Note when the parent is archived, and when there is no parent (it was deleted or the fork was detached: treat the repo as the user's own). When the fork has commits beyond its parent, read who made them from the same compare call (`.commits[] | .author.login, (.commit.author.email | split("@")[1]), .commit.message`; it lists at most 250). Count a commit as possibly the user's when its login is the user's, or when it has no login at all: commits made under an email that isn't linked to the user's account have none, so GitHub's `author=` filter misses them. Record the email domains of those, not the addresses, so the user can recognise a former employer's. When `ahead_by` runs into the thousands, or none of the listed commits look like the user's, the fork's default branch has most likely drifted from the parent's (an old `master` against a newer `main`): say so, and count the user's commits with `gh api --paginate 'repos/OWNER/REPO/commits?author=OWNER&per_page=100' --jq '.[].sha' | wc -l`. Then list the user's pull requests to the parent and whether each was merged: `gh api 'search/issues?q=repo:PARENT-OWNER/PARENT-REPO+author:OWNER+type:pr'` (`.items[] | .title, .state, .pull_request.merged_at`).
- **Each repo of the user's own**: the first lines of its README, from `gh api repos/OWNER/REPO/readme --jq .content | base64 -d | head -20`, and whether it says the project is unmaintained or archived. A 404 means there is no README. When `license` is null, add the signal "no licence"; when its `spdx_id` is `NOASSERTION`, add "licence not recognised by GitHub". A fork's licence is its parent's, so leave it out for forks.

Write each repo's signals as short facts, as in The recommendation.

### Sorting

Give each repo a provisional action from The recommendation, and mark it `clear` or `review`:
- **clear delete**: an empty repo (`size` 0); or a fork with no commits beyond its parent, that nobody else has starred, forked or opened an issue on, and that isn't pinned. Nothing of the user's is lost.
- **likely delete, to review**: a fork whose commits beyond its parent look like the ones the user's merged pull requests already brought upstream. The work survives in the parent, but the full review should confirm nothing else is in the fork.
- **review**: everything else, with the likeliest action and the question the full review has to answer ("does the README say what the changes were for?", "worth publishing?"). When the repo has no licence and the likeliest action is keep, publish or archive, say in the question that one is needed: the full review fails Way in without it, and every checklist before archiving, publishing or featuring asks for one. Triage never settles keep, publish, archive, make-private or feature: each depends on the page and the work, which only the full review reads.

Among the repos to review, put first the ones where the most is at stake: those pinned on the user's profile, private repos that may be worth publishing, and public repos others have starred, forked or opened issues on.

### The triage page

Write the run as JSON and publish it from the same template as Step 5, titled "Repo triage", with the icon `checklist`. Republish to an existing "Repo triage" artifact if `list_artifacts` finds one, and compare with it: name the repos that have gone since (the user acted on them) and any whose provisional action changed. Its JSON:
- `triage`: `true`
- `title`: "Repo triage"; `subject`: how many repos, which filters and the listing's source; `date`
- `changes` (only when there was a previous triage): `since` (its date) and `items`
- `repos`: one object per repo with `name` (owner/name), `link`, `visibility` (`public` or `private`), `kind` (`own` or `fork`), `pinned` (`true` or `false`), `pushed` (date only), `stars`, `signals` (the short facts), `action` (the provisional action), `sure` (`clear` or `review`), `reason` (one sentence) and, for `review`, `question` (what the full review has to answer). List the repos to review in the order above, then the clear ones.
- `commands`: for the clear deletes, one `gh repo delete OWNER/REPO` per repo, without `--yes`, so that each asks the user to confirm; leave it out when there are none. Introduce them in `commandsNote`: deleting needs the `delete_repo` scope (`gh auth refresh -s delete_repo`), a deleted repo can be restored within 90 days unless it's part of a fork network with other repos in it, and the user runs them only if they agree.
- `next`: the command that reviews the first ten repos marked `review`, `/github-curator:repo-review overview` followed by their URLs in the order above, and `nextNote` saying how many are left for later runs
- `footer`: which repos were included and how they were chosen, the pins' source, and that triage reads only the API, so every `review` action is provisional

Never run the commands, and never archive, delete or change the visibility of anything during triage.

Reply in two lines: the counts (`N clear deletes · N to review`, with the provisional actions among those to review, such as `4 likely archive`), then the first three repos to review, with the question for each.
