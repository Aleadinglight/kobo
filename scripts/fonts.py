"""Load the source fonts and rebrand them into the stock UI font names."""

import io
import zipfile
from pathlib import Path

from fontTools.ttLib import TTFont

from .targets import STYLES

RIBBI = {"Regular": "Regular", "Bold": "Bold", "Italic": "Italic", "Bold Italic": "BoldItalic"}

# Name IDs we set ourselves, or drop because they carry the source name.
REPLACED_IDS = {1, 2, 3, 4, 6, 16, 17, 21, 22, 25}


def family_name(font):
    name = font["name"]
    return name.getDebugName(16) or name.getDebugName(1)


def _style_name(font):
    name = font["name"]
    return name.getDebugName(17) or name.getDebugName(2)


def _candidates(src_dir):
    """Yield (label, bytes) for every .ttf in src_dir and inside any .zip there."""
    for path in sorted(Path(src_dir).iterdir()):
        if path.suffix.lower() == ".ttf":
            yield path.name, path.read_bytes()
        elif path.suffix.lower() == ".zip":
            with zipfile.ZipFile(path) as z:
                for member in sorted(z.namelist()):
                    if member.lower().endswith(".ttf") and "/__MACOSX/" not in "/" + member:
                        yield f"{path.name}:{member}", z.read(member)


def load_sources(src_dir):
    """Pick one font per style. Returns ({style: (label, bytes, TTFont)}, errors)."""
    found, variable = {}, []
    for label, data in _candidates(src_dir):
        font = TTFont(io.BytesIO(data))
        if "fvar" in font:
            variable.append(label)
            continue
        style = RIBBI.get(_style_name(font))
        if style is None or font["OS/2"].usWidthClass != 5:
            continue  # other weights (Light, Black...) and widths (Condensed...)
        found.setdefault(style, []).append((label, data, font))

    errors, picked = [], {}
    for style in STYLES:
        hits = found.get(style, [])
        if len(hits) == 1:
            picked[style] = hits[0]
        elif not hits:
            hint = " Only variable fonts were found; use the static files." if variable else ""
            errors.append(f"No {style} font found in {Path(src_dir).name}/.{hint}")
        else:
            errors.append(f"More than one {style} font: " + ", ".join(h[0] for h in hits))
    return picked, errors


def rebrand(source_bytes, family, subfamily, weight):
    """Return a TTFont with the source outlines under the stock family/subfamily name."""
    # Keep head.modified from the source so rebuilds are byte-identical.
    font = TTFont(io.BytesIO(source_bytes), recalcTimestamp=False)
    old_family = family_name(font)
    old_tokens = {old_family.lower(), old_family.replace(" ", "").lower()}

    name = font["name"]
    name.names = [
        r for r in name.names
        if r.nameID not in REPLACED_IDS
        and not any(t in r.toUnicode().lower() for t in old_tokens)
    ]
    ps_name = f"{family}-{subfamily}".replace(" ", "")
    full_name = family if subfamily == "Regular" else f"{family} {subfamily}"
    for name_id, value in {1: family, 2: subfamily, 3: ps_name, 4: full_name, 6: ps_name}.items():
        name.setName(value, name_id, 3, 1, 0x409)

    # STAT points at the source's style names; Qt 4.6 doesn't use it.
    if "STAT" in font:
        del font["STAT"]

    font["OS/2"].usWeightClass = weight
    return font
