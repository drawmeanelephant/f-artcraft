#!/usr/bin/env python3
"""Zodiac plate base — the Celestial Seal series.

One seal per animal: element-coloured disc, a ring of the twelve earthly
branches, the branch character as a watermark, the animal as a bold
paper-cut bust, and the years it governs. 1000x1000.
"""
import math
import sys

from orient.plate import (Plate, PCX, PCY, PR, INK, GOLD, GOLD_HI, GOLD_LO,
                          PAPER, LATIN, CJK, lin, rad, gold_lin, smooth,
                          blossom, cloud, coin, blend, bez, ribbon, NONE)

ELEMENTS = {
    "wood":  {"disc": ("#24503A", "#0B1F15"), "accent": "#9FD8A8",
              "glow": "#2E7A50", "rim": "#C9A45A", "rim2": "#4E3416"},
    "fire":  {"disc": ("#5C1814", "#240707"), "accent": "#F4A45E",
              "glow": "#8E2A1E", "rim": "#D8A24E", "rim2": "#5A2A12"},
    "earth": {"disc": ("#4E3014", "#1C0E04"), "accent": "#E8B76A",
              "glow": "#7A4E22", "rim": "#D0A052", "rim2": "#4E3414"},
    "metal": {"disc": ("#3A424A", "#111419"), "accent": "#DEE4EA",
              "glow": "#4E5A66", "rim": "#C9C2AC", "rim2": "#3A3E44"},
    "water": {"disc": ("#103448", "#05111A"), "accent": "#8FD4F2",
              "glow": "#1C5570", "rim": "#B9A46A", "rim2": "#3A3A2A"},
}

BRANCHES = "子丑寅卯辰巳午未申酉戌亥"


class ZodiacPlate(Plate):
    def __init__(self, slug, name, char, branch, element, years, title):
        super().__init__(f"{title} — Celestial Seal", 1000, 1000)
        self.slug = slug
        self.element = ELEMENTS[element]
        self.branch = branch
        d = self.d
        e = self.element
        self.backdrop(top="#111821", bottom="#05070A", glow=(e["glow"], 12))
        self.stars(n=40, color=e["accent"], seed=sum(ord(c) for c in slug) or 11, maxr=2.2)
        self.disc(e["disc"][0], e["disc"][1], rim=e["rim"], rim2=e["rim2"])
        # soft element glow behind the animal, so the bust sits in light
        d.shape("ellipse", "Disc aura", x=196, y=156, width=608, height=608,
                fill=rad((0, e["accent"], 16), (0.55, e["accent"], 6),
                         (1, e["accent"], 0)), stroke=NONE)
        self.ring_ticks(n=12, color=e["rim"], width=3)
        self.ring_text(BRANCHES, size=21, color=e["rim"], r=400, opacity=72)
        # seal stamp at the top right, outside the disc
        d.shape("rectangle", "Branch seal", x=874, y=94, width=48, height=48,
                radius=3, fill=lin((874, 94), (922, 142), (0, "#B23A30"), (1, "#7E1F1B")),
                stroke="#5E1412", strokeWidth=2)
        d.text(branch, "Branch seal glyph", x=898, y=130, size=28, font=CJK,
               color=GOLD_HI, justify="center")
        self.name = name
        self.char = char
        self.years = years

    def close(self):
        self.caption(self.name, f"{self.char} · {self.years}",
                     name_color="#F0E2C4", sub_color=self.element["rim"],
                     name_size=50, sub_size=21, tracking_name=90,
                     tracking_sub=150)
        return self.finish(self.slug)


# --- shared animal parts -----------------------------------------------------
def almond_eye(d, cx, cy, w, h, label, iris="#F2C15C", iris2="#A86A1E",
               pupil="#20140E", tilt=0, look=(0, 0), lid=True):
    """Big expressive seal eye; tilt in degrees, look in -1..1 units."""
    d.shape("ellipse", f"{label} socket", x=cx - w * 0.58, y=cy - h * 0.62,
            width=w * 1.16, height=h * 1.24, fill="#2A1A16", opacity=28,
            stroke=NONE, rotation=tilt)
    d.shape("ellipse", f"{label} white", x=cx - w / 2, y=cy - h / 2,
            width=w, height=h, fill=rad((0, "#FFFDF2"), (1, "#E8DCC4")),
            stroke=INK, strokeWidth=4, rotation=tilt)
    ix, iy = cx + look[0] * w * 0.14, cy + look[1] * h * 0.12
    d.shape("ellipse", f"{label} iris", x=ix - w * 0.27, y=iy - h * 0.34,
            width=w * 0.54, height=h * 0.68,
            fill=rad((0, iris), (0.65, iris), (1, iris2)), stroke=INK,
            strokeWidth=2, rotation=tilt)
    d.shape("ellipse", f"{label} pupil", x=ix - w * 0.11, y=iy - h * 0.26,
            width=w * 0.22, height=h * 0.52, fill=pupil, stroke=NONE,
            rotation=tilt)
    d.shape("ellipse", f"{label} glint", x=ix - w * 0.05, y=iy - h * 0.18,
            width=w * 0.13, height=h * 0.16, fill="#FFFFFF", stroke=NONE,
            rotation=tilt)
    if lid:
        d.path(f"M{cx - w * 0.55:.1f},{cy - h * 0.35:.1f} "
               f"C{cx - w * 0.2:.1f},{cy - h * 0.72:.1f} "
               f"{cx + w * 0.24:.1f},{cy - h * 0.68:.1f} {cx + w * 0.55:.1f},{cy - h * 0.3:.1f}",
               f"{label} lid", fill=NONE, stroke=INK, strokeWidth=5, cap="round")


def brow(d, cx, cy, w, label, color=INK, tilt=0, sw=8):
    d.path(f"M{cx - w / 2:.1f},{cy:.1f} Q{cx:.1f},{cy - w * 0.22:.1f} {cx + w / 2:.1f},{cy + tilt:.1f}",
           label, fill=NONE, stroke=color, strokeWidth=sw, cap="round")


def blush(d, cx, cy, r, label, color="#E8705E", opacity=30):
    d.shape("ellipse", label, x=cx - r, y=cy - r * 0.6, width=r * 2, height=r * 1.2,
            fill=rad((0, color, opacity), (1, color, 0)), stroke=NONE)


def fang(d, x, y, w, h, label, fill="#FFF8E6", stroke=INK, sw=2):
    d.path(f"M{x - w / 2:.1f},{y:.1f} L{x + w / 2:.1f},{y:.1f} "
           f"C{x + w * 0.3:.1f},{y + h * 0.55:.1f} {x + w * 0.05:.1f},{y + h:.1f} "
           f"{x:.1f},{y + h:.1f} C{x - w * 0.05:.1f},{y + h:.1f} "
           f"{x - w * 0.3:.1f},{y + h * 0.55:.1f} {x - w / 2:.1f},{y:.1f} Z",
           label, fill=fill, stroke=stroke, strokeWidth=sw)


def whisker(d, x0, y0, cx1, cy1, x1, y1, label, color=GOLD_HI, sw=3.2, op=85):
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx1:.1f},{cy1:.1f} {x1:.1f},{y1:.1f}",
           label, fill=NONE, stroke=color, strokeWidth=sw, opacity=op, cap="round")


def scale_rows(d, cx, cy, w, rows, label, color="#2A5A46", hi="#8FD8B4", sw=2.2):
    """Rows of overlapping scallops, decreasing width downward."""
    for r in range(rows):
        y = cy + r * 17
        n = max(3, int(w / 34) - r // 2)
        span = w * (1 - r * 0.045)
        for i in range(n):
            x = cx - span / 2 + span * (i + 0.5) / n
            radius = span / n * 0.62
            d.path(f"M{x - radius:.1f},{y:.1f} A{radius:.1f},{radius * 0.85:.1f} 0 0 1 "
                   f"{x + radius:.1f},{y:.1f}", f"{label} scale {r}-{i}",
                   fill=NONE, stroke=color, strokeWidth=sw, opacity=55, cap="round")
            d.path(f"M{x - radius * 0.55:.1f},{y - 1:.1f} A{radius * 0.55:.1f},{radius * 0.5:.1f} 0 0 1 "
                   f"{x + radius * 0.1:.1f},{y - 1:.1f}", f"{label} glint {r}-{i}",
                   fill=NONE, stroke=hi, strokeWidth=1.4, opacity=40, cap="round")


def bust(d, body_fill, top=520, bottom=772, half_top=58, half_bottom=200,
         stroke=INK, sw=7, legs=True, leg_fill=None, paw_fill=None,
         paw_line="#5A3A1A", collar=None):
    """Generic seated bust: torso, two forelegs, paws. Returns paw centres."""
    BODY = (f"M{500-half_bottom},{bottom} "
            f"C{500-half_bottom},{bottom-82} {500-half_bottom+18},{bottom-152} "
            f"{500-half_bottom+62},{bottom-198} "
            f"C{500-half_bottom+98},{bottom-232} {500-half_top+42},{top} 500,{top} "
            f"C{500+half_top-42},{top} {500+half_bottom-98},{bottom-232} "
            f"{500+half_bottom-62},{bottom-198} "
            f"C{500+half_bottom-18},{bottom-152} {500+half_bottom},{bottom-82} "
            f"{500+half_bottom},{bottom} Z")
    d.shape("ellipse", "Body shadow", x=500-half_bottom+10, y=bottom-26,
            width=(half_bottom-10)*2, height=54, fill="#000000", opacity=26, stroke=NONE)
    BODY = BODY[:-2] + f" Q500,{bottom-30} {500-half_bottom},{bottom} Z"
    d.path(BODY, "Body", fill=body_fill, stroke=stroke, strokeWidth=sw)
    if collar:
        d.path(f"M{500-half_top-2},{top+16} C{500-30},{top-2} {500+30},{top-2} "
               f"{500+half_top+2},{top+16}", "Collar", fill=NONE,
               stroke=collar, strokeWidth=13, cap="round")
    paws = []
    if legs:
        lf = leg_fill if leg_fill is not None else body_fill
        for sign, nm in ((-1, "L"), (1, "R")):
            x0 = 500 + sign * 142
            leg = (f"M{x0:.1f},{top+66} C{x0 - sign*26:.1f},{top+106} "
                   f"{x0 - sign*34:.1f},{top+162} {x0 - sign*26:.1f},{top+204} "
                   f"L{x0 + sign*26:.1f},{top+204} "
                   f"C{x0 + sign*34:.1f},{top+162} {x0 + sign*26:.1f},{top+108} "
                   f"{x0 + sign*14:.1f},{top+72} Z")
            d.path(leg, f"Foreleg {nm}", fill=lf, stroke=stroke, strokeWidth=sw-1)
            d.path(f"M{x0 - sign*10:.1f},{top+82} C{x0 - sign*22:.1f},{top+120} "
                   f"{x0 - sign*20:.1f},{top+170} {x0 - sign*16:.1f},{top+194}",
                   f"Foreleg light {nm}", fill=NONE, stroke="#FFFFFF", strokeWidth=5,
                   opacity=22, cap="round")
            cx, cy = x0, top + 210
            d.shape("ellipse", f"Paw {nm}", x=cx - 30, y=cy - 16, width=60, height=42,
                    fill=paw_fill if paw_fill is not None else lf, stroke=stroke,
                    strokeWidth=sw-2)
            for j, dx in enumerate((-14, 0, 14)):
                d.path(f"M{cx + dx:.1f},{cy + 2:.1f} L{cx + dx:.1f},{cy + 16:.1f}",
                       f"Toe {nm}{j+1}", fill=NONE, stroke=paw_line, strokeWidth=2.4,
                       opacity=55, cap="round")
            paws.append((cx, cy))
    return paws


def curved_horn(d, cx, cy, sign, length, label, fill="#E8D8B0", stroke=INK, sw=6,
                curve=0.55, width=26):
    """A solid tapered horn: quadratic spine, ribbon body, ridge rings."""
    p0 = (cx, cy)
    p1 = (cx + sign * length * curve, cy - length * 0.42)
    p2 = (cx + sign * length * 0.78, cy - length * 0.82)
    p3 = (cx + sign * length * 0.52, cy - length)
    n = 14
    spine = [bez(p0, p1, p2, p3, i / n) for i in range(n + 1)]
    widths = [max(3, width * (1 - 0.92 * (i / n) ** 0.85)) for i in range(n + 1)]
    dd, L, R, norms = ribbon(spine, widths)
    d.path(dd, label, fill=fill, stroke=stroke, strokeWidth=sw)
    for k in (0.18, 0.38, 0.58, 0.76):
        idx = int(k * n)
        (x, y), (nx, ny, w) = spine[idx], norms[idx]
        d.path(f"M{x - nx*w*0.85:.1f},{y - ny*w*0.85:.1f} "
               f"Q{x + nx*w*0.25:.1f},{y + ny*w*0.25:.1f} "
               f"{x + nx*w*0.75:.1f},{y + ny*w*0.75:.1f}",
               f"{label} ridge {k}", fill=NONE, stroke="#B89A64",
               strokeWidth=max(1.4, w * 0.13), opacity=45, cap="round")
