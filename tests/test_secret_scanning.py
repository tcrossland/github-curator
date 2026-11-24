"""Tests for the check of GitHub's secret scanning in skills/repo-review/SKILL.md (Work before the action).

The command is taken from the skill as it stands, by 'secret-scanning/alerts', and run with a
stand-in gh that answers each of its calls from a table, as GitHub answered them on 2026-11-24:
the repo's settings with or without `security_and_analysis`, a list of open alerts when scanning
is on, and HTTP 404 "Secret scanning is disabled on this repository." when it's off.
Run: python3 -m unittest discover tests
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

SKILL = Path(__file__).resolve().parent.parent / "skills" / "repo-review" / "SKILL.md"
SETTINGS = "api repos/me/tool"
ALERTS = "api --paginate repos/me/tool/secret-scanning/alerts?state=open&per_page=100"
DISABLED = "Secret scanning is disabled on this repository."


def command():
    found = [b for b in re.findall(r"```sh\n(.*?)\n```", SKILL.read_text(encoding="utf-8"), re.S) if "secret-scanning/alerts" in b]
    if len(found) != 1:
        raise ValueError(f"expected one sh block containing 'secret-scanning/alerts' in SKILL.md, found {len(found)}")
    return found[0].replace("OWNER/REPO", "me/tool")


STAND_IN = """#!{python}
import json, subprocess, sys
args = sys.argv[1:]
q = None
if len(args) >= 2 and args[-2] == "--jq":
    q, args = args[-1], args[:-2]
key = " ".join(args)
open({calls!r}, "a").write(key + "\\n")
routes = json.load(open({routes!r}))
if key not in routes:
    sys.exit("unexpected: " + key)
r = routes[key]
if r["status"] != 200:
    sys.stderr.write("gh: %s (HTTP %d)\\n" % (r["message"], r["status"]))
    sys.exit(1)
body = json.dumps(r["body"])
if q is None:
    print(body)
else:
    sys.stdout.write(subprocess.run([{jq!r}, "-r", q], input=body, capture_output=True, text=True, check=True).stdout)
"""


def settings(scanning, push):
    sa = {"secret_scanning": {"status": scanning}, "secret_scanning_push_protection": {"status": push}}
    return {"status": 200, "body": {"full_name": "me/tool", "visibility": "public", "security_and_analysis": sa}}


SHELLS = ["sh"] + (["zsh"] if shutil.which("zsh") else [])


@unittest.skipUnless(shutil.which("jq"), "jq is needed to stand in for gh's --jq")
class SecretScanningTest(unittest.TestCase):
    def check(self, routes):
        """Run the command in each shell; return its output and the calls gh got, once the shells agree."""
        results = []
        for shell in SHELLS:
            with tempfile.TemporaryDirectory() as bindir:
                calls, table = Path(bindir) / "calls.txt", Path(bindir) / "routes.json"
                table.write_text(json.dumps(routes))
                gh = Path(bindir) / "gh"
                gh.write_text(STAND_IN.format(python=sys.executable, calls=str(calls), routes=str(table), jq=shutil.which("jq")))
                gh.chmod(0o755)
                env = {**os.environ, "PATH": f"{bindir}:/usr/bin:/bin"}
                out = subprocess.run([shell, "-c", command()], env=env, capture_output=True, text=True)
                results.append((out.returncode, out.stdout, calls.read_text().splitlines() if calls.exists() else []))
        for shell, r in zip(SHELLS[1:], results[1:]):
            self.assertEqual(r, results[0], f"{shell} differs from sh")
        return results[0]

    def test_scanning_on_with_no_alert_open_prints_only_the_settings(self):
        code, out, calls = self.check({SETTINGS: settings("enabled", "enabled"), ALERTS: {"status": 200, "body": []}})
        self.assertEqual((code, out), (0, "secret scanning, push protection: enabled enabled\n"))
        self.assertEqual(calls, [SETTINGS, ALERTS])

    def test_scanning_off_reads_no_alerts(self):
        # Asking would give HTTP 404 "Secret scanning is disabled on this repository." (seen 2026-11-24).
        code, out, calls = self.check({SETTINGS: settings("disabled", "disabled"), ALERTS: {"status": 404, "message": DISABLED}})
        self.assertEqual((code, out), (0, "secret scanning, push protection: disabled disabled\n"))
        self.assertEqual(calls, [SETTINGS])

    def test_each_open_alert_is_listed_without_its_secret(self):
        alert = {"number": 3, "secret_type_display_name": "GitHub Personal Access Token", "created_at": "2026-11-20T09:15:02Z",
                 "html_url": "https://github.com/me/tool/security/secret-scanning/3", "secret": "ghp_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE0000",
                 "state": "open"}
        code, out, _ = self.check({SETTINGS: settings("enabled", "disabled"), ALERTS: {"status": 200, "body": [alert]}})
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), ["secret scanning, push protection: enabled disabled",
                                            "3\tGitHub Personal Access Token\t2026-11-20\thttps://github.com/me/tool/security/secret-scanning/3"])
        self.assertNotIn("ghp_", out)

    def test_settings_shown_only_to_admins_read_as_unread(self):
        # Someone else's repo, or a private repo of the user's, came back without security_and_analysis (2026-11-24).
        code, out, calls = self.check({SETTINGS: {"status": 200, "body": {"full_name": "me/tool", "visibility": "public"}}})
        self.assertEqual((code, out), (0, "secret scanning, push protection: unread unread\n"))
        self.assertEqual(calls, [SETTINGS])

    def test_alerts_refused_after_settings_say_on_print_alerts_unread(self):
        code, out, _ = self.check({SETTINGS: settings("enabled", "enabled"), ALERTS: {"status": 404, "message": DISABLED}})
        self.assertEqual((code, out), (0, "secret scanning, push protection: enabled enabled\nalerts unread\n"))


if __name__ == "__main__":
    unittest.main()
