"""Tests for the quote check in skills/repo-review/quick.md (Step 9).

The loop is taken from quick.md by its content (`quotes.json`) and run as it
stands, with the quote checker beside it and a README clone per repo under
readmes/OWNER--REPO, as the clone in Similar repos leaves them.
Run: python3 -m unittest discover tests
"""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills" / "repo-review"


def loop():
    found = [b for b in re.findall(r"```sh\n(.*?)\n```", (SKILLS / "quick.md").read_text(encoding="utf-8"), re.S) if "quotes.json" in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing quotes.json in quick.md, found {len(found)}")
    return found[0]


def question(short, text, source):
    return {"short": short, "status": "pass", "note": "n", "quotes": [{"text": text, "source": source}]}


class QuickQuotesTest(unittest.TestCase):
    def run_loop(self, repos, readmes):
        if not shutil.which("jq"):
            self.skipTest("jq not installed")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, text in readmes.items():
                path = root / "readmes" / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            shutil.copy(SKILLS / "verify_run.py", root / "verify_run.py")
            (root / "QUICK.json").write_text(json.dumps({"quick": True, "repos": repos}), encoding="utf-8")
            out = subprocess.run(["sh", "-c", loop()], cwd=root, capture_output=True, text=True)
            self.assertEqual(out.returncode, 0, out.stderr)
            return out.stdout

    def test_each_repo_is_checked_against_its_own_readme(self):
        out = self.run_loop(
            [
                {"name": "me/alpha", "questions": [question("Hook", "Alpha diffs tables.", "README.md, line 3"),
                                                   question("Findable", "x", "GitHub repo description, read via the search API")]},
                {"name": "me/beta", "questions": [question("Hook", "Beta opens here.", ".github/README.md, line 1"),
                                                  question("Way in", "Alpha diffs tables.", "README.md, line 3")]},
            ],
            {"me--alpha/README.md": "# Alpha\n\nAlpha diffs tables.\n",
             "me--beta/.github/README.md": "Beta opens here.\n"},
        )
        self.assertIn("== me/alpha\nHook: ok (README.md, line 3)\nFindable: not a file quote, skipped", out)
        self.assertIn("== me/beta\nHook: ok (.github/README.md, line 1)\nWay in: MISSING FILE README.md", out)
        self.assertEqual(re.findall(r"problems: (\d+)", out), ["0", "1"])

    def test_a_quote_on_the_wrong_line_is_a_problem(self):
        out = self.run_loop(
            [{"name": "me/alpha", "questions": [question("Hook", "Alpha diffs tables.", "README.md, line 1")]}],
            {"me--alpha/README.md": "# Alpha\n\nAlpha diffs tables.\n"},
        )
        self.assertIn("Hook: not on line 1 of README.md", out)


if __name__ == "__main__":
    unittest.main()
