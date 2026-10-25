#!/usr/bin/env python3
"""Thanksgiving — Festival Seal V1R00.

A wicker cornucopia lying on a dark harvest table, its mouth tipped low and
spilling the season: a ribbed pumpkin, bottle and wart gourds, two maize ears
crossed in their husks, a grape cluster, an apple, wheat stalks fanning out
behind and maple leaves scattered on the table. Deep russet field, gold rim,
vermilion chop with a drawn wheat ear. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth,
                          blend, ribbon)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "thanksgiving-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#46220F"
FIELD_LO = "#180A04"
TABLE_HI = "#5A3218"
TABLE_LO = "#2A1408"
HORN_HI = "#D89A4E"
HORN = "#B07030"
HORN_LO = "#6E3C14"
PUMP_HI = "#F6A54A"
PUMP = "#E87A24"
PUMP_LO = "#9E4A10"
GOURD = "#D8B86A"
GOURD_LO = "#8A6A2E"
MAIZE = "#F2C24E"
MAIZE_LO = "#C0821C"
HUSK = "#7A8A3E"
HUSK_LO = "#46541E"
GRAPE = "#6A3E6E"
GRAPE_LO = "#3A1E42"
WHEAT = "#D8B45E"
WHEAT_LO = "#9A742E"

p = Plate("Thanksgiving — Festival Seal", 1000, 1000)
d = p.d
TAU = math.pi * 2


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def wheat(x0, y0, cx_, cy_, tipx, tipy, label, grains=7):
    """Wheat stalk: curved stem + alternating grains bunched near the tip."""
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx_:.1f},{cy_:.1f} {tipx:.1f},{tipy:.1f}",
           label, fill=NONE, stroke=WHEAT_LO, strokeWidth=2.6, cap="round")
    inside(tipx, tipy, 6, f"{label} tip")
    # direction at the tip for grain alignment
    dx, dy = tipx - cx_, tipy - cy_
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx / ln, dy / ln
    for i in range(grains):
        t = i / (grains - 1)
        # grain position along the last stretch of the stem
        gx = tipx - ux * t * 44
        gy = tipy - uy * t * 44
        ang = math.degrees(math.atan2(uy, ux)) - 90
        for sgn in (-1, 1):
            d.shape("ellipse", f"{label} grain {i}{'a' if sgn < 0 else 'b'}",
                    x=gx + (-uy) * sgn * 4 - 4.5,
                    y=gy + ux * sgn * 4 - 6,
                    width=9, height=12, fill=WHEAT, stroke=WHEAT_LO,
                    strokeWidth=0.8, opacity=95,
                    rotation=round(ang + sgn * 22, 1))
    # awn whiskers off the tip
    for sgn in (-1, 1):
        d.path(f"M{tipx:.1f},{tipy:.1f} "
               f"L{tipx + ux * 26 - uy * sgn * 10:.1f},"
               f"{tipy + uy * 26 + ux * sgn * 10:.1f}",
               f"{label} awn {sgn}", fill=NONE, stroke=WHEAT_LO,
               strokeWidth=1.4, opacity=80, cap="round")


def pumpkin(cx, cy, r, label):
    ry = r * 0.86
    inside(cx - r, cy, 4, f"{label} L")
    inside(cx + r, cy, 4, f"{label} R")
    inside(cx, cy + ry, 4, f"{label} B")
    d.shape("ellipse", label, x=cx - r, y=cy - ry, width=2 * r, height=2 * ry,
            fill=rad((0, PUMP_HI), (0.5, PUMP), (1, PUMP_LO)),
            stroke=INK, strokeWidth=2.8)
    # ribs converging at stem and base
    for i, k in enumerate((-0.72, -0.40, 0.0, 0.40, 0.72)):
        d.path(f"M{cx + k*r*0.42:.1f},{cy - ry*0.90:.1f} "
               f"C{cx + k*r*1.55:.1f},{cy - ry*0.45:.1f} "
               f"{cx + k*r*1.55:.1f},{cy + ry*0.45:.1f} "
               f"{cx + k*r*0.42:.1f},{cy + ry*0.90:.1f}",
               f"{label} rib {i+1}", fill=NONE, stroke=PUMP_LO,
               strokeWidth=3.2, opacity=45, cap="round")
    # sheen
    d.shape("ellipse", f"{label} sheen", x=cx - r * 0.62, y=cy - ry * 0.66,
            width=r * 0.66, height=ry * 0.4,
            fill=rad((0, "#FFD8A8", 50), (1, "#FFD8A8", 0)), stroke=NONE)
    # stem
    d.path(f"M{cx - 5:.1f},{cy - ry*0.86:.1f} "
           f"C{cx - 7:.1f},{cy - ry*1.1:.1f} {cx + 2:.1f},{cy - ry*1.22:.1f} "
           f"{cx + 8:.1f},{cy - ry*1.26:.1f} "
           f"C{cx + 12:.1f},{cy - ry*1.16:.1f} {cx + 10:.1f},{cy - ry*1.0:.1f} "
           f"{cx + 6:.1f},{cy - ry*0.88:.1f} Z",
           f"{label} stem", fill=lin((cx, cy - ry * 1.26), (cx, cy - ry * 0.86),
                                     (0, "#7A8A3E"), (1, "#46541E")),
           stroke=INK, strokeWidth=1.6)


def bottle_gourd(cx, cy, w, h, label, body=GOURD, lo=GOURD_LO):
    """Bottle/birdhouse gourd: round bulb with a narrow neck knob."""
    rn, rb = w * 0.24, w * 0.52
    d.path(f"M{cx - rn:.1f},{cy - h*0.30:.1f} "
           f"C{cx - rn:.1f},{cy - h*0.52:.1f} {cx + rn:.1f},{cy - h*0.52:.1f} "
           f"{cx + rn:.1f},{cy - h*0.30:.1f} "
           f"C{cx + rn*1.3:.1f},{cy - h*0.12:.1f} {cx + rb:.1f},{cy + h*0.05:.1f} "
           f"{cx + rb:.1f},{cy + h*0.28:.1f} "
           f"C{cx + rb:.1f},{cy + h*0.62:.1f} {cx + rb*0.55:.1f},{cy + h*0.5:.1f} "
           f"{cx:.1f},{cy + h*0.5:.1f} "
           f"C{cx - rb*0.55:.1f},{cy + h*0.5:.1f} {cx - rb:.1f},{cy + h*0.62:.1f} "
           f"{cx - rb:.1f},{cy + h*0.28:.1f} "
           f"C{cx - rb:.1f},{cy + h*0.05:.1f} {cx - rn*1.3:.1f},{cy - h*0.12:.1f} "
           f"{cx - rn:.1f},{cy - h*0.30:.1f} Z", label,
           fill=lin((cx - rb, cy - h * 0.5), (cx + rb, cy + h * 0.5),
                    (0, "#F2DCA0"), (0.45, body), (1, lo)),
           stroke=INK, strokeWidth=2.4)
    inside(cx - rb, cy + h * 0.2, 4, f"{label} L")
    inside(cx + rb, cy + h * 0.2, 4, f"{label} R")
    # pale waist ring where bulb meets neck
    d.path(f"M{cx - rn*1.35:.1f},{cy - h*0.14:.1f} "
           f"Q{cx:.1f},{cy - h*0.05:.1f} {cx + rn*1.35:.1f},{cy - h*0.14:.1f}",
           f"{label} waist", fill=NONE, stroke=lo, strokeWidth=2.6,
           opacity=55, cap="round")
    d.path(f"M{cx:.1f},{cy - h*0.46:.1f} C{cx - 2:.1f},{cy - h*0.58:.1f} "
           f"{cx + 3:.1f},{cy - h*0.62:.1f} {cx + 7:.1f},{cy - h*0.64:.1f}",
           f"{label} stem", fill=NONE, stroke="#5A4A22", strokeWidth=3.2,
           cap="round")


def wart_gourd(cx, cy, r, label):
    """Small warty ornamental gourd, squat orange-green."""
    ry = r * 0.72
    inside(cx - r, cy, 4, f"{label} L")
    inside(cx + r, cy, 4, f"{label} R")
    d.shape("ellipse", label, x=cx - r, y=cy - ry, width=2 * r, height=2 * ry,
            fill=rad((0, "#E8B04E"), (0.55, "#C8822E"), (1, "#7A5014")),
            stroke=INK, strokeWidth=2.2)
    s = int(cx + cy)
    for i in range(9):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = TAU * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = 0.75 * (s / 2 ** 31)
        x, y = cx + math.cos(a) * rr * r * 0.9, cy + math.sin(a) * rr * ry * 0.9
        d.shape("ellipse", f"{label} wart {i+1}", x=x - 3, y=y - 2.4,
                width=6, height=4.8, fill="#F2D08A" if i % 3 else "#6A7A2E",
                opacity=80, stroke=NONE)
    d.path(f"M{cx:.1f},{cy - ry*0.9:.1f} C{cx - 2:.1f},{cy - ry*1.1:.1f} "
           f"{cx + 4:.1f},{cy - ry*1.16:.1f} {cx + 8:.1f},{cy - ry*1.18:.1f}",
           f"{label} stem", fill=NONE, stroke="#5A4A22", strokeWidth=3,
           cap="round")


def maize(cx, cy, length, ang, label):
    """Maize ear: tapered cob with kernel grid, husk leaves at the base."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    w = length * 0.30
    # husk leaves first, fanning from the butt end
    bx, by = cx - ux * length * 0.42, cy - uy * length * 0.42
    for i, sgn in enumerate((-1, 1, 0)):
        ha = a + sgn * 0.55 + (0.12 if i == 2 else 0)
        hx_, hy_ = math.cos(ha), math.sin(ha)
        tipx, tipy = bx - hx_ * length * 0.34, by - hy_ * length * 0.34
        d.path(f"M{bx:.1f},{by:.1f} "
               f"C{bx - hx_*length*0.12 - hy_*sgn*w*0.9:.1f},"
               f"{by - hy_*length*0.12 + hx_*sgn*w*0.9:.1f} "
               f"{tipx - hy_*sgn*w*0.3:.1f},{tipy + hx_*sgn*w*0.3:.1f} "
               f"{tipx:.1f},{tipy:.1f} "
               f"C{bx - hx_*length*0.22 + hy_*sgn*w*0.4:.1f},"
               f"{by - hy_*length*0.22 - hx_*sgn*w*0.4:.1f} "
               f"{bx + uy*sgn*6:.1f},{by - ux*sgn*6:.1f} {bx:.1f},{by:.1f} Z",
               f"{label} husk {i+1}",
               fill=lin((bx, by), (tipx, tipy), (0, HUSK), (1, HUSK_LO)),
               stroke=INK, strokeWidth=1.8)
    inside(tipx, tipy, 4, f"{label} husk tip")
    # cob body: tapered ellipse
    d.shape("ellipse", label, x=cx - length * 0.5, y=cy - w / 2,
            width=length, height=w,
            fill=lin((cx, cy - w / 2), (cx, cy + w / 2),
                     (0, "#FBE08A"), (0.5, MAIZE), (1, MAIZE_LO)),
            stroke=INK, strokeWidth=2.2, rotation=-ang)
    # kernel rows: 3 lengthwise grooves + cross ticks
    for k in (-0.28, 0.0, 0.28):
        x0, y0 = cx - ux * length * 0.44 - uy * k * w, \
                 cy - uy * length * 0.44 + ux * k * w
        x1, y1 = cx + ux * length * 0.44 - uy * k * w, \
                 cy + uy * length * 0.44 + ux * k * w
        d.path(f"M{x0:.1f},{y0:.1f} Q{cx - uy*k*w*1.6:.1f},{cy + ux*k*w*1.6:.1f} "
               f"{x1:.1f},{y1:.1f}", f"{label} row {k}", fill=NONE,
               stroke=MAIZE_LO, strokeWidth=1.6, opacity=55, cap="round")
    for i in range(7):
        t = (i + 0.5) / 7
        px_ = cx + ux * (t - 0.5) * length * 0.82
        py_ = cy + uy * (t - 0.5) * length * 0.82
        hw = w * 0.40 * math.sin(math.pi * (0.15 + 0.7 * t)) ** 0.6
        d.path(f"M{px_ - uy*hw:.1f},{py_ + ux*hw:.1f} "
               f"L{px_ + uy*hw:.1f},{py_ - ux*hw:.1f}",
               f"{label} tick {i+1}", fill=NONE, stroke=MAIZE_LO,
               strokeWidth=1.5, opacity=45, cap="round")
    # silk threads at the tip
    tx_, ty_ = cx + ux * length * 0.5, cy + uy * length * 0.5
    inside(tx_, ty_, 4, f"{label} silk")
    for i, sgn in enumerate((-1, 0, 1)):
        d.path(f"M{tx_:.1f},{ty_:.1f} "
               f"Q{tx_ + ux*18 - uy*sgn*12:.1f},{ty_ + uy*18 + ux*sgn*12:.1f} "
               f"{tx_ + ux*30 - uy*sgn*20:.1f},{ty_ + uy*30 + ux*sgn*20:.1f}",
               f"{label} silk {i+1}", fill=NONE, stroke="#B87038",
               strokeWidth=1.8, opacity=70, cap="round")


def grapes(cx, cy, r, label):
    """Cluster of grapes, triangular bunch."""
    s = int(cx * 3 + cy)
    rows = [(0, 0, 3), (-0.9, 1, 2), (0.9, 1, 2), (-0.45, 2, 2), (0.45, 2, 1)]
    i = 0
    for dx, dy, n in rows:
        for k in range(n):
            s = (1103515245 * s + 12345) % (2 ** 31)
            ox = (s / 2 ** 31 - 0.5) * r * 0.24
            gx = cx + dx * r + ox + (k - (n - 1) / 2) * r * 0.55
            gy = cy + dy * r * 0.8 + (s % 7) - 3
            d.shape("ellipse", f"{label} {i+1}", x=gx - r * 0.5,
                    y=gy - r * 0.5, width=r, height=r,
                    fill=rad((0, "#9A6AA0"), (0.6, GRAPE), (1, GRAPE_LO)),
                    stroke=INK, strokeWidth=1.4)
            d.shape("ellipse", f"{label} hi {i+1}", x=gx - r * 0.3,
                    y=gy - r * 0.34, width=r * 0.26, height=r * 0.2,
                    fill="#E8D0EC", opacity=55, stroke=NONE)
            i += 1
    d.path(f"M{cx:.1f},{cy - r*0.6:.1f} C{cx - 3:.1f},{cy - r*1.1:.1f} "
           f"{cx + 4:.1f},{cy - r*1.4:.1f} {cx + 10:.1f},{cy - r*1.5:.1f}",
           f"{label} stem", fill=NONE, stroke="#5A4A22", strokeWidth=2.6,
           cap="round")


def apple(cx, cy, r, label):
    """Small red apple with a dimpled top."""
    inside(cx - r, cy, 4, f"{label} L")
    inside(cx + r, cy, 4, f"{label} R")
    d.path(f"M{cx:.1f},{cy - r*0.82:.1f} "
           f"C{cx + r*0.35:.1f},{cy - r*1.0:.1f} {cx + r*0.95:.1f},{cy - r*0.6:.1f} "
           f"{cx + r:.1f},{cy - r*0.1:.1f} "
           f"C{cx + r:.1f},{cy + r*0.65:.1f} {cx + r*0.5:.1f},{cy + r:.1f} "
           f"{cx:.1f},{cy + r:.1f} "
           f"C{cx - r*0.5:.1f},{cy + r:.1f} {cx - r:.1f},{cy + r*0.65:.1f} "
           f"{cx - r:.1f},{cy - r*0.1:.1f} "
           f"C{cx - r*0.95:.1f},{cy - r*0.6:.1f} {cx - r*0.35:.1f},{cy - r*1.0:.1f} "
           f"{cx:.1f},{cy - r*0.82:.1f} Z", label,
           fill=rad((0, "#E86A4A"), (0.55, "#C0392B"), (1, "#7E1F1B")),
           stroke=INK, strokeWidth=2.0)
    d.shape("ellipse", f"{label} sheen", x=cx - r * 0.6, y=cy - r * 0.55,
            width=r * 0.5, height=r * 0.3,
            fill=rad((0, "#FFD0B8", 55), (1, "#FFD0B8", 0)), stroke=NONE)
    d.path(f"M{cx:.1f},{cy - r*0.84:.1f} L{cx + 2:.1f},{cy - r*1.14:.1f}",
           f"{label} stem", fill=NONE, stroke="#4A3418", strokeWidth=2.6,
           cap="round")


def maple_leaf(cx, cy, r, rot, col, label):
    """Lobed autumn leaf: five pointed lobes, valleys between, short stem."""
    outer = [math.radians(a + rot) for a in (-234, -162, -90, -18, 54)]
    pts = []
    for i, a in enumerate(outer):
        pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        a_next = outer[(i + 1) % 5] + (TAU if i == 4 else 0)
        mid = (a + a_next) / 2
        pts.append((cx + math.cos(mid) * r * 0.40,
                    cy + math.sin(mid) * r * 0.40))
    for a in outer:
        inside(cx + math.cos(a) * r, cy + math.sin(a) * r, 6, f"{label} tip")
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z",
           label, fill=lin((cx - r, cy - r), (cx + r, cy + r),
                           (0, col), (1, blend(col, INK, 0.45))),
           stroke=INK, strokeWidth=1.6, opacity=95)
    a = math.radians(90 + rot)
    d.path(f"M{cx:.1f},{cy:.1f} L{cx + math.cos(a)*r*0.85:.1f},"
           f"{cy + math.sin(a)*r*0.85:.1f}", f"{label} stem", fill=NONE,
           stroke=INK, strokeWidth=2.2, cap="round")
    for i, a in enumerate(outer):
        d.path(f"M{cx:.1f},{cy:.1f} L{cx + math.cos(a)*r*0.72:.1f},"
               f"{cy + math.sin(a)*r*0.72:.1f}",
               f"{label} vein {i+1}", fill=NONE, stroke=GOLD_HI,
               strokeWidth=1.1, opacity=40, cap="round")


# --- field -------------------------------------------------------------------
p.backdrop(top="#1E0E06", bottom="#0A0402", glow=("#5A2A12", 16))
dust(d, n=40, r=402, colors=("#F6E3B8", "#E8B868"), seed=41, smin=1.0,
     smax=2.4, opmin=8, opmax=20, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#5E3A16")
glow(d, 500, 420, 320, "#C8822E", a=18, label="Hearth glow")
glow(d, 500, 420, 170, "#E8A852", a=14, label="Hearth core")
ring_dots(d, r=397, n=56, size=2.4, color=GOLD, opacity=30)

# --- table band hugging the bottom rim ----------------------------------------
a_r = math.asin(252 / (PR - 6))
n_arc = 26
arc = [(PCX + (PR - 6) * math.cos(a_r + (math.pi - 2 * a_r) * i / n_arc),
        PCY + (PR - 6) * math.sin(a_r + (math.pi - 2 * a_r) * i / n_arc))
       for i in range(n_arc + 1)]
chord_l = (PCX - (PR - 6) * math.cos(a_r), PCY + 252)
d.path(f"M{chord_l[0]:.1f},{chord_l[1]:.1f} L{arc[-1][0]:.1f},{arc[-1][1]:.1f} " +
       smooth(arc, move=False) + " Z", "Table",
       fill=lin((0, 712), (0, 880), (0, TABLE_HI), (1, TABLE_LO)),
       stroke=NONE)
d.path(f"M{chord_l[0]:.1f},{chord_l[1]:.1f} L{arc[-1][0]:.1f},{arc[-1][1]:.1f}",
       "Table edge", fill=NONE, stroke="#1E0E04", strokeWidth=3,
       opacity=50, cap="round")

# --- wheat fan behind the horn mouth ------------------------------------------
for i, (tx_, ty_, cdx, cdy) in enumerate([
        (278, 322, -130, -120), (310, 296, -100, -150),
        (350, 282, -60, -160), (392, 290, -20, -150),
        (432, 310, 20, -140), (462, 340, 60, -120)]):
    wheat(394, 548, 394 + cdx, 548 + cdy, tx_, ty_, f"Wheat {i+1}",
          grains=6)

# --- cornucopia horn -------------------------------------------------------------
# spine curls at the tip so the horn hooks like a snail, opening low-left
SP = [(706, 252), (678, 246), (648, 254), (620, 272), (588, 304),
      (548, 352), (502, 412), (456, 466), (418, 514), (394, 544)]
W = [8, 18, 34, 58, 88, 118, 148, 172, 188, 198]
d_horn, HL, HR, _ = ribbon(SP, W)
d.path(d_horn, "Horn",
       fill=lin((SP[-1][0], SP[-1][1]), (SP[0][0], SP[0][1]),
                (0, HORN_HI), (0.4, HORN), (1, HORN_LO)),
       stroke=INK, strokeWidth=3.0)
# weave: ridge arcs across the horn, bulging toward the mouth
for i in range(1, len(SP) - 1):
    lx, ly = HL[i]
    rx, ry = HR[i]
    mx, my = (lx + rx) / 2, (ly + ry) / 2
    tx_, ty_ = SP[-1][0] - SP[i][0], SP[-1][1] - SP[i][1]
    ln = math.hypot(tx_, ty_) or 1
    bx, by = mx + tx_ / ln * W[i] * 0.16, my + ty_ / ln * W[i] * 0.16
    d.path(f"M{lx:.1f},{ly:.1f} Q{bx:.1f},{by:.1f} {rx:.1f},{ry:.1f}",
           f"Horn ridge {i}", fill=NONE, stroke="#5E3418",
           strokeWidth=3.4, opacity=55, cap="round")
    d.path(f"M{lx:.1f},{ly + 4:.1f} Q{bx:.1f},{by + 4:.1f} {rx:.1f},{ry + 4:.1f}",
           f"Horn ridge hi {i}", fill=NONE, stroke="#F2C078",
           strokeWidth=1.4, opacity=40, cap="round")
# weave: lengthwise strands between L and R at 1/3 and 2/3
for frac, nm in ((0.34, "a"), (0.66, "b")):
    pts = [(HL[i][0] * (1 - frac) + HR[i][0] * frac,
            HL[i][1] * (1 - frac) + HR[i][1] * frac)
           for i in range(len(SP))]
    d.path(smooth(pts), f"Horn strand {nm}", fill=NONE, stroke="#5E3418",
           strokeWidth=2.0, opacity=42, cap="round")
# sheen along the upper edge
edge = [HL[i] for i in range(1, len(SP) - 1)]
d.path(smooth(edge), "Horn sheen", fill=NONE, stroke="#F2C078",
       strokeWidth=5, opacity=28, cap="round")
# curled tip accent: the narrow end hooks back on itself
d.path("M706,252 C724,244 726,222 706,220 C692,218 686,230 694,238",
       "Horn tip curl", fill=NONE, stroke=INK, strokeWidth=3.4, cap="round")
d.path("M706,252 C724,244 726,222 706,220 C692,218 686,230 694,238",
       "Horn tip curl hi", fill=NONE, stroke=HORN_HI, strokeWidth=1.8,
       opacity=70, cap="round")

# mouth: dark opening + lip ring, tilted off the spine tangent
MX, MY, MROT = 388, 546, 28
d.shape("ellipse", "Mouth lip", x=MX - 104, y=MY - 72, width=208, height=144,
        fill=lin((MX - 80, MY - 60), (MX + 80, MY + 60),
                 (0, HORN_HI), (1, HORN_LO)),
        stroke=INK, strokeWidth=2.6, rotation=MROT)
d.shape("ellipse", "Mouth", x=MX - 92, y=MY - 62, width=184, height=124,
        fill=rad((0, "#3A1E0C"), (0.7, "#241004"), (1, "#140802")),
        stroke="#4A2A10", strokeWidth=2.4, rotation=MROT)

# --- spilled harvest ---------------------------------------------------------------
# shadows first
d.shape("ellipse", "Pile shadow", x=300, y=730, width=430, height=52,
        fill=rad((0, INK, 42), (0.6, INK, 18), (1, INK, 0)), stroke=NONE)
# produce tipping over the mouth lip — these overlap the dark opening
pumpkin(352, 562, 34, "Spill pumpkin")
grapes(430, 568, 12, "Spill grapes")
bottle_gourd(372, 668, 92, 128, "Bottle gourd")
grapes(586, 636, 15, "Grapes")
pumpkin(502, 664, 64, "Pumpkin")
apple(310, 662, 27, "Apple")
wart_gourd(600, 722, 34, "Wart gourd")
maize(424, 756, 210, -8, "Maize 1")
maize(330, 742, 180, 14, "Maize 2")

# --- scattered leaves ---------------------------------------------------------------
maple_leaf(288, 566, 34, -28, "#C0392B", "Leaf L")
maple_leaf(648, 600, 30, 38, "#C26A24", "Leaf R")
maple_leaf(500, 816, 26, 108, "#A84A1E", "Leaf low")
maple_leaf(216, 692, 24, -60, "#8A5A22", "Leaf far L")

# --- seal + caption -------------------------------------------------------------------
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
    # drawn wheat ear mark
    d.path(f"M{cx:.1f},{cy + 13:.1f} L{cx:.1f},{cy - 12:.1f}", "Chop stem",
           fill=NONE, stroke="#FBE6B4", strokeWidth=2.0, cap="round")
    for i in range(4):
        gy = cy - 10 + i * 5.5
        for sgn in (-1, 1):
            d.shape("ellipse", f"Chop grain {i}{sgn}",
                    x=cx + sgn * 4 - 3, y=gy - 3.4, width=6, height=7,
                    fill="#FBE6B4", stroke=NONE,
                    rotation=round(sgn * 24, 1))


seal_chop()
caption(p, "THANKSGIVING", "4TH THURSDAY IN NOVEMBER",
        name_color="#F4EBD4", sub_color="#C9A46A",
        name_size=46, tracking_name=56, sub_size=20, tracking_sub=40,
        sub_font=SERIF)
p.finish(SLUG)
