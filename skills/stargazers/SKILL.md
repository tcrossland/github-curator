---
name: "stargazers"
description: "List who starred one of the user's GitHub repos and when, and pick out stargazers whose work is in the same field. Use when the user asks who starred a repo or which stargazers are worth a look."
---

# Stargazers

Find out who starred one of the user's public GitHub repos, and which of them are worth a look because their own work is in the same field. The repo review runs Steps 1 to 3 for its Outcomes panel, so a change to them changes the scorecard too.

The argument is a repo URL or `OWNER/REPO`. With several, take each in turn.

## Rules

- Use only what GitHub shows publicly, through `gh api`. Don't search the web or other sites for a stargazer, and don't record email addresses.
- Never follow, star, message or open an issue for anyone: that's the user's call. If the user asks for one of these, do it only for the people they name.
- Say what someone's profile and repos suggest about their work. Never say they influenced, copied or were influenced by anything.

## Step 1: list the stargazers

First check the repo is public with `gh api repos/OWNER/REPO --jq .private`. If it's private, or the call returns 404, stop and say so in one line: only people with access can star a private repo, so there are no stargazers to list yet.

Then run `gh api -H "Accept: application/vnd.github.star+json" --paginate 'repos/OWNER/REPO/stargazers?per_page=100'` and keep `starred_at` and `user.login` for each. Leave out the user's own star (`gh api user` gives the user's login). A public repo's stargazers are public, so this needs no push access.

## Step 2: read each profile

For each stargazer (the 30 most recent, if there are more), read:

- their public profile with `gh api users/LOGIN`: `name`, `company`, `location`, `bio`, `followers` and `type`;
- the date of their latest public activity with `gh api 'users/LOGIN/events/public?per_page=1'`; none in the last 90 days counts as "no recent activity";
- their three most-starred repos that aren't forks, with `gh api 'users/LOGIN/repos?per_page=100&type=owner'`;
- for an organisation their profile names as its company, that organisation's three most-starred repos, with `gh api 'orgs/ORG/repos?per_page=100'`.

## Step 3: pick the ones worth a look

Pick the stargazers whose bio, repos or organisation are in the same field as the repo. For each, write one line saying why, from what their profile and repos show, such as "maintains a popular NLP annotation library (860 stars) and works at a company in the same field; active 2026-11-18". If none are, say so.

## Step 4: reply

1. **Worth a look**: one line per pick from Step 3, most relevant first, each starting with the login in backticks.
2. **All stargazers**: a table, oldest first, with the date starred, login, what the profile gives of name, company and location, followers, and latest activity. When only the 30 most recent were read, say how many earlier stargazers aren't listed.
3. One line on the pattern, if there is one, such as when most stars came, or that none have come in years.

Don't offer to follow or contact anyone unless the user asks.
