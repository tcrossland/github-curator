"""Tests for the routes that work on claude.ai as well as in Claude Code.

The git commands in skills/repo-review/SKILL.md (a fork's commits beyond its parent,
by `refs/parent/`; a README's opening, by `sparse-checkout`) run as written against
local repos served over file://. The searches in triage.md (pull requests, by
`-user:OWNER`) and in skills/stargazers/SKILL.md (the claude.ai listing, by
`search/repositories?q=user:LOGIN`) run with a stand-in gh that checks its arguments
and applies the command's own --jq to each page. Run: python3 -m unittest discover tests
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills"
REVIEW = SKILLS / "repo-review" / "SKILL.md"
TRIAGE = SKILLS / "repo-review" / "triage.md"
STARGAZERS = SKILLS / "stargazers" / "SKILL.md"


def block(path, marker):
    """The one sh block in the file that contains the marker, with its list indent removed."""
    found = [b for b in re.findall(r"```sh\n(.*?)\n\s*```", path.read_text(encoding="utf-8"), re.S) if marker in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing {marker!r} in {path.name}, found {len(found)}")
    lines = found[0].splitlines()
    indent = min(len(l) - len(l.lstrip(" ")) for l in lines if l.strip())
    return "\n".join(l[indent:] for l in lines)


def line(path, marker):
    """The one command line, in any sh block of the file, that contains the marker."""
    found = [l.strip() for b in re.findall(r"```sh\n(.*?)\n\s*```", path.read_text(encoding="utf-8"), re.S)
             for l in b.splitlines() if marker in l]
    if len(found) != 1:
        raise ValueError(f"expected one sh line containing {marker!r} in {path.name}, found {len(found)}")
    return found[0]


GIT_ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_COMMITTER_NAME": "Committer", "GIT_COMMITTER_EMAIL": "committer@example.com"}


def git(repo, *args, author=("Parent Dev", "dev@parent.example"), date=None):
    env = {**GIT_ENV, "GIT_AUTHOR_NAME": author[0], "GIT_AUTHOR_EMAIL": author[1]}
    if date:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
    return subprocess.run(["git", "-C", str(repo), *args], env=env, capture_output=True, text=True, check=True).stdout


def new_repo(path, branch):
    path.mkdir(parents=True)
    git(path, "init", "-q", "-b", branch)
    git(path, "config", "uploadpack.allowFilter", "true")
    return path


def commit(repo, name, text, message, **kw):
    f = repo / name
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")
    git(repo, "add", name)
    git(repo, "commit", "-q", "-m", message, **kw)


def run_sh(script, cwd):
    return subprocess.run(["sh", "-c", script], cwd=cwd, env=GIT_ENV, capture_output=True, text=True)


@unittest.skipUnless(shutil.which("git"), "git is needed")
class ForkCommitsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.parent = new_repo(self.tmp / "parent", "main")
        for i in range(3):
            commit(self.parent, "lib.txt", f"v{i}\n", f"Parent commit {i}")
        git(self.parent, "clone", "-q", str(self.parent), str(self.tmp / "fork"))
        self.fork = self.tmp / "fork"
        git(self.fork, "config", "uploadpack.allowFilter", "true")
        self.work = self.tmp / "work"
        self.work.mkdir()

    def run_snippet(self, shell="sh"):
        script = (block(REVIEW, "refs/parent/")
                  .replace("https://github.com/PARENT-OWNER/PARENT-REPO.git", f"file://{self.parent}")
                  .replace("https://github.com/OWNER/REPO.git", f"file://{self.fork}")
                  .replace("REPO", "fork"))
        out = subprocess.run([shell, "-c", script], cwd=self.work, env=GIT_ENV, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout.splitlines()

    def test_counts_and_lists_the_fork_s_own_commits_with_email_domains_only(self):
        commit(self.fork, "lib.txt", "mine\n", "Parse two-digit years", author=("Alex Rivera", "alex@oldjob.example"),
               date="2017-08-20T10:00:00Z")
        commit(self.fork, "lib.txt", "mine 2\n", "Build dist files", author=("Alex Rivera", "alex@oldjob.example"),
               date="2017-08-22T10:00:00Z")
        commit(self.parent, "lib.txt", "upstream\n", "Parent moves on")
        lines = self.run_snippet()
        self.assertEqual(lines[0], "2")
        self.assertEqual([l.split("\t") for l in lines[1:]], [
            ["Alex Rivera", "oldjob.example", "2017-08-22", "Build dist files"],
            ["Alex Rivera", "oldjob.example", "2017-08-20", "Parse two-digit years"],
        ])
        self.assertNotIn("alex@", "\n".join(lines))

    def test_an_unchanged_fork_counts_zero_even_when_the_parent_has_moved_on(self):
        commit(self.parent, "lib.txt", "upstream\n", "Parent moves on")
        self.assertEqual(self.run_snippet(), ["0"])

    def test_the_parent_s_default_branch_is_read_from_git(self):
        # The fork's default branch is an old master; the parent's is main.
        git(self.fork, "branch", "-m", "main", "master")
        commit(self.fork, "lib.txt", "mine\n", "On the old branch", author=("Alex Rivera", "a@x.example"))
        self.assertEqual(self.run_snippet()[0], "1")

    @unittest.skipUnless(shutil.which("zsh"), "zsh is needed")
    def test_zsh_keeps_the_branch_name_whole(self):
        # Claude Code on a Mac runs commands in zsh, where $b:r is a modifier that cuts the name at its last dot.
        git(self.parent, "branch", "-m", "main", "5.0.x")
        commit(self.fork, "lib.txt", "mine\n", "Mine", author=("Alex Rivera", "a@x.example"))
        self.assertEqual(self.run_snippet("zsh")[0], "1")

    def test_a_clone_left_from_an_earlier_run_is_brought_up_to_date(self):
        self.run_snippet()
        commit(self.fork, "lib.txt", "later\n", "Later", author=("Alex Rivera", "a@x.example"))
        self.assertEqual(self.run_snippet()[0], "1")

    def test_a_parent_that_cannot_be_read_fails_the_command(self):
        script = (block(REVIEW, "refs/parent/")
                  .replace("https://github.com/PARENT-OWNER/PARENT-REPO.git", f"file://{self.tmp}/gone")
                  .replace("https://github.com/OWNER/REPO.git", f"file://{self.fork}")
                  .replace("REPO", "fork"))
        out = run_sh(script, self.work)
        self.assertNotEqual(out.returncode, 0)
        self.assertEqual(out.stdout, "")


@unittest.skipUnless(shutil.which("git"), "git is needed")
class ReadmeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.work = self.tmp / "work"
        self.work.mkdir()

    def readme(self, files):
        repo = new_repo(self.tmp / "repo", "main")
        for name, text in files.items():
            commit(repo, name, text, f"Add {name}")
        script = block(REVIEW, "sparse-checkout").replace("https://github.com/OWNER/REPO.git", f"file://{repo}") \
            .replace("OWNER--REPO", "o--r")
        out = run_sh(script, self.work)
        self.assertEqual(out.returncode, 0, out.stderr)
        return out.stdout, self.work / "readmes" / "o--r"

    def test_prints_the_first_20_lines_and_checks_out_nothing_else(self):
        text = "".join(f"line {i}\n" for i in range(1, 30))
        out, clone = self.readme({"README.md": text, "src/big.txt": "x" * 1000})
        self.assertEqual(out, "== README.md\n" + "".join(f"line {i}\n" for i in range(1, 21)))
        self.assertFalse((clone / "src").exists())

    def test_the_plain_readme_comes_before_a_translation(self):
        out, _ = self.readme({"README.md": "English\n", "README.ja.md": "Japanese\n"})
        self.assertEqual(out, "== README.md\nEnglish\n")

    def test_github_s_order_github_folder_then_root_then_docs(self):
        out, _ = self.readme({"docs/README.md": "docs\n", "readme.rst": "root\n"})
        self.assertEqual(out, "== readme.rst\nroot\n")
        shutil.rmtree(self.tmp / "repo")
        shutil.rmtree(self.work / "readmes")
        out, _ = self.readme({".github/README.md": "github\n", "README.md": "root\n"})
        self.assertEqual(out, "== .github/README.md\ngithub\n")

    def test_a_readme_only_in_docs_is_found(self):
        out, _ = self.readme({"docs/README.md": "docs\n", "main.py": "print()\n"})
        self.assertEqual(out, "== docs/README.md\ndocs\n")

    def test_no_readme(self):
        out, _ = self.readme({"main.py": "print()\n"})
        self.assertEqual(out, "no README\n")

    @unittest.skipUnless(shutil.which("zsh"), "zsh is needed")
    def test_zsh_finds_it_without_complaining_about_the_places_with_none(self):
        # Claude Code on a Mac runs commands in zsh, which stops a command on a glob that matches nothing.
        repo = new_repo(self.tmp / "repo", "main")
        commit(repo, "docs/README.md", "docs\n", "Add docs/README.md")
        script = block(REVIEW, "sparse-checkout").replace("https://github.com/OWNER/REPO.git", f"file://{repo}") \
            .replace("OWNER--REPO", "o--r")
        out = subprocess.run(["zsh", "-c", script], cwd=self.work, env=GIT_ENV, capture_output=True, text=True)
        self.assertEqual((out.returncode, out.stdout, out.stderr), (0, "== docs/README.md\ndocs\n", ""))

    def test_a_repo_that_cannot_be_cloned_prints_nothing(self):
        script = block(REVIEW, "sparse-checkout").replace("https://github.com/OWNER/REPO.git", f"file://{self.tmp}/gone")
        out = run_sh(script, self.work)
        self.assertNotEqual(out.returncode, 0)
        self.assertEqual(out.stdout, "")


def stand_in_gh(bindir, expected_args, pages):
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


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class SearchTest(unittest.TestCase):
    def run_line(self, command, expected_args, pages):
        with tempfile.TemporaryDirectory() as bindir, tempfile.TemporaryDirectory() as cwd:
            stand_in_gh(bindir, expected_args, pages)
            env = {**os.environ, "PATH": f"{bindir}:/usr/bin:/bin"}
            out = subprocess.run(["sh", "-c", command], cwd=cwd, env=env, capture_output=True, text=True, check=True)
            written = Path(cwd) / "prs.tsv"
            return written.read_text() if written.exists() else out.stdout

    def test_one_search_lists_every_pull_request_to_other_people_s_repos(self):
        command = line(TRIAGE, "-user:OWNER").replace("OWNER", "octo-dev")
        pr = lambda repo, state, merged, title: {"repository_url": f"https://api.github.com/repos/{repo}", "state": state,
                                                 "title": title, "pull_request": {"merged_at": merged}}
        pages = [{"total_count": 3, "items": [pr("picker-org/datepicker", "closed", "2017-09-01T10:00:00Z", "Two-digit years"),
                                              pr("other/tool", "open", None, "Fix typo")]},
                 {"total_count": 3, "items": [pr("picker-org/datepicker", "closed", None, "Closed unmerged")]}]
        out = self.run_line(command, "api --paginate search/issues?q=author:octo-dev+type:pr+-user:octo-dev&per_page=100", pages)
        self.assertEqual([l.split("\t") for l in out.splitlines()], [
            ["picker-org/datepicker", "closed", "2017-09-01", "Two-digit years"],
            ["other/tool", "open", "", "Fix typo"],
            ["picker-org/datepicker", "closed", "", "Closed unmerged"],
        ])

    def test_stargazers_lists_the_starred_repos_from_search_on_claude_ai(self):
        found = re.findall(r"`(gh api --paginate 'search/repositories\?q=user:LOGIN[^`]*)`", STARGAZERS.read_text(encoding="utf-8"))
        self.assertEqual(len(found), 1)
        command = found[0].replace("LOGIN", "octo-dev")
        repo = lambda name, stars: {"full_name": name, "stargazers_count": stars}
        pages = [{"items": [repo("octo-dev/a", 3), repo("octo-dev/b", 0)]}, {"items": [repo("octo-dev/c", 1)]}]
        out = self.run_line(command, "api --paginate search/repositories?q=user:octo-dev+fork:true&per_page=100", pages)
        self.assertEqual(out.splitlines(), ["octo-dev/a", "octo-dev/c"])


if __name__ == "__main__":
    unittest.main()
