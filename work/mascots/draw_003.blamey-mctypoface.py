#!/usr/bin/env python3
"""Blamey McTypoface — mascot portrait V1R00.
A parchment-cream clerk blob mid-toss, flicking blame-stamped parchments
into a wire wastebasket tagged OTHER PEOPLE'S PROBLEMS, red NOTED hand
stamp in the other fist. Perpetual smirk of feigned innocence: one brow
up, one down. Warm bureaucratic umber palette, never pure black.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Blamey McTypoface — Mascot Portrait", 1000, 1000)

INK = "#2E1B0E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#171008"}, {"offset": 1, "color": "#080503"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A3E22"}, {"offset": 0.7, "color": "#33220F"},
    {"offset": 1, "color": "#181008"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2A16"}, {"offset": 1, "color": "#181008"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6E6BE"}, {"offset": 0.72, "color": "#DFC393"},
    {"offset": 1, "color": "#B8975F"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E4C2"}, {"offset": 0.65, "color": "#DEC99E"},
    {"offset": 1, "color": "#BDA275"}]}}
METAL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6D58"}, {"offset": 0.55, "color": "#4C4B3C"},
    {"offset": 1, "color": "#2A2920"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5A30"}, {"offset": 0.6, "color": "#5E3A1C"},
    {"offset": 1, "color": "#3A2410"}]}}
STAMP_RED = "#A63A2E"
CREAM = "#F0E2C4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C890", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193, 233, 8), (801, 230, 7), (157, 524, 9),
                               (837, 544, 8), (247, 766, 7), (753, 749, 9),
                               (133, 393, 6), (864, 391, 7), (391, 113, 7),
                               (613, 110, 8), (333, 823, 6), (665, 821, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5232", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0805",
       strokeWidth=4, opacity=70)

# --- the wastebasket: OTHER PEOPLE'S PROBLEMS ------------------------------------
bx0, bx1, bty, bby = 592, 736, 512, 688   # rim x, rim y, base y
# shadow under the bin
d.shape("ellipse", "Bin shadow", x=bx0 - 14, y=bby - 8, width=bx1 - bx0 + 28,
        height=22, fill="#000000", opacity=35, stroke=NONE)
# tapered wire body
btcx = (bx0 + bx1) / 2
d.path(f"M{bx0},{bty} L{bx1},{bty} L{bx1 - 26},{bby} L{bx0 + 26},{bby} Z",
       "Bin body", fill=METAL_GRAD, stroke=INK, strokeWidth=5, join="round")
# wire mesh: verticals + two horizontal wires
for i in range(1, 6):
    t = i / 6
    xt, xb = bx0 + (bx1 - bx0) * t, bx0 + 26 + (bx1 - bx0 - 52) * t
    d.path(f"M{xt:.0f},{bty + 6} L{xb:.0f},{bby - 4}", f"Bin wire v{i}",
           fill=NONE, stroke="#24231B", strokeWidth=3, opacity=70)
for j, wy in enumerate([bty + 56, bty + 116]):
    shrink = (wy - bty) / (bby - bty) * 26
    d.path(f"M{bx0 + shrink:.0f},{wy} L{bx1 - shrink:.0f},{wy}",
           f"Bin wire h{j+1}", fill=NONE, stroke="#24231B", strokeWidth=3,
           opacity=70)
# papers already inside: a crumpled wad peeking over the back of the rim
d.path(f"M{btcx - 36},{bty + 4} L{btcx - 8},{bty - 22} L{btcx + 28},{bty - 12} "
       f"L{btcx + 16},{bty + 4} Z",
       "Bin paper wad", fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
# rim
d.shape("rectangle", "Bin rim", x=bx0 - 8, y=bty - 10, width=bx1 - bx0 + 16,
        height=18, radius=6, fill="#7C7B64", stroke=INK, strokeWidth=4)
# bin tag, slightly askew
d.path(rot_rect_path(btcx, 622, 152, 64, -4), "Bin tag", fill="#C9B183",
       stroke=INK, strokeWidth=3)
d.text("OTHER PEOPLE'S", "Tag line 1", x=btcx, y=632, size=13,
       font="Virelai Sans", color=INK, justify="center")
d.text("PROBLEMS", "Tag line 2", x=btcx, y=650, size=13,
       font="Virelai Sans", color=INK, justify="center")

# --- the toss: dashed trajectory + parchments in flight ---------------------------
d.path("M605,440 Q585,240 664,498", "Toss arc", fill=NONE,
       stroke="#E8C890", strokeWidth=2.5, opacity=35, dash=[8, 10])

def flying_paper(cx, cy, w, h, deg, label, noted=False):
    d.path(rot_rect_path(cx + 3, cy + 4, w, h, deg), f"{label} shadow",
           fill="#000000", opacity=22, stroke=NONE)
    d.path(rot_rect_path(cx, cy, w, h, deg), f"{label} sheet",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5)
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    for k in range(3):
        lw = w * (0.6 - k * 0.07)
        lx = cx - (-h * 0.24 + k * h * 0.18) * s
        ly = cy + (-h * 0.24 + k * h * 0.18) * c
        d.path(rot_rect_path(lx, ly, lw, 3, deg), f"{label} line {k+1}",
               fill=INK, opacity=50, stroke=NONE)
    if noted:
        # red NOTED stamp impression low on the sheet, rotated with it
        sx = cx - (-h * 0.28) * s
        sy = cy + (-h * 0.28) * c
        d.path(rot_rect_path(sx, sy, 46, 20, deg),
               f"{label} stamp", fill=NONE, stroke=STAMP_RED,
               strokeWidth=2.5, opacity=85)
        r = d.text("NOTED", f"{label} stamp text", x=sx, y=sy + 5, size=9,
                   font="Virelai Sans", color=STAMP_RED, justify="center")
        if r and r.get("id") and deg:
            d.cmd("object.rotate", "stamp text tilt", ids=[r["id"]],
                  angle=-deg, origin=[sx, sy])

flying_paper(603, 356, 56, 72, -18, "Paper 1")
flying_paper(621, 374, 60, 78, -2, "Paper 2", noted=True)
flying_paper(649, 451, 52, 68, 20, "Paper 3")
# one that missed — even the aim is someone else's fault
flying_paper(792, 664, 50, 64, 38, "Stray paper")

# --- Blamey: the blob -------------------------------------------------------------
# body: a soft trapezoid blob, wider than tall, sitting on the floor
d.path("M388,286 C470,286 524,352 532,462 C538,548 522,632 500,692 "
       "C476,702 300,702 276,692 C254,632 238,548 244,462 "
       "C252,352 306,286 388,286 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# side shade + belly highlight
d.path("M268,470 C262,552 272,634 292,686 C268,676 250,560 256,468 "
       "C258,428 262,448 268,470 Z", "Shade L", fill="#9A7A4C",
       opacity=30, stroke=NONE)
d.shape("ellipse", "Belly light", x=296, y=480, width=190, height=170,
        fill="#FFFFFF", opacity=13, stroke=NONE)
d.shape("ellipse", "Top light", x=320, y=302, width=150, height=44,
        fill="#FFFFFF", opacity=16, stroke=NONE)
# feet
for lbl, fx in [("Foot L", 292), ("Foot R", 424)]:
    d.shape("ellipse", lbl, x=fx, y=678, width=76, height=34,
            fill="#C7A670", stroke=INK, strokeWidth=4)
# a coffee-ring stain on the lower belly — he works here
d.shape("ellipse", "Coffee ring", x=318, y=590, width=46, height=28,
        fill=NONE, stroke="#8A5F30", strokeWidth=4, opacity=35)

# left arm: raised mid-flick toward the bin
d.path("M508,470 C546,452 572,448 596,452", "Arm R", fill=NONE,
       stroke="#DFC393", strokeWidth=30, cap="round")
d.shape("ellipse", "Hand R", x=586, y=428, width=40, height=34,
        fill="#E8CD9C", stroke=INK, strokeWidth=4)
# fingers splayed after the release
for i, (fx, fy) in enumerate([(602, 432), (612, 440), (616, 452)]):
    d.path(f"M596,444 L{fx},{fy}", f"Finger {i+1}", fill=NONE,
           stroke="#E8CD9C", strokeWidth=7, cap="round")

# right arm (viewer left): the NOTED stamp, held low and ready
d.path("M262,520 C238,546 234,572 242,594", "Arm L", fill=NONE,
       stroke="#DFC393", strokeWidth=30, cap="round")
d.shape("ellipse", "Hand L", x=228, y=572, width=42, height=36,
        fill="#E8CD9C", stroke=INK, strokeWidth=4)
# the stamp: grip, stem, red base — business end out
d.shape("ellipse", "Stamp grip", x=196, y=508, width=58, height=30,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Grip sheen", x=210, y=513, width=24, height=9,
        fill="#B8804A", opacity=60, stroke=NONE)
d.shape("rectangle", "Stamp neck", x=214, y=534, width=22, height=16,
        fill="#4A2E14", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp base", x=196, y=546, width=58, height=26,
        radius=4, fill="#7E2B22", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Base sheen", x=200, y=549, width=50, height=8,
        fill="#B8543E", opacity=55, stroke=NONE)

# --- the face: smug, blameless, delighted ------------------------------------------
for i, cx in enumerate([340, 424]):
    d.shape("ellipse", f"Eye {i+1}", x=cx - 14, y=428, width=28, height=32,
            fill="#241812", stroke=NONE)
    d.shape("ellipse", f"Glint {i+1}", x=cx - 7, y=434, width=8, height=8,
            fill="#FFFFFF", opacity=85, stroke=NONE)
# brows: left arched in innocence, right lowered in judgement
d.path("M318,412 C330,398 352,396 366,406", "Brow innocent", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M402,404 C416,410 430,408 442,400", "Brow judge", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# the asymmetric smirk
d.path("M340,500 C368,522 408,520 434,498", "Smirk", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M434,498 C442,494 446,488 447,482", "Smirk corner", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
# a single satisfied cheek line
d.path("M442,516 C450,512 456,506 458,498", "Smirk crease", fill=NONE,
       stroke="#B08A58", strokeWidth=4, cap="round", opacity=70)

# --- captions ----------------------------------------------------------------------
d.text("BLAMEY MCTYPOFACE", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E2C4", justify="center")
r = d.text("FAULT ROUTING ANALYST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C9A06A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("003.blamey-mctypoface-V1R00")
