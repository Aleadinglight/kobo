# PLAN.md

Plan and progress. Rules: `CLAUDE.md`. Questions: `TODO.md`.

Status: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked

## Layout

```
kobo/
├── CLAUDE.md  PLAN.md  TODO.md  FIRMWARE.md  README.md
├── build.py                    # the one command
├── sources/                    # user drops the Google Fonts zip here
├── vendor/
│   └── fonttools-4.65.0-py3-none-any.whl
├── scripts/
│   ├── targets.py              # 16-row table
│   ├── fontsource.py           # find zip, pick 4 static styles + OFL.txt
│   ├── verify.py               # source + output checks
│   └── rebrand.py              # rewrite name table
└── .github/workflows/build.yml # build + publish Release
```

Git-ignored: `build/`, `KoboRoot.tgz`.

## Phases

### 0. Frame
- [x] CLAUDE.md, PLAN.md, TODO.md
- [x] Verify target filenames/names against firmware → `FIRMWARE.md`
- [x] Decide build approach → single `build.py`, bundled fonttools

### 1. Scripts (no real font needed)
- [ ] `.gitignore`, `vendor/` wheel, `sources/README.md`
- [ ] `targets.py`
- [ ] `fontsource.py` — pick styles by `usWeightClass` + italic bit from the
      zip's static fonts; clear error if a style is missing or ambiguous
- [ ] `verify.py` — checks from CLAUDE.md, one line per failure
- [ ] `rebrand.py` — name IDs 1, 2, 3, 4, 6, 16, 17 (21/22 if present);
      drop the source name elsewhere; weight per target table
- [ ] `build.py` — pipeline + tgz with `tarfile` + read-back check
- [ ] Test with a throwaway zip (built from an open font) that the checks
      both pass and fail as expected

### 2. CI + release
- [ ] GitHub Actions: run `build.py` on push to `sources/` or scripts,
      upload tgz, publish Release

### 3. Real font  `[!]` TODO B1
- [ ] User adds the Google Fonts zip to `sources/`
- [ ] `python3 build.py` passes locally and in CI

### 4. Docs + device test
- [ ] README: what it is, download + install (Mac/Windows hidden `.kobo`),
      how to build, font credit + license, undo, firmware-update note
- [ ] User installs on device, records result in TODO W2

## Done when

`python3 build.py` on a clean checkout produces `KoboRoot.tgz` with all
checks passing, CI publishes the same as a Release, and the device test in
TODO W2 is recorded.
