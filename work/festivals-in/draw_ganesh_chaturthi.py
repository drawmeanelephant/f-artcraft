#!/usr/bin/env python3
"""Ganesh Chaturthi — Festival Seal V1R00.

The iconic-emblem plate: a dignified, symmetric gold Ganesha icon — halo,
tiered crown, fan ears, meditative closed eyes, trunk curling to a modak —
on deep saffron. Below the head, the offering row: modaks, one hibiscus,
durva grass. No scene, no caricature. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, DEVA, lin, rad, gold_lin, smooth, ribbon)
from festival_kit import seal_disc, glow, dust, ring_dots, deva_seal, caption

SLUG = "ganesh-chaturthi-V1R00"
SAFFRON = "#6E1E10"
SAFFRON_LO = "#20080A"
AURUM_HI = "#F6D88E"
AURUM = "#D8A44E"
AURUM_LO = "#8E5A1E"

p = Plate("Ganesh Chaturthi — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def aurum(y0, y1):
    return lin((0, y0), (0, y1), (0, AURUM_HI), (0.5, AURUM), (1, AURUM_LO))


def modak(cx, cy, s, label):
    """Sweet dumpling: pleated dome on a small base."""
    d.path(f"M{cx:.1f},{cy - s * 0.55:.1f} "
           f"C{cx + s * 0.55:.1f},{cy - s * 0.45:.1f} {cx + s * 0.62:.1f},{cy + s * 0.15:.1f} "
           f"{cx + s * 0.48:.1f},{cy + s * 0.42:.1f} "
           f"C{cx + s * 0.2:.1f},{cy + s * 0.56:.1f} {cx - s * 0.2:.1f},{cy + s * 0.56:.1f} "
           f"{cx - s * 0.48:.1f},{cy + s * 0.42:.1f} "
           f"C{cx - s * 0.62:.1f},{cy + s * 0.15:.1f} {cx - s * 0.55:.1f},{cy - s * 0.45:.1f} "
           f"{cx:.1f},{cy - s * 0.55:.1f} Z", f"{label} dome",
           fill=rad((0, "#F2C884"), (0.6, "#CE8E3E"), (1, "#8E5220")),
           stroke=INK, strokeWidth=2.2)
    for k in (-0.5, 0.0, 0.5):
        d.path(f"M{cx:.1f},{cy - s * 0.55:.1f} Q{cx + k * s * 0.5:.1f},{cy - s * 0.2:.1f} "
               f"{cx + k * s * 0.44:.1f},{cy + s * 0.38:.1f}", f"{label} pleat {k}",
               fill=NONE, stroke="#7A4418", strokeWidth=1.4, opacity=60)


def hibiscus(cx, cy, r, label):
    for i in range(5):
        a = math.radians(-90 + i * 72)
        px, py = cx + math.cos(a) * r * 0.52, cy + math.sin(a) * r * 0.52
        d.shape("ellipse", f"{label} petal {i+1}", x=px - r * 0.52,
                y=py - r * 0.44, width=r * 1.04, height=r * 0.88,
                fill=lin(0, cy - r, 0, cy + r, (0, "#E85A4A"), (1, "#A82418")),
                stroke="#6E1010", strokeWidth=1.6,
                rotation=round(math.degrees(a) + 90, 1))
    d.shape("ellipse", f"{label} throat", x=cx - r * 0.16, y=cy - r * 0.16,
            width=r * 0.32, height=r * 0.32, fill="#F6D488", stroke=NONE)
    d.shape("ellipse", f"{label} pistil", x=cx - 1.6, y=cy - 1.6, width=3.2,
            height=3.2, fill="#8E4A18", stroke=NONE)


# --- field ------------------------------------------------------------------
p.backdrop(top="#2A0C08", bottom="#0A0405", glow=("#9E3A18", 12))
dust(d, n=42, r=402, colors=("#F6D88E", "#F2A33C"), seed=31,
     smin=1.0, smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, SAFFRON, SAFFRON_LO, rim=GOLD, rim2="#3E120A")
dust(d, n=62, r=390, colors=("#F6D88E", "#F2A33C", "#E8C074"), seed=19,
     smin=1.0, smax=3.0, opmin=10, opmax=28, label="Disc dust")
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#F4CE8A"), (0.5, "#B8803E"),
                   (1, "#E8B870")), strokeWidth=4)
for i in range(40):
    a = math.radians(i * 9)
    x0, y0 = PCX + 150 * math.cos(a), PCY + 150 * math.sin(a)
    x1, y1 = PCX + 374 * math.cos(a), PCY + 374 * math.sin(a)
    d.shape("line", f"Field ray {i+1}", x1=round(x0, 1), y1=round(y0, 1),
            x2=round(x1, 1), y2=round(y1, 1), stroke=GOLD, strokeWidth=1.5,
            opacity=8, cap="round")
ring_dots(d, r=397, n=60, size=2.6, color=GOLD, opacity=30)
p.ring_ticks(n=24, color="#B8864E", r_in=378, r_out=396, width=2.2)

# --- the emblem ----------------------------------------------------------------
HX, HY, HR = 500, 386, 96
inside(HX - 190, HY - 96, 12, "ear L")
inside(HX + 190, HY - 96, 12, "ear R")
inside(HX, HY - HR - 74, 12, "crown tip")
inside(HX, HY + 168, 12, "offerings")
glow(d, HX, HY, 200, "#E8A44E", a=18, label="Icon glow")
# halo ring
d.shape("ellipse", "Halo", x=HX - 150, y=HY - 150, width=300, height=300,
        fill=NONE, stroke=gold_lin(HY - 150, HY + 150), strokeWidth=3.4,
        opacity=80)
d.shape("ellipse", "Halo inner", x=HX - 132, y=HY - 132, width=264, height=264,
        fill=NONE, stroke=GOLD, strokeWidth=1.2, opacity=44)
# ears (fans behind the head)
for sign, nm in ((-1, "L"), (1, "R")):
    ex, ey = HX + sign * 86, HY + 10
    d.shape("ellipse", f"Ear {nm}", x=ex - 44, y=ey - 66, width=88,
            height=132, fill=lin(0, ey - 66, 0, ey + 66, (0, AURUM_HI),
                                 (0.55, AURUM), (1, AURUM_LO)),
            stroke=INK, strokeWidth=3.4, rotation=sign * 26)
    d.shape("ellipse", f"Ear inner {nm}", x=ex - 26, y=ey - 46, width=52,
            height=92, fill=rad((0, "#B87E30", 38), (1, "#8E5A1E", 6)),
            stroke=NONE, rotation=sign * 26)
# head
d.shape("ellipse", "Head", x=HX - HR, y=HY - HR, width=HR * 2, height=HR * 2,
        fill=lin((HX - HR, HY - HR), (HX + HR * 0.7, HY + HR), (0, AURUM_HI),
                 (0.5, AURUM), (1, AURUM_LO)), stroke=INK, strokeWidth=3.6)
d.shape("ellipse", "Head sheen", x=HX - HR * 0.62, y=HY - HR * 0.82,
        width=HR * 0.8, height=HR * 0.6,
        fill=rad((0, "#FFF2C8", 30), (1, "#FFF2C8", 0)), stroke=NONE)
# crown: pointed mukut arch on a band, finial on the peak
base = HY - HR - 10
d.shape("rectangle", "Crown band", x=HX - 52, y=base, width=104, height=15,
        radius=7, fill=aurum(base, base + 17), stroke=INK, strokeWidth=2.4)
d.path(f"M{HX - 50},{base} Q{HX - 28},{base - 36} {HX},{base - 50} "
       f"Q{HX + 28},{base - 36} {HX + 50},{base} Z", "Crown fan",
       fill=lin(0, base - 52, 0, base, (0, AURUM_HI), (1, AURUM)),
       stroke=INK, strokeWidth=2.4)
for i in range(5):
    t = (i - 2) / 2
    px = HX + t * 26
    py = base - 14 - (14 - t * t * 13)
    d.shape("ellipse", f"Crown jewel {i+1}", x=px - 2.6, y=py - 2.6, width=5.2,
            height=5.2, fill="#E85A4A" if i == 2 else GOLD_HI, stroke=INK,
            strokeWidth=1)
d.shape("ellipse", "Crown finial", x=HX - 8, y=base - 66, width=16,
        height=16, fill=rad((0, "#F8E4A0"), (0.6, GOLD), (1, AURUM_LO)),
        stroke=INK, strokeWidth=2.2)
d.shape("ellipse", "Crown finial glint", x=HX - 4, y=base - 62, width=5,
        height=4.5, fill="#FFFFFF", opacity=60, stroke=NONE)
# meditative closed eyes + brows
for sign in (-1, 1):
    ex, ey = HX + sign * 38, HY - 6
    d.path(f"M{ex - 13:.1f},{ey - 2:.1f} Q{ex:.1f},{ey + 9:.1f} {ex + 13:.1f},{ey - 2:.1f}",
           f"Eye {sign}", fill=NONE, stroke="#4A2410", strokeWidth=4,
           cap="round")
    d.path(f"M{ex - 12:.1f},{ey - 16:.1f} Q{ex:.1f},{ey - 22:.1f} {ex + 12:.1f},{ey - 16:.1f}",
           f"Brow {sign}", fill=NONE, stroke="#8E5A1E", strokeWidth=2.6,
           opacity=70, cap="round")
# tilaka
d.shape("ellipse", "Tilaka", x=HX - 5, y=HY - 36, width=10, height=18,
        fill="#B83626", stroke=INK, strokeWidth=1.4)
# trunk: grows from the brow line, S down, tip curling up with a modak
SPINE = [(HX + 2, HY + 2), (HX + 1, HY + 16), (HX - 6, HY + 44),
         (HX - 17, HY + 74), (HX - 19, HY + 104), (HX - 10, HY + 128),
         (HX + 8, HY + 138), (HX + 26, HY + 130)]
WIDTHS = [8, 28, 24, 20, 16, 13, 10, 8]
td, _, _, _ = ribbon(SPINE, WIDTHS)
d.path(td, "Trunk", fill=lin(0, HY + 2, 0, HY + 138, (0, AURUM_HI),
                             (0.5, AURUM), (1, AURUM_LO)),
       stroke=INK, strokeWidth=3)
d.path(smooth(SPINE), "Trunk ridge", fill=NONE, stroke="#8E5A1E",
       strokeWidth=2, opacity=40, cap="round")
for i in (2, 4, 5):
    px, py = SPINE[i]
    nx = -1 if i < 4 else 1
    d.path(f"M{px + nx * 7:.1f},{py:.1f} Q{px:.1f},{py + 6:.1f} {px - nx * 7:.1f},{py:.1f}",
           f"Trunk crease {i}", fill=NONE, stroke="#8E5A1E", strokeWidth=1.8,
           opacity=45, cap="round")
modak(HX + 38, HY + 122, 25, "Trunk modak")

# --- offering row -----------------------------------------------------------------
PY = HY + 168
d.shape("ellipse", "Offering shadow", x=HX - 180, y=PY + 4, width=360,
        height=56, fill=rad((0, "#000000", 32), (1, "#000000", 0)), stroke=NONE)
d.path(f"M{HX - 168},{PY + 26} Q{HX - 60},{PY - 14} {HX + 90},{PY - 4} "
       f"Q{HX + 160},{PY + 2} {HX + 172},{PY + 20} "
       f"Q{HX + 60},{PY + 56} {HX - 90},{PY + 50} "
       f"Q{HX - 160},{PY + 46} {HX - 168},{PY + 26} Z", "Banana leaf",
       fill=lin(0, PY - 6, 0, PY + 50, (0, "#3E7A3E"), (1, "#1E4424")),
       stroke="#123018", strokeWidth=2.6)
d.path(f"M{HX - 150},{PY + 26} Q{HX},{PY + 6} {HX + 152},{PY + 20}",
       "Leaf vein", fill=NONE, stroke="#7AA85E", strokeWidth=1.6, opacity=50)
modak(HX - 104, PY + 6, 32, "Modak L")
modak(HX - 46, PY + 10, 28, "Modak C")
modak(HX + 8, PY + 6, 32, "Modak R")
hibiscus(HX + 76, PY + 10, 24, "Hibiscus")
for k in range(3):
    bx = HX + 120 + k * 9
    d.path(f"M{bx},{PY + 30} Q{bx - 4},{PY + 8} {bx - 12},{PY - 4} "
           f"M{bx},{PY + 30} Q{bx + 2},{PY + 6} {bx - 4},{PY - 10}",
           f"Durva blade {k+1}", fill=NONE, stroke="#4E8A46", strokeWidth=2.4,
           cap="round")

# --- sparks -------------------------------------------------------------------------
for i, (x, y, s) in enumerate([(330, 250, 2.4), (672, 262, 2.0), (360, 560, 2.0),
                               (654, 560, 2.2), (500, 176, 1.8)]):
    glow(d, x, y, 12, "#FFD98A", a=36, label=f"Spark glow {i+1}")
    d.shape("ellipse", f"Spark {i+1}", x=x - s, y=y - s, width=s * 2,
            height=s * 2, fill="#FFF2C4", opacity=85, stroke=NONE)

# --- seal + caption -------------------------------------------------------------------
deva_seal(d, "गणेश", cx=744, cy=213, s=64, size=23)
caption(p, "GANESH CHATURTHI", "गणेश चतुर्थी · BHADRAPADA · DAY 4",
        name_color="#FBE8CC", sub_color="#D8A468",
        name_size=48, tracking_name=40, sub_size=20, tracking_sub=40)
p.finish(SLUG)
