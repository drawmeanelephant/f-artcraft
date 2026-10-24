#!/usr/bin/env python3
"""wallpaper-workshop V1R00 — issue #1251, variant 3.

The "from-scratch OS" variant: the mascot at a workbench surrounded by tiny
machines and blueprints — a little gear train running, a wind-up bot on the
bench, blueprint sheet, hanging tools. Cel-shaded flat-ink family, navy
field warmed by a bench lamp. 2560x1440, center-weighted.
"""
import sys, os, math, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import NAVY, WALL_TOP, WALL_BOT, INK, BUN
from virelai.sexiburger import mascot

W, H = 2560, 1440
d = Draw()
d.new_doc("VirelaiOS — wallpaper workshop", W, H)

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0},
                                     {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], \
                                     [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def rrect(x0, y0, x1, y1, r):
    return (f"M{x0+r},{y0} L{x1-r},{y0} Q{x1},{y0} {x1},{y0+r} L{x1},{y1-r} "
            f"Q{x1},{y1} {x1-r},{y1} L{x0+r},{y1} Q{x0},{y1} {x0},{y1-r} "
            f"L{x0},{y0+r} Q{x0},{y0} {x0+r},{y0} Z")

def gear(cx, cy, r, teeth, name, fill, sw=6, rot=0):
    """Filled gear silhouette: toothed ring via polar polygon."""
    pts = []
    n = teeth * 2
    for i in range(n * 2):
        a = math.radians(rot + i * 360.0 / (n * 2))
        rr = r if i % 4 in (0, 1) else r * 0.78
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    p = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + \
        " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    d.path(p, name, fill=fill, stroke=INK, strokeWidth=sw, join="round")
    d.shape("ellipse", f"{name} hub", x=cx - r * 0.3, y=cy - r * 0.3,
            width=r * 0.6, height=r * 0.6, fill=NAVY, stroke=INK,
            strokeWidth=sw * 0.8)

# --- palette ---------------------------------------------------------------------
WOOD_HI, WOOD_MID, WOOD_LO = "#A5733F", "#7E5028", "#5A371C"
BRASS_HI, BRASS_LO = "#E8C26A", "#8A5E22"
STEEL_HI, STEEL_LO = "#B9C4D4", "#6E7B8E"
BP = "#2A4470"                        # blueprint blue
BP_LINE = "#9CC3E8"
LAMP = "#FFC65E"

# --- field ------------------------------------------------------------------------
d.shape("rectangle", "field", x=0, y=0, width=W, height=H,
        fill=lin("#21213A", "#12121F", (0, 0), (0, H)), stroke=NONE)
# warm lamplight pool over the bench
d.shape("ellipse", "lamp pool", x=830, y=260, width=900, height=860,
        fill=rad({"offset": 0, "color": "#F0A83C", "opacity": 0.30},
                 {"offset": 0.55, "color": "#D88A28", "opacity": 0.10},
                 {"offset": 1, "color": "#D88A28", "opacity": 0}), stroke=NONE)
# faint dust motes
for i, (x, y, w) in enumerate([(250, 240, 4), (560, 150, 4), (2020, 190, 5),
                               (2280, 480, 4), (190, 760, 4), (2330, 900, 4),
                               (2160, 1240, 5), (300, 1290, 4), (1980, 140, 3)]):
    d.shape("ellipse", f"mote{i}", x=x - w / 2, y=y - w / 2, width=w, height=w,
            fill="#C8D6F0", opacity=20, stroke=NONE)

# --- pegboard wall of tools, right of stage ----------------------------------------
PBX0, PBY0, PBX1, PBY1 = 1740, 420, 2150, 780
d.path(rrect(PBX0, PBY0, PBX1, PBY1, 10), "pegboard",
       fill=lin("#2A2A44", "#1B1B30", (0, PBY0), (0, PBY1)),
       stroke=INK, strokeWidth=6, opacity=85)
for i, hx in enumerate(range(PBX0 + 40, PBX1 - 20, 60)):
    for j, hy in enumerate(range(PBY0 + 40, PBY1 - 20, 60)):
        d.shape("ellipse", f"peg{i}x{j}", x=hx - 4, y=hy - 4, width=8,
                height=8, fill="#15152A", stroke=NONE)
# hanging silhouettes: wrench, screwdriver, hammer
d.path(f"M{PBX0 + 70},{PBY0 + 70} l26,10 l-8,18 l-26,-10 l4,120 q2,16 -12,16 "
       f"q-14,0 -12,-16 l4,-120 l-10,-6 l8,-18 Z", "wrench", fill=STEEL_LO,
       stroke=INK, strokeWidth=5, join="round", opacity=90)
d.path(f"M{PBX0 + 160},{PBY0 + 70} q-14,0 -14,16 l0,30 q0,16 14,16 l0,0 "
       f"l0,60 l-8,8 l0,26 l16,0 l0,-26 l-8,-8 l0,-60 q14,0 14,-16 l0,-30 "
       f"q0,-16 -14,-16 Z", "screwdriver", fill=STEEL_LO, stroke=INK,
       strokeWidth=5, join="round", opacity=90)
d.path(f"M{PBX0 + 260},{PBY0 + 70} h56 q10,0 10,12 l0,14 q0,12 -10,12 h-56 "
       f"l-6,16 h-12 l6,-16 q-8,0 -8,-12 l0,-14 q0,-12 8,-12 l6,-16 h12 Z"
       f"M{PBX0 + 280},{PBY0 + 120} l16,0 l0,100 l-16,0 Z",
       "hammer", fill=STEEL_LO, stroke=INK, strokeWidth=5, join="round",
       opacity=90)

# --- blueprint pinned on the wall, left of stage ------------------------------------
BPX, BPY = 420, 430
d.path(f"M{BPX},{BPY} L{BPX + 380},{BPY - 24} L{BPX + 396},{BPY + 300} "
       f"L{BPX + 10},{BPY + 320} Z", "blueprint",
       fill=lin("#33548C", BP, (BPX, BPY), (BPX + 380, BPY + 300)),
       stroke=INK, strokeWidth=6, join="round")
# blueprint linework: an isometric-ish box + dimension rules + title block
d.path(f"M{BPX + 70},{BPY + 90} L{BPX + 190},{BPY + 50} L{BPX + 300},{BPY + 86} "
       f"L{BPX + 180},{BPY + 128} Z", "bp top", fill=NONE, stroke=BP_LINE,
       strokeWidth=4, opacity=75, join="round")
d.path(f"M{BPX + 70},{BPY + 90} L{BPX + 70},{BPY + 180} L{BPX + 180},{BPY + 220} "
       f"L{BPX + 180},{BPY + 128}", "bp left", fill=NONE, stroke=BP_LINE,
       strokeWidth=4, opacity=75, join="round")
d.path(f"M{BPX + 300},{BPY + 86} L{BPX + 300},{BPY + 176} L{BPX + 180},{BPY + 220} "
       f"L{BPX + 180},{BPY + 128}", "bp right", fill=NONE, stroke=BP_LINE,
       strokeWidth=4, opacity=75, join="round")
d.shape("line", "bp dim", x1=BPX + 60, y1=BPY + 250, x2=BPX + 330, y2=BPY + 226,
        stroke=BP_LINE, strokeWidth=3, opacity=60, cap="round")
for i in range(3):
    d.shape("line", f"bp row{i}", x1=BPX + 60, y1=BPY + 262 + i * 16,
            x2=BPX + 300 - i * 30, y2=BPY + 244 + i * 16, stroke=BP_LINE,
            strokeWidth=3, opacity=45, cap="round")
d.shape("ellipse", "bp pin", x=BPX + 176, y=BPY - 30, width=20, height=20,
        fill=BRASS_HI, stroke=INK, strokeWidth=4)

# --- workbench ----------------------------------------------------------------------
BT, BB = 900, 960                      # bench top edge / apron bottom
BX0, BX1 = 880, 1720
# bench shadow
d.shape("ellipse", "bench shadow", x=BX0 - 80, y=1170, width=BX1 - BX0 + 160,
        height=90, fill=rad({"offset": 0, "color": "#06060E", "opacity": 0.6},
                            {"offset": 1, "color": "#06060E", "opacity": 0}),
        stroke=NONE)
# legs
for i, lx in enumerate([BX0 + 90, BX1 - 130]):
    d.path(rrect(lx, BB, lx + 44, 1180, 6), f"leg{i}",
           fill=lin(WOOD_MID, WOOD_LO, (lx, BB), (lx, 1180)), stroke=INK,
           strokeWidth=6)
# apron + thick top
d.path(rrect(BX0 + 30, BB, BX1 - 30, BB + 60, 6), "apron",
       fill=lin(WOOD_MID, WOOD_LO, (0, BB), (0, BB + 60)), stroke=INK,
       strokeWidth=6)
d.path(rrect(BX0, BT, BX1, BT + 46, 8), "bench top",
       fill=lin(WOOD_HI, WOOD_MID, (0, BT), (0, BT + 46)), stroke=INK,
       strokeWidth=7)
d.shape("line", "bench lit edge", x1=BX0 + 16, y1=BT + 10, x2=BX1 - 16,
        y2=BT + 10, stroke=WOOD_HI, strokeWidth=4, opacity=60, cap="round")

# --- bench dressing: machines, lamp, paper -------------------------------------------
# desk lamp, left end of the bench — the warm light source
LXp = BX0 + 120
d.path(f"M{LXp - 40},{BT + 6} L{LXp + 40},{BT + 6} L{LXp + 26},{BT - 20} "
       f"L{LXp - 26},{BT - 20} Z", "lamp base", fill=lin("#3A4356", "#232A38"),
       stroke=INK, strokeWidth=6, join="round")
d.path(f"M{LXp},{BT - 24} L{LXp - 56},{BT - 150} L{LXp + 60},{BT - 240}",
       "lamp arm", fill=NONE, stroke="#3A4356", strokeWidth=12, cap="round",
       join="round")
d.path(f"M{LXp},{BT - 24} L{LXp - 56},{BT - 150} L{LXp + 60},{BT - 240}",
       "lamp arm ink", fill=NONE, stroke=INK, strokeWidth=12, cap="round",
       join="round", opacity=35)
d.shape("ellipse", "lamp joint", x=LXp - 66, y=BT - 160, width=20, height=20,
        fill=BRASS_HI, stroke=INK, strokeWidth=5)
d.path(f"M{LXp + 30},{BT - 268} L{LXp + 118},{BT - 296} L{LXp + 138},{BT - 224} "
       f"L{LXp + 64},{BT - 196} Z", "lamp shade",
       fill=lin("#4A5468", "#232A38", (LXp, BT - 296), (LXp, BT - 196)),
       stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "lamp bulb", x=LXp + 82, y=BT - 240, width=34, height=22,
        fill=LAMP, stroke=NONE)
d.shape("ellipse", "lamp glow", x=LXp - 10, y=BT - 290, width=260, height=260,
        fill=rad({"offset": 0, "color": LAMP, "opacity": 0.30},
                 {"offset": 1, "color": LAMP, "opacity": 0}), stroke=NONE)

# gear train running between two bench posts, right side of the bench
gear(1530, 830, 78, 9, "gear A", lin(BRASS_HI, BRASS_LO, (1460, 770),
     (1600, 890)), rot=8)
gear(1660, 782, 52, 7, "gear B", lin(STEEL_HI, STEEL_LO, (1610, 740),
     (1710, 830)), rot=24)
gear(1648, 892, 40, 6, "gear C", lin(BRASS_HI, BRASS_LO, (1610, 860),
     (1690, 930)), rot=40)

# little wind-up bot sitting on the bench, right end — one of the tiny machines
BXx, BYy = 1805, BT
d.shape("ellipse", "bot shadow", x=BXx - 46, y=BYy - 4, width=92, height=16,
        fill=rad({"offset": 0, "color": "#06060E", "opacity": 0.5},
                 {"offset": 1, "color": "#06060E", "opacity": 0}), stroke=NONE)
d.path(rrect(BXx - 38, BYy - 108, BXx + 38, BYy - 4, 12), "bot body",
       fill=lin(STEEL_HI, STEEL_LO, (BXx - 38, BYy - 108), (BXx + 38, BYy)),
       stroke=INK, strokeWidth=6)
d.shape("ellipse", "bot eye L", x=BXx - 24, y=BYy - 88, width=16, height=20,
        fill="#FFF6D2", stroke=INK, strokeWidth=4)
d.shape("ellipse", "bot eye R", x=BXx + 8, y=BYy - 88, width=16, height=20,
        fill="#FFF6D2", stroke=INK, strokeWidth=4)
d.shape("ellipse", "bot pupil L", x=BXx - 20, y=BYy - 82, width=7, height=9,
        fill=INK, stroke=NONE)
d.shape("ellipse", "bot pupil R", x=BXx + 12, y=BYy - 82, width=7, height=9,
        fill=INK, stroke=NONE)
d.shape("line", "bot smile", x1=BXx - 16, y1=BYy - 56, x2=BXx + 16,
        y2=BYy - 56, stroke=INK, strokeWidth=4, cap="round")
# wind-up key
d.shape("line", "key stem", x1=BXx + 38, y1=BYy - 64, x2=BXx + 62, y2=BYy - 64,
        stroke=INK, strokeWidth=6, cap="round")
d.path(f"M{BXx + 62},{BYy - 80} q26,0 26,16 q0,16 -26,16 q-8,0 -8,-8 "
       f"q0,-8 8,-8 q10,0 10,-8", "key wing", fill=NONE, stroke=BRASS_HI,
       strokeWidth=7, cap="round")
# antenna
d.shape("line", "bot ant", x1=BXx, y1=BYy - 108, x2=BXx, y2=BYy - 132,
        stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "bot ant tip", x=BXx - 7, y=BYy - 146, width=14, height=14,
        fill="#E04B35", stroke=INK, strokeWidth=4)

# paper sheet + pencil nub on the bench, left of the mascot
d.path(f"M{BX0 + 300},{BT - 4} L{BX0 + 480},{BT - 22} L{BX0 + 496},{BT + 60} "
       f"L{BX0 + 310},{BT + 74} Z", "paper", fill="#E8EDF5", stroke=INK,
       strokeWidth=5, join="round")
for i in range(3):
    d.shape("line", f"paper line{i}", x1=BX0 + 326, y1=BT + 14 + i * 16,
            x2=BX0 + 460 - i * 18, y2=BT + 2 + i * 16, stroke="#8B98A5",
            strokeWidth=4, opacity=70, cap="round")
d.path(f"M{BX0 + 500},{BT + 40} L{BX0 + 560},{BT + 26} L{BX0 + 566},{BT + 40} "
       f"L{BX0 + 506},{BT + 54} Z", "pencil", fill="#F59E0B", stroke=INK,
       strokeWidth=4, join="round")

# --- the actor ----------------------------------------------------------------------
# leaning on the bench mid-work: one glove on the bench top, other holding a
# tiny gear up for inspection. Feet hidden behind the bench is wrong — he
# stands behind it; draw him so his tentacles tuck behind the apron.
d.shape("ellipse", "mascot shadow", x=1120, y=1160, width=240, height=34,
        fill=rad({"offset": 0, "color": "#06060E", "opacity": 0.55},
                 {"offset": 1, "color": "#06060E", "opacity": 0}), stroke=NONE)
mascot(d, 1240, 690, 340,
       mouth="grin", pupils=(6, -3), brows="raise",
       arm_right=((56, 122), (104, 96), (138, 60)),
       arm_left=((-56, 122), (-96, 150), (-120, 168)))
# tiny gear in the raised glove for scale
gear(1240 + 140 * (340 / 230.0), 690 + 58 * (340 / 230.0), 30, 6,
     "held gear", lin(BRASS_HI, BRASS_LO, (1400, 750), (1460, 810)),
     sw=4, rot=15)

# --- finish ---------------------------------------------------------------------------
os.makedirs("work/out", exist_ok=True)
d.finish("wallpaper-workshop-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 1280}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/wallpaper-workshop-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
        print("preview saved")
