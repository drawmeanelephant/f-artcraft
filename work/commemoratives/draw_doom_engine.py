#!/usr/bin/env python3
"""doom-engine — commemorative plate V1R00. The GPL Corridor: a first-person
corridor in pure geometry — phosphor-green wall ribs receding to an ember-red
vanishing point, a pale heraldic shield standing on the boundary line where
the GPL world ends and the syscall ABI begins. Hell suggested, never quoted.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("doom-engine — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
VPX, VPY = 500, 424          # vanishing point, a touch above disc centre
HW, HH = 264, 272            # outer corridor frame half-extents about the VP
INK = "#0A0D08"              # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def pt(s, fx, fy):
    """Point on the corridor lattice: frame scale s, offset fraction fx/fy."""
    return (VPX + fx * HW * s, VPY + fy * HH * s)

def quad(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"

# corridor depth scales, near -> far
S = [1.0, 0.68, 0.46, 0.30, 0.20, 0.13, 0.085, 0.055]
SB = 0.30                    # boundary frame: GPL ends, syscall ABI begins
S_END = S[-1]

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#0B120B", "#040604", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#1E3020"},
                 {"offset": 0.65, "color": "#101E12"},
                 {"offset": 1, "color": "#070D08"}),
        stroke="#3E6B48", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BFE8C8", strokeWidth=3, opacity=25)
# patina flecks, phosphor-tinted
for i, (x, y, w) in enumerate([(215,235,7),(795,225,6),(150,470,8),(855,450,6),
                               (240,720,6),(760,745,8),(360,105,5),(640,110,6),
                               (130,610,5),(875,600,5),(420,830,5),(580,835,6)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Fleck {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#5E8A64", opacity=32, stroke=NONE)
# mouth ambience: faint phosphor bloom around the corridor entrance
d.shape("ellipse", "Mouth bloom", x=160, y=110, width=680, height=630,
        fill=rad({"offset": 0, "color": "#2E7A44", "opacity": 0.20},
                 {"offset": 0.75, "color": "#2E7A44", "opacity": 0.07},
                 {"offset": 1, "color": "#2E7A44", "opacity": 0}), stroke=NONE)

# --- corridor shell: floor, ceiling, walls ------------------------------------
floor = [pt(1, -1, 1), pt(1, 1, 1), pt(S_END, 1, 1), pt(S_END, -1, 1)]
ceil  = [pt(1, -1, -1), pt(1, 1, -1), pt(S_END, 1, -1), pt(S_END, -1, -1)]
left  = [pt(1, -1, -1), pt(1, -1, 1), pt(S_END, -1, 1), pt(S_END, -1, -1)]
right = [pt(1, 1, -1), pt(1, 1, 1), pt(S_END, 1, 1), pt(S_END, 1, -1)]
d.path(quad(floor), "Floor", fill=lin("#1E3020", "#0C1810", (500, VPY), (500, VPY + HH)), stroke=NONE)
d.path(quad(ceil), "Ceiling", fill=lin("#0C1610", "#182A1C", (500, VPY - HH), (500, VPY)), stroke=NONE)
d.path(quad(left), "Wall L", fill=lin("#1A2C1E", "#0B150E", (VPX - HW, 0), (VPX, 0)), stroke=NONE)
d.path(quad(right), "Wall R", fill=lin("#0B150E", "#1A2C1E", (VPX, 0), (VPX + HW, 0)), stroke=NONE)

# hell seep: ember gradient washing the stretch beyond the boundary
for name, pts in (("Floor hell", [pt(SB, -1, 1), pt(SB, 1, 1), pt(S_END, 1, 1), pt(S_END, -1, 1)]),
                  ("Ceil hell", [pt(SB, -1, -1), pt(SB, 1, -1), pt(S_END, 1, -1), pt(S_END, -1, -1)]),
                  ("Wall L hell", [pt(SB, -1, -1), pt(SB, -1, 1), pt(S_END, -1, 1), pt(S_END, -1, -1)]),
                  ("Wall R hell", [pt(SB, 1, -1), pt(SB, 1, 1), pt(S_END, 1, 1), pt(S_END, 1, -1)])):
    d.path(quad(pts), name,
           fill={"gradient": {"kind": "linear",
                              "stops": [{"offset": 0, "color": "#A83412", "opacity": 0.02},
                                        {"offset": 1, "color": "#C8401A", "opacity": 0.42}],
                              "start": [VPX, VPY - HH * SB], "end": [VPX, VPY]}},
           stroke=NONE)

# wall seams: rails converging on the VP, left wall then right wall
for side, fx in (("L", -1), ("R", 1)):
    for j, fy in enumerate((-0.45, 0.35)):
        x0, y0 = pt(1, fx, fy)
        d.path(f"M{x0:.1f},{y0:.1f} L{VPX},{VPY}", f"Wall {side} seam {j+1}",
               fill=NONE, stroke="#1E7A3E", strokeWidth=3, opacity=42, cap="round")
# floor seams: centre line plus two panel joints
for j, fx in enumerate((-0.45, 0.0, 0.45)):
    x0, y0 = pt(1, fx, 1)
    d.path(f"M{x0:.1f},{y0:.1f} L{VPX},{VPY}", f"Floor seam {j+1}",
           fill=NONE, stroke="#1E7A3E", strokeWidth=3,
           opacity=38 if fx else 55, cap="round")
# corner edges: the four arrises of the corridor
for i, (fx, fy) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
    x0, y0 = pt(1, fx, fy)
    x1, y1 = pt(S_END, fx, fy)
    d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", f"Arris {i+1}",
           fill=NONE, stroke="#239A4E", strokeWidth=4, opacity=75, cap="round")

# frame ribs: rectangular portal frames shrinking to the vanishing point
RIB_W = {1.0: 6.5, 0.68: 5.5, 0.46: 4.5, 0.30: 4.0, 0.20: 3.5, 0.13: 3.0, 0.085: 3.0, 0.055: 3.0}
for i, s in enumerate(S):
    x0, y0 = pt(s, -1, -1)
    x1, y1 = pt(s, 1, 1)
    if abs(s - SB) < 1e-9:
        continue                          # boundary frame drawn separately, brighter
    d.path(quad([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]), f"Rib {i+1}",
           fill=NONE, stroke="#33D667", strokeWidth=RIB_W[s],
           opacity=88 - i * 6)
# innermost doorway: a hot dark opening at the corridor's end
dx0, dy0 = pt(S_END, -1, -1)
dx1, dy1 = pt(S_END, 1, 1)
d.path(quad([(dx0, dy0), (dx1, dy0), (dx1, dy1), (dx0, dy1)]), "Far door",
       fill=rad({"offset": 0, "color": "#3A1408"},
                 {"offset": 1, "color": "#120604"}),
       stroke="#C84818", strokeWidth=3)

# hell, suggested: jagged spires and embers crowding the far door
for i, (cx_, bw, h) in enumerate([(452, 26, 52), (474, 20, 66), (528, 22, 58),
                                  (552, 26, 44), (500, 30, 74)]):
    base = VPY + HH * S_END + 2
    d.path(f"M{cx_-bw/2},{base} L{cx_},{base-h} L{cx_+bw/2},{base} Z",
           f"Spire {i+1}", fill="#4A160B", opacity=78, stroke=NONE)
# ember glow swallowing the vanishing point
d.shape("ellipse", "VP glow", x=400, y=350, width=200, height=150,
        fill=rad({"offset": 0, "color": "#FF8A34", "opacity": 0.55},
                 {"offset": 0.5, "color": "#D8481A", "opacity": 0.28},
                 {"offset": 1, "color": "#D8481A", "opacity": 0}), stroke=NONE)
# stray embers drifting up out of the glow
for i, (x, y, w) in enumerate([(468, 396, 6), (512, 384, 5), (545, 402, 6),
                               (488, 366, 4), (522, 350, 5), (498, 330, 4)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFB050", opacity=60, stroke=NONE)

# --- the boundary line: GPL world ends, syscall ABI begins ---------------------
bx0, by0 = pt(SB, -1, -1)
bx1, by1 = pt(SB, 1, 1)
# energy curtain across the frame
d.path(quad([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)]), "Curtain",
       fill={"gradient": {"kind": "linear",
                          "stops": [{"offset": 0, "color": "#BFFFD0", "opacity": 0.05},
                                    {"offset": 1, "color": "#BFFFD0", "opacity": 0.17}],
                          "start": [VPX, by0], "end": [VPX, by1]}},
       stroke=NONE)
# curtain shimmer: three faint vertical streaks
for i, fx in enumerate((-0.5, 0.0, 0.5)):
    x = VPX + fx * HW * SB
    d.path(f"M{x:.1f},{by0+4} L{x:.1f},{by1-4}", f"Curtain streak {i+1}",
           fill=NONE, stroke="#D8FFE2", strokeWidth=3, opacity=18, cap="round")
# the boundary frame itself, drawn bright
d.path(quad([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)]), "Boundary frame",
       fill=NONE, stroke="#8FFFB0", strokeWidth=4.5, opacity=95)
# the boundary line proper: glowing sill across the floor
d.path(f"M{bx0-6},{by1} L{bx1+6},{by1}", "Boundary glow",
       fill=NONE, stroke="#BFFFD0", strokeWidth=13, opacity=22, cap="round")
d.path(f"M{bx0-6},{by1} L{bx1+6},{by1}", "Boundary line",
       fill=NONE, stroke="#E8FFE8", strokeWidth=4, opacity=95, cap="round")

# --- the heraldic shield on the boundary line ----------------------------------
SHW, SHT = 27, 66                       # shield half-width, height
sxt, syb = VPY - SHT, by1               # shield top, base point on the line
# ground shadow under the point
d.shape("ellipse", "Shield shadow", x=500 - 34, y=syb - 4, width=68, height=8,
        fill="#071009", opacity=45, stroke=NONE)
d.path(f"M{500-SHW},{sxt} L{500+SHW},{sxt} L{500+SHW},{sxt+38} "
       f"Q{500+SHW},{syb-6} 500,{syb} Q{500-SHW},{syb-6} {500-SHW},{sxt+38} Z",
       "Shield", fill=lin("#F2ECDC", "#9A8F70", (500, sxt), (500, syb)),
       stroke="#3C352A", strokeWidth=3.5)
# party per pale division
d.path(f"M500,{sxt+3} L500,{syb-3}", "Shield pale", fill=NONE,
       stroke="#6A6250", strokeWidth=2.5, opacity=55, cap="round")
# annulet charge, centred on the field
d.shape("ellipse", "Shield annulet", x=500 - 9, y=sxt + 21, width=18, height=18,
        fill=NONE, stroke="#5A5240", strokeWidth=3)
# rim light along the left flank
d.path(f"M{500-SHW+4},{sxt+4} L{500-SHW+4},{sxt+36} Q{500-SHW+4},{syb-10} 502,{syb-2}",
       "Shield sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=2.5,
       opacity=50, cap="round")

# phosphor dust on the near floor
for i, (x, y, w) in enumerate([(350, 660, 7), (640, 672, 6), (450, 620, 5),
                               (560, 640, 6), (300, 560, 5)]):
    assert on_disc(x, y, 10)
    d.shape("ellipse", f"Phosphor dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#7AE8A0", opacity=35, stroke=NONE)

# --- name + role ---------------------------------------------------------------
d.text("DOOM-ENGINE", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#DFF2DC", justify="center")
LINE2, SZ2, TRK = "DOOM ON BARE METAL", 23, 300
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C88050", justify="center")
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

d.finish("doom-engine-V1R00")
