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


def run_json(doc, previous=None):
    """Run the counts script on this JSON, and the previous run's when given; return (exit code, stdout, stderr)."""
    with tempfile.TemporaryDirectory() as tmp:
        path, data = Path(tmp) / "counts.py", Path(tmp) / "run.json"
        path.write_text(script(), encoding="utf-8")
        data.write_text(json.dumps(doc), encoding="utf-8")
        args = [sys.executable, "-I", str(path), str(data)]
        if previous is not None:
            (Path(tmp) / "previous.json").write_text(json.dumps(previous), encoding="utf-8")
            args.append(str(Path(tmp) / "previous.json"))
        out = subprocess.run(args, capture_output=True, text=True)
        return out.returncode, out.stdout, out.stderr


def run(questions):
    return run_json({"title": "Repo review: x", "questions": questions})


SHORTS = ["Hook", "Proof", "Getting started", "Signal", "Findable", "Current", "Tone"]


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
        self.assertIn("unknown status in: Getting started", err)


def review(date, action, *statuses):
    return {"title": "Repo review: x", "date": date, "recommendation": {"action": action}, "questions": questions(*statuses)}


class SinceLineTest(unittest.TestCase):
    def test_a_first_run_has_no_since_line(self):
        code, out, _ = run_json(review("2026-11-22", "keep", *["pass"] * 7))
        self.assertEqual((code, out), (0, "7 pass · 0 fail · 0 flagged\n"))

    def test_a_rerun_names_each_status_and_action_that_moved_first(self):
        code, out, _ = run_json(review("2026-11-22", "keep", "pass", "pass", "flagged", *["pass"] * 4),
                                review("2026-11-21T10:00:00Z", "archive", "fail", "pass", "pass", *["pass"] * 4))
        self.assertEqual((code, out), (0, "Since 2026-11-21: Hook fail → pass; Getting started pass → flagged; action archive → keep\n"
                                          "6 pass · 0 fail · 1 flagged\n"))

    def test_a_change_of_audience_comes_first_and_a_run_without_one_used_employers(self):
        now = {**review("2026-11-22", "keep", *["pass"] * 6, "flagged"), "audience": "users"}
        code, out, _ = run_json(now, review("2026-11-21", "keep", *["pass"] * 7))
        self.assertEqual(out.splitlines()[0], "Since 2026-11-21: audience employers → users; Tone pass → flagged")
        same = {**review("2026-11-21", "keep", *["pass"] * 7), "audience": "employers"}
        code, out, _ = run_json(review("2026-11-22", "keep", *["pass"] * 7), same)
        self.assertEqual(out.splitlines()[0], "Since 2026-11-21: no status or action changed")

    def test_a_rerun_with_nothing_moved_says_so(self):
        code, out, _ = run_json(review("2026-11-22", "keep", *["pass"] * 7), review("2026-11-21", "keep", *["pass"] * 7))
        self.assertEqual(out.splitlines()[0], "Since 2026-11-21: no status or action changed")

    def test_old_labels_are_matched_by_order(self):
        old = review("2026-11-20", "keep", *["pass"] * 7)
        for q, name in zip(old["questions"][3:6], ["Defensible", "Context", "Way in"]):
            q["short"] = name
        old["questions"][5]["status"] = "fail"
        code, out, _ = run_json(review("2026-11-22", "keep", *["pass"] * 7), old)
        self.assertEqual(out.splitlines()[0], "Since 2026-11-20: Current fail → pass")

    def test_a_previous_run_it_cannot_read_is_said_not_guessed(self):
        code, out, _ = run_json(review("2026-11-22", "keep", *["pass"] * 7), {"date": "2026-11-01", "questions": []})
        self.assertEqual(out.splitlines()[0], "Since 2026-11-01: the previous run's questions can't be compared")

    def test_a_run_it_cannot_count_prints_nothing(self):
        code, out, err = run_json(review("2026-11-22", "keep", *["pass"] * 6), review("2026-11-21", "keep", *["pass"] * 7))
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")


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

    def test_quick_counts_each_question_across_repos(self):
        def q(*st):
            return [{"short": n, "status": x} for n, x in zip(["Hook", "Findable", "Getting started"], st)]
        code, out, _ = run_json({"quick": True, "repos": [
            {"name": "o/a", "questions": q("pass", "flagged", "fail")},
            {"name": "o/b", "questions": q("fail", "pass", "fail")},
        ]})
        self.assertEqual((code, out), (0, "2 repos; Hook 1 pass · 1 fail · 0 flagged; "
                                          "Findable 1 pass · 0 fail · 1 flagged; Getting started 0 pass · 2 fail · 0 flagged\n"))

    def test_quick_refuses_a_repo_without_its_three_questions(self):
        code, out, err = run_json({"quick": True, "repos": [
            {"name": "o/a", "questions": [{"short": "Hook", "status": "pass"}, {"short": "Findable", "status": "pass"}]},
        ]})
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("cannot count o/a", err)

    def test_quick_refuses_an_unknown_status(self):
        code, _, err = run_json({"quick": True, "repos": [
            {"name": "o/a", "questions": [{"short": n, "status": "ok"} for n in ["Hook", "Findable", "Getting started"]]},
        ]})
        self.assertNotEqual(code, 0)
        self.assertIn("cannot count o/a", err)


if __name__ == "__main__":
    unittest.main()
