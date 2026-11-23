#!/usr/bin/env python3
"""Refresh the free plug-in catalog: re-rank by GitHub stars, re-pin newer author releases, open a PR.

Usage: python3 tools/refresh_catalog.py [--pr]       (needs the GitHub CLI `gh`, signed in)

For each catalog/*.toml entry whose builds come from a GitHub release:
- updates `stars` and `selected`;
- looks at the author's latest release (or the same rolling tag) and, for each download, finds the
  asset of the same shape (the old file name with its version, date and commit hash as wildcards);
  when it is a different file, downloads it, and re-pins `version`, `url`, `size` and `sha256`;
- prints entries whose release is older than 18 months (CURATION.md: drop unless an exception).

It never adds or removes an entry by itself and never checks the new build's contents: a human
reviews the PR (bundle paths inside a new archive, signing) before merging. With --pr it commits on
a new branch with a sign-off and opens the pull request.
"""
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import tomllib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().isoformat()
STALE_DAYS = 548  # about 18 months


def gh(path):
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def shape(name):
    """A regex for files like `name` in a later release: digits runs, dates and hex hashes vary."""
    pattern = re.escape(name)
    pattern = re.sub(r"(\\-)?[0-9a-f]{7,40}(?=\\\.|\\-|$)", r"\\-?[0-9a-f]{7,40}", pattern)
    pattern = re.sub(r"\d+", r"\\d+", pattern)
    return re.compile("^" + pattern + "$")


def sha256_of(url):
    h = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(url, timeout=120) as r:
        while chunk := r.read(1 << 20):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def set_value(text, key, value, start=0):
    """Replaces the first `key = …` line at or after `start` (keeps the file's layout and comments)."""
    m = re.compile(rf"^{key} = .*$", re.M).search(text, start)
    if not m:
        return text
    return text[: m.start()] + f"{key} = {json.dumps(value)}" + text[m.end():]


def refresh(path):
    text = path.read_text(encoding="utf-8")
    e = tomllib.loads(text)
    notes = []
    repo = e["source"].removeprefix("https://github.com/")
    try:
        stars = gh(f"repos/{repo}")["stargazers_count"]
        if stars != e["stars"]:
            notes.append(f"stars {e['stars']} -> {stars}")
            text = set_value(text, "stars", stars)
    except subprocess.CalledProcessError:
        notes.append(f"can't read {repo}")
    for d in e["downloads"]:
        if d["origin"] != "github-release":
            continue
        m = re.match(r"https://github\.com/([^/]+/[^/]+)/releases/download/([^/]+)/(.+)$", d["url"])
        if not m:
            continue
        rel_repo, tag, name = m.groups()
        try:
            rel = gh(f"repos/{rel_repo}/releases/tags/{tag}") if d.get("rolling") else gh(f"repos/{rel_repo}/releases/latest")
        except subprocess.CalledProcessError:
            notes.append(f"{d['platform']}: no release found")
            continue
        age = (datetime.date.today() - datetime.date.fromisoformat(rel["published_at"][:10])).days
        if age > STALE_DAYS and "exception" not in e:
            notes.append(f"release {rel['tag_name']} is {age} days old: drop or add an exception")
        want = shape(name)
        found = [a for a in rel["assets"] if want.match(a["name"])]
        if len(found) != 1:
            notes.append(f"{d['platform']}: {len(found)} assets look like {name}; check by hand")
            continue
        a = found[0]
        if a["browser_download_url"] == d["url"] and a["size"] == d["size"]:
            continue
        digest, size = sha256_of(a["browser_download_url"])
        at = text.find(d["url"])
        block = text.rfind("[[downloads]]", 0, at)
        for key, value in (("version", rel["tag_name"].lstrip("v")), ("url", a["browser_download_url"]), ("size", size), ("sha256", digest)):
            text = set_value(text, key, value, block)
        notes.append(f"{d['platform']}: re-pinned to {a['name']} (check its bundles and signing)")
    if notes:
        text = set_value(text, "selected", TODAY)
        path.write_text(text, encoding="utf-8")
    return notes


def main(argv):
    changed = {}
    for path in sorted((ROOT / "catalog").glob("*.toml")):
        notes = refresh(path)
        if notes:
            changed[path.name] = notes
            print(f"{path.name}:\n  " + "\n  ".join(notes))
    if not changed:
        print("catalog is current")
        return 0
    if "--pr" in argv:
        branch = f"catalog-refresh-{TODAY}"
        body = "\n".join(f"- `{n}`: " + "; ".join(v) for n, v in changed.items())
        subprocess.run(["git", "switch", "-c", branch], check=True, cwd=ROOT)
        subprocess.run(["git", "commit", "-s", "-am", f"Catalog refresh {TODAY}"], check=True, cwd=ROOT)
        subprocess.run(["git", "push", "-u", "origin", branch], check=True, cwd=ROOT)
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("Automatic re-rank and re-pin. Review each re-pinned build (bundle paths, signing) before merging.\n\n" + body)
        subprocess.run(["gh", "pr", "create", "--title", f"Catalog refresh {TODAY}", "--body-file", f.name], check=True, cwd=ROOT)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
