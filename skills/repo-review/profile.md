# Step 10: profile review

`repo-review` in profile mode, read only in that mode. The steps and sections it names (Step 1, Step 2, Step 4, Step 5, Step 6, Timing, House style, The previous run, Similar repos, Feature) are in [SKILL.md](SKILL.md), and Step 7 is in [portfolio.md](portfolio.md).

A profile review checks the user's own GitHub profile as a visitor meets it: the bio, the pinned repos and the profile README (the public `LOGIN/LOGIN` repo's `README.md`, which GitHub shows at the top of the profile). It answers three questions, recommends which repos to pin and which to drop, and drafts a profile README and a bio. It runs no full review of its own: the pins come from the feature calls on the user's existing scorecards and portfolio page. It never pins, edits the bio, commits to the profile repo or creates it: each is the user's to do.

It reviews the profile of the account `gh` is signed in as. Other words in the arguments: `employers:OWNER,OWNER` and `orgs:ORG,ORG` go to the `contributions` steps as that skill reads them, and `no-publish` as everywhere else.

**Timing**: log as set out under Timing in `SKILL.md`, in `profile-timings.log`, with the steps `Profile`, `Pages`, `Contributions`, `Questions` (the quote check included), `Draft` and `Build`.

## Profile

Read the login and the profile's own fields, in a working folder outside any clone:

```sh
gh api user --jq '{login, name, bio, company, blog, location, twitter_username}' > user.json
```

`bio`, `name`, `company`, `blog` and `location` are what the profile shows beside the avatar. On claude.ai, `user` answers where `users/LOGIN` is refused. If `bio` comes back missing there, take it from the profile page below, labelled "profile page summary, may not be verbatim", and if neither gives it, say the bio couldn't be read and flag Introduction rather than judging a bio nobody saw.

List the user's repos, public and private, forks included, from repository search, which answers on claude.ai with nothing attached:

```sh
gh api --paginate 'search/repositories?q=user:LOGIN+fork:true&per_page=100' | jq -c '.items[]' > repos.jsonl
```

Read the pinned repos as Step 1 of `SKILL.md` says, with its notice before a WebFetch of the profile page and its labels. When the page is fetched for the pins, ask for the bio too.

Read the profile README with the clone in Similar repos, which checks out the README and nothing else, from `https://github.com/LOGIN/LOGIN.git`. It shows on the profile only when that repo is public and holds `README.md` in its root, so check both: the repo is in `repos.jsonl` with `private` false, and the clone printed `README.md`. A README in `.github/` or `docs/` doesn't show on the profile. When the repo is private, missing or has no root `README.md`, there is no profile README: say which in the subject. Note the clone's commit (`git -C readmes/LOGIN--LOGIN rev-parse --short HEAD`).

Then list the GitHub repos the profile README links to and read each from one search, run in the same folder:

```sh
f="readmes/LOGIN--LOGIN/README.md" &&
grep -oiE 'github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' "$f" | cut -d/ -f2,3 | sed -E 's/\.+$//; s/\.git$//' |
  grep -viE '^(sponsors|orgs|settings|users|user-attachments|features|topics|marketplace|apps|about|pricing|collections|trending|search|login|notifications|account)/' | sort -fu > linked.txt &&
q=$(sed 's/^/repo:/' linked.txt | paste -sd+ -) &&
{ [ -z "$q" ] || gh api "search/repositories?q=$q+fork:true&per_page=100" | jq -c '.items[]'; } > linked.jsonl &&
jq -rn --rawfile names linked.txt --slurpfile found linked.jsonl '
  ($found | map({key: (.full_name | ascii_downcase), value: .}) | from_entries) as $f |
  $names | split("\n")[] | select(length > 0) | . as $n | $f[$n | ascii_downcase] as $r |
  "\($n)\t" + (if $r == null then "not found" elif $r.private then "private" elif $r.archived then "archived" else "public" end)'
```

Each line is a linked repo and what a visitor finds: `public`, `archived`, `private` (a visitor gets a 404) or `not found` (deleted, renamed or never there; a renamed repo's old link still redirects, so open it before calling it broken). Search drops a `repo:` qualifier that names no repo and answers for the rest. With more than 40 linked repos, split them across searches of 40. Check the README's other links when the session can open them, as Facts does in Step 2.

## Pages

The pin ranking comes from full reviews the user has already run, never from a new one.
- **The portfolio page**: look for the newest "Portfolio overview" artifact, as The previous run says, and read its `date`, its `pins` (`recommended`, in order, and `why`) and each repo's `feature` call.
- **Scorecards**: list the user's artifacts and read every "Repo review: NAME" scorecard whose NAME is one of the user's public repos in `repos.jsonl` or a current pin. From each, take its `date`, its `recommendation.action` and `recommendation.feature` (`recommended` and `why`). A scorecard newer than the portfolio page settles that repo's feature call.
- **The previous profile review**: look for "Profile review: LOGIN" and save its JSON as `PREVIOUS.json`, to compare against when the page is built.

In Claude Code the listing can stop at the 50 most recently updated artifacts, as the list at the top of `SKILL.md` says: when a page or scorecard isn't among them, say in the footer that an older one may exist.

## Contributions

Run Steps 1 to 4 of the `contributions` skill under its rules, with the `employers:` and `orgs:` words given. Its Step 5 reply doesn't apply here. From its `others` group, pick at most three projects worth naming on the profile: the most-starred, or those with several merged pull requests over time, said in a few words from the pull requests' titles. Never pick an employer's or a private repo: whether to show an employer's work is the user's call. If the `contributions` skill isn't available, leave contributions out and say so in the footer.

## Questions

Start with this step's progress line, as under Timing. Answer three questions, each with a `status` (`pass`, `fail` or `flagged`, as in The questions), a finding, quotes and a fix, as Step 2 sets out:

1. **Introduction**: would a visitor who has never heard of the user know, from the name, the bio and the opening of the profile README, who they are and what they work on? It passes when the bio or the README's opening says it in plain words. It's flagged when only a list of technologies, figures (stars, followers, years) or labels ("passionate developer") stands in for what they work on, or when the bio couldn't be read. It fails when neither the bio nor a profile README says anything about their work.
2. **Pins**: do the pins show the user's strongest work, by the feature calls of their full reviews? It passes when the pins read in full are the recommended ones (below). It fails when a pin is private or gone, or its latest scorecard says not to feature it. Otherwise it's flagged: the pins differ from the recommended ones, they may be incomplete or couldn't be read, or too few repos have full reviews to rank them.
3. **Facts**: does everything the profile README and bio state match what's live? Every linked repo is public, an archived one isn't described as active, each repo is described as its own description and README say, any figure matches its source now, and every other link resolves when the session can open it. A link to a private or missing repo fails it, as does a figure that no longer matches; the rest is flagged. With no profile README and nothing to check in the bio, it passes, with no quote and the note "nothing to check".

Quote the bio as "GitHub profile bio, read via the API", the README as its path and line ("README.md, line 3"), and pins and feature calls by where they came from ("pinned items, read via GraphQL", "Repo review: NAME, feature call of 2026-11-21"). Write each fix in the profile README's house style, as House style in `SKILL.md` says, and under the rules for the draft below.

**Check the quotes.** Write the page's JSON (below) with its `questions`, copy [verify_run.py](verify_run.py) beside it, and check the README quotes against the clone and the bio quotes against `user.json`:
```sh
python3 verify_run.py PROFILE.json readmes/LOGIN--LOGIN
jq -rn --slurpfile p user.json --slurpfile page PROFILE.json '
  $page[0].questions[] | .short as $s | .quotes[] | select(.source | startswith("GitHub profile bio")) | .text as $t |
  "\($s): " + (if ($p[0].bio // "") | contains($t) then "ok (bio)" else "NOT IN THE BIO" end)'
```
Fix or replace any quote either reports, and recount every number in the findings and fixes from the source with code.

## Draft

**The pins.** Rank as Step 7 does across the user's repos, from Pages:
- A repo is a candidate when its latest feature call is yes and it's public now. One whose call is yes but which is still private goes in `why` as one to pin once published.
- Take the portfolio page's recommended order, and place a repo with a newer yes call by the reasons on its scorecard, saying so.
- Keep a current pin that has no full review, a gist among them, unless six reviewed candidates are clearly stronger; say it wasn't reviewed.
- Drop a pin that is private or gone, or whose latest call is no, with that scorecard's reason in your own words.

Give every current pin and every recommended repo a change, `pin`, `keep` or `drop`, with a reason of one sentence naming the scorecard or page and its date. When no scorecard or portfolio page has feature calls, recommend nothing: say so, keep the current pins as they are, and give `next`.

**The profile README.** Draft one for the profile repo's `README.md`, whether or not there is one now, in its house style, or the user's other READMEs' spelling and voice when it has none. Write it plain, so each line says what the thing is:
- Open with who the user is and what they work on, in a sentence or two in the first person.
- Then one line per recommended pin, linking it, saying what it is from its own description and README opening, never more than they claim.
- Then the contributions picked above, each linking the project and saying what the user did there.
- No list of languages or tools, no figures (stars, followers, counts of anything, years of experience), no stats cards or badges, no labels or slogans ("passionate", "full-stack", "10x"), no emoji. A visitor learns more from what the repos are.
- Start from the current README when there is one: keep its lines that meet these rules, in its own words, and say in `readmeNote` what the draft drops or changes and why.

Recount anything in the draft that could go stale against its source, and make sure every recommended pin is linked.

**The bio.** Suggest a bio of at most 160 characters, the most GitHub accepts, counted with code, under the same rules: what the user works on, in plain words. When the bio passes Introduction already, the suggestion is "No change".

## The profile page

Publish the run from the same template as Step 5 (or save it, with `no-publish`), titled "Profile review: LOGIN", with the icon `checklist`, republishing to the previous one if Pages found it. Its JSON:
- `profile`: `true`
- `title`: "Profile review: LOGIN"; `subject`: what was read ("bio, 6 pins, profile README at COMMIT", or "no profile README: the repo is private"); `link` and `linkText`: `https://github.com/LOGIN` and LOGIN; `date`
- `rerun`: `/github-curator:repo-review profile`, followed by any `employers:` and `orgs:` words given
- `changes` (only when there was a previous profile review): `since` (its date) and `items`: each question whose status moved (old → new, matched by `short`), pins added to or dropped from the recommendation, and whether the draft changed
- `verdict`: as in Step 4 of `SKILL.md`, from these three questions: `question` (the number as a string, or empty when all pass), `fix` and `why`
- `questions`: the three, in order, each `{short, status, question, finding, quotes, fix}` as in Step 5, with `short` `Introduction`, `Pins` and `Facts`
- `pins`: `current` and `source`, as Step 7 gives them; `recommended` (up to six, in the order to pin them); `why` (one or two sentences); `basis` (which pages and scorecards the ranking came from, with their dates); and `changes`, a list of `{name, change, why}` with `change` `pin`, `keep` or `drop`
- `draft`: `readme` (the draft, as Markdown), `readmeNote`, `bio`, `bioNote` (its length, and what it replaces), and `where`: where the draft goes (`README.md` in the root of `LOGIN/LOGIN`), or, with no public profile repo, that GitHub shows a profile README only from a public repo named LOGIN with `README.md` in its root, with `gh repo create LOGIN --public` for the user to run when there's none, or making it public when it's private
- `contributions` (when the `contributions` steps ran): `line` (the counts line as its script printed it), `named` (the projects the draft names, each "`OWNER/REPO` · what the user did"), and `note` (that employers' and private repos' pull requests are left out, and what was left out)
- `next` and `nextNote` (when the ranking lacks full reviews): `/github-curator:repo-review portfolio` followed by the URLs of up to ten of the user's public repos with no scorecard, those not forks and most starred first, and how many more there are
- `timings`: the rows from the log, as set out under Timing
- `footer`: where the bio and pins came from, which pages the ranking used and any older ones that may exist, and that the review only recommends: pinning, the bio and the README are the user's to change

Append the `Build` line, add `timings`, then fill the template as in Step 5.

Reply in three lines: the pins recommendation (what to pin, what to drop, or that nothing could be ranked and why); the verdict's fix; and the counts, exactly as Step 6's script prints them from the page's JSON (`python3 counts.py PROFILE.json`, or with `PREVIOUS.json` too on a re-run, when its first line goes before these three). If it prints `cannot count`, fix the `questions` and rebuild the page first. With `no-publish`, add a last line with the saved file's full path.
