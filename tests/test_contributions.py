"""Tests for skills/contributions/SKILL.md.

The commands and the grouping script are taken from the skill as it stands. The
commands run with a stand-in gh that checks its arguments and applies the command's
own --jq to each page, as gh does with --paginate. Run: python3 -m unittest discover tests
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

SKILL = Path(__file__).resolve().parent.parent / "skills" / "contributions" / "SKILL.md"


def block(lang, marker):
    found = [b for b in re.findall(rf"```{lang}\n(.*?)\n\s*```", SKILL.read_text(encoding="utf-8"), re.S) if marker in b]
    if len(found) != 1:
        raise ValueError(f"expected one {lang} block containing {marker!r} in SKILL.md, found {len(found)}")
    return found[0]


def line(marker):
    """The one command line, in any sh block, that contains the marker."""
    found = [l.strip() for b in re.findall(r"```sh\n(.*?)\n\s*```", SKILL.read_text(encoding="utf-8"), re.S)
             for l in b.splitlines() if marker in l]
    if len(found) != 1:
        raise ValueError(f"expected one sh line containing {marker!r} in SKILL.md, found {len(found)}")
    return found[0]


def pr(repo, number, merged, title):
    return {"repository_url": f"https://api.github.com/repos/{repo}", "number": number, "title": title,
            "pull_request": {"merged_at": merged}}


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class CommandTest(unittest.TestCase):
    def run_line(self, command, expected_args, pages, cwd):
        """Run a command against a gh that serves `pages` when called with `expected_args` then --jq."""
        with tempfile.TemporaryDirectory() as bindir:
            files = []
            for i, page in enumerate(pages):
                f = Path(bindir) / f"page{i}.json"
                f.write_text(json.dumps(page))
                files.append(f'"{f}"')
            n = len(expected_args.split(" "))
            got = " ".join(f"${i}" for i in range(1, n + 2))
            jq_arg = f"${n + 2}"
            gh = Path(bindir) / "gh"
            gh.write_text(
                "#!/bin/sh\n"
                f'[ "{got}" = "{expected_args} --jq" ] || {{ echo "unexpected: $*" >&2; exit 2; }}\n'
                f'for p in {" ".join(files)}; do "{shutil.which("jq")}" -r "{jq_arg}" "$p" || exit 1; done\n')
            gh.chmod(0o755)
            env = {**os.environ, "PATH": f"{bindir}:/usr/bin:/bin"}
            return subprocess.run(["sh", "-c", command], env=env, cwd=cwd, capture_output=True, text=True, check=True).stdout

    def test_the_public_listing_reads_every_page_into_one_row_per_pull_request(self):
        command = line("is:public").replace("LOGIN", "someone")
        pages = [{"total_count": 3, "items": [pr("acme/tool", 12, "2014-12-10T17:55:53Z", "Fix the parser"),
                                              pr("acme/tool", 15, "2015-01-02T08:00:00Z", "Add a test")]},
                 {"total_count": 3, "items": [pr("other/lib", 3, "2020-05-06T10:00:00Z", "Document\tthe flag")]}]
        with tempfile.TemporaryDirectory() as work:
            self.run_line(command, "api --paginate search/issues?q=author:someone+type:pr+is:merged+-user:someone+is:public&per_page=100",
                          pages, work)
            rows = [l.split("\t") for l in (Path(work) / "public.tsv").read_text().splitlines()]
        self.assertEqual(rows[0], ["acme/tool", "12", "2014-12-10", "Fix the parser"])
        self.assertEqual([r[0] for r in rows], ["acme/tool", "acme/tool", "other/lib"])
        # @tsv escapes a tab inside a title, so each row keeps four fields.
        self.assertEqual(rows[2], ["other/lib", "3", "2020-05-06", "Document\\tthe flag"])

    def test_the_private_listing_writes_its_own_file(self):
        command = line("is:private").replace("LOGIN", "someone")
        with tempfile.TemporaryDirectory() as work:
            self.run_line(command, "api --paginate search/issues?q=author:someone+type:pr+is:merged+-user:someone+is:private&per_page=100",
                          [{"items": [pr("secret/app", 1, "2021-03-04T00:00:00Z", "Bump")]}], work)
            self.assertEqual((Path(work) / "private.tsv").read_text(), "secret/app\t1\t2021-03-04\tBump\n")

    def test_the_total_comes_from_a_search_with_no_visibility_filter(self):
        command = line("per_page=1'").replace("LOGIN", "someone")
        with tempfile.TemporaryDirectory() as work:
            out = self.run_line(command, "api search/issues?q=author:someone+type:pr+is:merged+-user:someone&per_page=1",
                                [{"total_count": 288, "items": []}], work)
        self.assertEqual(out.strip(), "288")

    def test_own_organisations_are_those_the_user_is_an_admin_of(self):
        command = line("user/memberships/orgs")
        pages = [[{"role": "admin", "organization": {"login": "mine"}},
                  {"role": "member", "organization": {"login": "employer"}}],
                 [{"role": "admin", "organization": {"login": "mine-too"}}]]
        with tempfile.TemporaryDirectory() as work:
            out = self.run_line(command, "api --paginate user/memberships/orgs?per_page=100", pages, work)
        self.assertEqual(out.split(), ["mine", "mine-too"])

    def test_repo_search_gives_stars_archived_and_description(self):
        command = line("search/repositories").replace("repo:OWNER/REPO+repo:OWNER/REPO", "repo:acme/tool+repo:other/lib")
        page = {"items": [{"full_name": "acme/tool", "stargazers_count": 12626, "archived": False, "description": "A tool"},
                          {"full_name": "other/lib", "stargazers_count": 3, "archived": True, "description": None}]}
        with tempfile.TemporaryDirectory() as work:
            out = self.run_line(command, "api search/repositories?q=repo:acme/tool+repo:other/lib+fork:true&per_page=100", [page], work)
        self.assertEqual([l.split("\t") for l in out.splitlines()], [["acme/tool", "12626", "false", "A tool"], ["other/lib", "3", "true", ""]])


class GroupTest(unittest.TestCase):
    def group(self, public, private, *args):
        with tempfile.TemporaryDirectory() as work:
            w = Path(work)
            (w / "group.py").write_text(block("python", "employers"), encoding="utf-8")
            (w / "public.tsv").write_text("".join("\t".join(r) + "\n" for r in public), encoding="utf-8")
            (w / "private.tsv").write_text("".join("\t".join(r) + "\n" for r in private), encoding="utf-8")
            out = subprocess.run([sys.executable, "-I", "group.py", "public.tsv", "private.tsv", *args],
                                 cwd=work, capture_output=True, text=True, check=True)
        return json.loads(out.stdout)

    PUBLIC = [
        ("MyOrg/site", "1", "2019-01-01", "Own work"),
        ("Employer/app", "7", "2018-03-01", "Job work"),
        ("Employer/app", "9", "2018-06-01", "More job work"),
        ("acme/tool", "12", "2014-12-10", "Fix the parser"),
        ("acme/tool", "15", "2015-01-02", "Add a test"),
        ("other/lib", "3", "2020-05-06", "Document the flag"),
    ]
    PRIVATE = [("myorg/secret", "2", "2021-01-01", "Own private"), ("employer/vault", "4", "2017-01-01", "Job private"),
               ("stranger/app", "5", "2022-02-02", "Private elsewhere")]

    def test_groups_add_up_and_follow_their_order(self):
        d = self.group(self.PUBLIC, self.PRIVATE, "total=9", "own=myorg", "employers=employer")
        self.assertEqual(d["counts"], {"own": 2, "employers": 3, "private": 1, "others": 3})
        self.assertEqual(d["check"], "ok")
        # An owner spelt in two cases is one group, under the first spelling seen.
        self.assertEqual(d["line"], "9 merged pull requests to repos you don't own: 2 to your organisations (MyOrg), "
                                    "3 to employers (Employer), 3 to other people's projects in 2 repos, 1 to private repos")

    def test_other_people_s_projects_are_one_entry_per_repo_with_dates_and_titles(self):
        d = self.group(self.PUBLIC, self.PRIVATE, "total=9", "own=myorg", "employers=employer")
        tool = d["groups"]["others"][0]
        self.assertEqual((tool["name"], tool["merged"], tool["first"], tool["last"]), ("acme/tool", 2, "2014-12-10", "2015-01-02"))
        self.assertEqual(tool["titles"], ["#12 2014-12-10: Fix the parser", "#15 2015-01-02: Add a test"])
        self.assertEqual([e["name"] for e in d["groups"]["private"]], ["stranger"])
        self.assertEqual(d["groups"]["private"][0]["titles"], [])

    def test_without_employers_their_public_work_counts_as_other_people_s(self):
        d = self.group(self.PUBLIC, self.PRIVATE, "total=9", "own=myorg")
        self.assertEqual(d["counts"], {"own": 2, "employers": 0, "private": 2, "others": 5})
        self.assertIn("0 to employers (none named)", d["line"])

    def test_a_pull_request_listed_twice_counts_once_and_the_check_says_so(self):
        d = self.group(self.PUBLIC + [("acme/tool", "12", "2014-12-10", "Fix the parser")], [], "total=7")
        self.assertEqual(sum(d["counts"].values()), 6)
        self.assertEqual(d["check"], "search total 7, listed 6")


if __name__ == "__main__":
    unittest.main()
