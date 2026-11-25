# Wisdom plug-in maps

Open, factual maps of third-party audio plug-ins: who a plug-in is in each format, what its
controls do, and measured calibration points, so a host or an AI mixing assistant can set the
plug-in up by meaning ("2.4 s of decay", "a 4:1 ratio") instead of guessing at opaque 0..1 knobs.

One TOML file per plug-in, in [`maps/`](maps). Every map is checked against a JSON Schema
([`schema/plugin-map.schema.json`](schema/plugin-map.schema.json)) and a few extra rules by
[`tools/validate.py`](tools/validate.py), on every pull request.

The maps are dedicated to the public domain ([CC0 1.0](LICENSE)): use them in any host, free or
commercial, with or without credit.

## What a map holds

```toml
format = 1          # the map format (this is format 1)
revision = 1        # raised by one on every change

sources = ["Identity: the Audio Unit's component description and version (Info.plist)"]

[plugin]
name = "ValhallaRoom"
vendor = "Valhalla DSP"
type = "reverb"     # eq, dynamics, de_esser, reverb, delay, modulation, saturation, pitch, utility, ducking, instrument, other
roles = ["reverb"]  # mixing jobs it can take
tested_versions = ["2.0.0"]

[formats.au]        # Audio Unit component description: three four-character codes
type = "aufx"
subtype = "Ruum"
manufacturer = "oDin"

[formats.vst3]
class_id = "5653545275756D76616C68616C6C6172"   # the audio processor's class id
matches_au = true   # same parameter ids, names, ranges and defaults as the AU

# [formats.clap]
# id = "com.vendor.product"

[[controls]]
role = "decay"      # what the control is for
param = "decay"     # the parameter's name as the plug-in reports it
calibration = "decay_s"

[calibration.decay_s]
x = "decay_s"       # what the first number of each point is
method = "how it was measured"
points = [[0.60, 0.005], [1.12, 0.01], [10.0, 0.1]]   # [x, native value], x rising

[[fixed]]           # a setting written exactly as given when a host sets the plug-in up
param = "Mode"
value = 0.396
```

- **Identity** (`formats`): the Audio Unit's type/subtype/manufacturer codes, the VST3 class id,
  the CLAP id. A host finds the map by any of them (`au:aufx:Ruum:oDin`,
  `vst3:5653…6172`, `clap:com.vendor.product`).
- **Controls**: a role, the parameter's name (per format if they differ), its native range, unit,
  taper, default and choice labels.
- **Fixed settings**: values a host writes as given (bypass off, unity output, a mode).
- **Calibration**: measured `[x, native value]` points, read piecewise-linear and held at the
  ends. They turn a meaning (seconds, ms, a ratio, dBFS) into the plug-in's own value.
- **Measurements**: single measured numbers (`first_return_ms`).

The data is identity and parameter facts only: no presets, no vendor binaries, no manual text.

## How Wisdom Pro uses it

Wisdom Pro, a mixing app, ships a snapshot of `maps/` inside the app, and
reads newer maps from this repo's releases:

- Each release carries `plugin-maps.json` (every map, as JSON) and `plugin-maps.json.minisig`, a
  [minisign](https://jedisct1.github.io/minisign/) signature made with the Wisdom Pro release key.
  The app checks the signature before it keeps anything and refuses a bundle that was changed or
  signed by anyone else.
- A downloaded map replaces the bundled one only when its `revision` is higher; a map for a plug-in
  the app doesn't know is added. Downloaded maps name plug-ins and colour their type in the mixer
  at once. The settings Wisdom Pro's AI mixing writes come from the maps built into the app, so a
  new or changed map reaches AI mixing with the next app release, after it is tested there.
- Wisdom Pro's "Map my plug-ins" writes its result in this format, ready to submit here.

Any other host can read the same files: the format is plain TOML and the schema is JSON Schema
2020-12.

## Free plug-in catalog

[`catalog/`](catalog) is a short, curated list of free, open-source or freeware plug-ins (the top few per
category, with open-source choices ranked by GitHub stars under the rules in [CURATION.md](CURATION.md)) that a host can offer to
install or obtain from its author. Direct downloads for macOS and Windows are pinned by size and
SHA-256 and says how it installs: plug-in bundles copied into the per-user plug-in folders, or the
author's installer opened for the user. Email/account/checkout entries instead open the official
product page and show its requirements; the host does not download them. Nothing is re-hosted here. Entries are checked against
[`schema/catalog-entry.schema.json`](schema/catalog-entry.schema.json) by the same validator.

## Contributing

New maps and corrections are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md): one map per file,
checked with `python3 tools/validate.py`, every commit signed off (DCO).

Catalog update 2026-11-25: the owner withdrew all pitch plug-in recommendations.
The Pitch enum and freeware/author-page schema remain compatible with older catalogs.
