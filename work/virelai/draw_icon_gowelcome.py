#!/usr/bin/env python3
"""icon-gowelcome V1R00 — issue #1248.

VirelaiOS app icon: 64x64 master on transparent in the shared navy tile
frame (virelai.icons.frame); must read at 24 px dock and 16 px file rows.
Shape lives in virelai.icons.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw
from virelai.icons import new_doc, frame, SHAPES

d = Draw()
new_doc(d, "icon-gowelcome-V1R00")
frame(d)
SHAPES["gowelcome"](d)
r = d.finish("icon-gowelcome-V1R00")
