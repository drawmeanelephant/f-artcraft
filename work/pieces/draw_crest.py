#!/usr/bin/env python3
# Fart Knocker ornamental crest - VectorCraft, 1000x1250.
import sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

OCTO = "\ue007"
CANDLE = "\ue006"

d = Draw()
d.new_doc("Fart Knocker - Ornamental Crest", 1000, 1250)

PAPER = "#F5EFE0"; INK = "#2B2620"; GOLD = "#B98A2F"; GOLD_D = "#8A7648"
OLIVE = "#76755F"; RED = "#B03A2E"
BUN = {"gradient": {"kind": "radial", "stops": [{"offset": 0, "color": "#F5B942"}, {"offset": 1, "color": "#C96A12"}]}}
CX, CY = 500, 452

d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1250, fill=PAPER, stroke=NONE)

# sunburst rays
for i in range(36):
    a = math.radians(i * 10)
    r0, r1 = 336, 396 if i % 2 == 0 else 372
    w = 0.045
    x0, y0 = CX + r0 * math.cos(a - w), CY + r0 * math.sin(a - w)
    x1, y1 = CX + r0 * math.cos(a + w), CY + r0 * math.sin(a + w)
    xt, yt = CX + r1 * math.cos(a), CY + r1 * math.sin(a)
    d.path(f"M{x0:.0f},{y0:.0f} L{xt:.0f},{yt:.0f} L{x1:.0f},{y1:.0f} Z", f"Ray {i}",
           fill=GOLD, opacity=30, stroke=NONE)

# medallion rings
d.shape("ellipse", "Outer ring", x=CX - 332, y=CY - 332, width=664, height=664, fill="#FBF7EA", stroke=GOLD, strokeWidth=4)
d.shape("ellipse", "Inner ring", x=CX - 312, y=CY - 312, width=624, height=624, fill=NONE, stroke=GOLD_D, strokeWidth=1.4)

# burger head
d.path("M282,432 C282,302 382,226 500,226 C618,226 718,302 718,432 Z", "Bun dome", fill=BUN, stroke=NONE)
for i, (x, y, r) in enumerate([(408, 292, -18), (500, 268, 8), (588, 296, 20), (452, 330, -30), (556, 338, 42),
                               (372, 348, 12), (632, 356, -8)]):
    d.path(f"M{x-11},{y} A11,6 {r} 1 1 {x+11},{y} A11,6 {r} 1 1 {x-11},{y} Z", f"Sesame {i}",
           fill="#FBE3B0", stroke=NONE)
d.path("M282,432 C340,448 380,424 430,440 C480,456 520,430 575,444 C630,458 672,434 718,446 L718,464 L282,464 Z",
       "Lettuce", fill="#7C9A52", stroke=NONE)
d.shape("rectangle", "Tomato", x=282, y=458, width=436, height=15, fill="#C8452C", stroke=NONE)
d.path("M282,473 L718,473 L718,488 C680,488 668,506 640,492 C612,478 600,502 566,490 C532,478 512,504 478,490 "
       "C444,476 428,502 394,490 C360,478 344,500 316,488 C296,480 282,492 282,488 Z", "Cheese", fill="#F2A83B", stroke=NONE)
d.shape("rectangle", "Patty", x=282, y=492, width=436, height=24, fill="#6B4226", stroke=NONE)
d.path("M282,516 C282,612 388,674 500,674 C612,674 718,612 718,516 Z", "Face bun", fill="#F2C063", stroke=NONE)
d.shape("ellipse", "Face highlight", x=360, y=528, width=280, height=66, fill="#FFFFFF", opacity=16, stroke=NONE)
d.shape("ellipse", "Eye L", x=428, y=552, width=26, height=34, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=546, y=552, width=26, height=34, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=434, y=558, width=7, height=7, fill="#FFF6E0", stroke=NONE)
d.path("M452,622 C476,640 524,640 548,622", "Smile", fill=NONE, stroke=INK, strokeWidth=8, cap="round")
d.shape("ellipse", "Monocle", x=527, y=536, width=64, height=64, fill="#FFFFFF", opacity=14, stroke=GOLD, strokeWidth=5)
d.path("M559,600 C600,640 648,660 694,668", "Monocle chain", fill=NONE, stroke=GOLD, strokeWidth=3, dash=[2, 7], cap="round")
d.path("M470,548 L527,552", "Monocle bridge", fill=NONE, stroke=GOLD, strokeWidth=3.4)
d.path("M492,692 L382,640 C344,622 322,646 326,690 C322,734 344,758 382,740 L492,692 Z", "Bowtie L", fill="#23201B", stroke=NONE)
d.path("M508,692 L618,640 C656,622 678,646 674,690 C678,734 656,758 618,740 L508,692 Z", "Bowtie R", fill="#23201B", stroke=NONE)
d.shape("rectangle", "Bowtie knot", x=470, y=662, width=60, height=60, radius=13, fill="#322E28", stroke=NONE)

# tentacle curls
def spiral(cx, cy, r0, r1, a0, a1, steps=26):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = a0 + (a1 - a0) * t
        r = r0 + (r1 - r0) * t
        pts.append(f"{cx + r * math.cos(a):.0f},{cy + r * math.sin(a):.0f}")
    return "M" + " L".join(pts)

for lbl, (cx, cy, flip) in {"Curl L1": (306, 742, 1), "Curl L2": (392, 776, 1),
                            "Curl R1": (694, 742, -1), "Curl R2": (608, 776, -1)}.items():
    d.path(spiral(cx, cy, 30, 5, math.radians(90), math.radians(90 + 300 * flip)), lbl,
           fill=NONE, stroke="#D98A4A", strokeWidth=15, cap="round")
    d.shape("ellipse", lbl + " tip", x=cx - 5, y=cy - 5, width=10, height=10, fill="#B85C1E", stroke=NONE)

# laurel branches
def leaf(cx, cy, ang, size=30):
    ux, uy = math.cos(ang), math.sin(ang)
    vx, vy = -uy, ux
    L, W = size, size * 0.34
    tip = (cx + ux * L, cy + uy * L)
    base = (cx - ux * L, cy - uy * L)
    c1 = (cx + vx * W, cy + vy * W)
    c2 = (cx - vx * W, cy - vy * W)
    return (f"M{base[0]:.0f},{base[1]:.0f} Q{c1[0]:.0f},{c1[1]:.0f} {tip[0]:.0f},{tip[1]:.0f} "
            f"Q{c2[0]:.0f},{c2[1]:.0f} {base[0]:.0f},{base[1]:.0f} Z")

for side in (1, -1):
    stem_pts = []
    for i in range(21):
        t = i / 20
        a = math.radians(90 + side * (18 + 62 * t))
        stem_pts.append(f"{CX + 352 * math.cos(a):.0f},{CY + 352 * math.sin(a):.0f}")
    d.path("M" + " L".join(stem_pts), f"Laurel stem {'L' if side==1 else 'R'}",
           fill=NONE, stroke=OLIVE, strokeWidth=4, cap="round")
    for i in range(6):
        t = 0.08 + i * 0.165
        a = math.radians(90 + side * (18 + 62 * t))
        lx, ly = CX + 352 * math.cos(a), CY + 352 * math.sin(a)
        tang = a + math.pi / 2 * (1 if side == 1 else -1) * -1
        d.path(leaf(lx, ly, tang + side * 0.5, 30), f"Leaf {'L' if side==1 else 'R'}{i}",
               fill=OLIVE, stroke=NONE)
        d.path(leaf(lx, ly, tang - side * 0.9, 24), f"Leaf in {'L' if side==1 else 'R'}{i}",
               fill="#8B8A70", stroke=NONE)

# top ornament: octopus glyph astride the ring
d.text(OCTO, "Octopus crest", x=500, y=118, size=64, font="Virelai Mascots", color=GOLD_D, justify="center")
for sx in (-1, 1):
    d.path(f"M{500 + sx * 64},74 l10,14 -10,14 -10,-14 Z", f"Top diamond {sx}", fill=GOLD, stroke=NONE)

# lettering
d.text("FART KNOCKER", "Title", x=500, y=916, size=66, font="Virelai Sans", color=INK, justify="center")
d.shape("rectangle", "Title rule L", x=238, y=940, width=170, height=2.4, fill=GOLD, stroke=NONE)
d.shape("rectangle", "Title rule R", x=592, y=940, width=170, height=2.4, fill=GOLD, stroke=NONE)
d.path("M500,926 l11,13 -11,13 -11,-13 Z", "Title diamond", fill=RED, stroke=NONE)
d.text("BAD MANNERS - GOOD ENGINEERING", "Motto", x=500, y=1006, size=31,
       font="Virelai Sans", color=GOLD_D, justify="center")
d.text(CANDLE, "Candle L", x=196, y=1120, size=46, font="Virelai Mascots", color=OLIVE, justify="center")
d.text(CANDLE, "Candle R", x=804, y=1120, size=46, font="Virelai Mascots", color=OLIVE, justify="center")
d.text("EST. MMXXVI - DRAWMEANELEPHANT", "Footer", x=500, y=1124, size=21,
       font="Virelai Sans", color=OLIVE, justify="center")

d.finish("fart-knocker-crest")
