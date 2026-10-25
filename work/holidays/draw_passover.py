#!/usr/bin/env python3
"""Passover — Festival Seal V1R00.

The seder plate as the hero: a porcelain ka'arah in blue and white, its
six wells in the classic order — beitzah, zeroa, karpas, maror, charoset,
chazeret — each captioned in tiny Hebrew. Elijah's cup lower left, a
stack of matzo lower right. Deep blue + white. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN,
                          PCX, PCY, PR, lin, rad, gold_lin, smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "passover-V1R00"
HEBREW = "Arial Hebrew"
DIGITS = "Source Sans 3"
COBALT = "#2A4E8C"
COBALT_HI = "#5A82C0"
CHINA = "#F4F0E4"
CHINA_LO = "#D8CCAE"
WINE = "#6E1A30"

p = Plate("Passover — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#0B1526", bottom="#030610", glow=("#1E3A66", 13))
p.stars(n=26, color="#DCE8F6", seed=41, maxr=2.0)
seal_disc(p, "#22407E", "#081226", rim="#D8E4F2", rim2="#3A4E6E")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.6, "#000000", 0), (1, "#000000", 54)),
        stroke=NONE)
dust(d, n=52, r=392, colors=("#DCE8F6", "#9FC0E8", "#F6E3B8"), seed=29,
     smin=1.0, smax=2.6, opmin=8, opmax=24, label="Disc dust")
ring_dots(d, r=396, n=60, size=2.4, color="#BCD0E8", opacity=30)
# faint concentric echoes of the plate
for i, rr in enumerate((330, 360)):
    d.shape("ellipse", f"Field ring {i}", x=PCX - rr, y=PCY - rr * 0.78,
            width=2 * rr, height=2 * rr * 0.78, fill=NONE, stroke="#7EA4DC",
            strokeWidth=1.4, opacity=10)

glow(d, 500, 480, 300, "#9FC0E8", a=16, label="Plate aura", squash=0.9)

# --- the ka'arah --------------------------------------------------------------
PLX, PLY, PRX, PRY = 500, 462, 246, 182
d.shape("ellipse", "Plate shadow", x=PLX - 200, y=PLY + 160, width=400,
        height=44, fill=rad((0, INK, 58), (0.6, INK, 26), (1, INK, 0)),
        stroke=NONE)
d.shape("ellipse", "Seder plate", x=PLX - PRX, y=PLY - PRY, width=2 * PRX,
        height=2 * PRY,
        fill=lin((PLX - PRX, PLY - PRY), (PLX + PRX, PLY + PRY),
                 (0, "#FBF8EE"), (0.55, CHINA), (1, CHINA_LO)),
        stroke=INK, strokeWidth=3.4)
# cobalt rim: band + double pinline + scallop ticks
d.shape("ellipse", "Plate rim band", x=PLX - PRX * 0.94, y=PLY - PRY * 0.94,
        width=2 * PRX * 0.94, height=2 * PRY * 0.94, fill=NONE,
        stroke=COBALT, strokeWidth=16, opacity=90)
d.shape("ellipse", "Plate rim pin hi", x=PLX - PRX * 0.845, y=PLY - PRY * 0.845,
        width=2 * PRX * 0.845, height=2 * PRY * 0.845, fill=NONE,
        stroke=COBALT_HI, strokeWidth=2.2, opacity=85)
d.shape("ellipse", "Plate rim pin lo", x=PLX - PRX * 0.965, y=PLY - PRY * 0.965,
        width=2 * PRX * 0.965, height=2 * PRY * 0.965, fill=NONE,
        stroke=COBALT_HI, strokeWidth=2.2, opacity=85)
for i in range(28):
    a = math.radians(i * 360 / 28)
    x = PLX + PRX * 0.895 * math.cos(a)
    y = PLY + PRY * 0.895 * math.sin(a)
    d.shape("ellipse", f"Rim scallop {i+1}", x=x - 4.4, y=y - 3.2, width=8.8,
            height=6.4, fill="#FBF8EE", opacity=85, stroke=NONE)
# sheen
d.path(f"M{PLX - 190},{PLY - 120} C{PLX - 90},{PLY - 168} {PLX + 60},{PLY - 172} "
       f"{PLX + 150},{PLY - 140}", "Plate sheen", fill=NONE, stroke="#FFFFFF",
       strokeWidth=7, opacity=40, cap="round")


def well(cx, cy, r, label):
    d.shape("ellipse", f"{label} dish", x=cx - r, y=cy - r * 0.82, width=2 * r,
            height=2 * r * 0.82,
            fill=lin((cx - r, cy - r), (cx + r, cy + r * 0.8),
                     (0, "#E4DBC2"), (0.6, "#F8F4E8"), (1, "#CFC2A0")),
            stroke=COBALT, strokeWidth=2.4)
    d.shape("ellipse", f"{label} well", x=cx - r * 0.78, y=cy - r * 0.62,
            width=2 * r * 0.78, height=2 * r * 0.62 * 0.82,
            fill=rad((0, "#D8CCAA"), (0.7, "#EFE8D2"), (1, "#F8F4E8")),
            stroke="#B8A87E", strokeWidth=1.2)


def heb(text, cx, cy, size=12, label="Heb"):
    d.text(text, label, x=cx, y=cy, size=size, font=HEBREW, color=COBALT,
           justify="center")


# beitzah — roasted egg (upper left)
well(395, 380, 40, "Beitzah")
d.shape("ellipse", "Egg", x=378, y=364, width=30, height=36,
        fill=rad((0, "#E0B070"), (0.65, "#B8823E"), (1, "#8A5426")),
        stroke="#5E3414", strokeWidth=1.8, rotation=-14)
d.shape("ellipse", "Egg gloss", x=383, y=368, width=9, height=12,
        fill="#FFEDC8", opacity=50, stroke=NONE, rotation=-14)
heb("ביצה", 395, 438)

# zeroa — roasted shank bone (upper right)
well(605, 380, 40, "Zeroa")
d.path("M584,388 C580,378 586,368 596,370 C600,362 612,362 616,370 "
       "C624,368 630,376 626,384 L634,396 C638,402 632,410 624,406 "
       "C620,412 608,412 606,404 C600,408 590,404 592,396 Z",
       "Shank meat", fill=lin((584, 364), (634, 410), (0, "#A85C30"),
                              (0.55, "#8A4420"), (1, "#5E2A12")),
       stroke="#3E1C0C", strokeWidth=1.8)
d.path("M592,394 L580,404 M580,404 C574,406 574,414 580,414 C578,420 586,422 590,416",
       "Shank bone", fill=NONE, stroke="#EFE4CC", strokeWidth=5, cap="round")
d.path("M588,380 C594,374 604,372 612,374", "Shank gloss", fill=NONE,
       stroke="#E8A87A", strokeWidth=2.4, opacity=55, cap="round")
heb("זרוע", 605, 438)

# karpas — parsley sprig (middle left)
well(368, 498, 40, "Karpas")
for i, (dx, dy, ang) in enumerate([(-8, 4, -30), (0, -2, 0), (8, 4, 30),
                                   (-4, 8, -15), (4, 8, 15)]):
    d.shape("ellipse", f"Parsley leaf {i+1}", x=368 + dx - 7, y=498 + dy - 13,
            width=14, height=20, fill=lin(0, 480, 0, 505, (0, "#6E9A4E"),
                                          (1, "#3A6426")),
            stroke="#244A18", strokeWidth=1.2, rotation=ang)
d.path("M368,512 L368,486", "Parsley stem", fill=NONE, stroke="#3A6426",
       strokeWidth=2, cap="round")
heb("כרפס", 368, 556)

# maror — grated horseradish mound (centre)
well(500, 502, 42, "Maror")
d.path("M478,514 C474,498 484,486 500,486 C516,486 526,498 522,514 "
       "C514,520 486,520 478,514 Z",
       "Maror mound", fill=rad((0, "#F4EAD2"), (0.7, "#DCCBA4"),
                               (1, "#B8A87E")), stroke="#8A7A50",
       strokeWidth=1.8)
for i, (dx, dy) in enumerate([(-8, 502), (2, 494), (9, 506), (-2, 510), (6, 500)]):
    d.path(f"M{500 + dx},{502 + dy} l{4 - i},{3}", f"Maror shred {i+1}",
           fill=NONE, stroke="#A8946A", strokeWidth=1.4, opacity=70,
           cap="round")
heb("מרור", 500, 562)

# charoset — chunky paste (middle right)
well(632, 498, 40, "Charoset")
d.path("M612,514 C608,498 618,488 632,488 C648,488 656,500 652,514 "
       "C644,520 620,520 612,514 Z",
       "Charoset mound", fill=rad((0, "#A8763E"), (0.65, "#7A4A22"),
                                  (1, "#52300F")), stroke="#3E240E",
       strokeWidth=1.8)
for i, (dx, dy, s) in enumerate([(-7, 499, 3), (3, 494, 3.4), (10, 503, 2.6),
                                 (-2, 508, 2.8)]):
    d.shape("ellipse", f"Charoset nut {i+1}", x=632 + dx - s / 2,
            y=498 + dy - s / 2, width=s, height=s, fill="#D9B87E",
            opacity=85, stroke=NONE)
d.path("M622,496 C628,492 638,492 644,496", "Charoset gloss", fill=NONE,
       stroke="#E8C88E", strokeWidth=2, opacity=45, cap="round")
heb("חרוסת", 632, 556)

# the holiday name across the plate's top
d.text("פסח", "Plate title", x=500, y=336, size=21, font=HEBREW,
       color=COBALT, justify="center")

# chazeret — romaine leaf (bottom centre)
well(500, 598, 34, "Chazeret")
d.path("M500,616 C488,608 482,594 486,582 C490,572 500,568 500,568 "
       "C500,568 510,572 514,582 C518,594 512,608 500,616 Z",
       "Romaine leaf", fill=lin((486, 568), (514, 616), (0, "#8AB86A"),
                                (0.55, "#5A8A3E"), (1, "#3A6426")),
       stroke="#244A18", strokeWidth=1.6)
d.path("M500,572 L500,612 M500,584 L492,578 M500,584 L508,578 "
       "M500,596 L491,590 M500,596 L509,590 M500,606 L493,602 M500,606 L507,602",
       "Romaine veins", fill=NONE, stroke="#C8E4A8", strokeWidth=1.4,
       opacity=75, cap="round")
heb("חזרת", 570, 616)

# --- Elijah's cup -------------------------------------------------------------
CX, CY = 312, 700
d.shape("ellipse", "Cup shadow", x=CX - 46, y=CY + 90, width=92, height=20,
        fill=rad((0, INK, 55), (0.6, INK, 24), (1, INK, 0)), stroke=NONE)
# foot + stem
d.path(f"M{CX - 34},{CY + 78} C{CX - 20},{CY + 66} {CX - 10},{CY + 52} "
       f"{CX - 8},{CY + 34} L{CX + 8},{CY + 34} C{CX + 10},{CY + 52} "
       f"{CX + 20},{CY + 66} {CX + 34},{CY + 78} Z",
       "Cup stem", fill=lin((CX - 30, CY + 34), (CX + 30, CY + 78),
                            (0, "#C8D4E4"), (0.5, "#F4F8FC"), (1, "#8AA0BC")),
       stroke=INK, strokeWidth=2.4)
d.shape("ellipse", "Cup foot", x=CX - 38, y=CY + 74, width=76, height=16,
        fill=lin(0, CY + 74, 0, CY + 90, (0, "#F4F8FC"), (1, "#8AA0BC")),
        stroke=INK, strokeWidth=2.2)
# bowl
d.path(f"M{CX - 44},{CY - 44} C{CX - 44},{CY - 8} {CX - 26},{CY + 14} "
       f"{CX},{CY + 16} C{CX + 26},{CY + 14} {CX + 44},{CY - 8} "
       f"{CX + 44},{CY - 44} Z",
       "Cup bowl", fill=lin((CX - 44, CY - 44), (CX + 44, CY + 16),
                            (0, "#B8C8DC"), (0.45, "#F4F8FC"), (0.8, "#A8BCd4".upper()),
                            (1, "#7A90AC")),
       stroke=INK, strokeWidth=2.6)
# rim + wine
d.shape("ellipse", "Cup rim", x=CX - 44, y=CY - 52, width=88, height=18,
        fill=lin(0, CY - 52, 0, CY - 34, (0, "#F4F8FC"), (1, "#9AB0CC")),
        stroke=INK, strokeWidth=2.2)
d.shape("ellipse", "Wine", x=CX - 37, y=CY - 49, width=74, height=13,
        fill=rad((0, "#8E2A44"), (0.7, WINE), (1, "#46101E")), stroke=NONE)
d.shape("ellipse", "Wine glint", x=CX - 22, y=CY - 48, width=26, height=5,
        fill="#D88AA0", opacity=40, stroke=NONE)
d.path(f"M{CX - 36},{CY - 30} C{CX - 38},{CY - 4} {CX - 22},{CY + 10} "
       f"{CX - 6},{CY + 14}", "Cup sheen", fill=NONE, stroke="#FFFFFF",
       strokeWidth=4, opacity=45, cap="round")
# gold band on the bowl
d.path(f"M{CX - 43},{CY - 18} C{CX - 20},{CY - 8} {CX + 20},{CY - 8} "
       f"{CX + 43},{CY - 18}", "Cup band", fill=NONE, stroke=GOLD,
       strokeWidth=3.2, opacity=80, cap="round")

# --- matzo stack --------------------------------------------------------------
def matzo(cx, cy, w, deg, label):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)

    def rp(x, y):
        return (cx + (x - cx) * c - (y - cy) * s,
                cy + (x - cx) * s + (y - cy) * c)

    h = w
    pts = [rp(cx - w / 2, cy - h / 2), rp(cx + w / 2, cy - h / 2),
           rp(cx + w / 2, cy + h / 2), rp(cx - w / 2, cy + h / 2)]
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", label,
           fill=lin((cx - w / 2, cy - h / 2), (cx + w / 2, cy + h / 2),
                    (0, "#E8CC96"), (0.55, "#D9B97E"), (1, "#B8935C")),
           stroke="#7A5A2A", strokeWidth=2.4)
    for i in (-1, 0, 1):
        y0 = cy + i * h * 0.28
        p0 = rp(cx - w * 0.42, y0)
        p1 = rp(cx, y0 + 5)
        p2 = rp(cx + w * 0.42, y0)
        d.path(f"M{p0[0]:.1f},{p0[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} "
               f"{p2[0]:.1f},{p2[1]:.1f}", f"{label} score {i}",
               fill=NONE, stroke="#B8935C", strokeWidth=2.2, opacity=75,
               cap="round")
    for gy in (-0.3, -0.1, 0.1, 0.3):
        for gx in (-0.32, -0.11, 0.11, 0.32):
            px_, py_ = rp(cx + gx * w, cy + gy * h)
            d.shape("ellipse", f"{label} hole {gx}-{gy}", x=px_ - 1.6,
                    y=py_ - 1.6, width=3.2, height=3.2, fill="#9A7238",
                    opacity=65, stroke=NONE)


matzo(600, 726, 112, -9, "Matzo back")
matzo(634, 754, 116, 6, "Matzo mid")
matzo(604, 780, 108, -4, "Matzo front")

# --- chop + caption -----------------------------------------------------------
CHX, CHY, CHW, CHH = 712, 152, 50, 110
inside(CHX + CHW, CHY, 6, "chop TR")
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("פסח", x=CHX, y=CHY, w=CHW, h=CHH, size=27, font=HEBREW)

caption(p, "PASSOVER", "15–22 NISAN · MARCH – APRIL",
        sub_font=DIGITS, name_color="#EAF0FA", sub_color="#9DB8D8",
        name_size=52, tracking_name=90, sub_size=20, tracking_sub=40)

p.finish(SLUG)
