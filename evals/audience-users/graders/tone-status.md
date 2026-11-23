---
type: regex
pattern: '"question"\s*:\s*"Tone"\s*,\s*"status"\s*:\s*"(?:fail|flagged)"\s*,\s*"text"\s*:\s*"(?:[^"\\]|\\.)*(?:[Ss]upport|Python 3|[Ww]here to)'
---

Tone is failed or flagged with a fix about what users need: what it supports or where to get help (The audience, users, in `SKILL.md`). The fix item, not a passing status, carries it.
