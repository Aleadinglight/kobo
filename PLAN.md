# PLAN.md

Implementation plan for the Vietnamese Kobo UI font build. Rules and
background: `CLAUDE.md`. Open questions: `TODO.md`.

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done ·
`[!]` blocked (see TODO.md)

## Layout

```
kobo/
├── CLAUDE.md
├── PLAN.md
├── TODO.md
├── README.md               # install steps, real font name, license, limits
├── requirements.txt        # fonttools (pinned)
├── build.sh                # single entry point
├── sources/                # 4 static TTFs + license (OFL.txt)
│   ├── <Source>-Regular.ttf
│   ├── <Source>-Bold.ttf
│   ├── <Source>-Italic.ttf
│   ├── <Source>-BoldItalic.ttf
│   └── OFL.txt
└── scripts/
    ├── targets.py          # the 16-row table + style → source mapping
    ├── verify.py           # --sources / --outputs, hard fail
    ├── rebrand.py          # rewrite name table, save to stock filename
    └── inspect_tgz.py      # diagnostic: weights + hashes of an existing tgz
```

Generated (git-ignored): `.venv/`, `build/fonts/` (16 outputs),
`root/usr/...` (staging), `KoboRoot.tgz`.

## Phases

### Phase 0 — Frame
- [x] `CLAUDE.md` rules, `PLAN.md`, `TODO.md`
- [ ] `.gitignore`, `requirements.txt`

### Phase 1 — Source fonts  `[!]` blocked by TODO B1, B2
- [ ] Obtain 4 static TTFs (Regular, Bold, Italic, BoldItalic) + license
- [ ] Record origin URL / version in README

### Phase 2 — `verify.py --sources`
Each check prints PASS/FAIL per file; any FAIL → exit 1.
- [ ] `OS/2.usWeightClass`: 400 Regular/Italic, 700 Bold/BoldItalic
- [ ] SHA-256: 4 distinct
- [ ] Italic bit: `OS/2.fsSelection` bit 0 and `head.macStyle` bit 1 set on
      italics, clear on uprights; Bold bit (fsSelection bit 5 / macStyle
      bit 0) consistent too
- [ ] `fvar` absent
- [ ] `glyf` present, `CFF `/`CFF2` absent
- [ ] Vietnamese: every precomposed letter in the Vietnamese alphabet
      (upper + lower, all tones) plus `đ Đ ₫` present in the cmap

### Phase 3 — `rebrand.py`
- [ ] For each of the 16 targets: load the source for its style, rewrite
      name IDs 1, 2, 3, 4, 6, 16, 17 (and 21/22 if present); drop IDs that
      carry the source name (trademark, manufacturer, etc.) or replace them
- [ ] Keep license name IDs (13, 14) — OFL requires the license stay
- [ ] Save to `build/fonts/<exact stock filename>`

### Phase 4 — `verify.py --outputs`
- [ ] Exactly 16 files, filenames == target table (no extras, no missing)
- [ ] Weight and italic checks as Phase 2, per target style
- [ ] Hashes: files of the same style may match (same source); files of
      different styles must not
- [ ] Name ID 1/2 (and 16/17 if present) == target family/subfamily
- [ ] Source family name (e.g. "Noto") absent from every name record, except
      license text (ID 13/14) — see TODO W3
- [ ] Vietnamese coverage as Phase 2

### Phase 5 — Package (`build.sh`)
- [ ] venv create + `pip install -r requirements.txt` (idempotent)
- [ ] Run phases 2 → 4, stop on first failure
- [ ] Stage into `root/usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts/`
- [ ] Delete `.DS_Store` and `._*`
- [ ] `COPYFILE_DISABLE=1 tar -czf KoboRoot.tgz -C root usr`
- [ ] `tar -tzf` check: every entry starts `usr/`, exactly 16 `.ttf`, no junk

### Phase 6 — Docs
- [ ] README: what it does, install, real font name + license, known limits,
      how to rebuild after firmware update

### Phase 7 — Bold UI diagnostic  `[!]` blocked by TODO B3
- [ ] `inspect_tgz.py <old KoboRoot.tgz>`: print weight + hash per file
- [ ] If weights were correct: build the Bold-with-Regular-outlines test tgz

## Definition of done

`./build.sh` on a clean checkout produces `KoboRoot.tgz`, both verify passes
print all PASS, and `tar -tzf` lists exactly the 16 paths under `usr/`.
Device test (render Vietnamese in menus) is done by the user and recorded
in TODO.md.
