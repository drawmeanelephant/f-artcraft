#!/usr/bin/env python3
"""wallpaper-night-watch V1R00 — issue #1251, variant 2.

Same mascot, new scene: the night watch. He stands a battlement on the
ramparts with the candle from the #595 Bare-Metal Vigil plate — the brand's
second motif — flame pooling warm UEFI light on the stone, deep navy night
behind. 2560x1440, center-weighted clear of seat chrome.
"""
import sys, os, math, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import NAVY, WALL_TOP, WALL_BOT, INK, BUN
from virelai.sexiburger import mascot

W, H = 2560, 1440
d = Draw()
d.new_doc("VirelaiOS — wallpaper night watch", W, H)

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

# --- palette ---------------------------------------------------------------------
STONE_HI, STONE_MID, STONE_LO = "#4A5468", "#333C4E", "#232A38"
WAX = "#F0E4BC"
FLAME_OUT = rad({"offset": 0, "color": "#FFD98A"},
                {"offset": 0.62, "color": "#F59A33"},
                {"offset": 1, "color": "#D95E14"})
FLAME_IN = rad({"offset": 0, "color": "#FFF6D2"},
               {"offset": 1, "color": "#FFC65E"})

# --- night field ------------------------------------------------------------------
d.shape("rectangle", "night field", x=0, y=0, width=W, height=H,
        fill=lin(WALL_TOP, WALL_BOT, (0, 0), (0, H)), stroke=NONE)

# crescent moon, upper right of the stage but out of the top chrome strip
MX, MY, MR = 1900, 330, 92
d.shape("ellipse", "moon halo", x=MX - 170, y=MY - 170, width=340, height=340,
        fill=rad({"offset": 0, "color": "#D8DEEA", "opacity": 0.20},
                 {"offset": 1, "color": "#D8DEEA", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "moon", x=MX - MR, y=MY - MR, width=2 * MR, height=2 * MR,
        fill=rad({"offset": 0, "color": "#E8EDF5"},
                 {"offset": 1, "color": "#B9C4D8"}), stroke=NONE)
d.shape("ellipse", "moon bite", x=MX - MR + 44, y=MY - MR - 18,
        width=2 * MR, height=2 * MR, fill=WALL_TOP, stroke=NONE)
for i, (cx, cy, r) in enumerate([(MX - 30, MY - 18, 13), (MX - 52, MY + 26, 9),
                                 (MX - 8, MY + 44, 7)]):
    d.shape("ellipse", f"crater{i}", x=cx - r, y=cy - r, width=2 * r,
            height=2 * r, fill="#C6D0E0", opacity=55, stroke=NONE)

stars = [(240, 200, 5), (520, 130, 4), (860, 170, 4), (1200, 120, 3),
         (1560, 180, 4), (2180, 160, 5), (2340, 340, 4), (2080, 560, 4),
         (160, 620, 4), (340, 980, 5), (2360, 900, 4), (2160, 1200, 5),
         (240, 1280, 4), (1000, 100, 3), (1450, 90, 4)]
for i, (x, y, w) in enumerate(stars):
    d.shape("ellipse", f"star{i}", x=x - w / 2, y=y - w / 2, width=w, height=w,
            fill="#C8D6F0", opacity=26, stroke=NONE)

# --- candle glow (behind stone and actor) -----------------------------------------
CX, FY = 1520, 700                     # candle x, flame center y
d.shape("ellipse", "candle pool", x=CX - 480, y=FY - 420, width=960,
        height=860,
        fill=rad({"offset": 0, "color": "#F0A83C", "opacity": 0.34},
                 {"offset": 0.55, "color": "#D88A28", "opacity": 0.13},
                 {"offset": 1, "color": "#D88A28", "opacity": 0}), stroke=NONE)

# --- ramparts ---------------------------------------------------------------------
# parapet band across the stage; walk top at y 985, face down to y 1180
WT, WB = 985, 1180
WX0, WX1 = 780, 1870
d.path(rrect(WX0, WT, WX1, WB, 8), "parapet face",
       fill=lin(STONE_MID, STONE_LO, (0, WT), (0, WB)), stroke=INK,
       strokeWidth=8)
# walk top surface (slightly lighter cap)
d.path(rrect(WX0 - 16, WT - 26, WX1 + 16, WT + 12, 8), "walk cap",
       fill=lin(STONE_HI, STONE_MID, (0, WT - 26), (0, WT + 12)),
       stroke=INK, strokeWidth=7)
# merlons (crenellation blocks) riding the cap
for i, mx in enumerate(range(WX0 + 20, WX1 - 40, 176)):
    d.path(rrect(mx, WT - 118, mx + 96, WT - 14, 8), f"merlon{i}",
           fill=lin(STONE_HI, STONE_MID, (0, WT - 118), (0, WT - 14)),
           stroke=INK, strokeWidth=7)
# stone courses on the face
for j, ry in enumerate([1040, 1100, 1152]):
    d.shape("line", f"course{j}", x1=WX0 + 14, y1=ry, x2=WX1 - 14, y2=ry,
            stroke=STONE_LO, strokeWidth=5, opacity=70, cap="round")
for i, sx in enumerate(range(WX0 + 110, WX1 - 60, 220)):
    rya = 1040 if (i % 2 == 0) else 1100
    d.shape("line", f"joint{i}", x1=sx, y1=rya - 34, x2=sx, y2=rya - 6,
            stroke=STONE_LO, strokeWidth=5, opacity=55, cap="round")
# warm candle-side rim on the wall face
d.path(f"M{CX - 300},{WT + 30} L{WX1 - 14},{WT + 30} L{WX1 - 14},{WT + 58} "
       f"L{CX - 300},{WT + 58} Z", "candle rim",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#F0A83C", "opacity": 0},
           {"offset": 0.6, "color": "#F0A83C", "opacity": 0.22},
           {"offset": 1, "color": "#FFC65E", "opacity": 0.4}],
           "start": [CX - 300, 0], "end": [WX1, 0]}}, stroke=NONE)
# ground shadow under the wall
d.shape("ellipse", "wall shadow", x=WX0 - 60, y=WB - 6,
        width=WX1 - WX0 + 120, height=80,
        fill=rad({"offset": 0, "color": "#06060E", "opacity": 0.6},
                 {"offset": 1, "color": "#06060E", "opacity": 0}), stroke=NONE)

# --- the vigil candle --------------------------------------------------------------
# holder dish on the walk cap
d.shape("ellipse", "holder", x=CX - 52, y=WT - 52, width=104, height=34,
        fill=lin("#8A6428", "#5E4014", (CX, WT - 52), (CX, WT - 18)),
        stroke=INK, strokeWidth=6)
# wax body with a drip
d.path(f"M{CX - 22},{WT - 48} L{CX - 22},{WT - 190} "
       f"Q{CX - 22},{WT - 200} {CX - 12},{WT - 200} L{CX + 12},{WT - 200} "
       f"Q{CX + 22},{WT - 200} {CX + 22},{WT - 190} L{CX + 22},{WT - 48} "
       f"Q{CX},{WT - 36} {CX - 22},{WT - 48} Z",
       "candle wax", fill=lin("#F7EDCB", "#D8C690", (CX - 22, 0), (CX + 22, 0)),
       stroke=INK, strokeWidth=6)
d.path(f"M{CX - 22},{WT - 160} q10,4 8,22 q-2,14 -8,10 q-6,-4 0,-32 Z",
       "wax drip", fill="#F7EDCB", stroke=INK, strokeWidth=4)
# wick + flame (Vigil plate recipe, scaled)
d.shape("line", "wick", x1=CX, y1=WT - 204, x2=CX, y2=WT - 216,
        stroke="#3A2A16", strokeWidth=6, cap="round")
fyt = WT - 216                      # flame base
d.path(f"M{CX},{fyt - 108} "
       f"C{CX + 34},{fyt - 62} {CX + 30},{fyt - 24} {CX},{fyt} "
       f"C{CX - 30},{fyt - 24} {CX - 34},{fyt - 62} {CX},{fyt - 108} Z",
       "flame outer", fill=FLAME_OUT, stroke=NONE)
d.path(f"M{CX},{fyt - 74} "
       f"C{CX + 19},{fyt - 44} {CX + 17},{fyt - 14} {CX},{fyt - 2} "
       f"C{CX - 17},{fyt - 14} {CX - 19},{fyt - 44} {CX},{fyt - 74} Z",
       "flame inner", fill=FLAME_IN, stroke=NONE)
# ember motes rising
for i, (ex, ey, r) in enumerate([(CX - 40, fyt - 190, 5), (CX + 30, fyt - 240, 4),
                                 (CX - 8, fyt - 300, 4), (CX + 56, fyt - 160, 3)]):
    d.shape("ellipse", f"mote{i}", x=ex - r, y=ey - r, width=2 * r,
            height=2 * r, fill="#FFC65E", opacity=60, stroke=NONE)

# --- the actor ----------------------------------------------------------------------
# mascot on the walk, turned toward the candle: right arm reaches to it,
# pupils glance right. Feet on the cap top (~y 960).
d.shape("ellipse", "mascot shadow", x=1030, y=944, width=230, height=30,
        fill=rad({"offset": 0, "color": "#06060E", "opacity": 0.55},
                 {"offset": 1, "color": "#06060E", "opacity": 0}), stroke=NONE)
mascot(d, 1140, 660, 300,
       mouth="smile", pupils=(5, 0),
       arm_right=((56, 122), (108, 108), (150, 96)),
       arm_left=((-56, 122), (-84, 152), (-76, 184)))
# warm candle-side edge on the mascot: translucent glaze over his right
d.shape("ellipse", "candle kiss", x=1230, y=740, width=190, height=290,
        fill=rad({"offset": 0, "color": "#FFB85C", "opacity": 0.22},
                 {"offset": 1, "color": "#FFB85C", "opacity": 0}), stroke=NONE)

# --- finish --------------------------------------------------------------------------
os.makedirs("work/out", exist_ok=True)
d.finish("wallpaper-night-watch-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 1280}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/wallpaper-night-watch-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
        print("preview saved")
