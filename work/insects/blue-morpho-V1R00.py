#!/usr/bin/env python3
"""Blue morpho — field plate V1R00. Living Morpho helenor peleides in side
view, wings opening into an electric-blue sail over a small fallen fruit on
the forest floor. The far wing shows only a sliver of the brown eyespotted
underside where the angle permits. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; wingtips and antennae stay inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Blue Morpho — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241410"


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def F(p):
    return "%.1f,%.1f" % p


def cr(pts, closed=True):
    n = len(pts)
    s = "M" + F(pts[0])
    for i in range(n if closed else n - 1):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%s %s %s" % (F(c1), F(c2), F(p2))
    return s + (" Z" if closed else "")


def blob(cx, cy, rx, ry, n=10):
    return cr([(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n))
               for k in range(n)])


def lin(a, b, stops):
    return {"gradient": {"kind": "linear", "start": list(a), "end": list(b),
                         "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(stops):
    return {"gradient": {"kind": "radial",
                         "stops": [{"offset": o, "color": c} for o, c in stops]}}


BG_GRAD    = lin((0, 0), (0, 1000), [(0, "#181410"), (1, "#070503")])
PLATE_GRAD = rad([(0, "#7A8A5A"), (0.6, "#4E5E3C"), (1, "#23301E")])
FLOOR_GRAD = lin((0, 780), (0, 880), [(0, "#5E4E30"), (1, "#2A2010")])
FRUIT_GRAD = rad([(0, "#D8A048"), (0.55, "#A86828"), (1, "#5E3414")])
# the morpho blue: saturated centre, deep rim, electric sheen
BLUE_GRAD  = rad([(0, "#5EC0F0"), (0.4, "#2E8AE0"), (0.75, "#1660C0"), (1, "#0C3A80")])
BLUE_FAR   = rad([(0, "#2A60A8"), (1, "#123264")])
UNDER_GRAD = lin((380, 480), (560, 660), [(0, "#8A5E34"), (0.5, "#6A4224"), (1, "#3E2412")])

# --- backdrop + forest-floor plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#5E7040", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD,
        stroke="#1E2A16", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792, fill=NONE,
        stroke="#DCE8C4", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=200, y=200, width=230, height=120, fill="#BCC89A", opacity=15, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=560, width=220, height=110, fill="#BCC89A", opacity=13, stroke=NONE)
for i, (x, y, w) in enumerate([(185, 340, 6), (815, 305, 5), (155, 505, 6), (858, 475, 5),
                               (415, 102, 5), (605, 98, 6), (305, 152, 4), (705, 162, 5),
                               (245, 255, 4), (775, 235, 4), (135, 425, 4), (878, 565, 4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w, fill="#4A5A34",
            opacity=35, stroke=NONE)

# --- floor band closing on the disc arc ------------------------------------------------
gy = 798
gdx = math.sqrt(PR * PR - (gy - PCY) ** 2)
d.path(f"M{PCX-gdx:.1f},{gy} C330,792 420,802 500,800 C590,798 670,802 {PCX+gdx:.1f},{gy} "
       f"A{PR},{PR} 0 0 1 {PCX-gdx:.1f},{gy} Z",
       "Forest floor", fill=FLOOR_GRAD, opacity=92, stroke=NONE)
# litter strokes on the floor
for i, (x0, y0, x1, y1) in enumerate([(290,830,330,818),(660,838,700,826),(560,856,592,848),
                                      (380,852,408,844),(740,846,768,838)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)//2},{y0-16} {x1},{y1}", f"Litter {i+1}",
           fill=NONE, stroke="#7A6A42", strokeWidth=3, opacity=50, cap="round")

# --- the fallen fruit the butterfly works ------------------------------------------------
d.shape("ellipse", "Fruit shadow", x=400, y=802, width=220, height=18,
        fill="#140E04", opacity=45, stroke=NONE)
d.path(blob(500, 756, 92, 62), "Fallen fruit", fill=FRUIT_GRAD, stroke=INK, strokeWidth=4)
d.path("M470,698 C478,688 494,684 506,690 C500,700 486,704 470,698 Z",
       "Fruit stem scar", fill="#4A2E12", stroke=NONE)
d.shape("ellipse", "Fruit bruise", x=540, y=740, width=44, height=30,
        fill="#5E2E12", opacity=50, stroke=NONE)
d.shape("ellipse", "Fruit light", x=430, y=716, width=70, height=34,
        fill="#F0C878", opacity=35, stroke=NONE)

# --- far wing: brown eyespotted underside, a restrained sliver behind --------------------
# visible along the near wing's trailing/lower edge where the open V permits
FARW = [(452, 610), (400, 596), (346, 560), (310, 510), (306, 460),
        (330, 424), (372, 404), (420, 404), (452, 430)]
d.path(cr(FARW), "Far wing underside", fill=UNDER_GRAD, stroke=INK, strokeWidth=4)
# eyespot row on the visible underside sliver
for k, (ex, ey, s) in enumerate([(336, 508, 1.0), (352, 462, 0.85), (382, 428, 0.7)]):
    d.shape("ellipse", f"Underspot {k+1} ring", x=ex - 13*s, y=ey - 13*s,
            width=26*s, height=26*s, fill="#D8C49A", opacity=90, stroke=NONE)
    d.shape("ellipse", f"Underspot {k+1} dark", x=ex - 8*s, y=ey - 8*s,
            width=16*s, height=16*s, fill="#3A2410", stroke=NONE)
    d.shape("ellipse", f"Underspot {k+1} pupil", x=ex - 4*s, y=ey - 4*s,
            width=8*s, height=8*s, fill="#8A5E34", stroke=NONE)
# underside vein hints
for k, (x1, y1) in enumerate([(370, 540), (400, 570)]):
    d.path(f"M330,{y1-60} Q350,{y1-20} {x1},{y1}", f"Underside vein {k+1}",
           fill=NONE, stroke="#2E1C0C", strokeWidth=2.5, opacity=55, cap="round")

# --- near wing: the great blue sail, half-open ---------------------------------------------
# leading edge sweeps up-right from the thorax; trailing edge curves back down
NEARW = [(470, 606), (452, 540), (438, 460), (436, 384), (452, 320),
         (486, 272), (534, 244), (588, 236), (640, 248), (678, 280),
         (696, 326), (692, 384), (668, 442), (632, 496), (590, 540),
         (546, 572), (508, 592)]
for p in NEARW:
    assert on_disc(*p, 12), p
d.path(cr(NEARW), "Near wing", fill=BLUE_GRAD, stroke=NONE, opacity=96)

# black border band along the margin (inside the outline)
d.path(cr([(452, 540), (438, 460), (436, 384), (452, 320), (486, 272),
           (534, 244), (588, 236), (640, 248), (678, 280), (696, 326),
           (692, 384), (668, 442), (632, 496), (590, 540), (546, 572),
           (560, 546), (596, 512), (630, 458), (656, 402), (664, 344),
           (648, 300), (614, 274), (568, 264), (524, 280), (494, 316),
           (478, 376), (478, 452), (490, 522)]),
       "Wing border", fill="#14100C", opacity=92, stroke=NONE)
# re-lay the blue field so the border sits as a rim
d.path(cr([(478, 528), (468, 462), (468, 390), (482, 330), (512, 292),
           (556, 270), (604, 266), (642, 288), (660, 332), (650, 396),
           (624, 452), (588, 500), (548, 538), (512, 552)]),
       "Blue field", fill=BLUE_GRAD, stroke=NONE)
# iridescent sheen + scale shading
d.path(blob(560, 380, 80, 100), "Sheen", fill="#9AE0FF", opacity=22, stroke=NONE)
d.path(blob(530, 460, 60, 60), "Depth", fill="#0A2E6E", opacity=20, stroke=NONE)
# pale border spots of the morpho margin
for k, (sx, sy) in enumerate([(648, 268), (674, 300), (686, 344), (682, 396)]):
    d.shape("ellipse", f"Border spot {k+1}", x=sx - 5, y=sy - 5, width=10, height=10,
            fill="#E8E4D0", opacity=85, stroke=NONE)
# veins, subordinate to the colour
for k, (tx, ty) in enumerate([(560, 280), (620, 292), (652, 344), (640, 412), (600, 478), (552, 532)]):
    d.path(f"M480,560 Q{(480+tx)/2 + (ty-560)*0.04:.0f},{(560+ty)/2 - (tx-480)*0.04:.0f} {tx},{ty}",
           f"Wing vein {k+1}", fill=NONE, stroke="#0A2A5E", strokeWidth=3, opacity=55, cap="round")
# ink rim
d.path(cr(NEARW), "Near wing outline", fill=NONE, stroke=INK, strokeWidth=4)

# --- body over the fruit --------------------------------------------------------------------
d.path(cr([(452, 596), (462, 560), (468, 520), (474, 560), (478, 600), (470, 620)]),
       "Abdomen", fill="#3A2414", stroke=INK, strokeWidth=3)
for k, y in enumerate([570, 586, 600]):
    d.path(f"M458,{y} Q466,{y+4} 474,{y}", f"Abdomen band {k+1}", fill=NONE,
           stroke="#D8C8A8", strokeWidth=2.5, opacity=55, cap="round")
d.path(blob(464, 540, 20, 28), "Thorax",
       fill=rad([(0, "#5E3A20"), (1, "#281608")]), stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Thorax fuzz", x=448, y=516, width=22, height=18,
        fill="#8A6A40", opacity=45, stroke=NONE)
d.path(blob(458, 500, 13, 11), "Head", fill=rad([(0, "#4A2E18"), (1, "#1E1008")]),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye", x=448, y=496, width=9, height=11, fill="#0C0806", stroke=NONE)
d.shape("ellipse", "Eye glint", x=450, y=498, width=3, height=3, fill="#FFFFFF", opacity=85, stroke=NONE)

# clubbed antennae — a butterfly, not a moth
for sgn, (x1, y1, cx, cy) in enumerate([(430, 452, 444, 462), (442, 446, 452, 458)]):
    d.path(f"M458,494 Q{cx},{cy} {x1},{y1}", f"Antenna {sgn+1}", fill=NONE,
           stroke="#2E1C0C", strokeWidth=3.5, cap="round")
    d.shape("ellipse", f"Antenna club {sgn+1}", x=x1 - 4, y=y1 - 5, width=9, height=10,
            fill="#2E1C0C", stroke=NONE)

# legs standing on the fruit
for k, (x0, y0, x1, y1) in enumerate([(456, 570, 428, 700), (464, 580, 458, 706),
                                      (472, 576, 500, 698)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)//2 - 6},{(y0+y1)//2} {x1},{y1}", f"Leg {k+1}",
           fill=NONE, stroke="#2E1C0C", strokeWidth=3, opacity=85, cap="round")
# proboscis unrolled toward the fruit — the feeding morpho's tell
d.path("M456,506 C446,540 448,590 462,632 C468,652 470,676 468,700",
       "Proboscis", fill=NONE, stroke="#2E1C0C", strokeWidth=2.5, opacity=80, cap="round")

# --- captions --------------------------------------------------------------------------------
d.text("BLUE MORPHO", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4EED2", justify="center")
d.text("L E P I D O P T E R A", "Order", x=500, y=968, size=22, font="Virelai Sans",
       color="#AAC4A0", justify="center")

d.finish("blue-morpho-V1R00")
