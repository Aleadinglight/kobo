# CLAUDE.md

Makes the Kobo interface (Kobo nickel) render Vietnamese by replacing the
system UI fonts, packaged as KoboRoot.tgz.

Scope: the interface only (titles, menus, progress, TOC). Book text uses
normal sideloaded fonts. Not a UI translation.

Working files:
- `PLAN.md` — implementation plan and progress. Update it as phases complete.
- `TODO.md` — open questions and issues, ordered Breaking / Warning /
  Improvement. Add any question there instead of guessing.

## How it works

The Kobo interface is drawn by nickel using Qt 4.6.2 embedded. Fonts live at
`/usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts/`.

Note: "Kobo Nickel" is also the name of a reading font in the font picker, for
book text. Unrelated to the nickel process. This repo changes UI fonts, not
reading fonts.

Qt matches fonts by **internal name table (name ID 1), not filename.**
Renaming a file alone does nothing — and breaks things, because the family
that previously claimed that name no longer exists. The rebrand must rewrite
the name table AND save to the exact stock filename.

Install: copy `KoboRoot.tgz` to `.kobo/`, eject. Applied on boot, then deleted.

## Font verification (do this first — it gates everything)

Two scripted checks, same script, run at two points.

**On source fonts, before any rebrand.** Fail loudly on any violation:

- `usWeightClass` — 400 for Regular and Italic, 700 for Bold and BoldItalic
- File hashes — four distinct values (catches the same file downloaded four times)
- Italic bit set on italic faces, clear on uprights
- Static, not variable (`fvar` absent) — variable fonts fail silently on Kobo's
  Qt/FreeType, and variable is the Google Fonts default download
- `glyf` outlines, not CFF/OTF
- Vietnamese precomposed coverage including `đ` and `₫`

**On the 16 built files, before packaging.** Same weight and hash checks, plus:

- Family and subfamily names match the target table
- No trace of the source font name anywhere in the name table
- Vietnamese coverage survived the rebrand

The second pass is not redundant. A bug that copies the wrong source into the
wrong slot is invisible unless the outputs are read back.

Weight and hash are the checks that matter most — a wrong-weight source
produces a uniformly bold UI while every other check passes.

## The 16 files

**Source: `lelinhtinh/kobo-tieng-viet` payload. Not verified against stock
firmware.** Confirm by extracting the official firmware zip for the target
model (it contains a KoboRoot.tgz with the rootfs fonts) and listing the font
directory. USB mass storage only exposes the user partition, so the device
itself can't be listed without SSH.

| Filename | Family | Subfamily |
|---|---|---|
| RakutenSansUIApp-Regular.ttf | Rakuten Sans | Regular |
| RakutenSansUIApp-Bold.ttf | Rakuten Sans | Bold |
| RakutenSansUIApp-Italic.ttf | Rakuten Sans | Italic |
| RakutenSansUIApp-BoldItali.ttf | Rakuten Sans | Bold Italic |
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

Filename oddities, per that source: sans bold-italic is `BoldItali` (no
trailing c), serif bold-italic is `BoldItalic` (has it), Georgia uses b/i/z
suffixes. A mismatch adds a file instead of overwriting and the stock font
wins — silently. Bold-italic and the legacy families are rarely rendered, so
a typo there would go unnoticed by everyone downstream.

Rakuten Sans/Serif are current firmware; Avenir/Georgia legacy. Build all 16.

## Source fonts

Noto Sans (static) verified for coverage. Ship the license file and state the
real font name in the README even though the internal name is rewritten.

Mapping one source across both Rakuten Sans and Rakuten Serif makes those
families byte-identical — selecting either gives the same rendering. That's
expected, not a bug. Use a separate serif source if the distinction matters.

## Build

Python venv with fonttools — not system pip, no sudo. `build.sh` creates
`.venv/` and calls `.venv/bin/python` directly; no manual activation.

1. Verify sources (above) — hard fail, don't continue
2. Rebrand 16 outputs to the exact filenames above
3. Verify outputs (above) — hard fail
4. Stage under `usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts/`
5. `find . -name '.DS_Store' -delete; find . -name '._*' -delete`
6. `COPYFILE_DISABLE=1 tar -czf KoboRoot.tgz -C root usr`
7. `tar -tzf KoboRoot.tgz` — starts at `usr/`, no wrapper dir, no junk

## Note: bold UI

A previous build rendered UI text bold. The most likely cause is source fonts
that weren't the weights they were assumed to be — that build only checked
static/glyf and never checked `usWeightClass`, which is exactly the property
that produces this symptom while everything else passes.

Confirm before investigating further: read `usWeightClass` and file hashes out
of the previously installed tgz. Uniform 700, or identical hashes, closes it.

Only if the weights were genuinely correct is there a real open question, and
the diagnostic is: build one tgz where the Bold file carries Regular outlines
but stays labeled Bold. Renders normal → the header is being served the Bold
file. Still bold → the weight comes from nickel's stylesheet or synthetic
bold, and there is no font-side fix.

## Known limits

- Firmware updates restore stock fonts. Fix: re-copy the same tgz, no rebuild.
- If a firmware renames the UI families (Rakuten already did this once:
  Avenir → Rakuten Sans), re-copying won't work. Read the new family name from
  the firmware zip and redo the rebrand.
- Dictionary is a separate install — not a file overwrite, can't share the
  tgz. Source and mechanism both undecided.

## Rules

- Don't state as verified what hasn't been checked. Anything asserted as fact
  carries the command that produced it, or is marked an assumption.
- Don't patch libnickel or its stylesheets.
- Verification failures are hard stops. Never loosen a check to get a build
  through; fix the input or record it in `TODO.md`.
- The 16-row target table lives in one place in code (`scripts/targets.py`)
  and must match the table above exactly.
- Open questions go in `TODO.md`, not in guesses. Don't implement past a
  Breaking item that blocks the step.
- Build outputs (`build/`, `root/`, `KoboRoot.tgz`, `.venv/`) are not
  committed unless `TODO.md` records a decision to do so.
