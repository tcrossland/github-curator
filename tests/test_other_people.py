"""Tests for Contributors and Waiting on you in skills/repo-review/SKILL.md (Outcomes).

The commands and the people.py script are taken from the skill as it stands. The
commands run with a stand-in gh that checks its arguments and applies the command's
own --jq to each page, as gh does with --paginate. Run: python3 -m unittest discover tests
"""
import datetime
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


def line(marker):
    """The one command, in any sh block, that contains the marker, without its list indent."""
    found = [l.strip() for b in re.findall(r"```sh\n(.*?)\n\s*```", SKILL.read_text(encoding="utf-8"), re.S)
             for l in b.splitlines() if marker in l]
    if len(found) != 1:
        raise ValueError(f"expected one sh line containing {marker!r} in SKILL.md, found {len(found)}")
    return found[0]


def inline(marker):
    """The one inline `gh api ...` command in the skill's prose that contains the marker."""
    found = [c for c in re.findall(r"`(gh api [^`]*)`", SKILL.read_text(encoding="utf-8")) if marker in c]
    if len(found) != 1:
        raise ValueError(f"expected one inline command containing {marker!r} in SKILL.md, found {len(found)}")
    return found[0]


def people_script():
    found = [b for b in re.findall(r"```python\n(.*?)\n```", SKILL.read_text(encoding="utf-8"), re.S) if "mine" in b]
    if len(found) != 1:
        raise ValueError(f"expected one python block containing 'mine' in SKILL.md, found {len(found)}")
    return found[0]


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class CommandTest(unittest.TestCase):
    def run_command(self, command, expected_args, pages, cwd):
        with tempfile.TemporaryDirectory() as bindir:
            files = []
            for i, page in enumerate(pages):
                f = Path(bindir) / f"page{i}.json"
                f.write_text(json.dumps(page))
                files.append(f'"{f}"')
            n = len(expected_args.split(" "))
            got = " ".join(f"${i}" for i in range(1, n + 2))
            gh = Path(bindir) / "gh"
            gh.write_text(
                "#!/bin/sh\n"
                f'[ "{got}" = "{expected_args} --jq" ] || {{ echo "unexpected: $*" >&2; exit 2; }}\n'
                f'for p in {" ".join(files)}; do "{shutil.which("jq")}" -r "${n + 2}" "$p" || exit 1; done\n')
            gh.chmod(0o755)
            env = {**os.environ, "PATH": f"{bindir}:/usr/bin:/bin"}
            return subprocess.run(["sh", "-c", command], env=env, cwd=cwd, capture_output=True, text=True, check=True).stdout

    def commits(self, pages):
        command = line("commits?per_page=100").replace("OWNER/REPO", "me/demo")
        with tempfile.TemporaryDirectory() as work:
            self.run_command(command, "api --paginate repos/me/demo/commits?per_page=100", pages, work)
            return (Path(work) / "commits.tsv").read_text()

    @staticmethod
    def commit(login, name, date, message="Change something"):
        return {"author": {"login": login} if login else None,
                "commit": {"author": {"name": name, "email": "x@example.com", "date": date}, "message": message}}

    def test_commits_list_login_name_and_date_never_the_email(self):
        c = self.commit
        text = self.commits([[c("me", "Me Myself", "2024-01-02T10:00:00Z"), c(None, "Me Myself", "2015-03-04T10:00:00Z")],
                             [c("helper", "Helper Person", "2020-06-07T10:00:00Z")]])
        self.assertEqual([l.split("\t") for l in text.splitlines()],
                         [["me", "Me Myself", "2024-01-02"], ["", "Me Myself", "2015-03-04"], ["helper", "Helper Person", "2020-06-07"]])
        self.assertNotIn("example.com", text)

    def test_co_authors_from_trailers_with_their_login_from_a_no_reply_address_never_the_email(self):
        message = ("Add the parser\n\nCo-authored-by: Pair Person <1234+pairp@users.noreply.github.com>\n"
                   "co-authored-by:  Old Friend  <friend@example.org>\n"
                   "Co-Authored-By: Legacy User <legacyu@users.noreply.github.com>")
        text = self.commits([[self.commit("me", "Me Myself", "2024-01-02T10:00:00Z", message)]])
        self.assertEqual([l.split("\t") for l in text.splitlines()],
                         [["me", "Me Myself", "2024-01-02"], ["pairp", "Pair Person", "2024-01-02", "co"],
                          ["", "Old Friend", "2024-01-02", "co"], ["legacyu", "Legacy User", "2024-01-02", "co"]])
        self.assertNotIn("example.org", text)
        self.assertNotIn("noreply", text)

    def test_coding_assistants_and_bots_are_not_co_authors(self):
        message = "\n".join(["Fix it", ""] + [f"Co-authored-by: {t}" for t in [
            "Claude Opus 5.5 <noreply@anthropic.com>", "Cursor Agent <cursoragent@cursor.com>",
            "aider (deepseek/deepseek-v4-flash) <aider@aider.chat>", "Codex <codex@openai.com>",
            "Copilot <223556219+Copilot@users.noreply.github.com>",
            "dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>"]])
        text = self.commits([[self.commit("me", "Me Myself", "2024-01-02T10:00:00Z", message)]])
        self.assertEqual(text.splitlines(), ["me\tMe Myself\t2024-01-02"])

    def test_waiting_on_you_lists_only_other_people_s_issues_and_pull_requests_with_their_age(self):
        command = line("issues?state=open").replace("OWNER/REPO", "me/demo").replace('"OWNER"', '"me"')
        opened = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=40, hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        pages = [[{"number": 3, "user": {"login": "stranger"}, "created_at": opened, "comments": 0, "title": "Crash on start"},
                  {"number": 4, "user": {"login": "me"}, "created_at": opened, "comments": 0, "title": "My own note"},
                  {"number": 5, "user": {"login": "helper"}, "created_at": opened, "comments": 2, "title": "Add a flag",
                   "pull_request": {"url": "x"}}]]
        with tempfile.TemporaryDirectory() as work:
            out = self.run_command(command, "api --paginate repos/me/demo/issues?state=open&per_page=100", pages, work)
        rows = [l.split("\t") for l in out.splitlines()]
        self.assertEqual([(r[0], r[1], r[2]) for r in rows], [("3", "issue", "stranger"), ("5", "pull request", "helper")])
        self.assertEqual({r[4] for r in rows}, {"40"})
        self.assertEqual(rows[0][5:], ["0", "Crash on start"])

    def test_the_user_s_last_reply_is_their_latest_comment(self):
        command = inline("/comments?per_page=100").replace("OWNER/REPO", "me/demo").replace('"OWNER"', '"me"').replace("issues/N", "issues/3")
        pages = [[{"user": {"login": "stranger"}, "created_at": "2024-01-01T00:00:00Z"},
                  {"user": {"login": "me"}, "created_at": "2024-01-05T00:00:00Z"}],
                 [{"user": {"login": "me"}, "created_at": "2024-02-09T00:00:00Z"},
                  {"user": {"login": "stranger"}, "created_at": "2024-03-01T00:00:00Z"}]]
        with tempfile.TemporaryDirectory() as work:
            out = self.run_command(command.split(" | tail")[0], "api --paginate repos/me/demo/issues/3/comments?per_page=100", pages, work)
            last = self.run_command(command, "api --paginate repos/me/demo/issues/3/comments?per_page=100", pages, work)
        self.assertEqual(out.split(), ["2024-01-05", "2024-02-09"])
        self.assertEqual(last.strip(), "2024-02-09")


class PeopleTest(unittest.TestCase):
    def people(self, rows, user):
        with tempfile.TemporaryDirectory() as work:
            w = Path(work)
            (w / "people.py").write_text(people_script(), encoding="utf-8")
            (w / "commits.tsv").write_text("".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")
            out = subprocess.run([sys.executable, "-I", "people.py", "commits.tsv", user], cwd=work,
                                 capture_output=True, text=True, check=True)
        return json.loads(out.stdout)

    def test_unlinked_commits_under_the_user_s_name_are_the_user_s(self):
        d = self.people([("Me", "Me Myself", "2024-01-02"), ("", "me myself", "2015-03-04"), ("", "Me Myself", "2016-01-01")], "me")
        self.assertEqual((d["commits"], d["user"], d["others"]), (3, 3, []))

    def test_others_are_grouped_by_login_or_name_most_commits_first(self):
        d = self.people([("me", "Me Myself", "2024-01-02"),
                         ("helper", "Helper Person", "2020-06-07"), ("Helper", "H. Person", "2021-01-01"),
                         ("", "Old Colleague", "2014-05-05"),
                         ("", "nightly job", "2025-01-01"), ("", "Nightly Job", "2025-02-01"), ("", "nightly job", "2024-12-01")], "me")
        self.assertEqual(d["user"], 1)
        self.assertEqual(d["others"], [
            {"who": "nightly job", "login": False, "commits": 3, "coauthored": 0, "last": "2025-02-01"},
            {"who": "helper", "login": True, "commits": 2, "coauthored": 0, "last": "2021-01-01"},
            {"who": "Old Colleague", "login": False, "commits": 1, "coauthored": 0, "last": "2014-05-05"},
        ])

    def test_a_name_seen_only_without_a_login_is_someone_else(self):
        d = self.people([("me", "Me Myself", "2024-01-02"), ("", "Someone Else", "2019-09-09")], "me")
        self.assertEqual([p["who"] for p in d["others"]], ["Someone Else"])

    def test_co_authored_commits_count_apart_from_the_author_s(self):
        d = self.people([("me", "Me Myself", "2024-01-02"), ("me", "Me Myself", "2024-02-02"),
                         ("pairp", "Pair Person", "2024-01-02", "co"), ("pairp", "Pair Person", "2024-02-02", "co"),
                         ("helper", "Helper Person", "2023-05-05"),
                         ("", "Helper Person", "2024-02-02", "co"), ("", "Old Friend", "2022-01-01", "co"),
                         ("", "Me Myself", "2024-03-03", "co"), ("me", "Me Myself", "2024-03-04", "co")], "me")
        self.assertEqual((d["commits"], d["user"]), (3, 2))
        self.assertEqual(d["others"], [
            {"who": "helper", "login": True, "commits": 1, "coauthored": 1, "last": "2024-02-02"},
            {"who": "pairp", "login": True, "commits": 0, "coauthored": 2, "last": "2024-02-02"},
            {"who": "Old Friend", "login": False, "commits": 0, "coauthored": 1, "last": "2022-01-01"},
        ])


if __name__ == "__main__":
    unittest.main()
