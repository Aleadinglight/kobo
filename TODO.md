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

- [ ] **W1. Clara BW firmware version mapping is assumed.**
  Libra H2O confirmed by user: 4.38.23697 (kobo7). Clara BW assumed kobo12
  → 4.45.23697. Confirm: Settings → Device information → firmware version.
  > Libra H2O: 4.38.23697 ✔ / Clara BW: …

- [ ] **W2. Device test (manual).** After first install, record:
  - menus / library titles show Vietnamese correctly (no boxes)
  - UI text is not bold
  - device model + firmware version
  > Result:

## Improvement

- [ ] **I1. Match stock metrics.** Stock Rakuten fonts set USE_TYPO_METRICS
  (fsSelection 0x80). If the new font's line height clips or shifts the UI,
  copy vertical metrics from stock. Only if the device test shows problems.
- [ ] **I2. Distribute `KoboRoot.tgz` how?** Default: not committed; attach
  to a GitHub Release.
- [ ] **I3. CI build** — GitHub Actions runs `./build.sh`, uploads the tgz.
- [ ] **I4. Test EPUB** — tiny EPUB with a Vietnamese title, author and TOC,
  to check the UI quickly on device.
- [ ] **I5. Render preview** — PNG of a Vietnamese sample line per output.
- [ ] **I6. Firmware check script** — turn the `FIRMWARE.md` commands into
  `scripts/inspect_firmware.py`, to re-run after future firmware updates.
- [ ] **I7. Old bold tgz** — if found, run it through the same inspection.
- [ ] **I8. Dictionary** — separate install, out of scope.

## Resolved

- [x] One source or separate serif? → One source for all families.
- [x] Target devices? → Libra H2O (4.38.23697) + Clara BW 2024.
- [x] Ship Avenir/Georgia? → Yes, all 16 files, one tgz for both devices.
  On Clara BW the 8 legacy files are simply extra and unused.
- [x] Avenir regular/italic → labelled Medium / Medium Italic, weight 500,
  to mirror stock.
- [x] Source name vs. license text → fine. Source is a Google Fonts (OFL)
  font; drop its name from the name table, ship the license file, name the
  real font in README.
- [x] Plain TTF or wrapped like stock? → Plain TTF. Assumption based on the
  user's earlier build and the reference payload, both plain TTF, which
  changed the UI on device.
- [x] Filenames and family names vs. stock firmware → verified, see
  `FIRMWARE.md`. `RakutenSansUIApp-BoldItali.ttf` was a typo; the real file
  is `RakutenSansUIApp-BoldItalic.ttf`. Avenir regular/italic are Medium/500.
