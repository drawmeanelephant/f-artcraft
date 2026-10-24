#!/usr/bin/env python3
"""wallpaper-guillotine V1R00 — issue #1251.

Full-res re-render of WALLPAPER.QOI (the 640x360 ship fixture): dark navy
field, the sexiburger mascot standing inside a wooden guillotine under the
raised blade, waving cheerfully. Same composition and joke, drawn for
2560x1440 instead of up-scaled — a fidelity pass, not a redesign.

Center-weighted: seat chrome eats the top ~80px and a left/bottom rail, so
the stage sits inside x 960-1600, y 250-1200. A stage with one actor.
"""
import sys, os, math, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import DARK, NAVY, INK, BUN
from virelai.sexiburger import mascot, POSES

W, H = 2560, 1440
d = Draw()
d.new_doc("VirelaiOS — wallpaper guillotine", W, H)

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

# --- palette -------------------------------------------------------------------
WOOD_HI, WOOD_MID, WOOD_LO = "#A5733F", "#7E5028", "#5A371C"
WOOD_EDGE = "#462A14"                    # dark side / end grain
STEEL_HI, STEEL_LO = "#D8E2EA", "#78879A"
ROPE = "#C9A86A"
STAR = "#C8D6F0"

# --- field ---------------------------------------------------------------------
d.shape("rectangle", "navy field", x=0, y=0, width=W, height=H,
        fill=NAVY, stroke=NONE)
# moody stage glow — wallpaper is allowed moodier than plates
d.shape("ellipse", "stage glow", x=700, y=240, width=1160, height=1000,
        fill=rad({"offset": 0, "color": "#2E2E4A", "opacity": 0.9},
                 {"offset": 0.6, "color": "#262640", "opacity": 0.45},
                 {"offset": 1, "color": NAVY, "opacity": 0}), stroke=NONE)
# faint starfield dust, kept out of the stage center
stars = [(210, 190, 5), (420, 120, 4), (700, 150, 4), (1900, 140, 5),
         (2180, 220, 4), (2360, 420, 5), (150, 520, 4), (300, 900, 5),
         (2280, 880, 4), (2120, 1180, 5), (190, 1240, 4), (2380, 660, 3),
         (960, 120, 3), (1620, 100, 4), (560, 1310, 4), (1780, 1330, 4)]
for i, (x, y, w) in enumerate(stars):
    d.shape("ellipse", f"star{i}", x=x - w / 2, y=y - w / 2, width=w, height=w,
            fill=STAR, opacity=26, stroke=NONE)

# --- ground --------------------------------------------------------------------
d.shape("ellipse", "ground shadow", x=880, y=1120, width=800, height=110,
        fill=rad({"offset": 0, "color": "#0A0A16", "opacity": 0.75},
                 {"offset": 1, "color": "#0A0A16", "opacity": 0}), stroke=NONE)

# --- guillotine -----------------------------------------------------------------
GXL, GXR = 1015, 1545            # post center x
POST_W = 92
POST_TOP, POST_BOT = 300, 1090

# feet: splayed base wedges under each post
for i, cx in enumerate([GXL, GXR]):
    sgn = -1 if i == 0 else 1
    d.path(f"M{cx - 30},{POST_BOT - 60} L{cx + sgn * 150},{POST_BOT + 30} "
           f"L{cx + sgn * 150},{POST_BOT + 66} L{cx - 30},{POST_BOT + 66} Z"
           if sgn > 0 else
           f"M{cx + 30},{POST_BOT - 60} L{cx + sgn * 150},{POST_BOT + 30} "
           f"L{cx + sgn * 150},{POST_BOT + 66} L{cx + 30},{POST_BOT + 66} Z",
           f"foot{i}", fill=lin(WOOD_MID, WOOD_LO, (cx, POST_BOT - 60),
                                (cx, POST_BOT + 66)),
           stroke=INK, strokeWidth=7, join="round")

# platform the mascot stands on, between the posts
d.path(rrect(GXL - 60, 1030, GXR + 60, 1090, 10), "platform",
       fill=lin(WOOD_HI, WOOD_MID, (GXL, 1030), (GXL, 1090)),
       stroke=INK, strokeWidth=7)
d.shape("line", "platform lit edge", x1=GXL - 48, y1=1041, x2=GXR + 48, y2=1041,
        stroke=WOOD_HI, strokeWidth=4, opacity=70, cap="round")

# posts
for i, cx in enumerate([GXL, GXR]):
    x0, x1 = cx - POST_W / 2, cx + POST_W / 2
    d.path(rrect(x0, POST_TOP, x1, POST_BOT + 10, 10), f"post{i}",
           fill=lin(WOOD_HI, WOOD_MID, (x0, 0), (x1, 0)),
           stroke=INK, strokeWidth=7)
    # blade channel groove on the inner face
    inner = x1 if i == 0 else x0
    sgn = 1 if i == 0 else -1
    d.shape("line", f"groove{i}", x1=inner + sgn * 14, y1=POST_TOP + 20,
            x2=inner + sgn * 14, y2=POST_BOT - 20,
            stroke=WOOD_LO, strokeWidth=8, opacity=80, cap="round")
    # post lit edge (light from upper left)
    d.shape("line", f"post lit{i}", x1=x0 + 10, y1=POST_TOP + 30,
            x2=x0 + 10, y2=POST_BOT - 30,
            stroke=WOOD_HI, strokeWidth=5, opacity=45, cap="round")
    # bolt heads
    for j, by in enumerate([420, 700, 980]):
        d.shape("ellipse", f"bolt{i}.{j}", x=cx - 9, y=by - 9, width=18,
                height=18, fill=WOOD_EDGE, stroke=INK, strokeWidth=4)

# top crossbar with a shallow cap
d.path(rrect(GXL - 90, POST_TOP - 30, GXR + 90, POST_TOP + 34, 12),
       "crossbar", fill=lin(WOOD_HI, WOOD_MID, (0, POST_TOP - 30),
                            (0, POST_TOP + 34)), stroke=INK, strokeWidth=7)
d.shape("line", "crossbar lit", x1=GXL - 74, y1=POST_TOP - 16,
        x2=GXR + 74, y2=POST_TOP - 16, stroke=WOOD_HI, strokeWidth=5,
        opacity=55, cap="round")

# lunette board hinged open against the left post — the machine's other half
d.path(f"M{GXL + 30},1005 L{GXL + 118},1005 L{GXL + 66},700 L{GXL - 22},700 Z",
       "lunette board", fill=lin(WOOD_MID, WOOD_LO, (GXL, 700), (GXL, 1005)),
       stroke=INK, strokeWidth=6, join="round", opacity=92)
d.shape("ellipse", "lunette hole", x=GXL + 16, y=786, width=64, height=64,
        fill="#0F0F1C", stroke=INK, strokeWidth=5, opacity=92)

# --- raised blade ---------------------------------------------------------------
# trapezoid, bevel biting down-left; hung by the rope over the crossbar
BX0, BX1 = GXL + 56, GXR - 56        # 1071 .. 1489, inside the channels
BT = POST_TOP + 70                    # blade top edge y
d.path(f"M{BX0},{BT} L{BX1},{BT} L{BX1},{BT + 150} L{BX0},{BT + 240} Z",
       "blade", fill=lin(STEEL_HI, STEEL_LO, (BX0, BT), (BX1, BT + 240)),
       stroke=INK, strokeWidth=8, join="round")
# honed bevel highlight along the cutting edge
d.shape("line", "bevel glint", x1=BX0 + 6, y1=BT + 234, x2=BX1 - 6,
        y2=BT + 144, stroke="#F2F7FB", strokeWidth=5, opacity=80, cap="round")
# blade rivets
for i, (rx, ry) in enumerate([(BX0 + 60, BT + 50), (BX1 - 60, BT + 50),
                              (BX0 + 110, BT + 130)]):
    d.shape("ellipse", f"rivet{i}", x=rx - 8, y=ry - 8, width=16, height=16,
            fill=STEEL_LO, stroke=INK, strokeWidth=4)
# rope: up through a pulley on the crossbar, tail tied off on the right post
d.shape("ellipse", "pulley", x=1266, y=POST_TOP - 18, width=28, height=28,
        fill=WOOD_EDGE, stroke=INK, strokeWidth=5)
d.shape("line", "rope drop", x1=1280, y1=POST_TOP - 4, x2=1280, y2=BT,
        stroke=ROPE, strokeWidth=7, cap="round")
d.path(f"M1280,{POST_TOP - 4} C1440,{POST_TOP - 40} {GXR + 60},{POST_TOP + 60} "
       f"{GXR + 62},{POST_TOP + 190}", "rope tail", fill=NONE, stroke=ROPE,
       strokeWidth=7, cap="round")
for j, ty in enumerate([POST_TOP + 196, POST_TOP + 214, POST_TOP + 232]):
    d.shape("line", f"rope wrap{j}", x1=GXR + 30, y1=ty, x2=GXR + 96, y2=ty + 8,
            stroke=ROPE, strokeWidth=6, cap="round")

# --- the actor -------------------------------------------------------------------
# waving under the raised blade; feet on the platform top (~y 1060)
d.shape("ellipse", "mascot shadow", x=1170, y=1046, width=220, height=34,
        fill=rad({"offset": 0, "color": "#0A0A16", "opacity": 0.6},
                 {"offset": 1, "color": "#0A0A16", "opacity": 0}), stroke=NONE)
mascot(d, 1280, 730, 330, **POSES["wave"])

# --- finish ----------------------------------------------------------------------
os.makedirs("work/out", exist_ok=True)
d.finish("wallpaper-guillotine-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 1280}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/wallpaper-guillotine-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
        print("preview saved")
