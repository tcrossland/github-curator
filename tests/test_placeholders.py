"""No SKILL.md may hold text that Claude Code fills with the skill's arguments.

Claude Code replaces `$ARGUMENTS`, `$ARGUMENTS[N]` and `$N` (0-based) in a skill's
SKILL.md with the arguments it was invoked with, code blocks included: an awk
`$0` reached a triage run as the word `triage`. The skills read their arguments as
keywords, so none of these may appear, escaped or not, since a claude.ai run may
not strip the escape. Run: python3 -m unittest discover tests
"""
import re
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills"


class PlaceholderTest(unittest.TestCase):
    def test_no_skill_md_holds_an_argument_placeholder(self):
        bad = []
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            for n, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                for m in re.finditer(r"\$(\d|ARGUMENTS)", text):
                    bad.append(f"{path.parent.name}/SKILL.md:{n}: {text.strip()[:80]}")
        self.assertEqual(bad, [], "Claude Code would replace these with the skill's arguments")

    def test_no_skill_declares_named_arguments(self):
        # A name declared in `arguments` frontmatter becomes a placeholder too, such as awk's `$email`.
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            front = path.read_text(encoding="utf-8").split("---", 2)[1]
            self.assertNotRegex(front, r"(?m)^arguments:", path.parent.name)


if __name__ == "__main__":
    unittest.main()
