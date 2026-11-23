# Contributing a plug-in map

Thank you. A map is a small TOML file of facts about one plug-in; a good one lets a host set the
plug-in up correctly with no guessing.

## Add or change a map

1. Copy a map close to yours from [`maps/`](maps) and name the file `vendor-product.toml`
   (lower case, words joined by `-`: `fabfilter-pro-q-4.toml`).
2. Fill in the identity from the installed plug-in, not from memory:
   - **Audio Unit**: the `type`, `subtype` and `manufacturer` codes from the component's
     `Contents/Info.plist` (`AudioComponents`), or `auval -a`.
   - **VST3**: the audio processor's class id, 32 upper-case hex digits (your host's plug-in scan,
     or the VST3 SDK's validator).
   - **CLAP**: the descriptor `id`.
   - `tested_versions`: the version you checked it on.
3. Controls: use the parameter names exactly as the plug-in reports them, and the native range
   your host shows for them. Give each control a short `role` (`wet`, `decay`, `threshold`).
4. Calibration points are measurements: say how you measured in `method`, keep `x` rising, and
   only add points you measured.
5. Raise `revision` by one when you change an existing map.
6. Check it:

   ```sh
   python3 -m pip install -r tools/requirements.txt   # once (Python 3.11 or newer)
   python3 tools/validate.py                          # every map
   python3 tools/validate.py maps/your-map.toml       # just yours
   ```

7. Open a pull request. CI runs the same check and the sign-off check below.

## The free plug-in catalog

Catalog entries (`catalog/*.toml`) follow [CURATION.md](CURATION.md): suggest a plug-in in an issue
or a PR with its entry; `tools/refresh_catalog.py` re-pins newer releases. Pin only the author's
own downloads, with the size and SHA-256 you measured.

## What belongs here

- Yes: plug-in identity and parameter facts (ids, names, ranges, units, defaults, choice labels),
  settings that make a setup repeatable, and your own measurements.
- No: presets or preset files, plug-in binaries or installers, text or images copied from a
  vendor's manual or website, code from any app, personal information. Vendor and product names
  are used only to identify the plug-in.

## Sign-off (Developer Certificate of Origin)

Every commit must carry a `Signed-off-by:` line (`git commit -s`), certifying the
[Developer Certificate of Origin 1.1](https://developercertificate.org/): that you made the
contribution, or have the right to submit it, under this repository's licence.

## Licence

The maps, the schema and the tools are dedicated to the public domain under
[CC0 1.0](LICENSE). By contributing you dedicate your contribution the same way.

Why CC0: the maps are facts about plug-ins (codes, names, ranges, measurements) that every host
should be able to read and build on, commercial or not, without attribution clauses to track.
CC0 makes that explicit worldwide, including where a collection of facts could otherwise carry a
database right; MIT is written for software and would ask every host to carry its notice.

## Releases

A maintainer builds and signs a release after merging:

```sh
python3 tools/validate.py
python3 tools/bundle.py 2026.11.23            # writes plugin-maps.json
minisign -S -m plugin-maps.json -t "wisdom-plugin-maps 2026.11.23"
gh release create maps-2026.11.23 plugin-maps.json plugin-maps.json.minisig --title "Maps 2026.11.23"
```

Wisdom Pro accepts only bundles signed with its release key and that trusted comment.
