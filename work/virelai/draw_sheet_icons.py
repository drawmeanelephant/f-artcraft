#!/usr/bin/env python3
"""sheet-icons V1R00 — issue #1248 contact sheet.

All 31 app icons on a uniform grid in the issue's checklist order (core
desk, system, life), navy field, labeled in Virelai Sans (letters only —
the face has no digits and the names carry none). Review aid for the wave;
the per-icon masters are `art/virelai/icon-*/`.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import NAVY
from virelai.icons import new_doc, frame, SHAPES, ORDER

COLS, CW, RH = 8, 76, 82
ROWS = (len(ORDER) + COLS - 1) // COLS

d = Draw()
d.new_doc("sheet-icons-V1R00", COLS * CW, ROWS * RH)
d.shape("rectangle", "field", x=0, y=0, width=COLS * CW, height=ROWS * RH,
        fill=NAVY, stroke=NONE)

for i, name in enumerate(ORDER):
    col, row = i % COLS, i // COLS
    ox, oy = col * CW + 6, row * RH + 4
    frame(d, ox, oy)
    SHAPES[name](d, ox, oy)
    d.text(name.upper(), f"label/{name}", x=col * CW + CW / 2,
           y=oy + 72, size=8.5, font="Virelai Sans", color="#94A3B8",
           justify="center")

r = d.finish("sheet-icons-V1R00")
