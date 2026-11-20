"""Tests for the timing log in skills/repo-review/SKILL.md (Timing).

The shell line and the script are extracted from the skill as it stands, so these
tests check what the skill tells Claude to run. Run: python3 -m unittest discover tests
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "repo-review" / "SKILL.md"


def blocks(lang, marker):
    """Return the one code block in the given language that contains the marker."""
    found = [b for b in re.findall(rf"```{lang}\n(.*?)\n```", SKILL.read_text(encoding="utf-8"), re.S) if marker in b]
    if len(found) != 1:
        raise ValueError(f"expected one {lang} block containing {marker!r} in SKILL.md, found {len(found)}")
    return found[0]


def convert(log_text):
    with tempfile.TemporaryDirectory() as tmp:
        script, log = Path(tmp) / "timings.py", Path(tmp) / "run.log"
        script.write_text(blocks("python", "'reset'"), encoding="utf-8")
        log.write_text(log_text, encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(script), str(log)], capture_output=True, text=True, check=True)
        return json.loads(out.stdout)


class ConvertTest(unittest.TestCase):
    def test_rows_take_the_time_and_calls_since_the_line_before(self):
        rows = convert("start\t100\t10\t9000\nGet the draft\t130\t25\t9000\nOutcomes\t230\t65\t9000\n")
        self.assertEqual(rows, [
            {"step": "Get the draft", "seconds": 30, "calls": 15},
            {"step": "Outcomes", "seconds": 100, "calls": 40},
        ])

    def test_calls_are_null_when_the_hourly_window_reset(self):
        rows = convert("start\t100\t4990\t9000\nForks\t400\t12\t12600\n")
        self.assertEqual(rows, [{"step": "Forks", "seconds": 300, "calls": None}])

    def test_resets_a_second_apart_are_one_window(self):
        # Seen on 2026-11-20: two reads in one window gave resets one second apart.
        rows = convert("start\t1795190698\t49\t1795193016\nQuestions\t1795190719\t49\t1795193015\n"
                       "Compare\t1795190740\t52\t1795193016\n")
        self.assertEqual([r["calls"] for r in rows], [0, 3])

    def test_a_read_from_a_later_window_that_did_not_begin_blanks_two_rows(self):
        # The log of a review on 2026-11-20: one read gave used 0 with a reset in a later window,
        # and the next read was back in the earlier one. Only that read's two rows lose their count.
        rows = convert(
            "start\t1795190624\t43\t1795193016\n"
            "Get the draft\t1795190675\t46\t1795193016\n"
            "Outcomes\t1795190680\t49\t1795193016\n"
            "Similar repos\t1795190698\t49\t1795193016\n"
            "Questions\t1795190719\t49\t1795193015\n"
            "Compare\t1795190754\t0\t1795194355\n"
            "Verify and recommend\t1795190755\t49\t1795193016\n"
            "Build\t1795190756\t49\t1795193016\n")
        self.assertEqual([(r["step"], r["calls"]) for r in rows], [
            ("Get the draft", 3), ("Outcomes", 3), ("Similar repos", 0), ("Questions", 0),
            ("Compare", None), ("Verify and recommend", None), ("Build", 0),
        ])

    def test_calls_are_null_when_the_count_falls_within_a_window(self):
        rows = convert("start\t100\t40\t9000\nOutcomes\t160\t12\t9010\n")
        self.assertEqual(rows, [{"step": "Outcomes", "seconds": 60, "calls": None}])

    def test_calls_are_null_when_the_rate_limit_could_not_be_read(self):
        rows = convert("start\t100\t\nowner/a\t160\t\nBuild\t170\t\n")
        self.assertEqual(rows, [
            {"step": "owner/a", "seconds": 60, "calls": None},
            {"step": "Build", "seconds": 10, "calls": None},
        ])

    def test_lines_that_cannot_be_read_are_skipped(self):
        rows = convert("start\t100\t10\t9000\n\nnot a log line\nOutcomes\t160\t20\t9000\n")
        self.assertEqual(rows, [{"step": "Outcomes", "seconds": 60, "calls": 10}])

    def test_an_error_body_in_the_count_field_is_no_count(self):
        rows = convert('start\t100\t10\t9000\nOutcomes\t160\t{"message":"Forbidden"}\n')
        self.assertEqual(rows, [{"step": "Outcomes", "seconds": 60, "calls": None}])

    def test_step_names_may_hold_spaces_and_slashes(self):
        rows = convert("start\t0\t1\t5\nVerify and recommend\t5\t1\t5\ntcrossland/spacy-annotator\t9\t3\t5\n")
        self.assertEqual([r["step"] for r in rows], ["Verify and recommend", "tcrossland/spacy-annotator"])


# What `gh api rate_limit` returns, cut down to the fields the skill reads.
RATE_LIMIT = {"resources": {"core": {"used": 0, "reset": 9000}, "search": {"used": 3, "reset": 60}}}


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class ShellLineTest(unittest.TestCase):
    """Run the skill's printf line with a stand-in gh, and convert what it logs."""

    def run_line(self, name, log, used=None, error=None):
        """Log one line. The stand-in gh applies the line's own --jq to RATE_LIMIT with core.used set to `used`,
        or, given `error`, prints it to stdout and exits 1, as gh does on an HTTP error."""
        line = blocks("sh", "rate_limit").replace("'NAME'", f"'{name}'").replace("LOG", str(log))
        with tempfile.TemporaryDirectory() as bindir:
            sample = Path(bindir) / "rate_limit.json"
            data = json.loads(json.dumps(RATE_LIMIT))
            data["resources"]["core"]["used"] = used
            sample.write_text(json.dumps(data))
            if error is None:
                body = f'[ "$1 $2 $3" = "api rate_limit --jq" ] || exit 2\n"{shutil.which("jq")}" -r "$4" "{sample}"\n'
            else:
                body = f"cat <<'EOF'\n{error}\nEOF\nexit 1\n"
            gh = Path(bindir) / "gh"
            gh.write_text("#!/bin/sh\n" + body)
            gh.chmod(0o755)
            env = {**os.environ, "PATH": f"{bindir}:/usr/bin:/bin"}
            subprocess.run(["sh", "-c", line], env=env, check=True)

    def test_logged_lines_convert(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "run.log"
            self.run_line("start", log, used=7)
            self.run_line("Get the draft", log, used=19)
            rows = convert(log.read_text(encoding="utf-8"))
        self.assertEqual([(r["step"], r["calls"]) for r in rows], [("Get the draft", 12)])
        self.assertGreaterEqual(rows[0]["seconds"], 0)

    def test_a_refused_read_logs_no_error_body(self):
        refusal = '{\n  "message": "This GitHub API path is not available:\tsessions are bound",\n  "status": "403"\n}'
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "run.log"
            self.run_line("start", log, used=7)
            self.run_line("Outcomes", log, error=refusal)
            self.run_line("Build", log, used=9)
            text = log.read_text(encoding="utf-8")
            rows = convert(text)
        self.assertEqual(len(text.splitlines()), 3)
        self.assertNotIn("message", text)
        self.assertEqual([(r["step"], r["calls"]) for r in rows], [("Outcomes", None), ("Build", None)])


if __name__ == "__main__":
    unittest.main()
