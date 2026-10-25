#!/usr/bin/env python3
"""Guy Fawkes Night — Festival Seal V1R00.

Bonfire Night: a teepee of split logs burning low-centre on a charcoal
night field, layered flame and rising embers, two rockets still climbing
to their bursts and a slow spark shower falling from a high shell.
Vermilion chop with a drawn flame mark. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth)
from festival_kit import seal_disc, glow, dust, ring_dots, caption, firework, flame

SLUG = "guy-fawkes-night-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

FIELD_HI = "#201E3C"
FIELD_LO = "#07060E"
LOG_HI = "#7A4E26"
LOG = "#573517"
LOG_LO = "#331D0C"
EMBER = "#FFC46B"

p = Plate("Guy Fawkes Night — Festival Seal", 1000, 1000)
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


def log(x0, y0, x1, y1, w, col, label, char=True):
    """One log: thick round-capped stroke, bark line, charred tip."""
    d.shape("line", label, x1=round(x0, 1), y1=round(y0, 1), x2=round(x1, 1),
            y2=round(y1, 1), stroke=col, strokeWidth=w, cap="round")
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    d.shape("line", f"{label} bark", x1=round(x0 + (x1 - x0) * 0.18, 1),
            y1=round(y0 + (y1 - y0) * 0.18, 1), x2=round(x1 - (x1 - x0) * 0.2, 1),
            y2=round(y1 - (y1 - y0) * 0.2, 1), stroke=LOG_LO, strokeWidth=w * 0.22,
            opacity=45, cap="round")
    if char:
        d.shape("ellipse", f"{label} char", x=x1 - w * 0.42, y=y1 - w * 0.42,
                width=w * 0.84, height=w * 0.84, fill="#1A100A",
                stroke="#E86A3A", strokeWidth=1.6, opacity=96)


def cut_face(x, y, r, lit, label):
    """Sawn log end: pale wood face with a growth ring."""
    d.shape("ellipse", label, x=x - r, y=y - r, width=2 * r, height=2 * r,
            fill="#C89A68" if lit else "#7A5430", stroke=INK, strokeWidth=1.4)
    d.shape("ellipse", f"{label} ring", x=x - r * 0.55, y=y - r * 0.55,
            width=2 * r * 0.55, height=2 * r * 0.55, fill=NONE,
            stroke="#8A6238" if lit else "#4A3018", strokeWidth=1.2,
            opacity=75)


def rocket_trail(x0, y0, cx1, cy1, x1, y1, label):
    """Dashed gold ascent ending near a burst, ember head partway up."""
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx1:.1f},{cy1:.1f} {x1:.1f},{y1:.1f}",
           f"{label} glow", fill=NONE, stroke=GOLD, strokeWidth=6,
           opacity=12, cap="round")
    d.path(f"M{x0:.1f},{y0:.1f} Q{cx1:.1f},{cy1:.1f} {x1:.1f},{y1:.1f}",
           label, fill=NONE, stroke=GOLD_HI, strokeWidth=2.4, opacity=60,
           cap="round", dash=[9, 7])
    hx, hy = bez2((x0, y0), (cx1, cy1), (x1, y1), 0.86)
    d.shape("ellipse", f"{label} head glow", x=hx - 12, y=hy - 12, width=24,
            height=24, fill=rad((0, "#FFD98A", 60), (1, "#FFD98A", 0)),
            stroke=NONE)
    d.shape("ellipse", f"{label} head", x=hx - 3.4, y=hy - 3.4, width=6.8,
            height=6.8, fill="#FFEFC4", opacity=95, stroke=NONE)


def spark_shower(cx, cy, n=26, seed=17, spread=170, fall=300, label="Shower"):
    """Slow ember rain under a high shell: bowed falling strokes + dots."""
    s = seed
    for i in range(n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        fx = (s % 1000) / 1000 - 0.5
        s = (1103515245 * s + 12345) % (2 ** 31)
        fy = (s % 1000) / 1000
        s = (1103515245 * s + 12345) % (2 ** 31)
        ln = 26 + (s % 1000) / 1000 * 60
        s = (1103515245 * s + 12345) % (2 ** 31)
        drift = ((s % 1000) / 1000 - 0.5) * 60
        x0 = cx + fx * spread
        y0 = cy + fy * 60
        x1, y1 = x0 + drift, y0 + ln * 2.2
        mx = (x0 + x1) / 2 + drift * 0.3
        my = (y0 + y1) / 2 + 14
        if math.hypot(x1 - PCX, y1 - PCY) > PR - 20:
            continue
        col = EMBER if i % 3 else "#FF9E5A"
        d.path(f"M{x0:.1f},{y0:.1f} Q{mx:.1f},{my:.1f} {x1:.1f},{y1:.1f}",
               f"{label} streak {i+1}", fill=NONE, stroke=col,
               strokeWidth=1.8, opacity=30 + (i * 7) % 34, cap="round")
        if i % 2:
            d.shape("ellipse", f"{label} drop {i+1}", x=x1 - 1.8, y=y1 - 1.8,
                    width=3.6, height=3.6, fill=col, opacity=66, stroke=NONE)


def seal_chop(cx=744, cy=214, s=62):
    """Vermilion chop inside the disc, top right; drawn flame mark."""
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
    d.path(f"M{cx:.1f},{cy + 15:.1f} C{cx - 13:.1f},{cy + 7:.1f} "
           f"{cx - 8:.1f},{cy - 10:.1f} {cx:.1f},{cy - 19:.1f} "
           f"C{cx + 8:.1f},{cy - 10:.1f} {cx + 13:.1f},{cy + 7:.1f} "
           f"{cx:.1f},{cy + 15:.1f} Z", "Chop flame", fill="#FBE6B4",
           opacity=94, stroke=NONE)
    d.path(f"M{cx:.1f},{cy + 12:.1f} C{cx - 6:.1f},{cy + 6:.1f} "
           f"{cx - 3:.1f},{cy - 3:.1f} {cx:.1f},{cy - 8:.1f} "
           f"C{cx + 3:.1f},{cy - 3:.1f} {cx + 6:.1f},{cy + 6:.1f} "
           f"{cx:.1f},{cy + 12:.1f} Z", "Chop flame core", fill="#C0473A",
           stroke=NONE)


# --- field -------------------------------------------------------------------
p.backdrop(top="#191830", bottom="#050409", glow=("#4A3060", 11))
dust(d, n=44, r=402, colors=("#F6E3B8", "#D8CCF0"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=24, label="Backdrop dust")
seal_disc(p, FIELD_HI, FIELD_LO, rim=GOLD, rim2="#241E4A")
d.shape("ellipse", "Vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.62, "#000000", 0), (1, "#000000", 58)),
        stroke=NONE)
ring_dots(d, r=397, n=56, size=2.6, color=GOLD, opacity=28)
dust(d, n=50, r=392, colors=("#F6E3B8", "#E8DCF0", "#FFC46B"), seed=23,
     smin=1.0, smax=2.6, opmin=10, opmax=28, label="Disc dust")

# --- sky: bursts, rockets, shower ----------------------------------------------
firework(d, 330, 244, 66, col1=GOLD, col2="#F2705A", rays=16, seed=7,
         label="Burst L")
firework(d, 640, 258, 62, col1=GOLD, col2="#FF9E5A", rays=14, seed=11,
         label="Burst R")
firework(d, 500, 148, 48, col1="#F6E3B8", col2=GOLD, rays=12, seed=19,
         label="Burst top")
spark_shower(500, 176, n=26, seed=17, spread=190, label="Shower")
rocket_trail(296, 742, 268, 500, 316, 268, "Rocket trail L")
rocket_trail(704, 730, 690, 500, 652, 280, "Rocket trail R")

# --- the bonfire -----------------------------------------------------------------
d.shape("ellipse", "Fire ground shadow", x=368, y=706, width=264, height=38,
        fill=INK, opacity=34, stroke=NONE)
glow(d, 500, 608, 215, "#FF9E4A", a=32, label="Firelight", squash=0.82)

# crossed pyre logs, ends sticking out past the coals
log(436, 684, 570, 718, 20, LOG_LO, "Log back A", char=False)
log(566, 682, 432, 720, 20, LOG_LO, "Log back B", char=False)
cut_face(570, 718, 10, False, "Log A cut")
cut_face(432, 720, 10, True, "Log B cut")
# coal bed nestled on the crossing
d.shape("ellipse", "Coal bed", x=434, y=664, width=132, height=26,
        fill=rad((0, "#FF8A44"), (0.55, "#C8431F"), (1, "#3E1408")),
        stroke=INK, strokeWidth=1.6)
for i, (cx_, cy_, cr) in enumerate([(464, 672, 3.2), (494, 667, 2.6), (524, 673, 3.0),
                                    (546, 668, 2.2)]):
    d.shape("ellipse", f"Coal glow {i+1}", x=cx_ - cr, y=cy_ - cr, width=2 * cr,
            height=2 * cr, fill="#FFD98A", opacity=85, stroke=NONE)
# flames rise off the coals
flame(d, 500, 670, 184, 116, label="Bonfire main", smoke=3)
flame(d, 460, 664, 102, 52, lean=-0.5, label="Flame L", smoke=1)
flame(d, 540, 664, 110, 48, lean=0.55, label="Flame R", smoke=1)
# short front log tying the pyre together
log(452, 726, 550, 716, 16, LOG, "Log front", char=False)
cut_face(452, 726, 8, True, "Log front cut L")
cut_face(550, 716, 8, False, "Log front cut R")

# rising embers over the flames
s = 41
for i in range(14):
    s = (1103515245 * s + 12345) % (2 ** 31)
    ex = 500 + ((s % 1000) / 1000 - 0.5) * 150
    s = (1103515245 * s + 12345) % (2 ** 31)
    ey = 470 - (s % 1000) / 1000 * 190
    s = (1103515245 * s + 12345) % (2 ** 31)
    er = 1.6 + (s % 1000) / 1000 * 2.4
    inside(ex, ey, 18, f"ember {i}")
    d.shape("ellipse", f"Fire ember {i+1}", x=ex - er, y=ey - er,
            width=2 * er, height=2 * er, fill=EMBER if i % 3 else "#FF8A3C",
            opacity=70 - i * 3, stroke=NONE)

# --- seal + caption --------------------------------------------------------------
seal_chop()
caption(p, "GUY FAWKES NIGHT", "NOVEMBER 5 · BONFIRE NIGHT",
        name_color="#F2ECD8", sub_color="#C9A46A",
        name_size=50, tracking_name=58, sub_size=21, tracking_sub=44,
        sub_font=SERIF)
p.finish(SLUG)
