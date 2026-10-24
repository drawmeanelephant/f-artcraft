#!/usr/bin/env python3
"""cursor-resize-y V1R00 — issue #1249.

VirelaiOS cursor set: chrome-register 32x48 master (2x of the shipping
16x24), transparent bg, closed white+INK silhouette built to survive the
kernel's 2-color mask path. Shape lives in virelai.cursors; hotspot table
in art/virelai/HOTSPOTS.md.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw
from virelai.cursors import new_doc, SHAPES

d = Draw()
new_doc(d, "cursor-resize-y-V1R00")
SHAPES["resize-y"](d)
r = d.finish("cursor-resize-y-V1R00")
