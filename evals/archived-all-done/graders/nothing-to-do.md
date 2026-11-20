---
type: regex
pattern: '"before"\s*:\s*\[\s*\{(?:(?!"todo")[^\]])*"status"\s*:\s*"(?:done|n/a)"(?:(?!"todo")[^\]])*\]'
---

No item before archiving is left to do: the reply's `before` list has at least one item, each done or doesn't apply, and none `todo`. It matches the list rather than checking that `todo` is absent, so a reply without the JSON fails instead of passing.
