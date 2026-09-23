# FIRMWARE.md

What the stock firmware actually contains. Every fact here has the command
that produced it. Checked 2026-09-23.

## Firmware checked

| Device (assumed) | Platform | Version | URL |
|---|---|---|---|
| Libra H2O | kobo7 | 4.38.23697 | `https://ereaderfiles.kobo.com/firmwares/kobo7/May2026/kobo-update-4.38.23697.zip` |
| (Libra 2, reference) | kobo9 | 4.38.23697 | `https://ereaderfiles.kobo.com/firmwares/kobo9/May2026/kobo-update-4.38.23697.zip` |
| Clara BW | kobo12 | 4.45.23697 | `https://ereaderfiles.kobo.com/firmwares/kobo12/May2026/kobo-update-4.45.23697.zip` |

URLs from Kobo's update API:

```sh
curl -sS "https://api.kobobooks.com/1.0/UpgradeCheck/Device/00000000-0000-0000-0000-000000000<ID>/kobo/4.0.0/N0"
```

Libra H2O: user confirmed firmware 4.38.23697; the kobo7 zip contains
`zImage-E70K00` (Libra H2O board, assumed). Clara BW → kobo12 is an
assumption; confirm the version under Settings → Device information (should
start with 4.45).

The Libra 2 (kobo9) zip was checked first by mistake. Its 16 UI font files
are byte-identical to Libra H2O's:

```sh
# per file: compare sha256 of kobo9 and kobo7 copies → all 16 "same"
[ "$(sha256sum < kobo9/$f)" = "$(sha256sum < kobo7/$f)" ] && echo same
```

## Font directory listing

```sh
unzip -o -q kobo-update-*.zip KoboRoot.tgz
tar -tzf KoboRoot.tgz | grep 'QtEmbedded-4.6.2-arm/lib/fonts/'
```

UI font files present:

| File | Libra H2O | Clara BW |
|---|---|---|
| RakutenSansUIApp-{Regular,Bold,Italic,BoldItalic}.ttf | yes | yes |
| RakutenSerifApp-{Regular,Bold,Italic,BoldItalic}.ttf | yes | yes |
| Avenir.ttf, Avenir-{Bold,Italic,BoldItalic}.ttf | yes | **no** |
| georgia.ttf, georgia{b,i,z}.ttf | yes | **no** |

- Sans bold-italic is `RakutenSansUIApp-BoldItalic.ttf`. `BoldItali` was a
  typo.
- The 8 Rakuten files are byte-identical on Clara BW and Libra 2 (and so
  Libra H2O):
  `sha256sum */Rakuten* | awk '{print $1}' | sort | uniq -c` → 8 hashes,
  each seen twice.

## Stock files are wrapped, not plain TTF

```sh
od -A x -t x1 -N 16 RakutenSansUIApp-Regular.ttf
# 51 54 44 00 01 57 38 78 da ...
```

Layout: `"QTD"` (3 bytes) + uncompressed length (uint32 big-endian) + zlib
stream. Unwrapping with `zlib.decompress(data[7:])` gives a normal TTF (or a
TTC), and the length matches for all files.

Open question: does nickel also load **plain** TTF at these paths? See
`TODO.md`.

## Name table and metrics (after unwrapping)

Read with fonttools 4.65.0 (`name` IDs 1/2, `OS/2.usWeightClass`,
`OS/2.fsSelection`).

| File | Family (ID 1) | Subfamily (ID 2) | Weight | fsSelection | Format |
|---|---|---|---|---|---|
| RakutenSansUIApp-Regular | Rakuten Sans | Regular | 400 | 0x00c0 | TTF |
| RakutenSansUIApp-Bold | Rakuten Sans | Bold | 700 | 0x00a0 | TTF |
| RakutenSansUIApp-Italic | Rakuten Sans | Italic | 400 | 0x0081 | TTF |
| RakutenSansUIApp-BoldItalic | Rakuten Sans | Bold Italic | 700 | 0x00a1 | TTF |
| RakutenSerifApp-Regular | Rakuten Serif | Regular | 400 | 0x00c0 | TTF |
| RakutenSerifApp-Bold | Rakuten Serif | Bold | 700 | 0x00a0 | TTF |
| RakutenSerifApp-Italic | Rakuten Serif | Italic | 400 | 0x0081 | TTF |
| RakutenSerifApp-BoldItalic | Rakuten Serif | Bold Italic | 700 | 0x00a1 | TTF |
| Avenir | Avenir Next | **Medium** | **500** | 0x0040 | TTC (2 fonts) |
| Avenir-Bold | Avenir Next | Bold | 700 | 0x0020 | TTF |
| Avenir-Italic | Avenir Next | **Medium Italic** | **500** | 0x0001 | TTC (2 fonts) |
| Avenir-BoldItalic | Avenir Next | Bold Italic | 700 | 0x0021 | TTF |
| georgia | Georgia | Regular | 400 | 0x0040 | TTC (2 fonts) |
| georgiab | Georgia | Bold | 700 | 0x0020 | TTC (2 fonts) |
| georgiai | Georgia | Italic | 400 | 0x0001 | TTC (2 fonts) |
| georgiaz | Georgia | Bold Italic | 700 | 0x0021 | TTC (2 fonts) |

- Rakuten fonts have no name IDs 16/17. Avenir has ID 16 = "Avenir Next".
- fsSelection 0x80 (USE_TYPO_METRICS) is set on all Rakuten fonts.
- All are `glyf`, none variable.

## Vietnamese coverage of stock fonts

60 test characters (Vietnamese letters with diacritics, `đ Đ`, `₫`):
Rakuten and Georgia are missing 49, Avenir is missing 54. That is the bug
this project fixes.

## Where nickel names these families

```sh
strings -n 4 usr/local/Kobo/libnickel.so.1.0.0 | grep -iE 'georgia|avenir'
strings -n 4 usr/local/Kobo/nickel | grep -iE 'georgia|avenir'
```

Libra 2 4.38 (same fonts as Libra H2O): `Avenir Next`, `Avenir.ttf`, and `font-family: Avenir;` /
`font-family: Georgia;` in embedded HTML/CSS (e.g. "What's new" text).
`Rakuten` does not appear as a plain string. Its stylesheet is probably
stored compressed. Not investigated (we don't patch nickel).
