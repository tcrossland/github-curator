---
name: "traffic"
description: "Save a snapshot of the views, clones, stars and referrers of every public GitHub repo the user owns to a page that keeps them beyond GitHub's 14 days, and chart the trend. Use when the user asks to save, track or chart their repos' traffic, or to schedule a weekly snapshot."
argument-hint: "[schedule] [no-publish]"
---

# Traffic

GitHub keeps a repo's views, clones and referrers for 14 days only. This skill saves what GitHub holds now, for every public repo the user owns, forks included, as one document in the database of a page titled "Traffic history", which merges every snapshot saved there and charts them. Run once a week, the page keeps the whole history.

The arguments are optional keywords:
- `schedule`: after saving a snapshot, set up a weekly task that saves the next ones (Step 6). Without it, nothing is scheduled.
- `no-publish`: save the document as a file in the working folder, and neither publish the page nor write to its database.

It only reads GitHub. Never star, follow, comment on or change a repo, and never contact anyone.

**In Claude Code.** The steps name claude.ai's tools. In Claude Code, use these in their place:
- `add_repo`: none needed. Claude Code's `gh` uses the account it's signed in with, which can read every repo's traffic.
- `list_artifacts`, `read_artifact`, `get_artifact` and `publish_files`: the Artifact tool's `list`, `read` and `publish` actions. `list` takes no query, so look for the title among the artifacts it lists, paging on while the listing says more follow. A listing can instead stop at 50, the most it shows, saying that more may exist beyond it. When "Traffic history" isn't among those, the page may still exist, and a second one would split the snapshots between them: ask the user for the page's link, or to confirm there is none, before publishing a new one. When no one can answer, as in a scheduled task, publish nothing and write nothing: keep `doc.json`, and say in the reply where it is and that it can be saved to the page once its link is known. Read an existing artifact before republishing to it, and republish by passing its `url`. `declare_capabilities`: the `capabilities` field of the same `publish`.
- `db_write`: the ArtifactData tool's `set` action, with `file_path`.
- `create_trigger` and `list_triggers`: the scheduled-tasks tools `create_scheduled_task`, whose `cronExpression` is in local time, and `list_scheduled_tasks`.
- With no artifact tool, work as with `no-publish`, and say so in the reply.

Work in the scratchpad, or a working folder of your own. `SKILL_DIR` below is the folder this file is in.

## Step 1: The repos

Find the user's login with `gh api user --jq .login`. Then list their public repos, one line each, into `repos.tsv`:
- In Claude Code:
  ```sh
  gh api --paginate 'user/repos?affiliation=owner&visibility=public&per_page=100' --jq '.[] | [.full_name, .fork, .archived, .stargazers_count, .forks_count] | @tsv' > repos.tsv
  ```
- On claude.ai, where `user/repos` is refused, search, which counts as one search request per 100 repos:
  ```sh
  gh api --paginate 'search/repositories?q=user:LOGIN+is:public+fork:true&per_page=100' --jq '.items[] | [.full_name, .fork, .archived, .stargazers_count, .forks_count] | @tsv' > repos.tsv
  ```

## Step 2: Attach them (claude.ai chat only)

GitHub serves traffic only to someone with push access, so on claude.ai each repo must be attached with `add_repo` and `access: "push"` before Step 3 can read it. In a chat, attach every repo in `repos.tsv` that isn't attached yet, one call each. Don't clone them: `add_repo`'s result asks for a clone, but traffic needs none. A run of a scheduled task can't attach repos: it reads those attached in the chat that created it, and Step 3 lists the rest as not read. Skip this step in Claude Code.

## Step 3: The snapshot

```sh
python3 -I SKILL_DIR/traffic.py snapshot repos.tsv raw.json
python3 -I SKILL_DIR/traffic.py doc raw.json doc.json
```

The first reads three traffic requests per repo, which don't count against the rate limit, and prints how many repos were read and how many weren't, and the views and clones in the days GitHub gave; a repo it couldn't read is kept in the document's `missing` with GitHub's reason. The second writes the page's document and prints its id (the UTC time the snapshot was taken), its size and how many repos it holds. If the size is over 250000 bytes, stop and say so: the database takes documents up to 256 KiB.

With `no-publish`, stop here: `doc.json` is the result.

## Step 4: The page

Look for the page with `list_artifacts` and the query "Traffic history".
- **None**: publish `SKILL_DIR/traffic-page.html` as it is with `publish_files`, titled "Traffic history", with the icon `chart`. Give it a database with `declare_capabilities`, where only its owner writes: `{"db": {"rules": [{"path": "snapshots", "read": "view", "write": "owner"}]}}`.
- **One exists**: read it with `read_artifact`. If its `<meta name="traffic-page" content="N">` is missing or its N is lower than the file's, republish the file to it (`get_artifact` gives the `base_version`), keeping its capabilities. Otherwise leave it.

Never fill the page with data: everything it shows comes from its database.

## Step 5: Save the snapshot

Write `doc.json` to the page's database with `db_write`: collection `snapshots`, the id Step 3 printed, and the file as the document (or its contents as the data, if the tool takes no file). Each snapshot is a new document, so the write never replaces one. If a document with that id already exists, the same snapshot was saved before: say so and stop.

Reply with the page's link, the number of repos read, each repo not read with its reason, and the views and clones Step 3 printed. When repos weren't read on claude.ai because they aren't attached, say that attaching them in a chat and running `schedule` again brings them into the next snapshots.

## Step 6: Schedule (with `schedule` only)

Set up a recurring task that runs this skill once a week, so no day leaves GitHub's 14 days unsaved: `create_trigger` with `cron_expression` `0 6 * * 1` (Mondays, 06:00 UTC), `permission_mode` `auto` if the tool accepts it (its runs needn't stop for approval), and the prompt "Run the github-curator plugin's traffic skill to save this week's snapshot of my public repos' traffic." On claude.ai, the task's runs get the repos attached in this chat, so do it after Step 2. Never create a second task: look for one with `list_triggers` first, and if one exists, say so and stop.

Say in the reply when it runs next, and that the user can change or delete it in claude.ai's scheduled tasks. In Claude Code, say the task runs only while the desktop app is open, and catches up on its next launch.
