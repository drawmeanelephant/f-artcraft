#!/usr/bin/env python3
"""Eid al-Fitr — Festival Seal V1R00.

Night plate: a gold crescent high on the left, a brass fanous lantern
hanging centre-right on a beaded chain, its arched glass panels glowing
amber. Rooftop silhouette along the foot of the disc, scattered stars.
Deep indigo field, gold rim, vermilion chop with a drawn crescent.
No human figures. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "eid-al-fitr-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#232052"
FIELD_LO = "#0A0A1A"
BRASS_HI = "#E8C074"
BRASS = "#B8842E"
BRASS_LO = "#6E4414"
AMBER = "#FFB45C"
AMBER_HI = "#FFE2A8"
ROOF = "#120F22"

p = Plate("Eid al-Fitr — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def circle_path(cx, cy, r, sweep=1):
    """Full circle as two arcs; sweep picks winding direction."""
    return (f"M{cx - r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 1,{sweep} "
            f"{cx + r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 1,{sweep} "
            f"{cx - r:.1f},{cy:.1f} Z")


def crescent(cx, cy, r, bite=0.62, tilt=-38, label="Crescent",
             col=None, edge=INK):
    """Crescent via compound path: outer disc wound CW, bite disc CCW ->
    a true hole under the nonzero rule, so the field shows through."""
    a = math.radians(tilt)
    bx, by = cx + math.cos(a) * r * bite, cy + math.sin(a) * r * bite
    br = r * 0.86
    fill = col or lin((cx - r, cy - r), (cx + r, cy + r),
                      (0, GOLD_HI), (0.5, GOLD), (1, GOLD_LO))
    d.shape("ellipse", f"{label} halo", x=cx - r * 1.7, y=cy - r * 1.7,
            width=r * 3.4, height=r * 3.4,
            fill=rad((0, "#FFD98A", 22), (0.55, "#FFD98A", 7),
                     (1, "#FFD98A", 0)), stroke=NONE)
    d.path(circle_path(cx, cy, r) + " " + circle_path(bx, by, br, sweep=0),
           label, fill=fill, stroke=edge, strokeWidth=3)
    # soft inner light along the outer edge
    d.path(circle_path(cx, cy, r * 0.93) + " " +
           circle_path(bx, by, br, sweep=0),
           f"{label} sheen", fill="#FFF2C8", opacity=16, stroke=NONE)


def star4(x, y, r, col="#F2DFA8", op=90, label="Star"):
    q = r * 0.20
    d.path(f"M{x:.1f},{y - r:.1f} Q{x + q:.1f},{y - q:.1f} {x + r:.1f},{y:.1f} "
           f"Q{x + q:.1f},{y + q:.1f} {x:.1f},{y + r:.1f} "
           f"Q{x - q:.1f},{y + q:.1f} {x - r:.1f},{y:.1f} "
           f"Q{x - q:.1f},{y - q:.1f} {x:.1f},{y - r:.1f} Z",
           label, fill=col, opacity=op, stroke=NONE)


def arch_window(cx, y0, y1, w, label, hot=AMBER_HI, cool=AMBER):
    """Pointed-arch glass panel, glowing."""
    d.path(f"M{cx - w/2:.1f},{y1:.1f} L{cx - w/2:.1f},{y0 + w*0.55:.1f} "
           f"Q{cx - w/2:.1f},{y0:.1f} {cx:.1f},{y0:.1f} "
           f"Q{cx + w/2:.1f},{y0:.1f} {cx + w/2:.1f},{y0 + w*0.55:.1f} "
           f"L{cx + w/2:.1f},{y1:.1f} Z", label,
           fill=rad((0, hot), (0.6, cool), (1, "#C25E1E")),
           stroke=NONE)
    d.shape("ellipse", f"{label} glint", x=cx - w * 0.22,
            y=y0 + w * 0.3, width=w * 0.3, height=w * 0.5,
            fill="#FFF6DC", opacity=35, stroke=NONE)


def fanous(cx, hang_y, w, bh, label="Fanous"):
    """Brass fanous: finial dome, tapered body of arched glass panels,
    tray base and a drop finial. hang_y is the top of the dome cap."""
    hw = w / 2
    y0 = hang_y + w * 0.16          # shoulder line
    y1 = y0 + bh                    # tray line
    # glow behind the lantern
    d.shape("ellipse", f"{label} aura", x=cx - w, y=hang_y - w * 0.3,
            width=2 * w, height=bh + w * 0.9,
            fill=rad((0, "#FFB45C", 30), (0.5, "#FF8A3C", 8),
                     (1, "#FF8A3C", 0)), stroke=NONE)
    # finial spire + dome cap
    d.path(f"M{cx:.1f},{hang_y - w*0.16:.1f} L{cx:.1f},{hang_y - w*0.05:.1f}",
           f"{label} spire", fill=NONE, stroke=BRASS, strokeWidth=4,
           cap="round")
    d.shape("ellipse", f"{label} finial ball", x=cx - 6, y=hang_y - w * 0.05 - 6,
            width=12, height=12, fill=gold_lin(hang_y - 20, hang_y),
            stroke=INK, strokeWidth=1.6)
    d.path(f"M{cx - w*0.30:.1f},{y0:.1f} Q{cx - w*0.30:.1f},{hang_y - w*0.02:.1f} "
           f"{cx:.1f},{hang_y - w*0.02:.1f} "
           f"Q{cx + w*0.30:.1f},{hang_y - w*0.02:.1f} {cx + w*0.30:.1f},{y0:.1f} Z",
           f"{label} dome", fill=lin((cx - hw, hang_y), (cx + hw, y0),
                                     (0, BRASS_HI), (1, BRASS_LO)),
           stroke=INK, strokeWidth=2.6)
    # shoulder ring
    d.shape("rectangle", f"{label} shoulder", x=cx - hw * 0.72, y=y0 - 5,
            width=hw * 1.44, height=12, radius=4,
            fill=gold_lin(y0 - 5, y0 + 7), stroke=INK, strokeWidth=2)
    # body frame: gentle outward taper then in
    d.path(f"M{cx - hw*0.72:.1f},{y0 + 6:.1f} "
           f"L{cx - hw:.1f},{y0 + bh*0.30:.1f} "
           f"L{cx - hw*0.88:.1f},{y1:.1f} "
           f"L{cx + hw*0.88:.1f},{y1:.1f} "
           f"L{cx + hw:.1f},{y0 + bh*0.30:.1f} "
           f"L{cx + hw*0.72:.1f},{y0 + 6:.1f} Z", f"{label} frame",
           fill=lin((cx - hw, y0), (cx + hw, y1),
                    (0, BRASS_HI), (0.5, BRASS), (1, BRASS_LO)),
           stroke=INK, strokeWidth=3)
    # glass panels: centre + two side arches set into the frame
    wy0, wy1 = y0 + bh * 0.14, y1 - bh * 0.12
    arch_window(cx, wy0, wy1, w * 0.24, f"{label} pane C")
    arch_window(cx - hw * 0.44, wy0 + 10, wy1 - 6, w * 0.17,
                f"{label} pane L", hot="#F6C47E")
    arch_window(cx + hw * 0.44, wy0 + 10, wy1 - 6, w * 0.17,
                f"{label} pane R", hot="#F6C47E")
    # ribs between panels
    for i, k in enumerate((-0.30, 0.30)):
        d.path(f"M{cx + k*w:.1f},{wy0 - 4:.1f} L{cx + k*w*1.06:.1f},{wy1 + 4:.1f}",
               f"{label} rib {i+1}", fill=NONE, stroke=BRASS_LO,
               strokeWidth=4.4, opacity=85, cap="round")
    # tray + drop finial
    d.shape("ellipse", f"{label} tray", x=cx - hw * 0.96, y=y1 - 8,
            width=hw * 1.92, height=20, fill=gold_lin(y1 - 8, y1 + 12),
            stroke=INK, strokeWidth=2.4)
    d.path(f"M{cx:.1f},{y1 + 8:.1f} C{cx - 10:.1f},{y1 + 22:.1f} "
           f"{cx - 6:.1f},{y1 + 34:.1f} {cx:.1f},{y1 + 40:.1f} "
           f"C{cx + 6:.1f},{y1 + 34:.1f} {cx + 10:.1f},{y1 + 22:.1f} "
           f"{cx:.1f},{y1 + 8:.1f} Z", f"{label} drop",
           fill=lin((cx - 10, y1 + 8), (cx + 10, y1 + 40),
                    (0, BRASS_HI), (1, BRASS_LO)), stroke=INK,
           strokeWidth=1.8)


def chain(x, y0, y1, label="Chain"):
    for i, y in enumerate(range(int(y0), int(y1), 17)):
        d.shape("ellipse", f"{label} {i+1}", x=x - 3.2, y=y - 3.2,
                width=6.4, height=6.4, fill=NONE, stroke=BRASS_HI,
                strokeWidth=2.2, opacity=88)


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn gold crescent mark."""
    x, y = cx - s / 2, cy - s / 2
    inside(cx + s / 2, cy + s / 2, 8, "chop BR")
    d.shape("ellipse", "Chop shadow", x=x + 3, y=y + 5, width=s, height=s,
            fill=INK, opacity=28, stroke=NONE)
    d.shape("rectangle", "Chop", x=x, y=y, width=s, height=s, radius=5,
            fill=lin((x, y), (x + s, y + s), (0, "#C0473A"), (1, "#7E1F1B")),
            stroke="#4E100E", strokeWidth=2.2)
    d.shape("rectangle", "Chop inner", x=x + 4.5, y=y + 4.5, width=s - 9,
            height=s - 9, radius=2.5, fill=NONE, stroke="#F6D9A0",
            strokeWidth=1.4, opacity=78)
    a = math.radians(-38)
    bx, by = cx + math.cos(a) * 5.5, cy + math.sin(a) * 5.5
    d.path(circle_path(cx, cy, 11) + " " + circle_path(bx, by, 9.4, sweep=0),
           "Chop crescent", fill="#FBE6B4", stroke=NONE)


# --- field -------------------------------------------------------------------
p.backdrop(top="#0E0C24", bottom="#050510", glow=("#2A2860", 14))
dust(d, n=42, r=402, colors=("#F6E3B8", "#C8D0F0"), seed=41, smin=1.0,
     smax=2.4, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#5E3A16")
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=30)

# star field: sparkles + dust over the whole disc
s = 77
for i in range(64):
    s = (1103515245 * s + 12345) % (2 ** 31)
    a = (s / 2 ** 31) * math.pi * 2
    s = (1103515245 * s + 12345) % (2 ** 31)
    rr = 388 * math.sqrt(s / 2 ** 31)
    x, y = PCX + math.cos(a) * rr, PCY + math.sin(a) * rr
    if math.hypot(x - 575, y - 540) < 130 or math.hypot(x - 415, y - 290) < 130:
        continue
    sz = 1.0 + (s % 100) / 100 * 1.8
    d.shape("ellipse", f"Star dust {i+1}", x=round(x - sz / 2, 1),
            y=round(y - sz / 2, 1), width=round(sz, 1), height=round(sz, 1),
            fill="#EDEAFA", opacity=26 + s % 30, stroke=NONE)
for i, (x, y, r) in enumerate([(268, 196, 13), (586, 172, 11), (652, 296, 9),
                               (308, 420, 8), (180, 300, 9), (748, 452, 8),
                               (238, 560, 8), (498, 156, 7)]):
    star4(x, y, r, label=f"Star {i+1}")

# --- crescent ------------------------------------------------------------------
crescent(408, 292, 96, label="Crescent")

# --- fanous lantern --------------------------------------------------------------
chain(588, 168, 398)
fanous(588, 408, 190, 240)

# --- rooftop silhouette along the foot -------------------------------------------
d.path("M258,800 "
       "L258,780 L280,780 L280,762 L290,762 L290,780 L314,780 "
       "L314,794 L340,794 L340,770 Q358,746 376,770 L376,794 "
       "L414,794 L414,776 L422,776 L422,794 L470,794 "
       "L470,780 L474,780 L474,794 L560,794 "
       "L560,778 Q580,752 600,778 L600,794 "
       "L648,794 L648,774 L656,774 L656,794 L700,794 "
       "L700,782 L710,782 L710,794 L742,794 "
       "A420,420 0 0 0 258,800 Z", "Rooftops",
       fill=lin((0, 750), (0, 880), (0, "#1B1736"), (1, ROOF)),
       stroke=NONE, opacity=94)
# a few lit windows
for i, (x, y) in enumerate([(306, 784), (410, 784), (624, 788), (672, 784)]):
    d.shape("rectangle", f"Window {i+1}", x=x, y=y, width=7, height=9,
            radius=1.5, fill="#FFC97E", opacity=80, stroke=NONE)

# --- seal + caption -------------------------------------------------------------
seal_chop()
caption(p, "EID AL-FITR", "1 SHAWWAL · END OF RAMADAN",
        name_color="#F4EBD4", sub_color="#C9A46A",
        name_size=52, tracking_name=72, sub_size=21, tracking_sub=44,
        sub_font=SERIF)
p.finish(SLUG)
