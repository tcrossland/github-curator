"""Tests for the quote check in skills/repo-review/quick.md (Step 9).

The check is taken from quick.md by its content (`quotes.json`) and run as it
stands, with the quote checker beside it, a README clone per repo under
readmes/OWNER--REPO, as the clone in Similar repos leaves them, and the search
listing in repos.jsonl, one repo a line, which description quotes are checked
against.
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
    def run_loop(self, repos, readmes, listing=(), shell="sh"):
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
            (root / "repos.jsonl").write_text("".join(json.dumps(x) + "\n" for x in listing), encoding="utf-8")
            out = subprocess.run([shell, "-c", loop()], cwd=root, capture_output=True, text=True)
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

    def test_description_quotes_are_checked_against_the_listing(self):
        desc = "GitHub repo description, read via the search API"
        out = self.run_loop(
            [
                {"name": "me/alpha", "questions": [question("Hook", "Diff two CSV files", desc)]},
                {"name": "me/beta", "questions": [question("Findable", "Diff two TSV files", desc)]},
                {"name": "me/gamma", "questions": [question("Hook", "anything", desc)]},
            ],
            {"me--alpha/README.md": "# Alpha\n", "me--beta/README.md": "# Beta\n", "me--gamma/README.md": "# Gamma\n"},
            [{"full_name": "me/alpha", "description": "Diff two CSV files by key column"},
             {"full_name": "me/beta", "description": "Diff two CSV files"},
             {"full_name": "me/gamma", "description": None}],
        )
        self.assertIn("me/alpha Hook: ok (description)", out)
        self.assertIn("me/beta Findable: NOT IN THE DESCRIPTION", out)
        self.assertIn("me/gamma Hook: NOT IN THE DESCRIPTION", out)

    @unittest.skipUnless(shutil.which("zsh"), "zsh is needed")
    def test_zsh_runs_it_as_written(self):
        # Claude Code on a Mac runs commands in zsh.
        out = self.run_loop(
            [{"name": "me/alpha", "questions": [question("Hook", "Alpha diffs tables.", "README.md, line 3"),
                                                question("Findable", "Diff tables", "GitHub repo description, read via the search API")]}],
            {"me--alpha/README.md": "# Alpha\n\nAlpha diffs tables.\n"},
            [{"full_name": "me/alpha", "description": "Diff tables by key"}],
            shell="zsh",
        )
        self.assertIn("== me/alpha\nHook: ok (README.md, line 3)", out)
        self.assertIn("me/alpha Findable: ok (description)", out)

    def test_a_repo_with_nothing_to_quote_passes_the_check(self):
        out = self.run_loop(
            [{"name": "me/dotfiles", "questions": [{"short": "Hook", "status": "fail", "note": "no README or description", "quotes": []}]}],
            {"me--dotfiles/.keep": ""},
            [{"full_name": "me/dotfiles", "description": None}],
        )
        self.assertIn("== me/dotfiles\nproblems: 0", out)
        self.assertNotIn("NOT IN", out)


if __name__ == "__main__":
    unittest.main()
