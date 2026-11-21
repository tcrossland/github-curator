# Security

github-curator's skills run with the GitHub access of whoever runs them: their own `gh` login in Claude Code, or the repos attached to a claude.ai chat. Before a private repo is published, the review also scans its full history for secrets, and on claude.ai it downloads betterleaks to do so. A problem in any of that is a security problem, for example a skill that:

- copies a secret's value into a scorecard, a fix prompt or a reply;
- sends a secret or a private repo's content anywhere outside the session;
- changes a repo, closes an issue or pull request, or contacts anyone, which the skills rule out;
- runs a download that doesn't match its release's checksums.

## Reporting a vulnerability

Report it privately, through GitHub's [private vulnerability reporting](https://github.com/tcrossland/github-curator/security/advisories/new), not as a public issue. Say which version you ran, from `.claude-plugin/plugin.json` or the top of [CHANGELOG.md](CHANGELOG.md); whether it ran on claude.ai or in Claude Code; the command you gave; and what happened.

Leave out real secrets, other people's details and the names of private repos. If a secret is needed to show the problem, use a made-up one in the same format.

It's a personal project with one author, so reports are answered as time allows, with no set response time. A fix goes into the next release, and the advisory is published with it.

## Supported versions

Only the latest release gets fixes.
