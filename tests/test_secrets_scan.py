"""Tests for the secrets scan in skills/repo-review/SKILL.md (Work before the action).

The script is taken from the skill as it stands, found by 'betterleaks'. Most tests run
it with a stand-in betterleaks that checks its arguments and writes a report in the
shape each major version writes. One test runs real betterleaks over a repo with fake
keys planted in its history; it runs when betterleaks is on PATH, or with BETTERLEAKS
set to one or more binaries separated by ':'. Run: python3 -m unittest discover tests
"""
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "repo-review" / "SKILL.md"


def scan_script():
    found = [b for b in re.findall(r"```sh\n(.*?)\n```", SKILL.read_text(encoding="utf-8"), re.S) if "betterleaks" in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing 'betterleaks' in SKILL.md, found {len(found)}")
    return found[0]


V1_ARGS = "git CLONE --no-banner --redact --exit-code 0 --report-format json --report-path secrets.json"
V2_ARGS = "git CLONE --no-banner --silent --redact --exit-code 0 --validate=false --analyze=false --output secrets.json"

# Trimmed from what 1.10.1 and 2.0.0-rc.9 wrote for the same planted key, redacted.
V1_REPORT = [{
    "RuleID": "github-pat", "StartLine": 1, "Match": "REDACTED", "Secret": "REDACTED",
    "Attributes": {"git.sha": "14d13b17fa57cf9fb6e3710143677535902d8290", "git.date": "2026-11-20T21:11:50Z",
                   "git.author_name": "Tester", "path": "config.env"},
    "File": "config.env", "Commit": "14d13b17fa57cf9fb6e3710143677535902d8290", "Date": "2026-11-20T21:11:50Z"}]
V2_REPORT = {
    "schema_version": "1",
    "findings": [{
        "rule_id": "stripe-access-token", "match": {"full": "REDACTED\"", "value": "REDACTED"},
        "attributes": {"git.sha": "9d15314f488f7428801f0aacb3c86f72e6dc1c1f", "git.date": "2026-11-20T21:11:50Z",
                       "git.author_name": "Tester"},
        "location": {"path": "pay.py", "start_line": 1, "end_line": 1}}],
    "scan": {"state": "complete", "num_findings": 1}}


@unittest.skipUnless(shutil.which("jq"), "the script reads the report with jq")
class StandInTest(unittest.TestCase):
    def run_script(self, name, version, expected_args, report, status=0):
        """Run the script with a stand-in betterleaks called NAME; return (exit code, stdout, stderr)."""
        with tempfile.TemporaryDirectory() as bindir, tempfile.TemporaryDirectory() as work:
            if name:
                canned = Path(bindir) / "report.json"
                canned.write_text(json.dumps(report))
                stand_in = Path(bindir) / name
                stand_in.write_text(
                    "#!/bin/sh\n"
                    f'[ "$1" = version ] && {{ echo "{version}"; exit 0; }}\n'
                    f'[ "$*" = "{expected_args}" ] || {{ echo "unexpected: $*" >&2; exit 2; }}\n'
                    f'cp "{canned}" secrets.json\n'
                    f"exit {status}\n")
                stand_in.chmod(0o755)
            jq_dir = Path(bindir) / "jq-only"
            jq_dir.mkdir()
            (jq_dir / "jq").symlink_to(shutil.which("jq"))
            env = {**os.environ, "PATH": f"{bindir}:{jq_dir}:/usr/bin:/bin"}
            r = subprocess.run(["sh", "-c", scan_script()], env=env, cwd=work, capture_output=True, text=True)
            return r.returncode, r.stdout, r.stderr

    def test_version_1_scans_locally_and_lists_commit_file_line_rule_and_date(self):
        code, out, err = self.run_script("betterleaks", "1.10.1", V1_ARGS, V1_REPORT)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "14d13b1\tconfig.env\t1\tgithub-pat\t2026-11-20\n")

    def test_version_2_turns_validation_off_and_reads_the_new_report(self):
        code, out, err = self.run_script("betterleaks", "2.0.0-rc.9", V2_ARGS, V2_REPORT)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "9d15314\tpay.py\t1\tstripe-access-token\t2026-11-20\n")

    def test_the_versioned_command_from_the_v1_cask_is_found(self):
        code, out, err = self.run_script("betterleaks-v1", "1.10.1", V1_ARGS, V1_REPORT)
        self.assertEqual(code, 0, err)
        self.assertIn("config.env", out)

    def test_a_clean_scan_prints_nothing_and_succeeds(self):
        code, out, err = self.run_script("betterleaks", "2.0.0-rc.9", V2_ARGS, {**V2_REPORT, "findings": []})
        self.assertEqual((code, out), (0, ""), err)

    def test_a_failed_scan_fails(self):
        code, out, _ = self.run_script("betterleaks", "2.0.0-rc.9", V2_ARGS, V2_REPORT, status=80)
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")

    def test_without_betterleaks_it_says_so_and_fails(self):
        code, out, err = self.run_script(None, "", "", None)
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertIn("betterleaks not found", err)

    def test_an_unknown_major_version_is_not_run(self):
        code, out, err = self.run_script("betterleaks", "3.0.0", "", V2_REPORT)
        self.assertNotEqual(code, 0)
        self.assertIn("3.0.0", err)


def real_binaries():
    named = [p for p in os.environ.get("BETTERLEAKS", "").split(":") if p]
    found = shutil.which("betterleaks")
    return named or ([found] if found else [])


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def planted_repo(repo):
    """A repo with a GitHub token added then removed on main, and a Stripe key on a branch never merged."""
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Tester")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "commit.gpgsign", "false")
    alnum = "aB3dE5fG7hI9jK1mN3pQ5rS7tU9vW1xY3zA5cD7eF9"
    token, key = "ghp_" + alnum[:36], "sk_live_" + alnum[5:29]
    (repo / "README.md").write_text("# demo\n")
    git(repo, "add", "README.md")
    git(repo, "commit", "-qm", "init")
    (repo / "config.env").write_text(f"GITHUB_TOKEN={token}\n")
    git(repo, "add", "config.env")
    git(repo, "commit", "-qm", "add config")
    git(repo, "rm", "-q", "config.env")
    git(repo, "commit", "-qm", "remove config")
    git(repo, "checkout", "-qb", "side")
    (repo / "pay.py").write_text(f'stripe_key = "{key}"\n')
    git(repo, "add", "pay.py")
    git(repo, "commit", "-qm", "payments")
    git(repo, "checkout", "-q", "main")
    sha = lambda ref: subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=7", ref],
                                     check=True, capture_output=True, text=True).stdout.strip()
    return {"config.env": sha("main~1"), "pay.py": sha("side")}, [token, key]


@unittest.skipUnless(shutil.which("jq") and shutil.which("git"), "jq and git are needed")
@unittest.skipUnless(real_binaries(), "betterleaks isn't on PATH and BETTERLEAKS isn't set")
class PlantedKeyTest(unittest.TestCase):
    def test_keys_anywhere_in_the_history_are_caught_and_never_printed(self):
        for binary in real_binaries():
            with self.subTest(binary=binary), tempfile.TemporaryDirectory() as tmp:
                tmp = Path(tmp)
                commits, secrets = planted_repo(tmp / "clone")
                bindir, work = tmp / "bin", tmp / "work"
                bindir.mkdir()
                work.mkdir()
                (bindir / "betterleaks").symlink_to(Path(binary).resolve())
                script = scan_script().replace("CLONE", str(tmp / "clone"))
                env = {**os.environ, "PATH": f"{bindir}:{os.environ['PATH']}",
                       "BETTERLEAKS_VALIDATE": "true", "BETTERLEAKS_ANALYZE": "true"}
                r = subprocess.run(["sh", "-c", script], env=env, cwd=work, capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stderr)
                rows = sorted((l.split("\t")[:3] for l in r.stdout.splitlines()), key=lambda row: row[1])
                self.assertEqual(rows, [[commits["config.env"], "config.env", "1"], [commits["pay.py"], "pay.py", "1"]])
                report = (work / "secrets.json").read_text()
                for secret in secrets:
                    self.assertNotIn(secret, r.stdout + r.stderr + report)
                if '"scan"' in report:
                    self.assertEqual(json.loads(report)["scan"]["status_counts"]["none"], 2)


if __name__ == "__main__":
    unittest.main()
