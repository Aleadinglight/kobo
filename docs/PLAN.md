# PLAN.md

Plan and progress. Rules: `.claude/CLAUDE.md`. Questions: `docs/TODO.md`.

Status: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked

## Layout

```
kobo/
├── README.md
├── .claude/CLAUDE.md           # project rules for Claude
├── docs/
│   ├── INSTALL.md              # user guide, also the Release notes
│   ├── PLAN.md  TODO.md        # progress and open questions
│   └── FIRMWARE.md             # what stock firmware contains
├── build.py                    # the one command
├── sources/                    # Noto Sans 4 static TTFs + OFL.txt
├── vendor/
│   └── fonttools-4.60.2-py3-none-any.whl
├── scripts/
│   ├── targets.py              # 16-row table
│   ├── fonts.py                # pick source styles, rebrand
│   └── verify.py               # source + output checks
└── .github/workflows/build.yml # build on GitHub, publish Release
```

Git-ignored: `build/` (fonts + `KoboRoot.tgz`).

## Phases

### 0. Frame
- [x] CLAUDE.md, PLAN.md, TODO.md
- [x] Verify target filenames/names against firmware → `FIRMWARE.md`
- [x] Decide build approach → single `build.py`, bundled fonttools

### 1. Build
- [x] `targets.py`, `fonts.py`, `verify.py`, `build.py`, `.gitignore`
- [x] Source font in `sources/`
- [x] `python3 build.py` passes; tgz read back with GNU tar and a separate
      fonttools install
- [x] Every check fails when it should (wrong weight / italic / bold flag,
      variable only, missing style, missing Vietnamese, filename typo,
      source-name leak, Regular in a Bold slot); Google zip layout picked
      correctly — scratch test, not committed
- [x] Same tgz hash on Python 3.9, 3.10, 3.11, 3.13 (Linux)

### 2. CI + release
- [x] Workflow: one Linux job builds; on main it also publishes a Release
- [ ] First CI run green (needs merge to main or a PR)

### 3. Docs + device test
- [x] README: short install, reading fonts, use your own font; docs in `docs/`
- [x] `docs/INSTALL.md`: full install, check, troubleshooting, undo; used
      as Release notes
- [ ] User installs on device, records result in TODO W2

## Done when

CI is green, a Release with `KoboRoot.tgz` exists, and the
device test in TODO W2 is recorded.
