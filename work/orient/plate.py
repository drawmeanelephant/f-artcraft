#!/usr/bin/env python3
"""Shared plate system for the Orient series — Chinese zodiac, Chinese
festivals, Indian festivals, Indian symbols.

One canvas grammar, four dressings:

    backdrop -> plate disc -> rim -> field ornament -> subject -> seal text

The disc is always centre (500,460) r420, the name block always at the
bottom (name baseline 934, second line 970). Every piece is 1000x1000, so a
plate from any of the four series hangs next to the field plates.

House style holds: gradients and translucent shading, never flat fills;
warm dark ink, never pure black; check rims and proof edges before done.
"""
import os
import sys
import math

WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORK)
from vc import Draw, NONE  # noqa: E402

PCX, PCY, PR = 500, 460, 420
LATIN = "Virelai Sans"
CJK = "Noto Sans CJK SC"
DEVA = "ITF Devanagari"

INK = "#1D1216"          # warm near-black for outlines
GOLD = "#E8C074"
GOLD_HI = "#FBE6B4"
GOLD_LO = "#9A6A24"
PAPER = "#F4E7CE"


# --- paint -------------------------------------------------------------------
def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(*args):
    """lin((x0,y0),(x1,y1), stops...) or lin(x0,y0,x1,y1, stops...)."""
    if len(args) >= 4 and all(isinstance(v, (int, float)) for v in args[:4]):
        a, b, pairs = (args[0], args[1]), (args[2], args[3]), args[4:]
    else:
        a, b, pairs = args[0], args[1], args[2:]
    return {"gradient": {"kind": "linear",
                         "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)],
                         "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def gold_lin(y0=0, y1=1000, lo=GOLD_LO, mid=GOLD, hi=GOLD_HI):
    return lin((0, y0), (0, y1), (0, lo), (0.45, mid), (0.62, hi), (1, mid))


# --- geometry ----------------------------------------------------------------
def smooth(pts, closed=False, move=True):
    """Catmull-Rom through points as cubic Beziers."""
    n = len(pts)
    if n < 2:
        return ""
    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def ribbon(spine, widths, cap_round=True):
    """Closed path around a spine, width per point. Returns (d, left, right, norms)."""
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
    d = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    if cap_round:
        d += " A%.1f,%.1f 0 0 0 %.1f,%.1f " % (norms[-1][2], norms[-1][2], R[-1][0], R[-1][1])
    else:
        d += " L%.1f,%.1f " % R[-1]
    d += " ".join("L%.1f,%.1f" % p for p in reversed(R[:-1])) + " Z"
    return d, L, R, norms


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
            u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1])


def spiral(cx, cy, r0, r1, turns, n=90, phase=0.0):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = phase + t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def blend(hex_a, hex_b, t):
    """Mix two #rrggbb colours, t=0 -> a."""
    a = [int(hex_a[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(hex_b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


# --- plate builder -----------------------------------------------------------
class Plate:
    def __init__(self, title, w=1000, h=1000):
        self.d = Draw()
        self.w, self.h = w, h
        self.d.new_doc(title, w, h)

    # -- paper ---------------------------------------------------------------
    def backdrop(self, top="#121A24", bottom="#07090D", glow=None):
        d = self.d
        d.shape("rectangle", "Backdrop", x=0, y=0, width=self.w, height=self.h,
                fill=lin((0, 0), (0, self.h), (0, top), (1, bottom)), stroke=NONE)
        if glow:
            d.shape("ellipse", "Backdrop glow", x=110, y=70, width=780, height=780,
                    fill=rad((0, glow[0], glow[1]), (1, glow[0], 0)), stroke=NONE)

    def stars(self, n=34, color="#F6E3B8", seed=7, maxr=2.4, region=(30, 30, 940, 900)):
        d = self.d
        x0, y0, x1, y1 = region
        s = seed
        for i in range(n):
            s = (1103515245 * s + 12345) % (2**31)
            x = x0 + (s % 10000) / 10000 * (x1 - x0)
            s = (1103515245 * s + 12345) % (2**31)
            y = y0 + (s % 10000) / 10000 * (y1 - y0)
            s = (1103515245 * s + 12345) % (2**31)
            r = 0.7 + (s % 1000) / 1000 * maxr
            if math.hypot(x - PCX, y - PCY) < PR - 12:
                continue
            d.shape("ellipse", f"Star {i+1}", x=round(x, 1), y=round(y, 1),
                    width=round(r, 1), height=round(r, 1), fill=color,
                    opacity=28 + (s % 40), stroke=NONE)

    def disc(self, top, bottom, rim="#C79A46", rim2="#6E4A1A", inner_ring=True):
        d = self.d
        d.shape("ellipse", "Plate shadow", x=72, y=32, width=856, height=856,
                fill="#000000", opacity=28, stroke=NONE)
        d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
                fill=lin((0, 40), (0, 880), (0, top), (1, bottom)),
                stroke=rim2, strokeWidth=10)
        d.shape("ellipse", "Plate rim", x=86, y=46, width=828, height=828,
                fill=NONE, stroke=rim, strokeWidth=4)
        if inner_ring:
            d.shape("ellipse", "Plate inner ring", x=110, y=70, width=780, height=780,
                    fill=NONE, stroke=rim, strokeWidth=2, opacity=55)

    def ring_ticks(self, n=12, color=GOLD, r_in=376, r_out=394, width=3, phase=-90):
        for i in range(n):
            a = math.radians(phase + i * 360 / n)
            x0, y0 = PCX + r_in * math.cos(a), PCY + r_in * math.sin(a)
            x1, y1 = PCX + r_out * math.cos(a), PCY + r_out * math.sin(a)
            self.d.shape("line", f"Tick {i+1}", x1=round(x0, 1), y1=round(y0, 1),
                         x2=round(x1, 1), y2=round(y1, 1), stroke=color,
                         strokeWidth=width, opacity=80, cap="round")

    def ring_text(self, text, size=27, color=GOLD, r=368, phase=-90, opacity=72,
                  font=CJK):
        """Ring of characters, first at top, running clockwise, each upright."""
        n = len(text)
        for i, ch in enumerate(text):
            a = phase + i * 360 / n
            ar = math.radians(a)
            x, y = PCX + r * math.cos(ar), PCY + r * math.sin(ar)
            self.d.text(ch, f"Ring glyph {i+1}", x=round(x, 1),
                        y=round(y + size * 0.34, 1), size=size, font=font,
                        color=color, justify="center")

    def watermark(self, ch, size=330, color="#FFFFFF", bg="#5E1616", alpha=0.07, font=CJK):
        """Large translucent-looking character, pre-blended into the plate."""
        col = blend(bg, color, alpha)
        self.d.text(ch, "Watermark", x=PCX, y=round(PCY + size * 0.35, 1),
                    size=size, font=font, color=col, justify="center")

    def caption(self, name, sub, name_color=PAPER, sub_color="#C9A46A",
                name_size=52, sub_size=21, tracking_name=55, tracking_sub=180,
                sub_font=LATIN):
        d = self.d
        n = d.text(name, "Name", x=PCX, y=934, size=name_size, font=LATIN,
                   color=name_color, justify="center")
        s = d.text(sub, "Second line", x=PCX, y=970, size=sub_size, font=sub_font,
                   color=sub_color, justify="center")
        d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=tracking_name)
        d.cmd("text.setStyle", "Sub tracking", ids=[s["id"]], tracking=tracking_sub)
        return n, s

    def chop(self, text, x=878, y=96, w=54, h=150, fill="#9E2B25", color=GOLD_HI,
             size=30, font=CJK, horizontal=False):
        """Vertical seal column at the top right, outside the disc."""
        d = self.d
        d.shape("rectangle", "Chop", x=x, y=y, width=w, height=h, radius=4,
                fill=lin((x, y), (x + w, y + h), (0, "#B23A30"), (1, "#7E1F1B")),
                stroke="#5E1412", strokeWidth=2)
        d.shape("rectangle", "Chop inner", x=x + 4, y=y + 4, width=w - 8, height=h - 8,
                radius=2, fill=NONE, stroke=color, strokeWidth=1.5, opacity=70)
        if horizontal:
            d.text(text, "Chop text", x=x + w / 2, y=y + h * 0.68,
                   size=size, font=font, color=color, justify="center")
        else:
            step = (h - 24) / max(len(text), 1)
            for i, ch in enumerate(text):
                d.text(ch, f"Chop glyph {i+1}", x=x + w / 2, y=y + 12 + step * (i + 0.78),
                       size=size, font=font, color=color, justify="center")

    def finish(self, slug):
        return self.d.finish(slug)


# --- motifs ------------------------------------------------------------------
def cloud(d, cx, cy, s=1.0, label="Cloud", fill=GOLD, opacity=55, stroke=NONE, sw=0):
    """Ruyi / auspicious cloud, drawn as overlapping scallops with a tail."""
    p = []
    p.append(f"M{cx - 70*s:.1f},{cy + 16*s:.1f}")
    p.append(f"C{cx - 92*s:.1f},{cy - 2*s:.1f} {cx - 74*s:.1f},{cy - 30*s:.1f} {cx - 48*s:.1f},{cy - 26*s:.1f}")
    p.append(f"C{cx - 40*s:.1f},{cy - 52*s:.1f} {cx - 4*s:.1f},{cy - 56*s:.1f} {cx + 6*s:.1f},{cy - 30*s:.1f}")
    p.append(f"C{cx + 24*s:.1f},{cy - 46*s:.1f} {cx + 52*s:.1f},{cy - 34*s:.1f} {cx + 52*s:.1f},{cy - 8*s:.1f}")
    p.append(f"C{cx + 76*s:.1f},{cy - 6*s:.1f} {cx + 82*s:.1f},{cy + 26*s:.1f} {cx + 58*s:.1f},{cy + 30*s:.1f}")
    p.append(f"C{cx + 30*s:.1f},{cy + 38*s:.1f} {cx - 10*s:.1f},{cy + 34*s:.1f} {cx - 30*s:.1f},{cy + 34*s:.1f}")
    p.append(f"C{cx - 34*s:.1f},{cy + 48*s:.1f} {cx - 62*s:.1f},{cy + 44*s:.1f} {cx - 70*s:.1f},{cy + 16*s:.1f} Z")
    d.path(" ".join(p), label, fill=fill, opacity=opacity, stroke=stroke,
           strokeWidth=sw if sw else 0)
    sp = spiral(cx - 22 * s, cy + 2 * s, 2 * s, 15 * s, 1.55, 34, phase=math.radians(200))
    d.path(smooth(sp), f"{label} curl", fill=NONE,
           stroke=stroke if stroke != NONE else "#FFFFFF",
           strokeWidth=max(1.4, 2.2 * s), opacity=min(85, opacity + 20), cap="round")


def coin(d, cx, cy, r, label="Coin", fill=None, stroke=INK, sw=4, square=0.34):
    fill = fill or gold_lin(cy - r, cy + r)
    d.shape("ellipse", label, x=cx - r, y=cy - r, width=2 * r, height=2 * r,
            fill=fill, stroke=stroke, strokeWidth=sw)
    d.shape("ellipse", f"{label} inner", x=cx - r * 0.82, y=cy - r * 0.82,
            width=r * 1.64, height=r * 1.64, fill=NONE, stroke=stroke,
            strokeWidth=1.4, opacity=45)
    s = r * square
    d.shape("rectangle", f"{label} hole", x=cx - s, y=cy - s, width=2 * s, height=2 * s,
            fill="#241512", stroke=stroke, strokeWidth=2)


def blossom(d, cx, cy, r, petals=5, label="Blossom", fill="#F2C6CF",
            core="#C2455A", stroke=NONE, rot=-90, opacity=95):
    for i in range(petals):
        a = math.radians(rot + i * 360 / petals)
        px, py = cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62
        d.shape("ellipse", f"{label} petal {i+1}", x=round(px - r * 0.48, 1),
                y=round(py - r * 0.38, 1), width=round(r * 0.96, 1),
                height=round(r * 0.76, 1), fill=fill, opacity=opacity,
                stroke=stroke, strokeWidth=1.5,
                rotation=round(math.degrees(a) + 90, 1))
    d.shape("ellipse", f"{label} core", x=cx - r * 0.2, y=cy - r * 0.2,
            width=r * 0.4, height=r * 0.4, fill=core, stroke=NONE)
    for i in range(5):
        a = math.radians(rot + 36 + i * 72)
        d.shape("ellipse", f"{label} stamen {i+1}",
                x=cx + math.cos(a) * r * 0.28 - 2, y=cy + math.sin(a) * r * 0.28 - 2,
                width=4, height=4, fill="#F8E3A8", stroke=NONE)


def lantern(d, cx, cy, w, h, label="Lantern", body=("#D9433B", "#8E1F1E"),
            gold=GOLD, tassel=True, glow=True):
    if glow:
        d.shape("ellipse", f"{label} glow", x=cx - w * 1.1, y=cy - h * 0.9,
                width=w * 2.2, height=h * 1.9,
                fill=rad((0, "#FFB36B", 26), (1, "#FFB36B", 0)), stroke=NONE)
    d.shape("rectangle", f"{label} cap top", x=cx - w * 0.34, y=cy - h / 2 - 9,
            width=w * 0.68, height=12, radius=3, fill=gold_lin(cy - h, cy),
            stroke=INK, strokeWidth=2)
    d.shape("rectangle", f"{label} cap bottom", x=cx - w * 0.34, y=cy + h / 2 - 3,
            width=w * 0.68, height=12, radius=3, fill=gold_lin(cy, cy + h),
            stroke=INK, strokeWidth=2)
    d.shape("ellipse", label, x=cx - w / 2, y=cy - h / 2, width=w, height=h,
            fill=rad((0, body[0]), (1, body[1])), stroke=INK, strokeWidth=4)
    for k in (-0.52, -0.26, 0, 0.26, 0.52):
        x = cx + k * w
        d.path(f"M{x:.1f},{cy - h * 0.46:.1f} C{x + 10:.1f},{cy - h * 0.15:.1f} "
               f"{x + 10:.1f},{cy + h * 0.15:.1f} {x:.1f},{cy + h * 0.46:.1f}",
               f"{label} rib {k}", fill=NONE, stroke="#F6B07A", strokeWidth=2.2,
               opacity=45, cap="round")
    d.shape("ellipse", f"{label} sheen", x=cx - w * 0.34, y=cy - h * 0.36,
            width=w * 0.26, height=h * 0.4, fill="#FFFFFF", opacity=18, stroke=NONE)
    d.path(f"M{cx:.1f},{cy - h / 2 - 9:.1f} C{cx - 6:.1f},{cy - h / 2 - 34:.1f} "
           f"{cx + 18:.1f},{cy - h / 2 - 40:.1f} {cx + 22:.1f},{cy - h / 2 - 22:.1f}",
           f"{label} loop", fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
    if tassel:
        d.shape("rectangle", f"{label} tassel knot", x=cx - 5, y=cy + h / 2 + 9,
                width=10, height=10, radius=3, fill=gold, stroke=INK, strokeWidth=1.5)
        for i, dx in enumerate((-7, 0, 7)):
            d.path(f"M{cx + dx:.1f},{cy + h / 2 + 17:.1f} "
                   f"C{cx + dx * 1.6:.1f},{cy + h / 2 + 44:.1f} "
                   f"{cx + dx * 1.4:.1f},{cy + h / 2 + 64:.1f} "
                   f"{cx + dx * 1.2:.1f},{cy + h / 2 + 78:.1f}",
                   f"{label} tassel {i+1}", fill=NONE, stroke="#C03A2E",
                   strokeWidth=3, cap="round")


def lotus(d, cx, cy, r, label="Lotus", petal="#F6BCCB", petal2="#E98AA6",
          edge="#B94A6A", core=GOLD):
    for row, (rr, n, tilt, col, op) in enumerate([
            (r * 0.98, 9, 0.74, petal2, 80),
            (r * 0.76, 7, 0.86, petal, 92),
            (r * 0.52, 5, 1.0, "#FBD9E1", 96)]):
        for i in range(n):
            a = math.radians(-90 + (i - (n - 1) / 2) * 26 * tilt)
            px, py = cx + math.cos(a) * rr * 0.62, cy + math.sin(a) * rr * 0.42
            d.path(f"M{cx:.1f},{cy + r * 0.30:.1f} "
                   f"C{cx + math.cos(a - 0.28) * rr * 0.6:.1f},{cy + math.sin(a - 0.28) * rr * 0.75:.1f} "
                   f"{px + math.cos(a) * rr * 0.2:.1f},{py - rr * 0.28:.1f} {px:.1f},{py - rr * 0.42:.1f} "
                   f"C{px - math.cos(a) * rr * 0.12:.1f},{py - rr * 0.2:.1f} "
                   f"{cx + math.cos(a + 0.3) * rr * 0.55:.1f},{cy + math.sin(a + 0.3) * rr * 0.7:.1f} "
                   f"{cx:.1f},{cy + r * 0.30:.1f} Z",
                   f"{label} petal {row+1}-{i+1}", fill=col, opacity=op,
                   stroke=edge, strokeWidth=2)
    d.shape("ellipse", f"{label} core", x=cx - r * 0.14, y=cy - r * 0.05,
            width=r * 0.28, height=r * 0.2, fill=core, stroke=NONE)
    for i in range(7):
        a = math.radians(200 + i * 23)
        d.shape("ellipse", f"{label} stamen {i+1}",
                x=cx + math.cos(a) * r * 0.22 - 2, y=cy + math.sin(a) * r * 0.12 - 2,
                width=4, height=4, fill="#FFF0C0", stroke=NONE)


def marigold(d, cx, cy, r, label="Marigold", petals=14, col="#F2A33C", col2="#D9701C"):
    for ring, (rr, n, c) in enumerate([(r, petals, col2), (r * 0.66, petals - 3, col),
                                       (r * 0.36, 9, "#F7C96A")]):
        for i in range(n):
            a = math.radians(i * 360 / n + ring * 8)
            px, py = cx + math.cos(a) * rr * 0.55, cy + math.sin(a) * rr * 0.55
            d.shape("ellipse", f"{label} petal {ring}-{i}",
                    x=px - rr * 0.24, y=py - rr * 0.17, width=rr * 0.48,
                    height=rr * 0.34, fill=c, stroke="#9A4A12", strokeWidth=1.2,
                    rotation=math.degrees(a))
    d.shape("ellipse", f"{label} core", x=cx - r * 0.15, y=cy - r * 0.15,
            width=r * 0.3, height=r * 0.3, fill="#8A4510", stroke=NONE)


def diya(d, cx, cy, w=150, label="Diya", flame=True):
    """Clay oil lamp, three-quarter: bowl, lip, flame."""
    if flame:
        d.shape("ellipse", f"{label} halo", x=cx - w * 0.9, y=cy - w * 1.25,
                width=w * 1.8, height=w * 1.8,
                fill=rad((0, "#FFC46B", 45), (0.55, "#FF8A3C", 14), (1, "#FF8A3C", 0)),
                stroke=NONE)
        d.path(f"M{cx:.1f},{cy - w * 0.22:.1f} C{cx - w * 0.16:.1f},{cy - w * 0.5:.1f} "
               f"{cx - w * 0.05:.1f},{cy - w * 0.78:.1f} {cx + w * 0.04:.1f},{cy - w * 0.96:.1f} "
               f"C{cx + w * 0.18:.1f},{cy - w * 0.7:.1f} {cx + w * 0.12:.1f},{cy - w * 0.44:.1f} "
               f"{cx:.1f},{cy - w * 0.22:.1f} Z",
               f"{label} flame", fill=lin(0, cy - w, 0, cy,
                                           (0, "#FFF6C8"), (0.5, "#FFC24E"), (1, "#F26A2E")),
               stroke=NONE)
        d.path(f"M{cx:.1f},{cy - w * 0.34:.1f} C{cx - w * 0.04:.1f},{cy - w * 0.52:.1f} "
               f"{cx + w * 0.02:.1f},{cy - w * 0.66:.1f} {cx + w * 0.04:.1f},{cy - w * 0.76:.1f} "
               f"C{cx + w * 0.1:.1f},{cy - w * 0.58:.1f} {cx + w * 0.06:.1f},{cy - w * 0.44:.1f} "
               f"{cx:.1f},{cy - w * 0.34:.1f} Z", f"{label} flame core",
               fill="#FFFBE4", opacity=85, stroke=NONE)
    d.path(f"M{cx - w * 0.5:.1f},{cy - w * 0.16:.1f} "
           f"C{cx - w * 0.48:.1f},{cy + w * 0.16:.1f} {cx - w * 0.24:.1f},{cy + w * 0.32:.1f} {cx:.1f},{cy + w * 0.32:.1f} "
           f"C{cx + w * 0.24:.1f},{cy + w * 0.32:.1f} {cx + w * 0.48:.1f},{cy + w * 0.16:.1f} {cx + w * 0.5:.1f},{cy - w * 0.16:.1f} Z",
           f"{label} bowl", fill=lin(0, cy - w * 0.16, 0, cy + w * 0.32,
                                      (0, "#C46A3C"), (0.55, "#9A4A28"), (1, "#5E2A18")),
           stroke="#4A2014", strokeWidth=3)
    d.path(f"M{cx - w * 0.52:.1f},{cy - w * 0.16:.1f} "
           f"C{cx - w * 0.3:.1f},{cy - w * 0.08:.1f} {cx + w * 0.3:.1f},{cy - w * 0.08:.1f} {cx + w * 0.52:.1f},{cy - w * 0.16:.1f}",
           f"{label} lip", fill=NONE, stroke="#E8A06A", strokeWidth=7, cap="round")
    d.path(f"M{cx - w * 0.3:.1f},{cy + w * 0.12:.1f} C{cx - w * 0.14:.1f},{cy + w * 0.18:.1f} "
           f"{cx + w * 0.02:.1f},{cy + w * 0.18:.1f} {cx + w * 0.16:.1f},{cy + w * 0.12:.1f}",
           f"{label} glaze", fill=NONE, stroke="#F2C08A", strokeWidth=3, opacity=45, cap="round")


def mango_leaf(d, x, y, h, w, label="Mango leaf", fill="#2F6B3A"):
    d.path(f"M{x:.1f},{y:.1f} C{x - w:.1f},{y + h * 0.32:.1f} "
           f"{x - w * 0.5:.1f},{y + h * 0.82:.1f} {x:.1f},{y + h:.1f} "
           f"C{x + w * 0.5:.1f},{y + h * 0.82:.1f} {x + w:.1f},{y + h * 0.32:.1f} {x:.1f},{y:.1f} Z",
           label, fill=fill, stroke="#163A1E", strokeWidth=2)
    d.path(f"M{x:.1f},{y + h * 0.08:.1f} L{x:.1f},{y + h * 0.92:.1f}",
           f"{label} vein", fill=NONE, stroke="#8CC08A", strokeWidth=1.6, opacity=55)


def torana(d, cy=150, cx=PCX, span=620, color="#E8A33C", leaf="#2F6B3A"):
    """Mango-leaf string across the top of the disc."""
    d.path(f"M{cx - span/2:.1f},{cy:.1f} C{cx - span/4:.1f},{cy + 70:.1f} "
           f"{cx + span/4:.1f},{cy + 70:.1f} {cx + span/2:.1f},{cy:.1f}",
           "Torana string", fill=NONE, stroke="#6E4A1A", strokeWidth=3, opacity=80)
    for i in range(9):
        t = i / 8
        x = cx - span / 2 + span * t
        y = cy + 70 * math.sin(math.pi * t) * 0.5
        d.path(f"M{x:.1f},{y:.1f} L{x:.1f},{y + 16:.1f}", f"Torana drop {i+1}",
               fill=NONE, stroke="#6E4A1A", strokeWidth=1.6, opacity=70)
        mango_leaf(d, x, y + 14, 46, 13, label=f"Torana leaf {i+1}", fill=leaf)
        d.shape("ellipse", f"Torana bead {i+1}", x=x - 4, y=y + 60, width=8,
                height=8, fill=color, stroke="#6E4A1A", strokeWidth=1)


def rangoli_ring(d, cx, cy, r, petals=16, col=(GOLD, "#D9701C", "#F2C6CF"), opacity=55):
    for i in range(petals):
        a = math.radians(i * 360 / petals)
        px, py = cx + math.cos(a) * r * 0.72, cy + math.sin(a) * r * 0.72
        d.shape("ellipse", f"Rangoli petal {i+1}", x=px - r * 0.1, y=py - r * 0.07,
                width=r * 0.2, height=r * 0.14, fill=col[i % len(col)],
                opacity=opacity, stroke=NONE, rotation=math.degrees(a))
    for rr, n in ((r * 0.5, 12), (r * 0.32, 8)):
        for i in range(n):
            a = math.radians(i * 360 / n + 8)
            d.shape("ellipse", f"Rangoli dot {rr}-{i}",
                    x=cx + math.cos(a) * rr - 3, y=cy + math.sin(a) * rr - 3,
                    width=6, height=6, fill=col[1], opacity=opacity, stroke=NONE)


# --- text helpers ------------------------------------------------------------
def vertical_text(d, text, x, y, size, color, font=CJK, gap=1.18, label="Vertical"):
    ids = []
    for i, ch in enumerate(text):
        t = d.text(ch, f"{label} {i+1}", x=x, y=y + i * size * gap, size=size,
                   font=font, color=color, justify="center")
        ids.append(t["id"])
    return ids
