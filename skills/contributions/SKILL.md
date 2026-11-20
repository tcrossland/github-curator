---
name: "contributions"
description: "List the user's merged pull requests to GitHub repos they don't own, with their own organisations, their employers and other people's projects kept apart. Use when the user asks what they've contributed to other projects, or which contributions are worth showing."
argument-hint: "[employers:OWNER,…] [own:ORG,…]"
---

# Contributions

A merged pull request to someone else's project shows how the user works with others: that project's maintainers reviewed it and took it. List the user's merged pull requests to repos they don't own, and sort them into three groups:
- **the user's own organisations**: their own work, so counted, not listed;
- **employers**: work done for a job, listed apart, since whether to show it is the user's call;
- **other people's projects**: the open-source contributions, one entry per repo.

The arguments are optional keywords:
- `employers:OWNER,OWNER`: the GitHub owners (organisations or users) the user worked for. Also take any the user's instructions or memory name as their employers' GitHub owners.
- `own:ORG,ORG`: more organisations to count as the user's own, beside those found in Step 1.

## Rules

- Use only what GitHub shows through `gh api`. Don't search the web or other sites, and don't record email addresses.
- Never comment on, react to or reopen a pull request, and never contact a maintainer: that's the user's call.
- Say what each pull request did, from its title. Never claim more for it than the title and the repo show.
- A pull request to a private repo is counted, never named: it isn't evidence a visitor can see.

## Step 1: who the user is

Read the user's login with `gh api user --jq .login`. Then their own organisations, the ones they're an admin of:

```sh
gh api --paginate 'user/memberships/orgs?per_page=100' --jq '.[] | select(.role == "admin") | .organization.login'
```

If that's refused (as unscoped paths are in a claude.ai session), take instead the owners, other than the user, of the repos `list_repos` lists, and say in the reply that the organisations came from there and may include an employer's. Add any given with `own:`.

## Step 2: list the merged pull requests

Search gives the user's merged pull requests to repos outside their own account, the public ones and the private ones apart. In a working folder outside any clone, run each of these, with LOGIN replaced, into its own file:

```sh
gh api --paginate 'search/issues?q=author:LOGIN+type:pr+is:merged+-user:LOGIN+is:public&per_page=100' --jq '.items[] | [(.repository_url | split("/")[-2:] | join("/")), .number, .pull_request.merged_at[:10], .title] | @tsv' > public.tsv
gh api --paginate 'search/issues?q=author:LOGIN+type:pr+is:merged+-user:LOGIN+is:private&per_page=100' --jq '.items[] | [(.repository_url | split("/")[-2:] | join("/")), .number, .pull_request.merged_at[:10], .title] | @tsv' > private.tsv
gh api 'search/issues?q=author:LOGIN+type:pr+is:merged+-user:LOGIN&per_page=1' --jq .total_count
```

The last gives the total the groups must add up to. Search returns at most 1,000 results for one query: when either listing's total passes 1,000, run it again for each year, adding `+merged:YYYY-01-01..YYYY-12-31` to the query, and join the files. Search allows 30 requests a minute; if a request is refused for its rate limit, wait a minute and run it again.

## Step 3: sort them into groups

Count with the script below, not by hand: `python3 group.py public.tsv private.tsv total=TOTAL own=ORG,ORG employers=OWNER,OWNER`. A pull request to one of the user's own organisations counts there whatever its visibility; then one to an employer counts as the employer's; then any other private one counts as private; the rest are other people's projects. It prints the counts line and the groups as JSON, and `check` says whether the groups add up to the search's total.

```python
import json, sys

def read(path):
    with open(path, encoding='utf-8') as f:
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 3 and '/' in p[0]:
                yield p[0], p[1], p[2], p[3] if len(p) > 3 else ''

opts = dict(a.split('=', 1) for a in sys.argv[3:] if '=' in a)
names = lambda key: {o.strip().lower() for o in opts.get(key, '').split(',') if o.strip()}
own, employers = names('own'), names('employers')
seen, groups = set(), {'own': {}, 'employers': {}, 'private': {}, 'others': {}}
for visibility, path in (('public', sys.argv[1]), ('private', sys.argv[2])):
    for repo, number, merged, title in read(path):
        if (repo.lower(), number) in seen:
            continue
        seen.add((repo.lower(), number))
        owner = repo.split('/')[0]
        group = ('own' if owner.lower() in own else 'employers' if owner.lower() in employers
                 else 'private' if visibility == 'private' else 'others')
        name = repo if group == 'others' else owner
        entry = groups[group].setdefault(name.lower(), {'name': name, 'merged': 0, 'first': merged, 'last': merged, 'titles': []})
        entry['merged'] += 1
        entry['first'], entry['last'] = min(entry['first'], merged), max(entry['last'], merged)
        if group == 'others':
            entry['titles'].append(f'#{number} {merged}: {title}')

count = {g: sum(e['merged'] for e in groups[g].values()) for g in groups}
listed = sum(count.values())
total = int(opts['total']) if opts.get('total', '').isdigit() else None
names_of = lambda g: ', '.join(sorted((e['name'] for e in groups[g].values()), key=str.lower))
line = (f"{listed} merged pull requests to repos you don't own: "
        f"{count['own']} to your organisations ({names_of('own') or 'none'}), "
        f"{count['employers']} to employers ({names_of('employers') or 'none named'}), "
        f"{count['others']} to other people's projects in {len(groups['others'])} repos, "
        f"{count['private']} to private repos")
check = 'ok' if total == listed else f'search total {total}, listed {listed}'
print(json.dumps({'line': line, 'check': check, 'counts': count,
                  'groups': {g: sorted(groups[g].values(), key=lambda e: (-e['merged'], e['name'].lower())) for g in groups}},
                 indent=1))
```

If `check` isn't `ok`, say so in the reply with both numbers: search can return a pull request twice across pages, or miss one while its index updates. Run Step 2 again once before reporting a gap.

## Step 4: read the repos

For the repos in `others`, read stars, whether each is archived, and its description, with one repository search for up to 40 repos at a time (`fork:true` keeps repos that are forks themselves):

```sh
gh api 'search/repositories?q=repo:OWNER/REPO+repo:OWNER/REPO+fork:true&per_page=100' --jq '.items[] | [.full_name, .stargazers_count, .archived, (.description // "")] | @tsv'
```

A repo that isn't in the results was renamed, moved or deleted since: say "not found" for its stars rather than guessing.

## Step 5: reply

1. The counts line, exactly as the script printed it.
2. **Other people's projects**: a table, most-starred repo first, with the repo, its stars (and "archived" when it is), the number merged, the dates of the first and last, and one line on what they did, from the titles.
3. **Employers**: one line per owner, with the number merged and the years. When no employers were named, say instead which owners outside the user's organisations have the most merged pull requests, and that `employers:OWNER` lists an employer's apart.
4. One line on what stands out, if anything does: a long-running contribution, a widely used project, or none in years.

Don't offer to comment on or follow up any pull request unless the user asks.
