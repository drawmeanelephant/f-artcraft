#!/usr/bin/env python3
"""Onam — Festival Seal V1R00.

The harvest plate: a pookalam of flower petals in perspective fills the
disc's floor — rings of jasmine white, marigold orange, sunflower yellow
around a rose heart — under a marigold torana on the upper arc, two brass
lamps flanking. Verdant Kerala green field. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, DEVA, lin, rad, gold_lin, smooth, blend)
from festival_kit import seal_disc, glow, dust, ring_dots, lamp, garland, deva_seal, caption

SLUG = "onam-V1R00"
VERDANT = "#1E3A2A"
VERDANT_LO = "#0A1410"
JASMINE = "#FBEFD8"
MARIGOLD = "#F2A33C"
SUNFLOWER = "#F6C84A"
ROSE = "#C2426A"

p = Plate("Onam — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def pookalam(cx, cy, rx, label="Pookalam"):
    """Flower carpet in perspective: rings of petals + dot rings + heart."""
    k = 0.42
    rings = [(rx, 28, MARIGOLD, "#D9701C"),
             (rx * 0.78, 24, SUNFLOWER, "#E0A02C"),
             (rx * 0.56, 20, JASMINE, "#F2E2BC"),
             (rx * 0.34, 14, "#E88AA8", ROSE)]
    d.shape("ellipse", f"{label} base", x=cx - rx * 1.06, y=cy - rx * 1.06 * k,
            width=rx * 2.12, height=rx * 2.12 * k,
            fill=rad((0, "#3E6A4A", 90), (1, "#16281C", 80)), stroke=INK,
            strokeWidth=2.6, opacity=92)
    for ri, (rr, n, col, col2) in enumerate(rings):
        for i in range(n):
            a = 2 * math.pi * i / n + ri * 0.16
            px = cx + math.cos(a) * rr
            py = cy + math.sin(a) * rr * k
            pw = rr * 0.20 if i % 2 else rr * 0.22
            ph = pw * 0.55
            inside(px + pw / 2, py + ph / 2, 12, f"{label} petal {ri}-{i}")
            d.shape("ellipse", f"{label} petal {ri+1}-{i+1}", x=round(px - pw / 2, 1),
                    y=round(py - ph / 2, 1), width=round(pw, 1),
                    height=round(ph, 1), fill=col if i % 2 else col2,
                    stroke="#3A5A42" if ri == 2 else "#8A4A12", strokeWidth=1,
                    opacity=94, rotation=round(math.degrees(a) + 90, 1))
        # dot ring between flower rings
        dn = n * 2
        for i in range(dn):
            a = 2 * math.pi * i / dn + 0.1
            rr2 = rr * 0.885
            px = cx + math.cos(a) * rr2
            py = cy + math.sin(a) * rr2 * k
            sz = rr2 * 0.045
            d.shape("ellipse", f"{label} dot {ri}-{i}", x=round(px - sz, 1),
                    y=round(py - sz * k, 1), width=sz * 2, height=sz * 2 * k,
                    fill=GOLD_HI if i % 3 else "#E88AA8", opacity=85,
                    stroke=NONE)
    # heart
    hr = rx * 0.18
    d.shape("ellipse", f"{label} heart", x=cx - hr, y=cy - hr * k, width=hr * 2,
            height=hr * 2 * k, fill=rad((0, "#F8D8E0"), (0.6, ROSE), (1, "#8E2A4A")),
            stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"{label} heart core", x=cx - hr * 0.3, y=cy - hr * 0.3 * k,
            width=hr * 0.6, height=hr * 0.6 * k, fill=GOLD_HI, opacity=90,
            stroke=NONE)


# --- field ------------------------------------------------------------------
p.backdrop(top="#0F2018", bottom="#050A07", glow=("#2E5A3E", 12))
dust(d, n=40, r=402, colors=("#F6E3B8", "#F2A33C"), seed=27,
     smin=1.0, smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, VERDANT, VERDANT_LO, rim=GOLD, rim2="#12281A")
dust(d, n=58, r=390, colors=("#F6E3B8", "#F2A33C", "#E8C074"), seed=33,
     smin=1.0, smax=3.0, opmin=10, opmax=28, label="Disc dust")
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#E8D8A0"), (0.5, "#8E8A4E"),
                   (1, "#D8C888")), strokeWidth=4)
# faint kasavu rays
for i in range(36):
    a = math.radians(i * 10)
    x0, y0 = PCX + 140 * math.cos(a), PCY + 140 * math.sin(a)
    x1, y1 = PCX + 372 * math.cos(a), PCY + 372 * math.sin(a)
    d.shape("line", f"Field ray {i+1}", x1=round(x0, 1), y1=round(y0, 1),
            x2=round(x1, 1), y2=round(y1, 1), stroke=GOLD, strokeWidth=1.5,
            opacity=8, cap="round")
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=30)
p.ring_ticks(n=24, color="#A89858", r_in=378, r_out=396, width=2.2)

# --- torana on the upper arc ----------------------------------------------------
garland(d, r=366, a0=-148, a1=-32, swags=4, sag=24, flower_r=15)

# --- the pookalam -----------------------------------------------------------------
glow(d, 500, 636, 340, "#C2426A", a=14, label="Pookalam glow", squash=0.4)
glow(d, 500, 430, 240, "#E8C074", a=8, label="Hall glow", squash=0.9)
pookalam(500, 628, 262)

# --- flanking lamps ------------------------------------------------------------------
inside(258 + 34, 762 + 26, 12, "lamp L")
lamp(d, 258, 762, 62, label="Gate lamp L", flame_h=54, glow_a=24)
inside(742 - 34, 762 + 26, 12, "lamp R")
lamp(d, 742, 762, 62, label="Gate lamp R", flame_h=54, glow_a=24)

# --- fallen petals --------------------------------------------------------------------
for i, (x, y, ang, col) in enumerate([(348, 470, -30, JASMINE), (640, 452, 40, MARIGOLD),
                                      (300, 560, 15, SUNFLOWER), (688, 556, -18, "#E88AA8")]):
    d.shape("ellipse", f"Fallen petal {i+1}", x=x - 9, y=y - 5, width=18,
            height=10, fill=col, opacity=62, stroke=NONE, rotation=ang)

# --- sparks ------------------------------------------------------------------------------
for i, (x, y, s) in enumerate([(352, 262, 2.2), (648, 272, 2.0), (500, 330, 1.8),
                               (416, 438, 2.0), (588, 452, 2.2), (322, 386, 1.8),
                               (682, 400, 2.0)]):
    glow(d, x, y, 11, "#FFD98A", a=34, label=f"Spark glow {i+1}")
    d.shape("ellipse", f"Spark {i+1}", x=x - s, y=y - s, width=s * 2,
            height=s * 2, fill="#FFF2C4", opacity=85, stroke=NONE)

# --- seal + caption -------------------------------------------------------------------------
deva_seal(d, "ഓണം", cx=744, cy=213, s=70, size=21)
caption(p, "ONAM", "ഓണം · HARVEST OF KERALA · THIRUVONAM",
        name_color="#F2ECD4", sub_color="#C8B878",
        name_size=52, tracking_name=110, sub_size=20, tracking_sub=42)
p.finish(SLUG)
