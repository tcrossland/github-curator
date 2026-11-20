"""Every relative link in a file the zip ships must point to a file the zip also holds.

The shipped paths are read from the zip command in scripts/package.sh, so the test
follows what the build actually packs. Run: python3 -m unittest discover tests
"""
import posixpath
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def shipped():
    """Every file the zip holds, as paths relative to the repo root."""
    line = next(l for l in (ROOT / "scripts" / "package.sh").read_text(encoding="utf-8").splitlines() if l.startswith("zip "))
    names = line.split('"$out"', 1)[1].split(" -x ", 1)[0].split()
    files = set()
    for name in names:
        path = ROOT / name
        found = [p for p in path.rglob("*") if p.is_file()] if path.is_dir() else [path]
        files.update(p.relative_to(ROOT).as_posix() for p in found if p.name != ".DS_Store")
    return files


class ShippedLinksTest(unittest.TestCase):
    def test_relative_links_in_shipped_markdown_stay_in_the_zip(self):
        files = shipped()
        self.assertIn("README.md", files)
        bad = []
        for name in sorted(f for f in files if f.endswith(".md")):
            text = (ROOT / name).read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)\s]+)\)", text):
                if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                    continue
                path = posixpath.normpath(posixpath.join(posixpath.dirname(name), target.split("#", 1)[0]))
                if path not in files:
                    bad.append(f"{name}: {target}")
        self.assertEqual(bad, [], "links to files the zip doesn't hold")


if __name__ == "__main__":
    unittest.main()
