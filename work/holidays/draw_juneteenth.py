#!/usr/bin/env python3
"""Juneteenth — Festival Seal V1R00.

Freedom Day: a single gold star over a fan of red and cream burst wedges on
a deep green field, and a bronze chain arcing along the lower rim — broken
at its centre link, the snapped halves splayed, three shards still flying.
Objects and geometry only. Vermilion chop with a drawn star. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "juneteenth-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#173F2A"
FIELD_LO = "#071A10"
BURST_RED = "#C0372B"
BURST_CREAM = "#F6E3B8"
LINK_HI = "#F2C66E"
LINK = "#C8963E"
LINK_LO = "#7A5A1E"

p = Plate("Juneteenth — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def star5(cx, cy, R, label, rot=-90):
    """Five-point star, outer radius R. Returns path d."""
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36)
        r = R if i % 2 == 0 else R * 0.40
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return ("M%.1f,%.1f " % pts[0]
            + " ".join("L%.1f,%.1f" % q for q in pts[1:]) + " Z"), pts


def burst_wedge(cx, cy, a_deg, r0, r1, half_deg, col, op, label):
    """One tapered wedge ray of the dawn burst behind the star."""
    a = math.radians(a_deg)
    da = math.radians(half_deg)
    x0, y0 = cx + r0 * math.cos(a - da * 0.35), cy + r0 * math.sin(a - da * 0.35)
    x1, y1 = cx + r1 * math.cos(a - da), cy + r1 * math.sin(a - da)
    x2, y2 = cx + r1 * math.cos(a + da), cy + r1 * math.sin(a + da)
    x3, y3 = cx + r0 * math.cos(a + da * 0.35), cy + r0 * math.sin(a + da * 0.35)
    inside(x1, y1, 6, f"{label} tip")
    inside(x2, y2, 6, f"{label} tip")
    d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f} "
           f"Q{cx + r1*1.04*math.cos(a):.1f},{cy + r1*1.04*math.sin(a):.1f} "
           f"{x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} Z",
           label, fill=col, opacity=op, stroke=NONE)


def link(cx, cy, ang, label, w=34, h=20, sw=7.5):
    """One chain link: rotated ellipse outline, warm bronze, inner glint."""
    d.shape("ellipse", label, x=cx - w / 2, y=cy - h / 2, width=w, height=h,
            fill=NONE, stroke=INK, strokeWidth=sw + 3, opacity=90,
            rotation=round(ang, 1))
    d.shape("ellipse", f"{label} metal", x=cx - w / 2, y=cy - h / 2, width=w,
            height=h, fill=NONE, stroke=LINK, strokeWidth=sw,
            rotation=round(ang, 1))
    d.path(f"M{cx - w*0.28:.1f},{cy - h*0.30:.1f} "
           f"Q{cx:.1f},{cy - h*0.55:.1f} {cx + w*0.28:.1f},{cy - h*0.30:.1f}",
           f"{label} glint", fill=NONE, stroke=LINK_HI, strokeWidth=1.8,
           opacity=75, cap="round")


def broken_link(cx, cy, ang, side, label, w=34, h=20, sw=7.5):
    """Half a snapped link: a C-arc opening away from the break."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    # link-local frame: u along the link, v across
    ux, uy = ca, sa
    vx, vy = -sa, ca
    sgn = 1 if side == "right" else -1
    p0 = (cx + ux * w * 0.42 * sgn, cy + uy * w * 0.42 * sgn + h * 0.18)
    c1 = (cx + ux * w * 0.30 * sgn + vx * h * 0.85,
          cy + uy * w * 0.30 * sgn + vy * h * 0.85)
    c2 = (cx - ux * w * 0.30 * sgn + vx * h * 0.85,
          cy - uy * w * 0.30 * sgn + vy * h * 0.85)
    p1 = (cx - ux * w * 0.44 * sgn + vx * h * 0.30,
          cy - uy * w * 0.44 * sgn + vy * h * 0.30)
    for off, col, sww, op in ((0, INK, sw + 3, 90), (0, LINK, sw, 100)):
        d.path(f"M{p0[0]:.1f},{p0[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} "
               f"{c2[0]:.1f},{c2[1]:.1f} {p1[0]:.1f},{p1[1]:.1f}",
               label if off == 0 and col == LINK else f"{label} edge",
               fill=NONE, stroke=col, strokeWidth=sww, opacity=op,
               cap="round")
    # torn ends: two short jagged nubs at the break side
    for k, tt in enumerate((0.15, 0.6)):
        ex = cx + ux * w * 0.46 * sgn
        ey = cy + uy * w * 0.46 * sgn + h * (tt - 0.25)
        d.path(f"M{ex:.1f},{ey:.1f} l{ux * 8 * sgn:.1f},{uy * 8 * sgn + 3:.1f}",
               f"{label} torn {k+1}", fill=NONE, stroke=LINK_HI,
               strokeWidth=3.2, opacity=90, cap="round")


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn star mark."""
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
    star_d, _ = star5(cx, cy, 17, "Chop star")
    d.path(star_d, "Chop star", fill="#FBE6B4", opacity=95, stroke=NONE)


# --- field -------------------------------------------------------------------
p.backdrop(top="#0F2618", bottom="#040C07", glow=("#2A6B42", 13))
dust(d, n=44, r=402, colors=("#F6E3B8", "#C8E0CC"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#0E3A20")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.62, "#000000", 0), (1, "#000000", 58)),
        stroke=NONE)
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=30)
dust(d, n=52, r=392, colors=("#F6E3B8", "#D8E8D0", "#E8C074"), seed=13,
     smin=1.0, smax=2.8, opmin=10, opmax=28, label="Disc dust")

# --- dawn burst behind the star ------------------------------------------------
SX, SY = 500, 372
for i, a in enumerate(range(200, 341, 14)):
    inside(SX + 196 * math.cos(math.radians(a)),
           SY + 196 * math.sin(math.radians(a)), 4, f"wedge {a}")
    burst_wedge(SX, SY, a, 74, 196, 4.6,
                BURST_RED if i % 2 else BURST_CREAM,
                50 if i % 2 else 28, f"Burst wedge {i+1}")
glow(d, SX, SY, 210, "#F2C66E", a=30, label="Dawn glow")

# --- the star -------------------------------------------------------------------
star_d, _ = star5(SX + 6, SY + 9, 128, "Star shadow")
d.path(star_d, "Star shadow", fill=INK, opacity=30, stroke=NONE)
star_d2, _ = star5(SX, SY, 128, "Freedom star")
d.path(star_d2, "Freedom star",
       fill=lin((SX, SY - 128), (SX, SY + 128),
                (0, GOLD_HI), (0.5, GOLD), (1, GOLD_LO)),
       stroke=INK, strokeWidth=4.5)
inner_d, _ = star5(SX, SY - 10, 78, "Star inner")
d.path(inner_d, "Star inner",
       fill=lin((SX, SY - 88), (SX, SY + 68),
                (0, "#FFF4CE"), (1, "#F0BE6A")), opacity=88, stroke=NONE)
d.shape("ellipse", "Star core", x=SX - 13, y=SY - 13, width=26, height=26,
        fill="#FFFBE8", opacity=92, stroke=NONE)

# --- the broken chain along the lower rim -----------------------------------------
# faint horizon arc the chain rests on
d.path(f"M{PCX + 305*math.cos(math.radians(40)):.1f},{PCY + 305*math.sin(math.radians(40)):.1f} "
       f"A305,305 0 0 1 {PCX + 305*math.cos(math.radians(140)):.1f},{PCY + 305*math.sin(math.radians(140)):.1f}",
       "Horizon arc", fill=NONE, stroke=GOLD, strokeWidth=2.4, opacity=32,
       cap="round")
ARC_R = 292
for i, a_deg in enumerate([52, 61, 70, 79, 101, 110, 119, 128]):
    a = math.radians(a_deg)
    lx, ly = PCX + ARC_R * math.cos(a), PCY + ARC_R * math.sin(a)
    inside(lx, ly, 18, f"link {i}")
    # tangent angle along the arc; alternate links lie across it
    link(lx, ly, a_deg + 90 + (42 if i % 2 else 0), f"Link {i+1}")

# the snapped pair flanking the break, pulled apart and tilted
broken_link(448, 724, -18, "left", "Broken link L")
broken_link(552, 724, 18, "right", "Broken link R")

# shards flung from the break
for i, (x, y, w, rot) in enumerate([(486, 700, 7, -30), (514, 694, 8, 20),
                                    (500, 668, 5, 70), (476, 676, 5, -60),
                                    (528, 668, 6, 40)]):
    inside(x, y, 12, f"shard {i}")
    d.shape("line", f"Shard {i+1}", x1=x, y1=y, x2=x + w * math.cos(math.radians(rot)),
            y2=y + w * math.sin(math.radians(rot)), stroke=LINK_HI,
            strokeWidth=3.4, opacity=88, cap="round")
for i, (x, y, r) in enumerate([(470, 700, 2.6), (534, 702, 2.4), (500, 646, 2.2)]):
    d.shape("ellipse", f"Shard dot {i+1}", x=x - r, y=y - r, width=2 * r,
            height=2 * r, fill=GOLD_HI, opacity=82, stroke=NONE)

# a few ember-like sparks rising beside the star
for i, (x, y, r, c) in enumerate([(330, 300, 3.0, GOLD_HI), (668, 312, 2.8, "#F6E3B8"),
                                  (360, 460, 2.4, "#E88A5A"), (640, 452, 2.6, GOLD_HI),
                                  (420, 208, 2.4, "#F6E3B8"), (584, 216, 2.6, "#E88A5A")]):
    inside(x, y, 14, f"spark {i}")
    d.shape("ellipse", f"Spark {i+1}", x=x - r, y=y - r, width=2 * r,
            height=2 * r, fill=c, opacity=78, stroke=NONE)

# --- seal + caption --------------------------------------------------------------
seal_chop()
caption(p, "JUNETEENTH", "JUNE 19 · 1865 · FREEDOM DAY",
        name_color="#F2ECD8", sub_color="#C9A46A",
        name_size=52, tracking_name=92, sub_size=21, tracking_sub=42,
        sub_font=SERIF)
p.finish(SLUG)
