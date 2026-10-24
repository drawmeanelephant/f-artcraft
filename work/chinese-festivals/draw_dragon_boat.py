#!/usr/bin/env python3
"""Dragon Boat Festival — 端午 · River Rites. Festival Seal V1R00.

A dragon-headed boat with oars cutting the wave, zongzi in the foreground,
a tied bundle of calamus and mugwort at the bank, late-spring sun.
1000x1000, disc centre (500,460) r420. Gradients and translucent
shading throughout; warm ink outlines, never pure black.
"""
import sys
import os
import math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from orient.plate import (Plate, NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth, spiral,
                          cloud, PCX, PCY, PR)  # noqa: E402

# --- palette -----------------------------------------------------------------
SEA_HI = "#A6E0D4"
SEA = "#2F8C8C"
SEA_MID = "#175E68"
SEA_DEEP = "#082E3A"
LAC_HI = "#E4694C"
LAC = "#B23627"
LAC_LO = "#7C1B16"
LAC_DEEP = "#4C0D0C"
LEAF_HI = "#8FB86A"
LEAF = "#4E7A3E"
LEAF_DEEP = "#16281A"
RICE = "#F6E9C8"

# --- helpers -----------------------------------------------------------------
def plate_disc(p, top, bottom, rim="#D0A45A", rim2="#4A3212", shadow_r=426):
    """The house disc, with the drop shadow kept inside the rim-check band."""
    d = p.d
    sr = shadow_r
    d.shape("ellipse", "Plate shadow", x=PCX - sr, y=PCY - sr, width=2 * sr,
            height=2 * sr, fill="#000000", opacity=30, stroke=NONE)
    d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
            fill=lin((0, 40), (0, 880), (0, top), (1, bottom)),
            stroke=rim2, strokeWidth=10)
    d.shape("ellipse", "Plate rim", x=86, y=46, width=828, height=828,
            fill=NONE, stroke=rim, strokeWidth=4)


def rim_pass(p, rim, rim2):
    """Redraw the rim over full-bleed art so the edge stays crisp."""
    d = p.d
    d.shape("ellipse", "Plate edge", x=80, y=40, width=840, height=840,
            fill=NONE, stroke=rim2, strokeWidth=10)
    d.shape("ellipse", "Plate rim", x=86, y=46, width=828, height=828,
            fill=NONE, stroke=rim, strokeWidth=4)


def chord(y, r=420.0):
    """Closed path for the part of the disc below horizontal chord y."""
    half = math.sqrt(max(r * r - (y - PCY) ** 2, 0.0))
    x0, x1 = PCX - half, PCX + half
    return (f"M{x0:.1f},{y:.1f} L{x1:.1f},{y:.1f} "
            f"A{r:.0f},{r:.0f} 0 0 1 {x0:.1f},{y:.1f} Z")


def wave_pts(y, amp, x0, x1, k=3, phase=0.0, n=44):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t,
                    y + amp * math.sin(2 * math.pi * k * t + phase * math.pi)))
    return pts


def band(y0, y1, amp, x0, x1, k=3, phase=0.0):
    top = wave_pts(y0, amp, x0, x1, k, phase)
    bot = wave_pts(y1, amp, x0, x1, k, phase + 0.7)
    return smooth(top + bot[::-1], closed=True)


def zongzi(d, cx, cy, w, h, rot, label, opened=False):
    """One wrapped rice dumpling: leaf body, bamboo string, optional opened corner."""
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)

    def P(x, y):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)

    top = P(0, -h * 0.52)
    pts = [P(0, -h * 0.52), P(w * 0.30, -h * 0.30), P(w * 0.48, h * 0.10),
           P(w * 0.40, h * 0.34), P(w * 0.10, h * 0.50), P(-w * 0.24, h * 0.46),
           P(-w * 0.46, h * 0.20), P(-w * 0.36, -h * 0.22), P(-w * 0.20, -h * 0.44)]
    body = smooth(pts, closed=True)
    d.path(body, label, fill=lin(0, cy - h * 0.5, 0, cy + h * 0.5,
                                 (0, LEAF_HI), (0.42, LEAF), (1, LEAF_DEEP)),
           stroke=INK, strokeWidth=3.2)
    d.path(smooth([P(-w * 0.08, -h * 0.42), P(-w * 0.22, -h * 0.10),
                   P(-w * 0.18, h * 0.20), P(-w * 0.10, h * 0.44)]),
           f"{label} seam", fill=NONE, stroke=LEAF_DEEP, strokeWidth=2, opacity=55, cap="round")
    d.path(smooth([P(-w * 0.26, -h * 0.30), P(-w * 0.32, -h * 0.04),
                   P(-w * 0.27, h * 0.18), P(-w * 0.17, h * 0.36)]),
           f"{label} lit fold", fill=NONE, stroke="#D8E8A8", strokeWidth=3.2,
           opacity=38, cap="round")
    for i, (ya, yb) in enumerate([(-0.26, 0.16), (-0.08, 0.30)]):
        pa, pb = P(w * 0.08, h * ya), P(w * 0.30, h * yb)
        d.path(f"M{pa[0]:.1f},{pa[1]:.1f} Q{(pa[0] + pb[0]) / 2 + 5:.1f},"
               f"{(pa[1] + pb[1]) / 2:.1f} {pb[0]:.1f},{pb[1]:.1f}",
               f"{label} vein {i+1}", fill=NONE, stroke="#BCD48E", strokeWidth=1.4,
               opacity=35, cap="round")
    for i, yy in enumerate((-0.12, 0.16)):
        pa, pb = P(-w * 0.47, h * yy - 2), P(w * 0.47, h * yy + 4)
        d.path(f"M{pa[0]:.1f},{pa[1]:.1f} Q{cx:.1f},{cy + h * yy + 12:.1f} "
               f"{pb[0]:.1f},{pb[1]:.1f}", f"{label} string {i+1}", fill=NONE,
               stroke="#E8D39A", strokeWidth=3, opacity=85, cap="round")
    kx, ky = P(w * 0.20, h * 0.02)
    d.shape("ellipse", f"{label} knot", x=kx - 6, y=ky - 5, width=12, height=10,
            fill=GOLD, stroke=INK, strokeWidth=1.6, rotation=rot)
    if opened:
        o = P(w * 0.02, -h * 0.30)
        d.path(f"M{o[0]:.1f},{o[1] - h * 0.10:.1f} L{o[0] + w * 0.19:.1f},{o[1] + h * 0.04:.1f} "
               f"L{o[0] - w * 0.04:.1f},{o[1] + h * 0.13:.1f} Z", f"{label} rice corner",
               fill=lin(0, o[1] - h * 0.1, 0, o[1] + h * 0.14, (0, "#FFF8E4"), (1, "#E2C896")),
               stroke=INK, strokeWidth=2)
        for gi, (gx, gy) in enumerate([(-0.05, -0.03), (0.05, 0.03), (0.0, 0.08)]):
            px, py = P(w * (0.02 + gx), -h * (0.30 - gy))
            d.shape("ellipse", f"{label} grain {gi+1}", x=px - 2.2, y=py - 1.6,
                    width=4.4, height=3.2, fill="#FFFDF2", opacity=85, stroke=NONE)


def ribbon(spine, widths):
    """Closed path around a spine, width per point (local copy of plate.ribbon)."""
    n = len(spine)
    L, R, norms = [], [], []
    for i, (x, y) in enumerate(spine):
        ax, ay = spine[max(i - 1, 0)]
        bx, by = spine[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        norms.append((nx, ny, w))
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " A%.1f,%.1f 0 0 0 %.1f,%.1f " % (norms[-1][2], norms[-1][2], R[-1][0], R[-1][1])
    dd += " ".join("L%.1f,%.1f" % p for p in reversed(R[:-1])) + " Z"
    return dd, L, R, norms


def calamus_blade(d, bx, by, tipx, tipy, bend, w0, label):
    spine = []
    n = 6
    for i in range(n + 1):
        t = i / n
        x = bx + (tipx - bx) * t + bend * math.sin(math.pi * t) * 0.5
        y = by + (tipy - by) * t
        spine.append((x, y))
    widths = [w0 * (1 - 0.88 * (i / n) ** 1.3) + 0.8 for i in range(n + 1)]
    dpath, L, R, _ = ribbon(spine, widths)
    d.path(dpath, label, fill=lin(0, by, 0, tipy,
                                  (0, "#8EA84C"), (0.45, "#4C6B34"), (1, "#1E3220")),
           stroke=INK, strokeWidth=2)
    mid = [((L[i][0] + R[i][0]) / 2, (L[i][1] + R[i][1]) / 2) for i in range(len(L))]
    d.path(smooth(mid), f"{label} rib", fill=NONE, stroke="#C6D692",
           strokeWidth=1.5, opacity=40, cap="round")


# --- plate -------------------------------------------------------------------
p = Plate("Dragon Boat — Festival Seal", 1000, 1000)
d = p.d

p.backdrop(top="#0B2028", bottom="#04080B", glow=("#1E6B72", 10))
p.stars(n=24, color="#CFE8E2", seed=41, maxr=1.5)
plate_disc(p, "#2A7076", "#072730")

# --- sky: sun and cloud bands ------------------------------------------------
d.shape("ellipse", "Sun halo", x=170, y=86, width=280, height=280,
        fill=rad((0, "#FFD98C", 22), (0.55, "#FFC46B", 9), (1, "#FFC46B", 0)),
        stroke=NONE)
d.shape("ellipse", "Sun", x=242, y=158, width=118, height=118,
        fill=rad((0, "#FFF7DC"), (0.45, "#F8DE9E"), (0.8, "#E8BE72"), (1, "#C08E44")),
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Sun top light", x=258, y=170, width=62, height=40,
        fill=rad((0, "#FFFFFF", 55), (1, "#FFFFFF", 0)), stroke=NONE, rotation=-24)

for i, (yy, op) in enumerate([(322, 20), (352, 14)]):
    d.path(smooth(wave_pts(yy, 5, 140, 690, 3, phase=i * 0.5)),
           f"Cloud streak {i+1}", fill=NONE, stroke="#DCEFE6",
           strokeWidth=3.4, opacity=op, cap="round")

cloud(d, 176, 300, 0.78, "Cloud L", fill="#CFE9E0", opacity=13)
cloud(d, 690, 236, 0.62, "Cloud R", fill="#CFE9E0", opacity=10)

# --- far bank + pagoda -------------------------------------------------------
d.path(smooth([(104, 590), (170, 574), (236, 582), (300, 566), (368, 580),
               (430, 572), (500, 582), (566, 570), (640, 580), (716, 566),
               (792, 580), (852, 570), (900, 582), (900, 604), (104, 604)],
              closed=True),
       "Far bank", fill=lin(0, 560, 0, 604, (0, "#2E7278"), (1, "#174E58")),
       opacity=62, stroke=NONE)
d.path(smooth(wave_pts(592, 2.5, 108, 896, 4)), "Bank light", fill=NONE,
       stroke="#9AD3C8", strokeWidth=2.2, opacity=24, cap="round")

# pagoda silhouette on the far bank
PX, PY = 646, 590
for i, (w, h, y) in enumerate([(34, 12, 0), (27, 10, -15), (20, 9, -28)]):
    d.shape("rectangle", f"Pagoda eave {i+1}", x=PX - w, y=PY + y - h,
            width=2 * w, height=h, radius=2,
            fill=lin(0, PY + y - h, 0, PY + y, (0, "#3E7C80"), (1, "#1C4A52")),
            stroke=INK, strokeWidth=1.6, opacity=90)
    d.shape("rectangle", f"Pagoda body {i+1}", x=PX - w * 0.52, y=PY + y,
            width=w * 1.04, height=8, fill="#255C64", stroke=INK,
            strokeWidth=1.4, opacity=90)
d.path(f"M{PX},{PY - 40} L{PX},{PY - 58}", "Pagoda spire", fill=NONE,
       stroke=INK, strokeWidth=2.4, opacity=90, cap="round")

# --- water -------------------------------------------------------------------
d.path(chord(600), "Water", fill=lin(0, 600, 0, 880,
                                     (0, "#3A8A8C"), (0.18, "#1E6E76"),
                                     (0.55, "#0E4A56"), (0.84, "#082E3A"), (1, "#05202A")),
       stroke=NONE)
d.path(chord(600), "Water sheen", fill=rad((0, "#A6E0D4", 14), (0.65, "#A6E0D4", 4),
                                           (1, "#A6E0D4", 0)), stroke=NONE)

# sun glitter column on the water
for i in range(9):
    y = 616 + i * 15
    w = 30 + i * 9
    d.path(smooth(wave_pts(y, 2.2, 292 - w / 2, 292 + w / 2, 2, phase=i * 0.3)),
           f"Sun glitter {i+1}", fill=NONE, stroke=GOLD_HI,
           strokeWidth=3.2 - i * 0.18, opacity=44 - i * 3.4, cap="round")

# broad translucent swells
for i, (y0, y1, amp, x0, x1, op) in enumerate([
        (626, 660, 6, 120, 470, 16), (640, 672, 5, 520, 880, 13),
        (700, 742, 8, 110, 500, 12), (760, 806, 9, 470, 890, 10),
        (812, 862, 10, 150, 860, 9)]):
    d.path(band(y0, y1, amp, x0, x1, 3, phase=i * 0.6), f"Swell {i+1}",
           fill="#BFE8DF", opacity=op, stroke=NONE)

for i, (yy, amp, x0, x1, op, sw) in enumerate([
        (656, 7, 130, 470, 30, 3.6), (670, 6, 520, 880, 26, 3.2),
        (722, 9, 120, 430, 26, 4), (778, 8, 500, 890, 22, 3.4),
        (836, 7, 180, 840, 18, 3)]):
    d.path(smooth(wave_pts(yy, amp, x0, x1, 3, phase=i * 0.4)), f"Ripple {i+1}",
           fill=NONE, stroke="#BFE8DF", strokeWidth=sw, opacity=op, cap="round")

for i, (x, y, w) in enumerate([(250, 730, 46), (352, 790, 30), (610, 742, 52),
                               (700, 820, 36), (430, 838, 44), (300, 806, 26),
                               (760, 772, 24)]):
    d.path(f"M{x:.1f},{y:.1f} C{x + w * 0.3:.1f},{y - 3:.1f} {x + w * 0.7:.1f},{y + 3:.1f} "
           f"{x + w:.1f},{y:.1f}", f"Glint {i+1}", fill=NONE, stroke=GOLD,
           strokeWidth=2.4, opacity=42, cap="round")

# --- boat: hull ---------------------------------------------------------------
HULL = ("M246,592 C278,676 356,724 500,728 C624,732 712,704 772,632 "
        "L752,596 C690,646 596,664 500,660 C402,656 300,622 246,592 Z")
d.path(HULL, "Hull", fill=lin(0, 590, 0, 730,
                              (0, LAC_HI), (0.26, LAC), (0.68, LAC_LO), (1, LAC_DEEP)),
       stroke=INK, strokeWidth=6)
d.path("M254,608 C288,676 360,714 500,718 C600,720 678,698 738,650 "
       "C660,700 560,710 470,702 C382,694 306,660 254,608 Z", "Hull shadow",
       fill="#2A0708", opacity=24, stroke=NONE)
d.path("M246,592 C278,676 356,724 500,728 C624,732 712,704 772,632", "Hull light",
       fill=NONE, stroke="#F0906A", strokeWidth=2.6, opacity=34, cap="round")
d.path("M752,596 C690,646 596,664 500,660 C402,656 300,622 246,592", "Gunwale",
       fill=NONE, stroke=gold_lin(590, 670), strokeWidth=9, cap="round")
d.path("M752,596 C690,646 596,664 500,660 C402,656 300,622 246,592", "Gunwale light",
       fill=NONE, stroke="#FFF0C0", strokeWidth=2.4, opacity=58, cap="round")
d.path("M256,622 C300,690 372,722 500,724 C616,726 700,696 760,636", "Keel",
       fill=NONE, stroke=GOLD_LO, strokeWidth=2.6, opacity=62, cap="round")
for row, (yy, x0, x1, stepx) in enumerate([(692, 330, 700, 42), (716, 380, 660, 42)]):
    x = x0
    i = 0
    while x < x1:
        d.path(f"M{x - 17:.1f},{yy:.1f} A17,12 0 0 0 {x + 17:.1f},{yy:.1f}",
               f"Hull scale {row}-{i}", fill=NONE, stroke="#F0B86A", strokeWidth=1.8,
               opacity=30, cap="round")
        x += stepx
        i += 1

# stern: fan tail + steering oar
for i, (ang, ln) in enumerate([(196, 92), (212, 108), (228, 88)]):
    a = math.radians(ang)
    bx, by = 252, 590
    tx, ty = bx + math.cos(a) * ln, by + math.sin(a) * ln * 0.9
    d.path(f"M{bx - 10:.1f},{by + 8:.1f} Q{bx + math.cos(a) * ln * 0.55 - 15:.1f},"
           f"{by + math.sin(a) * ln * 0.6:.1f} {tx:.1f},{ty:.1f} "
           f"Q{bx + math.cos(a) * ln * 0.5 + 12:.1f},{by + math.sin(a) * ln * 0.55:.1f} "
           f"{bx + 10:.1f},{by - 6:.1f} Z", f"Stern fin {i+1}",
           fill=lin(0, by - 100, 0, by, (0, "#F49A5E"), (1, LAC)),
           stroke=INK, strokeWidth=2.4)
d.path("M262,596 C258,576 262,560 272,548", "Stern post", fill=NONE,
       stroke=INK, strokeWidth=13, cap="round")
d.path("M262,596 C258,576 262,560 272,548", "Stern post gold", fill=NONE,
       stroke=gold_lin(545, 600), strokeWidth=6, cap="round")
# steering oar
d.path("M268,612 C232,646 210,700 206,752", "Steering oar", fill=NONE,
       stroke=INK, strokeWidth=9, cap="round")
d.path("M268,612 C232,646 210,700 206,752", "Steering oar shaft", fill=NONE,
       stroke=lin(0, 612, 0, 752, (0, "#E8C08A"), (1, "#8A5A2E")), strokeWidth=5, cap="round")
d.shape("ellipse", "Steering blade", x=188, y=744, width=30, height=56,
        fill=lin(0, 744, 0, 800, (0, "#E4B478"), (1, "#7A4A22")), stroke=INK,
        strokeWidth=2.4, rotation=-14)

# --- boat: oars ---------------------------------------------------------------
for i, ox in enumerate((322, 400, 478, 556, 634)):
    hx, hy = ox + 24, 648
    bx, by = ox - 52, 766
    d.path(f"M{hx:.1f},{hy:.1f} L{bx:.1f},{by:.1f}", f"Oar {i+1}",
           fill=NONE, stroke=INK, strokeWidth=10, cap="round")
    d.path(f"M{hx:.1f},{hy:.1f} L{bx:.1f},{by:.1f}", f"Oar shaft {i+1}",
           fill=NONE, stroke=lin(0, hy, 0, by, (0, "#E8C08A"), (1, "#8A5A2E")),
           strokeWidth=5.4, cap="round")
    d.shape("ellipse", f"Oar blade {i+1}", x=bx - 14, y=by - 2, width=28, height=52,
            fill=lin(0, by - 2, 0, by + 50, (0, "#E4B478"), (1, "#7A4A22")),
            stroke=INK, strokeWidth=2.4, rotation=-20)
    d.shape("ellipse", f"Oar blade water {i+1}", x=bx - 14, y=by - 2, width=28,
            height=52, fill="#0C3A44", opacity=42, stroke=NONE, rotation=-20)
    d.shape("ellipse", f"Oar ring {i+1}", x=bx - 32, y=748, width=64, height=16,
            fill=NONE, stroke="#DFF4EA", strokeWidth=2.2, opacity=40)
    for k, dx in enumerate((-38, -26, 24, 36)):
        d.shape("ellipse", f"Oar drop {i+1}-{k}", x=bx + dx - 3, y=734 - (k % 2) * 7,
                width=5, height=8, fill="#EAF8EF", opacity=50, stroke=NONE)

# --- boat: drum ---------------------------------------------------------------
for i, (x0, y0, x1, y1) in enumerate([(474, 578, 500, 612), (566, 578, 542, 612)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Drum stick {i+1}", fill=NONE,
           stroke="#C99A5A", strokeWidth=4, cap="round")
d.shape("ellipse", "Drum body", x=486, y=596, width=72, height=60,
        fill=rad((0, "#E06A4A"), (0.6, LAC), (1, LAC_DEEP)), stroke=INK, strokeWidth=3.2)
d.shape("ellipse", "Drum head", x=494, y=604, width=56, height=42,
        fill=rad((0, "#F6E3C0"), (1, "#D8B98A")), stroke=INK, strokeWidth=2.2)
d.path("M502,626 C512,618 526,620 540,626", "Drum mark", fill=NONE,
       stroke="#A8442E", strokeWidth=2.2, opacity=55, cap="round")

# --- boat: neck + head --------------------------------------------------------
NECK = [(760, 486), (764, 520), (768, 560), (768, 600), (766, 640)]
neck_d, _, _, _ = ribbon(NECK, [58, 66, 74, 82, 88])
d.path(neck_d, "Neck", fill=lin(0, 486, 0, 640, (0, LAC_HI), (0.45, LAC), (1, LAC_DEEP)),
       stroke=INK, strokeWidth=6)
for row, yy in enumerate((516, 544, 572, 600)):
    for k in range(3):
        x = 748 + k * 22 + (row % 2) * 7
        d.path(f"M{x - 9:.1f},{yy:.1f} A9,7 0 0 0 {x + 9:.1f},{yy:.1f}",
               f"Neck scale {row}-{k}", fill=NONE, stroke="#F0B86A", strokeWidth=1.7,
               opacity=34, cap="round")
# dorsal spines
for i, (y, ln) in enumerate([(516, 22), (546, 26), (576, 26), (606, 22)]):
    d.path(f"M742,{y} L{742 - ln},{y - 10} L746,{y + 10} Z", f"Dorsal fin {i+1}",
           fill=lin(0, y - 10, 0, y + 10, (0, "#F6B06A"), (1, "#A82E20")),
           stroke=INK, strokeWidth=1.8)
# collar
d.path("M726,514 C746,504 768,506 784,516", "Collar", fill=NONE,
       stroke=gold_lin(505, 525), strokeWidth=12, cap="round")
d.path("M728,510 C748,500 768,502 782,511", "Collar light", fill=NONE,
       stroke="#FFF0C0", strokeWidth=2.6, opacity=52, cap="round")

# mane behind head
for i, (ang, ln) in enumerate([(146, 84), (164, 104), (182, 100), (200, 82), (216, 60)]):
    a = math.radians(ang)
    bx, by = 744, 452
    tx, ty = bx + math.cos(a) * ln, by + math.sin(a) * ln
    d.path(f"M{bx:.1f},{by - 15:.1f} Q{bx + math.cos(a) * ln * 0.5:.1f},"
           f"{by + math.sin(a) * ln * 0.4 - 20:.1f} {tx:.1f},{ty:.1f} "
           f"Q{bx + math.cos(a) * ln * 0.45:.1f},{by + math.sin(a) * ln * 0.5 + 9:.1f} "
           f"{bx:.1f},{by + 15:.1f} Z", f"Mane {i+1}",
           fill=lin(0, by - 40, 0, by + 20, (0, "#F6B06A"), (1, "#C2402A")),
           stroke=INK, strokeWidth=2.2)

# lower jaw (behind the skull)
d.path("M796,492 C806,518 828,530 852,522 C860,518 864,510 860,504 "
       "C848,512 828,510 814,500 Z", "Lower jaw",
       fill=lin(0, 492, 0, 530, (0, "#F0E2BE"), (1, "#B8A070")),
       stroke=INK, strokeWidth=3)
d.path("M800,496 C814,512 838,518 859,508 C850,520 828,522 812,510 Z",
       "Mouth interior", fill="#3A0C0C", stroke=NONE)
d.path("M812,508 C822,514 838,514 848,508 C842,518 820,518 812,508 Z",
       "Tongue", fill="#8E2418", opacity=85, stroke=NONE)
for i, (x, y, w) in enumerate([(816, 500, 8), (830, 500, 8), (844, 498, 7)]):
    d.path(f"M{x - w / 2:.1f},{y:.1f} L{x + w / 2:.1f},{y:.1f} L{x:.1f},{y + 10:.1f} Z",
           f"Tooth {i+1}", fill=lin(0, y, 0, y + 10, (0, "#FFF8E4"), (1, "#D8C49A")),
           stroke=INK, strokeWidth=1.3)
d.path("M846,506 L850,496 L854,506 Z", "Lower fang",
       fill=lin(0, 496, 0, 506, (0, "#FFF8E4"), (1, "#D8C49A")), stroke=INK, strokeWidth=1.3)

SKULL = ("M736,470 C738,440 752,420 776,414 C800,408 826,416 840,430 "
         "C850,438 858,442 866,448 C874,454 876,464 868,470 "
         "C860,476 850,476 844,480 C830,488 816,490 804,486 "
         "C784,480 760,486 746,478 Z")
d.path(SKULL, "Dragon skull", fill=lin(0, 408, 0, 490,
                                      (0, "#F4AC70"), (0.42, LAC), (1, "#8E2318")),
       stroke=INK, strokeWidth=5)
d.path("M754,438 C772,422 800,416 822,424 C800,424 778,430 760,444 Z",
       "Head sheen", fill="#FFD9A8", opacity=34, stroke=NONE)
d.path("M790,434 C804,424 826,428 838,438 C822,434 804,434 790,442 Z",
       "Brow", fill=lin(0, 424, 0, 442, (0, GOLD_HI), (1, GOLD_LO)),
       stroke=INK, strokeWidth=2.2)
d.shape("ellipse", "Eye socket", x=800, y=442, width=44, height=32,
        fill="#5A1208", opacity=40, stroke=NONE)
d.shape("ellipse", "Eye white", x=802, y=444, width=40, height=28,
        fill=rad((0, "#FFFDF2"), (1, "#E8DCC4")), stroke=INK, strokeWidth=2.6)
d.shape("ellipse", "Eye iris", x=812, y=447, width=19, height=21,
        fill=rad((0, "#FFD36A"), (0.6, "#E09A2E"), (1, "#8A5210")), stroke=INK,
        strokeWidth=1.6)
d.shape("ellipse", "Eye pupil", x=818, y=451, width=8, height=13, fill="#1A0C0A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=820, y=449, width=4.4, height=4.4, fill="#FFFFFF",
        opacity=90, stroke=NONE)
d.path("M800,430 C814,422 832,426 842,434", "Eye lid", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=70, cap="round")
# nostril + nose bump
d.path("M858,450 C864,448 870,452 868,458", "Nose bump", fill=NONE,
       stroke=INK, strokeWidth=2.4, opacity=60, cap="round")
d.shape("ellipse", "Nostril", x=858, y=458, width=7, height=5, fill="#3A0C0C",
        stroke=NONE, rotation=-18)
# horns / antlers
for i, (pts, w_out, w_in) in enumerate([
        ([(788, 418), (772, 392), (756, 372), (752, 350)], 14, 7.5),
        ([(774, 416), (762, 398), (744, 386), (730, 372)], 9, 4.5)]):
    d.path(smooth(pts), f"Antler {i+1}", fill=NONE, stroke=INK, strokeWidth=w_out, cap="round")
    d.path(smooth(pts), f"Antler ivory {i+1}", fill=NONE, stroke="#F6E2B0",
           strokeWidth=w_in, cap="round")
d.path("M758,376 Q744,364 730,360", "Antler tine", fill=NONE, stroke=INK,
       strokeWidth=9, cap="round")
d.path("M758,376 Q744,364 730,360", "Antler tine ivory", fill=NONE,
       stroke="#F6E2B0", strokeWidth=4.5, cap="round")
# ear fin
d.path("M744,448 C730,436 712,436 704,446 C716,452 730,464 742,470 Z",
       "Ear fin", fill=lin(0, 436, 0, 470, (0, "#F6C48A"), (1, "#C2603A")),
       stroke=INK, strokeWidth=2.2)
# beard
d.path("M812,522 C818,544 818,562 812,578 C802,562 798,542 802,526 Z",
       "Beard", fill=lin(0, 522, 0, 578, (0, "#F0905E"), (1, "#A82E20")),
       stroke=INK, strokeWidth=2.2)
# whiskers
d.path("M866,466 C820,452 776,438 726,432 C710,430 700,436 702,446",
       "Whisker upper", fill=NONE, stroke=GOLD_HI, strokeWidth=2.8, opacity=80, cap="round")
d.path("M860,474 C816,486 772,500 730,508 C712,512 702,506 706,496",
       "Whisker lower", fill=NONE, stroke=GOLD, strokeWidth=2.4, opacity=66, cap="round")

# --- splash at the bow --------------------------------------------------------
for i, (x, y, r) in enumerate([(792, 684, 24), (820, 664, 16), (836, 694, 11),
                               (772, 706, 20), (806, 714, 13)]):
    d.shape("ellipse", f"Splash {i+1}", x=x - r, y=y - r * 0.7, width=2 * r,
            height=1.4 * r, fill=rad((0, "#FFFFFF", 80), (1, "#BFE8DF", 28)),
            stroke=NONE)
for i, (x, y, r) in enumerate([(812, 632, 6), (832, 650, 4.5), (846, 672, 4),
                               (788, 620, 4.5), (770, 640, 3.6)]):
    d.shape("ellipse", f"Spray {i+1}", x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="#FFFFFF", opacity=58, stroke=NONE)
d.path("M736,700 C766,674 800,656 830,660", "Splash crest", fill=NONE,
       stroke="#FFFFFF", strokeWidth=4.4, opacity=50, cap="round")

# --- foreground: leaf pad + zongzi -------------------------------------------
d.shape("ellipse", "Pad shadow", x=356, y=784, width=300, height=66,
        fill="#02100E", opacity=42, stroke=NONE)
d.path(smooth([(384, 786), (410, 764), (470, 754), (528, 760), (566, 774),
               (572, 790), (528, 806), (462, 808), (408, 800)], closed=True),
       "Leaf pad", fill=lin(0, 752, 0, 810, (0, "#5E8A48"), (0.5, "#3A5E32"), (1, "#1E3320")),
       stroke=INK, strokeWidth=3.2)
d.path("M392,788 C440,776 510,774 562,788", "Pad midrib", fill=NONE,
       stroke="#A8C07A", strokeWidth=2.2, opacity=52, cap="round")
for i in range(6):
    x = 412 + i * 26
    d.path(f"M{x},786 C{x + 7},770 {x + 15},762 {x + 22},758", f"Pad vein {i+1}",
           fill=NONE, stroke="#8FB06A", strokeWidth=1.5, opacity=32, cap="round")

zongzi(d, 424, 762, 84, 80, -9, "Zongzi back L")
zongzi(d, 494, 748, 78, 76, 9, "Zongzi back R", opened=True)
zongzi(d, 458, 790, 92, 88, -3, "Zongzi front")

# --- calamus / mugwort bundle at the bank -------------------------------------
BX, BY = 196, 754
for i, (tx, ty, bend, w0) in enumerate([
        (146, 486, -40, 14), (166, 446, -28, 13), (186, 420, -16, 12),
        (206, 410, -4, 12), (228, 424, 12, 11), (246, 462, 20, 10),
        (258, 512, 24, 9.5)]):
    calamus_blade(d, BX + (i - 3) * 4, BY - 12, tx, ty, bend, w0, f"Calamus blade {i+1}")
for i, (cx, cy, r, rot) in enumerate([(172, 546, 24, -22), (232, 520, 20, 16),
                                      (202, 494, 18, -4)]):
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def RP(x, y, cx=cx, cy=cy, ca=ca, sa=sa):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)

    pts = [RP(0, -r), RP(r * 0.8, -r * 0.4), RP(r * 0.7, r * 0.6),
           RP(0, r), RP(-r * 0.7, r * 0.6), RP(-r * 0.8, -r * 0.4)]
    d.path(smooth(pts, closed=True), f"Mugwort leaf {i+1}",
           fill=lin(0, cy - r, 0, cy + r, (0, "#A8BC94"), (1, "#4E6A46")),
           stroke=INK, strokeWidth=1.8)
    d.path(f"M{cx},{cy - r * 0.8} L{cx},{cy + r * 0.8}", f"Mugwort rib {i+1}",
           fill=NONE, stroke="#DCE8C8", strokeWidth=1.4, opacity=48, cap="round")
# red cord tie
d.path("M160,652 C184,642 216,642 240,654 C218,668 182,668 160,658 Z",
       "Bundle cord", fill=lin(0, 642, 0, 668, (0, "#D8503C"), (1, "#8A1E18")),
       stroke=INK, strokeWidth=2.4)
d.shape("ellipse", "Cord knot", x=188, y=656, width=21, height=17,
        fill=rad((0, "#E4604A"), (1, "#8E2018")), stroke=INK, strokeWidth=2)
for i, dx in enumerate((-6, 3, 12)):
    d.path(f"M{198 + dx},{670} C{202 + dx * 1.4},{694} {198 + dx * 1.3},{716} "
           f"{194 + dx * 1.2},{732}", f"Cord tail {i+1}", fill=NONE,
           stroke="#C8402E", strokeWidth=2.2, cap="round")

# --- rim, seals, caption -------------------------------------------------------
rim_pass(p, "#D0A45A", "#4A3212")
p.ring_ticks(n=24, color=GOLD, r_in=392, r_out=404, width=2, phase=-90)

p.chop("端午", x=700, y=176, w=48, h=124, size=28)
p.caption("DRAGON BOAT", "端午節 · 5TH MOON 5TH DAY · RIVER RITES",
          name_color="#F4E7CE", sub_color="#D8B47A", name_size=50,
          sub_size=18, tracking_name=60, tracking_sub=60, sub_font=CJK)

print("calls", d.count, "errors", len(d.errors))
d.finish("dragon-boat-V1R00")
