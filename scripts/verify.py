"""Checks that gate the build. Each function returns a list of error strings."""

import hashlib
import io
import unicodedata

from fontTools.ttLib import TTFont

from .targets import STYLES, TARGETS

# Every precomposed Vietnamese letter (12 vowels x 5 tones + bare), both
# cases, plus đ/Đ and the dong sign.
_VOWELS = "aăâeêioôơuưy"
_TONES = ["", "\u0300", "\u0301", "\u0309", "\u0303", "\u0323"]  # grave acute hook tilde dot
VIETNAMESE = sorted(
    {unicodedata.normalize("NFC", v + t) for v in _VOWELS for t in _TONES}
    | {unicodedata.normalize("NFC", v.upper() + t) for v in _VOWELS for t in _TONES}
    | set("đĐ₫")
)


def _flag(font, fs_bit, mac_bit):
    """True/False if OS/2.fsSelection and head.macStyle agree, None if they don't."""
    fs, mac = bool(font["OS/2"].fsSelection & fs_bit), bool(font["head"].macStyle & mac_bit)
    return fs if fs == mac else None


def _font_checks(label, font, weight, italic, bold):
    """bold: True for Bold/BoldItalic styles. Catches Regular outlines in a
    Bold slot even when the weight number was rewritten."""
    errors = []
    actual = font["OS/2"].usWeightClass
    if actual != weight:
        errors.append(f"{label}: weight is {actual}, expected {weight}")
    if _flag(font, 1, 2) is not italic:
        errors.append(f"{label}: italic flag should be {'on' if italic else 'off'}")
    if _flag(font, 32, 1) is not bold:
        errors.append(f"{label}: bold flag should be {'on' if bold else 'off'}")
    if "fvar" in font:
        errors.append(f"{label}: variable font; Kobo needs static fonts")
    if "glyf" not in font or "CFF " in font or "CFF2" in font:
        errors.append(f"{label}: needs TrueType (glyf) outlines, not CFF")
    cmap = font.getBestCmap() or {}
    missing = [c for c in VIETNAMESE if ord(c) not in cmap]
    if missing:
        errors.append(f"{label}: missing {len(missing)} Vietnamese characters: {''.join(missing[:20])}")
    return errors


def check_sources(picked):
    """picked: {style: (label, bytes, TTFont)} from fonts.load_sources."""
    errors = []
    for style, (label, _, font) in picked.items():
        weight, italic = STYLES[style]
        errors += _font_checks(f"{label} ({style})", font, weight, italic, weight == 700)
    hashes = {hashlib.sha256(data).hexdigest() for _, data, _ in picked.values()}
    if len(hashes) != len(picked):
        errors.append("Some source styles are the same file (identical hashes)")
    return errors


def check_outputs(outputs, source_family):
    """outputs: {filename: bytes} as written. Re-reads every file from bytes."""
    errors = []
    expected = {t[0] for t in TARGETS}
    if set(outputs) != expected:
        errors.append(f"Output files differ from targets: extra {sorted(set(outputs) - expected)}, "
                      f"missing {sorted(expected - set(outputs))}")

    style_by_hash = {}
    tokens = {source_family.lower(), source_family.replace(" ", "").lower()}
    for filename, family, subfamily, weight, style in TARGETS:
        if filename not in outputs:
            continue
        data = outputs[filename]
        font = TTFont(io.BytesIO(data))
        src_weight, italic = STYLES[style]
        errors += _font_checks(filename, font, weight, italic, src_weight == 700)

        name = font["name"]
        if name.getDebugName(1) != family or name.getDebugName(2) != subfamily:
            errors.append(f"{filename}: named '{name.getDebugName(1)} / {name.getDebugName(2)}', "
                          f"expected '{family} / {subfamily}'")
        for r in name.names:
            if any(t in r.toUnicode().lower() for t in tokens):
                errors.append(f"{filename}: name ID {r.nameID} still mentions '{source_family}'")

        style_by_hash.setdefault(hashlib.sha256(data).hexdigest(), set()).add(style)
    for styles in style_by_hash.values():
        if len(styles) > 1:
            errors.append(f"Different styles produced identical files: {sorted(styles)}")
    return errors
