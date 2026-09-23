# PLAN.md

Plan and progress. Rules: `CLAUDE.md`. Questions: `TODO.md`.

Status: `[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked

## Layout

```
kobo/
├── CLAUDE.md  PLAN.md  TODO.md  README.md
├── requirements.txt        # fonttools, pinned
├── build.sh                # single entry point
├── sources/                # user-provided: 4 static TTFs + license
└── scripts/
    ├── targets.py          # 16-row table, style names, weights
    ├── verify.py           # --sources / --outputs
    ├── rebrand.py          # name-table rewrite → build/fonts/
    └── inspect_tgz.py      # print weight + hash of fonts in any tgz
```

Git-ignored: `.venv/`, `build/`, `root/`, `KoboRoot.tgz`.

## Phases

### 0. Frame
- [x] CLAUDE.md, PLAN.md, TODO.md
- [x] Verify target filenames/names against firmware → `FIRMWARE.md`
- [ ] `.gitignore`, `requirements.txt`, `sources/README` (what to drop in)

### 1. Scripts (no real font needed)
- [ ] `targets.py`
- [ ] `verify.py` — sources + outputs checks from CLAUDE.md, PASS/FAIL per
      check, exit 1 on any FAIL
- [ ] `rebrand.py` — rewrite name IDs 1, 2, 3, 4, 6, 16, 17 (21/22 if
      present); scrub source name from others; save to exact filename
- [ ] `inspect_tgz.py`
- [ ] Self-test with a throwaway font (e.g. generated or a system TTF) to
      prove each check can fail and pass. Not committed as a real source.

### 2. Build
- [ ] `build.sh` — venv, verify → rebrand → verify, stage, clean, tar, list

### 3. Real sources  `[!]` TODO B1
- [ ] User adds fonts to `sources/`
- [ ] `./build.sh` passes

### 4. Docs + device test
- [ ] README: what it is, font credit + license, install, test, uninstall,
      firmware-update note
- [ ] User installs on device, records result in TODO W2

## Done when

`./build.sh` on a clean checkout produces `KoboRoot.tgz`, both verify passes
are all PASS, `tar -tzf` lists exactly the target fonts under `usr/`, and the device
test in TODO W2 is recorded.
