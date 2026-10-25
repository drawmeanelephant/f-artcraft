#!/usr/bin/env python3
"""Marine iguana — field plate V1R00. Amblyrhynchus cristatus hauled out
on a dark volcanic ledge after the swim: low-slung three-quarter body,
blunt salt-crusted snout, the ragged dorsal crest marching down the
neck, stout splayed feet gripping basalt, and the laterally flattened
tail running long behind inside the rim. Galápagos lava-coast plate,
night-surf mood — charcoal disc, turquoise reflected light off the
waterline under the ledge. 1000x1000. House style: gradients +
translucent shading, never flat fills. Plate = circle center (500,460)
r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Marine Iguana — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#14161C"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0A0E16"), (1, "#040608"))
PLATE_GRAD = rad((0, "#52565C"), (0.5, "#2E3238"), (1, "#101418"))
BASALT   = lin(0, 720, 0, 880, (0, "#3E3E46"), (0.5, "#282830"), (1, "#141419"))
SCALE    = rad((0, "#767A70"), (0.55, "#4E5048"), (1, "#2C2C28"))
BELLY_GR = rad((0, "#8A8C7E"), (1, "#565448"))

# --- backdrop + night-lava plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,115,4),(852,120,5),(115,448,3),(872,500,4),
                               (176,735,4),(856,755,4),(264,150,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D2D8", opacity=26, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#52565C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C2026", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCD6DC", strokeWidth=3, opacity=34)

# cold moon-sheen high in the plate
d.shape("ellipse", "Moon sheen", x=330, y=210, width=400, height=280,
        fill=rad((0, "#B8C8D4", 26), (0.6, "#B8C8D4", 8), (1, "#B8C8D4", 0)),
        stroke=NONE)
# patina flecks
for i, (x, y, w) in enumerate([(308,178,4),(452,142,5),(592,170,4),(226,268,3),
                               (370,220,4),(522,194,3),(690,150,4),(250,418,3),
                               (750,430,4),(208,558,3)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D4DCD8", opacity=40, stroke=NONE)

# --- surf glow: turquoise reflected light washing under the ledge --------------------
sy = 838
sl, sr = disc_x(sy, -1), disc_x(sy, 1)
d.path(f"M{sl:.1f},{sy} L{sr:.1f},{sy} A{R},{R} 0 0 1 {sl:.1f},{sy} Z",
       "Surf wash", fill=rad((0, "#2EB8AE", 34), (0.7, "#2EB8AE", 12),
       (1, "#2EB8AE", 0)), stroke=NONE)
d.path(f"M{sl+8:.1f},{sy} L{sr-8:.1f},{sy}", "Surf line", fill=NONE,
       stroke="#5ED8CE", strokeWidth=4, opacity=45, cap="round")

# --- the volcanic ledge: basalt slab closing on the disc arc -------------------------
ly = 770
ll, lr = disc_x(ly, -1), disc_x(ly, 1)
d.path(f"M{ll:.1f},{ly} L240,752 L400,764 L560,750 L720,766 L{lr:.1f},{ly} "
       f"A{R},{R} 0 0 1 {sl+8:.1f},{sy} L{sl:.1f},{sy} "
       f"A{R},{R} 0 0 1 {ll:.1f},{ly} Z",
       "Ledge", fill=BASALT, stroke=NONE)
# wet sheen on the ledge lip where the surf glow catches
d.path(f"M{ll+6:.1f},{ly} L240,752 L400,764 L560,750 L720,766 L{lr-6:.1f},{ly}",
       "Ledge sheen", fill=NONE, stroke="#58C4BC", strokeWidth=4,
       opacity=38, cap="round")
# basalt vesicles and cracks
for i, (x, y, w) in enumerate([(300,800,14),(380,824,10),(520,806,12),(640,830,9),
                               (720,800,11),(450,846,8)]):
    assert on_disc(x, y, 8), (x, y)
    d.shape("ellipse", f"Vesicle {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#101014", opacity=70, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(340, 788, 318, 822), (600, 782, 620, 816)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Ledge crack {i+1}", fill=NONE,
           stroke="#101014", strokeWidth=3, opacity=60, cap="round")

# contact shadow under the sprawled body
d.shape("ellipse", "Body shadow", x=330, y=740, width=340, height=36,
        fill="#06060A", opacity=50, stroke=NONE)

# === the tail: laterally flattened, running long behind on the ledge =================
# base buried under the rump so it reads as one animal; tip curls up inside the rim
d.path("M614,700 "
       "C676,696 724,712 750,738 "                   # upper edge easing to the tip
       "C760,750 762,758 754,763 "                   # tip kicking up a touch
       "C740,772 710,772 684,766 "                   # tip underside
       "C658,760 640,758 628,754 "                   # lower edge into the belly
       "C622,738 620,718 614,700 Z",
       "Tail", fill=lin(620, 690, 760, 780, (0, "#5A5C54"), (0.6, "#3C3E38"),
       (1, "#24241F")), stroke=INK, strokeWidth=5)
# crest continues down the tail top, shrinking to the tip
for i, (tx, ty, s) in enumerate([(648, 700, 0.85), (680, 708, 0.75),
                                 (710, 722, 0.65), (736, 740, 0.5)]):
    d.path(f"M{tx - 10*s},{ty} L{tx},{ty - 18*s} L{tx + 10*s},{ty + 2} Z",
           f"Tail spike {i+1}", fill="#8E8A78", stroke=INK, strokeWidth=3)
# lateral flattening: a midline crease and two soft diagonal wrinkles
d.path("M636,724 C676,720 716,730 748,750", "Tail crease", fill=NONE,
       stroke="#1E1E1A", strokeWidth=3, opacity=50, cap="round")
for i, (bx, by) in enumerate([(664, 714), (700, 726)]):
    d.path(f"M{bx},{by} q-8,18 -12,34", f"Tail wrinkle {i+1}", fill=NONE,
           stroke="#1E1E1A", strokeWidth=3, opacity=40, cap="round")
# turquoise bounce light along the tail's underside
d.path("M640,756 C676,764 716,770 748,762", "Tail bounce", fill=NONE,
       stroke="#58C4BC", strokeWidth=4, opacity=30, cap="round")

# === the body: low-slung barrel sprawled on the basalt ===============================
d.path("M378,640 "                                   # neck top behind the head
       "C440,622 520,624 578,648 "                   # back line sloping up-right
       "C622,664 644,688 650,714 "                   # rump into the tail
       "C646,740 624,758 592,764 "                   # belly rear
       "C520,772 440,772 400,756 "                   # belly line, low on rock
       "C372,744 360,720 362,696 "                   # chest front
       "C364,672 368,654 378,640 Z",
       "Body", fill=SCALE, stroke=INK, strokeWidth=6)
# belly wash and the turquoise bounce under it
d.path("M400,720 C440,744 520,756 580,750 C540,764 460,764 410,748 "
       "C396,742 394,730 400,720 Z", "Belly wash", fill=BELLY_GR,
       opacity=55, stroke=NONE)
d.path("M404,756 C470,768 540,768 596,756", "Surf bounce", fill=NONE,
       stroke="#58C4BC", strokeWidth=5, opacity=28, cap="round")
# flank scale shading: loose vertical wrinkles behind the foreleg
for i, wx in enumerate([430, 458, 486, 514]):
    d.path(f"M{wx},660 q-10,36 -4,72", f"Flank fold {i+1}", fill=NONE,
           stroke="#2A2A26", strokeWidth=3, opacity=45, cap="round")
# pale dorsal flecking — dried salt and scale highlights, sparing
for i, (x, y) in enumerate([(430, 648), (472, 640), (516, 644), (556, 656),
                            (404, 676), (470, 672), (534, 678)]):
    d.shape("ellipse", f"Salt fleck {i+1}", x=x, y=y, width=7, height=4,
            fill="#C8C6B4", opacity=55, stroke=NONE)

# === dorsal crest: ragged spines marching from the nape down the back ================
for i, (bx, by, s) in enumerate([(382, 638, 1.05), (414, 630, 1.15),
                                 (448, 626, 1.2), (484, 626, 1.15),
                                 (520, 632, 1.05), (554, 642, 0.95),
                                 (586, 654, 0.85), (614, 668, 0.7)]):
    d.path(f"M{bx - 11*s},{by} L{bx},{by - 26*s} L{bx + 11*s},{by + 2} Z",
           f"Crest spine {i+1}", fill=lin(0, by - 26*s, 0, by,
           (0, "#9A947E"), (1, "#4E4A3E")), stroke=INK, strokeWidth=3)

# === legs: stout, splayed, long-clawed feet gripping the rock ========================
# far-side legs first (darker, tucked behind the body line)
for i, (kx, ky) in enumerate([(430, 730), (560, 738)]):
    d.path(f"M{kx},{ky} C{kx-14},{ky+6} {kx-20},{ky+20} {kx-16},{ky+32} "
           f"C{kx-8},{ky+40} {kx+8},{ky+40} {kx+14},{ky+30} "
           f"C{kx+18},{ky+18} {kx+12},{ky+6} {kx},{ky} Z",
           f"Far leg {i+1}", fill="#33332E", stroke=INK, strokeWidth=3.5)
# near foreleg: shoulder down to a spread hand of clawed toes
d.path("M404,668 C392,690 386,714 388,738 C390,754 400,764 414,764 "
       "C428,764 436,752 436,736 C436,712 432,690 424,672 "
       "C418,662 410,660 404,668 Z",
       "Foreleg", fill=lin(390, 668, 430, 764, (0, "#5C5E56"), (1, "#33332E")),
       stroke=INK, strokeWidth=4)
for k in range(4):                                   # toes + claws
    tx = 384 + k * 16
    d.path(f"M{tx},{766} C{tx-4},{774} {tx-6},{782} {tx-2},{790}",
           f"Fore toe {k+1}", fill=NONE, stroke="#3C3A30", strokeWidth=4,
           cap="round")
    d.path(f"M{tx-2},{790} L{tx-8},{800}", f"Fore claw {k+1}", fill=NONE,
           stroke="#1C1810", strokeWidth=3.5, cap="round")
# near hind leg: heavy thigh folded, foot forward with long toes
d.path("M566,700 C588,692 612,696 624,714 C634,730 632,750 620,762 "
       "C604,772 580,772 566,760 C552,748 550,724 556,708 Z",
       "Thigh", fill=lin(560, 696, 620, 770, (0, "#585A52"), (1, "#30302C")),
       stroke=INK, strokeWidth=4)
for k in range(4):                                   # toes + claws
    tx = 574 + k * 17
    d.path(f"M{tx},{768} C{tx-4},{776} {tx-6},{784} {tx-2},{792}",
           f"Hind toe {k+1}", fill=NONE, stroke="#3C3A30", strokeWidth=4,
           cap="round")
    d.path(f"M{tx-2},{792} L{tx-8},{802}", f"Hind claw {k+1}", fill=NONE,
           stroke="#1C1810", strokeWidth=3.5, cap="round")

# === head: blunt snout, salt crust on the crown, facing left =========================
d.path("M368,606 "                                   # crown behind the crest
       "C340,600 314,606 298,624 "                   # sloping forehead
       "C282,640 276,660 282,678 "                   # blunt squared snout front
       "C286,694 300,704 318,706 "                   # jaw/chin
       "C344,710 372,706 390,694 "                   # throat back to the neck
       "C402,684 406,668 404,652 "                   # back of jaw
       "C400,630 388,612 368,606 Z",
       "Head", fill=rad((0, "#7A7E72"), (0.55, "#525448"), (1, "#32322C")),
       stroke=INK, strokeWidth=5)
# blunt muzzle front plane
d.path("M282,646 C276,660 280,678 292,688 C304,696 320,698 332,694 "
       "C322,682 318,664 322,648 C310,640 292,640 282,646 Z",
       "Muzzle front", fill="#6A6E62", opacity=75, stroke=NONE)
# salt crust on the crown — the white cap that gives the species its look
d.path("M300,614 C316,604 344,602 366,610 C374,614 378,620 376,626 "
       "C360,620 340,620 324,624 C314,626 306,624 300,614 Z",
       "Salt crust", fill="#D8D6C4", opacity=90, stroke=NONE)
# nostril and sneeze-speck below the snout
d.shape("ellipse", "Nostril", x=290, y=650, width=9, height=6,
        fill="#1C1C18", stroke=NONE)
for i, (x, y) in enumerate([(286, 662), (294, 672), (288, 680)]):
    d.shape("ellipse", f"Salt speck {i+1}", x=x, y=y, width=4, height=3,
            fill="#D8D6C4", opacity=70, stroke=NONE)
# the eye: high-set, dark with a pale lid arc
d.shape("ellipse", "Eye", x=334, y=634, width=24, height=22,
        fill="#16160F", stroke=NONE)
d.path("M334,636 C342,628 354,628 360,636", "Lid arc", fill=NONE,
       stroke="#8E8A76", strokeWidth=3, opacity=80, cap="round")
d.shape("ellipse", "Glint", x=342, y=639, width=6, height=6,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# mouth line back under the jaw
d.path("M288,682 C312,690 340,692 366,686", "Mouth", fill=NONE,
       stroke="#22221C", strokeWidth=3, opacity=80, cap="round")
# dewlap fold under the throat
d.path("M336,706 C356,716 384,716 402,704", "Dewlap", fill=NONE,
       stroke="#2C2C26", strokeWidth=4, opacity=70, cap="round")
# cool rim light along the back
d.path("M392,640 C460,624 540,630 596,656", "Back rim", fill=NONE,
       stroke="#A8B8BC", strokeWidth=5, opacity=28, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C1014", strokeWidth=6)

# --- captions -----------------------------------------------------------------------
r1 = d.text("MARINE IGUANA", "Name", x=500, y=930, size=58,
            font="Virelai Sans", color="#CCD6DC", justify="center")
r2 = d.text("AMBLYRHYNCHUS CRISTATUS", "Second line", x=500, y=968, size=22,
            font="Virelai Sans", color="#8FA4A8", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r2["id"], tracking=260)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for r, lab, wmax in [(r1, "name", 800), (r2, "line2", 760)]:
    b = find(layers, r["id"])["bounds"]
    print(lab, "bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= wmax and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("marine-iguana-V1R00")
