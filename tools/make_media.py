#!/usr/bin/env python3
"""Build media/corpus.jpg: a contact sheet of the real images in testRecipes/.

Nothing here is staged. The tiles are the five JPEGs committed in
testRecipes/, downscaled, in filename order, with the filename under each one.

    python3 tools/make_media.py

Requires Pillow.
"""

import glob
import os

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "testRecipes")
OUT = os.path.join(REPO, "media", "corpus.jpg")

TILE_W = 260
GAP = 14
PAD = 18
LABEL_H = 22
BG = (13, 17, 23)        # GitHub dark canvas; readable on both themes
FG = (201, 209, 217)


def load_font(size):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


def main():
    paths = sorted(glob.glob(os.path.join(SRC, "*.jpeg")) +
                   glob.glob(os.path.join(SRC, "*.jpg")) +
                   glob.glob(os.path.join(SRC, "*.png")))
    if not paths:
        raise SystemExit("no images in %s" % SRC)

    tiles = []
    for path in paths:
        im = Image.open(path).convert("RGB")
        h = round(im.height * TILE_W / im.width)
        tiles.append((os.path.basename(path), im.resize((TILE_W, h), Image.LANCZOS)))

    tile_h = max(t[1].height for t in tiles)
    cols = len(tiles)
    width = PAD * 2 + cols * TILE_W + (cols - 1) * GAP
    height = PAD * 2 + tile_h + LABEL_H

    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    font = load_font(13)

    for i, (name, im) in enumerate(tiles):
        x = PAD + i * (TILE_W + GAP)
        sheet.paste(im, (x, PAD))
        label = name.replace("Groß ", "").replace(".jpeg", "")
        draw.text((x, PAD + tile_h + 5), label, fill=FG, font=font)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sheet.save(OUT, quality=80, optimize=True, progressive=True)
    print("wrote %s  %dx%d  %s bytes  from %d source images"
          % (os.path.relpath(OUT, REPO), sheet.width, sheet.height,
             format(os.path.getsize(OUT), ","), len(tiles)))


if __name__ == "__main__":
    main()
