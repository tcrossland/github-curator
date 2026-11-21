"""Tests for skills/traffic: the snapshot script, the repo listings in its SKILL.md, and the page.

The listings are taken from the skill as it stands and run with a stand-in gh that checks
its arguments and applies the command's own --jq to each page, as gh does with --paginate.
The snapshot script runs against a stand-in gh too. Run: python3 -m unittest discover tests
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "skills" / "traffic"
SKILL = DIR / "SKILL.md"
PAGE = DIR / "traffic-page.html"

spec = importlib.util.spec_from_file_location("traffic", DIR / "traffic.py")
traffic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(traffic)


def command(marker):
    """Return the one sh block in the skill that contains the marker, without its list indent."""
    found = [b for b in re.findall(r"```sh\n(.*?)\n\s*```", SKILL.read_text(encoding="utf-8"), re.S) if marker in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing {marker!r} in SKILL.md, found {len(found)}")
    return "\n".join(l.strip() for l in found[0].splitlines())


def daily(start_day, counts):
    """GitHub's daily rows from 2026-11-START_DAY, one per count, each with uniques of half the count."""
    return [{"timestamp": f"2026-11-{start_day + i:02}T00:00:00Z", "count": c, "uniques": c // 2} for i, c in enumerate(counts)]


def raw_repo(name, views, clones, referrers=(), **flags):
    return {"name": name, "fork": flags.get("fork", False), "archived": flags.get("archived", False),
            "stars": flags.get("stars", 0), "forks": flags.get("forks", 0),
            "views": {"count": sum(d["count"] for d in views), "uniques": 0, "daily": views},
            "clones": {"count": sum(d["count"] for d in clones), "uniques": 0, "daily": clones},
            "referrers": list(referrers)}


class DocTest(unittest.TestCase):
    def test_a_repo_keeps_its_span_and_only_the_days_with_traffic(self):
        raw = {"taken": "2026-11-20T17:04:41+00:00", "missing": [],
               "repos": [raw_repo("me/a", daily(5, [0, 4, 0]), daily(5, [0, 0, 2]), stars=3, forks=1,
                                  referrers=[{"referrer": "github.com", "count": 4, "uniques": 2}])]}
        d = traffic.doc(raw)
        self.assertEqual(d["taken"], "2026-11-20T17:04:41+00:00")
        self.assertEqual(d["repos"]["me/a"], {
            "fork": False, "archived": False, "stars": 3, "forks": 1,
            "views": {"from": "2026-11-05", "to": "2026-11-07", "days": {"2026-11-06": [4, 2]}},
            "clones": {"from": "2026-11-05", "to": "2026-11-07", "days": {"2026-11-07": [2, 1]}},
            "referrers": [["github.com", 4, 2]],
        })

    def test_a_repo_with_no_rows_has_no_span(self):
        d = traffic.doc({"taken": "2026-11-20T00:00:00+00:00", "repos": [raw_repo("me/new", [], [])]})
        self.assertEqual(d["repos"]["me/new"]["views"], {"from": None, "to": None, "days": {}})
        self.assertEqual(d["missing"], [])

    def test_a_hand_snapshot_with_no_missing_list_still_converts(self):
        raw = {"taken": "2026-11-20T17:04:41+00:00", "repos": [raw_repo("me/a", daily(5, [1]), daily(5, [0]))]}
        self.assertEqual(traffic.doc(raw)["missing"], [])

    def test_the_id_is_the_utc_time_taken_and_a_valid_path_segment(self):
        self.assertEqual(traffic.doc_id({"taken": "2026-11-20T17:04:41+00:00"}), "2026-11-20T17:04:41Z")
        self.assertEqual(traffic.doc_id({"taken": "2026-11-20T18:04:41+01:00"}), "2026-11-20T17:04:41Z")
        self.assertRegex(traffic.doc_id({"taken": "2026-11-20T17:04:41+00:00"}), r"^[A-Za-z0-9_\-.~:@+]{1,200}$")


class SnapshotTest(unittest.TestCase):
    def test_a_repo_whose_traffic_is_refused_is_missing_and_the_rest_carry_on(self):
        calls = []

        def read(path):
            calls.append(path)
            if path.startswith("repos/me/private-now/"):
                return None, "gh: Resource not accessible by integration (HTTP 403)"
            if path.endswith("/views"):
                return {"count": 1, "uniques": 1, "views": daily(5, [1])}, None
            if path.endswith("/clones"):
                return {"count": 0, "uniques": 0, "clones": daily(5, [0])}, None
            return [{"referrer": "github.com", "count": 1, "uniques": 1}], None

        repos = [{"name": "me/zeta", "fork": False, "archived": False, "stars": 0, "forks": 0},
                 {"name": "me/private-now", "fork": False, "archived": False, "stars": 0, "forks": 0}]
        raw = traffic.snapshot(repos, read=read)
        self.assertEqual([r["name"] for r in raw["repos"]], ["me/zeta"])
        self.assertEqual(raw["missing"], [{"name": "me/private-now", "reason": "gh: Resource not accessible by integration (HTTP 403)"}])
        self.assertEqual(calls, ["repos/me/private-now/traffic/views", "repos/me/zeta/traffic/views",
                                 "repos/me/zeta/traffic/clones", "repos/me/zeta/traffic/popular/referrers"])

    def test_the_repo_list_reads_gh_s_tsv(self):
        repos = traffic.read_repos("me/a\tfalse\ttrue\t14\t2\nnot a repo line\nme/b\ttrue\tfalse\t0\t0\n")
        self.assertEqual(repos, [{"name": "me/a", "fork": False, "archived": True, "stars": 14, "forks": 2},
                                 {"name": "me/b", "fork": True, "archived": False, "stars": 0, "forks": 0}])

    def test_the_script_runs_end_to_end_against_gh(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "views.json").write_text(json.dumps({"count": 3, "uniques": 2, "views": daily(5, [0, 3])}))
            (tmp / "clones.json").write_text(json.dumps({"count": 1, "uniques": 1, "clones": daily(5, [1, 0])}))
            (tmp / "refs.json").write_text("[]")
            gh = tmp / "gh"
            gh.write_text(
                "#!/bin/sh\n"
                '[ "$1" = api ] || exit 2\n'
                'case $2 in\n'
                '  repos/me/gone/*) echo "gh: Not Found (HTTP 404)" >&2; exit 1 ;;\n'
                f'  repos/me/a/traffic/views) cat "{tmp}/views.json" ;;\n'
                f'  repos/me/a/traffic/clones) cat "{tmp}/clones.json" ;;\n'
                f'  repos/me/a/traffic/popular/referrers) cat "{tmp}/refs.json" ;;\n'
                '  *) echo "unexpected: $*" >&2; exit 2 ;;\n'
                'esac\n')
            gh.chmod(0o755)
            (tmp / "repos.tsv").write_text("me/a\tfalse\tfalse\t1\t0\nme/gone\tfalse\tfalse\t0\t0\n")
            env = {**os.environ, "PATH": f"{tmp}:/usr/bin:/bin"}
            script = str(DIR / "traffic.py")
            out = subprocess.run([sys.executable, "-I", script, "snapshot", "repos.tsv", "raw.json"],
                                 cwd=tmp, env=env, capture_output=True, text=True, check=True)
            self.assertEqual(out.stdout.strip(), "1 repos read, 1 not read; 3 views and 1 clones in the days GitHub gave")
            out = subprocess.run([sys.executable, "-I", script, "doc", "raw.json", "doc.json"],
                                 cwd=tmp, env=env, capture_output=True, text=True, check=True)
            doc = json.loads((tmp / "doc.json").read_text())
        self.assertRegex(out.stdout, r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ\t\d+ bytes\t1 repos\n$")
        self.assertEqual(doc["repos"]["me/a"]["views"]["days"], {"2026-11-06": [3, 1]})
        self.assertEqual(doc["missing"], [{"name": "me/gone", "reason": "gh: Not Found (HTTP 404)"}])


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class ListingTest(unittest.TestCase):
    def run_command(self, marker, path, pages, **names):
        line = command(marker)
        for placeholder, value in names.items():
            line = line.replace(placeholder, value)
        with tempfile.TemporaryDirectory() as tmp:
            files = []
            for i, page in enumerate(pages):
                f = Path(tmp) / f"page{i}.json"
                f.write_text(json.dumps(page))
                files.append(f'"{f}"')
            gh = Path(tmp) / "gh"
            gh.write_text(
                "#!/bin/sh\n"
                f'[ "$1 $2 $3 $4" = "api --paginate {path} --jq" ] || {{ echo "unexpected: $*" >&2; exit 2; }}\n'
                f'for p in {" ".join(files)}; do "{shutil.which("jq")}" -r "$5" "$p" || exit 1; done\n')
            gh.chmod(0o755)
            env = {**os.environ, "PATH": f"{tmp}:/usr/bin:/bin"}
            subprocess.run(["sh", "-c", line], cwd=tmp, env=env, capture_output=True, text=True, check=True)
            return traffic.read_repos((Path(tmp) / "repos.tsv").read_text())

    def repo(self, name, fork=False):
        return {"full_name": name, "fork": fork, "archived": False, "stargazers_count": 2, "forks_count": 1}

    def test_claude_code_lists_every_page_of_the_owner_s_public_repos(self):
        pages = [[self.repo(f"me/r{i}") for i in range(100)], [self.repo("me/fork", fork=True)]]
        repos = self.run_command("user/repos", "user/repos?affiliation=owner&visibility=public&per_page=100", pages)
        self.assertEqual(len(repos), 101)
        self.assertEqual(repos[-1], {"name": "me/fork", "fork": True, "archived": False, "stars": 2, "forks": 1})

    def test_claude_ai_searches_for_them_forks_included(self):
        pages = [{"total_count": 2, "items": [self.repo("me/a"), self.repo("me/f", fork=True)]}]
        repos = self.run_command("search/repositories", "search/repositories?q=user:me+is:public+fork:true&per_page=100",
                                 pages, LOGIN="me")
        self.assertEqual([r["name"] for r in repos], ["me/a", "me/f"])


class PageTest(unittest.TestCase):
    def test_the_page_has_a_version_the_skill_compares(self):
        self.assertRegex(PAGE.read_text(encoding="utf-8"), r'<meta name="traffic-page" content="\d+">')

    def test_the_page_reads_the_collection_the_skill_writes(self):
        skill, page = SKILL.read_text(encoding="utf-8"), PAGE.read_text(encoding="utf-8")
        self.assertIn('collection `snapshots`', skill)
        self.assertIn('"path": "snapshots"', skill)
        self.assertIn('db.collection("snapshots")', page)

    @unittest.skipUnless(shutil.which("node"), "node is needed to parse the page's script")
    def test_the_page_s_script_parses(self):
        script = re.search(r"<script>\n(.*?)</script>", PAGE.read_text(encoding="utf-8"), re.S).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "page.js"
            f.write_text(script)
            subprocess.run(["node", "--check", str(f)], check=True, capture_output=True)


if __name__ == "__main__":
    unittest.main()
