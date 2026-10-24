#!/usr/bin/env python3
"""Bastille Day — Festival Seal V1R00.

La Fête Nationale: a pleated tricolor cockade — cobalt, cream and scarlet
concentric ribbon with twin stitched tails — pinned low on the disc, gold and
vermilion firework bursts over a deep twilight field, one rocket trail still
climbing. Vermilion chop with a drawn cockade mark. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, caption, firework

SLUG = "bastille-day-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#27386B"
FIELD_LO = "#0A1024"
COBALT_HI = "#5C7FE4"
COBALT = "#3351B4"
COBALT_LO = "#18295E"
CREAM_HI = "#FBF4E2"
CREAM = "#F0E2C4"
CREAM_LO = "#C8AC7C"
SCARLET_HI = "#F0705E"
SCARLET = "#C8372B"
SCARLET_LO = "#711A15"

p = Plate("Bastille Day — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def bez2(p0, p1, p2, t):
    mt = 1 - t
    return (mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0],
            mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1])


def pleats(cx, cy, r_in, r_out, n, dark, lite, phase=0.0):
    """Alternating shadow/highlight radial pleats on a ribbon band."""
    for i in range(n):
        a = phase + math.pi * 2 * i / n
        ca, sa = math.cos(a), math.sin(a)
        x0, y0 = cx + ca * r_in, cy + sa * r_in
        x1, y1 = cx + ca * r_out, cy + sa * r_out
        col = dark if i % 2 else lite
        d.shape("line", f"Pleat {r_out:.0f}-{i}", x1=round(x0, 1),
                y1=round(y0, 1), x2=round(x1, 1), y2=round(y1, 1),
                stroke=col, strokeWidth=2.0, opacity=34, cap="round")


def tail(top_x, top_y, lean, label):
    """Swallowtailed ribbon tail under the rosette; lean=-1 hangs left,
    +1 hangs right. Cobalt cloth, cream spine stripe, scarlet edge stitch."""
    l = lean
    ax, ay = top_x + 16 * l, top_y              # outer top (hidden)
    bx, by = top_x - 22 * l, top_y + 12         # inner top (hidden)
    tx, ty = top_x + 92 * l, top_y + 130        # outer bottom tip
    nx, ny = top_x + 54 * l, top_y + 100        # notch
    t2x, t2y = top_x + 14 * l, top_y + 132      # inner bottom tip
    d.path(f"M{ax:.1f},{ay:.1f} "
           f"C{ax + 28*l:.1f},{ay + 66:.1f} {tx - 4*l:.1f},{ty - 54:.1f} "
           f"{tx:.1f},{ty:.1f} L{nx:.1f},{ny:.1f} L{t2x:.1f},{t2y:.1f} "
           f"C{t2x - 10*l:.1f},{t2y - 56:.1f} {bx + 4*l:.1f},{by + 38:.1f} "
           f"{bx:.1f},{by:.1f} Z",
           label, fill=lin(0, ay, 0, t2y, (0, COBALT), (0.55, "#2A4496"),
                           (1, COBALT_LO)), stroke=INK, strokeWidth=2.4)
    # cream centre stripe along the spine
    d.path(f"M{top_x:.1f},{top_y + 14:.1f} C{top_x + 22*l:.1f},{top_y + 68:.1f} "
           f"{top_x + 50*l:.1f},{top_y + 108:.1f} {top_x + 52*l:.1f},{top_y + 118:.1f}",
           f"{label} stripe", fill=NONE, stroke=CREAM, strokeWidth=7,
           opacity=42, cap="round")
    # scarlet stitch along the outer edge
    d.path(f"M{ax + 4*l:.1f},{ay + 8:.1f} C{ax + 30*l:.1f},{ay + 68:.1f} "
           f"{tx - 8*l:.1f},{ty - 52:.1f} {tx - 4*l:.1f},{ty - 8:.1f}",
           f"{label} stitch", fill=NONE, stroke=SCARLET_HI, strokeWidth=2.2,
           opacity=55, cap="round", dash=[5, 5])


def cockade(cx, cy, r, label="Cockade"):
    """Pleated tricolor rosette: cobalt outer, cream middle, scarlet heart."""
    d.shape("ellipse", f"{label} shadow", x=cx - r + 5, y=cy - r + 8,
            width=2 * r, height=2 * r, fill=INK, opacity=30, stroke=NONE)
    d.shape("ellipse", f"{label} outer", x=cx - r, y=cy - r, width=2 * r,
            height=2 * r,
            fill=rad((0, COBALT_HI), (0.55, COBALT), (1, COBALT_LO)),
            stroke=INK, strokeWidth=3.2)
    pleats(cx, cy, r * 0.55, r * 0.96, 36, "#121F48", "#8FA6EE")
    d.shape("ellipse", f"{label} rim light", x=cx - r * 0.985,
            y=cy - r * 0.985, width=2 * r * 0.985, height=2 * r * 0.985,
            fill=NONE, stroke="#9AB2F2", strokeWidth=1.8, opacity=38)
    # cream band
    d.shape("ellipse", f"{label} cream", x=cx - r * 0.56, y=cy - r * 0.56,
            width=2 * r * 0.56, height=2 * r * 0.56,
            fill=rad((0, CREAM_HI), (0.68, CREAM), (1, CREAM_LO)),
            stroke=INK, strokeWidth=2.4)
    pleats(cx, cy, r * 0.335, r * 0.53, 26, "#A8864E", "#FFFDF2",
           phase=0.11)
    # scarlet heart
    d.shape("ellipse", f"{label} heart", x=cx - r * 0.33, y=cy - r * 0.33,
            width=2 * r * 0.33, height=2 * r * 0.33,
            fill=rad((0, SCARLET_HI), (0.6, SCARLET), (1, SCARLET_LO)),
            stroke=INK, strokeWidth=2.4)
    pleats(cx, cy, r * 0.13, r * 0.30, 16, "#4E1210", "#FF9E88",
           phase=0.06)
    d.shape("ellipse", f"{label} stud", x=cx - r * 0.105, y=cy - r * 0.105,
            width=2 * r * 0.105, height=2 * r * 0.105,
            fill=rad((0, GOLD_HI), (0.6, GOLD), (1, GOLD_LO)), stroke=INK,
            strokeWidth=1.8)
    d.shape("ellipse", f"{label} sheen", x=cx - r * 0.55, y=cy - r * 0.72,
            width=r * 0.9, height=r * 0.5, fill="#FFFFFF", opacity=14,
            stroke=NONE, rotation=-18)


def rocket_trail(x0, y0, cx1, cy1, x1, y1, label):
    """Dashed gold ascent line ending near a burst, ember head partway up."""
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx1:.1f},{cy1:.1f} {x1:.1f},{y1:.1f}",
           f"{label} glow", fill=NONE, stroke=GOLD, strokeWidth=6,
           opacity=12, cap="round")
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx1:.1f},{cy1:.1f} {x1:.1f},{y1:.1f}",
           label, fill=NONE, stroke=GOLD_HI, strokeWidth=2.4, opacity=62,
           cap="round", dash=[9, 7])
    hx, hy = bez2((x0, y0), (cx1, cy1), (x1, y1), 0.86)
    d.shape("ellipse", f"{label} head glow", x=hx - 12, y=hy - 12, width=24,
            height=24, fill=rad((0, "#FFD98A", 60), (1, "#FFD98A", 0)),
            stroke=NONE)
    d.shape("ellipse", f"{label} head", x=hx - 3.4, y=hy - 3.4, width=6.8,
            height=6.8, fill="#FFEFC4", opacity=95, stroke=NONE)


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn cockade mark."""
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
    for i, rr in enumerate((19.5, 13, 7)):
        d.shape("ellipse", f"Chop ring {i+1}", x=cx - rr, y=cy - rr,
                width=2 * rr, height=2 * rr, fill=NONE, stroke="#FBE6B4",
                strokeWidth=2.6, opacity=92)
    d.shape("ellipse", "Chop heart", x=cx - 2.8, y=cy - 2.8, width=5.6,
            height=5.6, fill="#FBE6B4", opacity=95, stroke=NONE)


# --- field -------------------------------------------------------------------
p.backdrop(top="#141C38", bottom="#05070F", glow=("#31448A", 13))
dust(d, n=44, r=402, colors=("#F6E3B8", "#C8D0F0"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#1C2A58")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.62, "#000000", 0), (1, "#000000", 58)),
        stroke=NONE)
d.shape("ellipse", "Night aura", x=160, y=90, width=680, height=600,
        fill=rad((0, "#46589E", 14), (0.55, "#31448A", 6), (1, "#31448A", 0)),
        stroke=NONE)
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=30)
dust(d, n=58, r=392, colors=("#F6E3B8", "#E8ECF8", "#E8C074"), seed=17,
     smin=1.0, smax=2.8, opmin=10, opmax=30, label="Disc dust")

# --- fireworks ---------------------------------------------------------------
firework(d, 332, 268, 100, col1=GOLD, col2="#FFF0C8", rays=20, seed=5,
         label="Burst L")
firework(d, 622, 252, 84, col1=GOLD, col2=SCARLET_HI, rays=16, seed=9,
         label="Burst R")
firework(d, 508, 148, 50, col1="#F6E3B8", col2="#8FA6EE", rays=12, seed=13,
         label="Burst top")
rocket_trail(318, 738, 296, 480, 318, 292, "Rocket trail")
rocket_trail(700, 720, 664, 470, 636, 272, "Rocket trail R")

# a few drifting embers between the bursts
for i, (x, y, r, c) in enumerate([(262, 378, 3.4, GOLD_HI), (414, 208, 2.8, "#FFF0C8"),
                                  (564, 336, 3.0, SCARLET_HI), (700, 340, 2.6, GOLD_HI),
                                  (206, 316, 2.4, "#E8ECF8"), (612, 168, 2.2, "#FFF0C8"),
                                  (370, 452, 2.6, "#E8ECF8"), (640, 440, 2.8, GOLD_HI),
                                  (470, 380, 2.2, SCARLET_HI), (760, 470, 2.4, "#FFF0C8")]):
    inside(x, y, 14, f"ember {i}")
    d.shape("ellipse", f"Ember {i+1}", x=x - r, y=y - r, width=2 * r,
            height=2 * r, fill=c, opacity=78, stroke=NONE)

# --- the cockade ---------------------------------------------------------------
tail(488, 656, -1, "Tail L")
tail(512, 656, 1, "Tail R")
cockade(500, 572, 118)

# --- seal + caption -------------------------------------------------------------
seal_chop()
caption(p, "BASTILLE DAY", "JULY 14 · FÊTE NATIONALE",
        name_color="#F2ECD8", sub_color="#C9A46A",
        name_size=52, tracking_name=82, sub_size=21, tracking_sub=44,
        sub_font=SERIF)
p.finish(SLUG)
