# TODO.md

Open questions and issues, by severity:

- **Breaking** — blocks a build step or can produce a wrong tgz.
- **Warning** — build works, but a result is unverified or may be wrong.
- **Improvement** — nice to have.

Resolve by writing the answer under the item and marking `[x]`.

## Breaking

- [ ] **B1. Source font files.**
  User will add 4 static TTFs (Regular, Bold, Italic, BoldItalic) + license
  to `sources/`. Blocks the first real build; all scripts can be written and
  tested before that.
  > Pending: user upload.

## Warning

- [ ] **W1. 16 filenames + family names unverified against stock firmware.**
  Target: Clara BW and Libra 2, recent firmware. Verify by extracting the
  official firmware zip for each model (it contains a KoboRoot.tgz with the
  font directory), listing the fonts, and reading name ID 1. If the two
  models differ, we need per-model targets.
  Firmware hosts are blocked in the build environment, so the user must
  download the zip, or allow `ereaderfiles.kobo.com` in the environment's
  network settings.
  Suspect rows:
  - `RakutenSansUIApp-BoldItali.ttf` — inconsistent with
    `RakutenSerifApp-BoldItalic.ttf`; likely a typo.
  - Avenir filenames — no evidence either way.
  - `georgia/b/i/z.ttf` — matches Microsoft's standard Georgia filenames, so
    plausible.
  Fallback if unverifiable: ship both `BoldItali` and `BoldItalic` for sans.
  The extra file is harmless (same font, same names); whichever matches
  stock overwrites it.
  > Firmware versions to check:

- [ ] **W2. "No source name in name table" vs. license text.**
  Copyright (ID 0) and license (ID 13) usually name the source font. Plan:
  rewrite those to drop the source name, keep license URL (ID 14), ship the
  license file + real font name in README. Renaming a modified OFL font is
  what the OFL asks for, so this should be compliant. Confirm.
  > Answer:

- [ ] **W3. Device test (manual).** After first install, record:
  - menus / library titles show Vietnamese correctly (no boxes)
  - UI text is not bold
  - device model + firmware version
  > Result:

## Improvement

- [ ] **I1. Distribute `KoboRoot.tgz` how?** Default: not committed; attach
  to a GitHub Release.
- [ ] **I2. CI build** — GitHub Actions runs `./build.sh`, uploads the tgz.
- [ ] **I3. Test EPUB** — build a tiny EPUB with a Vietnamese title, author
  and TOC, to check the UI quickly on device.
- [ ] **I4. Render preview** — PNG of a Vietnamese sample line per output
  font, before copying to the device.
- [ ] **I5. Old bold tgz** — if found, run `inspect_tgz.py` on it to confirm
  the wrong-weight theory. Low priority.
- [ ] **I6. Dictionary** — separate install, out of scope.

## Resolved

- [x] One source or separate serif? → One source for all families.
- [x] Target devices? → Clara BW + Libra 2, recent firmware.
