---
type: regex
pattern: '"status"\s*:\s*"reply"\s*,\s*"text"\s*:\s*"(?:[^"\\]|\\.)*#12(?:[^"\\]|\\.){40,}'
---

The fix prompt has a draft reply item for issue #12, with at least a sentence after the issue's number (the fix prompt rules, in `SKILL.md`). The `reply` status comes only from the skill.
