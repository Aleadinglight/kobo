# Install guide: Vietnamese UI fonts for Kobo

`KoboRoot.tgz` replaces the Kobo's **system UI font** (the font of the
Kobo's own screens: library, book titles, menus, settings, table of
contents, reading progress) with Noto Sans, so Vietnamese displays
correctly there. It does **not** change the **book font**; your books,
settings and reading-font choice are not touched.

**Works on:** Kobo Libra H2O (firmware 4.38.23697) and Kobo Clara BW
(firmware 4.45). Check yours under **Settings → Device information**.

## 1. Download

Download `KoboRoot.tgz` from the
[latest release](https://github.com/Aleadinglight/kobo/releases/latest).

- Keep the name exactly `KoboRoot.tgz`. If your browser saved it as
  `KoboRoot (1).tgz`, rename it.
- **Mac + Safari:** Safari may unpack it into `KoboRoot.tar` or a folder.
  If so, download again with Chrome or Firefox, or turn off Safari →
  Settings → General → *Open "safe" files after downloading*.

## 2. Copy it to the Kobo

1. Connect the Kobo to your computer with USB and tap **Connect** on the
   Kobo.
2. Open the Kobo drive (usually named `KOBOeReader`).
3. Show hidden files so the `.kobo` folder appears:
   - **Mac:** in Finder press `Cmd + Shift + .`
   - **Windows:** File Explorer → **View** → **Show** → **Hidden items**
4. Copy `KoboRoot.tgz` **into** the `.kobo` folder:

   ```
   KOBOeReader/
   └── .kobo/
       └── KoboRoot.tgz   ← here
   ```

5. Eject the Kobo (Mac: eject button in Finder; Windows: *Safely Remove
   Hardware*), then unplug it.

The Kobo shows an update screen and restarts. This takes about a minute.

## 3. Check it worked

- Book titles and authors with Vietnamese accents display correctly in the
  library, e.g. *Truyện Kiều*, *Nguyễn Du*.
- Menus and the table of contents show no boxes (□) or broken accents.
- UI text looks normal weight, not bold.
- Connect the Kobo again: `.kobo/KoboRoot.tgz` is gone. The Kobo deletes it
  after installing.

## Troubleshooting

| Problem | Fix |
|---|---|
| No update screen, nothing changed | The file wasn't found. Check it's named exactly `KoboRoot.tgz` and is inside `.kobo`, not next to it. Then eject properly. |
| `KoboRoot.tgz` is still in `.kobo` after restart | Same as above: wrong name or location, or the Kobo wasn't ejected before unplugging. |
| Menus are fine, but the **book text** has boxes | That's the book font, not the system UI font. Pick a reading font that covers Vietnamese in the **Aa** menu, or add one: copy its `.ttf` files into the `fonts` folder at the top of the Kobo drive (next to `.kobo`). See [README](https://github.com/Aleadinglight/kobo#reading-fonts). |
| UI text looks bold | Please [open an issue](https://github.com/Aleadinglight/kobo/issues) with your model, firmware version and a photo. |

## After a Kobo firmware update

Firmware updates put the original fonts back. Copy the same `KoboRoot.tgz`
into `.kobo` again.

## Undo

Reinstall the official firmware for your model (search Kobo Help for
"manually update your Kobo eReader"), or wait for the next firmware update.
Either restores the original fonts.

## Credits

UI font: [Noto Sans](https://fonts.google.com/noto/specimen/Noto+Sans)
v2.015, © The Noto Project Authors, SIL Open Font License 1.1. Its internal
names are changed so the Kobo uses it as its UI font; the letters themselves
are unchanged.
