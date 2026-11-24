"""Tests for the commands in skills/repo-review/profile.md (Step 10, the profile review).

Each command is taken from profile.md by its content and run as it stands, with a
stand-in gh that checks its arguments and serves a page (applying the command's own
--jq when it has one), and the README clone and quote checker laid out as the steps
leave them. Run: python3 -m unittest discover tests
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent / "skills" / "repo-review"


def command(marker):
    """Return the one sh block in profile.md that contains the marker."""
    found = [b for b in re.findall(r"```sh\n(.*?)\n```", (SKILLS / "profile.md").read_text(encoding="utf-8"), re.S) if marker in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing {marker!r} in profile.md, found {len(found)}")
    return found[0]


def fake_gh(bindir, args, page):
    """A gh that answers only `args` (its arguments before any --jq), with `page`, through --jq when given."""
    f = Path(bindir) / "page.json"
    f.write_text(json.dumps(page))
    gh = Path(bindir) / "gh"
    gh.write_text(
        "#!/bin/sh\n"
        'if [ "$(eval echo \\${$#})" != "--jq" ] && [ $# -ge 2 ] && [ "$(eval echo \\${$(($# - 1))})" = "--jq" ]; then\n'
        '  q="$(eval echo \\"\\${$#}\\")"; n=$(($# - 2))\n'
        "else q=; n=$#; fi\n"
        'got=$(i=0; for a in "$@"; do i=$((i + 1)); [ $i -le $n ] && printf "%s " "$a"; done)\n'
        f'[ "$got" = "{args} " ] || {{ echo "unexpected: $*" >&2; exit 2; }}\n'
        f'if [ -n "$q" ]; then "{shutil.which("jq")}" "$q" "{f}"; else cat "{f}"; fi\n')
    gh.chmod(0o755)


SHELLS = ["sh"] + (["zsh"] if shutil.which("zsh") else [])


def run(line, cwd, bindir):
    """Run the command in sh, then in zsh where it's installed, and return sh's result once both agree."""
    env = {**os.environ, "PATH": f"{bindir}:/usr/bin:/bin:{os.path.dirname(shutil.which('jq'))}"}
    outs = [subprocess.run([shell, "-c", line], cwd=cwd, env=env, capture_output=True, text=True) for shell in SHELLS]
    for shell, out in zip(SHELLS[1:], outs[1:]):
        assert (out.returncode, out.stdout) == (outs[0].returncode, outs[0].stdout), f"{shell} differs: {out.stderr}"
    return outs[0]


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class ProfileCommandsTest(unittest.TestCase):
    def test_the_profile_fields_are_saved_without_the_rest_of_the_user(self):
        user = {"login": "me", "name": "Me", "bio": "I build data tools.", "company": None, "blog": "", "location": "Leeds",
                "twitter_username": None, "email": "me@example.com", "public_repos": 17}
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as bindir:
            fake_gh(bindir, "api user", user)
            out = run(command("twitter_username"), tmp, bindir)
            self.assertEqual(out.returncode, 0, out.stderr)
            saved = json.loads((Path(tmp) / "user.json").read_text())
        self.assertEqual(saved["bio"], "I build data tools.")
        self.assertNotIn("email", saved)
        self.assertEqual(set(saved), {"login", "name", "bio", "company", "blog", "location", "twitter_username"})

    def test_the_listing_keeps_one_repo_a_line(self):
        page = {"total_count": 2, "items": [{"full_name": "me/a", "private": False}, {"full_name": "me/me", "private": True}]}
        line = command("user:LOGIN+fork:true").replace("LOGIN", "me")
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as bindir:
            fake_gh(bindir, "api --paginate search/repositories?q=user:me+fork:true&per_page=100", page)
            out = run(line, tmp, bindir)
            self.assertEqual(out.returncode, 0, out.stderr)
            rows = [json.loads(l) for l in (Path(tmp) / "repos.jsonl").read_text().splitlines()]
        self.assertEqual([r["full_name"] for r in rows], ["me/a", "me/me"])

    def links(self, readme, found, expect_query):
        line = command("linked.txt").replace("LOGIN", "me")
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as bindir:
            path = Path(tmp) / "readmes" / "me--me" / "README.md"
            path.parent.mkdir(parents=True)
            path.write_text(readme, encoding="utf-8")
            fake_gh(bindir, f"api search/repositories?q={expect_query}+fork:true&per_page=100", {"items": found})
            out = run(line, tmp, bindir)
            self.assertEqual(out.returncode, 0, out.stderr)
            return [l.split("\t") for l in out.stdout.splitlines()]

    def test_each_linked_repo_gets_what_a_visitor_finds(self):
        readme = ("I work on [Alpha](https://github.com/me/alpha) and [beta](https://github.com/Me/Beta/blob/main/README.md).\n"
                  "Old: <a href=\"https://github.com/me/gone\">gone</a>, private: github.com/me/secret.\n"
                  "Sponsor me at https://github.com/sponsors/me. Picture: https://github.com/user-attachments/assets/1.\n"
                  "Contributed to https://github.com/other/lib.git and again https://github.com/other/lib.\n")
        found = [{"full_name": "me/alpha", "private": False, "archived": False},
                 {"full_name": "me/beta", "private": False, "archived": True},
                 {"full_name": "me/secret", "private": True, "archived": False},
                 {"full_name": "other/lib", "private": False, "archived": False}]
        rows = self.links(readme, found, "repo:me/alpha+repo:Me/Beta+repo:me/gone+repo:me/secret+repo:other/lib")
        self.assertEqual(rows, [["me/alpha", "public"], ["Me/Beta", "archived"], ["me/gone", "not found"],
                                ["me/secret", "private"], ["other/lib", "public"]])

    def test_a_link_at_the_end_of_a_sentence_loses_its_full_stop(self):
        rows = self.links("See github.com/me/alpha.\n", [{"full_name": "me/alpha", "private": False, "archived": False}], "repo:me/alpha")
        self.assertEqual(rows, [["me/alpha", "public"]])

    def test_a_readme_that_links_no_repo_makes_no_search(self):
        line = command("linked.txt").replace("LOGIN", "me")
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as bindir:
            path = Path(tmp) / "readmes" / "me--me" / "README.md"
            path.parent.mkdir(parents=True)
            path.write_text("I build data tools.\n", encoding="utf-8")
            gh = Path(bindir) / "gh"
            gh.write_text("#!/bin/sh\necho called >&2\nexit 2\n")
            gh.chmod(0o755)
            out = run(line, tmp, bindir)
        self.assertEqual((out.returncode, out.stdout, out.stderr), (0, "", ""))

    def test_quotes_are_checked_against_the_readme_and_the_bio(self):
        line = command("NOT IN THE BIO").replace("LOGIN", "me")
        bio = "GitHub profile bio, read via the API"
        page = {"profile": True, "questions": [
            {"short": "Introduction", "quotes": [{"text": "I build data tools", "source": bio}, {"text": "I work on Alpha.", "source": "README.md, line 1"}]},
            {"short": "Facts", "quotes": [{"text": "I wrote compilers", "source": bio}]},
            {"short": "Pins", "quotes": [{"text": "me/alpha", "source": "pinned items, read via GraphQL"}]}]}
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as bindir:
            root = Path(tmp)
            (root / "readmes" / "me--me").mkdir(parents=True)
            (root / "readmes" / "me--me" / "README.md").write_text("I work on Alpha.\n", encoding="utf-8")
            shutil.copy(SKILLS / "verify_run.py", root / "verify_run.py")
            (root / "user.json").write_text(json.dumps({"login": "me", "bio": "I build data tools."}))
            (root / "PROFILE.json").write_text(json.dumps(page))
            out = run(line, tmp, bindir)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("Introduction: ok (README.md, line 1)", out.stdout)
        self.assertIn("problems: 0", out.stdout)
        self.assertIn("Introduction: ok (bio)", out.stdout)
        self.assertIn("Facts: NOT IN THE BIO", out.stdout)
        self.assertNotIn("Pins: ok (bio)", out.stdout)


if __name__ == "__main__":
    unittest.main()
