# Step 9: quick review

`repo-review` in quick mode, read only in that mode. The steps and sections it names (Step 1, Step 2, Similar repos, Step 6, Timing, The questions, The recommendation) are in [SKILL.md](SKILL.md).

**Timing**: log as set out under Timing in `SKILL.md`, in `quick-timings.log`, with the steps `List repos`, `READMEs`, `Questions` (the quote check included) and `Build`.

A quick review is an at-a-glance pass over one or many repos: it answers the three questions that GitHub's search and each README can settle, Hook, Findable and Way in, and gives each repo a provisional action. It reads no other file, makes no full clone, runs none of the other four questions, gathers no outcomes, searches for no similar repos and scans for no secrets, so its calls are provisional, as triage's are, and a full review settles them. It never writes to a repo's own scorecard.

## Which repos

Read the user's login with `gh api user --jq .login`. With repos given, read their listing fields from one search naming them all, `gh api 'search/repositories?q=repo:OWNER/A+repo:OWNER/B+fork:true&per_page=100' | jq -c '.items[]' > repos.jsonl`, with up to 40 `repo:` qualifiers per search. With none, take every repo the user owns that isn't a fork or archived, from `gh api --paginate 'search/repositories?q=user:OWNER+archived:false&per_page=100' | jq -c '.items[]' > repos.jsonl`, which leaves forks out and includes private repos; forks are triage's to sort. Either way the listing goes in `repos.jsonl` in the working folder, one repo a line, since the quote check reads descriptions from it. Repository search answers on claude.ai with nothing attached. Leave out, and name in the footer, an empty repo (`size` 0) and, unless named, the profile README repo (`OWNER/OWNER`), which is a profile's page rather than a project. Read the pinned repos as in Step 1.

From each result keep `full_name`, `html_url`, `private`, `pushed_at`, `stargazers_count`, `forks_count`, `open_issues_count`, `description`, `topics` and `license`.

**The previous quick review.** Look for the previous page, titled "Quick review", now, and read its `repos`, to compare with when the page is built.

## READMEs

Read each repo's README with the clone in Similar repos, which checks out the README and nothing else and prints its path and opening. Then read its headings, and the section that says how to install, run or use it if there is one, from the file the clone checked out. A private repo clones as the list at the top of `SKILL.md` says in Claude Code. On claude.ai it clones only once attached: attach the private repos as the Attaching section of [triage.md](triage.md) says (read only that section), and a private repo that isn't attached gets its row from the search result alone, with Hook and Way in flagged, noted "README not read: not attached".

## Questions

For each repo, answer Hook, Findable and Way in as The questions and Step 2 set them out, from the search result and the README alone:
- **Hook**: the repo's name, `description` and the README's opening.
- **Findable**: `description` and `topics`. A description with no topics, or topics with no description, is flagged; neither fails. A private repo's Findable is flagged rather than failed when visibility is its only gap.
- **Way in**: the licence, judged as in Step 2 from `license` (null fails, and so does a README that names a licence while `license` is null; an `spdx_id` of `NOASSERTION` is flagged, since GitHub can't tell what it is), and whether the README says how to install, run or use it. A README that doesn't say how fails Way in whatever the licence, as the full review fails it: the question asks whether the page tells a visitor how. Leave out whether the repo wants contributions, which needs its settings and issues.

A repo with no README and no description has nothing to quote: give those questions no quote, say "no README or description" in the note, and fail Hook and Way in.

For each question give a `status` (`pass`, `fail` or `flagged`), a `note` of a few words naming the evidence ("no topics", "MIT; `pip install` under Install"), and one quote that decides it, copied character for character from the README file or from `repos.jsonl`, never retyped, with its source: the README's path as the clone printed it and its line ("README.md, line 3"), or "GitHub repo description, read via the search API".

Then give each repo:
- `fix`: the most important of its three fixes, the earliest failing question's, else the earliest flagged one's, as one direct sentence a reader could act on, in the README's own spelling and voice; "No change" when all three pass. A suggested description is at most 350 characters, counted with code.
- `action`: a provisional action from The recommendation, from the signals the search gives (`private`, `pushed_at`, stars, forks and open issues), whether the README says the project is unmaintained, and the three statuses; and `question`, what the full review has to answer to settle it. Never settle an action and never make a feature call: both need the questions a quick review doesn't run.

**Check the quotes.** Write the page's JSON (below) in the working folder, copy [verify_run.py](verify_run.py) beside it, and check each repo's quotes: those from a README against its clone, and those from a description against `repos.jsonl`, which the quote checker skips:
```sh
jq -r '.repos[].name' QUICK.json | while IFS= read -r r; do
  jq --arg r "$r" '{questions: [.repos[] | select(.name == $r) | .questions[]]}' QUICK.json > quotes.json &&
  echo "== $r" && python3 verify_run.py quotes.json "readmes/$(printf %s "$r" | sed 's#/#--#')"
done
jq -rn --slurpfile listing repos.jsonl --slurpfile page QUICK.json '
  ($listing | map({key: .full_name, value: (.description // "")}) | from_entries) as $d |
  $page[0].repos[] | .name as $r | .questions[] | .short as $s | .quotes[] |
  select(.source | startswith("GitHub repo description")) | .text as $t |
  "\($r) \($s): " + (if ($d[$r] // "") | contains($t) then "ok (description)" else "NOT IN THE DESCRIPTION" end)'
```
Fix or replace any quote either reports, and recount every number in the fixes and notes from the source with code.

## The quick review page

Publish the run from the same template as Step 5 (or save it, with `no-publish`), titled "Quick review", with the icon `checklist`. Republish to an existing "Quick review" artifact if one was found, and compare with it: name the repos whose statuses or provisional action changed, and those new or gone since. Its JSON:
- `quick`: `true`
- `title`: "Quick review"; `subject`: how many repos and how they were chosen; `date`
- `changes` (only when there was a previous quick review): `since` (its date) and `items`
- `repos`: one object per repo with `name` (owner/name), `link`, `visibility` (`public` or `private`), `pinned` (`true` or `false`), `pushed` (date only), `stars`, `questions` (Hook, Findable and Way in, in that order, each `{short, status, note, quotes}`, with `quotes` a list of `{text, source}`), `fix`, `action` and `question`. Order them by what's at stake: pinned first, then public repos others have starred or forked, then private repos, then the rest; within each, those with the most fails first.
- `next`: the command that reviews in full the first ten repos with a fail or flag whose provisional action isn't make-private or delete, `/github-curator:repo-review portfolio` followed by their URLs in page order, and `nextNote` saying how many are left for later runs; leave both out when every repo passes all three
- `timings`: the rows from the log, as set out under Timing
- `footer`: which repos were included and how they were chosen, any left out as empty, the pins' source, and that a quick review reads only GitHub's search and each README, so every status and action is provisional

Append the `Build` line, add `timings`, then fill the template as in Step 5.

Reply in two lines: the counts, exactly as Step 6's script prints them from the page's JSON (`python3 counts.py QUICK.json`), and the first three repos in page order that have a fix, each with its fix. If the script prints `cannot count`, fix that repo's `questions` and rebuild the page first. With `no-publish`, add a last line with the saved file's full path.
