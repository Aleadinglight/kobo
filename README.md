# Kobo tiếng Việt: Vietnamese UI fonts for Kobo

Makes the Kobo interface (library, book titles, menus, table of contents,
reading progress) show Vietnamese correctly instead of boxes or broken
accents.

It replaces the system UI fonts with **Noto Sans**, which covers every
Vietnamese letter. Book text is not affected; choose any reading font as
usual.

Tested targets: **Kobo Libra H2O** (firmware 4.38.23697) and **Kobo Clara BW**
(firmware 4.45).

## Install

1. Download `KoboRoot.tgz` from the latest
   [Release](../../releases/latest).
2. Connect the Kobo to your computer with USB and tap **Connect**.
3. Open the Kobo drive and show hidden files so the `.kobo` folder appears:
   - **Mac:** in Finder press `Cmd + Shift + .`
   - **Windows:** File Explorer → **View** → **Show** → **Hidden items**
4. Copy `KoboRoot.tgz` into the `.kobo` folder. Don't rename it.
5. Eject the Kobo and unplug it. It shows an update screen and restarts.

After a Kobo firmware update the original fonts come back. Just repeat the
steps with the same `KoboRoot.tgz`.

**Undo:** install the official firmware again (Kobo's "manual update"
instructions), or wait for the next firmware update.

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
