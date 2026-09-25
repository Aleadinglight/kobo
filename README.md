# Vietnamese system UI font for Kobo

Replaces the Kobo's **system UI font** with
[Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans)
([SIL Open Font License](sources/OFL.txt)), which covers every Vietnamese
letter. The system UI font is the one the Kobo uses for its own screens:
library, book titles and authors, menus, settings, table of contents,
reading progress. With the stock font, Vietnamese there shows as boxes or
broken accents.

It does **not** change the **book font** (the text inside a book). That's a
separate reading font you choose yourself; see [Custom book fonts](#custom-book-fonts).

Tested on **Kobo Libra H2O** (firmware 4.38.23697) and **Kobo Clara BW**
(firmware 4.45).

## Installation

1. Download `KoboRoot.tgz` from the latest
   [Release](https://github.com/Aleadinglight/kobo/releases/latest).
2. Copy it into the hidden `.kobo` folder on the Kobo drive.
3. Eject. The Kobo updates and restarts.

Full guide (Mac/Windows steps, checking it worked, troubleshooting, undo):
**[docs/INSTALL.md](docs/INSTALL.md)**.

## Custom book fonts

This project doesn't change the book font. To add your own book font:

1. Download a Vietnamese-capable font, e.g.
   [Literata](https://fonts.google.com/specimen/Literata) or
   [Noto Serif](https://fonts.google.com/noto/specimen/Noto+Serif) from
   Google Fonts. Use the static `.ttf` files.
2. Copy them into the `fonts` folder at the top of the Kobo drive (next to
   `.kobo`; create it if it's missing).
3. Eject.

## Use your own font

1. Clone this repository.
2. Replace the files in `sources/` with your font's four static `.ttf` files
   (Regular, Bold, Italic, Bold Italic) and its license. A Google Fonts zip
   ("Download family") dropped in `sources/` also works.
3. Build (needs only Python 3.9+):

   ```sh
   python3 build.py        # Windows: py build.py
   ```

4. Copy `build/KoboRoot.tgz` to the Kobo as in [Installation](#installation).

If your font isn't suitable, the build stops and says why.

## FAQ

**What does the build do?**

1. Picks your font's Regular, Bold, Italic and Bold Italic from `sources/`
   and checks them (correct weights and styles, full Vietnamese coverage).
2. Makes 16 copies, one per Kobo system UI font file, and in each one:
   - renames the font's **internal name** to the Kobo's (e.g. *Noto Sans
     Bold* → *Rakuten Sans Bold*). The Kobo finds fonts by this name.
   - saves it under the Kobo's **exact filename** (e.g.
     `RakutenSansUIApp-Bold.ttf`), so it overwrites the original.
3. Checks the 16 results again.
4. Packs them into `KoboRoot.tgz`, set to unpack into the Kobo's system font
   folder.

**Which built-in book fonts already support Vietnamese?**

See [docs/FIRMWARE.md](docs/FIRMWARE.md#built-in-reading-fonts-vietnamese-coverage).
On Clara BW: Bitter, Noto Sans, Texturina, Vollkorn. On Libra H2O: none, so
add your own.

**Where are the technical details and project status?**

[docs/FIRMWARE.md](docs/FIRMWARE.md) (what the Kobo firmware contains),
[docs/PLAN.md](docs/PLAN.md) and [docs/TODO.md](docs/TODO.md).
