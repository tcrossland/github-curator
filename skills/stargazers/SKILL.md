---
name: "stargazers"
description: "List who starred one of the user's GitHub repos and when, and pick out stargazers whose work is in the same field. Use when the user asks who starred a repo or which stargazers are worth a look."
argument-hint: "[repo-url | OWNER/REPO …] [since:YYYY-MM-DD] [all]"
---

# Stargazers

Find out who starred one of the user's public GitHub repos, and which of them are worth a look because their own work is in the same field. The repo review runs Steps 1 to 3 for its Outcomes panel, so a change to them changes the scorecard too.

The arguments are repo URLs or `OWNER/REPO` names, taken in turn, and two optional keywords:
- `since:YYYY-MM-DD`: only the stars given on or after that date.
- `all`: read every stargazer's profile in Step 2, not only the 30 most recent. Each profile takes at least four API calls (or a fetch of the profile page, on claude.ai), so when that's more than 100 profiles, say how many before starting.

With no repo given, run over every public repo the user owns that has stars, listed with `gh api --paginate 'user/repos?affiliation=owner&visibility=public&per_page=100' --jq '.[] | select(.stargazers_count > 0) | .full_name'`. On claude.ai that path is refused with HTTP 403; use `gh api --paginate 'search/repositories?q=user:LOGIN+fork:true&per_page=100' --jq '.items[] | select(.stargazers_count > 0) | .full_name'` instead, with the login from `gh api user`. Run Step 1 for each, then treat their stargazers as one list, each star tagged with its repo, for Steps 2 to 4, and read a profile once even when that person starred several of the repos.

## Rules

- Use only what GitHub shows publicly, through `gh api`, or on claude.ai the profile page as Step 2 says. Don't search the web or other sites for a stargazer, and don't record email addresses.
- Never follow, star, message or open an issue for anyone: that's the user's call. If the user asks for one of these, do it only for the people they name.
- Say what someone's profile and repos suggest about their work. Never say they influenced, copied or were influenced by anything.

## Step 1: list the stargazers

On claude.ai, the API answers for a repo only once it's attached: attach each repo first with `add_repo` and `access: "push"` (a review has already attached its repo), asking the user once for permission for all of them and suggesting they switch the chat to Manual mode, so each attach waits for their approval. Don't clone them. If a repo can't be attached, say so in one line and go on to the next.

First read the repo with `gh api repos/OWNER/REPO --jq '{full_name, private, stargazers_count}'`, and use its `full_name` from here on, since the name given may differ in case or be an old one. If the call returns 404, stop and say in one line that the repo doesn't exist or isn't visible to the user. If it's private, stop and say so in one line: only people with access can star a private repo, so there are no stargazers to list yet.

Then run `gh api -H "Accept: application/vnd.github.star+json" --paginate 'repos/OWNER/REPO/stargazers?per_page=100'` and keep `starred_at` and `user.login` for each. Leave out the user's own star (`gh api user` gives the user's login). GitHub lists a repo's stargazers only to its owner: for anyone else's public repo this call returns 404 (and GraphQL's `stargazers` comes back empty), however many stars the repo has. When that happens, stop and say so in one line, with the repo's `stargazers_count`: the count is public, the list isn't. Don't look for the list anywhere else.

With `since:`, keep only the stars from that date on, and say so when none are left.

## Step 2: read each profile

For each stargazer (the 30 most recent, if there are more, unless `all` was given), read:

- their public profile with `gh api users/LOGIN`: `name`, `company`, `location`, `bio`, `followers` and `type`;
- the date of their latest public activity with `gh api 'users/LOGIN/events/public?per_page=1'`; none in the last 90 days counts as "no recent activity";
- their three most-starred repos that aren't forks, each with its stars, name and description. The API can't sort someone's repos by stars, so read every page and sort them here:
  ```sh
  gh api --paginate 'users/LOGIN/repos?per_page=100&type=owner' --jq '.[] | select(.fork | not) | [.stargazers_count, .full_name, .description // ""] | @tsv' | sort -rn | head -3
  ```
- for an organisation their profile names as its company, that organisation's three most-starred repos, the same way:
  ```sh
  gh api --paginate 'orgs/ORG/repos?per_page=100' --jq '.[] | [.stargazers_count, .full_name, .description // ""] | @tsv' | sort -rn | head -3
  ```

On claude.ai, `users/LOGIN` and the paths after it are refused with HTTP 403, as the session is bound to its attached repos. When the first one is refused, read each profile instead from its page, `https://github.com/LOGIN`, with WebFetch, one at a time. Each fetch waits for the user's approval unless the link is already in the conversation, and an unanswered prompt closes on its own, so before the first, tell the user in one line that a prompt to fetch a GitHub page will come for each profile, to approve each, and that when one offers Always allow for this website, choosing it lets the rest through. Wait 10 seconds (`sleep 10`) before each fetch after the first, since GitHub rate-limits pages fetched in quick succession. Fetch each page asking for the name, company, location, bio, followers, and each pinned repo's owner/name, stars and description. A WebFetch result is a summary, not the page, so label what it gives "profile page summary". It doesn't give the latest activity or the most-starred repos, so mark those "Not available"; the pinned repos stand in for the most-starred, and the organisation's repos aren't read. If GitHub refuses a fetch (`RATE_LIMIT_EXCEEDED`), wait 30 seconds (`sleep 30`) and fetch that page once more; if it's refused again, mark that profile "Not available: GitHub refused the page twice" and go on to the next. If three profiles in a row end that way, stop fetching and mark the rest "Not available: GitHub refused further profile fetches". If the prompt is declined or goes unanswered, stop fetching and mark them "Not available: fetching GitHub's pages wasn't approved".

## Step 3: pick the ones worth a look

Pick the stargazers whose bio, repos or organisation are in the same field as the repo they starred. For each, write one line saying why, from what their profile and repos show, such as "maintains a popular NLP annotation library (860 stars) and works at a company in the same field; active 2026-11-18". From a profile page summary, judge by the pinned repos' descriptions and the bio, and say so in the line ("pins two NLP annotation tools, from the profile page summary"). If none are, say so. If no profile could be read, no pick was made: say "Not available" with the reason, never that none are in the same field.

## Step 4: reply

1. **Worth a look**: one line per pick from Step 3, most relevant first, each starting with the login in backticks.
2. **All stargazers**: a table, oldest first, with the date starred, login, what the profile gives of name, company and location, followers, and latest activity, and a column for the repo starred when the list covers more than one. When only the 30 most recent were read, say how many earlier stargazers aren't listed. When the profiles came from their pages, say so under the table, and which of bio, company and location none of them gave.
3. One line on the pattern, if there is one, such as when most stars came, or that none have come in years.

Don't offer to follow or contact anyone unless the user asks.
