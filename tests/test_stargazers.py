"""Tests for the most-starred repos in skills/stargazers/SKILL.md (Step 2).

The commands are taken from the skill as it stands and run with a stand-in gh that
checks its arguments and applies the command's own --jq to each page, as gh does
with --paginate. Run: python3 -m unittest discover tests
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "stargazers" / "SKILL.md"


def command(marker):
    """Return the one sh block in the skill that contains the marker, without its list indent."""
    found = [b for b in re.findall(r"```sh\n(.*?)\n\s*```", SKILL.read_text(encoding="utf-8"), re.S) if marker in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing {marker!r} in SKILL.md, found {len(found)}")
    return found[0].strip()


def repo(name, stars, fork=False, description=None):
    return {"full_name": name, "stargazers_count": stars, "fork": fork, "description": description}


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class MostStarredTest(unittest.TestCase):
    def run_command(self, marker, path, pages, **names):
        """Run the skill's command with LOGIN or ORG replaced, against a gh that serves `pages` for `path`."""
        line = command(marker)
        for placeholder, value in names.items():
            line = line.replace(placeholder, value)
        with tempfile.TemporaryDirectory() as bindir:
            files = []
            for i, page in enumerate(pages):
                f = Path(bindir) / f"page{i}.json"
                f.write_text(json.dumps(page))
                files.append(f'"{f}"')
            gh = Path(bindir) / "gh"
            gh.write_text(
                "#!/bin/sh\n"
                f'[ "$1 $2 $3 $4" = "api --paginate {path} --jq" ] || {{ echo "unexpected: $*" >&2; exit 2; }}\n'
                f'for p in {" ".join(files)}; do "{shutil.which("jq")}" -r "$5" "$p" || exit 1; done\n')
            gh.chmod(0o755)
            env = {**os.environ, "PATH": f"{bindir}:/usr/bin:/bin"}
            out = subprocess.run(["sh", "-c", line], env=env, capture_output=True, text=True, check=True)
        return [l.split("\t") for l in out.stdout.splitlines()]

    def test_a_user_s_top_three_come_from_every_page_and_leave_out_forks(self):
        first = [repo(f"someone/r{i:03}", i % 7) for i in range(100)]
        second = [repo("someone/big", 900, description="A popular tool"), repo("someone/forked", 5000, fork=True),
                  repo("someone/mid", 40), repo("someone/small", 8)]
        rows = self.run_command("users/LOGIN/repos", "users/someone/repos?per_page=100&type=owner",
                                [first, second], LOGIN="someone")
        self.assertEqual(rows, [["900", "someone/big", "A popular tool"], ["40", "someone/mid", ""], ["8", "someone/small", ""]])

    def test_stars_sort_as_numbers(self):
        rows = self.run_command("users/LOGIN/repos", "users/someone/repos?per_page=100&type=owner",
                                [[repo("someone/a", 9), repo("someone/b", 10), repo("someone/c", 100), repo("someone/d", 2)]],
                                LOGIN="someone")
        self.assertEqual([r[1] for r in rows], ["someone/c", "someone/b", "someone/a"])

    def test_an_organisation_s_top_three_come_from_every_page(self):
        pages = [[repo(f"someorg/r{i}", i) for i in range(100)], [repo("someorg/flagship", 12000)]]
        rows = self.run_command("orgs/ORG/repos", "orgs/someorg/repos?per_page=100", pages, ORG="someorg")
        self.assertEqual([(r[0], r[1]) for r in rows], [("12000", "someorg/flagship"), ("99", "someorg/r99"), ("98", "someorg/r98")])


if __name__ == "__main__":
    unittest.main()
