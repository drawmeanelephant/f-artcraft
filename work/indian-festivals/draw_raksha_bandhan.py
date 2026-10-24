#!/usr/bin/env python3
"""Raksha Bandhan — Festival Seal V1R00.

The thread plate: a rakhi rosette as hero — radiating silk loops around a
gold embossed medallion, a binding ring, bead fringe, the two thread tails
sweeping away — beside a brass thali holding kumkum, rice grains and a small
lit diya. One marigold keeps the season. Deep rose field. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, DEVA, lin, rad, gold_lin, smooth, blend,
                          blossom)
from festival_kit import (seal_disc, glow, dust, lamp, marigold_at, leaf_at,
                          deva_seal, caption)

SLUG = "raksha-bandhan-V1R00"
ROSE = "#4A1024"
ROSE_LO = "#160510"
SILK_RED = "#C22B46"
SILK_RED_HI = "#E85A6E"
GOLD_MED = "#E8BE6A"

p = Plate("Raksha Bandhan — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#200A14", bottom="#08030A", glow=("#7E2440", 11))
dust(d, n=40, r=402, colors=("#F6E3B8", "#E85A6E"), seed=23,
     smin=1.0, smax=2.4, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, ROSE, ROSE_LO, rim=GOLD, rim2="#380E1E")
dust(d, n=60, r=390, colors=("#F6E3B8", "#F2A33C", "#E85A6E"), seed=15,
     smin=1.0, smax=3.0, opmin=10, opmax=28, label="Disc dust")
d.shape("ellipse", "Rim relight", x=86, y=46, width=828, height=828, fill=NONE,
        stroke=lin((86, 46), (914, 874), (0, "#F2CC8E"), (0.5, "#B0804A"),
                   (1, "#E8BC78")), strokeWidth=4)
p.ring_ticks(n=24, color="#B08656", r_in=378, r_out=396, width=2.2)

# --- the rakhi ------------------------------------------------------------------
RCX, RCY = 458, 408
inside(RCX - 168, RCY, 12, "rakhi L")
inside(RCX + 168, RCY, 12, "rakhi R")
inside(RCX, RCY - 168, 12, "rakhi T")
inside(RCX, RCY + 190, 12, "rakhi B")
glow(d, RCX, RCY, 230, "#E88A9A", a=16, label="Rakhi glow")
d.shape("ellipse", "Rakhi shadow", x=RCX - 172, y=RCY + 126, width=344,
        height=94, fill=rad((0, "#000000", 36), (0.6, "#000000", 14),
                            (1, "#000000", 0)), stroke=NONE)
# radiating silk loops
N = 26
for i in range(N):
    a = i * 360 / N
    col = SILK_RED if i % 2 else GOLD
    hi = SILK_RED_HI if i % 2 else GOLD_HI
    leaf_at(d, RCX + math.cos(math.radians(a)) * 66,
            RCY + math.sin(math.radians(a)) * 66, a, 80, 11,
            fill=lin(0, RCY - 80, 0, RCY + 80, (0, hi), (1, col)),
            stroke="#6E1428" if i % 2 else "#6E4A1A", vein=False,
            label=f"Rakhi loop {i+1}")
# binding ring
d.shape("ellipse", "Rakhi binding", x=RCX - 72, y=RCY - 72, width=144,
        height=144, fill=NONE, stroke=lin((RCX - 72, RCY - 72),
                                          (RCX + 72, RCY + 72),
                                          (0, GOLD_HI), (1, "#8E5A1E")),
        strokeWidth=12)
d.shape("ellipse", "Rakhi binding thread", x=RCX - 72, y=RCY - 72, width=144,
        height=144, fill=NONE, stroke="#6E4A1A", strokeWidth=1.4, opacity=60)
# wound thread texture on the binding
for i in range(16):
    a = math.radians(i * 22.5 + 8)
    x0 = RCX + 66 * math.cos(a)
    y0 = RCY + 66 * math.sin(a)
    x1 = RCX + 78 * math.cos(a)
    y1 = RCY + 78 * math.sin(a)
    d.shape("line", f"Binding wrap {i+1}", x1=round(x0, 1), y1=round(y0, 1),
            x2=round(x1, 1), y2=round(y1, 1), stroke="#8E6A2E", strokeWidth=2.0,
            opacity=70)
# gold medallion with embossed blossom
d.shape("ellipse", "Medallion", x=RCX - 58, y=RCY - 58, width=116, height=116,
        fill=rad((0, "#FBE4A8"), (0.55, GOLD_MED), (1, "#8E5A1E")),
        stroke=INK, strokeWidth=3.4)
d.shape("ellipse", "Medallion ring", x=RCX - 46, y=RCY - 46, width=92,
        height=92, fill=NONE, stroke="#8E5A1E", strokeWidth=1.8, opacity=60)
blossom(d, RCX, RCY, 33, petals=8, label="Medallion emboss",
        fill="#C88A3E", core="#7A4A16", rot=-90, opacity=80)
for i in range(6):
    a = math.radians(i * 60 + 30)
    d.shape("ellipse", f"Medallion mirror {i+1}",
            x=RCX + 48 * math.cos(a) - 3, y=RCY + 48 * math.sin(a) - 3,
            width=6, height=6, fill="#FFF6D8", stroke="#6E4A1A",
            strokeWidth=0.9)
# bead fringe
for i in range(14):
    a = math.radians(i * 360 / 14)
    bx, by = RCX + 152 * math.cos(a), RCY + 152 * math.sin(a)
    d.shape("ellipse", f"Bead {i+1}", x=bx - 7.5, y=by - 7.5, width=15,
            height=15,
            fill=rad((0, "#F8D8B0" if i % 2 else "#F8A8B4"),
                     (0.6, GOLD if i % 2 else SILK_RED),
                     (1, "#6E1428" if i % 2 == 0 else "#6E4A1A")),
            stroke=INK, strokeWidth=1.6)
# thread tails sweeping to the lower right
TX, TY = RCX + 52, RCY + 164
d.path(f"M{RCX + 8},{RCY + 74} Q{TX - 8},{TY - 12} {TX + 56},{TY + 8}",
       "Thread tail A", fill=NONE, stroke=SILK_RED, strokeWidth=5, cap="round")
d.path(f"M{RCX + 26},{RCY + 66} Q{TX + 10},{TY - 22} {TX + 74},{TY - 4}",
       "Thread tail B", fill=NONE, stroke=SILK_RED_HI, strokeWidth=5, cap="round")
d.path(f"M{RCX + 8},{RCY + 74} Q{TX - 8},{TY - 12} {TX + 56},{TY + 8}",
       "Thread tail A gold", fill=NONE, stroke=GOLD, strokeWidth=1.4,
       opacity=50, cap="round")
# knot
d.shape("ellipse", "Tail knot", x=TX + 56, y=TY - 12, width=22, height=18,
        fill=rad((0, SILK_RED_HI), (1, SILK_RED)), stroke="#6E1428",
        strokeWidth=2.2)
for k, (dx, dy) in enumerate(((16, 24), (26, 10), (12, 36))):
    d.path(f"M{TX + 66},{TY - 2} Q{TX + 66 + dx * 0.6},{TY + dy * 0.5} "
           f"{TX + 60 + dx},{TY + dy}", f"Tail fringe {k+1}", fill=NONE,
           stroke=SILK_RED, strokeWidth=3.4, cap="round")
inside(TX + 88, TY + 48, 12, "tail fringe end")

# --- the thali ---------------------------------------------------------------------
TX2, TY2 = 686, 660
inside(TX2 - 108, TY2 + 46, 12, "thali L")
inside(TX2 + 108, TY2 + 46, 12, "thali R")
d.shape("ellipse", "Thali shadow", x=TX2 - 104, y=TY2 + 26, width=208,
        height=64, fill=rad((0, "#000000", 34), (1, "#000000", 0)), stroke=NONE)
d.shape("ellipse", "Thali", x=TX2 - 106, y=TY2 - 44, width=212, height=96,
        fill=lin(0, TY2 - 44, 0, TY2 + 52, (0, "#F2CC78"), (0.5, "#C89648"),
                 (1, "#7A521E")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Thali rim", x=TX2 - 98, y=TY2 - 37, width=196, height=82,
        fill=NONE, stroke="#FBE4A8", strokeWidth=2, opacity=55)
# kumkum heap
d.path(f"M{TX2 - 18},{TY2 + 8} Q{TX2 - 2},{TY2 - 26} {TX2 + 14},{TY2 + 8} Z",
       "Kumkum heap", fill=lin(0, TY2 - 26, 0, TY2 + 8, (0, "#E84838"),
                               (1, "#8E1414")), stroke="#5E0E0E", strokeWidth=2)
d.shape("ellipse", "Kumkum glow", x=TX2 - 26, y=TY2 - 18, width=52,
        height=30, fill=rad((0, "#E84838", 26), (1, "#E84838", 0)), stroke=NONE)
# rice grains on the right side of the plate
s = 53
for i in range(14):
    s = (1103515245 * s + 12345) % (2 ** 31)
    gx = TX2 + 6 + (s % 10000) / 10000 * 78
    s = (1103515245 * s + 12345) % (2 ** 31)
    gy = TY2 - 14 + (s % 10000) / 10000 * 32
    s = (1103515245 * s + 12345) % (2 ** 31)
    d.shape("ellipse", f"Rice {i+1}", x=round(gx - 3.4, 1), y=round(gy - 1.7, 1),
            width=6.8, height=3.4, fill="#FBEFD8", stroke="#B8A070",
            strokeWidth=0.8, rotation=round((s % 90) - 45, 1))
# small lamp on the thali's left edge
lamp(d, TX2 - 74, TY2 - 6, 52, label="Thali diya", flame_h=46, glow_a=26)

# --- marigolds + fallen petals ----------------------------------------------------
inside(250, 648, 34, "marigold")
inside(302, 694, 26, "marigold B")
marigold_at(d, 250, 648, 31, 1, label="Season marigold")
marigold_at(d, 302, 694, 21, 0, label="Season marigold B")
leaf_at(d, 282, 676, 128, 32, 8, fill="#2F6B3A", label="Marigold leaf")
for i, (x, y, ang) in enumerate([(348, 320, -30), (622, 300, 40), (580, 618, 15)]):
    d.shape("ellipse", f"Fallen petal {i+1}", x=x - 8, y=y - 5, width=16,
            height=10, fill="#F2A33C", opacity=55, stroke=NONE, rotation=ang)

# --- sparks ----------------------------------------------------------------------------
for i, (x, y, s2) in enumerate([(340, 250, 2.2), (640, 380, 2.0), (300, 500, 1.8),
                                (620, 520, 2.2)]):
    glow(d, x, y, 11, "#FFD98A", a=34, label=f"Spark glow {i+1}")
    d.shape("ellipse", f"Spark {i+1}", x=x - s2, y=y - s2, width=s2 * 2,
            height=s2 * 2, fill="#FFF2C4", opacity=85, stroke=NONE)

# --- seal + caption ----------------------------------------------------------------------
deva_seal(d, "रक्षा", cx=744, cy=213, s=64, size=25)
caption(p, "RAKSHA BANDHAN", "रक्षा बंधन · SHRAVAN PURNIMA",
        name_color="#F8E4CC", sub_color="#D8A0A8",
        name_size=48, tracking_name=48, sub_size=20, tracking_sub=50)
p.finish(SLUG)
