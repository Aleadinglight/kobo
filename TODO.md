# TODO.md

Open questions and issues. Ordered by severity:

- **Breaking** — blocks a build step or can produce a wrong/broken tgz.
- **Warning** — build works, but a result is unverified or may be wrong.
- **Improvement** — nice to have.

When an item is resolved, write the answer under it, mark `[x]`, and
update `PLAN.md` if it changes the plan.

## Breaking

- [ ] **B1. Where do the source fonts come from?**
  Options: (a) Claude downloads Noto Sans static TTFs from the notofonts
  GitHub release (network may block it); (b) you drop 4 TTFs + license into
  `sources/`. Blocks Phase 1.
  > Answer:

- [ ] **B2. One source for both Sans and Serif, or a separate serif?**
  One Noto Sans source → Rakuten Sans and Rakuten Serif (and Avenir /
  Georgia) render identically. Alternative: Noto Serif for Rakuten Serif and
  Georgia. Decides how many source files Phase 1 needs (4 or 8).
  > Answer:

- [ ] **B3. Do you still have the old KoboRoot.tgz that rendered bold?**
  Needed to close the bold-UI question (read weights + hashes). Without it,
  Phase 7 can't start. Doesn't block the main build.
  > Answer:

## Warning

- [ ] **W1. The 16 filenames are unverified against stock firmware.**
  They come from `lelinhtinh/kobo-tieng-viet`. A wrong name silently leaves
  the stock font in place. Fix: tell me the target Kobo model + firmware
  version so I can try to fetch the official firmware zip and list its font
  directory.
  > Model / firmware:

- [ ] **W2. Family names are unverified too.**
  "Rakuten Sans", "Rakuten Serif", "Avenir Next", "Georgia" come from the
  same source. Qt matches on these, so a wrong one means no effect. Same fix
  as W1 (read name ID 1 from the stock fonts in the firmware zip).

- [ ] **W3. "No trace of the source name" vs. the OFL license.**
  The OFL text in name ID 13 and the copyright in ID 0 mention "Noto".
  Plan: rewrite IDs 0/13 so they no longer mention "Noto", keep license URL
  (ID 14), and ship `OFL.txt` + README naming the real font. Also note OFL
  "Reserved Font Name" rules: renaming the family is what OFL asks for with
  modified fonts, so the rebrand is compliant. Confirm this is acceptable.
  > Answer:

- [ ] **W4. Device test is manual.**
  Only you can confirm on the device that menus render Vietnamese and are
  not bold. Record result here after first install.
  > Result:

## Improvement

- [ ] **I1. Commit `KoboRoot.tgz` to the repo, or publish as a GitHub
  Release?** Default: not committed (build output). A Release keeps the
  repo small and gives a download link.
  > Answer:

- [ ] **I2. CI build.** A GitHub Actions workflow that runs `./build.sh` and
  uploads the tgz as an artifact on each push.

- [ ] **I3. Dictionary install.** Separate from this tgz; source and
  mechanism undecided (see CLAUDE.md Known limits). Out of scope for now.

- [ ] **I4. Render preview.** Script that renders a Vietnamese sample line
  with each of the 16 outputs to a PNG, for a quick visual check before
  copying to the device.
