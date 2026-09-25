#!/usr/bin/env python3
"""Build KoboRoot.tgz: Vietnamese-capable Kobo UI fonts.

Usage:  python3 build.py        (Windows: py build.py)
Needs only Python 3.9+. fonttools is bundled in vendor/.
"""

import gzip
import io
import sys
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"
OUT = ROOT / "build"
TGZ = OUT / "KoboRoot.tgz"

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(errors="replace")  # Windows consoles without UTF-8
    except AttributeError:
        pass

if sys.version_info < (3, 9):
    sys.exit(f"❌ Python 3.9 or newer is needed (this is {sys.version.split()[0]}).")

wheels = sorted((ROOT / "vendor").glob("fonttools-*.whl"))
if not wheels:
    sys.exit("❌ vendor/fonttools-*.whl is missing. Re-download the repository.")
sys.path[:0] = [str(wheels[-1]), str(ROOT)]

from scripts import fonts, verify  # noqa: E402
from scripts.targets import FONT_DIR, TARGETS  # noqa: E402


def fail(step, errors):
    print(f"❌ {step} failed:")
    for e in errors:
        print(f"   - {e}")
    sys.exit(1)


def write_tgz(outputs):
    """Regular files only, no directory entries: extracting over / must not
    touch existing directories' owner or mode."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        for filename in sorted(outputs):
            data = outputs[filename]
            info = tarfile.TarInfo(f"{FONT_DIR}/{filename}")
            info.size, info.mode, info.mtime = len(data), 0o644, 0
            info.uid = info.gid = 0
            info.uname = info.gname = "root"
            tar.addfile(info, io.BytesIO(data))
    with open(TGZ, "wb") as f, gzip.GzipFile(fileobj=f, mode="wb", mtime=0) as gz:
        gz.write(buf.getvalue())


def check_tgz(outputs):
    errors, seen = [], {}
    with tarfile.open(TGZ, "r:gz") as tar:
        for m in tar.getmembers():
            if not m.isfile() or not m.name.startswith(FONT_DIR + "/"):
                errors.append(f"unexpected entry: {m.name}")
                continue
            if m.mode != 0o644 or m.uid != 0 or m.gid != 0:
                errors.append(f"{m.name}: mode {oct(m.mode)} uid {m.uid} gid {m.gid}")
            seen[m.name[len(FONT_DIR) + 1:]] = tar.extractfile(m).read()
    if seen != outputs:
        errors.append("archive contents differ from the checked fonts")
    return errors


def main():
    print(f"Reading fonts from {SOURCES.relative_to(ROOT)}/")
    picked, errors = fonts.load_sources(SOURCES)
    if errors:
        fail("Finding source fonts", errors)
    for style, (label, _, _) in picked.items():
        print(f"   {style:<11} {label}")
    source_family = fonts.family_name(picked["Regular"][2])

    errors = verify.check_sources(picked)
    if errors:
        fail("Source font check", errors)
    print(f"✅ Source fonts OK ({source_family})")

    outputs = {}
    for filename, family, subfamily, weight, style in TARGETS:
        font = fonts.rebrand(picked[style][1], family, subfamily, weight)
        buf = io.BytesIO()
        font.save(buf)
        outputs[filename] = buf.getvalue()

    errors = verify.check_outputs(outputs, source_family)
    if errors:
        fail("Output font check", errors)
    print(f"✅ {len(outputs)} Kobo fonts OK")

    OUT.mkdir(exist_ok=True)
    (OUT / "fonts").mkdir(exist_ok=True)
    for filename, data in outputs.items():
        (OUT / "fonts" / filename).write_bytes(data)
    write_tgz(outputs)
    errors = check_tgz(outputs)
    if errors:
        fail("Archive check", errors)
    print(f"✅ Built {TGZ.relative_to(ROOT)}")
    print("   Copy it into the .kobo folder on your Kobo, eject, and let it restart.")


if __name__ == "__main__":
    main()
