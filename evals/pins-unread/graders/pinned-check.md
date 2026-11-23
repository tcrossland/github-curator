---
type: regex
pattern: '"recommended"\s*:\s*false|"text"\s*:\s*"Pinned[^"]*"\s*,\s*"status"\s*:\s*"check"'
---

When the repo is recommended for featuring, the Pinned item before featuring is `check`, not to do, since nobody knows whether the repo is pinned (Feature, in `SKILL.md`). A call not to feature it has no such item, and passes.
