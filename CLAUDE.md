# CLAUDE.md

Builds `KoboRoot.tgz`: a patch that replaces the Kobo system UI fonts with a
Vietnamese-capable font, so the interface (titles, menus, progress, TOC)
renders Vietnamese.

Out of scope: book text (use normal sideloaded fonts), UI translation,
dictionaries, patching libnickel or its stylesheets.

Working files: `PLAN.md` (phases + progress), `TODO.md` (open questions,
Breaking / Warning / Improvement), `FIRMWARE.md` (what stock firmware
contains, with commands). Keep them current.

## Targets

- Devices: Kobo Libra H2O (fw 4.38.23697) and Clara BW 2024 (fw 4.45). Their
  Rakuten UI fonts are byte-identical; only Libra H2O also ships
  Avenir/Georgia. Details
  and commands: `FIRMWARE.md`.
- Font directory on device: `/usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts/`
  (nickel uses Qt 4.6.2 embedded).
- Stock fonts there are wrapped (`QTD` + length + zlib). We ship plain TTF,
  which nickel also loads (assumption from earlier plain-TTF builds that
  changed the UI).

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

- The user drops **one file** in `sources/`: the family zip from Google Fonts
  ("Download family"). The build picks the 4 static styles (Regular, Bold,
  Italic, BoldItalic) and `OFL.txt` out of it, and ignores the variable
  fonts.
- The same source feeds every target family. Rakuten Sans and Rakuten Serif
  (and Avenir / Georgia) end up identical — intended.
- Code must not hardcode the source's name; read it from the font files.
- README names the real font and ships its license, even though the internal
  name is rewritten.

## Target files

Defined once in `scripts/targets.py`; must match this table. Verified
against firmware (see `FIRMWARE.md`). Weight = stock `usWeightClass`.

| Filename | Family | Subfamily | Weight | On |
|---|---|---|---|---|
| RakutenSansUIApp-Regular.ttf | Rakuten Sans | Regular | 400 | both |
| RakutenSansUIApp-Bold.ttf | Rakuten Sans | Bold | 700 | both |
| RakutenSansUIApp-Italic.ttf | Rakuten Sans | Italic | 400 | both |
| RakutenSansUIApp-BoldItalic.ttf | Rakuten Sans | Bold Italic | 700 | both |
| RakutenSerifApp-Regular.ttf | Rakuten Serif | Regular | 400 | both |
| RakutenSerifApp-Bold.ttf | Rakuten Serif | Bold | 700 | both |
| RakutenSerifApp-Italic.ttf | Rakuten Serif | Italic | 400 | both |
| RakutenSerifApp-BoldItalic.ttf | Rakuten Serif | Bold Italic | 700 | both |
| Avenir.ttf | Avenir Next | Medium | 500 | Libra H2O |
| Avenir-Bold.ttf | Avenir Next | Bold | 700 | Libra H2O |
| Avenir-Italic.ttf | Avenir Next | Medium Italic | 500 | Libra H2O |
| Avenir-BoldItalic.ttf | Avenir Next | Bold Italic | 700 | Libra H2O |
| georgia.ttf | Georgia | Regular | 400 | Libra H2O |
| georgiab.ttf | Georgia | Bold | 700 | Libra H2O |
| georgiai.ttf | Georgia | Italic | 400 | Libra H2O |
| georgiaz.ttf | Georgia | Bold Italic | 700 | Libra H2O |

Filenames must match the firmware exactly. A wrong name adds a file instead
of overwriting, and the stock font silently wins. Only change a filename or
name based on a firmware listing, never by guessing.

Ship all 16 in one tgz for both devices. On Clara BW the Avenir/Georgia
files are extra and unused.

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
- Exactly the filenames in the target table
- Weight matches the table's Weight column; italic bit per target style
- Hashes differ across styles (same style may share a hash — same source)
- Family/subfamily match the table
- Source font name appears nowhere in the name table
- Vietnamese coverage survived

The output pass is not redundant: a wrong-source-in-wrong-slot bug is only
visible by reading outputs back. Weight and hash matter most — a
wrong-weight source gives a uniformly bold UI while everything else passes.

## Build

One command, same on every OS: `python3 build.py` (Windows: `py build.py`).
Only prerequisite: Python 3. No venv, no pip, no internet, no OS-specific
scripts.

- fonttools is bundled as `vendor/fonttools-<version>-py3-none-any.whl`
  (official pure-Python wheel from PyPI, MIT). `build.py` puts it on
  `sys.path` and imports from it directly.
- Pipeline: find the zip in `sources/` → extract the 4 styles → verify
  sources → rebrand to the 16 targets → verify outputs → write
  `KoboRoot.tgz` with Python's `tarfile`.
- The tgz: every entry under `usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts/`,
  exactly the 16 target files, owner root, mode 0644, no `.DS_Store` / `._*`.
  Read it back after writing and check this.
- Output: clear ✅ with the tgz path, or ❌ with a plain-language reason.
- GitHub Actions runs the same `build.py` on push and publishes `KoboRoot.tgz`
  as a GitHub Release. Most users just download it from there.

## Known limits

- Firmware updates restore stock fonts → re-copy the same tgz.
- If firmware renames UI families again (as with Avenir → Rakuten Sans),
  re-check the firmware as in `FIRMWARE.md`, update `targets.py`, rebuild.
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
4. Commit sources, scripts, the vendored wheel and docs. Don't commit
   `build/` or `KoboRoot.tgz`; releases carry the tgz.
5. Standard library + the vendored fonttools only. Never add a dependency
   that needs installing.
6. Focus on shipping. Only raise issues that would break the build or the
   result on the device; skip out-of-scope or hypothetical concerns.
