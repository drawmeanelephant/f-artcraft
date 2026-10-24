#!/usr/bin/env python3
"""Holi — Festival Seal V1R00.

The colour plate: no emblem but the gulal itself. Three soft thrown clouds
(magenta, marigold, green) cross the disc, two defined splash blobs anchor
the corners, dotted arcs of thrown powder connect them, and a few translucent
water droplets fall. Deep wine field so every colour sings. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, DEVA, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, gulal_cloud, splash, deva_seal, caption

SLUG = "holi-V1R00"
MAGENTA = "#D8408A"
MARIGOLD = "#F2B33C"
LEAF = "#58B868"
VIOLET = "#8A5AC8"
ORANGE = "#E8703C"
WATER = "#5AB4D0"

p = __import__("orient.plate", fromlist=["Plate"]).Plate("Holi — Festival Seal")
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


def throw_arc(a, b, lift, col, label, n=16, seed=5):
    """A dotted arc of thrown powder from a to b, grains scattering."""
    c = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - lift)
    s = seed
    for i in range(n):
        t = i / (n - 1)
        x, y = bez2(a, c, b, t)
        s = (1103515245 * s + 12345) % (2 ** 31)
        x += ((s % 10000) / 10000 - 0.5) * 26
        s = (1103515245 * s + 12345) % (2 ** 31)
        y += ((s % 10000) / 10000 - 0.5) * 26
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = 1.6 + (s % 1000) / 1000 * 3.4
        s = (1103515245 * s + 12345) % (2 ** 31)
        inside(x, y, 14, f"{label} {i}")
        d.shape("ellipse", f"{label} grain {i+1}", x=round(x - rr, 1),
                y=round(y - rr, 1), width=rr * 2, height=rr * 2, fill=col,
                opacity=34 + (s % 40), stroke=NONE)


def soft_splash(cx, cy, r, col, opacity=44, puffs=8, seed=3, label="Splash"):
    """A tighter burst of thrown powder: clustered radial puffs + spray dots."""
    s = seed
    d.shape("ellipse", f"{label} heart", x=cx - r, y=cy - r * 0.86,
            width=2 * r, height=1.72 * r,
            fill=rad((0, col, min(88, opacity + 24)), (0.55, col, opacity),
                     (1, col, 0)), stroke=NONE)
    for i in range(puffs):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = 2 * math.pi * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (0.24 + 0.6 * (s / 2 ** 31))
        s = (1103515245 * s + 12345) % (2 ** 31)
        pr = r * (0.22 + 0.3 * (s / 2 ** 31))
        px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.82
        inside(px + pr, py + pr, 12, f"{label} puff {i}")
        d.shape("ellipse", f"{label} puff {i+1}", x=round(px - pr, 1),
                y=round(py - pr * 0.9, 1), width=pr * 2, height=pr * 1.8,
                fill=rad((0, col, opacity), (0.6, col, opacity * 0.5),
                         (1, col, 0)), stroke=NONE)
    for i in range(10):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = 2 * math.pi * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (1.02 + 0.85 * (s / 2 ** 31))
        sz = 2.2 + 4.6 * (s % 100) / 100
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.85
        inside(x, y, 12, f"{label} sat {i}")
        d.shape("ellipse", f"{label} dot {i+1}", x=round(x - sz / 2, 1),
                y=round(y - sz / 2, 1), width=sz, height=sz, fill=col,
                opacity=min(88, opacity + 26), stroke=NONE)


def droplet(x, y, s, col=WATER, op=60, label="Droplet"):
    d.path(f"M{x:.1f},{y - s:.1f} C{x + s * 0.72:.1f},{y - s * 0.2:.1f} "
           f"{x + s * 0.62:.1f},{y + s * 0.55:.1f} {x:.1f},{y + s * 0.62:.1f} "
           f"C{x - s * 0.62:.1f},{y + s * 0.55:.1f} {x - s * 0.72:.1f},{y - s * 0.2:.1f} "
           f"{x:.1f},{y - s:.1f} Z", label,
           fill=lin(0, y - s, 0, y + s, (0, "#D8F0F8"), (1, col)),
           opacity=op, stroke=NONE)


# --- field ------------------------------------------------------------------
p.backdrop(top="#2A0E22", bottom="#0A040A", glow=("#8A2A5E", 12))
dust(d, n=40, r=402, colors=("#F2B33C", "#D8408A", "#8A5AC8"), seed=17,
     smin=1.0, smax=2.6, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, "#3C1230", "#140518", rim=GOLD, rim2="#401028")
dust(d, n=70, r=392, colors=("#F2B33C", "#D8408A", "#58B868", "#8A5AC8"),
     seed=9, smin=1.0, smax=3.0, opmin=10, opmax=30, label="Disc dust")
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#F0C88E"), (0.5, "#B87A4E"),
                   (1, "#E8B878")), strokeWidth=4)
p.ring_ticks(n=24, color="#B8865E", r_in=378, r_out=396, width=2.2)

# --- thrown colour ------------------------------------------------------------
glow(d, 330, 360, 190, MAGENTA, a=20, label="Glow magenta")
gulal_cloud(d, 330, 370, 148, MAGENTA, opacity=52, puffs=12, seed=9,
            label="Gulal magenta")
glow(d, 682, 316, 170, MARIGOLD, a=20, label="Glow marigold")
gulal_cloud(d, 682, 320, 126, MARIGOLD, opacity=54, puffs=11, seed=15,
            label="Gulal marigold")
glow(d, 520, 590, 175, LEAF, a=18, label="Glow green")
gulal_cloud(d, 520, 592, 136, LEAF, opacity=48, puffs=12, seed=21,
            label="Gulal green")

soft_splash(240, 596, 66, VIOLET, opacity=32, seed=7, label="Splash violet")
soft_splash(754, 570, 56, ORANGE, opacity=32, seed=11, label="Splash orange")

# dotted arcs of powder connecting the bursts
throw_arc((398, 420), (600, 348), 66, MARIGOLD, "Throw arc A", n=15, seed=3)
throw_arc((430, 500), (472, 528), 40, MAGENTA, "Throw arc B", n=11, seed=13)
throw_arc((620, 500), (700, 480), 48, LEAF, "Throw arc C", n=12, seed=23)

# --- water --------------------------------------------------------------------
for i, (x, y, s, op) in enumerate([(300, 470, 11, 58), (586, 300, 9, 52),
                                   (700, 640, 12, 56), (430, 640, 7, 48),
                                   (628, 448, 6, 44)]):
    inside(x + s, y + s, 12, f"droplet {i}")
    droplet(x, y, s, op=op, label=f"Droplet {i+1}")

# stray grains across the disc
s = 41
for i in range(26):
    s = (1103515245 * s + 12345) % (2 ** 31)
    x = 150 + (s % 10000) / 10000 * 700
    s = (1103515245 * s + 12345) % (2 ** 31)
    y = 120 + (s % 10000) / 10000 * 640
    s = (1103515245 * s + 12345) % (2 ** 31)
    rr = 1.4 + (s % 1000) / 1000 * 2.6
    if math.hypot(x - PCX, y - PCY) > 386:
        continue
    d.shape("ellipse", f"Stray grain {i+1}", x=round(x - rr, 1),
            y=round(y - rr, 1), width=rr * 2, height=rr * 2,
            fill=(MAGENTA, MARIGOLD, LEAF, VIOLET, ORANGE)[i % 5],
            opacity=30 + (s % 34), stroke=NONE)

# --- seal + caption -------------------------------------------------------------
deva_seal(d, "होली", cx=744, cy=213, s=64, size=26)
caption(p, "HOLI", "होली · FESTIVAL OF COLOURS · PHALGUN PURNIMA",
        name_color="#FBE6D8", sub_color="#D8A0B8",
        name_size=52, tracking_name=130, sub_size=20, tracking_sub=40)
p.finish(SLUG)
