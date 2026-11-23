#!/usr/bin/env python3
"""Build a release's plugin-maps.json: every map in maps/ and every entry in catalog/, as one JSON file.

Usage: python3 tools/bundle.py RELEASE [OUT]   (RELEASE like 2026.11.23; OUT default plugin-maps.json)
The maintainer signs the result with minisign (trusted comment "wisdom-plugin-maps RELEASE") and
attaches both files to the GitHub release; see CONTRIBUTING.md. Run tools/validate.py first.
"""
import json
import pathlib
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    release, out = argv[0], pathlib.Path(argv[1] if len(argv) > 1 else "plugin-maps.json")
    maps = [tomllib.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "maps").glob("*.toml"))]
    catalog = [tomllib.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "catalog").glob("*.toml"))]
    out.write_text(json.dumps({"format": 1, "release": release, "maps": maps, "catalog": catalog}, separators=(",", ":")), encoding="utf-8")
    print(f"{out}: {len(maps)} maps, {len(catalog)} catalog entries, release {release}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
