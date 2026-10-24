#!/usr/bin/env python3
"""Qingming — Festival Seal V1R00.

Pure Brightness, the rain festival: no vermilion, no fireworks. A rain-washed
celadon disc, willow strands hanging from the rim, barn swallows returning,
thin rain over everything — and an oil-paper umbrella seen from above as the
hero, its round echoing the plate. One apricot branch in from the lower left
keeps a single warm note (the apricot-village line of the old poem). 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth, ribbon,
                          blossom)

SLUG = "qingming-V1R00"
CELADON = "#9FB896"
CELADON_HI = "#E9E4C8"
CELADON_LO = "#3E5A48"
PINE = "#2A4238"
APRICOT = "#E8B4C4"
APRICOT_HI = "#F6D2DC"
RAIN = "#B8C8C4"
BRASS = "#C0AA60"
SWALLOW_DARK = "#2E3844"
SWALLOW_BELLY = "#F0E8D8"

p = Plate("Qingming — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def poly(pts, label, **kw):
    return d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z",
                  label, **kw)


def rain(n=64, seed=9, x0=150, x1=850, y0=110, y1=740):
    """Thin slanted rain, kept strictly inside the disc."""
    s = seed
    kept = 0
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        x = x0 + (s % 10000) / 10000 * (x1 - x0)
        s = (1103515245 * s + 12345) % (2 ** 31)
        y = y0 + (s % 10000) / 10000 * (y1 - y0)
        s = (1103515245 * s + 12345) % (2 ** 31)
        L = 13 + (s % 1000) / 1000 * 22
        if math.hypot(x - PCX, y - PCY) > PR - 22:
            continue
        if math.hypot(x - 5 - PCX, y + L - PCY) > PR - 22:
            continue
        kept += 1
        d.shape("line", f"Rain {kept}", x1=round(x, 1), y1=round(y, 1),
                x2=round(x - 5, 1), y2=round(y + L, 1), stroke=RAIN,
                strokeWidth=1.5, opacity=20 + (s % 22), cap="round")


def ripple(x, y, r, op=30, label="Ripple"):
    """Rain ring on the ground, flattened by perspective."""
    for k, rr in enumerate((r, r * 0.62)):
        d.shape("ellipse", f"{label} ring {k+1}", x=x - rr, y=y - rr * 0.30,
                width=rr * 2, height=rr * 0.60, fill=NONE, stroke=RAIN,
                strokeWidth=1.6, opacity=max(10, op - k * 10))


def leaf_down(x, y, ang, h, w, fill, label, op=88):
    """Tapered willow leaf hanging at `ang` degrees (90 = straight down)."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = -sa, ca
    tip = (x + ca * h, y + sa * h)
    c1 = (x + ca * h * 0.30 + tx * w, y + sa * h * 0.30 + ty * w)
    c2 = (x + ca * h * 0.74 + tx * w * 0.55, y + sa * h * 0.74 + ty * w * 0.55)
    c3 = (x + ca * h * 0.74 - tx * w * 0.55, y + sa * h * 0.74 - ty * w * 0.55)
    c4 = (x + ca * h * 0.30 - tx * w, y + sa * h * 0.30 - ty * w)
    d.path(f"M{x:.1f},{y:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} "
           f"{tip[0]:.1f},{tip[1]:.1f} C{c3[0]:.1f},{c3[1]:.1f} "
           f"{c4[0]:.1f},{c4[1]:.1f} {x:.1f},{y:.1f} Z", label,
           fill=fill, opacity=op, stroke="#3E5A44", strokeWidth=1.1)


def willow_cluster(x, y, twig_dx, label, strands=3, col="#8FB88E", op=88):
    """A willow twig reaching in from behind the rim, with drooping strands."""
    x1, y1 = x + twig_dx, y + 14
    d.path(f"M{x:.1f},{y:.1f} Q{(x + x1) / 2:.1f},{y - 10:.1f} {x1:.1f},{y1:.1f}",
           f"{label} twig", fill=NONE, stroke="#3A2E1C", strokeWidth=3.2,
           cap="round")
    for k in range(strands):
        sx = x1 - (k - (strands - 1) / 2) * 26
        sy = y1 + 4 + abs(k - 1) * 6
        length = 96 + (k % 3) * 30
        sway = (-1 if k % 2 else 1) * (10 + k * 6)
        pts = [(sx, sy), (sx + sway * 0.4, sy + length * 0.38),
               (sx + sway, sy + length * 0.72), (sx + sway * 0.7, sy + length)]
        d.path(smooth(pts), f"{label} strand {k+1}", fill=NONE,
               stroke="#5E7A50", strokeWidth=2.0, opacity=70, cap="round")
        nl = 6 + k % 2
        for j in range(nl):
            t = (j + 0.7) / (nl + 0.6)
            mt = 1 - t
            bx = (mt**3 * pts[0][0] + 3 * mt * mt * t * pts[1][0]
                  + 3 * mt * t * t * pts[2][0] + t**3 * pts[3][0])
            by = (mt**3 * pts[0][1] + 3 * mt * mt * t * pts[1][1]
                  + 3 * mt * t * t * pts[2][1] + t**3 * pts[3][1])
            ang = 90 + (34 if j % 2 else -34) + sway
            leaf_down(bx, by, ang, 17 + (j % 3) * 5, 3.4, col,
                      f"{label} leaf {k+1}-{j+1}", op=op - (k * 6))


def barn_swallow(x, y, s, flip=1, label="Swallow"):
    """Barn swallow in flight: dark coat, ivory belly, rust throat, forked tail."""
    f = flip
    # forked tail — two slim prongs
    poly([(x - f * 15 * s, y + 1 * s), (x - f * 36 * s, y - 9 * s),
          (x - f * 23 * s, y + 1 * s), (x - f * 38 * s, y + 10 * s)],
         f"{label} tail", fill=SWALLOW_DARK, stroke=NONE)
    # body: head to tail base
    d.path(f"M{x + f*22*s:.1f},{y - 4*s:.1f} "
           f"C{x + f*20*s:.1f},{y - 9*s:.1f} {x + f*6*s:.1f},{y - 10*s:.1f} "
           f"{x - f*8*s:.1f},{y - 6*s:.1f} C{x - f*17*s:.1f},{y - 4*s:.1f} "
           f"{x - f*19*s:.1f},{y + 1*s:.1f} {x - f*16*s:.1f},{y + 3*s:.1f} "
           f"C{x - f*4*s:.1f},{y + 8*s:.1f} {x + f*12*s:.1f},{y + 6*s:.1f} "
           f"{x + f*20*s:.1f},{y + 1*s:.1f} "
           f"C{x + f*23*s:.1f},{y - 1*s:.1f} {x + f*23*s:.1f},{y - 2*s:.1f} "
           f"{x + f*22*s:.1f},{y - 4*s:.1f} Z", f"{label} body",
           fill=lin((x - f * 20 * s, y), (x + f * 22 * s, y),
                    (0, "#232B36"), (1, "#3E4A58")), stroke=INK, strokeWidth=1.6)
    # upper wing, long and slim, swept back
    d.path(f"M{x + f*8*s:.1f},{y - 4*s:.1f} "
           f"C{x - f*4*s:.1f},{y - 12*s:.1f} {x - f*20*s:.1f},{y - 19*s:.1f} "
           f"{x - f*34*s:.1f},{y - 20*s:.1f} C{x - f*24*s:.1f},{y - 11*s:.1f} "
           f"{x - f*14*s:.1f},{y - 4*s:.1f} {x - f*6*s:.1f},{y - 1*s:.1f} Z",
           f"{label} wing", fill="#1E2630", stroke=NONE)
    # lower wing hint, tight against the body
    d.path(f"M{x + f*4*s:.1f},{y + 2*s:.1f} C{x - f*4*s:.1f},{y + 8*s:.1f} "
           f"{x - f*14*s:.1f},{y + 11*s:.1f} {x - f*22*s:.1f},{y + 10*s:.1f} "
           f"C{x - f*14*s:.1f},{y + 6*s:.1f} {x - f*6*s:.1f},{y + 3*s:.1f} "
           f"{x - f*0*s:.1f},{y + 1*s:.1f} Z", f"{label} wing low",
           fill="#394452", opacity=74, stroke=NONE)
    # ivory belly
    d.path(f"M{x - f*14*s:.1f},{y + 2*s:.1f} C{x - f*8*s:.1f},{y + 6*s:.1f} "
           f"{x + f*6*s:.1f},{y + 5*s:.1f} {x + f*16*s:.1f},{y - 1*s:.1f} "
           f"C{x + f*8*s:.1f},{y + 2*s:.1f} {x - f*4*s:.1f},{y + 2*s:.1f} "
           f"{x - f*14*s:.1f},{y + 2*s:.1f} Z", f"{label} belly",
           fill=SWALLOW_BELLY, opacity=92, stroke=NONE)
    # rust throat + head glint + eye
    d.shape("ellipse", f"{label} throat", x=x + f * 13 * s - 3 * s,
            y=y - 3 * s, width=7 * s, height=5 * s, fill="#B45A3A",
            stroke=NONE, rotation=-14 * f)
    d.shape("ellipse", f"{label} eye", x=x + f * 17 * s - 1.1 * s,
            y=y - 6.5 * s, width=2.2 * s, height=2.2 * s, fill="#F6EFDC",
            opacity=90, stroke=NONE)


# --- field ------------------------------------------------------------------
p.backdrop(top="#1C2420", bottom="#070A09", glow=("#3E5A48", 10))
p.disc(PINE, "#0B1410", rim=BRASS, rim2="#22301A")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.58, "#000000", 0), (1, "#000000", 64)),
        stroke=NONE)
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#D8D0A8"), (0.5, "#8E8A56"),
                   (1, "#C8C088")), strokeWidth=4)
d.shape("ellipse", "Rain aura", x=140, y=60, width=720, height=640,
        fill=rad((0, "#5E7A62", 16), (0.55, "#3E5A48", 7), (1, "#3E5A48", 0)),
        stroke=NONE)
p.ring_ticks(n=24, color="#8E9A6E", r_in=378, r_out=396, width=2.2)

# --- mist bands -------------------------------------------------------------
for cy, w, h, op in ((660, 620, 100, 6), (470, 520, 80, 5)):
    d.shape("ellipse", f"Mist {cy}", x=PCX - w / 2, y=cy - h / 2, width=w,
            height=h, fill=rad((0, CELADON_HI, op), (0.7, CELADON_HI, op * 0.4),
                               (1, CELADON_HI, 0)), stroke=NONE)

# --- rain --------------------------------------------------------------------
rain(n=92, seed=13)
ripple(360, 752, 40, op=26, label="Ripple L")
ripple(636, 770, 32, op=24, label="Ripple R")
ripple(288, 688, 22, op=18, label="Ripple far")
ripple(708, 648, 20, op=16, label="Ripple far R")

# --- oil-paper umbrella, seen from above -------------------------------------
UCX, UCY, UR = 500, 545, 168
inside(UCX - UR - 30, UCY, 12, "umbrella L")
inside(UCX + UR + 30, UCY, 12, "umbrella R")
inside(UCX, UCY + UR + 30, 12, "umbrella B")
inside(UCX, UCY - UR - 30, 12, "umbrella T")
# ground shadow + wet sheen under the canopy
d.shape("ellipse", "Umbrella shadow", x=UCX - UR * 1.12, y=UCY + UR * 0.66,
        width=UR * 2.24, height=UR * 0.52,
        fill=rad((0, "#000000", 42), (0.6, "#000000", 18), (1, "#000000", 0)),
        stroke=NONE)
d.shape("ellipse", "Puddle sheen", x=UCX - UR * 1.28, y=UCY + UR * 0.98,
        width=UR * 2.56, height=UR * 0.44,
        fill=rad((0, CELADON_HI, 12), (1, CELADON_HI, 0)), stroke=NONE)
# scalloped canopy: shallow outward bumps from notch to notch, then inner disc
NB = 18
bump_r = 34.0
notch = []
for i in range(NB):
    a = math.radians(-100 + i * 20)
    notch.append((UCX + UR * math.cos(a), UCY + UR * math.sin(a)))
seg = 2 * UR * math.sin(math.pi / NB)
sc = f"M{notch[0][0]:.1f},{notch[0][1]:.1f} "
for i in range(NB):
    nx, ny = notch[(i + 1) % NB]
    sc += f"A{bump_r:.1f},{bump_r:.1f} 0 0 1 {nx:.1f},{ny:.1f} "
d.path(sc + "Z", "Umbrella canopy edge",
       fill=lin((UCX - UR, UCY - UR), (UCX + UR * 0.7, UCY + UR),
                (0, "#D8D4B0"), (0.5, CELADON), (1, "#5E7856")),
       stroke=INK, strokeWidth=3.4)
RI = UR - 7
d.shape("ellipse", "Umbrella canopy", x=UCX - RI, y=UCY - RI, width=RI * 2,
        height=RI * 2,
        fill=lin((UCX - RI, UCY - RI), (UCX + RI * 0.7, UCY + RI),
                 (0, CELADON_HI), (0.42, CELADON), (1, CELADON_LO)),
        stroke=NONE)
d.shape("ellipse", "Umbrella dish", x=UCX - RI, y=UCY - RI, width=RI * 2,
        height=RI * 2,
        fill=rad((0, "#000000", 0), (0.72, "#1E3428", 0), (1, "#1E3428", 36)),
        stroke=NONE)
# alternating paper panels, light falling from the upper left
for i in range(0, NB, 2):
    a0 = math.radians(-90 + i * (360 / NB))
    a1 = math.radians(-90 + (i + 1) * (360 / NB))
    x0, y0 = UCX + RI * math.cos(a0), UCY + RI * math.sin(a0)
    x1, y1 = UCX + RI * math.cos(a1), UCY + RI * math.sin(a1)
    tilt = 0.5 - (math.degrees(a0) % 360) / 720.0
    d.path(f"M{UCX:.1f},{UCY:.1f} L{x0:.1f},{y0:.1f} "
           f"A{RI:.1f},{RI:.1f} 0 0 1 {x1:.1f},{y1:.1f} Z",
           f"Umbrella panel {i+1}", fill=CELADON_HI,
           opacity=round(5 + tilt * 11), stroke=NONE)
# sheen
d.shape("ellipse", "Umbrella sheen", x=UCX - UR * 0.64, y=UCY - UR * 0.80,
        width=UR * 0.88, height=UR * 0.62,
        fill=rad((0, "#FFFFFF", 24), (0.6, "#FFFFFF", 8), (1, "#FFFFFF", 0)),
        stroke=NONE)
# ribs to every notch
for i in range(NB):
    a = math.radians(-90 + i * (360 / NB))
    x1, y1 = UCX + RI * 0.985 * math.cos(a), UCY + RI * 0.985 * math.sin(a)
    d.shape("line", f"Umbrella rib {i+1}", x1=round(UCX + 9 * math.cos(a), 1),
            y1=round(UCY + 9 * math.sin(a), 1), x2=round(x1, 1), y2=round(y1, 1),
            stroke="#44523C", strokeWidth=2.4, opacity=64, cap="round")
    xg, yg = UCX + RI * 0.70 * math.cos(a), UCY + RI * 0.70 * math.sin(a)
    d.shape("line", f"Umbrella rib glint {i+1}",
            x1=round(UCX + 9 * math.cos(a), 1), y1=round(UCY + 9 * math.sin(a), 1),
            x2=round(xg, 1), y2=round(yg, 1), stroke="#F2EFD8", strokeWidth=1.0,
            opacity=32, cap="round")
# bamboo stretcher ring
d.shape("ellipse", "Umbrella stretcher", x=UCX - UR * 0.70, y=UCY - UR * 0.70,
        width=UR * 1.40, height=UR * 1.40, fill=NONE, stroke="#8A6A34",
        strokeWidth=2.6, opacity=55)
d.shape("ellipse", "Umbrella stretcher light", x=UCX - UR * 0.68, y=UCY - UR * 0.72,
        width=UR * 1.36, height=UR * 1.36, fill=NONE, stroke="#D8B878",
        strokeWidth=1.0, opacity=34)
# bamboo finial
d.shape("ellipse", "Umbrella finial shadow", x=UCX - 15, y=UCY - 9,
        width=34, height=28, fill="#000000", opacity=25, stroke=NONE)
d.shape("ellipse", "Umbrella finial", x=UCX - 15, y=UCY - 16, width=30,
        height=30, fill=rad((0, "#F6EFD4"), (0.6, "#C8A860"), (1, "#7A5A28")),
        stroke=INK, strokeWidth=2.2)
d.shape("ellipse", "Umbrella finial cap", x=UCX - 8, y=UCY - 27, width=16,
        height=12, fill=gold_lin(UCY - 27, UCY - 15), stroke=INK, strokeWidth=1.6)
d.shape("ellipse", "Umbrella finial glint", x=UCX - 9, y=UCY - 12, width=9,
        height=6, fill="#FFFFFF", opacity=45, stroke=NONE, rotation=-18)

# --- willow (anchors tucked behind the rim line, r≈404) ----------------------
AX, AY = PCX + 404 * math.cos(math.radians(-122)), PCY + 404 * math.sin(math.radians(-122))
willow_cluster(AX, AY, 72, "Willow A", strands=3, col="#9CC492", op=88)
BX, BY = PCX + 404 * math.cos(math.radians(-56)), PCY + 404 * math.sin(math.radians(-56))
willow_cluster(BX, BY, -64, "Willow B", strands=3, col="#8CB482", op=84)
CX, CY = PCX + 404 * math.cos(math.radians(-150)), PCY + 404 * math.sin(math.radians(-150))
willow_cluster(CX, CY, 58, "Willow C", strands=2, col="#7EA876", op=78)

# --- swallows -------------------------------------------------------------------
barn_swallow(612, 302, 1.25, flip=1, label="Swallow 1")
barn_swallow(690, 252, 0.9, flip=-1, label="Swallow 2")
barn_swallow(548, 246, 0.7, flip=1, label="Swallow 3")

# --- apricot branch -------------------------------------------------------------
SPINE = [(214, 738), (248, 700), (236, 652), (270, 606), (258, 566), (286, 532)]
WIDTHS = [15, 12.5, 10.5, 8.5, 7, 4.5]
bd, _, _, _ = ribbon(SPINE, WIDTHS)
d.path(bd, "Apricot branch", fill=lin((214, 738), (286, 532), (0, "#5E4636"),
                                      (0.55, "#3A2A20"), (1, "#241A14")),
       stroke="#140E0C", strokeWidth=3)
d.path(smooth(SPINE), "Apricot branch light", fill=NONE, stroke="#8A6A50",
       strokeWidth=2.2, opacity=38, cap="round")
TWIGS = [((248, 700), (292, 682)), ((236, 652), (196, 630)),
         ((270, 606), (312, 588)), ((258, 566), (222, 548)),
         ((286, 532), (318, 520)), ((230, 676), (206, 662))]
for i, (a, b) in enumerate(TWIGS):
    d.path(f"M{a[0]},{a[1]} Q{(a[0]+b[0])/2:.1f},{(a[1]+b[1])/2-6:.1f} {b[0]},{b[1]}",
           f"Apricot twig {i+1}", fill=NONE, stroke="#4A382A", strokeWidth=3.6,
           cap="round")
BLOSSOMS = [(292, 680, 20, -70), (196, 628, 17, 30), (312, 586, 16, -20),
            (222, 546, 15, 80), (318, 518, 14, 40), (232, 674, 11, 10),
            (268, 634, 10, -50), (296, 560, 9, 65)]
for i, (bx, by, br, rot) in enumerate(BLOSSOMS):
    inside(bx, by, br + 8, f"blossom {i}")
    blossom(d, bx, by, br, label=f"Apricot blossom {i+1}", fill=APRICOT,
            core="#B8627A", rot=rot, opacity=93)
for i, (bx, by, br, rot) in enumerate([(212, 606, 8, 30), (330, 548, 7, -20),
                                       (250, 690, 6, 70)]):
    d.shape("ellipse", f"Apricot bud {i+1}", x=bx - br * 0.55, y=by - br,
            width=br * 1.1, height=br * 1.9, fill="#C8788E",
            stroke="#6E3040", strokeWidth=1.2, rotation=rot, opacity=92)

# --- drifting petals in the rain ------------------------------------------------
PETALS = [(398, 356, 8, -25), (612, 398, 7, 40), (348, 470, 6, 15),
          (662, 520, 6, -55), (452, 302, 5, 10), (568, 682, 7, -35)]
for i, (x, y, r, rot) in enumerate(PETALS):
    d.shape("ellipse", f"Drifting petal {i+1}", x=x - r, y=y - r * 0.6,
            width=2 * r, height=r * 1.2, fill=APRICOT, opacity=42,
            stroke=NONE, rotation=rot)

# --- seal + caption --------------------------------------------------------------
CHX, CHY, CHW, CHH = 714, 148, 50, 136
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("清明", x=CHX, y=CHY, w=CHW, h=CHH, size=27)

p.caption("QINGMING", "清明 · PURE BRIGHTNESS · 4 APRIL",
          name_color="#EDEBDC", sub_color="#A8B898",
          name_size=52, sub_size=20, tracking_name=96, tracking_sub=120)
p.finish(SLUG)
