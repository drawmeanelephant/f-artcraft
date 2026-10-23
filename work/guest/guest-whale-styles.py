#!/usr/bin/env python3
"""Generate the JSONL session that draws the whale mascot in several styles.

Run from the repo root:  python3 work/guest-whale-styles.py > work/out/whales.jsonl
"""
import json
import os
import math
import re

os.makedirs("work/out", exist_ok=True)

TILE = 1000


def bezier(p0, c1, c2, p1, n=24):
    out = []
    for i in range(1, n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p1[0]
        y = u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p1[1]
        out.append((x, y))
    return out


def xf(d, s, tx, ty, rot=0.0, pivot=(0, 0)):
    """Scale, rotate and translate a path whose numbers are x,y coordinate pairs."""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)

    def sub(m):
        x, y = float(m.group(1)), float(m.group(2))
        dx, dy = x - pivot[0], y - pivot[1]
        nx = pivot[0] + s * (ca * dx - sa * dy) + tx
        ny = pivot[1] + s * (sa * dx + ca * dy) + ty
        return f"{nx:.2f},{ny:.2f}"

    return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", sub, d)


def fmt(pts):
    return " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


# ----------------------------------------------------------------- geometry
# Whale facing right: fat head, tapering to a tail stock on the left.
BODY_SEGS = [
    ((250, 500), (252, 438), (308, 392), (382, 366)),
    ((382, 366), (470, 336), (588, 332), (678, 360)),
    ((678, 360), (770, 388), (826, 458), (834, 534)),
    ((834, 534), (842, 614), (798, 694), (716, 730)),
    ((716, 730), (624, 770), (512, 760), (432, 720)),
    ((432, 720), (364, 686), (312, 634), (280, 588)),
    ((280, 588), (258, 556), (246, 528), (250, 500)),
]
BODY = "M 250,500 " + " ".join(f"C {c1[0]},{c1[1]} {c2[0]},{c2[1]} {p1[0]},{p1[1]}" for _, c1, c2, p1 in BODY_SEGS) + " Z"

TAIL = (
    "M 268,536 "
    "C 220,500 158,476 104,478 "
    "C 92,514 118,550 162,568 "
    "C 200,584 240,582 268,562 "
    "C 272,586 272,600 268,620 "
    "C 240,600 200,598 162,614 "
    "C 118,632 92,668 104,704 "
    "C 158,706 220,682 268,646 Z"
)
# pectoral fin, rooted on the body's lower-left flank
FIN = (
    "M 402,690 "
    "C 414,752 462,806 524,836 "
    "C 546,798 536,748 508,708 "
    "C 480,668 428,662 402,690 Z"
)
MOUTH = "M 828,560 C 800,610 756,634 712,630 C 696,628 684,622 674,612"
EYE = (742, 492, 44)

# belly: the lower slice of the body, inset so it can never poke out
_pts = []
_p = BODY_SEGS[0][0]
for seg in BODY_SEGS:
    _pts.extend(bezier(*seg))
_cx = sum(p[0] for p in _pts) / len(_pts)
_cy = sum(p[1] for p in _pts) / len(_pts)
CUT = 622
_run = [p for p in _pts if p[1] > CUT]
if _run[0][0] > _run[-1][0]:
    _run.reverse()
BELLY_PTS = []
for x, y in _run:
    dx, dy = _cx - x, _cy - y
    d = math.hypot(dx, dy) or 1
    BELLY_PTS.append((x + 26 * dx / d, y + 26 * dy / d))
_x0, _y0 = BELLY_PTS[0]
_xn, _yn = BELLY_PTS[-1]
_w = _xn - _x0
# top edge bows downward so the belly reads as a crescent, not a sliced-off half
BELLY = ("M " + fmt(BELLY_PTS)
         + f" C {_xn - _w * 0.3:.1f},{_yn + 92:.1f} {_x0 + _w * 0.3:.1f},{_y0 + 92:.1f} {_x0:.1f},{_y0:.1f} Z")


def shape(steps, **kw):
    steps.append({"id": "draw_shape", "params": kw})


def path(steps, d, fill="none", stroke="none", sw=0, closed=True, name=None, opacity=None, effects=None):
    p = {"d": d, "closed": closed, "fill": fill, "stroke": stroke, "strokeWidth": sw}
    if name:
        p["name"] = name
    if opacity is not None:
        p["opacity"] = opacity
    if effects:
        p["effects"] = effects
    steps.append({"id": "draw_path", "params": p})


def text(steps, x, y, s, size, color, font="Helvetica", justify="center"):
    steps.append({"id": "text.create", "params": {
        "x": x, "y": y, "text": s, "size": size, "font": font, "justify": justify, "color": color}})


GLOW = {"color": "#4D6BFE", "opacity": 95, "blur": 32, "mode": "screen"}


def whale(steps, body, tail, belly, eye, pupil, shine, blush, mouth, spout,
          outline=None, sw=0, shadow=False, name="mascot"):
    def solid(d, fill, nm, shadowed=False):
        eff = None
        if shadow and shadowed:
            eff = [{"effect": "stylize.dropShadow",
                    "params": {"x": 6, "y": 12, "blur": 16, "color": "#0B1533", "opacity": 45, "mode": "multiply"}}]
        path(steps, d, fill=fill, stroke=outline or "none", sw=sw, name=nm, effects=eff)

    if shadow:
        shape(steps, shape="ellipse", x=250, y=858, width=520, height=58, fill="#0B1533",
              stroke="none", opacity=13, name="Ground shadow")

    path(steps, "M 600,356 C 596,332 590,316 578,304", stroke=spout, sw=10, closed=False,
         name="Spout stream")
    for cx, cy, r in [(566, 300, 15), (610, 262, 20), (562, 220, 25)]:
        shape(steps, shape="ellipse", x=cx - r, y=cy - r, width=r * 2, height=r * 2,
              fill=spout, stroke="none", name="Spout")

    solid(TAIL, tail, "Tail", shadowed=True)
    solid(BODY, body, "Body", shadowed=True)
    solid(BELLY, belly, "Belly")

    path(steps, MOUTH, stroke=mouth, sw=9, closed=False, name="Mouth")
    shape(steps, shape="ellipse", x=EYE[0] - EYE[2], y=EYE[1] - EYE[2], width=EYE[2] * 2, height=EYE[2] * 2,
          fill=eye, stroke="none", name="Eye")
    shape(steps, shape="ellipse", x=EYE[0] - 19, y=EYE[1] - 15, width=38, height=38, fill=pupil,
          stroke="none", name="Pupil")
    shape(steps, shape="ellipse", x=EYE[0] - 31, y=EYE[1] - 29, width=16, height=16, fill=shine,
          stroke="none", name="Eye shine")
    shape(steps, shape="ellipse", x=676, y=574, width=62, height=32, fill=blush, stroke="none",
          opacity=55, name="Blush")


# ----------------------------------------------------------------- style A: flat
def build_flat():
    steps = []
    shape(steps, shape="rectangle", x=0, y=0, width=TILE, height=TILE, fill="#F2F6FF", stroke="none", name="Backdrop")
    shape(steps, shape="ellipse", x=176, y=150, width=648, height=648, fill="#E3ECFF", stroke="none", name="Halo")
    for x, y, s in [(186, 306, 26), (826, 268, 34), (872, 700, 22), (160, 648, 18), (330, 168, 16), (742, 812, 20)]:
        path(steps,
             f"M {x},{y - s} Q {x + s * 0.18},{y - s * 0.18} {x + s},{y} "
             f"Q {x + s * 0.18},{y + s * 0.18} {x},{y + s} "
             f"Q {x - s * 0.18},{y + s * 0.18} {x - s},{y} "
             f"Q {x - s * 0.18},{y - s * 0.18} {x},{y - s} Z",
             fill="#A9BEFF", name="Sparkle")
    for cx, cy, r in [(872, 392, 20), (910, 330, 12), (898, 470, 14), (150, 452, 16), (112, 512, 10)]:
        shape(steps, shape="ellipse", x=cx - r, y=cy - r, width=r * 2, height=r * 2, fill="none",
              stroke="#A9BEFF", strokeWidth=6, name="Bubble")
    whale(steps,
          body="#4D6BFE", tail="#3B55E0", belly="#DCE8FF",
          eye="#FFFFFF", pupil="#121E42", shine="#FFFFFF", blush="#4D6BFE",
          mouth="#121E42", spout="#6F8BFF", shadow=True)
    return steps


# ----------------------------------------------------------------- style B: sticker
def build_sticker():
    steps = []
    shape(steps, shape="rectangle", x=0, y=0, width=TILE, height=TILE, fill="#FFE9D6", stroke="none", name="Backdrop")
    pts = []
    for i in range(28):
        a = i * math.pi / 14
        r = 500 if i % 2 == 0 else 350
        pts.append((500 + r * math.cos(a), 490 + r * math.sin(a)))
    path(steps, "M " + fmt(pts) + " Z", fill="#FFC79A", name="Burst")
    whale(steps,
          body="#4D6BFE", tail="#3352E8", belly="#FFFFFF",
          eye="#FFFFFF", pupil="#0E1B3D", shine="#FFFFFF", blush="#FF8FA8",
          mouth="#0E1B3D", spout="#7FA0FF",
          outline="#FFFFFF", sw=20, shadow=True)
    text(steps, 500, 930, "deepseek", 112, "#1B2A6B")
    return steps


# ----------------------------------------------------------------- style C: neon
def build_neon():
    steps = []
    shape(steps, shape="rectangle", x=0, y=0, width=TILE, height=TILE, fill="#070B1E", stroke="none", name="Backdrop")
    for i in range(1, 10):
        v = i * 100
        path(steps, f"M {v},0 L {v},{TILE}", stroke="#1A2450", sw=2, closed=False, name="Grid")
        path(steps, f"M 0,{v} L {TILE},{v}", stroke="#1A2450", sw=2, closed=False, name="Grid")

    stroke = "#AFC4FF"
    for d, nm in [(TAIL, "Tail"), (BODY, "Body"), (BELLY, "Belly")]:
        path(steps, d, stroke=stroke, sw=9, name=nm,
             effects=[{"effect": "stylize.outerGlow", "params": GLOW}])
    path(steps, MOUTH, stroke="#EAF1FF", sw=7, closed=False, name="Mouth",
         effects=[{"effect": "stylize.outerGlow", "params": {"color": "#7CF2E0", "opacity": 80, "blur": 18, "mode": "screen"}}])
    shape(steps, shape="ellipse", x=EYE[0] - 30, y=EYE[1] - 30, width=60, height=60, fill="#EAF1FF",
          stroke="none", name="Eye",
          effects=[{"effect": "stylize.outerGlow", "params": {"color": "#7CF2E0", "opacity": 90, "blur": 24, "mode": "screen"}}])
    shape(steps, shape="ellipse", x=EYE[0] - 15, y=EYE[1] - 12, width=30, height=30, fill="#0A1030",
          stroke="none", name="Pupil")

    teal = {"color": "#7CF2E0", "opacity": 90, "blur": 26, "mode": "screen"}
    path(steps, "M 600,356 C 596,332 590,316 578,304", stroke="#7CF2E0", sw=6, closed=False,
         name="Spout stream", effects=[{"effect": "stylize.outerGlow", "params": teal}])
    for cx, cy, r in [(566, 300, 10), (610, 262, 13), (562, 220, 16)]:
        shape(steps, shape="ellipse", x=cx - r, y=cy - r, width=r * 2, height=r * 2, fill="#7CF2E0",
              stroke="none", name="Spout", effects=[{"effect": "stylize.outerGlow", "params": teal}])
    for cx, cy, r in [(878, 398, 22), (914, 332, 12), (900, 476, 15), (168, 462, 17), (130, 520, 10)]:
        shape(steps, shape="ellipse", x=cx - r, y=cy - r, width=r * 2, height=r * 2, fill="none",
              stroke="#7CF2E0", strokeWidth=4, name="Bubble",
              effects=[{"effect": "stylize.outerGlow", "params": {"color": "#7CF2E0", "opacity": 70, "blur": 18, "mode": "screen"}}])

    text(steps, 500, 945, "deepseek", 78, "#EAF1FF")
    return steps


# ----------------------------------------------------------------- style D: doodle
def build_doodle():
    steps = []
    shape(steps, shape="rectangle", x=0, y=0, width=TILE, height=TILE, fill="#FFF8E7", stroke="none", name="Backdrop")
    # confetti
    for x, y, r, c in [(120, 220, 9, "#FF8FA8"), (880, 250, 7, "#4D6BFE"), (150, 760, 8, "#FFC24D"),
                       (860, 740, 9, "#7CF2E0"), (300, 140, 6, "#FF8FA8"), (700, 130, 8, "#7CF2E0"),
                       (940, 520, 6, "#FFC24D"), (80, 520, 7, "#4D6BFE")]:
        shape(steps, shape="ellipse", x=x - r, y=y - r, width=r * 2, height=r * 2, fill=c, stroke="none",
              name="Confetti")
    whale(steps,
          body="#8FC4FF", tail="#6FB0F2", belly="#EAF5FF",
          eye="#FFFFFF", pupil="#16213F", shine="#FFFFFF", blush="#FF9FB2",
          mouth="#16213F", spout="#8FC4FF", outline="#16213F", sw=13)
    text(steps, 500, 935, "hello, ocean", 64, "#16213F")
    return steps


def grad(stops, kind="linear", angle=90):
    return {"gradient": {"kind": kind, "angle": angle,
                        "stops": [{"offset": o, "color": c, **({"opacity": op} if op is not None else {})}
                                  for o, c, op in stops]}}


# ----------------------------------------------------------------- style E: sunset
# A silhouette against a big sun: the same paths, no face, pure shape.
def build_sunset():
    steps = []
    shape(steps, shape="rectangle", x=0, y=0, width=TILE, height=TILE, name="Sky",
          fill=grad([(0, "#FFB25E", None), (0.3, "#F2657A", None), (0.62, "#6B2B6E", None), (1, "#241046", None)]),
          stroke="none")
    shape(steps, shape="ellipse", x=180, y=250, width=640, height=640, name="Sun",
          fill=grad([(0, "#FFF4C2", None), (0.45, "#FFD166", None), (1, "#FF8A5C", None)], kind="radial"),
          stroke="none",
          effects=[{"effect": "stylize.outerGlow", "params": {"color": "#FF9A5C", "opacity": 85, "blur": 80, "mode": "screen"}}])
    # retro sun bands
    for i, (y, h) in enumerate([(612, 16), (652, 22), (700, 30), (756, 40)]):
        shape(steps, shape="rectangle", x=0, y=y, width=TILE, height=h, fill="#F2657A", stroke="none",
              opacity=55, name="Sun band")
    # water
    shape(steps, shape="rectangle", x=0, y=812, width=TILE, height=TILE - 812, name="Sea",
          fill=grad([(0, "#4A1B52", 70), (1, "#170A2E", None)]), stroke="none")
    # whale, flat silhouette: scaled to 0.62 and placed on the sun's lower edge
    S, ROT, PIV, TX, TY = 0.62, -8.0, (544, 551), -44, 9
    def T(d):
        return xf(d, S, TX, TY, ROT, PIV)

    for cx, cy, r in [(604, 372, 15), (648, 330, 20), (598, 286, 25)]:
        shape(steps, shape="ellipse", x=cx - r, y=cy - r, width=r * 2, height=r * 2, fill="#FFD9A8",
              stroke="none", name="Spout", opacity=85)
    path(steps, T(TAIL), fill="#2A1140", name="Tail")
    path(steps, T(BODY), fill="#2A1140", name="Body")
    path(steps, T(BELLY), fill="#F6C08A", name="Belly", opacity=38)
    ex, ey = float(T(f"{EYE[0]},{EYE[1]}").split(",")[0]), float(T(f"{EYE[0]},{EYE[1]}").split(",")[1])
    shape(steps, shape="ellipse", x=ex - 11, y=ey - 11, width=22, height=22, fill="#FFF1D6",
          stroke="none", name="Eye")
    text(steps, 500, 948, "deepseek", 84, "#FFE3B0")
    return steps


BUILDERS = [("flat", build_flat), ("sticker", build_sticker), ("neon", build_neon),
            ("doodle", build_doodle), ("sunset", build_sunset)]


# A clean render on magenta, used by build_pixel.py to derive the pixel-art grid.
def build_pixelsrc():
    steps = []
    shape(steps, shape="rectangle", x=0, y=0, width=TILE, height=TILE, fill="#FF00FF", stroke="none", name="Backdrop")
    whale(steps,
          body="#4D6BFE", tail="#3B55E0", belly="#DCE8FF",
          eye="#FFFFFF", pupil="#121E42", shine="#FFFFFF", blush="#4D6BFE",
          mouth="#121E42", spout="#6F8BFF")
    return steps

session = []
for style, fn in BUILDERS:
    steps = fn()
    session.append({"tool": "run_command", "args": {"command": "file.new", "params": {
        "width": TILE, "height": TILE, "units": "Pixels", "name": f"whale-{style}"}}})
    session.append({"tool": "command_batch", "args": {"atomic": True, "label": f"whale {style}", "steps": steps}})
    session.append({"tool": "save_file", "args": {"path": f"work/out/whale-{style}.vectorcraft"}})
    session.append({"tool": "export", "args": {"path": f"work/out/whale-{style}.png", "format": "png", "scale": 1}})
    session.append({"tool": "export", "args": {"path": f"work/out/whale-{style}.svg", "format": "svg"}})

steps = build_pixelsrc()
session.append({"tool": "run_command", "args": {"command": "file.new", "params": {
    "width": TILE, "height": TILE, "units": "Pixels", "name": "whale-pixelsrc"}}})
session.append({"tool": "command_batch", "args": {"atomic": True, "label": "whale pixelsrc", "steps": steps}})
session.append({"tool": "export", "args": {"path": "work/out/_pixelsrc.png", "format": "png", "scale": 1}})

for line in session:
    print(json.dumps(line))
