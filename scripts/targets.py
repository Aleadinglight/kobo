"""The 16 stock UI font files we replace. Verified against firmware: docs/FIRMWARE.md."""

FONT_DIR = "usr/local/Trolltech/QtEmbedded-4.6.2-arm/lib/fonts"

# Source style -> (usWeightClass, italic) that the source file must have.
STYLES = {
    "Regular": (400, False),
    "Bold": (700, False),
    "Italic": (400, True),
    "BoldItalic": (700, True),
}

# (filename, family, subfamily, weight, source style)
TARGETS = [
    ("RakutenSansUIApp-Regular.ttf", "Rakuten Sans", "Regular", 400, "Regular"),
    ("RakutenSansUIApp-Bold.ttf", "Rakuten Sans", "Bold", 700, "Bold"),
    ("RakutenSansUIApp-Italic.ttf", "Rakuten Sans", "Italic", 400, "Italic"),
    ("RakutenSansUIApp-BoldItalic.ttf", "Rakuten Sans", "Bold Italic", 700, "BoldItalic"),
    ("RakutenSerifApp-Regular.ttf", "Rakuten Serif", "Regular", 400, "Regular"),
    ("RakutenSerifApp-Bold.ttf", "Rakuten Serif", "Bold", 700, "Bold"),
    ("RakutenSerifApp-Italic.ttf", "Rakuten Serif", "Italic", 400, "Italic"),
    ("RakutenSerifApp-BoldItalic.ttf", "Rakuten Serif", "Bold Italic", 700, "BoldItalic"),
    ("Avenir.ttf", "Avenir Next", "Medium", 500, "Regular"),
    ("Avenir-Bold.ttf", "Avenir Next", "Bold", 700, "Bold"),
    ("Avenir-Italic.ttf", "Avenir Next", "Medium Italic", 500, "Italic"),
    ("Avenir-BoldItalic.ttf", "Avenir Next", "Bold Italic", 700, "BoldItalic"),
    ("georgia.ttf", "Georgia", "Regular", 400, "Regular"),
    ("georgiab.ttf", "Georgia", "Bold", 700, "Bold"),
    ("georgiai.ttf", "Georgia", "Italic", 400, "Italic"),
    ("georgiaz.ttf", "Georgia", "Bold Italic", 700, "BoldItalic"),
]
