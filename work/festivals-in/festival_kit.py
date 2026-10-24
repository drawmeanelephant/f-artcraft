#!/usr/bin/env python3
"""Festival Seal — shared plate furniture for the Indian festival series.

The house plate grammar (1000x1000, disc centre 500,460 r420, caption at
934/970) lives in orient/plate.py.  This module adds the pieces these three
plates need and keeps them consistent:

    seal_disc   disc + rim without the oversized drop shadow that trips
                check_rim.py, plus a hugging shadow that stays inside r430
    glow        soft radial light pool
    dust        translucent flecks inside the disc (stars would sit outside)
    lamp        clay diya with a poured lip, cotton wick and layered flame
    rangoli     symmetric petal/dot rangoli in perspective
    garland     marigold + mango-leaf torana hung on the disc arc
    firework    radial burst with tipped rays and drifting sparks
    splash      gulal cloud / colour splash blob (Holi)
    deva_seal   square Devanagari seal stamped inside the disc, top right
    caption     name + Devanagari/Latin second line
"""
import math
import os
import sys

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORK not in sys.path:
    sys.path.insert(0, WORK)

from orient.plate import (NONE, INK, GOLD, GOLD_HI, GOLD_LO, PAPER, LATIN, DEVA,
                          PCX, PCY, PR, lin, rad, gold_lin, smooth, blend)

TAU = math.pi * 2


# --- backdrop / disc ---------------------------------------------------------
def seal_disc(p, top, bottom, rim=GOLD, rim2="#5E3A16", inner_ring=True):
    """Plate disc, with a shadow that stays inside the rim-check circle."""
    d = p.d
    d.shape("ellipse", "Plate shadow", x=PCX - 414, y=PCY - 408, width=828,
            height=828, fill=INK, opacity=30, stroke=NONE)
    d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
            fill=lin((0, 40), (0, 880), (0, top), (1, bottom)),
            stroke=rim2, strokeWidth=10)
    d.shape("ellipse", "Plate rim", x=86, y=46, width=828, height=828,
            fill=NONE, stroke=rim, strokeWidth=4)
    if inner_ring:
        d.shape("ellipse", "Plate inner ring", x=110, y=70, width=780,
                height=780, fill=NONE, stroke=rim, strokeWidth=2, opacity=62)


def glow(d, cx, cy, r, color, a=30, label="Glow", squash=1.0):
    d.shape("ellipse", label, x=cx - r, y=cy - r * squash,
            width=2 * r, height=2 * r * squash,
            fill=rad((0, color, a), (0.55, color, a * 0.35), (1, color, 0)),
            stroke=NONE)


def dust(d, n=54, r=400, colors=("#F6E3B8",), seed=11, smin=1.0, smax=2.8,
         opmin=10, opmax=32, label="Dust"):
    s = seed
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = (s / 2 ** 31) * TAU
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * math.sqrt(s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        sz = smin + (s / 2 ** 31) * (smax - smin)
        s = (1103515245 * s + 12345) % (2 ** 31)
        op = opmin + (s / 2 ** 31) * (opmax - opmin)
        x, y = PCX + math.cos(a) * rr, PCY + math.sin(a) * rr
        d.shape("ellipse", f"{label} {i+1}", x=round(x - sz / 2, 1),
                y=round(y - sz / 2, 1), width=round(sz, 1),
                height=round(sz, 1), fill=colors[i % len(colors)],
                opacity=round(op), stroke=NONE)


def ring_dots(d, r=398, n=48, size=3.0, color=GOLD, opacity=40, phase=-90,
              label="Ring dot"):
    for i in range(n):
        a = math.radians(phase + i * 360 / n)
        x, y = PCX + r * math.cos(a), PCY + r * math.sin(a)
        d.shape("ellipse", f"{label} {i+1}", x=round(x - size / 2, 1),
                y=round(y - size / 2, 1), width=size, height=size,
                fill=color, opacity=opacity, stroke=NONE)


# --- clay lamp ---------------------------------------------------------------
def flame(d, cx, base_y, h, w, lean=0.0, label="Flame", smoke=2):
    """Layered teardrop flame; h full height, w base width."""
    tipx, tipy = cx + lean * w, base_y - h
    d.path(f"M{cx - w*0.50:.1f},{base_y:.1f} "
           f"C{cx - w*0.64:.1f},{base_y - h*0.24:.1f} "
           f"{cx - w*0.26:.1f},{base_y - h*0.56:.1f} {tipx - w*0.03:.1f},{tipy:.1f} "
           f"C{tipx + w*0.26:.1f},{base_y - h*0.66:.1f} "
           f"{cx + w*0.62:.1f},{base_y - h*0.28:.1f} {cx + w*0.50:.1f},{base_y:.1f} "
           f"C{cx + w*0.24:.1f},{base_y + h*0.055:.1f} "
           f"{cx - w*0.24:.1f},{base_y + h*0.055:.1f} {cx - w*0.50:.1f},{base_y:.1f} Z",
           f"{label} outer",
           fill=lin(0, base_y - h, 0, base_y, (0, "#FFF4C6"), (0.34, "#FFD264"),
                    (0.66, "#FF9E3C"), (0.86, "#F2712C"), (1, "#DE4A22")),
           stroke=NONE, opacity=96)
    d.path(f"M{cx - w*0.31:.1f},{base_y:.1f} "
           f"C{cx - w*0.40:.1f},{base_y - h*0.26:.1f} "
           f"{cx - w*0.14:.1f},{base_y - h*0.58:.1f} {tipx - w*0.01:.1f},{tipy + h*0.16:.1f} "
           f"C{tipx + w*0.18:.1f},{base_y - h*0.60:.1f} "
           f"{cx + w*0.38:.1f},{base_y - h*0.26:.1f} {cx + w*0.31:.1f},{base_y:.1f} "
           f"C{cx + w*0.14:.1f},{base_y + h*0.04:.1f} "
           f"{cx - w*0.14:.1f},{base_y + h*0.04:.1f} {cx - w*0.31:.1f},{base_y:.1f} Z",
           f"{label} mid",
           fill=lin(0, base_y - h * 0.8, 0, base_y, (0, "#FFFFFF"), (0.45, "#FFF6C8"),
                    (0.8, "#FFE08A"), (1, "#FFC85E")), stroke=NONE, opacity=94)
    d.path(f"M{cx - w*0.15:.1f},{base_y:.1f} "
           f"C{cx - w*0.20:.1f},{base_y - h*0.24:.1f} "
           f"{cx - w*0.06:.1f},{base_y - h*0.44:.1f} {tipx + w*0.01:.1f},{tipy + h*0.44:.1f} "
           f"C{tipx + w*0.10:.1f},{base_y - h*0.44:.1f} "
           f"{cx + w*0.18:.1f},{base_y - h*0.22:.1f} {cx + w*0.15:.1f},{base_y:.1f} "
           f"C{cx + w*0.06:.1f},{base_y + h*0.02:.1f} "
           f"{cx - w*0.06:.1f},{base_y + h*0.02:.1f} {cx - w*0.15:.1f},{base_y:.1f} Z",
           f"{label} core", fill="#FFFFFF", opacity=86, stroke=NONE)
    for i in range(smoke):
        sx = tipx + (i - 0.5) * w * 0.16
        sy = tipy - h * 0.05
        d.path(f"M{sx:.1f},{sy:.1f} C{sx - w*0.16:.1f},{sy - h*0.12:.1f} "
               f"{sx + w*0.12:.1f},{sy - h*0.20:.1f} {sx + w*0.02:.1f},{sy - h*0.30:.1f}",
               f"{label} smoke {i+1}", fill=NONE, stroke="#E8C79A",
               strokeWidth=2.4, opacity=11, cap="round")


def lamp(d, cx, cy, w, label="Diya", flame_h=None, lean=0.0, sparks=0,
         glow_a=38, bowl=("#D9915E", "#A85C34", "#5E2A18"), rim_col="#F0B878"):
    """Clay diya, three-quarter front view.

    cy is the rim line, w the rim width.  A thick thrown rim, a small dark
    oil cavity, a pinched pouring lip at the front with a cotton wick, and a
    tall three-layer flame.
    """
    h = w * 0.42
    if flame_h is None:
        flame_h = w * 0.95
    # light pool
    d.shape("ellipse", f"{label} halo", x=cx - w * 0.80, y=cy - w * 1.12,
            width=w * 1.6, height=w * 1.6,
            fill=rad((0, "#FFC46B", glow_a), (0.42, "#FF8A3C", glow_a * 0.30),
                     (1, "#FF8A3C", 0)), stroke=NONE)
    # shadow on the floor
    d.shape("ellipse", f"{label} shadow", x=cx - w * 0.62, y=cy + h * 0.80,
            width=w * 1.24, height=w * 0.22,
            fill=rad((0, INK, 38), (0.55, INK, 20), (1, INK, 0)), stroke=NONE)
    # bowl body
    d.path(f"M{cx - w*0.50:.1f},{cy + h*0.06:.1f} "
           f"C{cx - w*0.50:.1f},{cy + h*0.62:.1f} "
           f"{cx - w*0.29:.1f},{cy + h:.1f} {cx:.1f},{cy + h:.1f} "
           f"C{cx + w*0.29:.1f},{cy + h:.1f} "
           f"{cx + w*0.50:.1f},{cy + h*0.62:.1f} {cx + w*0.50:.1f},{cy + h*0.06:.1f} "
           f"C{cx + w*0.30:.1f},{cy + h*0.20:.1f} "
           f"{cx - w*0.30:.1f},{cy + h*0.20:.1f} {cx - w*0.50:.1f},{cy + h*0.06:.1f} Z",
           f"{label} bowl",
           fill=lin((cx - w * 0.42, cy), (cx + w * 0.46, cy + h),
                    (0, bowl[0]), (0.40, bowl[1]), (1, bowl[2])),
           stroke=INK, strokeWidth=max(2.4, w * 0.013))
    # foot
    d.shape("ellipse", f"{label} foot", x=cx - w * 0.21, y=cy + h * 0.80,
            width=w * 0.42, height=w * 0.15,
            fill=lin(0, cy + h * 0.8, 0, cy + h, (0, "#8A4626"), (1, "#4A2014")),
            stroke=INK, strokeWidth=max(1.6, w * 0.008), opacity=92)
    # thick rim slab
    d.shape("ellipse", f"{label} rim", x=cx - w * 0.50, y=cy - h * 0.20,
            width=w, height=h * 0.40,
            fill=lin(0, cy - h * 0.2, 0, cy + h * 0.2,
                     (0, "#F2AE7C"), (0.45, "#D08452"), (1, "#9E5230")),
            stroke=INK, strokeWidth=max(2.2, w * 0.012))
    # oil cavity
    d.shape("ellipse", f"{label} oil", x=cx - w * 0.325, y=cy - h * 0.115,
            width=w * 0.65, height=h * 0.23,
            fill=lin(0, cy - h * 0.12, 0, cy + h * 0.12, (0, "#4A2414"),
                     (0.55, "#2E1410"), (1, "#1C0B08")), stroke="#3A1A10",
            strokeWidth=1.6, opacity=96)
    # oil sheen
    d.path(f"M{cx - w*0.26:.1f},{cy - h*0.02:.1f} "
           f"C{cx - w*0.10:.1f},{cy + h*0.06:.1f} {cx + w*0.10:.1f},{cy + h*0.06:.1f} "
           f"{cx + w*0.26:.1f},{cy - h*0.02:.1f}", f"{label} oil sheen",
           fill=NONE, stroke="#F2B888", strokeWidth=max(1.6, w * 0.007),
           opacity=34, cap="round")
    # pinched pouring lip at the front
    d.path(f"M{cx - w*0.145:.1f},{cy + h*0.055:.1f} "
           f"C{cx - w*0.115:.1f},{cy + h*0.16:.1f} "
           f"{cx - w*0.062:.1f},{cy + h*0.215:.1f} {cx:.1f},{cy + h*0.215:.1f} "
           f"C{cx + w*0.062:.1f},{cy + h*0.215:.1f} "
           f"{cx + w*0.115:.1f},{cy + h*0.16:.1f} {cx + w*0.145:.1f},{cy + h*0.055:.1f} "
           f"C{cx + w*0.075:.1f},{cy + h*0.115:.1f} "
           f"{cx - w*0.075:.1f},{cy + h*0.115:.1f} {cx - w*0.145:.1f},{cy + h*0.055:.1f} Z",
           f"{label} lip", fill=lin(0, cy + h * 0.05, 0, cy + h * 0.22,
                                     (0, "#F6C094"), (0.6, "#CE8250"), (1, "#8E4426")),
           stroke=INK, strokeWidth=max(1.7, w * 0.0085))
    d.shape("ellipse", f"{label} lip mouth", x=cx - w * 0.055, y=cy + h * 0.075,
            width=w * 0.11, height=h * 0.075, fill="#2A120C", stroke=NONE,
            opacity=90)
    # wick
    d.path(f"M{cx:.1f},{cy + h*0.14:.1f} C{cx - w*0.012:.1f},{cy + h*0.05:.1f} "
           f"{cx - w*0.018:.1f},{cy - h*0.06:.1f} {cx - w*0.012:.1f},{cy - h*0.16:.1f}",
           f"{label} wick", fill=NONE, stroke="#2E1B12",
           strokeWidth=max(2.0, w * 0.012), cap="round")
    # flame
    flame(d, cx, cy - h * 0.13, flame_h, w * 0.30, lean=lean,
          label=f"{label} flame")
    # painted bands on the belly
    d.path(f"M{cx - w*0.445:.1f},{cy + h*0.34:.1f} "
           f"Q{cx:.1f},{cy + h*0.66:.1f} {cx + w*0.445:.1f},{cy + h*0.34:.1f}",
           f"{label} band", fill=NONE, stroke=GOLD,
           strokeWidth=max(1.6, w * 0.009), opacity=66, cap="round")
    for i in range(7):
        t = (i + 0.5) / 7
        bx = cx - w * 0.33 + w * 0.66 * t
        by = cy + h * 0.52 + h * 0.085 * math.sin(math.pi * t)
        d.shape("ellipse", f"{label} band dot {i+1}", x=bx - w * 0.010,
                y=by - w * 0.010, width=w * 0.020, height=w * 0.020,
                fill=GOLD_HI, opacity=52, stroke=NONE)
    # sheen and rim light
    d.path(f"M{cx - w*0.40:.1f},{cy + h*0.16:.1f} "
           f"C{cx - w*0.375:.1f},{cy + h*0.50:.1f} {cx - w*0.24:.1f},{cy + h*0.78:.1f} "
           f"{cx - w*0.07:.1f},{cy + h*0.88:.1f}", f"{label} sheen",
           fill=NONE, stroke="#FFE2C0", strokeWidth=max(2.4, w * 0.015),
           opacity=24, cap="round")
    d.path(f"M{cx + w*0.435:.1f},{cy + h*0.14:.1f} "
           f"C{cx + w*0.425:.1f},{cy + h*0.48:.1f} {cx + w*0.32:.1f},{cy + h*0.74:.1f} "
           f"{cx + w*0.17:.1f},{cy + h*0.90:.1f}", f"{label} rim light",
           fill=NONE, stroke="#FFB878", strokeWidth=max(1.6, w * 0.008),
           opacity=38, cap="round")
    d.path(f"M{cx - w*0.47:.1f},{cy - h*0.05:.1f} "
           f"C{cx - w*0.30:.1f},{cy - h*0.14:.1f} {cx - w*0.05:.1f},{cy - h*0.16:.1f} "
           f"{cx + w*0.08:.1f},{cy - h*0.13:.1f}", f"{label} rim sheen",
           fill=NONE, stroke="#FFE6C8", strokeWidth=max(2.0, w * 0.011),
           opacity=30, cap="round")
    for i in range(sparks):
        a = math.radians(-104 + i * 26)
        rr = w * (0.52 + 0.10 * i)
        sx = cx + math.cos(a) * rr * 0.62
        sy = cy - h * 0.6 + math.sin(a) * rr * 0.58
        sz = w * (0.010 + 0.004 * (i % 3))
        d.shape("ellipse", f"{label} spark {i+1}", x=sx - sz, y=sy - sz,
                width=sz * 2, height=sz * 2, fill="#FFE6A8",
                opacity=72, stroke=NONE)


# --- rangoli -----------------------------------------------------------------
def _petal_path(P, a, r0, r1, half, sharp=True):
    ca, sa = math.cos(a), math.sin(a)
    ta, tb = -sa, ca
    b = (ca * r0, sa * r0)
    tp = (ca * r1, sa * r1)
    p1 = (b[0] + ta * half, b[1] + tb * half)
    p2 = (b[0] - ta * half, b[1] - tb * half)
    m1 = (b[0] + ca * (r1 - r0) * 0.52 + ta * half * 1.35,
          b[1] + sa * (r1 - r0) * 0.52 + tb * half * 1.35)
    m2 = (b[0] + ca * (r1 - r0) * 0.52 - ta * half * 1.35,
          b[1] + sa * (r1 - r0) * 0.52 - tb * half * 1.35)
    A, B, C, D, E, F = P(p1), P(m1), P(tp), P(m2), P(p2), P(b)
    if sharp:
        return (f"M{A[0]:.1f},{A[1]:.1f} Q{B[0]:.1f},{B[1]:.1f} {C[0]:.1f},{C[1]:.1f} "
                f"Q{D[0]:.1f},{D[1]:.1f} {E[0]:.1f},{E[1]:.1f} "
                f"Q{F[0]:.1f},{F[1]:.1f} {A[0]:.1f},{A[1]:.1f} Z")
    l1 = P((b[0] + ca * (r1 - r0) * 0.45 + ta * half * 1.5,
            b[1] + sa * (r1 - r0) * 0.45 + tb * half * 1.5))
    l2 = P((b[0] + ca * (r1 - r0) * 0.82 + ta * half * 1.12,
            b[1] + sa * (r1 - r0) * 0.82 + tb * half * 1.12))
    l3 = P((b[0] + ca * (r1 - r0) * 0.82 - ta * half * 1.12,
            b[1] + sa * (r1 - r0) * 0.82 - tb * half * 1.12))
    l4 = P((b[0] + ca * (r1 - r0) * 0.45 - ta * half * 1.5,
            b[1] + sa * (r1 - r0) * 0.45 - tb * half * 1.5))
    return (f"M{A[0]:.1f},{A[1]:.1f} C{l1[0]:.1f},{l1[1]:.1f} {l2[0]:.1f},{l2[1]:.1f} "
            f"{C[0]:.1f},{C[1]:.1f} C{l3[0]:.1f},{l3[1]:.1f} {l4[0]:.1f},{l4[1]:.1f} "
            f"{E[0]:.1f},{E[1]:.1f} Q{F[0]:.1f},{F[1]:.1f} {A[0]:.1f},{A[1]:.1f} Z")


def rangoli(d, cx, cy, rx, ry=None, col=(GOLD, "#F2A33C", "#C2455A", "#F6D9A0"),
            opacity=95, label="Rangoli", base="#4A1024"):
    """Dense symmetric rangoli in perspective: 32 / 16 / 8 petal rings + dots."""
    ry = rx * 0.39 if ry is None else ry
    k = ry / rx

    def P(q):
        return (cx + q[0], cy + q[1] * k)

    # dark carpet so the petals read
    d.shape("ellipse", f"{label} base", x=cx - rx, y=cy - ry, width=rx * 2,
            height=ry * 2, fill=rad((0, "#6A1830", 92), (0.65, base, 80),
                                    (1, base, 40)), stroke=INK,
            strokeWidth=2.4, opacity=88)
    # outer cream rim
    d.shape("ellipse", f"{label} rim", x=cx - rx * 0.995, y=cy - ry * 0.995,
            width=rx * 1.99, height=ry * 1.99, fill=NONE, stroke=col[3],
            strokeWidth=2.6, opacity=78)
    for frac, op in ((0.955, 40), (0.775, 34), (0.535, 32), (0.245, 30)):
        rr = rx * frac
        d.shape("ellipse", f"{label} guide {frac}", x=cx - rr, y=cy - rr * k,
                width=2 * rr, height=2 * rr * k, fill=NONE, stroke=col[3],
                strokeWidth=1.5, opacity=op)
    # ring A: 32 fine leaves
    for i in range(32):
        a = TAU * i / 32 - math.pi / 2
        d.path(_petal_path(P, a, rx * 0.79, rx * 0.955, rx * 0.0165),
               f"{label} leaf {i+1}", fill=col[0] if i % 2 else col[1],
               opacity=opacity, stroke=col[3], strokeWidth=0.9)
    # ring B: 16 lotus petals
    for i in range(16):
        a = TAU * i / 16 - math.pi / 2 + math.pi / 16
        d.path(_petal_path(P, a, rx * 0.545, rx * 0.775, rx * 0.045, sharp=False),
               f"{label} lotus {i+1}", fill=col[2] if i % 2 else "#E8791F",
               opacity=opacity - 2, stroke=col[3], strokeWidth=1.0)
    # ring C: 8 flame petals
    for i in range(8):
        a = TAU * i / 8 - math.pi / 2
        d.path(_petal_path(P, a, rx * 0.255, rx * 0.525, rx * 0.052),
               f"{label} flame {i+1}", fill=col[0], opacity=opacity - 4,
               stroke="#FFF0C8", strokeWidth=1.0)
    # dot rings
    for frac, n, s in ((0.885, 32, 0.010), (0.665, 24, 0.011),
                       (0.435, 16, 0.013), (0.155, 8, 0.014)):
        for i in range(n):
            a = TAU * i / n - math.pi / 2 + math.pi / n
            x, y = P((math.cos(a) * rx * frac, math.sin(a) * rx * frac))
            d.shape("ellipse", f"{label} dot {frac}-{i}", x=x - rx * s,
                    y=y - rx * s * k, width=2 * rx * s, height=2 * rx * s * k,
                    fill=col[3], opacity=min(96, opacity + 2), stroke=NONE)


# --- garland -----------------------------------------------------------------
def leaf_at(d, x, y, ang, h, w, fill="#2F6B3A", stroke="#163A1E", label="Leaf",
            vein=True):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    tx, ty = -sa, ca
    tip = (x + ca * h, y + sa * h)
    c1 = (x + ca * h * 0.28 + tx * w, y + sa * h * 0.28 + ty * w)
    c2 = (x + ca * h * 0.72 + tx * w * 0.62, y + sa * h * 0.72 + ty * w * 0.62)
    c3 = (x + ca * h * 0.72 - tx * w * 0.62, y + sa * h * 0.72 - ty * w * 0.62)
    c4 = (x + ca * h * 0.28 - tx * w, y + sa * h * 0.28 - ty * w)
    d.path(f"M{x:.1f},{y:.1f} C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} "
           f"{tip[0]:.1f},{tip[1]:.1f} C{c3[0]:.1f},{c3[1]:.1f} "
           f"{c4[0]:.1f},{c4[1]:.1f} {x:.1f},{y:.1f} Z",
           label, fill=fill, stroke=stroke, strokeWidth=1.8)
    if vein:
        d.path(f"M{x:.1f},{y:.1f} L{x + ca*h*0.86:.1f},{y + sa*h*0.86:.1f}",
               f"{label} vein", fill=NONE, stroke="#9AC98E", strokeWidth=1.4,
               opacity=45, cap="round")


def marigold_at(d, x, y, r, i, label="Marigold"):
    cols = [("#F2A33C", "#C9661A", "#F8CE84"),
            ("#E8791F", "#A8480E", "#F6B45C"),
            ("#F7C057", "#C2821C", "#FBE0A0")]
    c1, c2, c3 = cols[i % 3]
    for ring, (rr, n, cc) in enumerate([(r * 1.0, 11, c2), (r * 0.66, 9, c1),
                                       (r * 0.34, 6, c3)]):
        for j in range(n):
            a = TAU * j / n + ring * 0.28
            px, py = x + math.cos(a) * rr * 0.52, y + math.sin(a) * rr * 0.52
            d.shape("ellipse", f"{label} {i} petal {ring}-{j}",
                    x=round(px - rr * 0.30, 1), y=round(py - rr * 0.22, 1),
                    width=round(rr * 0.60, 1), height=round(rr * 0.44, 1),
                    fill=cc, opacity=96, stroke="#8A4010", strokeWidth=1.0,
                    rotation=round(math.degrees(a), 1))
    d.shape("ellipse", f"{label} {i} core", x=x - r * 0.12, y=y - r * 0.12,
            width=r * 0.24, height=r * 0.24, fill="#6E3208", stroke=NONE)


def garland(d, r=368, a0=-148, a1=-32, swags=4, sag=26, flower_r=16, label="Garland"):
    """Torana of marigolds + mango leaves hung on the disc's upper arc."""
    pts = []
    for i in range(swags):
        t0, t1 = i / swags, (i + 1) / swags
        A0 = math.radians(a0 + (a1 - a0) * t0)
        A1 = math.radians(a0 + (a1 - a0) * t1)
        p0 = (PCX + r * math.cos(A0), PCY + r * math.sin(A0))
        p1 = (PCX + r * math.cos(A1), PCY + r * math.sin(A1))
        am = (A0 + A1) / 2
        c = (PCX + (r - 2 * sag) * math.cos(am), PCY + (r - 2 * sag) * math.sin(am))
        d.path(f"M{p0[0]:.1f},{p0[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} "
               f"{p1[0]:.1f},{p1[1]:.1f}", f"{label} cord {i+1}", fill=NONE,
               stroke="#6E4A1A", strokeWidth=3.2, opacity=85, cap="round")
        pts.append((p0, c, p1))
    # flowers along each swag
    idx = 0
    for si, (p0, c, p1) in enumerate(pts):
        for t in (0.0, 0.34, 0.68):
            mt = 1 - t
            x = mt * mt * p0[0] + 2 * mt * t * c[0] + t * t * p1[0]
            y = mt * mt * p0[1] + 2 * mt * t * c[1] + t * t * p1[1]
            marigold_at(d, x, y, flower_r, idx, label)
            idx += 1
            # leaves between flowers
            for k, off in enumerate((0.17, 0.5)):
                tt = t + off * 0.34
                if tt >= 0.99:
                    continue
                mm = 1 - tt
                lx = mm * mm * p0[0] + 2 * mm * tt * c[0] + tt * tt * p1[0]
                ly = mm * mm * p0[1] + 2 * mm * tt * c[1] + tt * tt * p1[1]
                ang = 90 + (18 if k else -18) + (si - 1.5) * 4
                leaf_at(d, lx, ly, ang, 34, 8.5,
                        label=f"{label} leaf {si}-{k}")
    # last anchor flower
    p1 = pts[-1][2]
    marigold_at(d, p1[0], p1[1], flower_r, idx, label)


# --- fireworks ---------------------------------------------------------------
def firework(d, cx, cy, r, col1=GOLD, col2="#E06A7A", rays=18, seed=5,
             label="Firework"):
    d.shape("ellipse", f"{label} glow", x=cx - r * 1.15, y=cy - r * 1.15,
            width=r * 2.3, height=r * 2.3,
            fill=rad((0, col1, 26), (0.5, col1, 8), (1, col1, 0)), stroke=NONE)
    s = seed
    for i in range(rays):
        s = (1103515245 * s + 12345) % (2 ** 31)
        jitter = (s / 2 ** 31 - 0.5) * 0.10
        a = TAU * i / rays + jitter
        s = (1103515245 * s + 12345) % (2 ** 31)
        long = 0.74 + 0.26 * (s / 2 ** 31)
        x0, y0 = cx + math.cos(a) * r * 0.16, cy + math.sin(a) * r * 0.16
        x1, y1 = cx + math.cos(a) * r * long, cy + math.sin(a) * r * long
        col = col1 if i % 3 else col2
        d.shape("line", f"{label} ray {i+1}", x1=round(x0, 1), y1=round(y0, 1),
                x2=round(x1, 1), y2=round(y1, 1), stroke=col, strokeWidth=2.6,
                opacity=82, cap="round")
        d.shape("ellipse", f"{label} tip {i+1}", x=x1 - 2.6, y=y1 - 2.6,
                width=5.2, height=5.2, fill=col2 if i % 3 else "#FFF0C8",
                opacity=88, stroke=NONE)
        mx, my = cx + math.cos(a) * r * long * 0.62, cy + math.sin(a) * r * long * 0.62
        d.shape("ellipse", f"{label} mid {i+1}", x=mx - 1.5, y=my - 1.5,
                width=3, height=3, fill=col1, opacity=62, stroke=NONE)
    d.shape("ellipse", f"{label} core", x=cx - 4.5, y=cy - 4.5, width=9,
            height=9, fill="#FFF8DC", opacity=90, stroke=NONE)


# --- colour splash (Holi) ----------------------------------------------------
def splash(d, cx, cy, r, col, opacity=70, lobes=9, seed=3, label="Splash",
           streaky=True):
    """Irregular translucent colour blob with satellites and two streaks."""
    s = seed
    pts = []
    for i in range(lobes):
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (0.68 + 0.42 * (s / 2 ** 31))
        a = TAU * i / lobes
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.86))
    d.path(smooth(pts, closed=True), label, fill=col, opacity=opacity,
           stroke=NONE)
    for i in range(7):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = TAU * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (1.05 + 1.0 * (s / 2 ** 31))
        sz = 2.5 + 4.5 * (s % 100) / 100
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.9
        d.shape("ellipse", f"{label} dot {i+1}", x=x - sz / 2, y=y - sz / 2,
                width=sz, height=sz, fill=col, opacity=min(95, opacity + 10),
                stroke=NONE)
    if streaky:
        for k, (ang, ln) in enumerate(((-28, 1.9), (152, 1.5))):
            a = math.radians(ang)
            x1, y1 = cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9
            x2 = cx + math.cos(a) * r * ln
            y2 = cy + math.sin(a) * r * ln * 0.8
            d.path(f"M{x1:.1f},{y1:.1f} Q{(x1+x2)/2 - 18:.1f},{(y1+y2)/2 + 12:.1f} "
                   f"{x2:.1f},{y2:.1f}", f"{label} streak {k+1}", fill=NONE,
                   stroke=col, strokeWidth=max(3, r * 0.10), opacity=opacity * 0.75,
                   cap="round")


def gulal_cloud(d, cx, cy, r, col, opacity=46, puffs=11, seed=9, label="Gulal"):
    """Soft thrown colour cloud: overlapping radial puffs + a particle tail."""
    s = seed
    d.shape("ellipse", f"{label} heart", x=cx - r, y=cy - r * 0.9,
            width=2 * r, height=1.8 * r,
            fill=rad((0, col, min(90, opacity + 26)), (0.55, col, opacity),
                     (1, col, 0)), stroke=NONE)
    for i in range(puffs):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = TAU * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (0.28 + 0.64 * (s / 2 ** 31))
        s = (1103515245 * s + 12345) % (2 ** 31)
        pr = r * (0.24 + 0.26 * (s / 2 ** 31))
        px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr * 0.78
        d.shape("ellipse", f"{label} puff {i+1}", x=px - pr, y=py - pr * 0.9,
                width=pr * 2, height=pr * 1.8,
                fill=rad((0, col, opacity), (0.6, col, opacity * 0.55),
                         (1, col, 0)), stroke=NONE)
    # particle tail drifting downwind
    for i in range(9):
        s = (1103515245 * s + 12345) % (2 ** 31)
        t = i / 8
        px = cx + r * (0.55 + t * 1.0) + 10 * math.sin(i * 2.1)
        py = cy + r * (0.30 + t * 0.55)
        sz = 3.4 - t * 1.6
        d.shape("ellipse", f"{label} grain {i+1}", x=px - sz / 2, y=py - sz / 2,
                width=sz, height=sz, fill=col, opacity=72 - i * 3, stroke=NONE)


# --- seal + caption ----------------------------------------------------------
def deva_seal(d, text, cx=744, cy=214, s=62, size=26, fill=("#C0473A", "#7E1F1B")):
    x, y = cx - s / 2, cy - s / 2
    d.shape("ellipse", "Seal shadow", x=x + 3, y=y + 5, width=s, height=s,
            fill=INK, opacity=28, stroke=NONE)
    d.shape("rectangle", "Deva seal", x=x, y=y, width=s, height=s, radius=5,
            fill=lin((x, y), (x + s, y + s), (0, fill[0]), (1, fill[1])),
            stroke="#4E100E", strokeWidth=2.2)
    d.shape("rectangle", "Deva seal inner", x=x + 4.5, y=y + 4.5,
            width=s - 9, height=s - 9, radius=2.5, fill=NONE, stroke="#F6D9A0",
            strokeWidth=1.4, opacity=78)
    d.text(text, "Deva seal text", x=cx, y=cy + size * 0.34, size=size,
           font=DEVA, color="#FBE6B4", justify="center")
    for i in (-1, 1):
        d.shape("ellipse", f"Seal stud {i}", x=cx + i * (s * 0.5 - 7) - 1.6,
                y=cy + s * 0.5 - 8 - 1.6, width=3.2, height=3.2,
                fill="#F6D9A0", opacity=70, stroke=NONE)


def caption(p, name, sub, name_color=PAPER, sub_color="#C9A46A",
            name_size=52, sub_size=21, tracking_name=90, tracking_sub=46,
            sub_font=DEVA, name_font=LATIN, y1=934, y2=970):
    d = p.d
    n = d.text(name, "Name", x=PCX, y=y1, size=name_size, font=name_font,
               color=name_color, justify="center")
    s = d.text(sub, "Second line", x=PCX, y=y2, size=sub_size, font=sub_font,
               color=sub_color, justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=tracking_name)
    d.cmd("text.setStyle", "Sub tracking", ids=[s["id"]], tracking=tracking_sub)
    return n, s
