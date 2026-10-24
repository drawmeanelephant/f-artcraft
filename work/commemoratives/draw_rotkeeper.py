#!/usr/bin/env python3
"""rotkeeper — commemorative plate V1R00. What Lives in /bones/: a slate
headstone in a dark garden, carved with faint Markdown syntax instead of a
name; resurrection fern growing green across its face; a keeper's lantern
hanging off one corner. Moss, lamplight, and Bash.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("rotkeeper — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#0B0E0C"              # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def quad_bez(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    tx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    ty = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return (x, y), (tx, ty)

def carve(dstr, label):
    """An engraved mark: dark groove + a light edge shifted down-right."""
    d.path(dstr, label + " groove", fill=NONE, stroke="#222C33",
           strokeWidth=3, opacity=60, cap="round")
    import re
    d2 = re.sub(r"(\d+\.?\d*),(\d+\.?\d*)",
                lambda m: f"{float(m.group(1))+1.4:.1f},{float(m.group(2))+1.6:.1f}",
                dstr)
    d.path(d2, label + " edge", fill=NONE, stroke="#96A4AE",
           strokeWidth=2, opacity=30, cap="round")

def frond(p0, p1, p2, label, n=9, size0=15):
    """A resurrection-fern frond: curved stem with paired pinnate leaflets
    swept forward toward the tip."""
    d.path(f"M{p0[0]},{p0[1]} Q{p1[0]},{p1[1]} {p2[0]},{p2[1]}",
           label + " stem", fill=NONE, stroke="#3E7A46", strokeWidth=4.5,
           opacity=88, cap="round")
    for j in range(n):
        t = 0.14 + 0.80 * j / (n - 1)
        (x, y), (tx, ty) = quad_bez(p0, p1, p2, t)
        ln = math.hypot(tx, ty) or 1
        ux, uy = tx/ln, ty/ln
        s = size0 * (1 - 0.62 * t)
        for k, sgn in enumerate((-1, 1)):
            # leaflet angled ~55 degrees off the stem, raked toward the tip
            a = math.radians(55 * sgn)
            dx = ux*math.cos(a) - uy*math.sin(a)
            dy = ux*math.sin(a) + uy*math.cos(a)
            d.path(f"M{x:.1f},{y:.1f} L{x+dx*s*1.7:.1f},{y+dy*s*1.7:.1f}",
                   f"{label} leaflet {j+1}{'ab'[k]}", fill=NONE,
                   stroke="#55A45C" if (j + k) % 2 else "#41894A",
                   strokeWidth=max(3.0, s*0.5), opacity=90, cap="round")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#0B1210", "#040706", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#213830"},
                 {"offset": 0.62, "color": "#122019"},
                 {"offset": 1, "color": "#080F0C"}),
        stroke="#41584C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DCD0", strokeWidth=3, opacity=22)
# night garden: a thin moon and a scatter of stars
d.shape("ellipse", "Moon halo", x=205, y=128, width=130, height=130,
        fill=rad({"offset": 0, "color": "#D8E4D8", "opacity": 0.22},
                 {"offset": 1, "color": "#D8E4D8", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Moon", x=238, y=158, width=62, height=62,
        fill=rad({"offset": 0, "color": "#E6EEE2"},
                 {"offset": 1, "color": "#9CAFA2"}), stroke=NONE)
d.shape("ellipse", "Moon shade", x=262, y=168, width=44, height=44,
        fill="#122019", opacity=55, stroke=NONE)
for i, (x, y, w) in enumerate([(320,110,3),(400,150,2.6),(190,300,3),(770,160,3),
                               (830,270,3.4),(160,430,2.6),(690,135,2.6),(860,430,3)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E4D8", opacity=45, stroke=NONE)
# low mist band hanging behind the stone
d.shape("ellipse", "Mist", x=180, y=600, width=640, height=90,
        fill=rad({"offset": 0, "color": "#9FB8AC", "opacity": 0.10},
                 {"offset": 1, "color": "#9FB8AC", "opacity": 0}), stroke=NONE)

# --- the slate headstone ------------------------------------------------------
# arched slab: flat sides, semicircular crown, base sunk in the ground
STONE = ("M370,726 L370,414 Q370,318 500,318 Q630,318 630,414 L630,726 Z")
d.path(STONE, "Headstone",
       fill=lin("#7E8C96", "#3A464F", (500, 318), (500, 726)),
       stroke="#232C32", strokeWidth=5)
# inner panel line, inset from the slab's silhouette
d.path("M386,712 L386,416 Q386,334 500,334 Q614,334 614,416 L614,712",
       "Stone inset", fill=NONE, stroke="#5E6C76", strokeWidth=2.5, opacity=50)
# a hairline crack wandering down from the crown
d.path("M548,320 L540,368 L552,410 L544,452 L550,486", "Crack",
       fill=NONE, stroke="#222C33", strokeWidth=2.5, opacity=45, cap="round")
# slate striations
for i, y in enumerate((455, 545, 640)):
    d.path(f"M382,{y} Q500,{y+14} 618,{y}", f"Striation {i+1}",
           fill=NONE, stroke="#4A5860", strokeWidth=2.5, opacity=35, cap="round")

# --- the carved inscription: faint Markdown syntax in place of a name ---------
carve("M478,382 L478,406 M492,382 L492,406 M472,390 L498,390 M472,398 L498,398",
      "Carve hash")
carve("M440,442 L440,458 M448,442 L448,458 M436,447 L452,447 M436,453 L452,453",
      "Carve hash2")
carve("M464,442 L464,458 M472,442 L472,458 M460,447 L476,447 M460,453 L476,453",
      "Carve hash2b")
carve("M496,448 L528,448", "Carve dash")
carve("M452,496 L464,508 L452,520", "Carve quote")
carve("M478,507 L524,507", "Carve text")
carve("M452,556 L468,556", "Carve item")
d.path("M486,548 L502,548 L502,564 L486,564 Z", "Carve checkbox groove",
       fill=NONE, stroke="#222C33", strokeWidth=3, opacity=60)
d.path("M487.5,549.6 L503.5,549.6 L503.5,565.6 L487.5,565.6 Z",
       "Carve checkbox edge", fill=NONE, stroke="#96A4AE",
       strokeWidth=2, opacity=30)
carve("M516,556 L544,556", "Carve item2")
# three backticks: short angled ticks in a row
for i, x in enumerate((466, 482, 498)):
    carve(f"M{x},608 L{x+9},616", f"Carve tick{i+1}")
carve("M524,612 L556,612", "Carve fence tail")
# worn footer lines
carve("M462,652 L538,652", "Carve footer1")
carve("M478,676 L522,676", "Carve footer2")

# --- the ground: a dark mound closing on the disc's own arc --------------------
d.path("M206.1,760 Q500,682 793.9,760 A420,420 0 0 1 206.1,760 Z", "Mound",
       fill=lin("#1B2A1E", "#0B130D", (500, 690), (500, 880)), stroke=NONE)
d.shape("ellipse", "Stone contact shadow", x=360, y=714, width=280, height=22,
        fill="#060B08", opacity=50, stroke=NONE)

# moss creeping over the base and up the left flank
for i, (x, y, w, h) in enumerate([(392,700,64,34),(428,714,88,30),(560,712,96,32),
                                  (610,696,54,30),(376,640,30,58),(382,592,22,44)]):
    d.shape("ellipse", f"Moss {i+1}", x=x-w/2, y=y-h/2, width=w, height=h,
            fill=rad({"offset": 0, "color": "#4A6B3E"},
                     {"offset": 1, "color": "#22351F"}), opacity=72, stroke=NONE)

# grass tufts on the mound
for i, (x, y, h) in enumerate([(280,758,26),(330,742,20),(430,724,22),(560,724,24),
                               (640,730,20),(720,748,26),(766,766,18),(240,782,18)]):
    for k, lean in enumerate((-9, 0, 9)):
        d.path(f"M{x+lean*0.4},{y} Q{x+lean*0.8},{y-h*0.7} {x+lean},{y-h}",
               f"Grass {i+1}{'abc'[k]}", fill=NONE, stroke="#2E4A30",
               strokeWidth=3, opacity=80, cap="round")

# --- resurrection fern, green across the face ----------------------------------
frond((430, 706), (398, 590), (402, 452), "Fern A", n=9, size0=15)
frond((566, 710), (556, 570), (524, 428), "Fern B", n=9, size0=15)
frond((392, 372), (410, 430), (440, 540), "Fern C", n=7, size0=11)
frond((614, 668), (606, 570), (596, 486), "Fern D", n=7, size0=11)

# --- the keeper's lantern, hung off the top-right corner -----------------------
LX, LY = 676, 408                          # lantern centre
# iron arm rising off the stone's right flank
d.path("M628,428 C660,424 668,398 672,382", "Lantern arm",
       fill=NONE, stroke="#24292E", strokeWidth=5, cap="round")
d.shape("ellipse", "Hang ring", x=LX-5, y=372, width=10, height=10,
        fill=NONE, stroke="#24292E", strokeWidth=3)
# cap + cage + base
d.path(f"M{LX-13},392 L{LX+13},392 L{LX+9},378 L{LX-9},378 Z", "Lantern cap",
       fill=lin("#3E454C", "#22262B", (LX, 378), (LX, 392)), stroke="#191D20",
       strokeWidth=2.5)
d.path(f"M{LX-12},394 L{LX+12},394 L{LX+15},436 L{LX-15},436 Z", "Lantern cage",
       fill=lin("#FFC26A", "#B06E28", (LX, 394), (LX, 436)), opacity=38,
       stroke="#1B1F22", strokeWidth=3)
for i, xoff in enumerate((-6, 6)):
    d.path(f"M{LX+xoff},395 L{LX+xoff*1.25},435", f"Cage mullion {i+1}",
           fill=NONE, stroke="#1B1F22", strokeWidth=2.5, opacity=80)
d.path(f"M{LX-15},436 L{LX+15},436 L{LX+10},444 L{LX-10},444 Z", "Lantern base",
       fill="#22262B", stroke="#191D20", strokeWidth=2.5)
# the flame and its light
d.shape("ellipse", "Flame glow", x=LX-13, y=LY-16, width=26, height=32,
        fill=rad({"offset": 0, "color": "#FFE9B0", "opacity": 0.95},
                 {"offset": 1, "color": "#FFB84E", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Flame", x=LX-4, y=LY-7, width=8, height=14,
        fill="#FFE9B0", stroke=NONE)
# lamplight: a halo on the garden, a wash on the stone, a pool on the ground
d.shape("ellipse", "Lamp halo", x=LX-140, y=LY-140, width=280, height=280,
        fill=rad({"offset": 0, "color": "#FFC878", "opacity": 0.20},
                 {"offset": 0.55, "color": "#FFC878", "opacity": 0.07},
                 {"offset": 1, "color": "#FFC878", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Stone wash", x=545, y=400, width=210, height=270,
        fill=rad({"offset": 0, "color": "#FFC878", "opacity": 0.11},
                 {"offset": 1, "color": "#FFC878", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Ground pool", x=600, y=726, width=180, height=52,
        fill=rad({"offset": 0, "color": "#FFC878", "opacity": 0.20},
                 {"offset": 1, "color": "#FFC878", "opacity": 0}), stroke=NONE)

# --- name + role ---------------------------------------------------------------
d.text("ROTKEEPER", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#DCE8E0", justify="center")
LINE2, SZ2, TRK = "BASH STATIC-SITE KEEPER", 23, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C89858", justify="center")
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

d.finish("rotkeeper-V1R00")
