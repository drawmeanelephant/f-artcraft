#!/usr/bin/env python3
"""oliver — commemorative plate V1R00. Three Streams In: three ribbons —
M for Markdown, T for Textile, C for Cooklang — braided down a loom's
warp into one deterministic engine core (a silver shuttle) that emits a
single steady beam of typed document. Indigo and silver; parsing as a
loom, not a parser. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("oliver — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#141126"   # warm dark indigo, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def smooth(pts, closed=False, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#0D1024", "#050614", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#2A3160"}, {"offset": 0.68, "color": "#171C40"},
                 {"offset": 1, "color": "#0B0E24"}),
        stroke="#7A84A8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D2EE", strokeWidth=3, opacity=30)
# faint constellation dust
for i, (x, y, w) in enumerate([(215,210,4),(790,200,5),(165,450,4),(845,420,4),(250,745,4),
                               (735,780,5),(350,110,3),(650,105,4),(140,600,3),(875,590,4)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Dust {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#C8D2EE", opacity=20, stroke=NONE)

# --- the loom's warp: faint vertical threads the ribbons weave through --------
for i, x in enumerate(range(400, 625, 25)):
    d.path(f"M{x},118 L{x},436", f"Warp {i+1}", fill=NONE,
           stroke="#8A92B8", strokeWidth=1.5, opacity=14, cap="round")
# heddle bar across the top of the braid field
d.path("M380,142 L620,142", "Heddle bar", fill=NONE, stroke="#7A84A8",
       strokeWidth=6, opacity=55, cap="round")

# --- the three ribbons, braided ------------------------------------------------
# each ribbon: sine-phase path converging on the shuttle's left horn (415,540)
RIBBONS = [
    ("M", "#5B6BE8", "#39448F"),   # Markdown — indigo
    ("T", "#9A6BD8", "#5B3C88"),   # Textile — violet-indigo
    ("C", "#C8CEDE", "#8A92AC"),   # Cooklang — silver
]
CORE_X, CORE_Y = 500, 545
def ribbon_pts(phase):
    pts = []
    for j in range(17):
        t = j / 16
        y = 118 + (CORE_Y - 118) * t
        amp = 165 * (1 - t) ** 0.9 + 8
        x = 500 + amp * math.sin(2 * math.pi * t * 1.5 + phase)
        pts.append((x, y))
    return pts

for i, (letter, col, dark) in enumerate(RIBBONS):
    pts = ribbon_pts(i * 2 * math.pi / 3)
    s = smooth(pts)
    # ribbon edge (dark under-stroke), satin band, center sheen
    d.path(s, f"Ribbon {letter} edge", fill=NONE, stroke=dark, strokeWidth=31, cap="round")
    d.path(s, f"Ribbon {letter}", fill=NONE,
           stroke=lin(col, dark, (380, 130), (620, 540)), strokeWidth=24, cap="round")
    d.path(s, f"Ribbon {letter} sheen", fill=NONE, stroke="#FFFFFF",
           strokeWidth=6, opacity=28, cap="round")
    # name chip at the tail
    x0, y0 = pts[0]
    assert on_disc(x0, y0, 30), (x0, y0)
    d.path(rot_rect_path(x0, y0 - 22, 52, 40, 0), f"Chip {letter}",
           fill=lin("#3A4278", "#232A52", (x0-26, y0-42), (x0+26, y0-2)),
           stroke="#8A92B8", strokeWidth=2.5)
    d.text(letter, f"Chip letter {letter}", x=x0, y=y0 - 10, size=26,
           font="Virelai Sans", color="#E8ECF8", justify="center")

# --- the core: a silver loom shuttle ---------------------------------------------
# glow pooling around the shuttle
d.shape("ellipse", "Core glow", x=330, y=430, width=340, height=230,
        fill=rad({"offset": 0, "color": "#AAB8F0", "opacity": 0.4},
                 {"offset": 1, "color": "#AAB8F0", "opacity": 0}), stroke=NONE)
# shuttle body: a pointed lens lying horizontal
d.path(f"M392,{CORE_Y} Q500,{CORE_Y-62} 608,{CORE_Y} "
       f"Q500,{CORE_Y+62} 392,{CORE_Y} Z",
       "Shuttle", fill=lin("#EEF1FA", "#8A92AC", (430, CORE_Y-50), (575, CORE_Y+55)),
       stroke="#4A5480", strokeWidth=5)
# inner lens (the wound weft)
d.path(f"M448,{CORE_Y} Q500,{CORE_Y-30} 552,{CORE_Y} "
       f"Q500,{CORE_Y+30} 448,{CORE_Y} Z",
       "Shuttle lens", fill=rad({"offset": 0, "color": "#F4F7FF"},
                                {"offset": 1, "color": "#5B66B8"}),
       stroke="#39448F", strokeWidth=3)
# wound-thread wraps across the lens — the braided input, wound for the shuttle
for i, xoff in enumerate((-24, -8, 8, 24)):
    d.path(f"M{CORE_X+xoff-7},{CORE_Y-22} Q{CORE_X+xoff},{CORE_Y} {CORE_X+xoff-7},{CORE_Y+22}",
           f"Weft wrap {i+1}", fill=NONE, stroke="#5B66B8", strokeWidth=3,
           opacity=55, cap="round")
# central knot where the three streams knot into one
d.shape("ellipse", "Weft knot", x=CORE_X-8, y=CORE_Y-8, width=16, height=16,
        fill=rad({"offset": 0, "color": "#FFFFFF"}, {"offset": 1, "color": "#8A92C8"}),
        stroke="#39448F", strokeWidth=2)
# shuttle top highlight
d.path(f"M420,{CORE_Y-18} Q500,{CORE_Y-48} 580,{CORE_Y-18}",
       "Shuttle sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=5,
       opacity=45, cap="round")

# --- the beam: one steady band of typed document ---------------------------------
BX0, BX1 = 604, 798
# beam halo
d.path(f"M{BX0},{CORE_Y-34} L{BX1},{CORE_Y-30} L{BX1},{CORE_Y+30} L{BX0},{CORE_Y+34} Z",
       "Beam halo", fill=lin("#C8D6FF", "#C8D6FF", (BX0, 0), (BX1, 0)),
       opacity=22, stroke=NONE)
d.path(f"M{BX0},{CORE_Y-18} L{BX1},{CORE_Y-15} L{BX1},{CORE_Y+15} L{BX0},{CORE_Y+18} Z",
       "Beam", fill=lin("#F4F8FF", "#9AABE0", (BX0, CORE_Y-18), (BX0, CORE_Y+18)),
       opacity=95, stroke=NONE)
# typed lines carried inside the beam (deterministic text)
for j, yoff in enumerate((-9, 0, 9)):
    for i, (xa, xb) in enumerate([(630, 678), (698, 744), (756, 792)]):
        d.path(f"M{xa},{CORE_Y+yoff} L{xb},{CORE_Y+yoff}", f"Beam type {j+1}-{i+1}",
               fill=NONE, stroke="#4A5480", strokeWidth=2.5, opacity=55, cap="round")

# the typed document arriving at the beam's end
DX, DY = 794, CORE_Y
d.path(rot_rect_path(DX + 26, DY, 66, 86, 0), "Typed document",
       fill=lin("#F4F1E8", "#C9C4B4", (DX, DY-43), (DX+52, DY+43)),
       stroke="#8A92B8", strokeWidth=3.5)
for j in range(4):
    d.path(f"M{DX+8},{DY-24+j*16} L{DX+44},{DY-24+j*16}", f"Doc line {j+1}",
           fill=NONE, stroke="#6A7290", strokeWidth=3, opacity=75, cap="round")
# fold mark on the page corner
d.path(f"M{DX+44},{DY-43} L{DX+59},{DY-30} L{DX+44},{DY-30} Z", "Doc fold",
       fill="#D8D2C0", stroke="#8A92B8", strokeWidth=2)
# document glow where the beam lands
d.shape("ellipse", "Doc glow", x=DX+6, y=DY-52, width=100, height=104,
        fill=rad({"offset": 0, "color": "#C8D6FF", "opacity": 0.35},
                 {"offset": 1, "color": "#C8D6FF", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Doc glow patch", x=DX-14, y=DY-50, width=50, height=100,
        fill=rad({"offset": 0, "color": "#F4F8FF", "opacity": 0.5},
                 {"offset": 1, "color": "#F4F8FF", "opacity": 0}), stroke=NONE)

# --- name + role ---------------------------------------------------------------
d.text("OLIVER", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#E8ECF8", justify="center")
LINE2, SZ2, TRK = "MARKUP PARSER IN ZIG", 24, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#9AA6D0", justify="center")
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

d.finish("oliver-V1R00")
