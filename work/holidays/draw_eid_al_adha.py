#!/usr/bin/env python3
"""Eid al-Adha — Festival Seal V1R00.

Emblematic prayer-rug plate: a garnet rug with a gold diamond meander
border, a pointed mihrab niche in deep indigo with a small hanging lamp,
side columns and a fringe of tassels. A gold crescent rides above the rug.
Deep garnet-ink field, gold rim, vermilion chop with an eight-point star.
No human figures. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "eid-al-adha-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#3A1E24"
FIELD_LO = "#140A0C"
GARNET_HI = "#8A3440"
GARNET = "#6E2230"
GARNET_LO = "#3A1018"
NICHE = "#1C2044"
BRASS_HI = "#E8C074"
BRASS = "#B8842E"
BRASS_LO = "#6E4414"
AMBER = "#FFB45C"

p = Plate("Eid al-Adha — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def circle_path(cx, cy, r, sweep=1):
    return (f"M{cx - r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 1,{sweep} "
            f"{cx + r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 1,{sweep} "
            f"{cx - r:.1f},{cy:.1f} Z")


def crescent(cx, cy, r, bite=0.62, tilt=-38, label="Crescent"):
    a = math.radians(tilt)
    bx, by = cx + math.cos(a) * r * bite, cy + math.sin(a) * r * bite
    d.shape("ellipse", f"{label} halo", x=cx - r * 1.6, y=cy - r * 1.6,
            width=r * 3.2, height=r * 3.2,
            fill=rad((0, "#FFD98A", 20), (0.55, "#FFD98A", 6),
                     (1, "#FFD98A", 0)), stroke=NONE)
    d.path(circle_path(cx, cy, r) + " " +
           circle_path(bx, by, r * 0.86, sweep=0), label,
           fill=lin((cx - r, cy - r), (cx + r, cy + r),
                    (0, GOLD_HI), (0.5, GOLD), (1, GOLD_LO)),
           stroke=INK, strokeWidth=3)


def diamond(cx, cy, r, col, label, stroke=NONE, sw=0):
    d.path(f"M{cx:.1f},{cy - r:.1f} L{cx + r:.1f},{cy:.1f} "
           f"L{cx:.1f},{cy + r:.1f} L{cx - r:.1f},{cy:.1f} Z",
           label, fill=col, stroke=stroke, strokeWidth=sw)


def star8(cx, cy, r, col, label):
    """Eight-point star: two squares of the same tip radius, 45 deg apart."""
    k = r / math.sqrt(2)              # axis square half-side -> corners at r
    d.path(f"M{cx:.1f},{cy - r:.1f} L{cx + r:.1f},{cy:.1f} "
           f"L{cx:.1f},{cy + r:.1f} L{cx - r:.1f},{cy:.1f} Z",
           f"{label} a", fill=col, stroke=NONE)
    d.path(f"M{cx - k:.1f},{cy - k:.1f} L{cx + k:.1f},{cy - k:.1f} "
           f"L{cx + k:.1f},{cy + k:.1f} L{cx - k:.1f},{cy + k:.1f} Z",
           f"{label} b", fill=col, stroke=NONE)


def star4(x, y, r, col="#F2DFA8", op=85, label="Star"):
    q = r * 0.20
    d.path(f"M{x:.1f},{y - r:.1f} Q{x + q:.1f},{y - q:.1f} {x + r:.1f},{y:.1f} "
           f"Q{x + q:.1f},{y + q:.1f} {x:.1f},{y + r:.1f} "
           f"Q{x - q:.1f},{y + q:.1f} {x - r:.1f},{y:.1f} "
           f"Q{x - q:.1f},{y - q:.1f} {x:.1f},{y - r:.1f} Z",
           label, fill=col, opacity=op, stroke=NONE)


def niche(cx, apex, base, hw, label="Mihrab"):
    """Pointed-arch mihrab niche; returns the springline y."""
    sy = apex + hw * 0.92
    path = (f"M{cx - hw:.1f},{base:.1f} L{cx - hw:.1f},{sy:.1f} "
            f"C{cx - hw:.1f},{sy - hw*0.72:.1f} {cx - hw*0.46:.1f},{apex + 10:.1f} "
            f"{cx:.1f},{apex:.1f} "
            f"C{cx + hw*0.46:.1f},{apex + 10:.1f} {cx + hw:.1f},{sy - hw*0.72:.1f} "
            f"{cx + hw:.1f},{sy:.1f} L{cx + hw:.1f},{base:.1f} Z")
    return path, sy


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn gold 8-point star."""
    x, y = cx - s / 2, cy - s / 2
    inside(cx + s / 2, cy + s / 2, 8, "chop BR")
    d.shape("ellipse", "Chop shadow", x=x + 3, y=y + 5, width=s, height=s,
            fill=INK, opacity=28, stroke=NONE)
    d.shape("rectangle", "Chop", x=x, y=y, width=s, height=s, radius=5,
            fill=lin((x, y), (x + s, y + s), (0, "#C0473A"), (1, "#7E1F1B")),
            stroke="#4E100E", strokeWidth=2.2)
    d.shape("rectangle", "Chop inner", x=x + 4.5, y=y + 4.5, width=s - 9,
            height=s - 9, radius=2.5, fill=NONE, stroke="#F6D9A0",
            strokeWidth=1.4, opacity=78)
    star8(cx, cy, 13, "#FBE6B4", "Chop star")


# --- field ---------------------------------------------------------------------
p.backdrop(top="#241016", bottom="#0C0608", glow=("#5A2A30", 14))
dust(d, n=42, r=402, colors=("#F6E3B8", "#E8C8C0"), seed=47, smin=1.0,
     smax=2.4, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#5E3A16")
dust(d, n=52, r=392, colors=("#F6E3B8", "#E8C074"), seed=19, smin=1.0,
     smax=2.6, opmin=9, opmax=26, label="Disc dust")
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=30)
for rr, op in ((176, 11), (270, 9), (346, 7)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke=GOLD,
            strokeWidth=1.4, opacity=op)

# --- crescent above the rug ------------------------------------------------------
crescent(500, 226, 58, label="Crescent")

# --- the prayer rug ----------------------------------------------------------------
RX, RY, RW, RH = 352, 322, 296, 430
d.shape("ellipse", "Rug shadow", x=RX - 30, y=RY + RH - 6, width=RW + 60,
        height=40, fill=rad((0, INK, 34), (0.6, INK, 14), (1, INK, 0)),
        stroke=NONE)
# fringe tassels along the bottom edge
for i in range(15):
    x = RX + 8 + i * (RW - 16) / 14
    d.path(f"M{x:.1f},{RY + RH - 2:.1f} L{x:.1f},{RY + RH + 20:.1f}",
           f"Fringe {i+1}", fill=NONE,
           stroke=GOLD if i % 2 else "#F6D9A0", strokeWidth=3.4,
           opacity=88, cap="round")
# rug body
d.shape("rectangle", "Rug", x=RX, y=RY, width=RW, height=RH, radius=3,
        fill=lin((RX, RY), (RX + RW, RY + RH),
                 (0, GARNET_HI), (0.45, GARNET), (1, GARNET_LO)),
        stroke=INK, strokeWidth=3.4)
# double border bands
d.shape("rectangle", "Border outer", x=RX + 10, y=RY + 10, width=RW - 20,
        height=RH - 20, radius=2, fill=NONE, stroke=GOLD_LO,
        strokeWidth=2.2, opacity=95)
d.shape("rectangle", "Border inner", x=RX + 34, y=RY + 34, width=RW - 68,
        height=RH - 68, radius=2, fill=NONE, stroke=GOLD,
        strokeWidth=1.8, opacity=85)
# diamond meander in the border band
bx0, by0, bw, bh = RX + 22, RY + 22, RW - 44, RH - 44
step = 30
pos = []
nx = int(bw / step)
for i in range(1, nx):
    pos.append((bx0 + i * bw / nx, by0))
    pos.append((bx0 + i * bw / nx, by0 + bh))
ny = int(bh / step)
for i in range(1, ny):
    pos.append((bx0, by0 + i * bh / ny))
    pos.append((bx0 + bw, by0 + i * bh / ny))
for i, (dx, dy) in enumerate(pos):
    diamond(dx, dy, 7, GOLD if i % 3 else "#F6D9A0", f"Meander {i+1}")

# --- mihrab niche -------------------------------------------------------------------
NICHE_HW = 78
nband, _ = niche(500, 412, 706, NICHE_HW + 14, "Mihrab band")
d.path(nband, "Mihrab band", fill=gold_lin(390, 706), stroke=INK,
       strokeWidth=2.6)
npath, nsy = niche(500, 424, 706, NICHE_HW, "Mihrab")
d.path(npath, "Mihrab niche",
       fill=lin((500, 424), (500, 706), (0, "#2A2E5E"), (0.6, NICHE),
                (1, "#12142E")), stroke=INK, strokeWidth=2.2)
# inner arch bead line
inpath, _ = niche(500, 442, 706, NICHE_HW - 14, "Mihrab inner")
d.path(inpath, "Mihrab bead", fill=NONE, stroke="#F6D9A0", strokeWidth=1.8,
       opacity=66)
# side columns just inside the inner border
for i, sx in enumerate((-1, 1)):
    colx = 500 + sx * 98
    d.shape("rectangle", f"Column {i+1}", x=colx - 7, y=nsy + 4, width=14,
            height=706 - nsy - 4, fill=gold_lin(nsy, 706), stroke=INK,
            strokeWidth=1.8)
    d.shape("rectangle", f"Column {i+1} cap", x=colx - 11, y=nsy - 8,
            width=22, height=12, radius=3, fill=BRASS_HI, stroke=INK,
            strokeWidth=1.6)
    d.shape("rectangle", f"Column {i+1} foot", x=colx - 11, y=694, width=22,
            height=12, radius=3, fill=BRASS, stroke=INK, strokeWidth=1.6)

# hanging lamp inside the niche, chain from the apex
for i, y in enumerate(range(452, 546, 14)):
    d.shape("ellipse", f"Lamp chain {i+1}", x=497.8, y=y - 2.6, width=4.4,
            height=4.4, fill=NONE, stroke=BRASS_HI, strokeWidth=1.6,
            opacity=90)
d.shape("ellipse", "Lamp aura", x=500 - 52, y=548 - 40, width=104,
        height=116, fill=rad((0, AMBER, 34), (0.55, AMBER, 10),
                             (1, AMBER, 0)), stroke=NONE)
d.path("M488,552 Q488,540 500,540 Q512,540 512,552 L514,552 "
       "C514,576 508,592 500,596 C492,592 486,576 486,552 Z",
       "Lamp body", fill=lin((486, 540), (514, 596),
                             (0, "#FFE2A8"), (0.55, AMBER), (1, "#C25E1E")),
       stroke=INK, strokeWidth=2.2)
d.shape("ellipse", "Lamp lip", x=486, y=548, width=28, height=9,
        fill=gold_lin(548, 557), stroke=INK, strokeWidth=1.6)
d.path("M500,596 C497,604 497,610 500,614 C503,610 503,604 500,596 Z",
       "Lamp drop", fill=BRASS_HI, stroke=INK, strokeWidth=1.2)
# star motif at the niche base
star8(500, 652, 15, "#F6D9A0", "Niche star")
diamond(452, 652, 8, GOLD, "Niche dot L")
diamond(548, 652, 8, GOLD, "Niche dot R")

# small motifs in the field above the arch
star8(500, 376, 11, "#F6D9A0", "Rug crest")
diamond(466, 378, 7, GOLD, "Rug crest L", stroke=INK, sw=1.0)
diamond(534, 378, 7, GOLD, "Rug crest R", stroke=INK, sw=1.0)

# flanking sparkles balancing the empty mid-field
for i, (x, y, r) in enumerate([(268, 430, 11), (732, 430, 11),
                               (232, 570, 8), (768, 570, 8),
                               (316, 232, 9), (684, 150, 8)]):
    star4(x, y, r, label=f"Field star {i+1}")

# --- seal + caption -----------------------------------------------------------------
seal_chop()
caption(p, "EID AL-ADHA", "10 DHU AL-HIJJAH · THE GREATER EID",
        name_color="#F4EBD4", sub_color="#C9A46A",
        name_size=52, tracking_name=72, sub_size=20, tracking_sub=40,
        sub_font=SERIF)
p.finish(SLUG)
