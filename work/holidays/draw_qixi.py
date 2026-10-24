#!/usr/bin/env python3
"""Qixi — Festival Seal V1R00.

The Double Seventh: a night plate. Deep indigo disc, the Milky Way as a
translucent diagonal band, the Weaver Girl's star and the Cowherd's star at
its ends joined by the fine red thread of fate, a bridge of magpies flying
the line between them, low night clouds at the foot of the disc. Gold stars,
one vermilion note. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth)

SLUG = "qixi-V1R00"
STAR_GOLD = "#F2DFA8"
STAR_WHITE = "#EDEAFA"
THREAD = "#D9433B"
INDIGO_HI = "#2A2454"
INDIGO_LO = "#0C0A1E"

p = Plate("Qixi — Festival Seal", 1000, 1000)
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


def sparkle(x, y, r, col=STAR_GOLD, op=92, label="Star"):
    """Four-point star with a soft halo and a bright core."""
    d.shape("ellipse", f"{label} halo", x=x - r * 2.6, y=y - r * 2.6,
            width=r * 5.2, height=r * 5.2,
            fill=rad((0, col, 42), (0.5, col, 12), (1, col, 0)), stroke=NONE)
    q = r * 0.22
    d.path(f"M{x:.1f},{y - r:.1f} Q{x + q:.1f},{y - q:.1f} {x + r:.1f},{y:.1f} "
           f"Q{x + q:.1f},{y + q:.1f} {x:.1f},{y + r:.1f} "
           f"Q{x - q:.1f},{y + q:.1f} {x - r:.1f},{y:.1f} "
           f"Q{x - q:.1f},{y - q:.1f} {x:.1f},{y - r:.1f} Z",
           f"{label} cross", fill=col, opacity=op, stroke=NONE)
    d.shape("ellipse", f"{label} core", x=x - r * 0.28, y=y - r * 0.28,
            width=r * 0.56, height=r * 0.56, fill="#FFFBE8", opacity=95,
            stroke=NONE)


def starfield(n=70, seed=21, rmax=392):
    """Fine stars scattered over the whole disc, denser near the band."""
    s = seed
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        x = 120 + (s % 10000) / 10000 * 760
        s = (1103515245 * s + 12345) % (2 ** 31)
        y = 90 + (s % 10000) / 10000 * 660
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = 0.8 + (s % 1000) / 1000 * 1.8
        s = (1103515245 * s + 12345) % (2 ** 31)
        if math.hypot(x - PCX, y - PCY) > rmax:
            continue
        d.shape("ellipse", f"Fine star {i+1}", x=round(x - rr, 1),
                y=round(y - rr, 1), width=rr * 2, height=rr * 2,
                fill=STAR_GOLD if i % 3 else STAR_WHITE,
                opacity=18 + (s % 40), stroke=NONE)


def cloud_drift_low(d, cx, cy, w, label, color, opacity):
    for i, (dx, dy, r) in enumerate([(-0.32, 0.05, 0.28), (-0.08, -0.08, 0.34),
                                     (0.2, 0.0, 0.3), (0.4, 0.08, 0.2)]):
        d.shape("ellipse", f"{label} puff {i+1}", x=cx + dx * w - r * w,
                y=cy + dy * w - r * w * 0.6, width=r * 2 * w, height=r * 1.2 * w,
                fill=color, opacity=opacity, stroke=NONE)


def qixi_magpie(x, y, s, flip=1, label="Magpie"):
    """Sleek magpie in flight: long tail, swept wing, soft white shoulder."""
    f = flip
    # long graduated tail
    d.path(f"M{x - f*14*s:.1f},{y + 2*s:.1f} L{x - f*40*s:.1f},{y - 8*s:.1f} "
           f"L{x - f*26*s:.1f},{y + 4*s:.1f} L{x - f*38*s:.1f},{y + 12*s:.1f} "
           f"L{x - f*14*s:.1f},{y + 7*s:.1f} Z", f"{label} tail",
           fill="#181822", stroke=NONE)
    # body, head to tail base
    d.path(f"M{x + f*20*s:.1f},{y - 4*s:.1f} "
           f"C{x + f*18*s:.1f},{y - 9*s:.1f} {x + f*6*s:.1f},{y - 10*s:.1f} "
           f"{x - f*6*s:.1f},{y - 7*s:.1f} C{x - f*14*s:.1f},{y - 5*s:.1f} "
           f"{x - f*17*s:.1f},{y + 1*s:.1f} {x - f*14*s:.1f},{y + 5*s:.1f} "
           f"C{x - f*8*s:.1f},{y + 9*s:.1f} {x + f*8*s:.1f},{y + 7*s:.1f} "
           f"{x + f*16*s:.1f},{y + 2*s:.1f} "
           f"C{x + f*19*s:.1f},{y:.1f} {x + f*21*s:.1f},{y - 2*s:.1f} "
           f"{x + f*20*s:.1f},{y - 4*s:.1f} Z", f"{label} body",
           fill=lin((x - f * 16 * s, y), (x + f * 20 * s, y),
                    (0, "#15151E"), (1, "#333344")), stroke=NONE)
    # swept-up wing
    d.path(f"M{x + f*6*s:.1f},{y - 4*s:.1f} "
           f"C{x - f*2*s:.1f},{y - 14*s:.1f} {x - f*16*s:.1f},{y - 22*s:.1f} "
           f"{x - f*28*s:.1f},{y - 20*s:.1f} C{x - f*20*s:.1f},{y - 12*s:.1f} "
           f"{x - f*12*s:.1f},{y - 5*s:.1f} {x - f*6*s:.1f},{y + 1*s:.1f} Z",
           f"{label} wing", fill="#22222E", stroke=NONE)
    d.path(f"M{x + f*2*s:.1f},{y - 6*s:.1f} C{x - f*6*s:.1f},{y - 12*s:.1f} "
           f"{x - f*14*s:.1f},{y - 16*s:.1f} {x - f*22*s:.1f},{y - 16*s:.1f}",
           f"{label} wing glint", fill=NONE, stroke="#4A4A62", strokeWidth=1.4,
           opacity=60, cap="round")
    # soft white shoulder + breast hint
    d.shape("ellipse", f"{label} shoulder", x=x - f * 2 * s - 4 * s,
            y=y - 4 * s, width=9 * s, height=6 * s, fill="#E8E2F0",
            opacity=52, stroke=NONE, rotation=-16 * f)
    # head, beak, eye
    d.shape("ellipse", f"{label} head", x=x + f * 14 * s - 5 * s,
            y=y - 10 * s, width=11 * s, height=10 * s, fill="#1A1A26",
            stroke=NONE)
    d.path(f"M{x + f*23*s:.1f},{y - 8*s:.1f} L{x + f*31*s:.1f},{y - 6*s:.1f} "
           f"L{x + f*23*s:.1f},{y - 4*s:.1f} Z", f"{label} beak",
           fill="#D8A040", stroke=NONE)
    d.shape("ellipse", f"{label} eye", x=x + f * 19 * s - 1.1 * s,
            y=y - 8.5 * s, width=2.2 * s, height=2.2 * s, fill="#F6EFDC",
            opacity=88, stroke=NONE)


# --- field ------------------------------------------------------------------
p.backdrop(top="#141226", bottom="#05040C", glow=("#3A2E5E", 12))
p.disc(INDIGO_HI, INDIGO_LO, rim=GOLD, rim2="#241C44")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.58, "#000000", 0), (1, "#000000", 64)),
        stroke=NONE)
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#E8D8A8"), (0.5, "#9A8A5E"),
                   (1, "#D8C890")), strokeWidth=4)
d.shape("ellipse", "Night aura", x=150, y=80, width=700, height=620,
        fill=rad((0, "#4A3E7E", 15), (0.55, "#3A2E5E", 7), (1, "#3A2E5E", 0)),
        stroke=NONE)
p.ring_ticks(n=24, color="#8E84B8", r_in=378, r_out=396, width=2.2)

# --- Milky Way: soft nebula blobs along a diagonal spine ----------------------
A = (212, 652)
B = (762, 248)
C = (452, 478)  # control: gentle bow to the lower right
inside(*A, 16, "band A")
inside(*B, 16, "band B")
dx, dy = B[0] - A[0], B[1] - A[1]
ln = math.hypot(dx, dy)
ux, uy = dx / ln, dy / ln
for i in range(9):
    t = i / 8
    bx, by = bez2(A, C, B, t)
    edge = min(t, 1 - t)
    rr = (54 + 52 * math.sin(math.pi * t)) * (0.55 + 0.45 * min(1.0, edge * 6))
    d.shape("ellipse", f"Milky Way {i+1}", x=bx - rr, y=by - rr * 0.72,
            width=rr * 2, height=rr * 1.44,
            fill=rad((0, "#DDD6F2", 13), (0.6, "#C8C0E8", 7), (1, "#C8C0E8", 0)),
            stroke=NONE, rotation=-40.9)
    core = rr * 0.52
    d.shape("ellipse", f"Milky Way core {i+1}", x=bx - core, y=by - core * 0.72,
            width=core * 2, height=core * 1.44,
            fill=rad((0, "#EFEAF8", 11), (1, "#EFEAF8", 0)), stroke=NONE,
            rotation=-40.9)
# dense fine stars hugging the band
s = 31
for i in range(90):
    s = (1103515245 * s + 12345) % (2 ** 31)
    t = (s % 10000) / 10000
    s = (1103515245 * s + 12345) % (2 ** 31)
    off = ((s % 10000) / 10000 - 0.5) * 96
    s = (1103515245 * s + 12345) % (2 ** 31)
    x, y = bez2(A, C, B, t)
    dx, dy = 466, -404
    ln = math.hypot(dx, dy)
    x, y = x - dy / ln * off, y + dx / ln * off
    rr = 0.7 + (s % 1000) / 1000 * 1.7
    if math.hypot(x - PCX, y - PCY) > 396:
        continue
    d.shape("ellipse", f"Band star {i+1}", x=round(x - rr, 1), y=round(y - rr, 1),
            width=rr * 2, height=rr * 2,
            fill=STAR_WHITE if i % 2 else STAR_GOLD,
            opacity=26 + (s % 44), stroke=NONE)
starfield(n=64, seed=47)

# --- the two hero stars -------------------------------------------------------
SA = bez2(A, C, B, 0.20)
SB = bez2(A, C, B, 0.80)
inside(*SA, 14, "star A")
inside(*SB, 14, "star B")
sparkle(SA[0], SA[1], 26, col=STAR_GOLD, label="Weaver star")
sparkle(SB[0], SB[1], 26, col=STAR_GOLD, label="Cowherd star")
for (hx, hy, lbl) in ((SA[0] - 34, SA[1] - 26, "A"), (SB[0] + 30, SB[1] - 30, "B")):
    sparkle(hx, hy, 9, col=STAR_WHITE, op=80, label=f"Star glint {lbl}")

# --- red thread of fate -------------------------------------------------------
TC = ((SA[0] + SB[0]) / 2 + 24, (SA[1] + SB[1]) / 2 - 96)
inside(*TC, 14, "thread crown")
d.path(f"M{SA[0]:.1f},{SA[1] - 30:.1f} Q{TC[0]:.1f},{TC[1]:.1f} {SB[0]:.1f},{SB[1] - 30:.1f}",
       "Red thread glow", fill=NONE, stroke=THREAD, strokeWidth=6, opacity=16,
       cap="round")
d.path(f"M{SA[0]:.1f},{SA[1] - 30:.1f} Q{TC[0]:.1f},{TC[1]:.1f} {SB[0]:.1f},{SB[1] - 30:.1f}",
       "Red thread", fill=NONE, stroke=THREAD, strokeWidth=2.2, opacity=86,
       cap="round")
for k in (1, 2, 3):
    t = k / 4
    tx, ty = bez2((SA[0], SA[1] - 30), TC, (SB[0], SB[1] - 30), t)
    d.shape("ellipse", f"Thread bead {k}", x=tx - 2.4, y=ty - 2.4, width=4.8,
            height=4.8, fill=GOLD_HI, opacity=85, stroke=NONE)

# --- magpie bridge -------------------------------------------------------------
for i, t in enumerate((0.34, 0.43, 0.52, 0.61, 0.70)):
    bx, by = bez2(A, C, B, t)
    bx += (i % 2 - 0.5) * 30
    by -= 44 + (i % 3) * 14
    inside(bx, by, 14, f"bridge {i}")
    qixi_magpie(bx, by, 0.95 + (i % 2) * 0.18, flip=1 if i % 2 else -1,
                label=f"Bridge magpie {i+1}")
# two magpies close together near the crown of the thread
mx, my = bez2(A, C, B, 0.5)[0] + 6, bez2(A, C, B, 0.5)[1] - 128
inside(mx, my, 14, "pair")
qixi_magpie(mx - 26, my + 4, 0.82, flip=1, label="Magpie pair L")
qixi_magpie(mx + 26, my - 2, 0.74, flip=-1, label="Magpie pair R")
# a pair crossing the quiet lower right
qixi_magpie(568, 606, 0.7, flip=1, label="Stray magpie")
qixi_magpie(642, 664, 0.55, flip=-1, label="Stray magpie B")
for gx, gy, gr in ((718, 590, 8), (612, 700, 7), (524, 566, 6)):
    sparkle(gx, gy, gr, col=STAR_WHITE, op=72, label=f"Far glint {gx}")

# --- night clouds at the foot of the disc --------------------------------------
cloud_drift_low(d, 340, 760, 150, "Cloud L", color="#8E86B8", opacity=12)
cloud_drift_low(d, 600, 782, 120, "Cloud R", color="#7E76AC", opacity=9)

# --- seal + caption --------------------------------------------------------------
CHX, CHY, CHW, CHH = 714, 148, 50, 136
inside(CHX + CHW, CHY + CHH, 6, "chop BR")
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW, height=CHH,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
p.chop("七夕", x=CHX, y=CHY, w=CHW, h=CHH, size=27)

p.caption("QIXI FESTIVAL", "七夕 · MAGPIE BRIDGE · NIGHT OF 7/7",
          name_color="#EDE8DC", sub_color="#A89EC8",
          name_size=52, sub_size=20, tracking_name=64, tracking_sub=120)
p.finish(SLUG)
