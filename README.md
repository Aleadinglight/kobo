# Vietnamese UI fonts for Kobo

Makes the Kobo interface (library, book titles, menus, table of contents,
reading progress) show Vietnamese correctly instead of boxes or broken
accents.

Tested targets: **Kobo Libra H2O** (firmware 4.38.23697) and **Kobo Clara BW**
(firmware 4.45).

## UI fonts vs. reading fonts

A Kobo uses two separate sets of fonts:

| | UI fonts | Reading fonts |
|---|---|---|
| Used for | Library, book titles, menus, table of contents, progress | The text of the book you're reading |
| Chosen by | The Kobo itself, you can't pick them | You, in the **Aa** menu while reading |
| Stored in | Hidden system folder inside the Kobo | Built in, plus the `fonts` folder on the Kobo drive |
| Changed by | **This project** (`KoboRoot.tgz`) | Copying `.ttf` files into `fonts` |

This project only replaces the **UI fonts**, with **Noto Sans**, which covers
every Vietnamese letter. Your books and your reading-font choice are not
touched.

### Vietnamese in book text

Book text uses whatever reading font you pick, so that font must support
Vietnamese too. Built-in reading fonts that fully cover Vietnamese:

| Device | Built-in reading fonts with full Vietnamese |
|---|---|
| Clara BW (4.45) | Bitter, Noto Sans, Texturina, Vollkorn |
| Libra H2O (4.38) | none |

If yours isn't in the list, or accents show as boxes in a book, add your own
reading font:

1. Connect the Kobo with USB.
2. Open the Kobo drive. At the top level (next to `.kobo`, not inside it),
   create a folder named `fonts` if it isn't there.
3. Copy a Vietnamese-capable font's `.ttf` files into it, e.g. Noto Serif or
   Literata from Google Fonts. Use the static files, named like
   `Family-Regular.ttf`, `Family-Bold.ttf`, `Family-Italic.ttf`,
   `Family-BoldItalic.ttf`.
4. Eject. The font appears in the **Aa** menu while reading.

No `KoboRoot.tgz` is needed for reading fonts, and they survive firmware
updates.

## Install

1. Download `KoboRoot.tgz` from the latest
   [Release](https://github.com/Aleadinglight/kobo/releases/latest).
2. Copy it into the hidden `.kobo` folder on the Kobo drive.
3. Eject. The Kobo updates and restarts.

Full guide with Mac/Windows steps, how to check it worked, troubleshooting
and undo: **[docs/INSTALL.md](docs/INSTALL.md)**.

## Build it yourself

You only need **Python 3.9 or newer**. Nothing else to install, no internet.

```sh
python3 build.py        # Windows: py build.py
```

The result is `build/KoboRoot.tgz`. The build checks every font before and
after conversion and stops with a plain message if anything is wrong.

To use a different font, replace the files in `sources/` with that font's
four static `.ttf` files (Regular, Bold, Italic, Bold Italic) and its license,
or just drop in the zip from Google Fonts ("Download family"). The font must
cover Vietnamese; the build will tell you if it doesn't.

## Font and license

The UI font is [Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans)
v2.015, © The Noto Project Authors, under the SIL Open Font License 1.1 (see
[`sources/OFL.txt`](sources/OFL.txt)). Inside `KoboRoot.tgz` its internal
names are changed to the Kobo UI font names so the Kobo picks it up; the font
itself is unchanged.

The build uses [fontTools](https://github.com/fonttools/fonttools) (MIT),
bundled in `vendor/`.
