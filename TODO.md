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

- [ ] **B2. Ship the Avenir/Georgia files?**
  Facts (`FIRMWARE.md`): Clara BW firmware doesn't contain them at all;
  Libra H2O does. Nickel uses `font-family: Georgia` / `Avenir` in some
  built-in HTML (e.g. "What's new" pages). Unknown whether they are also
  reading-font choices for book text, which is out of scope.
  Options:
  - (a) Ship only the 8 Rakuten files. Same tgz works on both devices, adds
    nothing to Clara BW. Legacy pages on Libra H2O may still show boxes.
  - (b) Ship all 16. On Clara BW this *adds* two new families instead of
    replacing anything.
  - (c) Two tgz files, one per device.
  Recommendation: (a) first, add Avenir/Georgia later only if a Libra H2O
  screen still shows boxes.
  > Answer:

- [ ] **B3. Plain TTF or wrapped like stock?**
  Stock fonts are `QTD` + length + zlib (`FIRMWARE.md`). Unknown whether
  nickel also loads plain TTF at these paths. A previous build (believed to
  be plain TTF) did change the UI, which suggests plain works, but that
  hasn't been verified.
  Options: (a) plain TTF; (b) wrap outputs the same way as stock (easy:
  `b"QTD" + len.to_bytes(4,"big") + zlib.compress(ttf)`).
  Recommendation: build both variants; test plain first on device. If it
  works, keep plain (simpler).
  > Answer:

## Warning

- [ ] **W1. Avenir regular weight is Medium/500, not Regular/400.**
  Only matters if B2 ships Avenir. Plan: label the output "Medium", weight
  500, using the Regular source outlines, to mirror stock.

- [ ] **W2. "No source name in name table" vs. license text.**
  Copyright (ID 0) and license (ID 13) usually name the source font. Plan:
  rewrite those to drop the source name, keep license URL (ID 14), ship the
  license file + real font name in README. Renaming a modified OFL font is
  what the OFL asks for, so this should be compliant. Confirm.
  > Answer:

- [ ] **W3. Device ↔ firmware mapping is assumed.**
  Libra H2O confirmed by user: 4.38.23697 (kobo7). Clara BW assumed kobo12
  → 4.45.23697. Confirm: Settings → Device information → firmware version.
  > Libra H2O: 4.38.23697 ✔ / Clara BW: …

- [ ] **W4. Device test (manual).** After first install, record:
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
- [x] Filenames and family names vs. stock firmware → verified, see
  `FIRMWARE.md`. `RakutenSansUIApp-BoldItali.ttf` was a typo; the real file
  is `RakutenSansUIApp-BoldItalic.ttf`. Avenir regular/italic are Medium/500.
