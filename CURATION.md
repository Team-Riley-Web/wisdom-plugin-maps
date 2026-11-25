# Curation of the free plug-in catalog

`catalog/` lists a small, curated set of free plug-ins a host can offer to install or obtain from their authors. It is deliberately not "every free plug-in": a few good ones per category.

## Selection rules

A plug-in is listed when all of these hold, with open-source entries ranked by source repository stars (freeware has no star ranking):

1. **Free to keep, not a trial.** Open-source licenses are recorded by SPDX id; freeware is clearly labeled as governed by the author's EULA.
2. **Maintained**: a release within about the last 18 months.
3. **Official builds for macOS and Windows x64** (VST3, AU and/or CLAP), published by the author:
   macOS universal or arm64 + x86_64.
4. **A working download from the author's own release** (GitHub release, or the author's official
   site). Nothing is ever re-hosted here: a direct download pins the author's URL with size and
   SHA-256, and a host refuses a mismatch. Email, account or checkout downloads instead
   list a per-platform author page and requirements; the host opens that page without downloading.
5. **At most 5-10 per category** (instruments: synths, samplers, drums). A thin category is left
   thin rather than padded with stale plug-ins.

Freeware is listed only from its official author page, with its terms and sign-up requirements
shown honestly. Never list anything that only exists as a re-upload, or star-farmed "cracked suite" repositories.

macOS signing is checked at selection and recorded per build (`signed`: `notarized`,
`developer-id`, `unsigned` for ad-hoc signed official builds, which hosts load). Windows builds are
the author's x64 builds; their signatures are not checked here (`not-checked`).

## The list at selection (2026-11-23)

Stars as reported by the GitHub API that day. `*` marks an exception (below).

### EQ / Filter

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [ZL Equalizer 2](https://github.com/ZL-Audio/ZLEqualizer) | 1080 | AGPL-3.0 | 1.4.2 | au, standalone, vst3 | arm64 unsigned, x86_64 unsigned |
| [filtr](https://github.com/tiagolr/filtr) | 179 | AGPL-3.0 | 1.3.0 | au, vst3 | universal unsigned |
| [ZL Spectrum Equalizer](https://github.com/ZL-Audio/ZLSpectrumEqualizer) | 91 | AGPL-3.0 | 0.1.2 | au, vst3 | arm64 unsigned, x86_64 unsigned |

### Dynamics

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [master_me](https://github.com/trummerschlunk/master_me) | 764 | GPL-3.0 | 1.3.1 | au, clap, vst3 | universal unsigned |
| [gate12](https://github.com/tiagolr/gate12) | 326 | GPL-3.0 | 1.3.3 | au, vst3 | universal unsigned |
| [ZL Compressor](https://github.com/ZL-Audio/ZLCompressor) | 233 | AGPL-3.0 | 0.6.1 | au, standalone, vst3 | arm64 unsigned, x86_64 unsigned |
| [Vocal Gate](https://github.com/dan-k-k/vocal-gate) | 69 | GPL-3.0 | 1.0.5 | au, vst3 | arm64 unsigned |
| [ZL Limiter](https://github.com/ZL-Audio/ZLLimiter) | 32 | AGPL-3.0 | 0.1.0 | au, vst3 | arm64 unsigned, x86_64 unsigned |

### De-esser

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [Airwindows Consolidated](https://github.com/baconpaul/airwin2rack) | 757 | MIT | 2026-11-22-91b3343 | au, clap, standalone, vst3 | universal notarized |

### Reverb

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [reevr](https://github.com/tiagolr/reevr) | 301 | GPL-3.0 | 1.4.0 | au, vst3 | universal unsigned |
| [Room Reverb](https://github.com/cvde/RoomReverb) | 148 | GPL-3.0 | 1.4.1 | au, clap, vst3 | universal developer-id |

### Delay

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [time12](https://github.com/tiagolr/time12) | 312 | GPL-3.0 | 1.2.3 | au, vst3 | universal unsigned |
| [QDelay](https://github.com/tiagolr/qdelay) | 166 | GPL-3.0 | 1.2.3 | au, vst3 | universal unsigned |

### Modulation

None qualifies yet. Airwindows Consolidated (De-esser) covers it.


### Saturation / Amp

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [Neural Amp Modeler (Gateway)](https://github.com/sdatkinson/NeuralAmpModelerPlugin) * | 3080 | MIT | 1.0.1 | au, standalone, vst3 | universal notarized |
| [CHOW Tape Model](https://github.com/jatinchowdhury18/AnalogTapeModel) * | 1466 | GPL-3.0 | 2.11.4 | au, clap, standalone, vst3 | universal notarized |
| [Homecorrupter](https://github.com/igorski/homecorrupter) | 66 | MIT | 1.2.0 | vst3 | universal developer-id |
| [Krunch](https://github.com/hollance/krunch) | 56 | GPL-3.0 | 1.0.1 | au, vst3 | universal developer-id |

### Pitch

Owner decision, 2026-11-25: all pitch plug-ins (PitchCure, THE_PITCH 2 MINI and PitchNet)
were removed from the catalog. The category schema remains readable for older bundles.
The freeware/author-page delivery code remains supported but is currently unused.

### Utility / Meters

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [Noise Suppression for Voice (RNNoise)](https://github.com/werman/noise-suppression-for-voice) | 6996 | GPL-3.0 | 1.22 | au, vst3 | universal unsigned |
| [NeuralNote](https://github.com/DamRsn/NeuralNote) | 3531 | Apache-2.0 | 2.2.0 | au, standalone, vst3 | arm64 notarized, x86_64 notarized |
| [ZL Splitter](https://github.com/ZL-Audio/ZLSplitter) | 168 | AGPL-3.0 | 0.4.0 | au, vst3 | arm64 unsigned, x86_64 unsigned |
| [PerceptoMap](https://github.com/hqrrr/PerceptoMap) | 83 | AGPL-3.0 | 0.18.2 | vst3 | arm64 unsigned, x86_64 unsigned |
| [The Informer](https://github.com/valeriorlandini/theinformer) | 54 | GPL-3.0 | 0.4.0 | au, vst3 | x86_64 unsigned |

### Instruments

| Plug-in | Stars | Licence | Release | Formats | macOS build |
|---|---:|---|---|---|---|
| [Surge XT](https://github.com/surge-synthesizer/surge) (synth) * | 4159 | GPL-3.0 | 1.3.4 | au, clap, standalone, vst3 | universal notarized |
| [Dexed](https://github.com/asb2m10/dexed) (synth) | 3678 | GPL-3.0 | 1.1.0 | au, clap, standalone, vst3 | universal notarized |
| [Cardinal](https://github.com/DISTRHO/Cardinal) (synth) | 3277 | GPL-3.0 | 26.02 | au, clap, standalone, vst3 | universal notarized |
| [RipplerX](https://github.com/tiagolr/ripplerx) (synth) | 665 | GPL-3.0 | 1.5.19 | au, vst3 | universal unsigned |
| [INTERSECT](https://github.com/tucktuckg00se/INTERSECT) (sampler) | 346 | GPL-3.0 | 0.20.0 | au, vst3 | arm64 unsigned, x86_64 unsigned |
| [Six Sines](https://github.com/baconpaul/six-sines) (synth) | 317 | MIT | 1.2.1 | au, clap, standalone, vst3 | universal notarized |
| [JC303](https://github.com/midilab/jc303) (synth) | 314 | GPL-3.0 | 0.14.0 | au, clap, vst3 | universal unsigned |
| [Just a Sample](https://github.com/BOBONA/Just-a-Sample) (sampler) | 228 | MIT | 1.3-latest | au, vst3 | universal unsigned |
| [Wavetable](https://github.com/FigBug/Wavetable) (synth) | 220 | BSD-3-Clause | 1.0.37 | au, clap, standalone, vst3 | universal notarized |
| [Aeolus](https://github.com/Archie3d/aeolus_plugin) (synth) | 172 | GPL-3.0 | 0.3.0 | vst3 | universal unsigned |
| [JS80P](https://github.com/attilammagyar/js80p) (synth) | 147 | GPL-3.0 | 4.1.1 | vst3 | universal notarized |
| [Niner](https://github.com/hyperfocusdsp/niner) (drums) | 47 | GPL-3.0 | 1.0.1 | clap, vst3 | arm64 unsigned, x86_64 unsigned |

## Exceptions (owner-approved, 2026-11-23)

- **Surge XT**: the last stable release, 1.3.4, is from 2024-08 (outside rule 2); the authors
  publish official builds every day. The stable 1.3.4 builds are pinned.
- **Neural Amp Modeler (Gateway)**: the author's pre-built installers (Gateway, his build of the
  MIT plug-in) are published only on his official site, not on GitHub (rule 4 allows the author's
  site). Pinned by size and SHA-256 like every other build.
- **CHOW Tape Model** ("stable classic"): release 2.11.4 is from 2023-11 (outside rule 2) but the
  plug-in is widely used; listed because its macOS installer is notarized and universal (Apple
  silicon and Intel) and Windows has an official 64-bit installer.

Checked and not listed:

- **Dragonfly Reverb** ("stable classic" candidate, 3.2.10, 2023-04): the binaries are universal,
  but the macOS installer is neither signed nor notarized, so it fails the condition for the
  exception.
- **Held until their licences are confirmed** (the repository's licence file is not recognised as
  a standard SPDX licence): Noise Repellent, Floe. They are added once clearly open.

## Notes

- **Airwindows Consolidated** is a rolling build: the author replaces it in place (`rolling = true`).
  When its pinned file is gone, a host says the catalog needs a refresh instead of installing
  anything else.
- Installers (`install = "installer"`: pkg, exe, msi, or one inside a dmg or zip) are downloaded,
  verified and opened for the user to click through; a host never runs one silently or with
  elevated rights. Archives with plain plug-in bundles (`install = "unpack"`) are copied into the
  per-user plug-in folders.

## Refreshing the list

`python3 tools/refresh_catalog.py --pr` (weekly, or before an app release) updates each entry's
stars, re-pins newer author releases (new URL, version, size and SHA-256) and flags entries whose
release went stale; it opens a pull request. A human reviews every re-pinned build (bundle paths
inside the archive, signing) and any ranking change before merging, and new candidates are added
by hand under the rules above. Removing an entry, or adding an exception, is a maintainer decision
recorded here.
