#!/usr/bin/env python3
"""Generate air-light-color-theme.json from the dark variant.

Approach: case-insensitive hex-code substitution using a curated palette map,
preserving structure and alpha channels. Then patch the `type`/`name` fields.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "themes" / "air-dark-color-theme.json"
DST = ROOT / "themes" / "air-light-color-theme.json"

# Map lowercased hex (no alpha) -> light replacement (no alpha, 6 hex digits).
# Alpha is preserved from the original when matching 8-digit codes.
RGB_MAP = {
    # ---------- syntax palette ----------
    "d6d6dd": "1F2024",   # default editor fg
    "dddddd": "1F2024",   # general fg
    "aaa0fa": "5A4ECF",   # purple keywords / properties / imports
    "e394dc": "B03A88",   # strings (pink)
    "efb080": "A85A29",   # classes / types (salmon)
    "a8cc7c": "4E7A2A",   # parameters / greens
    "82d2ce": "1F7F78",   # storage / control keywords (teal)
    "f8c762": "8D6B1F",   # functions / methods (amber)
    "ebc88d": "8F6614",   # numeric / units / constants
    "87c3ff": "0E5FA8",   # html tag / class / css prop-name
    "cc7c8a": "A54553",   # variable.language (rose)
    "5b8ce5": "1C5DB5",   # markdown link title
    "fad075": "8D6B1F",   # meta.tag
    "909192": "8C8C8C",   # comment
    "e4e4e4": "212124",   # xi translucent base

    # ---------- UI backgrounds (inverted) ----------
    "18191b": "FBFBFC",   # editor/sidebar/activity bar bg
    "090909": "E5E7EA",   # darker chrome (status/title/tab border)
    "252629": "F4F5F7",   # widgets / peek / hover
    "252526": "F4F5F7",   # debug toolbar
    "222222": "EAEBEE",   # tab selected bg
    "212121": "E0E2E6",   # terminal border
    "202020": "F4F5F7",   # misc action list / breadcrumb
    "262626": "F0F1F3",   # welcome tile / breadcrumb picker
    "282828": "E4E6EA",   # lineHighlight border
    "010409": "E5E7EA",   # overview ruler border

    # ---------- UI chrome ----------
    "313131": "EDEEF1",   # button secondary / input bg
    "3c3c3c": "D0D2D7",   # input borders
    "3d3f42": "D0D2D7",   # widget borders
    "383a49": "D6D8DD",   # actionBar toggled
    "383b3d": "D6D8DD",   # list drop
    "37373d": "D0D2D7",   # inactive selection
    "3a3d41": "D0D2D7",   # diff inactive selection
    "454545": "C8CACF",   # menu/widget border
    "4d4d4d": "B8BABF",   # profile badge
    "404040": "D0D2D7",   # indent guide bg
    "585858": "B8BABF",
    "5a5a5a": "A8ACB2",
    "5a5d5e": "A8ACB2",
    "616161": "B0B4BA",   # badge bg
    "6e7681": "90959D",   # line number fg
    "646464": "8C8C8C",
    "676767": "8C8C8C",
    "707070": "8C8C8C",   # indent guide active
    "53595d": "C8CACF",
    "63a0c0": "A0399A",
    "636667": "C8CACF",
    "8b8b8b": "8C8C8C",

    # ---------- text ----------
    "d7d7d7": "1F2024",
    "d0d0d0": "2A2D33",
    "cccccc": "2A2D33",
    "bbbbbb": "2A2D33",
    "aeafad": "3A3D42",
    "a0a0a0": "6E7177",
    "9d9d9d": "5C6067",
    "989898": "6E7177",
    "969696": "6E7177",
    "8c8c8c": "7C7F85",
    "999999": "6E7177",
    "868686": "6E7177",
    "848484": "808389",
    "808080": "7C7F85",
    "a4a4a4": "6E7177",
    "bfbfbf": "8C8C8C",
    "c1c1c1": "A8ACB2",
    "c3c5c9": "3A3D42",   # ansiBrightWhite
    "cfcfcf": "1F2024",   # ansiBlack
    "dfe0e3": "6E7177",   # ansiBrightBlack
    "e0e0e0": "2A2D33",
    "e7e7e7": "1F2024",
    "eeeeee": "2A2D33",
    "f8f8f8": "FFFFFF",

    # ---------- accents (blue) ----------
    "0078d4": "005FB0",
    "026ec1": "004B8E",
    "2aaaff": "005FB0",
    "4daafc": "005FB0",
    "2489db": "005FB0",
    "2488db": "005FB0",
    "59a4f9": "0969DA",
    "85b6ff": "0969DA",
    "6caddf": "0969DA",
    "75beff": "0969DA",
    "569cd6": "0969DA",
    "4e94ce": "0969DA",
    "4a90e2": "0969DA",
    "3794ff": "005FB0",
    "179fff": "005FB0",
    "3399cc": "0969DA",
    "3399ff": "0969DA",
    "236b8e": "0969DA",
    "007acc": "005FB0",
    "04395e": "CCE3F5",   # focus bg (selected list item)
    "063b49": "CCE3F5",   # info validation bg
    "8db9e2": "005FB0",
    "2a66de": "0D47A1",   # ansiBlue
    "5b8ce5": "1C5DB5",   # already in syntax; keep
    "64c9e2": "0277BD",   # ansiBrightCyan
    "53b7d3": "01579B",   # ansiCyan

    # ---------- git ----------
    "438e6b": "2D8F4E",
    "7aae92": "2D8F4E",
    "d05261": "C93643",
    "427ce3": "005FB0",
    "7ba2e9": "005FB0",

    # ---------- red / error ----------
    "f85149": "CF222E",
    "f14c4c": "CF222E",
    "cb2431": "CF222E",
    "be1100": "B91007",
    "e10013": "CF222E",
    "e90215": "CF222E",
    "e4676b": "CF222E",
    "fc6a6a": "CF222E",
    "f48771": "CF222E",
    "f88070": "CF222E",
    "a31515": "CF222E",
    "420b0d": "FADCDB",
    "6c2022": "FADCDB",
    "6c1717": "FADCDB",
    "781212": "FADCDB",
    "5a1d1d": "FADCDB",
    "4b1818": "FADCDB",
    "6f1313": "FADCDB",
    "b91007": "B91007",

    # ---------- green ----------
    "89d185": "2D8F4E",
    "7abd7a": "2D8F4E",
    "73c991": "2D8F4E",
    "54b054": "2D8F4E",
    "3fb950": "2D8F4E",
    "2ea043": "2D8F4E",
    "81b88b": "2D8F4E",
    "1d9271": "2D8F4E",
    "1b81a8": "005FB0",
    "369432": "2D8F4E",
    "175021": "D1EBD7",
    "9bb955": "2D8F4E",
    "9ccc2c": "2D8F4E",
    "97dc92": "2D8F4E",   # ansiBrightGreen
    "469c72": "1B5E20",   # ansiGreen
    "3d897a": "2D8F4E",
    "3fa266": "2D8F4E",

    # ---------- yellow / amber ----------
    "cca700": "9B7218",
    "bb8009": "9B7218",
    "d18616": "9B7218",
    "ee9d28": "B8710A",
    "e2c08d": "B8710A",
    "ea5c00": "B8440F",
    "b89500": "9B7218",
    "fcba03": "C9931E",
    "ffa500": "C9931E",
    "ffa600": "C9931E",
    "ff8e00": "C9931E",
    "9e6a03": "C9931E",
    "ffcc00": "C9931E",
    "ffb000": "C9931E",
    "ffd700": "C9931E",
    "d5943a": "8D4E00",   # ansiYellow
    "f3d282": "B8710A",   # ansiBrightYellow
    "352a05": "FFF3D1",
    "7a6400": "FFF3D1",
    "994f00": "B8440F",

    # ---------- purple / magenta ----------
    "b180d7": "6E40C9",
    "8957e5": "6E40C9",
    "c586c0": "A0399A",
    "da70d6": "A0399A",
    "d758b3": "A0399A",
    "dc267f": "A0399A",
    "b66dff": "6E40C9",
    "dd88dd": "A0399A",   # ansiBrightMagenta
    "ce55cd": "6A1B9A",   # ansiMagenta

    # ---------- cyan / teal ----------
    "40c8ae": "1F7F78",
    "40a6ff": "005FB0",
    "40b0a6": "1F7F78",

    # ---------- highlights / selections ----------
    "264f78": "A6CCFF",   # selection
    "add6ff": "005FB0",   # selection highlight (token)
    "26477 8": "A6CCFF",   # (typo-proof)
    "264778": "A6CCFF",
    "6e7a85": "C8CACF",   # linkedEditing
    "6e7681": "90959D",   # duplicate — ok
    "6e7681 ": "90959D",

    # ---------- alpha-on-white becomes alpha-on-black ----------
    "ffffff": "FFFFFF_KEEP",  # sentinel; see post-process

    # ---------- neutrals ----------
    "000000": "000000",   # stays black for shadows
    "0064 00": "2D8F4E",
    "004972": "005FB0",
    "0078d4": "005FB0",   # dup
    "60606 0": "6E7177",
    "606060": "6E7177",
    "747474": "8C8C8C",
    "797979": "8C8C8C",
    "333333": "B8BABF",
    "444444": "B8BABF",
    "888888": "B8BABF",
    "333333": "B8BABF",
    "adaca8": "6E7177",
    "868686": "6E7177",
    "c0a0c0": "A0399A",
    "a0a0a0": "6E7177",  # dup
    "0000 00": "000000",
    "3a3d41": "D0D2D7",  # dup
}

# Special handling: ffffff with alpha flips to 000000 with alpha (black overlay).
# ffffff fully opaque stays white (button text on blue, badge text).

HEX_RE = re.compile(r"#([0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?\b")

def transform(match: re.Match) -> str:
    rgb = match.group(1).lower()
    alpha = match.group(2) or ""

    # ffffff alpha flip
    if rgb == "ffffff":
        if alpha:
            return f"#000000{alpha}"
        return "#FFFFFF"

    if rgb in RGB_MAP and RGB_MAP[rgb] not in ("FFFFFF_KEEP",):
        return "#" + RGB_MAP[rgb] + alpha.upper()

    # Fallback: unmapped colors pass through unchanged
    return match.group(0)

def main() -> None:
    text = SRC.read_text()
    out = HEX_RE.sub(transform, text)

    # Header patch
    out = out.replace('"type": "dark"', '"type": "light"', 1)
    out = out.replace('"name": "Air dark"', '"name": "Air light"', 1)

    DST.write_text(out)
    print(f"Wrote {DST.relative_to(ROOT)} ({len(out)} bytes)")

if __name__ == "__main__":
    main()
