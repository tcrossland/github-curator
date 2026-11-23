---
type: regex
pattern: '"question"\s*:\s*"Tone"\s*,\s*"status"\s*:\s*"(?:fail|flagged)"\s*,\s*"text"\s*:\s*"(?:[^"\\]|\\.)*(?:[Mm]aintain|[Ss]tatus|[Ss]upport|[Ee]xperimental|[Ff]inished|Python 3|[Ww]here to)'
---

Tone is failed or flagged with a fix about what users need: whether it's maintained, its status, what it supports or where to get help (The audience, users, in `SKILL.md`). The fix item, not a passing status, carries it.
