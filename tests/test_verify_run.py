"""Tests for the quote checker embedded in skills/repo-review/SKILL.md (Step 4).

The checker is extracted from the skill as it stands, so these tests check the
code the skill actually tells Claude to run. Run: python3 -m unittest discover tests
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "repo-review" / "SKILL.md"

FILES = {
    "README.md": "# Title\nA hook line.\nSecond line here.\nThird.\n",
    "LICENSE": "MIT License\nCopyright 2026\n",
    ".github/workflows/ci.yml": "name: ci\non: push\n",
    "setup.cfg": "[metadata]\nversion = 1.2\n",
    "docs/my-notes.md": "note\n",
}

# (quote text, source, expected result): "ok", "skipped" or "problem"
CASES = [
    ("A hook line.", "README.md, line 2", "ok"),
    ("A hook line.", "README.md line 2", "ok"),
    ("A hook line.", "README.md:2", "ok"),
    ("Second line here.\nThird.", "README.md, lines 3-4", "ok"),
    ("Second line here.", "README.md, line 3 (working copy)", "ok"),
    ("MIT License", "LICENSE, line 1", "ok"),
    ("version = 1.2", "setup.cfg, line 2", "ok"),
    ("on: push", ".github/workflows/ci.yml, line 2", "ok"),
    ("note", "docs/my-notes.md, line 1", "ok"),
    ("x", "GitHub repo description, read via the API", "skipped"),
    ("x", "pasted text, paragraph 2", "skipped"),
    ("A hook line.", "README.md, line 3", "problem"),
    ("A hook line.", "README.md, line 99", "problem"),
    ("not in the file", "README.md, line 2", "problem"),
    ("x", "CONTRIBUTING.md, line 1", "problem"),
    ("A hook line.", "README.md, line two", "problem"),
]


def extract_checker(skill_text):
    """Return the python code block in the skill that prints the problem count."""
    blocks = [b for b in re.findall(r"```python\n(.*?)\n```", skill_text, re.S) if "'problems:'" in b]
    if len(blocks) != 1:
        raise ValueError(f"expected one quote checker block in SKILL.md, found {len(blocks)}")
    return blocks[0]


def build_run(cases):
    """One question per case, so each output line maps back to its case."""
    return {"questions": [{"short": f"case{i}", "quotes": [{"text": t, "source": s}]} for i, (t, s, _) in enumerate(cases)]}


def classify(line):
    if ": ok (" in line:
        return "ok"
    if "skipped" in line:
        return "skipped"
    return "problem"


def run_checker(checker, files, run):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        root = tmp / "repo"
        for name, text in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        (tmp / "verify_run.py").write_text(checker, encoding="utf-8")
        (tmp / "run.json").write_text(json.dumps(run), encoding="utf-8")
        result = subprocess.run([sys.executable, "-I", str(tmp / "verify_run.py"), str(tmp / "run.json"), str(root)],
                                capture_output=True, text=True, check=True)
        return result.stdout.splitlines()


class VerifyRunTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lines = run_checker(extract_checker(SKILL.read_text(encoding="utf-8")), FILES, build_run(CASES))

    def test_each_case(self):
        by_case = {line.split(":", 1)[0]: line for line in self.lines if line.startswith("case")}
        for i, (text, source, expected) in enumerate(CASES):
            with self.subTest(source=source, text=text):
                self.assertEqual(classify(by_case[f"case{i}"]), expected, by_case[f"case{i}"])

    def test_problem_count(self):
        expected = sum(1 for *_, e in CASES if e == "problem")
        self.assertEqual(self.lines[-1], f"problems: {expected}")


if __name__ == "__main__":
    unittest.main()
