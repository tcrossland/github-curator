"""Tests for skills/forks: the forks listing and the git commands that read each fork's commits.

The listing runs with a stand-in gh that checks its arguments and applies the command's own
--jq to each page, as gh does with --paginate. The git commands run as written against local
repos served over file://, in sh and in zsh. Run: python3 -m unittest discover tests
"""
import json
import re
import shutil
import subprocess
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_git_routes import GIT_ENV, commit, git, new_repo  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent / "skills" / "forks" / "SKILL.md"


def block(marker):
    """The one sh block in the skill that contains the marker."""
    found = [b for b in re.findall(r"```sh\n(.*?)\n```", SKILL.read_text(encoding="utf-8"), re.S) if marker in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing {marker!r} in SKILL.md, found {len(found)}")
    return found[0]


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class ListingTest(unittest.TestCase):
    def fork(self, name, created, pushed, **kw):
        return {"full_name": name, "owner": {"type": kw.get("type", "User")}, "created_at": created,
                "pushed_at": pushed, "stargazers_count": kw.get("stars", 0), "forks_count": kw.get("forks", 0),
                "default_branch": kw.get("branch", "main")}

    def test_lists_every_page_and_marks_the_forks_pushed_to_after_they_were_made(self):
        pages = [[self.fork("alice/r", "2015-06-13T10:00:00Z", "2015-07-11T09:00:00Z", stars=3)],
                 [self.fork("acme/r", "2014-10-20T10:00:00Z", "2014-08-28T10:00:00Z", type="Organization", forks=1, branch="master"),
                  self.fork("bob/r", "2015-09-22T10:00:00Z", "2015-09-22T10:00:05Z")]]
        with tempfile.TemporaryDirectory() as tmp:
            files = []
            for i, page in enumerate(pages):
                f = Path(tmp) / f"page{i}.json"
                f.write_text(json.dumps(page))
                files.append(f'"{f}"')
            gh = Path(tmp) / "gh"
            gh.write_text(
                "#!/bin/sh\n"
                '[ "$1 $2 $3 $4" = "api --paginate repos/me/r/forks?sort=newest&per_page=100 --jq" ] || { echo "unexpected: $*" >&2; exit 2; }\n'
                f'for p in {" ".join(files)}; do "{shutil.which("jq")}" -r "$5" "$p" || exit 1; done\n')
            gh.chmod(0o755)
            env = {**GIT_ENV, "PATH": f"{tmp}:/usr/bin:/bin"}
            subprocess.run(["sh", "-c", block("/forks?").replace("OWNER/REPO", "me/r").replace("REPO", "r")], cwd=tmp, env=env, check=True)
            rows = [l.split("\t") for l in (Path(tmp) / "forks-r.tsv").read_text().splitlines()]
        self.assertEqual(rows, [
            ["alice/r", "User", "main", "2015-06-13", "2015-07-11", "3", "0", "true"],
            ["acme/r", "Organization", "master", "2014-10-20", "2014-08-28", "0", "1", "false"],
            ["bob/r", "User", "main", "2015-09-22", "2015-09-22", "0", "0", "true"],
        ])


@unittest.skipUnless(shutil.which("git"), "git is needed")
class ForkCommitsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.repo = new_repo(self.tmp / "repo", "main")
        for i in range(3):
            commit(self.repo, "lib.txt", f"v{i}\n", f"Commit {i}", author=("Me", "me@me.example"))
        git(self.repo, "clone", "-q", str(self.repo), str(self.tmp / "fork"))
        self.fork = self.tmp / "fork"
        git(self.fork, "config", "uploadpack.allowFilter", "true")
        self.work = self.tmp / "work"
        self.work.mkdir()

    def run_snippets(self, shell="sh", upstream=None):
        script = block("--bare").replace("https://github.com/OWNER/REPO.git", f"file://{self.repo}").replace("REPO", "repo") + " &&\n"
        if upstream:
            script += block("refs/upstream/heads").replace("https://github.com/PARENT-OWNER/PARENT-REPO.git", f"file://{upstream}").replace("REPO", "repo") + " &&\n"
        script += (block("refs/forks/").replace("https://github.com/FORK-OWNER/FORK-REPO.git", f"file://{self.fork}")
                   .replace("FORK-OWNER", "alice").replace("REPO", "repo"))
        out = subprocess.run([shell, "-c", script], cwd=self.work, env=GIT_ENV, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout.splitlines()

    def test_lists_the_fork_s_commits_on_every_branch_without_email_addresses(self):
        commit(self.fork, "lib.txt", "theirs\n", "Fix two-digit years", author=("Alice", "alice@home.example"), date="2025-03-01T10:00:00Z")
        git(self.fork, "switch", "-q", "-c", "grails3")
        commit(self.fork, "lib.txt", "port\n", "Port to Grails 3", author=("Alice", "alice@home.example"), date="2025-03-02T10:00:00Z")
        git(self.fork, "switch", "-q", "main")
        lines = self.run_snippets()
        self.assertEqual(lines[0], "2")
        self.assertEqual([l.split("\t") for l in lines[1:]], [
            ["grails3", "Alice", "2025-03-02", "Port to Grails 3"],
            ["main", "Alice", "2025-03-01", "Fix two-digit years"],
        ])
        self.assertNotIn("@", "\n".join(lines))

    def test_an_untouched_fork_counts_nothing_even_when_the_repo_has_moved_on(self):
        commit(self.repo, "lib.txt", "later\n", "Later", author=("Me", "me@me.example"))
        self.assertEqual(self.run_snippets(), ["0"])

    def test_commits_the_repo_has_since_merged_or_tagged_count_nothing(self):
        commit(self.fork, "lib.txt", "merged\n", "Merged upstream", author=("Alice", "a@x.example"))
        git(self.fork, "switch", "-q", "-c", "old")
        commit(self.fork, "lib.txt", "tagged\n", "Released from a branch since deleted", author=("Alice", "a@x.example"))
        git(self.fork, "switch", "-q", "main")
        git(self.repo, "pull", "-q", "--ff-only", str(self.fork), "main")
        git(self.repo, "fetch", "-q", str(self.fork), "old:old")
        git(self.repo, "tag", "v1.0", "old")
        git(self.repo, "branch", "-q", "-D", "old")
        self.assertEqual(self.run_snippets(), ["0"])

    def test_lists_at_most_20_but_counts_them_all(self):
        for i in range(25):
            commit(self.fork, "lib.txt", f"t{i}\n", f"Theirs {i}", author=("Alice", "a@x.example"))
        lines = self.run_snippets()
        self.assertEqual(lines[0], "25")
        self.assertEqual(len(lines), 21)

    def test_a_clone_left_from_an_earlier_run_is_brought_up_to_date(self):
        self.run_snippets()
        commit(self.repo, "lib.txt", "mine\n", "Mine", author=("Me", "me@me.example"))
        git(self.fork, "pull", "-q", "--no-rebase", str(self.repo), "main")
        commit(self.fork, "lib.txt", "theirs\n", "Theirs", author=("Alice", "a@x.example"))
        self.assertEqual(self.run_snippets()[0], "1")

    @unittest.skipUnless(shutil.which("zsh"), "zsh is needed")
    def test_zsh_runs_it_as_written(self):
        # Claude Code on a Mac runs commands in zsh.
        commit(self.fork, "lib.txt", "theirs\n", "Theirs", author=("Alice", "a@x.example"))
        self.assertEqual(self.run_snippets("zsh")[0], "1")

    def test_when_the_repo_is_a_fork_its_parent_s_later_commits_are_not_the_fork_s_own(self):
        upstream = self.tmp / "upstream"
        git(self.repo, "clone", "-q", str(self.repo), str(upstream))
        git(upstream, "config", "uploadpack.allowFilter", "true")
        commit(upstream, "lib.txt", "upstream\n", "Upstream moves on", author=("Maintainer", "m@up.example"))
        git(self.fork, "pull", "-q", "--no-rebase", str(upstream), "main")
        commit(self.fork, "lib.txt", "theirs\n", "Theirs", author=("Alice", "a@x.example"))
        self.assertEqual(self.run_snippets()[0], "2")
        self.assertEqual(self.run_snippets(upstream=upstream)[0], "1")

    def test_a_fork_that_cannot_be_fetched_fails_the_command(self):
        shutil.rmtree(self.fork)
        script = (block("--bare").replace("https://github.com/OWNER/REPO.git", f"file://{self.repo}").replace("REPO", "repo")
                  + " &&\n" + block("refs/forks/").replace("https://github.com/FORK-OWNER/FORK-REPO.git", f"file://{self.fork}")
                  .replace("FORK-OWNER", "alice").replace("REPO", "repo"))
        out = subprocess.run(["sh", "-c", script], cwd=self.work, env=GIT_ENV, capture_output=True, text=True)
        self.assertNotEqual(out.returncode, 0)
        self.assertEqual(out.stdout, "")


if __name__ == "__main__":
    unittest.main()
