"""Save a traffic snapshot of public GitHub repos, and turn it into one document for the page.

    python3 -I traffic.py snapshot REPOS.tsv RAW.json
    python3 -I traffic.py doc RAW.json DOC.json

`snapshot` reads REPOS.tsv, one repo per line as `gh --jq ... | @tsv` prints it:
owner/name, fork, archived, stars, forks. For each it reads the daily views and clones
GitHub still holds (14 days) and the top referrers with `gh api`, and writes them all
to RAW.json. A repo whose traffic can't be read (not attached on claude.ai, or no push
access) goes under `missing` with the reason, and the rest carry on.

`doc` turns RAW.json into the document the page stores for that snapshot: per repo, its
flags, stars and forks, the first and last day GitHub gave for views and clones, only
the days with any traffic (the rest of that span were zero), and the referrers. One
document per snapshot means a run only ever creates a document; the page merges them,
the later snapshot winning for a day both hold.
"""
import datetime
import json
import subprocess
import sys


def gh(path):
    """One `gh api` call: (data, None), or (None, the reason it failed)."""
    p = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if p.returncode != 0:
        lines = [l for l in (p.stderr or p.stdout).strip().splitlines() if l.strip()]
        return None, (lines[-1] if lines else f"gh exited {p.returncode}")[:200]
    return json.loads(p.stdout), None


def read_repos(text):
    repos = []
    for line in text.splitlines():
        f = line.split("\t")
        if len(f) < 5 or "/" not in f[0]:
            continue
        repos.append({"name": f[0], "fork": f[1] == "true", "archived": f[2] == "true",
                      "stars": int(f[3]), "forks": int(f[4])})
    return repos


def snapshot(repos, read=gh, now=None):
    taken = (now or datetime.datetime.now(datetime.timezone.utc)).isoformat(timespec="seconds")
    out = {"taken": taken, "repos": [], "missing": []}
    for r in sorted(repos, key=lambda r: r["name"].lower()):
        views, why = read(f"repos/{r['name']}/traffic/views")
        clones, why2 = (None, None) if why else read(f"repos/{r['name']}/traffic/clones")
        referrers, why3 = (None, None) if why or why2 else read(f"repos/{r['name']}/traffic/popular/referrers")
        reason = why or why2 or why3
        if reason:
            out["missing"].append({"name": r["name"], "reason": reason})
            continue
        out["repos"].append({**r,
                             "views": {"count": views["count"], "uniques": views["uniques"], "daily": views["views"]},
                             "clones": {"count": clones["count"], "uniques": clones["uniques"], "daily": clones["clones"]},
                             "referrers": referrers})
    return out


def span(daily):
    """GitHub's daily rows as the first and last day given, and the days with any traffic."""
    days = sorted(d["timestamp"][:10] for d in daily)
    return {"from": days[0] if days else None, "to": days[-1] if days else None,
            "days": {d["timestamp"][:10]: [d["count"], d["uniques"]] for d in daily if d["count"] or d["uniques"]}}


def doc(raw):
    """The page's document for one snapshot. RAW is `snapshot`'s output, or a hand snapshot in the same shape."""
    return {
        "taken": raw["taken"],
        "repos": {r["name"]: {
            "fork": r["fork"], "archived": r["archived"], "stars": r["stars"], "forks": r["forks"],
            "views": span(r["views"]["daily"]), "clones": span(r["clones"]["daily"]),
            "referrers": [[x["referrer"], x["count"], x["uniques"]] for x in r.get("referrers") or []],
        } for r in raw["repos"]},
        "missing": raw.get("missing", []),
    }


def doc_id(raw):
    """The document's id: the time taken, in UTC, which a path segment allows (2026-11-20T17:04:41Z)."""
    t = datetime.datetime.fromisoformat(raw["taken"]).astimezone(datetime.timezone.utc)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv):
    if len(argv) == 4 and argv[1] == "snapshot":
        with open(argv[2], encoding="utf-8") as f:
            raw = snapshot(read_repos(f.read()))
        with open(argv[3], "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=1)
        views = sum(r["views"]["count"] for r in raw["repos"])
        clones = sum(r["clones"]["count"] for r in raw["repos"])
        print(f"{len(raw['repos'])} repos read, {len(raw['missing'])} not read; {views} views and {clones} clones in the days GitHub gave")
    elif len(argv) == 4 and argv[1] == "doc":
        with open(argv[2], encoding="utf-8") as f:
            raw = json.load(f)
        d = doc(raw)
        text = json.dumps(d, separators=(",", ":"))
        with open(argv[3], "w", encoding="utf-8") as f:
            f.write(text)
        print(f"{doc_id(raw)}\t{len(text.encode('utf-8'))} bytes\t{len(d['repos'])} repos")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
