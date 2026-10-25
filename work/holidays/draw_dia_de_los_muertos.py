#!/usr/bin/env python3
"""Día de los Muertos — Festival Seal V1R00.

A night ofrenda: a two-step altar under a violet field, banked with
cempasúchil marigolds and lit votives, papel picado swags overhead, and a
marigold-petal path spilling toward the viewer. Objects and settings only —
no skeletons. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth, blend)
from festival_kit import (seal_disc, glow, dust, ring_dots, caption, flame,
                          marigold_at, leaf_at)

SLUG = "dia-de-los-muertos-V1R00"
SS3 = "Source Sans 3"

VIOLET_HI = "#4A2058"
VIOLET_LO = "#14061E"
PAPEL = ["#E5488C", "#F28A2E", "#2FBFB4", "#E8C832", "#8E5AD8", "#4EA848"]
MARI_HI = "#F8CE84"
MARI = "#F2A33C"
MARI_LO = "#C9661A"
CANDLE = "#F2E4C4"
CANDLE_LO = "#C8A878"
ALT_HI = "#5A3060"
ALT_LO = "#2A1030"

p = Plate("Día de los Muertos — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#1E0A28", bottom="#08030C", glow=("#5A2E66", 18))
dust(d, n=44, r=404, colors=("#F6E3B8", "#E8A8D8"), seed=29,
     smin=0.8, smax=2.2, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, VIOLET_HI, VIOLET_LO, rim="#D8A85E", rim2="#3A1E40")
dust(d, n=56, r=392, colors=("#F6E3B8", "#F2A33C", "#E8A8D8"), seed=17,
     smin=1.0, smax=2.8, opmin=9, opmax=28, label="Disc dust")

# faint field guides + candle glow pooling over the altar
for rr, op in ((170, 11), (254, 9), (332, 8)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke="#D8A85E",
            strokeWidth=1.4, opacity=op)
ring_dots(d, r=398, n=56, size=2.6, color="#D8A85E", opacity=30)
glow(d, 500, 590, 340, "#F2A33C", a=22, label="Altar glow", squash=0.85)


# --- papel picado -------------------------------------------------------------
def papel_swag(x0, y0, x1, y1, sag, n, label, seed=1):
    """String of perforated paper flags hanging off a catenary-ish swag."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + sag * 2
    d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
           f"{label} cord", fill=NONE, stroke="#8A6A44", strokeWidth=2.2,
           opacity=80, cap="round")
    fw = 36
    for i in range(n):
        t = (i + 0.5) / n
        mt = 1 - t
        bx = mt * mt * x0 + 2 * mt * t * mx + t * t * x1
        by = mt * mt * y0 + 2 * mt * t * my + t * t * y1
        tx = 2 * mt * (mx - x0) + 2 * t * (x1 - mx)
        ty = 2 * mt * (my - y0) + 2 * t * (y1 - my)
        ang = math.degrees(math.atan2(ty, tx))
        col = PAPEL[(i + seed) % len(PAPEL)]
        # flag hangs from the cord, slightly rotated with the cord's slope
        rot = ang * 0.4
        a = math.radians(rot)
        ca, sa = math.cos(a), math.sin(a)
        # flag body: rectangle rotated about its top-centre anchor
        hw, hh = fw / 2, 21
        corners = []
        for dx, dy in ((-hw, 0), (hw, 0), (hw, hh), (-hw, hh)):
            corners.append((bx + dx * ca - dy * sa, by + dx * sa + dy * ca))
        d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in corners) + " Z",
               f"{label} flag {i+1}",
               fill=lin((bx, by), (bx, by + hh),
                        (0, blend(col, "#FFFFFF", 0.18)), (1, col)),
               stroke=blend(col, INK, 0.35), strokeWidth=1.2, opacity=94)
        # punched holes: a diamond + two dots showing the dark field through
        hx, hy = bx + 0 * ca - hh * 0.5 * sa, by + 0 * sa + hh * 0.5 * ca
        dd = [(0, 0), (-7, -4), (7, -4), (-7, 5), (7, 5)]
        for j, (ox, oy) in enumerate(dd):
            px = hx + ox * ca - oy * sa
            py = hy + ox * sa + oy * ca
            if j == 0:
                s = 3.4
                pts = [(px + 4.6 * ca, py + 4.6 * sa),
                       (px - 4.6 * sa, py + 4.6 * ca),
                       (px - 4.6 * ca, py - 4.6 * sa),
                       (px + 4.6 * sa, py - 4.6 * ca)]
                d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) +
                       " Z", f"{label} hole {i+1}-{j}",
                       fill=VIOLET_LO, opacity=88, stroke=NONE)
            else:
                d.shape("ellipse", f"{label} hole {i+1}-{j}", x=px - 1.9,
                        y=py - 1.9, width=3.8, height=3.8, fill=VIOLET_LO,
                        opacity=85, stroke=NONE)
        # scalloped bottom hem: two tiny notches
        for k, frac in enumerate((0.3, 0.7)):
            nx = bx + (frac - 0.5) * fw * ca - hh * sa
            ny = by + (frac - 0.5) * fw * sa + hh * ca
            d.shape("ellipse", f"{label} notch {i+1}-{k}", x=nx - 2.2,
                    y=ny - 1.4, width=4.4, height=2.8, fill=VIOLET_LO,
                    opacity=80, stroke=NONE)


papel_swag(232, 158, 768, 158, 46, 11, "Papel upper", seed=0)
papel_swag(168, 252, 832, 252, 52, 13, "Papel lower", seed=3)

# --- marigold arch over the altar (arco de flor) ------------------------------
arch_pts = [(264, 620), (500, 356), (736, 620)]
p0, pc, p1 = arch_pts
d.path(f"M{p0[0]},{p0[1]} Q{pc[0]},{pc[1]} {p1[0]},{p1[1]}", "Arch stem",
       fill=NONE, stroke="#5E3A18", strokeWidth=7, opacity=90,
       cap="round")
for i in range(19):
    t = i / 18
    mt = 1 - t
    bx = mt * mt * p0[0] + 2 * mt * t * pc[0] + t * t * p1[0]
    by = mt * mt * p0[1] + 2 * mt * t * pc[1] + t * t * p1[1]
    marigold_at(d, bx, by, 17, i, label="Arch marigold")
    # a leaf tucked under every other flower
    if i % 2:
        leaf_at(d, bx, by + 16, 90 + (i % 4 - 1.5) * 20, 26, 7,
                fill="#2F6B3A", stroke="#163A1E",
                label=f"Arch leaf {i}", vein=False)

# --- altar: two steps banked with marigolds ----------------------------------
AX, AY = 500, 780   # floor line of the bottom step

# petal path spilling toward the viewer from the altar base
import random
rnd = random.Random(5)
for i in range(22):
    t = rnd.random()
    px = 500 + rnd.uniform(-1, 1) * (26 + t * 150)
    py = 800 + t * 60
    s = 4 + t * 7
    leaf_at(d, px, py, rnd.uniform(0, 360), s * 1.8, s * 0.7,
            fill=[MARI, MARI_HI, MARI_LO][i % 3], stroke="#8A4010",
            label=f"Path petal {i+1}", vein=False)

# bottom step
d.path(f"M{AX - 250:.1f},{AY - 34:.1f} L{AX + 250:.1f},{AY - 34:.1f} "
       f"L{AX + 270:.1f},{AY + 20:.1f} L{AX - 270:.1f},{AY + 20:.1f} Z",
       "Altar step low",
       fill=lin((0, AY - 34), (0, AY + 20), (0, ALT_HI), (1, ALT_LO)),
       stroke=INK, strokeWidth=3.0)
d.shape("line", "Step edge low", x1=AX - 250, y1=AY - 34, x2=AX + 250,
        y2=AY - 34, stroke="#8A5E90", strokeWidth=2.4, opacity=60, cap="round")
# top step
d.path(f"M{AX - 176:.1f},{AY - 88:.1f} L{AX + 176:.1f},{AY - 88:.1f} "
       f"L{AX - 250:.1f},{AY - 34:.1f} L{AX + 250:.1f},{AY - 34:.1f} Z",
       "Altar step face",
       fill=lin((0, AY - 88), (0, AY - 34), (0, "#4A2650"), (1, "#2A1030")),
       stroke=INK, strokeWidth=2.4)
d.shape("line", "Step edge top", x1=AX - 176, y1=AY - 88, x2=AX + 176,
        y2=AY - 88, stroke="#9A6EA0", strokeWidth=2.4, opacity=65,
        cap="round")

# marigold bank along the step edges
bank = []
for i, x in enumerate(range(-240, 245, 32)):
    bank.append((AX + x, AY - 40 + abs(x) * 0.02, 15))
for i, x in enumerate(range(-164, 165, 30)):
    bank.append((AX + x, AY - 94, 14))
for i, (bx, by, br) in enumerate(bank):
    marigold_at(d, bx, by, br, i, label="Bank marigold")


# --- candles + offerings on the top step --------------------------------------
def votive(cx, base_y, w, h, label):
    """Glass votive candle: wax pillar, rim, flame, warm halo."""
    glow(d, cx, base_y - h - 30, w * 2.6, "#FFB85E", a=30,
         label=f"{label} halo")
    # glass sleeve
    d.path(f"M{cx - w/2:.1f},{base_y - h:.1f} L{cx - w/2:.1f},{base_y:.1f} "
           f"L{cx + w/2:.1f},{base_y:.1f} L{cx + w/2:.1f},{base_y - h:.1f} Z",
           f"{label} sleeve",
           fill=lin((cx - w / 2, base_y - h), (cx + w / 2, base_y),
                    (0, "#E8D8B8"), (0.5, "#8A6A4A"), (1, "#4A3020")),
           opacity=42, stroke="#2A1A12", strokeWidth=1.8)
    d.shape("ellipse", f"{label} rim", x=cx - w / 2, y=base_y - h - w * 0.16,
            width=w, height=w * 0.32, fill=NONE, stroke="#C8B088",
            strokeWidth=1.6, opacity=70)
    # wax inside
    d.shape("ellipse", f"{label} wax", x=cx - w * 0.36, y=base_y - h * 0.30,
            width=w * 0.72, height=w * 0.24,
            fill="#F6EACC", opacity=90, stroke=NONE)
    flame(d, cx, base_y - h - 2, h * 0.62, w * 0.42, label=f"{label} flame",
          smoke=0)


votive(AX - 116, AY - 92, 30, 108, "Candle L")
votive(AX - 44, AY - 92, 26, 76, "Candle lm")
votive(AX + 116, AY - 92, 30, 120, "Candle R")
votive(AX + 46, AY - 92, 24, 66, "Candle rm")

# pan de muerto — a round loaf with crosswise dough strips, centre step
LX, LY = AX, AY - 100
d.shape("ellipse", "Loaf shadow", x=LX - 36, y=LY + 12, width=72, height=10,
        fill=rad((0, INK, 44), (1, INK, 0)), stroke=NONE)
d.shape("ellipse", "Pan de muerto", x=LX - 33, y=LY - 22, width=66,
        height=47,
        fill=rad((0, "#E8BC78"), (0.6, "#C89048"), (1, "#8E5A24")),
        stroke="#5E3A14", strokeWidth=2.0)
# dough strips laid over the dome
for sgn, ang in ((-1, -32), (1, 32)):
    a = math.radians(ang)
    tx, ty = math.cos(a), math.sin(a)
    d.path(f"M{LX - tx * 26:.1f},{LY - 8 - ty * 26 * 0.5:.1f} "
           f"Q{LX:.1f},{LY - 20:.1f} "
           f"{LX + tx * 26:.1f},{LY - 8 + ty * 26 * 0.5:.1f}",
           f"Loaf strip {sgn}", fill=NONE, stroke="#F0D09A",
           strokeWidth=5.6, opacity=85, cap="round")
d.shape("ellipse", "Loaf knob", x=LX - 6, y=LY - 28, width=12, height=9,
        fill="#F0D09A", stroke="#8A5A20", strokeWidth=1.2)
for i, (sx, sy) in enumerate([(LX - 21, LY - 6), (LX + 19, LY - 3),
                              (LX - 8, LY + 9)]):
    d.shape("ellipse", f"Loaf sugar {i+1}", x=sx - 1.8, y=sy - 1.8,
            width=3.6, height=3.6, fill="#FFF4DC", opacity=80, stroke=NONE)

# a small water glass, right of the loaf
GX, GY = AX + 74, AY - 94
d.path(f"M{GX - 15:.1f},{GY - 36:.1f} L{GX - 13:.1f},{GY:.1f} "
       f"L{GX + 13:.1f},{GY:.1f} L{GX + 15:.1f},{GY - 36:.1f} Z", "Glass",
       fill=lin((GX - 15, GY - 36), (GX + 15, GY), (0, "#B8D8D8", 50),
                (1, "#5E8E92", 30)), stroke="#C8E4E4", strokeWidth=1.6,
       opacity=70)
d.shape("ellipse", "Glass water", x=GX - 12, y=GY - 21, width=24, height=9,
        fill="#8EC4C8", opacity=60, stroke=NONE)
d.path(f"M{GX - 9:.1f},{GY - 32:.1f} L{GX - 10:.1f},{GY - 6:.1f}",
       "Glass sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=1.8,
       opacity=40, cap="round")

# incense wisp rising off the top step
wisp_pts = [(AX - 160, AY - 110), (AX - 168, AY - 150), (AX - 152, AY - 190),
            (AX - 166, AY - 232), (AX - 156, AY - 268)]
d.path(smooth(wisp_pts), "Incense wisp", fill=NONE, stroke="#C8B8D8",
       strokeWidth=3.2, opacity=34, cap="round")
d.path(smooth([(x + 8, y - 6) for x, y in wisp_pts]), "Incense wisp 2",
       fill=NONE, stroke="#E8DCEE", strokeWidth=1.8, opacity=24,
       cap="round")

# --- scattered marigold petals on the field -----------------------------------
for i, (px, py, ang, s) in enumerate([(208, 420, -25, 11), (782, 402, 40, 10),
                                      (320, 488, 15, 9), (694, 500, -45, 11),
                                      (252, 600, 60, 8), (756, 616, -20, 9)]):
    leaf_at(d, px, py, ang, s * 1.9, s * 0.64, fill=MARI, stroke="#8A4010",
            label=f"Air petal {i+1}", vein=False)

# --- seal chop + caption ------------------------------------------------------
# square vermilion chop with a marigold mark, top right outside the disc
CHX, CHY, CS = 874, 98, 64
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CS,
        height=CS, radius=5, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Chop", x=CHX, y=CHY, width=CS, height=CS, radius=5,
        fill=lin((CHX, CHY), (CHX + CS, CHY + CS), (0, "#B23A30"),
                 (1, "#7E1F1B")), stroke="#5E1412", strokeWidth=2)
d.shape("rectangle", "Chop inner", x=CHX + 4, y=CHY + 4, width=CS - 8,
        height=CS - 8, radius=2, fill=NONE, stroke=GOLD_HI,
        strokeWidth=1.5, opacity=70)
marigold_at(d, CHX + CS / 2, CHY + CS / 2, 19, 0, label="Chop marigold")

caption(p, "DIA DE LOS MUERTOS",
        "NOV 1–2 · OFRENDA · MARIGOLDS & PAPEL PICADO",
        name_color="#F4E8D8", sub_color="#C8987A",
        name_size=40, tracking_name=46, sub_size=18, tracking_sub=40,
        sub_font=SS3)
p.finish(SLUG)
