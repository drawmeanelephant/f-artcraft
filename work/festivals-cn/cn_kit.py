#!/usr/bin/env python3
"""Festival Seal — shared furniture for the Chinese festival series.
Plate grammar lives in orient/plate.py; this adds the seasonal motifs:
lanterns, fireworks, willow, swallows, magpies, mooncake, jade rabbit,
osmanthus, rain.
"""
import math, os, sys
WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORK not in sys.path:
    sys.path.insert(0, WORK)
from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN, CJK,
                          lin, rad, gold_lin, smooth, blossom, cloud, coin)

VERM = "#D9433B"
VERM_HI = "#F2705A"
VERM_LO = "#8E1F1E"
CORD = "#B8342C"


def cord(d, x0, y0, x1, y1, sag, label, sw=5):
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + sag
    d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}", label,
           fill=NONE, stroke="#4A0E10", strokeWidth=sw + 2.4, cap="round")
    d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
           f"{label} silk", fill=NONE, stroke=CORD, strokeWidth=sw, opacity=92, cap="round")


def hanging_lantern(d, cx, cy, w, h, ch, label):
    a, b = w / 2, h / 2
    d.shape("ellipse", f"{label} glow", x=cx - w * 0.95, y=cy - h * 0.82,
            width=w * 1.9, height=h * 1.66,
            fill=rad((0, "#FFB874", 20), (0.5, "#D9433B", 7), (1, "#D9433B", 0)), stroke=NONE)
    d.shape("ellipse", label, x=cx - a, y=cy - b, width=w, height=h,
            fill=lin((cx, cy - b), (cx, cy + b), (0, "#E85A42"), (0.45, "#C9372C"), (1, "#7A1718")),
            stroke=INK, strokeWidth=4.5)
    d.shape("ellipse", f"{label} sheen", x=cx - a * 0.66, y=cy - b * 0.72,
            width=a * 1.02, height=b * 1.24,
            fill=rad((0, "#FFD9B4", 30), (0.6, "#FF9E72", 10), (1, "#FF9E72", 0)), stroke=NONE)
    for k in (-0.72, -0.54, -0.36, -0.18, 0.0, 0.18, 0.36, 0.54, 0.72):
        dx = k * a
        s = math.sqrt(max(0.0, 1 - k * k))
        y0, y1 = cy - b * s * 0.98, cy + b * s * 0.98
        d.path(f"M{cx + dx:.1f},{y0:.1f} Q{cx + dx + (a * 0.06 if k >= 0 else -a * 0.06):.1f},{cy:.1f} "
               f"{cx + dx:.1f},{y1:.1f}", f"{label} rib {k}", fill=NONE,
               stroke="#F6B07A", strokeWidth=1.7, opacity=34, cap="round")
    for yy, lab in ((cy - b - 10, "top"), (cy + b - 2, "bottom")):
        d.shape("rectangle", f"{label} cap {lab}", x=cx - w * 0.31, y=yy,
                width=w * 0.62, height=12, radius=3, fill=gold_lin(yy, yy + 12),
                stroke=INK, strokeWidth=2)
    d.path(f"M{cx:.1f},{cy - b - 10:.1f} C{cx - 7:.1f},{cy - b - 34:.1f} "
           f"{cx + 16:.1f},{cy - b - 40:.1f} {cx + 21:.1f},{cy - b - 22:.1f}",
           f"{label} loop", fill=NONE, stroke=GOLD, strokeWidth=2.8, cap="round")
    d.text(ch, f"{label} glyph", x=cx, y=cy + 17, size=w * 0.33, font=CJK,
           color="#FBE6B4", justify="center")
    ty = cy + b + 10
    d.shape("rectangle", f"{label} knot", x=cx - 7, y=ty, width=14, height=13,
            radius=3, fill=gold_lin(ty, ty + 13), stroke=INK, strokeWidth=1.6)
    for i, dx in enumerate((-19, -13, -7, 0, 7, 13, 19)):
        d.path(f"M{cx + dx*0.35:.1f},{ty + 18:.1f} C{cx + dx*0.9:.1f},{ty + 34:.1f} "
               f"{cx + dx*1.5:.1f},{ty + 48 + abs(dx):.1f} {cx + dx*1.5:.1f},{ty + 62 + abs(dx):.1f}",
               f"{label} tassel {i+1}", fill=NONE, stroke="#C0392E",
               strokeWidth=3 if i % 2 else 2.5, opacity=92, cap="round")


def firework(d, cx, cy, r, label, seed=5, n=12, op=55):
    d.shape("ellipse", f"{label} glow", x=cx - r * 1.05, y=cy - r * 1.05,
            width=2.1 * r, height=2.1 * r,
            fill=rad((0, "#FFC97E", 12), (0.55, "#E8663A", 5), (1, "#E8663A", 0)), stroke=NONE)
    s = seed
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = math.radians(i * 360 / n + (s % 100) / 100 * 8 - 4)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (0.72 + (s % 100) / 100 * 0.30)
        dx, dy = math.cos(a), math.sin(a)
        x0, y0 = cx + dx * r * 0.14, cy + dy * r * 0.14
        x1, y1 = cx + dx * rr, cy + dy * rr + rr * 0.16
        mx, my = (x0 + x1) / 2 - dy * rr * 0.10, (y0 + y1) / 2 + dx * rr * 0.10
        d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
               f"{label} trail {i+1}", fill=NONE, stroke=GOLD, strokeWidth=2.2, opacity=op, cap="round")
        d.shape("ellipse", f"{label} tip {i+1}", x=x1 - 2.6, y=y1 - 2.6, width=5.2,
                height=5.2, fill=GOLD_HI, opacity=min(92, op + 20), stroke=NONE)
    d.shape("ellipse", f"{label} core", x=cx - 5, y=cy - 5, width=10, height=10,
            fill="#FFF8E0", opacity=90, stroke=NONE)


# --- Qingming -----------------------------------------------------------------
def willow(d, x0, y0, x1, y1, label, leaves=26, sag=-70, color="#8FB88E"):
    d.path(f"M{x0:.1f},{y0:.1f} Q{(x0+x1)/2:.1f},{min(y0,y1)+sag:.1f} {x1:.1f},{y1:.1f}",
           f"{label} branch", fill=NONE, stroke="#4A3A22", strokeWidth=5, cap="round")
    for i in range(leaves):
        t = i / (leaves - 1)
        mt = 1 - t
        x = mt * mt * x0 + 2 * mt * t * ((x0 + x1) / 2) + t * t * x1
        y = mt * mt * y0 + 2 * mt * t * (min(y0, y1) + sag) + t * t * y1
        for sgn in (-1, 1):
            d.path(f"M{x:.1f},{y:.1f} C{x + sgn*6:.1f},{y + 12:.1f} "
                   f"{x + sgn*10:.1f},{y + 22:.1f} {x + sgn*8:.1f},{y + 34:.1f}",
                   f"{label} leaf {i}-{sgn}", fill=NONE, stroke=color,
                   strokeWidth=2.4, opacity=80, cap="round")


def swallow(d, x, y, s, flip=1, label="Swallow"):
    d.path(f"M{x:.1f},{y:.1f} C{x + flip*18*s:.1f},{y - 10*s:.1f} "
           f"{x + flip*38*s:.1f},{y - 4*s:.1f} {x + flip*46*s:.1f},{y + 10*s:.1f} "
           f"C{x + flip*30*s:.1f},{y + 6*s:.1f} {x + flip*16*s:.1f},{y + 10*s:.1f} "
           f"{x:.1f},{y + 18*s:.1f} Z", f"{label} wing", fill="#2A2A3A", stroke=NONE)
    d.shape("ellipse", f"{label} body", x=x - 10*s, y=y - 2*s, width=22*s, height=10*s,
            fill="#1E1E2A", stroke=NONE, rotation=-8*flip)
    d.path(f"M{x - 10*s:.1f},{y + 1*s:.1f} L{x - 22*s:.1f},{y - 4*s:.1f} "
           f"L{x - 20*s:.1f},{y + 6*s:.1f} Z", f"{label} tail", fill="#1E1E2A", stroke=NONE)
    d.shape("ellipse", f"{label} head", x=x + 8*s, y=y - 6*s, width=8*s, height=7*s,
            fill="#1E1E2A", stroke=NONE)
    d.shape("ellipse", f"{label} eye", x=x + 12*s, y=y - 7*s, width=2*s, height=2*s,
            fill="#FFFFFF", opacity=80, stroke=NONE)


def rain(d, n=46, seed=9, color="#B8D0D8", x0=120, x1=880, y0=100, y1=760):
    s = seed
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        x = x0 + (s % 10000) / 10000 * (x1 - x0)
        s = (1103515245 * s + 12345) % (2 ** 31)
        y = y0 + (s % 10000) / 10000 * (y1 - y0)
        s = (1103515245 * s + 12345) % (2 ** 31)
        L = 14 + (s % 1000) / 1000 * 26
        d.shape("line", f"Rain {i+1}", x1=round(x, 1), y1=round(y, 1),
                x2=round(x - 6, 1), y2=round(y + L, 1), stroke=color,
                strokeWidth=1.4, opacity=22 + (s % 20), cap="round")


# --- Qixi ---------------------------------------------------------------------
def magpie(d, x, y, s, flip=1, label="Magpie"):
    d.shape("ellipse", f"{label} body", x=x - 12*s, y=y - 7*s, width=26*s, height=14*s,
            fill="#1A1A24", stroke=NONE, rotation=-8*flip)
    d.shape("ellipse", f"{label} breast", x=x - 10*s, y=y - 3*s, width=18*s, height=7*s,
            fill="#F0E8D8", opacity=85, stroke=NONE)
    d.shape("ellipse", f"{label} head", x=x + 10*s, y=y - 10*s, width=10*s, height=9*s,
            fill="#1A1A24", stroke=NONE)
    d.path(f"M{x + 16*s:.1f},{y - 10*s:.1f} L{x + 24*s:.1f},{y - 8*s:.1f} "
           f"L{x + 16*s:.1f},{y - 6*s:.1f} Z", f"{label} beak", fill="#D8A040", stroke=NONE)
    d.shape("ellipse", f"{label} eye", x=x + 14*s, y=y - 12*s, width=2*s, height=2*s,
            fill="#FFFFFF", opacity=85, stroke=NONE)
    d.path(f"M{x - 8*s:.1f},{y - 4*s:.1f} C{x + flip*4*s:.1f},{y - 22*s:.1f} "
           f"{x + flip*22*s:.1f},{y - 16*s:.1f} {x + flip*26*s:.1f},{y - 2*s:.1f} "
           f"C{x + flip*12*s:.1f},{y - 6*s:.1f} {x - 2*s:.1f},{y - 2*s:.1f} "
           f"{x - 8*s:.1f},{y - 4*s:.1f} Z", f"{label} wing", fill="#2A2A38", stroke=NONE)
    d.path(f"M{x - 8*s:.1f},{y + 2*s:.1f} L{x - 22*s:.1f},{y - 2*s:.1f} "
           f"L{x - 20*s:.1f},{y + 8*s:.1f} Z", f"{label} tail", fill="#1A1A24", stroke=NONE)


# --- Mid-Autumn ---------------------------------------------------------------
def mooncake(d, cx, cy, r, label="Mooncake"):
    d.shape("ellipse", f"{label} side", x=cx - r, y=cy - r * 0.78, width=2*r, height=2*r,
            fill=lin(0, cy - r, 0, cy + r, (0, "#C88A3E"), (1, "#7A4A16")),
            stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"{label} top", x=cx - r * 0.94, y=cy - r * 0.94,
            width=r * 1.88, height=r * 1.88,
            fill=rad((0, "#F6D08A"), (0.6, "#D8A04E"), (1, "#A86A24")),
            stroke=INK, strokeWidth=2.5)
    # scalloped edge
    for i in range(16):
        a = math.radians(i * 22.5)
        d.shape("ellipse", f"{label} scallop {i+1}", x=cx + r*0.86*math.cos(a) - r*0.1,
                y=cy + r*0.86*math.sin(a) - r*0.1, width=r*0.2, height=r*0.2,
                fill="#E8B86A", stroke="#8A5A1E", strokeWidth=1.2, opacity=85)
    # pressed pattern: central blossom + ring
    d.shape("ellipse", f"{label} well", x=cx - r*0.62, y=cy - r*0.62,
            width=r*1.24, height=r*1.24, fill=NONE, stroke="#8A5A1E",
            strokeWidth=2, opacity=55)
    blossom(d, cx, cy, r * 0.52, petals=8, label=f"{label} blossom",
            fill="#C88A3E", core="#7A4A16", rot=-90, opacity=65)
    for i in range(8):
        a = math.radians(i * 45)
        d.shape("ellipse", f"{label} dot {i+1}", x=cx + r*0.72*math.cos(a) - 3,
                y=cy + r*0.72*math.sin(a) - 3, width=6, height=6,
                fill="#7A4A16", opacity=55, stroke=NONE)


def osmanthus(d, x0, y0, x1, y1, label, n=22, color="#F2C05A"):
    d.path(f"M{x0:.1f},{y0:.1f} Q{(x0+x1)/2:.1f},{min(y0,y1)-30:.1f} {x1:.1f},{y1:.1f}",
           f"{label} branch", fill=NONE, stroke="#4A3A22", strokeWidth=4, cap="round")
    for i in range(n):
        t = (i + 0.5) / n
        mt = 1 - t
        x = mt * mt * x0 + 2 * mt * t * ((x0 + x1) / 2) + t * t * x1
        y = mt * mt * y0 + 2 * mt * t * (min(y0, y1) - 30) + t * t * y1
        ox = (i % 3 - 1) * 10
        oy = (i % 4 - 1.5) * 8
        for k in range(4):
            a = math.radians(k * 90 + 45)
            d.shape("ellipse", f"{label} flower {i}-{k}", x=x + ox + 5*math.cos(a) - 3,
                    y=y + oy + 5*math.sin(a) - 3, width=6, height=6,
                    fill=color, opacity=82, stroke=NONE)


def jade_rabbit(d, cx, cy, s, label="Jade rabbit"):
    # body
    d.shape("ellipse", f"{label} body", x=cx - 34*s, y=cy - 20*s, width=68*s, height=58*s,
            fill=rad((0, "#E8F4E4"), (0.65, "#C8E0D0"), (1, "#8AB8A0")),
            stroke=INK, strokeWidth=3)
    # head
    d.shape("ellipse", f"{label} head", x=cx - 28*s, y=cy - 62*s, width=56*s, height=50*s,
            fill=rad((0, "#F8FFF4"), (0.6, "#D8EEDC"), (1, "#A8CCB8")),
            stroke=INK, strokeWidth=3)
    # ears
    for sign, nm in ((-1, "L"), (1, "R")):
        d.path(f"M{cx + sign*12*s:.1f},{cy - 78*s:.1f} C{cx + sign*18*s:.1f},{cy - 112*s:.1f} "
               f"{cx + sign*24*s:.1f},{cy - 136*s:.1f} {cx + sign*30*s:.1f},{cy - 146*s:.1f} "
               f"C{cx + sign*40*s:.1f},{cy - 124*s:.1f} {cx + sign*38*s:.1f},{cy - 96*s:.1f} "
               f"{cx + sign*30*s:.1f},{cy - 76*s:.1f} Z", f"{label} ear {nm}",
               fill=lin(0, cy - 146*s, 0, cy - 74*s, (0, "#F8FFF4"), (1, "#B8D8C4")),
               stroke=INK, strokeWidth=2.6)
        d.path(f"M{cx + sign*20*s:.1f},{cy - 84*s:.1f} C{cx + sign*24*s:.1f},{cy - 112*s:.1f} "
               f"{cx + sign*28*s:.1f},{cy - 128*s:.1f} {cx + sign*31*s:.1f},{cy - 136*s:.1f}",
               f"{label} ear inner {nm}", fill=NONE, stroke="#E8A8B8", strokeWidth=4*s,
               opacity=65, cap="round")
    # face
    d.shape("ellipse", f"{label} eye L", x=cx - 14*s, y=cy - 52*s, width=7*s, height=8*s,
            fill="#2A1A18", stroke=NONE)
    d.shape("ellipse", f"{label} eye R", x=cx + 8*s, y=cy - 52*s, width=7*s, height=8*s,
            fill="#2A1A18", stroke=NONE)
    d.shape("ellipse", f"{label} nose", x=cx - 4*s, y=cy - 40*s, width=8*s, height=6*s,
            fill="#E8A0B0", stroke=NONE)
    d.path(f"M{cx:.1f},{cy - 36*s:.1f} L{cx:.1f},{cy - 30*s:.1f}", f"{label} philtrum",
           fill=NONE, stroke=INK, strokeWidth=2*s, cap="round")
    # front paws holding a mooncake
    for sign, nm in ((-1, "L"), (1, "R")):
        d.shape("ellipse", f"{label} paw {nm}", x=cx + sign*22*s - 12*s, y=cy + 2*s,
                width=24*s, height=18*s, fill="#E8F4E4", stroke=INK, strokeWidth=2.4)


def cloud_drift(d, cx, cy, w, label, color="#D8E8E0", opacity=55):
    for i, (dx, dy, r) in enumerate([(-0.32, 0.05, 0.28), (-0.08, -0.08, 0.34),
                                     (0.2, 0.0, 0.3), (0.4, 0.08, 0.2)]):
        d.shape("ellipse", f"{label} puff {i+1}", x=cx + dx*w - r*w,
                y=cy + dy*w - r*w*0.6, width=r*2*w, height=r*1.2*w,
                fill=color, opacity=opacity, stroke=NONE)
