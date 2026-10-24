#!/usr/bin/env python3
"""VirelaiOS — commemorative plate V1R00. The Bare-Metal Vigil: one candle
flame standing upright on a bare Apple-silicon die, the whole machine lit
by a single warm pool of UEFI light in deep navy darkness. Brass-and-silicon
die in golds; Mascots candle glyph etched on the die face as the machine's
own sigil. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("VirelaiOS — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A0E"   # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def rrect(x0, y0, x1, y1, r):
    return (f"M{x0+r},{y0} L{x1-r},{y0} Q{x1},{y0} {x1},{y0+r} L{x1},{y1-r} "
            f"Q{x1},{y1} {x1-r},{y1} L{x0+r},{y1} Q{x0},{y1} {x0},{y1-r} "
            f"L{x0},{y0+r} Q{x0},{y0} {x0+r},{y0} Z")

BG_GRAD = lin("#0C1830", "#030713", (500, 0), (500, 1000))
PLATE_GRAD = rad({"offset": 0, "color": "#1B2D4E"}, {"offset": 0.68, "color": "#0D1B33"},
                 {"offset": 1, "color": "#050C1C"})
BRASS_GRAD = lin("#E8C26A", "#8A5E22", (350, 555), (660, 720))
DIE_GRAD = lin("#35415A", "#131C2C", (430, 588), (575, 690))
FLAME_OUT = rad({"offset": 0, "color": "#FFD98A"}, {"offset": 0.62, "color": "#F59A33"},
                {"offset": 1, "color": "#D95E14"})
FLAME_IN = rad({"offset": 0, "color": "#FFF6D2"}, {"offset": 1, "color": "#FFC65E"})

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6428", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8B56A", strokeWidth=3, opacity=35)
# faint starfield dust inside the disc
for i, (x, y, w) in enumerate([(210,190,4),(775,175,5),(160,430,4),(845,440,5),(250,745,4),
                               (750,750,5),(340,115,3),(670,110,4),(135,600,3),(870,590,4)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Dust {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#C8D6F0", opacity=22, stroke=NONE)

# --- the warm pool: light radiating out from the flame ------------------------
d.shape("ellipse", "UEFI pool", x=180, y=170, width=640, height=600,
        fill=rad({"offset": 0, "color": "#F0A83C", "opacity": 0.42},
                 {"offset": 0.55, "color": "#D88A28", "opacity": 0.16},
                 {"offset": 1, "color": "#D88A28", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Glow column", x=380, y=180, width=240, height=560,
        fill=rad({"offset": 0, "color": "#FFCA6E", "opacity": 0.30},
                 {"offset": 1, "color": "#FFCA6E", "opacity": 0}), stroke=NONE)

# --- circuit traces out of the die, fading into the navy ----------------------
TRACES = [
    # (start on die edge, elbow, end point, via?)
    ((300, 596), (236, 596), (196, 636)),
    ((300, 660), (230, 660), (190, 696)),
    ((300, 630), (250, 630), (214, 594)),
    ((700, 596), (764, 596), (804, 636)),
    ((700, 660), (770, 660), (810, 696)),
    ((700, 630), (750, 630), (786, 594)),
    ((430, 705), (430, 748), (388, 790)),
    ((570, 705), (570, 748), (612, 790)),
]
for i, (p0, p1, p2) in enumerate(TRACES):
    assert on_disc(*p2, 18), p2
    d.path(f"M{p0[0]},{p0[1]} L{p1[0]},{p1[1]} L{p2[0]},{p2[1]}",
           f"Trace {i+1}", fill=NONE, stroke="#C8973F", strokeWidth=5, opacity=45,
           cap="round", join="round")
    d.shape("ellipse", f"Via {i+1}", x=p2[0]-5, y=p2[1]-5, width=10, height=10,
            fill="#E8B95C", opacity=55, stroke=NONE)

# --- die package ---------------------------------------------------------------
# soft shadow under the package
d.shape("ellipse", "Die shadow", x=295, y=676, width=410, height=70,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.45},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
# substrate
d.path(rrect(292, 558, 708, 706, 16), "Substrate", fill=BRASS_GRAD,
       stroke="#5E4014", strokeWidth=5)
# substrate warm sheen from the flame above
d.path(rrect(292, 558, 708, 610, 16), "Substrate sheen",
       fill=lin("#FFDF96", "#FFDF96", (500, 558), (500, 610)), opacity=22, stroke=NONE)
# gold contact pads along the top edge strip
for i, x in enumerate(range(318, 685, 26)):
    if 400 <= x <= 600:
        continue
    d.shape("ellipse", f"Pad {i+1}", x=x-4, y=572, width=8, height=8,
            fill="#F2D488", opacity=75, stroke=NONE)
# silicon die seated on the substrate
d.path(rrect(392, 592, 608, 692, 8), "Silicon die", fill=DIE_GRAD,
       stroke="#0C1420", strokeWidth=4)
# die etch: faint circuit lines on the silicon face
for i, (y, x0, x1) in enumerate([(616, 410, 470), (640, 412, 452), (664, 410, 480),
                                 (616, 530, 590), (640, 548, 588), (664, 522, 592)]):
    d.path(f"M{x0},{y} L{x1},{y}", f"Etch {i+1}", fill=NONE,
           stroke="#9DB4D8", strokeWidth=2.5, opacity=30, cap="round")
for i, (x, y0, y1) in enumerate([(424, 600, 612), (578, 600, 612)]):
    d.path(f"M{x},{y0} L{x},{y1}", f"Etch v{i+1}", fill=NONE,
           stroke="#9DB4D8", strokeWidth=2.5, opacity=25, cap="round")
# the machine's own sigil: Mascots candle glyph etched center-die
d.text("\ue006", "Die sigil", x=500, y=662, size=52, font="Virelai Mascots",
       color="#E8B95C", justify="center")
# light catching the die's top face
d.path(rrect(392, 592, 608, 640, 8), "Die top light",
       fill=lin("#FFC964", "#FFC964", (500, 592), (500, 640)), opacity=14, stroke=NONE)

# --- the flame ------------------------------------------------------------------
# wick standing on the die top edge
d.path("M500,592 C499,580 499,570 500,558", "Wick", fill=NONE,
       stroke="#3A2812", strokeWidth=7, cap="round")
# halo behind the flame
d.shape("ellipse", "Flame halo", x=404, y=380, width=192, height=210,
        fill=rad({"offset": 0, "color": "#FFC964", "opacity": 0.55},
                 {"offset": 1, "color": "#FFC964", "opacity": 0}), stroke=NONE)
# outer teardrop
d.path("M500,562 C461,548 449,506 466,466 C479,436 491,420 500,398 "
       "C509,420 521,436 534,466 C551,506 539,548 500,562 Z",
       "Flame outer", fill=FLAME_OUT, stroke="#A8430C", strokeWidth=3)
# inner flame
d.path("M500,552 C476,541 470,512 481,486 C489,468 495,455 500,441 "
       "C505,455 511,468 519,486 C530,512 524,541 500,552 Z",
       "Flame inner", fill=FLAME_IN, stroke=NONE)
# white-hot core at the wick
d.shape("ellipse", "Flame core", x=487, y=512, width=26, height=38,
        fill=rad({"offset": 0, "color": "#FFFBEA"}, {"offset": 1, "color": "#FFE9A8"}),
        opacity=95, stroke=NONE)
# ember flecks rising
for i, (x, y, w, o) in enumerate([(468,352,7,60),(538,330,6,55),(512,288,5,45),(482,308,4,40)]):
    assert on_disc(x, y, 10)
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFB84E", opacity=o, stroke=NONE)

# --- name + role ---------------------------------------------------------------
d.text("VIRELAIOS", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#F0D9A8", justify="center")
LINE2, SZ2, TRK = "FREESTANDING AARCH64 OS", 23, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C49A58", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
# Virelai Sans has no digits — set "64" (bytes 18..20) in Source Sans 3
d.cmd("text.setStyle", "Second line digits", id=r["id"], font="Source Sans 3",
      start=18, end=20, size=SZ2 + 2)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("virelaios-V1R00")
