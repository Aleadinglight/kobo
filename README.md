# Vietnamese UI fonts for Kobo

Makes the Kobo interface (library, book titles, menus, table of contents,
reading progress) show Vietnamese correctly instead of boxes or broken
accents. It replaces the Kobo's UI fonts with
[Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans)
([SIL Open Font License](sources/OFL.txt)), which covers every Vietnamese
letter. Your books and reading-font choice are not touched.

Tested on **Kobo Libra H2O** (firmware 4.38.23697) and **Kobo Clara BW**
(firmware 4.45).

## Install

1. Download `KoboRoot.tgz` from the latest
   [Release](https://github.com/Aleadinglight/kobo/releases/latest).
2. Copy it into the hidden `.kobo` folder on the Kobo drive.
3. Eject. The Kobo updates and restarts.

Full guide (Mac/Windows steps, checking it worked, troubleshooting, undo):
**[docs/INSTALL.md](docs/INSTALL.md)**.

## Reading fonts

This project only changes the interface. For **book text**, pick a reading
font that supports Vietnamese in the **Aa** menu, or add your own: copy its
`.ttf` files into the `fonts` folder at the top of the Kobo drive (next to
`.kobo`, create it if missing), then eject. No `KoboRoot.tgz` needed.

## Use your own font

1. Clone this repository.
2. Replace the files in `sources/` with your font's four static `.ttf` files
   (Regular, Bold, Italic, Bold Italic) and its license. A Google Fonts zip
   ("Download family") dropped in `sources/` also works.
3. Build (needs only Python 3.9+):

   ```sh
   python3 build.py        # Windows: py build.py
   ```

4. Copy `build/KoboRoot.tgz` to the Kobo as in [Install](#install).

The build checks the font (weights, styles, Vietnamese coverage) and stops
with a plain message if something is wrong.

## More

- [docs/FIRMWARE.md](docs/FIRMWARE.md): what the Kobo firmware contains, and
  which built-in reading fonts cover Vietnamese
- [docs/PLAN.md](docs/PLAN.md), [docs/TODO.md](docs/TODO.md): project
  progress and open items
