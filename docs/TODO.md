# TODO.md

Open questions and issues, by severity:

- **Breaking** — blocks a build step or can produce a wrong tgz.
- **Warning** — build works, but a result is unverified or may be wrong.
- **Improvement** — nice to have.

Resolve by writing the answer under the item and marking `[x]`.

## Breaking

_None._

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
- [ ] **I2. Test EPUB** — tiny EPUB with a Vietnamese title, author and TOC,
  to check the UI quickly on device.
- [ ] **I3. Render preview** — PNG of a Vietnamese sample line per output.
- [ ] **I4. Firmware check script** — turn the `FIRMWARE.md` commands into
  `scripts/inspect_firmware.py`, to re-run after future firmware updates.
- [ ] **I5. Old bold tgz** — if found, run it through the same inspection.
- [ ] **I6. Dictionary** — separate install, out of scope.
- [ ] **I7. `kobo-drive.zip` release extra** — reading fonts in `fonts/` and
  sleep images in `.kobo/screensaver/`, laid out like the Kobo USB drive.
  No tgz needed; nickel reads both paths (`strings libnickel.so.1.0.0 |
  grep -E '/mnt/onboard/fonts|\.kobo/screensaver'`, Libra H2O + Clara BW).
  After the UI font build ships.
- [ ] **I8. Custom bookmark (dog-ear) icon** — separate project, later.
  The icon is not a file on the device: it's a Qt resource compiled into
  libnickel (`strings libnickel.so.1.0.0 | grep dogear` →
  `:/images/dogear/dogear.png`, `:/images/book/AnnotationsList_icon_dogear.png`,
  both firmwares). Changing it means patching libnickel per firmware version
  (kobopatch-style), which this project's rules exclude.

## Resolved

- [x] Source font → Noto Sans v2.015 static, 4 styles + OFL.txt in
  `sources/`, fetched from the Google Fonts manifest.
- [x] One source or separate serif? → One source for all families.
- [x] Target devices? → Libra H2O (4.38.23697) + Clara BW 2024.
- [x] Ship Avenir/Georgia? → Yes, all 16 files, one tgz for both devices.
  On Clara BW the 8 legacy files are simply extra and unused.
- [x] Avenir regular/italic → labelled Medium / Medium Italic, weight 500,
  to mirror stock.
- [x] Source name vs. license text → fine. Source is a Google Fonts (OFL)
  font; drop its name from the name table, ship the license file, name the
  real font in README.
- [x] Build approach → one `build.py`, Python 3 only, fonttools bundled as a
  wheel in `vendor/` (no venv, pip, internet or OS scripts).
- [x] Distribution → GitHub Actions builds and publishes a Release.
- [x] Plain TTF or wrapped like stock? → Plain TTF. Assumption based on the
  user's earlier build and the reference payload, both plain TTF, which
  changed the UI on device.
- [x] Filenames and family names vs. stock firmware → verified, see
  `FIRMWARE.md`. `RakutenSansUIApp-BoldItali.ttf` was a typo; the real file
  is `RakutenSansUIApp-BoldItalic.ttf`. Avenir regular/italic are Medium/500.
