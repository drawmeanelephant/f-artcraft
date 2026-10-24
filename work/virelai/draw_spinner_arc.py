#!/usr/bin/env python3
"""spinner-arc V1R00 — issue #1255.

Geometric indeterminate spinner in the VirelaiChrome register: a comet —
280° warm-INK tail arc + 55° Accent head arc, single stroke weight,
rounded caps, on a 10.5 radius inside the 32x32 frame. Rigid 30°/frame
rotation over 12 frames = seamless loop. Two-tone construction: the
Accent head carries the spin on dark chrome where the ink tail fades;
on light surfaces the full comet reads. Motif = 2 moving elements.

Sheet piece is the Nx1 uniform grid; per-frame PNGs (1x + @2x) ship
beside it for QOI adoption.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, OUT
from virelai.vkit import DARK, INK
from virelai import spinner

FRAMES = 12
R, SW = 10.5, 3.8
ACCENT = DARK["Accent"]   # #3B82F6 — the shipped attention token


def motif(d, cx, cy, f):
    rot = f * 30.0
    d.path(spinner.arc_path(cx, cy, R, 10 + rot, 290 + rot),
           "tail", fill=NONE, stroke=INK, strokeWidth=SW, cap="round")
    d.path(spinner.arc_path(cx, cy, R, 300 + rot, 355 + rot),
           "head", fill=NONE, stroke=ACCENT, strokeWidth=SW, cap="round")


d = Draw()
spinner.export_frames(d, "spinner-arc-V1R00", FRAMES, motif, OUT)
spinner.sheet(d, "spinner-arc-V1R00", FRAMES, motif)
r = d.finish("spinner-arc-V1R00")
