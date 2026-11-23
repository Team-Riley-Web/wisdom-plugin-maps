#!/usr/bin/env python3
"""Check plug-in maps and catalog entries: the JSON Schemas, then the rules a schema can't express.

Usage: python3 tools/validate.py [maps/*.toml catalog/*.toml ...]   (default: every map and entry)
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
CATALOG_SCHEMA = json.loads((ROOT / "schema" / "catalog-entry.schema.json").read_text())
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


def catalog_rules(path, e):
    """A catalog entry: its id is its file name, each platform once, a macOS and a Windows build,
    bundles exactly for unpacked archives, the instrument kind exactly for instruments, maps that exist."""
    p = []
    if e["id"] != path.stem:
        p.append(f"id {e['id']!r} must be the file name {path.stem!r}")
    plats = [d["platform"] for d in e["downloads"]]
    if len(plats) != len(set(plats)):
        p.append("a platform is listed twice")
    if not any(x.startswith("macos") for x in plats) or "windows-x86_64" not in plats:
        p.append("needs a macOS and a Windows x64 build")
    for d in e["downloads"]:
        unpack = d["install"] == "unpack"
        if unpack and d["archive"] not in ("dmg", "zip", "tar.gz"):
            p.append(f"{d['platform']}: only dmg, zip and tar.gz archives unpack")
        if unpack != bool(d.get("bundles")):
            p.append(f"{d['platform']}: bundles are listed for unpacked archives only, and they need some")
        boxed = d["archive"] in ("dmg", "zip", "tar.gz")
        if d["install"] == "installer" and boxed != ("installer" in d):
            p.append(f"{d['platform']}: an installer inside a dmg or zip names its path (installer), and only then")
    if (e["category"] == "instrument") != ("instrument" in e):
        p.append("instrument (synth, sampler, drums) is given for instruments only, and they need it")
    for m in e.get("maps", []):
        if not (ROOT / "maps" / m).exists():
            p.append(f"maps: {m} is not in maps/")
    return p


def check(path):
    if path.parent.name == "catalog":
        return check_entry(path)
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


def check_entry(path):
    problems = []
    if not FILE_NAME.match(path.name):
        problems.append("file names are lower-case words joined by '-', ending .toml")
    try:
        e = tomllib.loads(path.read_text(encoding="utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as err:
        return [f"not TOML: {err}"], None
    validator = jsonschema.Draft202012Validator(CATALOG_SCHEMA)
    for err in sorted(validator.iter_errors(e), key=lambda x: list(x.absolute_path)):
        where = "/".join(str(x) for x in err.absolute_path) or "(top)"
        problems.append(f"{where}: {err.message}")
    if not problems:
        problems += catalog_rules(path, e)
    return problems, None


def main(argv):
    paths = [pathlib.Path(a) for a in argv] or sorted((ROOT / "maps").glob("*.toml")) + sorted((ROOT / "catalog").glob("*.toml"))
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
    print(f"{len(paths) - failed} of {len(paths)} files pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
