#!/usr/bin/env python3
"""Oktoberfest — Festival Seal V1R00.

Wiesn table still life in brown + gold: a glass Mass of amber beer with a
foaming crown spilling over the rim, a fat salted pretzel leaning against
its lower left, and a hop vine sweeping the bottom of the disc with three
cones. Deep walnut field, gold rim, vermilion chop with a drawn mini
pretzel. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin,
                          smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "oktoberfest-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#3E2414"
FIELD_LO = "#140903"
BEER_HI = "#E8A82E"
BEER = "#C07E18"
BEER_LO = "#7A4A0C"
FOAM = "#F6EBD0"
FOAM_LO = "#D9C9A0"
GLASS = "#D8E2DC"
CRUST = "#5E2E0C"
PRETZEL = "#C88434"
PRETZEL_HI = "#E8AC54"
VINE = "#4E6B34"
LEAF = "#5E7A3E"
LEAF_LO = "#33491F"
CONE = "#A8BE5E"
CONE_LO = "#7A8F3C"

p = Plate("Oktoberfest — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def hop_cone(cx, cy, s, label, hang=90):
    """Hop cone: overlapping scale bracts on a short stem, tip down."""
    a = math.radians(hang)
    ux, uy = math.cos(a), math.sin(a)          # down the cone
    nx, ny = -uy, ux                            # across
    d.path(f"M{cx:.1f},{cy - s * 1.3 * abs(uy):.1f} L{cx + ux * s * 0.1:.1f},"
           f"{cy - s * 0.55 * uy:.1f}", f"{label} stem", fill=NONE,
           stroke=VINE, strokeWidth=2.4, cap="round")
    # cone body: pointed teardrop
    tx, ty = cx + ux * s, cy + uy * s
    d.path(f"M{cx - nx * s * 0.42:.1f},{cy - ny * s * 0.42:.1f} "
           f"Q{cx - nx * s * 0.55 + ux * s * 0.4:.1f},{cy - ny * s * 0.55 + uy * s * 0.4:.1f} "
           f"{tx:.1f},{ty:.1f} "
           f"Q{cx + nx * s * 0.55 + ux * s * 0.4:.1f},{cy + ny * s * 0.55 + uy * s * 0.4:.1f} "
           f"{cx + nx * s * 0.42:.1f},{cy + ny * s * 0.42:.1f} "
           f"Q{cx:.1f},{cy - s * 0.5:.1f} {cx - nx * s * 0.42:.1f},{cy - ny * s * 0.42:.1f} Z",
           f"{label} cone", fill=lin((cx - s * .4, cy), (cx + s * .4, cy + s),
                                     (0, CONE), (1, CONE_LO)),
           stroke=LEAF_LO, strokeWidth=1.6)
    # bract chevrons
    for k, t in enumerate((0.18, 0.45, 0.72)):
        bx, by = cx + ux * s * (t - 0.55), cy + uy * s * (t - 0.55)
        hw = s * (0.44 - t * 0.24)
        d.path(f"M{bx - nx * hw:.1f},{by - ny * hw:.1f} "
               f"Q{bx + ux * s * 0.14:.1f},{by + uy * s * 0.14:.1f} "
               f"{bx + nx * hw:.1f},{by + ny * hw:.1f}",
               f"{label} bract {k+1}", fill=NONE, stroke=LEAF_LO,
               strokeWidth=1.4, opacity=75, cap="round")


def hop_leaf(x, y, ang, s, label):
    """Simple pointed hop leaf."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = -sa, ca
    tip = (x + ca * s, y + sa * s)
    d.path(f"M{x:.1f},{y:.1f} "
           f"C{x + ca*s*0.3 + tx*s*0.42:.1f},{y + sa*s*0.3 + ty*s*0.42:.1f} "
           f"{x + ca*s*0.72 + tx*s*0.30:.1f},{y + sa*s*0.72 + ty*s*0.30:.1f} "
           f"{tip[0]:.1f},{tip[1]:.1f} "
           f"C{x + ca*s*0.72 - tx*s*0.30:.1f},{y + sa*s*0.72 - ty*s*0.30:.1f} "
           f"{x + ca*s*0.3 - tx*s*0.42:.1f},{y + sa*s*0.3 - ty*s*0.42:.1f} "
           f"{x:.1f},{y:.1f} Z",
           label, fill=lin((x, y), tip, (0, LEAF), (1, LEAF_LO)),
           stroke="#22301A", strokeWidth=1.6)
    d.path(f"M{x:.1f},{y:.1f} L{tip[0]:.1f},{tip[1]:.1f}",
           f"{label} vein", fill=NONE, stroke="#9AC98E", strokeWidth=1.2,
           opacity=50, cap="round")


def chop_pretzel(cx, cy, r, label="Chop pretzel"):
    """Mini pretzel mark for the vermilion chop."""
    d.shape("ellipse", f"{label} loop", x=cx - r, y=cy - r * 0.72,
            width=2 * r, height=r * 1.44, fill=NONE, stroke="#FBE6B4",
            strokeWidth=4.4)
    d.shape("line", f"{label} arm L", x1=cx - r * 0.52, y1=cy + r * 0.62,
            x2=cx + r * 0.34, y2=cy - r * 0.10, stroke="#FBE6B4",
            strokeWidth=4.4, cap="round")
    d.shape("line", f"{label} arm R", x1=cx + r * 0.52, y1=cy + r * 0.62,
            x2=cx - r * 0.34, y2=cy - r * 0.10, stroke="#FBE6B4",
            strokeWidth=4.4, cap="round")


def seal_chop(cx=744, cy=214, s=62):
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
    chop_pretzel(cx, cy, 15)


# --- field -------------------------------------------------------------------
p.backdrop(top="#18100A", bottom="#060302", glow=("#3E2414", 16))
dust(d, n=44, r=402, colors=("#F6E3B8", "#E8C074"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#5E3A16")
ring_dots(d, r=397, n=56, size=2.4, color=GOLD, opacity=30)
for rr, op in ((170, 9), (262, 7), (340, 6)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke=GOLD,
            strokeWidth=1.4, opacity=op)
# warm tavern glow behind the stein
glow(d, 540, 500, 320, "#E8A82E", a=15, label="Tavern glow")
glow(d, 540, 500, 150, "#F2C05C", a=18, label="Tavern core")

# --- hop vine along the disc floor ----------------------------------------------
VINE_PTS = [(196, 736), (300, 770), (430, 782), (560, 780), (690, 762),
            (796, 716)]
d.path(smooth(VINE_PTS), "Hop vine", fill=NONE, stroke=VINE, strokeWidth=4.2,
       cap="round")
d.path(smooth([(700, 758), (760, 706), (788, 652), (772, 610)]),
       "Hop vine curl", fill=NONE, stroke=VINE, strokeWidth=3.4, cap="round")
# leaves along the vine
for i, (x, y, ang, s) in enumerate([(286, 764, -126, 42), (446, 780, -60, 46),
                                    (612, 776, -112, 40), (742, 742, -34, 44),
                                    (772, 620, -96, 34)]):
    hop_leaf(x, y, ang, s, f"Hop leaf {i+1}")
# cones hanging off the vine
hop_cone(360, 764, 30, "Hop cone 1")
hop_cone(540, 786, 34, "Hop cone 2")
hop_cone(726, 730, 28, "Hop cone 3")

# --- the stein ---------------------------------------------------------------------
SX, SY = 575, 470          # stein centre
SW, SH = 172, 230        # body w/h
TOP, BOT = SY - SH / 2, SY + SH / 2
inside(SX - SW / 2, BOT + 30, 8, "stein BL")
inside(SX + SW / 2 + 62, SY, 8, "handle R")
# ground shadow
d.shape("ellipse", "Stein shadow", x=SX - SW * 0.75, y=BOT + 8, width=SW * 1.5,
        height=34, fill=rad((0, "#000000", 44), (1, "#000000", 0)), stroke=NONE)
# handle (behind body edges)
d.path(f"M{SX + SW * 0.44:.1f},{TOP + 42:.1f} "
       f"C{SX + SW * 0.86:.1f},{TOP + 52:.1f} {SX + SW * 0.92:.1f},{SY + 30:.1f} "
       f"{SX + SW * 0.70:.1f},{SY + 66:.1f} "
       f"C{SX + SW * 0.60:.1f},{SY + 80:.1f} {SX + SW * 0.52:.1f},{SY + 82:.1f} "
       f"{SX + SW * 0.48:.1f},{SY + 76:.1f}",
       "Stein handle", fill=NONE, stroke=GLASS, strokeWidth=22, cap="round")
d.path(f"M{SX + SW * 0.44:.1f},{TOP + 42:.1f} "
       f"C{SX + SW * 0.86:.1f},{TOP + 52:.1f} {SX + SW * 0.92:.1f},{SY + 30:.1f} "
       f"{SX + SW * 0.70:.1f},{SY + 66:.1f} "
       f"C{SX + SW * 0.60:.1f},{SY + 80:.1f} {SX + SW * 0.52:.1f},{SY + 82:.1f} "
       f"{SX + SW * 0.48:.1f},{SY + 76:.1f}",
       "Stein handle edge", fill=NONE, stroke=INK, strokeWidth=25,
       opacity=55, cap="round")
d.path(f"M{SX + SW * 0.44:.1f},{TOP + 42:.1f} "
       f"C{SX + SW * 0.86:.1f},{TOP + 52:.1f} {SX + SW * 0.92:.1f},{SY + 30:.1f} "
       f"{SX + SW * 0.70:.1f},{SY + 66:.1f} "
       f"C{SX + SW * 0.60:.1f},{SY + 80:.1f} {SX + SW * 0.52:.1f},{SY + 82:.1f} "
       f"{SX + SW * 0.48:.1f},{SY + 76:.1f}",
       "Stein handle glass", fill=NONE, stroke=GLASS, strokeWidth=16,
       cap="round")
# glass body: gentle barrel, thick base
d.path(f"M{SX - SW/2:.1f},{TOP:.1f} "
       f"C{SX - SW/2 - 8:.1f},{SY:.1f} {SX - SW*0.44:.1f},{BOT - 18:.1f} "
       f"{SX - SW*0.40:.1f},{BOT:.1f} L{SX + SW*0.40:.1f},{BOT:.1f} "
       f"C{SX + SW*0.44:.1f},{BOT - 18:.1f} {SX + SW/2 + 8:.1f},{SY:.1f} "
       f"{SX + SW/2:.1f},{TOP:.1f} Z",
       "Stein glass", fill=lin((SX - SW / 2, SY), (SX + SW / 2, SY),
                               (0, "#E8F0E8", 30), (0.5, "#B8CCC4", 16),
                               (1, "#8AA09A", 34)),
       stroke=INK, strokeWidth=3.4)
# beer inside
d.path(f"M{SX - SW/2 + 10:.1f},{TOP + 34:.1f} "
       f"C{SX - SW/2 + 2:.1f},{SY + 6:.1f} {SX - SW*0.40:.1f},{BOT - 26:.1f} "
       f"{SX - SW*0.36:.1f},{BOT - 14:.1f} L{SX + SW*0.36:.1f},{BOT - 14:.1f} "
       f"C{SX + SW*0.40:.1f},{BOT - 26:.1f} {SX + SW/2 - 2:.1f},{SY + 6:.1f} "
       f"{SX + SW/2 - 10:.1f},{TOP + 34:.1f} Z",
       "Beer", fill=lin((SX, TOP + 34), (SX, BOT - 14),
                        (0, BEER_HI), (0.55, BEER), (1, BEER_LO)),
       stroke=NONE, opacity=96)
# glass fluting
for i, fx in enumerate((-0.26, -0.09, 0.09, 0.26)):
    d.path(f"M{SX + fx*SW:.1f},{TOP + 44:.1f} L{SX + fx*SW*0.94:.1f},{BOT - 30:.1f}",
           f"Fluting {i+1}", fill=NONE, stroke="#FFF2C8", strokeWidth=2.4,
           opacity=22, cap="round")
# thick glass base
d.shape("rectangle", "Stein base", x=SX - SW * 0.44, y=BOT - 26, width=SW * 0.88,
        height=26, radius=8, fill=lin((SX, BOT - 26), (SX, BOT),
                                      (0, "#C8D4CE", 44), (1, "#7A8E88", 60)),
        stroke=INK, strokeWidth=2.6, opacity=90)
# lip highlight
d.path(f"M{SX - SW/2 + 4:.1f},{TOP + 10:.1f} C{SX - SW*0.2:.1f},{TOP + 2:.1f} "
       f"{SX + SW*0.2:.1f},{TOP + 2:.1f} {SX + SW/2 - 4:.1f},{TOP + 10:.1f}",
       "Rim light", fill=NONE, stroke="#FFFFFF", strokeWidth=3.0, opacity=40,
       cap="round")

# --- foam crown ---------------------------------------------------------------------
# spilling head: overlapping cream blobs over the lip + drips
for i, (fx, fr) in enumerate([(-0.44, 26), (-0.28, 34), (-0.08, 38),
                              (0.12, 36), (0.30, 32), (0.46, 24)]):
    bx = SX + fx * SW
    d.shape("ellipse", f"Foam crown {i+1}", x=bx - fr, y=TOP - fr * 0.62,
            width=2 * fr, height=fr * 1.5,
            fill=rad((0, "#FFF8E4"), (0.7, FOAM), (1, FOAM_LO)),
            stroke=INK, strokeWidth=2.2)
# foam drips over the glass edge
for i, (fx, dl, dw) in enumerate([(-0.38, 34, 15), (0.06, 48, 18),
                                  (0.40, 28, 13)]):
    bx = SX + fx * SW
    d.path(f"M{bx - dw/2:.1f},{TOP + 6:.1f} "
           f"C{bx - dw*0.7:.1f},{TOP + dl*0.5:.1f} {bx - dw*0.3:.1f},{TOP + dl - 6:.1f} "
           f"{bx:.1f},{TOP + dl:.1f} C{bx + dw*0.3:.1f},{TOP + dl - 6:.1f} "
           f"{bx + dw*0.7:.1f},{TOP + dl*0.5:.1f} {bx + dw/2:.1f},{TOP + 6:.1f} Z",
           f"Foam drip {i+1}", fill=lin((bx, TOP), (bx, TOP + dl),
                                        (0, FOAM), (1, FOAM_LO)),
           stroke=INK, strokeWidth=1.6)
# foam texture bubbles
for i, (fx, fy, fr) in enumerate([(-0.3, -0.5, 4), (-0.12, -0.8, 5),
                                  (0.05, -0.45, 3.4), (0.2, -0.9, 4.4),
                                  (0.33, -0.5, 3.6), (-0.05, -1.3, 3),
                                  (0.14, -1.25, 2.6)]):
    d.shape("ellipse", f"Foam bubble {i+1}", x=SX + fx * SW - fr,
            y=TOP + fy * 30 - fr, width=2 * fr, height=2 * fr,
            fill="#FFFFFF", opacity=55, stroke=NONE)
# rising bubbles drifting up-left
for i, (x, y, r) in enumerate([(548, 330, 4), (610, 296, 5), (585, 352, 3),
                               (505, 300, 3.4), (470, 348, 2.6),
                               (640, 340, 3)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x - r, y=y - r, width=2 * r,
            height=2 * r, fill="#F8EFD8", opacity=28, stroke=NONE)

# --- the pretzel, leaning on the stein's lower left --------------------------------
PCX2, PCY2 = 384, 618
PW, PH = 196, 158
d.shape("ellipse", "Pretzel shadow", x=PCX2 - PW * 0.62, y=PCY2 + PH * 0.52,
        width=PW * 1.24, height=PH * 0.3,
        fill=rad((0, "#000000", 40), (1, "#000000", 0)), stroke=NONE)


def pretzel_stroke(pts, label, w=30):
    dd = smooth(pts)
    d.path(dd, f"{label} crust", fill=NONE, stroke=CRUST, strokeWidth=w + 7,
           cap="round")
    d.path(dd, f"{label} dough", fill=NONE, stroke=PRETZEL, strokeWidth=w,
           cap="round")
    d.path(dd, f"{label} light", fill=NONE, stroke=PRETZEL_HI, strokeWidth=w * 0.34,
           opacity=55, cap="round")


# outer loop: closed-ish ring leaning -8deg
loop = []
for i in range(13):
    a = math.radians(-90 + i * 360 / 12)
    x = PCX2 + math.cos(a) * PW * 0.52 + math.sin(a) * 10
    y = PCY2 - 18 + math.sin(a) * PH * 0.46 - math.cos(a) * 6
    loop.append((x, y))
d.path(smooth(loop, closed=True), "Pretzel loop crust", fill=NONE,
       stroke=CRUST, strokeWidth=37, cap="round")
d.path(smooth(loop, closed=True), "Pretzel loop dough", fill=NONE,
       stroke=PRETZEL, strokeWidth=30, cap="round")
d.path(smooth(loop, closed=True), "Pretzel loop light", fill=NONE,
       stroke=PRETZEL_HI, strokeWidth=10, opacity=55, cap="round")
# crossing arms: each from the loop top down through the middle to the
# opposite lower side
pretzel_stroke([(PCX2 - 30, PCY2 - PH * 0.52), (PCX2 - 6, PCY2 - 20),
                (PCX2 + 26, PCY2 + 16), (PCX2 + 52, PCY2 + PH * 0.40)],
               "Pretzel arm A", w=27)
pretzel_stroke([(PCX2 + 34, PCY2 - PH * 0.50), (PCX2 + 8, PCY2 - 16),
                (PCX2 - 24, PCY2 + 20), (PCX2 - 50, PCY2 + PH * 0.42)],
               "Pretzel arm B", w=27)
# salt grains
for i, (x, y, rot) in enumerate([(PCX2 - 58, PCY2 - 52, 20),
                                 (PCX2 + 62, PCY2 - 46, -30),
                                 (PCX2 - 70, PCY2 + 8, 60),
                                 (PCX2 + 70, PCY2 + 14, -15),
                                 (PCX2 - 6, PCY2 - 66, 45),
                                 (PCX2 + 40, PCY2 + 46, 10),
                                 (PCX2 - 38, PCY2 + 48, -40)]):
    d.shape("ellipse", f"Salt {i+1}", x=x - 4, y=y - 2.4, width=8, height=4.8,
            fill="#F8F2E2", opacity=88, stroke=NONE, rotation=rot)

# --- seal + caption --------------------------------------------------------------
seal_chop()
caption(p, "OKTOBERFEST", "19 SEPT – 4 OCT · MUNICH",
        name_color="#F6EBD0", sub_color="#D8A85E",
        name_size=52, tracking_name=86, sub_size=21, tracking_sub=50,
        sub_font=SERIF)
p.finish(SLUG)
