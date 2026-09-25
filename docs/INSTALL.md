# Installation

For Kobo Libra H2O (firmware 4.38.23697) and Kobo Clara BW (firmware 4.45).

1. Download **KoboRoot.tgz** from the
   [latest release](https://github.com/Aleadinglight/kobo/releases/latest).
   Keep the name exactly `KoboRoot.tgz`.

   > **Mac + Safari:** Safari may unpack it into `KoboRoot.tar`. Download
   > with Chrome or Firefox instead, or turn off Safari → Settings → General
   > → *Open "safe" files after downloading*.

2. Connect the Kobo to your computer with USB and tap **Connect**.

3. On the Kobo drive, show hidden files (Mac: `Cmd + Shift + .` in Finder;
   Windows: File Explorer → View → Show → Hidden items) and copy the file
   **into the `.kobo` folder**:

   ```
   KOBOeReader/            ← the Kobo drive
   └── .kobo/              ← hidden folder
       └── KoboRoot.tgz    ← put it here
   ```

4. Eject the Kobo. It installs the file and restarts.

## Troubleshooting

| Problem | Fix |
|---|---|
| Nothing changed, or `KoboRoot.tgz` is still in `.kobo` | Check the name is exactly `KoboRoot.tgz` and it's inside `.kobo`, then eject properly before unplugging. |
| Book text shows boxes | That's the book font, not the system UI font. See [Custom book fonts](https://github.com/Aleadinglight/kobo#custom-book-fonts). |
| UI text looks bold | [Open an issue](https://github.com/Aleadinglight/kobo/issues) with your model, firmware version and a photo. |
| Original font is back after a Kobo update | Copy the same `KoboRoot.tgz` into `.kobo` again. |
| Want to undo | Reinstall the official Kobo firmware, or wait for the next Kobo update. |
