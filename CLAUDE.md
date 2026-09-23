# CLAUDE.md

Builds `KoboRoot.tgz`: a patch that replaces the Kobo system UI fonts with a
Vietnamese-capable font, so the interface (titles, menus, progress, TOC)
renders Vietnamese.

Out of scope: book text (use normal sideloaded fonts), UI translation,
dictionaries, patching libnickel or its stylesheets.

Working files: `PLAN.md` (phases + progress), `TODO.md` (open questions,
Breaking / Warning / Improvement). Keep both current.

## Targets

- Devices: Kobo Clara BW and Libra 2, recent firmware. Assumed to share the
  same UI font files (same nickel build line) — unverified, see `TODO.md`.
- Font directory on device: `/usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts/`
  (nickel uses Qt 4.6.2 embedded).

## How the patch works

Qt picks fonts by the **internal family name (name ID 1)**, not the filename.
So each output must:

1. carry the stock family/subfamily name in its name table, and
2. be saved under the exact stock filename, so it overwrites the stock file.

Renaming a file alone does nothing. A filename typo adds a file instead of
overwriting, and the stock font silently wins.

Install: copy `KoboRoot.tgz` into `.kobo/` on the device, eject. The device
applies it on reboot and deletes it.

"Kobo Nickel" in the reading-font picker is a book font, unrelated to the
nickel process. We don't touch reading fonts.

## Source font

- One font family, 4 static TTFs (Regular, Bold, Italic, BoldItalic) plus its
  license, committed in `sources/`. Provided by the user.
- The same source feeds all four target families. Rakuten Sans and Rakuten
  Serif (and Avenir / Georgia) end up identical — intended, for simplicity.
- Code must not hardcode the source's name; read it from the source files.
- README names the real font and ships its license, even though the internal
  name is rewritten.

## The 16 target files

Defined once in `scripts/targets.py`; must match this table.
**Candidate list — not yet verified against stock firmware** (see `TODO.md`).
Rows marked ⚠ are suspected wrong.

| Filename | Family | Subfamily |
|---|---|---|
| RakutenSansUIApp-Regular.ttf | Rakuten Sans | Regular |
| RakutenSansUIApp-Bold.ttf | Rakuten Sans | Bold |
| RakutenSansUIApp-Italic.ttf | Rakuten Sans | Italic |
| ⚠ RakutenSansUIApp-BoldItali.ttf | Rakuten Sans | Bold Italic |
| RakutenSerifApp-Regular.ttf | Rakuten Serif | Regular |
| RakutenSerifApp-Bold.ttf | Rakuten Serif | Bold |
| RakutenSerifApp-Italic.ttf | Rakuten Serif | Italic |
| RakutenSerifApp-BoldItalic.ttf | Rakuten Serif | Bold Italic |
| Avenir.ttf | Avenir Next | Regular |
| Avenir-Bold.ttf | Avenir Next | Bold |
| Avenir-Italic.ttf | Avenir Next | Italic |
| Avenir-BoldItalic.ttf | Avenir Next | Bold Italic |
| georgia.ttf | Georgia | Regular |
| georgiab.ttf | Georgia | Bold |
| georgiai.ttf | Georgia | Italic |
| georgiaz.ttf | Georgia | Bold Italic |

Filenames must match the firmware exactly. A wrong name adds a file instead
of overwriting, and the stock font silently wins. Only change a filename
based on the firmware listing, never by guessing a "correct" spelling.

Rakuten = current firmware, Avenir/Georgia = legacy; build all 16.

## Verification (gates the build)

One script, two passes. Any failure stops the build.

**Sources (before rebrand):**
- `usWeightClass`: 400 Regular/Italic, 700 Bold/BoldItalic
- 4 distinct file hashes
- Italic bit set on italics, clear on uprights
- Static: no `fvar` (variable fonts fail silently on Kobo; Google Fonts'
  default download is variable)
- TrueType `glyf` outlines, no CFF
- Vietnamese precomposed coverage, including `đ` and `₫`

**Outputs (after rebrand):**
- Exactly the 16 filenames above
- Same weight and italic checks, per target style
- Hashes differ across styles (same style may share a hash — same source)
- Family/subfamily match the table
- Source font name appears nowhere in the name table
- Vietnamese coverage survived

The output pass is not redundant: a wrong-source-in-wrong-slot bug is only
visible by reading outputs back. Weight and hash matter most — a
wrong-weight source gives a uniformly bold UI while everything else passes.

## Build

`./build.sh` is the only entry point. It:

1. creates `.venv/` with fonttools (no system pip, no sudo; no manual activate)
2. verifies sources → rebrands → verifies outputs
3. stages under `root/usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts/`
4. removes `.DS_Store` / `._*`, runs `COPYFILE_DISABLE=1 tar -czf KoboRoot.tgz -C root usr`
5. checks `tar -tzf`: every entry under `usr/`, exactly 16 fonts, no junk

## Known limits

- Firmware updates restore stock fonts → re-copy the same tgz.
- If firmware renames UI families again (as with Avenir → Rakuten Sans),
  update `targets.py` from the new firmware and rebuild.
- A previous build rendered the UI bold; most likely wrong-weight sources,
  which the weight check now catches. Only if it recurs with verified
  weights: test a tgz whose Bold file carries Regular outlines. Normal →
  font-side fixable; still bold → nickel stylesheet / synthetic bold, no
  font-side fix.

## Rules

1. Don't claim something is verified without the command that showed it;
   otherwise mark it an assumption.
2. Never loosen a check to get a build through. Fix the input, or log it in
   `TODO.md`.
3. Unclear decisions go in `TODO.md`, not in guesses. Don't build past a
   Breaking item that blocks the step.
4. Commit sources, scripts and docs. Don't commit `.venv/`, `build/`,
   `root/`, or `KoboRoot.tgz` (release decision tracked in `TODO.md`).
5. Keep scripts small, standard-library + fonttools only.
