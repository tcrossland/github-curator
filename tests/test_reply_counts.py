"""Tests for the reply counts in skills/repo-review/SKILL.md (Step 6, also run by Step 7).

The script is extracted from the skill as it stands, so these tests check what the
skill tells Claude to run. Run: python3 -m unittest discover tests
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "repo-review" / "SKILL.md"


def script():
    found = [b for b in re.findall(r"```python\n(.*?)\n```", SKILL.read_text(encoding="utf-8"), re.S) if "'flagged'" in b]
    if len(found) != 1:
        raise ValueError(f"expected one python block containing 'flagged' in SKILL.md, found {len(found)}")
    return found[0]


def run_json(doc):
    """Run the counts script on this JSON; return (exit code, stdout, stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        path, data = Path(tmp) / "counts.py", Path(tmp) / "run.json"
        path.write_text(script(), encoding="utf-8")
        data.write_text(json.dumps(doc), encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(path), str(data)], capture_output=True, text=True)
        return out.returncode, out.stdout, out.stderr


def run(questions):
    return run_json({"title": "Repo review: x", "questions": questions})


SHORTS = ["Hook", "Proof", "Way in", "Signal", "Findable", "Current", "Tone"]


def questions(*statuses):
    return [{"short": s, "status": st, "quotes": []} for s, st in zip(SHORTS, statuses)]


class CountsTest(unittest.TestCase):
    def test_counts_each_status(self):
        # The run from the backlog item: the reply said 2 · 0 · 5 where the scorecard had 0 · 5 · 2.
        code, out, _ = run(questions("fail", "fail", "flagged", "fail", "flagged", "fail", "fail"))
        self.assertEqual((code, out), (0, "0 pass · 5 fail · 2 flagged\n"))

    def test_all_pass(self):
        code, out, _ = run(questions(*["pass"] * 7))
        self.assertEqual((code, out), (0, "7 pass · 0 fail · 0 flagged\n"))

    def test_a_missing_question_is_not_counted(self):
        code, out, err = run(questions(*["pass"] * 6))
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("cannot count the run: 6 questions, expected 7", err)

    def test_an_unknown_status_names_its_question(self):
        code, out, err = run(questions("pass", "pass", "Flagged", "pass", "pass", "pass", "pass"))
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("unknown status in: Way in", err)


def repo(name, action, feature, *statuses):
    return {"name": name, "action": action, "feature": feature, "statuses": list(statuses)}


class OverviewCountsTest(unittest.TestCase):
    def test_one_entry_per_repo_with_its_action_and_feature(self):
        code, out, _ = run_json({"overview": True, "repos": [
            repo("o/a", "archive", True, *["pass"] * 7),
            repo("o/b", "keep", False, "fail", "flagged", "pass", "pass", "fail", "pass", "flagged"),
        ]})
        self.assertEqual((code, out), (0, "o/a: archive (featured), 7 pass · 0 fail · 0 flagged; "
                                          "o/b: keep, 3 pass · 2 fail · 2 flagged\n"))

    def test_a_repo_with_a_bad_status_is_named(self):
        code, out, err = run_json({"overview": True, "repos": [
            repo("o/a", "keep", False, *["pass"] * 7),
            repo("o/b", "keep", False, "pass", "pass", "pass", "ok", "pass", "pass", "pass"),
        ]})
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("cannot count o/b: 7 questions, expected 7; unknown status in: 4", err)


if __name__ == "__main__":
    unittest.main()
