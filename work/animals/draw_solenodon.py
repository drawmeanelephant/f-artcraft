#!/usr/bin/env python3
"""Solenodon — field plate V1R00. Full-body profile facing left, head low:
the venomous shrew out of the dinosaur era, all long mobile snout and
low-slung body — flexible rostrum sniffing the leaf litter, tiny eye,
half-buried ear, digging foreclaws, long naked scaly tail trailing right.
Umber coat on a leaf-litter plate. 1000x1000. House style: gradients +
translucent shading, never flat fills.
Plate = circle center (500,460) r420; snout tip, tail tip and leaves stay
inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Solenodon — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#2E1C10"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def smooth(pts, closed=True, k=1.0):
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

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

def qpt(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#1C1610"), (1, "#080604"))
PLATE_GRAD = rad((0, "#D8CBA0"), (0.6, "#A2946A"), (1, "#5E5438"))
COAT_GRAD  = rad((0, "#96684A"), (0.58, "#6E4630"), (1, "#42281A"))
BELLY_GRAD = lin(0, 640, 0, 730, (0, "#5C3A26"), (1, "#38200F"))
SNOUT_GRAD = lin(300, 620, 190, 690, (0, "#8A5C40"), (0.7, "#A87B58"), (1, "#C09070"))
TAIL_GRAD  = lin(660, 620, 830, 690, (0, "#8A6E50"), (1, "#B09472"))
LEG_GRAD   = lin(0, 680, 0, 780, (0, "#5E3C26"), (1, "#3A2212"))
LEG_FAR    = lin(0, 680, 0, 780, (0, "#3E2818"), (1, "#281708"))
LITTER_GRAD = lin(0, 760, 0, 880, (0, "#7A643C"), (1, "#463719"))
CLAW = "#EADFC4"

# --- backdrop + leaf-litter plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#8A7448", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E4228", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFE6C8", strokeWidth=3, opacity=45)
d.shape("ellipse", "Patina 1", x=200, y=170, width=240, height=130, fill="#C4B586", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=560, width=230, height=120, fill="#C4B586", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(210,330,7),(790,280,8),(160,470,8),(840,470,7),(250,700,7),(760,720,8),
                               (150,590,6),(860,580,6),(400,110,7),(610,120,6),(330,820,6),(690,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5F3E", opacity=38, stroke=NONE)
# soft canopy light high on the disc + a few leaves drifting down
for i, (x, y, w) in enumerate([(330,210,24),(480,170,18),(620,220,20)]):
    d.shape("ellipse", f"Canopy light {i+1}", x=x, y=y, width=w, height=w,
            fill="#F2EAD0", opacity=15, stroke=NONE)

def leaf(x, y, L, deg, fill, label, opacity=90):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    def rot(px, py):
        return (x + px * c - py * s, y + px * s + py * c)
    p = [rot(-L / 2, 0), rot(0, -L * 0.22), rot(L / 2, 0), rot(0, L * 0.22)]
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z"
           % (p[0] + p[1] + p[2] + p[3] + p[0]), label,
           fill=fill, stroke=NONE, opacity=opacity)

for i, (x, y, L, a) in enumerate([(268,300,40,-30),(740,340,44,22),(560,168,34,-12)]):
    leaf(x, y, L, a, "#8A7448", f"Falling leaf {i+1}", opacity=28)

# --- leaf-litter floor, closing on the disc's own arc -----------------------------
gy = 780
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C340,772 430,784 500,780 C580,776 660,784 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Leaf litter", fill=LITTER_GRAD, opacity=88, stroke=NONE)

def leaf_ink(x, y, L, deg, fill, label):
    leaf(x, y, L, deg, fill, label, 90)
    # stroked overlay for the litter leaves only
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    def rot(px, py):
        return (x + px * c - py * s, y + px * s + py * c)
    p = [rot(-L / 2, 0), rot(0, -L * 0.22), rot(L / 2, 0), rot(0, L * 0.22)]
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z"
           % (p[0] + p[1] + p[2] + p[3] + p[0]), label + " edge",
           fill=NONE, stroke=INK, strokeWidth=1.5, opacity=90)

for i, (x, y, L, a, f) in enumerate([(238,796,46,-24,"#A8622E"),(300,812,40,14,"#8A4A26"),
                                     (700,804,50,30,"#B07038"),(790,792,38,-18,"#7A4620"),
                                     (560,818,34,8,"#96632F")]):
    leaf_ink(x, y, L, a, f, f"Leaf {i+1}")

# shadow under the body
d.shape("ellipse", "Body shadow", x=290, y=758, width=430, height=26,
        fill="#241806", opacity=38, stroke=NONE)

# --- tail: long, naked, faintly ringed — drawn first, sits behind the rump ---------
tail = "M650,606 C716,616 780,642 824,678 C832,685 836,692 838,698"
d.path(tail, "Tail", fill=NONE, stroke=TAIL_GRAD, strokeWidth=15, cap="round")
d.path(tail, "Tail core", fill=NONE, stroke="#5E462E", strokeWidth=6, cap="round", opacity=55)
for i, t in enumerate([0.22, 0.38, 0.54, 0.7, 0.85]):
    x, y = qpt((650, 606), (780, 642), (838, 698), t)
    d.path(f"M{x-4:.0f},{y-9:.0f} L{x+4:.0f},{y+9:.0f}", f"Tail ring {i+1}",
           fill=NONE, stroke="#4A3420", strokeWidth=2.5, opacity=50, cap="round")

# --- far legs (darker, behind body, offset to peek) --------------------------------
d.path(smooth([(404,692),(398,728),(394,764),(408,772),(422,764),(420,728),(422,694)]),
       "Foreleg far", fill=LEG_FAR, stroke=NONE)
d.path(smooth([(610,688),(606,726),(604,762),(618,770),(632,762),(630,726),(628,690)]),
       "Hindleg far", fill=LEG_FAR, stroke=NONE)

# --- body + head + snout, one silhouette ---------------------------------------------
body_pts = [(180,674),   # snout tip
            (238,646),   # snout top
            (292,606),   # nose bridge
            (334,584),   # crown
            (400,560),   # behind ear
            (470,550),   # shoulder hump
            (560,554),   # mid back
            (636,572),   # rump
            (676,600),   # tail base top
            (684,646),   # rear
            (656,692),   # rear lower
            (580,712),   # belly back
            (470,718),   # belly
            (372,706),   # chest
            (300,688),   # throat
            (226,684),   # snout underside
            ]
d.path(smooth(body_pts), "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# belly shade + back rim light + snout shading
d.path("M340,700 C430,716 560,714 640,688 C580,726 430,730 340,700 Z",
       "Belly shade", fill=BELLY_GRAD, opacity=50, stroke=NONE)
d.path("M336,586 C420,552 560,550 660,584", "Back rim", fill=NONE,
       stroke="#D8B88E", strokeWidth=7, opacity=45, cap="round")
d.path("M210,682 C240,662 276,638 310,616 C282,646 244,676 214,690 Z",
       "Snout sheen", fill="#D8AE8C", opacity=45, stroke=NONE)
d.shape("ellipse", "Shoulder glow", x=420, y=570, width=180, height=80,
        fill="#C08A60", opacity=18, stroke=NONE)
# coarse fur ticks along the back and flank
for i, (x, y, dx, dy) in enumerate([(360,584,-8,-14),(420,564,-6,-15),(480,558,-4,-15),
                                    (540,558,0,-15),(600,566,4,-14),(646,584,8,-12),
                                    (400,640,-6,12),(470,650,-4,14),(540,650,0,13)]):
    d.path(f"M{x},{y} l{dx},{dy}", f"Fur tick {i+1}", fill=NONE,
           stroke="#3A2210", strokeWidth=3, opacity=35, cap="round")

# --- near legs over the belly edge ----------------------------------------------------
d.path(smooth([(366,684),(358,724),(354,766),(372,774),(388,766),(384,724),(386,686)]),
       "Foreleg near", fill=LEG_GRAD, stroke=INK, strokeWidth=4)
d.path(smooth([(560,680),(552,722),(548,764),(566,772),(582,764),(578,722),(580,682)]),
       "Hindleg near", fill=LEG_GRAD, stroke=INK, strokeWidth=4)
# digging claws — front feet long and pale, rear feet shorter
for j, (fx, fy, L) in enumerate([(354,766,26),(394,764,22),(548,764,16),(604,762,14)]):
    for k, a in enumerate([-16, -4, 8]):
        t = math.radians(a - 90)
        cx2 = fx + 14 + k * 9
        tipx, tipy = cx2 + math.cos(t) * L, fy + 8 + math.sin(t) * L
        d.path(f"M{cx2-3:.0f},{fy+2:.0f} L{tipx:.0f},{tipy:.0f} L{cx2+4:.0f},{fy+4:.0f} Z",
               f"Claw {j+1}.{k+1}", fill=CLAW,
               stroke="#6E5638", strokeWidth=1.5)

# --- head detail ----------------------------------------------------------------------
# ear: small, rounded, half sunk in the crown fur
d.path("M358,566 C350,548 358,530 377,530 C395,530 402,548 395,563 C384,556 370,556 358,566 Z",
       "Ear", fill=rad((0, "#7A4E32"), (1, "#4E2E1C")), stroke=INK, strokeWidth=4)
d.path("M367,556 C365,546 371,538 380,538 C388,538 392,546 390,553",
       "Ear inner", fill=NONE, stroke="#B08060", strokeWidth=3, opacity=70, cap="round")
# eye: small bead, well above the snout line
d.shape("ellipse", "Eye", x=336, y=598, width=17, height=20, fill="#1E1208", stroke=NONE)
d.shape("ellipse", "Eye glint", x=340, y=602, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
# nostril + snout tip crease + whisker dots
d.shape("ellipse", "Nostril", x=176, y=670, width=8, height=10, fill="#26160C", stroke=NONE)
d.path("M192,682 C198,678 202,674 204,668", "Snout crease", fill=NONE,
       stroke="#4E2E1C", strokeWidth=3, opacity=60, cap="round")
for i, (x, y) in enumerate([(226,664),(238,670),(234,656),(250,664)]):
    d.shape("ellipse", f"Whisker dot {i+1}", x=x, y=y, width=4, height=4,
            fill="#3A2414", opacity=60, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(226,664,184,646),(238,670,192,656),(234,656,190,638)]):
    d.path(f"M{x0},{y0} C{x0-16},{y0-4} {x1+16},{y1+4} {x1},{y1}", f"Whisker {i+1}",
           fill=NONE, stroke="#E8DCC0", strokeWidth=1.8, opacity=55, cap="round")
# scent wisp at the snout tip — the snout is working
d.path("M152,688 C140,682 136,672 142,662", "Scent wisp 1", fill=NONE,
       stroke="#D8CBA0", strokeWidth=3, opacity=45, cap="round")
d.path("M136,698 C122,692 118,680 126,670", "Scent wisp 2", fill=NONE,
       stroke="#D8CBA0", strokeWidth=2.5, opacity=35, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3E341E", strokeWidth=6)

# --- name ------------------------------------------------------------------------------
d.text("SOLENODON", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#E4D6AE", justify="center")
LINE2, SZ2, TRK = "SOLENODON PARADOXUS", 21, 280
r = d.text(LINE2, "Second line", x=500, y=973, size=SZ2, font="Virelai Sans",
           color="#B49E72", justify="center")
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

d.finish("solenodon-V1R00")
