---
type: regex
pattern: '"Way in"\s*:\s*"fail"'
---

Way in fails: the README names a licence that no file holds and the API finds none (Step 2, in `SKILL.md`). The case runs three times, so a status that changes between runs on the same input fails it.
