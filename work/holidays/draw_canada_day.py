#!/usr/bin/env python3
"""Canada Day — Festival Seal V1R00.

July 1: a single maple leaf in warm scarlet on a cream field — eleven
points, drawn veins, a pale edge — with red-and-amber firework bursts
overhead, a gingham picnic-blanket edge sagging across the lower field,
maple keys drifting to rest on it, and a few sparks. Vermilion chop with
a drawn leaf mark. 1000x1000.

Recovered from a dead worker's worktree (t3/1c3b203b) and finished here:
stem-safe shadow/edge underlays, leaf drop shadow, picnic blanket arc +
samaras filling the lower field, bilingual date line.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, caption, firework

SLUG = "canada-day-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#F7EFDC"
FIELD_LO = "#D9C398"
MAPLE_HI = "#E85A44"
MAPLE = "#C8372B"
MAPLE_LO = "#7E1B16"
BURST_RED = "#B23A30"
BURST_AMBER = "#D08A3A"

p = Plate("Canada Day — Festival Seal", 1000, 1000)
d = p.d

# stylized eleven-point maple leaf, y up, unit ~150px tall
LEAF = [
    (0, 156), (20, 100), (52, 116), (42, 74), (102, 88), (86, 46),
    (134, 48), (106, 14), (146, -6), (100, -14), (110, -50),
    (26, -32), (11, -54), (11, -96), (-11, -96), (-11, -54),
    (-26, -32), (-110, -50), (-100, -14), (-146, -6), (-106, 14),
    (-134, 48), (-86, 46), (-102, 88), (-42, 74), (-52, 116),
    (-20, 100),
]
LEAF_NS = LEAF[:12] + LEAF[16:]          # same outline, stem chorded shut —
                                         # for underlays, so nothing pokes
                                         # out below the stem


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def leaf_d(cx, cy, s, sx=0.88, pts=None):
    pts = LEAF if pts is None else pts
    out = [(cx + px * s * sx, cy - py * s) for px, py in pts]
    return ("M%.1f,%.1f " % out[0]
            + " ".join("L%.1f,%.1f" % q for q in out[1:]) + " Z")


def maple_leaf(cx, cy, s, label="Maple leaf"):
    """Cream-edged scarlet leaf with drawn veins and a tapered stem."""
    for px, py in LEAF:
        inside(cx + px * s * 0.94, cy - py * s * 1.07, 10, f"{label} pt")
    # soft halo, drop shadow, cream edge
    glow(d, cx, cy - 10 * s, 190 * s, "#D08A3A", a=26, label=f"{label} halo")
    d.path(leaf_d(cx + 5 * s, cy + 8 * s, s, pts=LEAF_NS), f"{label} shadow",
           fill=INK, opacity=14, stroke=NONE)
    d.path(leaf_d(cx, cy + 0.7 * s, s * 1.018, pts=LEAF_NS), f"{label} edge",
           fill="#FBF2DF", opacity=92, stroke=NONE)
    d.path(leaf_d(cx, cy, s), label,
           fill=lin((cx, cy - 160 * s), (cx, cy + 130 * s),
                    (0, MAPLE_HI), (0.52, MAPLE), (1, MAPLE_LO)),
           stroke=INK, strokeWidth=3.6)
    # veins: centre stem up, diagonals to the six outer tips
    vx, vy = cx, cy - 4 * s                    # vein hub mid-leaf
    d.path(f"M{cx:.1f},{cy + 88*s:.1f} L{cx:.1f},{cy - 132*s:.1f}",
           f"{label} vein mid", fill=NONE, stroke=MAPLE_LO,
           strokeWidth=2.6, opacity=55, cap="round")
    for i, (tx, ty) in enumerate([(134, 48), (146, -6), (110, -50),
                                  (-134, 48), (-146, -6), (-110, -50)]):
        ex, ey = cx + tx * s * 0.76, cy - ty * s * 0.82
        d.path(f"M{vx:.1f},{vy:.1f} L{ex:.1f},{ey:.1f}",
               f"{label} vein {i+1}", fill=NONE, stroke=MAPLE_LO,
               strokeWidth=2.0, opacity=48, cap="round")
    # sheen on the upper-left lobe
    d.path(f"M{cx - 30*s:.1f},{cy - 108*s:.1f} Q{cx - 58*s:.1f},{cy - 70*s:.1f} "
           f"{cx - 70*s:.1f},{cy - 34*s:.1f}", f"{label} sheen",
           fill=NONE, stroke="#FFD9C8", strokeWidth=7 * s, opacity=30,
           cap="round")


def samara(x, y, ang, s, label):
    """Maple key: seed bead with two thin wings spreading in a V."""
    a = math.radians(ang)
    for i, sign in enumerate((-1, 1)):
        wa = a + sign * 0.55                       # wing ~±31° off the spine
        cx_ = x + math.cos(wa) * 24 * s
        cy_ = y + math.sin(wa) * 24 * s
        d.shape("ellipse", f"{label} wing {i+1}", x=cx_ - 15 * s,
                y=cy_ - 4.5 * s, width=30 * s, height=9 * s,
                fill=lin((cx_ - 15 * s, cy_), (cx_ + 15 * s, cy_),
                         (0, "#B8673A"), (1, "#E8A86A")),
                stroke=INK, strokeWidth=1.3, opacity=88,
                rotation=round(math.degrees(wa), 1))
    d.shape("ellipse", f"{label} seed", x=x - 5 * s, y=y - 5 * s,
            width=10 * s, height=10 * s,
            fill=rad((0, "#D8905A"), (1, "#8E4E24")), stroke=INK,
            strokeWidth=1.4)


def sparkle4(x, y, r, col, op=85, label="Sparkle"):
    q = r * 0.22
    d.path(f"M{x:.1f},{y - r:.1f} Q{x + q:.1f},{y - q:.1f} {x + r:.1f},{y:.1f} "
           f"Q{x + q:.1f},{y + q:.1f} {x:.1f},{y + r:.1f} "
           f"Q{x - q:.1f},{y + q:.1f} {x - r:.1f},{y:.1f} "
           f"Q{x - q:.1f},{y - q:.1f} {x:.1f},{y - r:.1f} Z",
           label, fill=col, opacity=op, stroke=NONE)


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn leaf mark."""
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
    d.path(leaf_d(cx, cy + 10 * 0.13, 0.13), "Chop leaf",
           fill="#FBE6B4", opacity=95, stroke=NONE)


# --- field -------------------------------------------------------------------
p.backdrop(top="#241A1C", bottom="#0A0608", glow=("#6E3A2E", 12))
dust(d, n=44, r=402, colors=("#F6E3B8", "#E8C8B8"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#8E1B12")
d.shape("ellipse", "Field vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#8E5A34", 0), (0.62, "#8E5A34", 0), (1, "#8E5A34", 30)),
        stroke=NONE)
ring_dots(d, r=397, n=56, size=2.6, color="#B23A30", opacity=30)
dust(d, n=52, r=392, colors=("#E8C074", "#D8A88A", "#C8735A"), seed=13,
     smin=1.0, smax=2.8, opmin=10, opmax=26, label="Disc dust")

# --- fireworks ------------------------------------------------------------------
firework(d, 304, 246, 68, col1=BURST_RED, col2=BURST_AMBER, rays=16, seed=7,
         label="Burst L")
firework(d, 646, 262, 58, col1=BURST_RED, col2="#E8C074", rays=14, seed=11,
         label="Burst R")
firework(d, 500, 146, 42, col1=BURST_AMBER, col2=BURST_RED, rays=12, seed=19,
         label="Burst top")

# --- the leaf ---------------------------------------------------------------------
maple_leaf(500, 458, 1.14)

# --- picnic blanket edge: a gingham band sagging across the lower field ------
def band_pt(t):
    """Top edge of the blanket arc (quadratic, control (500,806))."""
    u = 1 - t
    return (u * u * 272 + 2 * u * t * 500 + t * t * 728,
            u * u * 726 + 2 * u * t * 806 + t * t * 726)


def band_pt_lo(t):
    """Bottom edge (quadratic, control (500,858))."""
    u = 1 - t
    return (u * u * 272 + 2 * u * t * 500 + t * t * 728,
            u * u * 774 + 2 * u * t * 858 + t * t * 774)


for (bx, by) in [(272, 726), (728, 726), (272, 774), (728, 774), (500, 816)]:
    inside(bx, by, 10, "blanket")
d.path("M272,726 Q500,806 728,726 L728,774 Q500,858 272,774 Z",
       "Blanket", fill=lin((0, 726), (0, 860), (0, "#B8473A"), (1, "#7E2820")),
       stroke=INK, strokeWidth=2.2)
for i in range(9):
    t = 0.08 + i * 0.105
    (ax, ay), (bx, by) = band_pt(t), band_pt_lo(t)
    d.shape("line", f"Plaid V{i+1}", x1=round(ax, 1), y1=round(ay, 1),
            x2=round(bx, 1), y2=round(by, 1), stroke="#F6E3C4",
            strokeWidth=4.5, opacity=30, cap="round")
d.path("M276,749 Q500,831 724,749", "Plaid H", fill=NONE,
       stroke="#F6E3C4", strokeWidth=13, opacity=30, cap="round")

# drifting maple keys resting on / above the blanket.  (Small drift leaves
# read as starbursts at this scale — samaras stay botanical and read clean.)
samara(352, 752, 132, 0.85, "Samara L")
samara(652, 760, 55, 0.78, "Samara R")
samara(498, 806, 175, 0.70, "Samara C")
samara(606, 622, 205, 0.55, "Samara D")
samara(298, 636, 148, 0.62, "Samara E")
samara(700, 648, 32, 0.58, "Samara F")

# drifting sparks around the leaf
for i, (x, y, r, c) in enumerate([(356, 578, 8, BURST_AMBER), (648, 560, 7, BURST_RED),
                                  (300, 402, 6, "#D08A3A"), (706, 420, 6, BURST_RED),
                                  (388, 238, 5, "#B23A30"), (596, 226, 5, "#D08A3A"),
                                  (430, 662, 6, BURST_RED), (576, 656, 6, BURST_AMBER),
                                  (268, 606, 5, "#D08A3A"), (732, 646, 5, BURST_RED),
                                  (470, 772, 5, BURST_AMBER)]):
    inside(x, y, 14, f"sparkle {i}")
    sparkle4(x, y, r, c, op=72, label=f"Sparkle {i+1}")

# --- seal + caption --------------------------------------------------------------
seal_chop()
caption(p, "CANADA DAY", "JULY 1 · FÊTE DU CANADA",
        name_color="#F2ECD8", sub_color="#C9A46A",
        name_size=52, tracking_name=96, sub_size=21, tracking_sub=40,
        sub_font=SERIF)
p.finish(SLUG)
