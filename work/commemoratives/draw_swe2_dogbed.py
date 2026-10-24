#!/usr/bin/env python3
"""swe2-dogbed — commemorative plate V1R00. The Cognition Annals: a
phosphor-CRT terminal glowing in the dark, its curved glass showing a tiny
museum exhibit — miniature model-line artifacts on velvet plinths, SWE-1
through SWE-2 in a row. Green phosphor on black glass; a museum that only
exists on a thirteen-page terminal. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("swe2-dogbed — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#0A120C"   # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

PHOS, PHOS_HI, PHOS_DIM = "#46D992", "#BFFFD0", "#1E7A4E"
SCREEN = ("M312,244 Q500,216 688,244 Q704,248 704,390 "
         "Q704,530 688,534 Q500,560 312,534 Q296,530 296,390 Q296,248 312,244 Z")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#0B100C", "#030503", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#1B2A20"},
                 {"offset": 0.65, "color": "#0D170F"},
                 {"offset": 1, "color": "#050A06"}),
        stroke="#3E5544", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#7CE8B4", strokeWidth=3, opacity=22)
# dark-room dust
for i, (x, y, w, o) in enumerate([(215,205,4,22),(795,195,5,22),(160,450,4,20),
                                  (848,425,4,20),(245,750,4,18),(750,775,5,18),
                                  (355,105,3,22),(645,100,4,20),(140,595,3,18),(860,585,4,20)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Dust {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#7CE8B4", opacity=o, stroke=NONE)
# the terminal's own light spilling into the dark room
d.shape("ellipse", "CRT ambient", x=230, y=170, width=540, height=500,
        fill=rad({"offset": 0, "color": "#46D992", "opacity": 0.14},
                 {"offset": 1, "color": "#46D992", "opacity": 0}), stroke=NONE)

# --- the ground: a dark desk/mound closing on the disc's own arc -----------------
d.path("M206.1,760 Q500,682 793.9,760 A420,420 0 0 1 206.1,760 Z", "Mound",
       fill=lin("#0E1710", "#050805", (500, 690), (500, 880)), stroke=NONE)
# green pool of screen-light on the desk
d.shape("ellipse", "Desk pool", x=330, y=690, width=340, height=60,
        fill=rad({"offset": 0, "color": "#46D992", "opacity": 0.18},
                 {"offset": 1, "color": "#46D992", "opacity": 0}), stroke=NONE)

# --- the monitor ------------------------------------------------------------------
d.shape("ellipse", "Monitor shadow", x=340, y=690, width=320, height=42,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.55},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
# stand neck + foot
d.path("M472,584 L472,648 Q472,660 462,662 L452,664 L452,674 L548,674 L548,664 "
       "L538,662 Q528,660 528,648 L528,584 Z",
       "Stand", fill=lin("#2A3430", "#101612", (472, 584), (528, 674)),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Stand foot", x=396, y=662, width=208, height=26,
        fill=lin("#323E38", "#141B17", (396, 662), (604, 688)),
        stroke=INK, strokeWidth=3.5)
# bezel
d.path("M290,230 Q290,208 312,206 L688,206 Q710,208 710,230 L710,556 "
       "Q710,578 688,580 L312,580 Q290,578 290,556 Z",
       "Bezel", fill=lin("#3A463F", "#161D1A", (290, 206), (710, 580)),
       stroke=INK, strokeWidth=5)
# bezel sheen, top-left
d.path("M300,236 Q300,218 318,216 L500,216 L500,236 Q360,232 300,236 Z",
       "Bezel sheen", fill="#5E6E64", opacity=30, stroke=NONE)
# lower bezel chin: vents + status LED
for i, x in enumerate(range(360, 640, 20)):
    d.path(f"M{x},562 L{x+10},562", f"Vent {i+1}", fill=NONE,
           stroke="#0E1411", strokeWidth=3, opacity=70, cap="round")
d.shape("ellipse", "Power LED", x=664, y=556, width=9, height=9,
        fill=rad({"offset": 0, "color": "#BFFFD0"}, {"offset": 1, "color": "#2E9A5C"}),
        stroke="#0E2A1C", strokeWidth=2)
d.shape("ellipse", "LED glow", x=655, y=547, width=27, height=27,
        fill=rad({"offset": 0, "color": "#46D992", "opacity": 0.5},
                 {"offset": 1, "color": "#46D992", "opacity": 0}), stroke=NONE)

# --- the curved glass -------------------------------------------------------------
d.path(SCREEN, "Glass", fill=rad({"offset": 0, "color": "#0C2416"},
                                 {"offset": 0.7, "color": "#061308"},
                                 {"offset": 1, "color": "#020703"}),
       stroke="#0A1A0E", strokeWidth=4)

# === inside the glass: the museum (all phosphor monochrome) ========================
# back wall + floor of the tiny hall
d.path("M330,270 L670,270 L678,470 L322,470 Z", "Hall wall",
       fill=lin("#0E2A1A", "#050F08", (500, 270), (500, 470)), stroke=NONE)
d.path("M322,470 L678,470 L690,524 L310,524 Z", "Hall floor",
       fill=lin("#0A1E12", "#04100A", (500, 470), (500, 524)), stroke=NONE)
# faint hall depth: receding wall lines
for i, (x0, y0, x1, y1) in enumerate([(330,270,322,470),(670,270,678,470),
                                      (500,262,500,300)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Hall line {i+1}", fill=NONE,
           stroke="#1E4A30", strokeWidth=2, opacity=35, cap="round")

def plinth(cx, label, art):
    """A velvet plinth with a tiny model artifact and a lit label."""
    # spot cone from the gallery ceiling
    d.path(f"M{cx-8},272 L{cx-40},428 L{cx+40},428 Z", f"{label} spot",
           fill="#BFFFD0", opacity=8, stroke=NONE)
    d.path(f"M{cx-4},272 L{cx-22},428 L{cx+22},428 Z", f"{label} spot core",
           fill="#D8FFE2", opacity=10, stroke=NONE)
    # pedestal: velvet-wrapped block
    d.path(f"M{cx-34},428 L{cx+34},428 L{cx+38},508 L{cx-38},508 Z",
           f"{label} plinth", fill=lin("#16402A", "#08180F", (cx, 428), (cx, 508)),
           stroke="#0A2416", strokeWidth=3)
    d.shape("ellipse", f"{label} velvettap", x=cx-34, y=424, width=68, height=10,
            fill="#1E4A30", stroke="#0A2416", strokeWidth=2)
    # velvet sheen band
    d.path(f"M{cx-34},448 L{cx+34},448 L{cx+35},456 L{cx-35},456 Z",
           f"{label} sheen", fill="#2E6B48", opacity=30, stroke=NONE)
    # brass label rail + the model name in phosphor
    d.path(f"M{cx-26},478 L{cx+26},478 L{cx+26},492 L{cx-26},492 Z",
           f"{label} rail", fill="#0A1F14", stroke="#46D992",
           strokeWidth=1.5, opacity=90)
    d.text(label, f"{label} tag", x=cx, y=489, size=10, font="Source Sans 3",
           color="#7CE8B4", justify="center")
    art(cx)

def art_chip(cx):
    """SWE-1: the original — a chunky little proto-core."""
    d.path(f"M{cx-16},396 L{cx+16},396 L{cx+16},424 L{cx-16},424 Z",
           "SWE-1 body", fill=lin("#3FD68F", "#0E5A34", (cx, 396), (cx, 424)),
           stroke="#0A2E1C", strokeWidth=2.5)
    for j, dx in enumerate((-8, 0, 8)):
        d.path(f"M{cx+dx},396 L{cx+dx},388", f"SWE-1 pin {j+1}", fill=NONE,
               stroke="#7CE8B4", strokeWidth=2.5, cap="round")
    d.shape("ellipse", "SWE-1 eye", x=cx-4, y=404, width=8, height=8,
            fill="#0A2E1C", stroke=NONE)

def art_vessel(cx):
    """SWE-1.5: the interim — a small lidded vessel."""
    d.path(f"M{cx-14},392 L{cx+14},392 L{cx+10},398 L{cx+10},400 "
           f"C{cx+18},406 {cx+18},420 {cx},426 C{cx-18},420 {cx-18},406 "
           f"{cx-10},400 L{cx-10},398 Z",
           "SWE-1.5 body", fill=lin("#55E2A2", "#0E5A34", (cx, 392), (cx, 426)),
           stroke="#0A2E1C", strokeWidth=2.5)
    d.path(f"M{cx-16},398 L{cx+16},398", "SWE-1.5 collar", fill=NONE,
           stroke="#0A2E1C", strokeWidth=2, cap="round")

def art_obelisk(cx):
    """SWE-2: the standing obelisk, lit slit down its face."""
    d.path(f"M{cx-11},426 L{cx-9},390 L{cx-5},378 L{cx+5},378 L{cx+9},390 "
           f"L{cx+11},426 Z",
           "SWE-2 obelisk", fill=lin("#6FEAB2", "#12683C", (cx, 378), (cx, 426)),
           stroke="#0A2E1C", strokeWidth=2.5)
    d.path(f"M{cx},384 L{cx},420", "SWE-2 slit", fill=NONE,
           stroke="#D8FFE2", strokeWidth=3, opacity=85, cap="round")
    d.shape("ellipse", "SWE-2 cap light", x=cx-4, y=374, width=8, height=6,
            fill="#BFFFD0", stroke=NONE)

plinth(384, "SWE-1", art_chip)
plinth(500, "SWE-1.5", art_vessel)
plinth(616, "SWE-2", art_obelisk)

# terminal status line + block cursor, bottom of the glass
d.text("PG 01/13", "Page counter", x=322, y=532, size=11,
       font="Source Sans 3", color="#46D992", justify="left")
d.path("M388,522 L396,522 L396,532 L388,532 Z", "Cursor",
       fill="#46D992", opacity=80, stroke=NONE)

# scanlines + curved-glass glare over the museum
for i, y in enumerate(range(252, 530, 9)):
    d.path(f"M316,{y} L684,{y}", f"Scan {i+1}", fill=NONE,
           stroke="#0A1A0E", strokeWidth=2.5, opacity=25)
d.path("M330,250 L430,250 L360,530 L318,530 Z", "Glass glare",
       fill="#D8FFE2", opacity=5, stroke=NONE)
d.path("M450,250 L470,250 L400,530 L390,530 Z", "Glass glare 2",
       fill="#D8FFE2", opacity=4, stroke=NONE)
# glass rim light, top edge
d.path("M330,244 Q500,222 670,244", "Glass rim light", fill=NONE,
       stroke="#9FFFD0", strokeWidth=3, opacity=30, cap="round")

# --- name + role ------------------------------------------------------------------
NAME = "SWE2-DOGBED"
rn = d.text(NAME, "Name", x=500, y=930, size=56, font="Virelai Sans",
            color="#D8FFE2", justify="center")
# Virelai Sans has no digits — set "2" (bytes 3..4) in Source Sans 3
d.cmd("text.setStyle", "Name digit", id=rn["id"], font="Source Sans 3",
      start=3, end=4, size=58)
LINE2, SZ2, TRK = "PHOSPHOR-CRT MUSEUM", 23, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#6FD8A4", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
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

d.finish("swe2-dogbed-V1R00")
