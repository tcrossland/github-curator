---
type: regex
pattern: '"name"\s*:\s*"quantfolk/pairs-trading"[^}]*?"difference"\s*:\s*"(?![^"]*(?:README|readme|one line|one-line|reliab|lacks|never checked))[^"]{15,}"'
---

The Difference for quantfolk/pairs-trading says what the user's repo adds, and says nothing about the other repo's README, such as that it is one line (Similar repos, How each relates, in `SKILL.md`). It matches the Difference rather than checking that the words are absent, so a reply without the JSON fails.
