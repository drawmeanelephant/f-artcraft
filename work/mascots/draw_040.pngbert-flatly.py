#!/usr/bin/env python3
"""Pngbert Flatly — mascot portrait V1R00. Lossless Preservation Agent:
a crisp pixel-pure icon-being, CRISP. ALWAYS. bannered across its chest,
keeping a candle vigil for broken anchors on a transparency-checker
cloth. Cool slate-cyan plate on a deep ink-slate backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Pngbert Flatly — Mascot Plate", 1000, 1000)

INK = "#1E1A14"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0C1820"}, {"offset": 1, "color": "#04080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E7A8C"}, {"offset": 0.62, "color": "#2E5060"},
    {"offset": 1, "color": "#142832"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 340], "end": [0, 790], "stops": [
    {"offset": 0, "color": "#BFD2DC"}, {"offset": 0.55, "color": "#8AA2B0"},
    {"offset": 1, "color": "#5E7482"}]}}
WAX_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E4C8"}, {"offset": 1, "color": "#C8AE88"}]}}
FLAME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF4C8"}, {"offset": 0.55, "color": "#F2A83C"},
    {"offset": 1, "color": "#D86414"}]}}
BANNER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8D9B8"}, {"offset": 1, "color": "#B8A078"}]}}
CHK_A = "#D8E2E8"
CHK_B = "#9FB2BC"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#4E8A9C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A181E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D4DC", strokeWidth=3, opacity=28)
# patina + pixel flecks
d.shape("ellipse", "Patina 1", x=200, y=340, width=230, height=150,
        fill="#2A5866", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=630, y=580, width=220, height=140,
        fill="#5E94A4", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(215,335,6),(790,330,6),(190,560,6),(845,570,6),
                               (260,765,6),(740,758,6),(158,455,5),(855,450,5),
                               (430,125,6),(605,130,6),(335,155,5),(700,190,6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("rectangle", f"Pixel fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8E2EA", opacity=32, stroke=NONE)
# candle-glow ambience, lower right
d.shape("ellipse", "Vigil ambience", x=560, y=640, width=320, height=200,
        fill="#F2A83C", opacity=8, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M932,148 A108,108 0 0 0 838,58", "Ghost arc TR",
       fill=NONE, stroke="#3E7484", strokeWidth=14, opacity=10, cap="round")
d.path("M72,768 A122,122 0 0 0 182,878", "Ghost arc BL",
       fill=NONE, stroke="#3E7484", strokeWidth=10, opacity=8, cap="round")

# --- broken anchors drifting on the plate ---------------------------------------------
def anchor(cx, cy, s, deg, label, op=80):
    """Anchor of size s at (cx,cy): ring, shaft, crossbar, flukes — with a
    crack gap in the shaft (two halves shifted)."""
    d.path(f"M{cx},{cy - s} L{cx + 3},{cy + s * 0.12}",
           f"{label} shaft top", fill=NONE, stroke="#AEC6CE",
           strokeWidth=max(3, s * 0.14), cap="round", opacity=op)
    d.path(f"M{cx + 7},{cy + s * 0.3} L{cx + 4},{cy + s * 0.7}",
           f"{label} shaft bottom", fill=NONE, stroke="#AEC6CE",
           strokeWidth=max(3, s * 0.14), cap="round", opacity=op)
    d.shape("ellipse", f"{label} ring", x=cx - s * 0.22, y=cy - s * 1.28,
            width=s * 0.44, height=s * 0.44, fill=NONE,
            stroke="#AEC6CE", strokeWidth=max(3, s * 0.12), opacity=op)
    d.path(f"M{cx - s * 0.7},{cy + s * 0.15} L{cx + s * 0.7},{cy + s * 0.15}",
           f"{label} crossbar", fill=NONE, stroke="#AEC6CE",
           strokeWidth=max(3, s * 0.12), cap="round", opacity=op)
    d.path(f"M{cx - s * 0.75},{cy + s * 0.35} "
           f"A{s * 0.78},{s * 0.78} 0 0 0 {cx + s * 0.79},{cy + s * 0.35}",
           f"{label} flukes", fill=NONE, stroke="#AEC6CE",
           strokeWidth=max(3, s * 0.14), cap="round", opacity=op)
    d.path(f"M{cx - s * 0.75},{cy + s * 0.35} L{cx - s * 0.55},{cy + s * 0.1} "
           f"M{cx + s * 0.79},{cy + s * 0.35} L{cx + s * 0.6},{cy + s * 0.1}",
           f"{label} fluke tips", fill=NONE, stroke="#AEC6CE",
           strokeWidth=max(3, s * 0.13), cap="round", opacity=op)

anchor(268, 260, 42, 0, "Broken anchor 1")
anchor(770, 210, 34, 0, "Broken anchor 2", op=60)
anchor(205, 520, 30, 0, "Broken anchor 3", op=45)
# crack chips beside each shaft gap
for i, (x, y) in enumerate([(272, 264), (774, 214), (208, 524)]):
    d.shape("rectangle", f"Anchor chip {i+1}", x=x, y=y, width=5, height=5,
            fill="#AEC6CE", opacity=55, stroke=NONE)

# --- the vigil: candles on a transparency-checker cloth ---------------------------------
# checkerboard cloth, lower right (transparency grid — PNG's heraldry)
cx0, cy0, cs, cols, rows = 590, 716, 26, 7, 3
for r_ in range(rows):
    for c_ in range(cols):
        x, y = cx0 + c_ * cs, cy0 + r_ * cs
        if (r_ + c_) % 2 == 0:
            d.shape("rectangle", f"Chk {r_}-{c_}", x=x, y=y, width=cs, height=cs,
                    fill=CHK_B, opacity=55, stroke=NONE)
        else:
            d.shape("rectangle", f"Chk {r_}-{c_}", x=x, y=y, width=cs, height=cs,
                    fill=CHK_A, opacity=55, stroke=NONE)
d.path(rot_rect_path(cx0 + cols * cs / 2, cy0 + rows * cs / 2,
                     cols * cs + 10, rows * cs + 10, 0), "Cloth edge",
       fill=NONE, stroke="#0E2028", strokeWidth=3, opacity=60)

def candle(cx, base, w, h, label, lit=True):
    d.shape("ellipse", f"{label} pool", x=cx - w, y=base - 6, width=w * 2,
            height=12, fill="#D8C8A8", opacity=60, stroke=NONE)
    d.shape("rectangle", f"{label} body", x=cx - w // 2, y=base - h,
            width=w, height=h, radius=5, fill=WAX_GRAD, stroke=INK,
            strokeWidth=3)
    d.path(f"M{cx - w//2},{base - h + 8} C{cx - w//4},{base - h + 16} "
           f"{cx - w//6},{base - h + 4} {cx},{base - h + 12}",
           f"{label} drip", fill="#EAD9B4", stroke=NONE)
    if lit:
        d.shape("ellipse", f"{label} glow", x=cx - 26, y=base - h - 46,
                width=52, height=60, fill="#F2A83C", opacity=18, stroke=NONE)
        d.path(f"M{cx},{base - h - 34} C{cx + 8},{base - h - 20} "
               f"{cx + 7},{base - h - 8} {cx},{base - h - 4} "
               f"C{cx - 7},{base - h - 8} {cx - 8},{base - h - 20} "
               f"{cx},{base - h - 34} Z",
               f"{label} flame", fill=FLAME_GRAD, stroke="#8A4A10",
               strokeWidth=2)
        d.path(f"M{cx},{base - h - 6} L{cx},{base - h + 2}",
               f"{label} wick", fill=NONE, stroke="#241C14",
               strokeWidth=2.5, cap="round")
    else:
        d.path(f"M{cx},{base - h - 2} L{cx + 2},{base - h + 4}",
               f"{label} wick", fill=NONE, stroke="#241C14",
               strokeWidth=2.5, cap="round")
        d.path(f"M{cx},{base - h - 4} C{cx - 4},{base - h - 16} "
               f"{cx + 4},{base - h - 24} {cx},{base - h - 34}",
               f"{label} smoke", fill=NONE, stroke="#B8B0A0",
               strokeWidth=2.5, opacity=40, cap="round")

# three lit, one waiting for the taper
candle(640, 748, 34, 62, "Candle 1")
candle(706, 752, 30, 44, "Candle 2")
candle(768, 746, 36, 70, "Candle 3")
candle(600, 762, 26, 34, "Candle 4", lit=False)

# --- Pngbert ----------------------------------------------------------------------------
# pixel-corner notches on the head — the file format made flesh
d.shape("rectangle", "Body", x=408, y=360, width=186, height=420,
        radius=34, fill=BODY_GRAD, stroke=INK, strokeWidth=5)
for i, (x, y) in enumerate([(408, 360), (570, 360), (408, 756), (570, 756)]):
    d.shape("rectangle", f"Corner notch {i+1}", x=x + 4, y=y + 4,
            width=14, height=14, fill=PLATE_GRAD["gradient"]["stops"][1]["color"],
            stroke=INK, strokeWidth=2.5, opacity=90)
# body shading: crisp rim light left, soft shade right
d.path("M414,380 L438,380 C430,520 430,640 438,772 L414,772 Z",
       "Rim light", fill="#E4EEF2", opacity=40, stroke=NONE)
d.path("M560,390 C574,520 574,650 560,770 L592,770 C596,640 596,500 592,390 Z",
       "Body shade", fill="#2E4050", opacity=35, stroke=NONE)
# face: even-toned, quietly smug
d.shape("ellipse", "Eye L", x=442, y=452, width=26, height=30,
        fill="#F0F4F6", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye R", x=524, y=452, width=26, height=30,
        fill="#F0F4F6", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=452, y=460, width=10, height=12,
        fill="#1E1A14", stroke=NONE)
d.shape("ellipse", "Pupil R", x=534, y=460, width=10, height=12,
        fill="#1E1A14", stroke=NONE)
d.shape("ellipse", "Glint L", x=450, y=458, width=5, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=532, y=458, width=5, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# flat composed brows — smug
d.path("M438,434 L470,432", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M522,432 L554,434", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# the smallest satisfied smirk
d.path("M478,510 C492,518 506,518 518,510 C512,522 484,522 478,510 Z",
       "Smirk", fill="#4A5A64", stroke=INK, strokeWidth=2)
# checkerboard belly patch — transparency, worn proudly
for r_ in range(2):
    for c_ in range(6):
        x, y = 451 + c_ * 18, 692 + r_ * 18
        d.shape("rectangle", f"Belly chk {r_}-{c_}", x=x, y=y, width=18,
                height=18, fill=CHK_A if (r_ + c_) % 2 == 0 else CHK_B,
                stroke="#4A5A64", strokeWidth=0.75)
# the slogan, tattooed on a chest banner
d.path("M424,612 C470,600 534,600 580,612 L574,650 C532,640 470,640 430,650 Z",
       "Banner", fill=BANNER_GRAD, stroke=INK, strokeWidth=3)
d.path("M424,612 L408,606 L414,632 L430,636 Z", "Banner tail L",
       fill="#B8A078", stroke=INK, strokeWidth=2.5)
d.path("M580,612 L596,606 L590,632 L574,636 Z", "Banner tail R",
       fill="#B8A078", stroke=INK, strokeWidth=2.5)
d.text("CRISP. ALWAYS.", "Tattoo", x=502, y=633, size=14,
       font="Virelai Sans", color="#4A3423", justify="center")
# left arm at its side, palm open toward the vigil
d.path("M408,520 C384,560 372,610 372,652 C382,664 398,662 406,650 "
       "C408,608 414,566 422,540 Z",
       "Arm L", fill=BODY_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=366, y=640, width=32, height=28,
        fill=BODY_GRAD, stroke=INK, strokeWidth=3.5)
# right arm extended down-right, holding the lit taper to candle 4
d.path("M594,540 C634,570 662,610 678,652 C686,668 682,684 668,688 "
       "C648,682 630,652 616,614 C606,588 598,564 594,540 Z",
       "Arm R", fill=BODY_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=652, y=660, width=32, height=28,
        fill=BODY_GRAD, stroke=INK, strokeWidth=3.5)
# the taper: a lit spill reaching to the unlit wick
d.path("M662,676 L602,718", "Taper", fill=NONE, stroke="#C8AE88",
       strokeWidth=4, cap="round")
d.shape("ellipse", "Taper glow", x=584, y=700, width=40, height=44,
        fill="#F2A83C", opacity=22, stroke=NONE)
d.path("M600,696 C606,708 605,714 602,720 C598,714 595,708 600,696 Z",
       "Taper flame", fill=FLAME_GRAD, stroke="#8A4A10", strokeWidth=1.5)

# --- name + role ----------------------------------------------------------------------
d.text("PNGBERT FLATLY", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DCE8EE", justify="center")
r = d.text("LOSSLESS PRESERVATION AGENT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FC0CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("040.pngbert-flatly-V1R00")
