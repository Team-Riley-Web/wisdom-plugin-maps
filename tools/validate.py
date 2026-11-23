#!/usr/bin/env python3
"""Check plug-in map files: the JSON Schema, then the rules a schema can't express.

Usage: python3 tools/validate.py [maps/*.toml ...]   (default: every file in maps/)
Exit status 0 when every map passes; each problem is printed as `file: problem`.
Needs Python 3.11+ (tomllib) and `jsonschema` (pip install -r tools/requirements.txt).
"""
import json
import pathlib
import re
import sys
import tomllib

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "plugin-map.schema.json").read_text())
FILE_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.toml$")


def ids(m):
    """The plug-in's ids, one per format, as hosts write them."""
    f = m.get("formats", {})
    out = []
    if "au" in f:
        au = f["au"]
        out.append(f"au:{au['type']}:{au['subtype']}:{au['manufacturer']}")
    if "vst3" in f:
        out.append(f"vst3:{f['vst3']['class_id']}")
    if "clap" in f:
        out.append(f"clap:{f['clap']['id']}")
    return out


def rules(m):
    """What the schema can't check: unique roles, calibrations that exist, rising tables, ranges."""
    p = []
    calibration = m.get("calibration", {})
    seen = set()
    for c in m.get("controls", []):
        role = c["role"]
        if role in seen:
            p.append(f"control role {role!r} appears twice")
        seen.add(role)
        rng = c.get("range")
        if rng and not rng[0] < rng[1]:
            p.append(f"control {role!r}: range must be [min, max] with min < max")
        for key in ("default", "full_scale"):
            if key in c and rng and not rng[0] <= c[key] <= rng[1]:
                p.append(f"control {role!r}: {key} {c[key]} is outside its range")
        name = c.get("calibration")
        if name is not None:
            if name not in calibration:
                p.append(f"control {role!r} names calibration {name!r}, which the map lacks")
            elif rng and any(not rng[0] <= y <= rng[1] for _, y in calibration[name]["points"]):
                p.append(f"calibration {name!r} has native values outside control {role!r}'s range")
    for name, t in calibration.items():
        xs = [x for x, _ in t["points"]]
        if any(b <= a for a, b in zip(xs, xs[1:])):
            p.append(f"calibration {name!r}: x must rise strictly")
    return p


def check(path):
    problems = []
    if not FILE_NAME.match(path.name):
        problems.append("file names are lower-case words joined by '-', ending .toml (vendor-product.toml)")
    try:
        m = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        return [f"not TOML: {e}"], None
    validator = jsonschema.Draft202012Validator(SCHEMA)
    for e in sorted(validator.iter_errors(m), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(x) for x in e.absolute_path) or "(top)"
        problems.append(f"{where}: {e.message}")
    if not problems:
        problems += rules(m)
    return problems, m


def main(argv):
    paths = [pathlib.Path(a) for a in argv] or sorted((ROOT / "maps").glob("*.toml"))
    if not paths:
        print("no maps to check")
        return 1
    failed = 0
    owner = {}
    for path in paths:
        problems, m = check(path)
        if m is not None and not problems:
            for i in ids(m):
                if i in owner:
                    problems.append(f"{i} is already mapped by {owner[i]}")
                owner[i] = path.name
        for prob in problems:
            print(f"{path}: {prob}")
        failed += bool(problems)
    print(f"{len(paths) - failed} of {len(paths)} maps pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
