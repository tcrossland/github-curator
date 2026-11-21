---
type: regex
pattern: '"status"\s*:\s*"reply"\s*,\s*"text"\s*:\s*"(?:[^"\\]|\\.)*(?:#|issues/)12(?!\d)(?:[^"\\]|\\.){40,}'
---

The fix prompt has a draft reply item for issue #12, named by its number or its link, with at least a sentence after it (the fix prompt rules, in `SKILL.md`, which ask for the issue's link and title). The `reply` status comes only from the skill.
