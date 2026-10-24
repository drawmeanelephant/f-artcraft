#!/usr/bin/env python3
"""Read-at-size proof for virelai assets.

Usage: python3 work/tools/proof_size.py <@2x.png> <ship_w> <ship_h> [--mask]
Writes beside the source: <base>-ship.png (exact px on transparency),
<base>-ship-big.png (8x nearest on split dark|light field, for eyeballing)
and with --mask <base>-mask-big.png (coverage+ink 3-tone mask sim, 8x)."""
import sys, os
from PIL import Image

src, w, h = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
mask = "--mask" in sys.argv
img = Image.open(src).convert("RGBA")

ship = img.resize((w, h), Image.LANCZOS)
base = src.replace("@2x.png", "")
ship.save(f"{base}-ship.png")

# split-field view: same asset on navy chrome | light row, side by side
field = Image.new("RGBA", (w * 2 + 1, h))
field.paste(Image.new("RGBA", (w, h), (30, 30, 46, 255)), (0, 0))
field.paste(Image.new("RGBA", (w, h), (241, 245, 249, 255)), (w + 1, 0))
field.alpha_composite(ship, (0, 0))
field.alpha_composite(ship, (w + 1, 0))
field.resize((field.width * 8, h * 8), Image.NEAREST).save(f"{base}-ship-big.png")

if mask:
    # mask+data sim: uncovered = mid gray, covered-light = white, dark = ink
    px = ship.load()
    m = Image.new("RGBA", (w, h))
    mp = m.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a <= 96:
                mp[x, y] = (128, 128, 128, 255)        # outside silhouette
            elif (r + g + b) / 3 < 200:
                mp[x, y] = (20, 20, 20, 255)           # ink
            else:
                mp[x, y] = (255, 255, 255, 255)        # paper fill
    m.resize((w * 8, h * 8), Image.NEAREST).save(f"{base}-mask-big.png")
    print("mask:", f"{base}-mask-big.png")
print("ship:", f"{base}-ship.png", "| big:", f"{base}-ship-big.png")
