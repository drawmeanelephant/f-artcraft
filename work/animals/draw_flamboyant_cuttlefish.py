#!/usr/bin/env python3
"""Flamboyant cuttlefish — field plate V1R00. Metasepia pfefferi walking
the sand flat on arm tips — too poisonous to bother hiding, strobing
maroon, acid yellow and violet across the papillae-bumped mantle, the
small body hunched over splayed walking arms. Night sand-flat plate —
dim teal water, pale sand closing on the disc arc, the animal lit like
a warning sign. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Flamboyant Cuttlefish — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#241614"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0A1016"), (1, "#04080A"))
PLATE_GRAD = rad((0, "#465A58"), (0.5, "#243437"), (1, "#0E1416"))
SAND_GR  = lin(0, 760, 0, 880, (0, "#8E7E5E"), (0.5, "#5A4E40"), (1, "#28241E"))
MANTLE   = rad((0, "#6E3440"), (0.55, "#4A2430"), (1, "#281018"))
YELLOW   = rad((0, "#F0D45E"), (1, "#C09A2E"))

# --- backdrop + night sand-flat plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,118,4),(852,122,5),(118,447,3),(873,500,4),
                               (178,734,4),(855,757,4),(262,149,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4D4D2", opacity=24, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#465A58", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#182022", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D4D2", strokeWidth=3, opacity=34)

# dim teal waterlight overhead
d.shape("ellipse", "Waterlight", x=310, y=230, width=400, height=300,
        fill=rad((0, "#8EC4C0", 26), (0.6, "#8EC4C0", 8), (1, "#8EC4C0", 0)),
        stroke=NONE)
# patina flecks / drifting sediment
for i, (x, y, w) in enumerate([(308,178,4),(452,142,5),(592,170,4),(226,268,3),
                               (370,222,4),(524,194,3),(690,150,4),(250,418,3),
                               (750,430,4),(208,556,3)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D0D8D2", opacity=38, stroke=NONE)

# a distant sponge silhouette for depth
d.path("M712,720 C706,690 710,660 726,646 C740,660 744,690 740,720 Z",
       "Far sponge", fill="#2A3A38", opacity=80, stroke=NONE)
d.shape("ellipse", "Sponge osculum", x=719, y=652, width=14, height=8,
        fill="#182422", stroke=NONE)

# --- the sand flat: pale band closing on the disc arc ---------------------------------
fy = 788
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} L{fr:.1f},{fy} A{R},{R} 0 0 1 {fl:.1f},{fy} Z",
       "Sand flat", fill=SAND_GR, stroke=NONE)
# ripple ridges catching the dim light
for i, (ry, sag) in enumerate([(806, 6), (830, 8), (852, 7)]):
    rl, rr = disc_x(ry, -1) + 14, disc_x(ry, 1) - 14
    d.path(f"M{rl:.0f},{ry} C{(rl+rr)/2},{ry+sag} {(rl+rr)/2},{ry+sag} {rr:.0f},{ry}",
           f"Ripple {i+1}", fill=NONE, stroke="#B8A884", strokeWidth=3,
           opacity=40, cap="round")
# animal's shadow pooling on the sand
d.shape("ellipse", "Walk shadow", x=360, y=776, width=330, height=38,
        fill="#08080C", opacity=50, stroke=NONE)

# === arms walking the sand — drawn under the body =====================================
# the walking crown: splayed arms planted like fingers, strobe-banded
ARM = "#5A2E34"
for i, (ax, ay, bx, by, w, col) in enumerate([
        (430, 700, 376, 782, 15, "#D87898"),   # far-left strut
        (460, 712, 420, 792, 16, "#8E5EA8"),   # mid-left
        (492, 716, 466, 796, 17, "#D87898"),   # front pair L
        (524, 716, 512, 798, 17, "#8E5EA8"),   # front pair R
        (556, 712, 560, 794, 16, "#D87898"),   # mid-right
        (584, 704, 616, 784, 15, "#8E5EA8")]): # right strut
    mx, my = (ax+bx)/2 + (bx-ax)*0.12, (ay+by)/2 - 6
    d.path(f"M{ax-w/2},{ay} Q{mx-w/4},{my} {bx-w/4},{by-w/6} "
           f"Q{bx},{by+6} {bx+w/4},{by-w/6} "
           f"Q{mx+w/4},{my} {ax+w/2},{ay} Z",
           f"Arm {i+1}", fill=lin(ax, ay, bx, by, (0, ARM), (1, "#3A1E22")),
           stroke=INK, strokeWidth=3.5)
    # strobe band across each arm
    d.path(f"M{(ax+bx)/2 - w/2},{(ay+by)/2} Q{(ax+bx)/2},{(ay+by)/2+8} {(ax+bx)/2 + w/2},{(ay+by)/2}",
           f"Arm band {i+1}", fill=NONE, stroke=col, strokeWidth=5,
           opacity=85, cap="round")
# two raised scout arms waving ahead
for i, (ax, bx, by) in enumerate([(452, 400, 640), (496, 442, 622)]):
    d.path(f"M{ax-9},{700} Q{ax-14},{(700+by)/2} {bx-8},{by} "
           f"Q{bx},{by-8} {bx+8},{by} Q{ax+14},{(700+by)/2} {ax+9},{700} Z",
           f"Scout arm {i+1}", fill=lin(ax, 700, bx, by, (0, ARM), (1, "#3A1E22")),
           stroke=INK, strokeWidth=3)
    for j in range(2):
        byy = by + 26 + j*22
        d.path(f"M{bx-9},{byy} q9,4 17,0", f"Scout band {i+1}.{j+1}", fill=NONE,
               stroke="#D87898", strokeWidth=4, opacity=85, cap="round")

# === head: broad brow over splayed eyes ==============================================
d.path("M440,656 C418,660 402,676 400,696 C398,716 410,732 430,738 "
       "C456,744 486,742 508,730 C528,720 538,702 534,682 "
       "C530,662 512,650 488,648 C470,646 452,650 440,656 Z",
       "Head", fill=rad((0, "#6E3440"), (0.6, "#4A2430"), (1, "#2A1218")),
       stroke=INK, strokeWidth=4.5)
# violet head bands
for i, (x0, x1) in enumerate([(424, 452), (460, 486), (496, 518)]):
    d.path(f"M{x0},{684} C{x0+4},{696} {x1-4},{700} {x1},{692}",
           f"Head band {i+1}", fill=NONE, stroke="#8E5EA8", strokeWidth=5,
           opacity=80, cap="round")
# eyes: wide-set, pale with a W-ish brow ridge hint
for sgn, lab in ((-1, "L"), (1, "R")):
    ex = 448 + (0 if sgn < 0 else 56)
    d.shape("ellipse", f"Eye {lab}", x=ex, y=670, width=30, height=26,
            fill=rad((0, "#D8CCB0"), (0.6, "#8E8468"), (1, "#3E3828")),
            stroke=INK, strokeWidth=3.5)
    d.path(f"M{ex+4},{680} q6,6 12,3 q6,-3 10,-6", f"Pupil {lab}", fill=NONE,
           stroke="#181210", strokeWidth=4, cap="round")
# yellow eye ridge
d.path("M436,662 C452,652 472,650 494,654 C508,658 518,666 524,676",
       "Eye ridge", fill=NONE, stroke="#E8C84E", strokeWidth=4.5,
       opacity=90, cap="round")

# === mantle: the hunched dome with the strobe bands ==================================
d.path("M500,560 "                                   # mantle front top
       "C556,540 626,548 668,584 "                   # dorsal line rising right
       "C702,614 712,656 700,694 "                   # rounded rear
       "C690,724 664,744 632,750 "                   # under rear
       "C592,756 548,752 520,738 "                   # ventral edge
       "C500,728 490,712 490,692 "                   # front lower
       "C490,670 492,650 496,634 "                   # front face
       "C498,616 498,592 500,560 Z",
       "Mantle", fill=MANTLE, stroke=INK, strokeWidth=6)
# the papillae: bumps along the dorsal ridge, each tipped pale
for i, (px, py, s) in enumerate([(524, 552, 1.1), (566, 546, 1.2),
                                 (608, 550, 1.15), (648, 566, 1.05),
                                 (682, 592, 0.95), (698, 626, 0.8),
                                 (502, 586, 0.9)]):
    d.path(f"M{px - 12*s},{py} C{px - 10*s},{py - 16*s} {px + 10*s},{py - 16*s} {px + 12*s},{py} "
           f"C{px + 6*s},{py + 8*s} {px - 6*s},{py + 8*s} {px - 12*s},{py} Z",
           f"Papilla {i+1}", fill="#5A2E34", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Papilla tip {i+1}", x=px-4, y=py-14*s, width=8, height=6,
            fill="#E8C84E", opacity=90, stroke=NONE)
# the strobe: transverse bands across the mantle — yellow, violet, pink
for i, (bx, bow, col, w) in enumerate([(540, -8, "#E8C84E", 10),
                                       (580, 2, "#8E5EA8", 9),
                                       (622, 8, "#D87898", 9),
                                       (660, 12, "#E8C84E", 9),
                                       (688, 10, "#8E5EA8", 8)]):
    d.path(f"M{bx},{572 + bow*0.4} C{bx + bow},{616} {bx + bow - 6},{676} {bx - 10},{726}",
           f"Mantle band {i+1}", fill=NONE, stroke=col, strokeWidth=w,
           opacity=88, cap="round")
# dorsal acid-yellow patch — the warning field
d.path("M548,566 C576,556 610,558 634,572 C618,574 596,576 576,576 "
       "C564,576 554,572 548,566 Z", "Dorsal patch", fill=YELLOW,
       opacity=85, stroke=NONE)
# the wavy lateral fin — a translucent fringe along the mantle's lower edge
d.path("M504,700 q10,14 22,18 q4,-14 12,-14 q10,16 22,18 q4,-14 12,-12 "
       "q10,16 22,16 q6,-14 14,-12 q8,14 20,16",
       "Lateral fin", fill=NONE, stroke="#D87898", strokeWidth=5,
       opacity=70, cap="round")
# ventral sheen
d.path("M510,720 C550,740 610,746 654,734 C620,752 554,750 516,732 Z",
       "Ventral sheen", fill="#E8B8C8", opacity=30, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C1214", strokeWidth=6)

# --- captions -----------------------------------------------------------------------
r1 = d.text("FLAMBOYANT CUTTLEFISH", "Name", x=500, y=930, size=48,
            font="Virelai Sans", color="#D0DCD6", justify="center")
r2 = d.text("METASEPIA PFEFFERI", "Second line", x=500, y=968, size=22,
            font="Virelai Sans", color="#9AAEA8", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r2["id"], tracking=300)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for r, lab, wmax in [(r1, "name", 800), (r2, "line2", 760)]:
    b = find(layers, r["id"])["bounds"]
    print(lab, "bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= wmax and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("flamboyant-cuttlefish-V1R00")
