#!/usr/bin/env python3
"""Nile crocodile — field-guide plate V1R00. Head-on lurk: the skull rides
almost flush with the delta surface, eye bosses and the long snout ridge the
only dry land, nostril bump just kissing the waterline. Nuchal scute rosette
behind the eyes, the fourth tooth peeking over the jaw seam. Papyrus reeds in
the hush behind, murky water closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Nile Crocodile — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#201A0E"                    # deep umber-black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1B16"), (1, "#030805"))
PLATE_GRAD = rad((0, "#8B9C7E"), (0.6, "#5E7260"), (1, "#31433A"))
WATER_GRAD = lin(0, 610, 0, 880, (0, "#4E6353"), (0.45, "#2E4238"), (1, "#17251F"))
SKIN_GRAD = rad((0, "#93875A"), (0.55, "#6A6040"), (1, "#3E3A24"))
IRIS_GRAD = rad((0, "#F0C45C"), (0.55, "#C99536"), (1, "#7A5418"))
REED_GRAD = lin(0, 140, 0, 620, (0, "#31482F"), (1, "#16241A"))

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#7E9478", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26332A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DDE8CC", strokeWidth=3, opacity=40)
# hush: two mist bands drifting across the upper plate
for i, dd in enumerate(["M140,230 C340,208 560,214 810,240",
                        "M120,345 C330,322 590,328 850,352"]):
    d.path(dd, f"Mist band {i+1}", fill=NONE, stroke="#E6EEDA",
           strokeWidth=30, opacity=9, cap="round")
for i, (x, y, w) in enumerate([(200,190,6),(780,170,6),(150,430,7),(860,410,7),(260,130,5),
                               (700,120,6),(330,170,4),(640,150,5),(170,540,5),(840,540,5)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8EFD8", opacity=45, stroke=NONE)

# --- papyrus reeds, left and right ---------------------------------------------------
def reed(x, top, lean, label):
    tip = (x + lean, top)
    d.path(f"M{x},618 C{x + lean*0.4},{500} {tip[0]},{top + 40} {tip[0]},{tip[1]}",
           f"{label} stalk", fill=NONE, stroke=REED_GRAD, strokeWidth=5, cap="round")
    # papyrus head: a burst of fine rays with seed dots
    for k in range(11):
        a = math.radians(205 + 130 * k / 10)
        L = 30 + 12 * math.sin(k * 2.1)
        ex, ey = tip[0] + L * math.cos(a), tip[1] + 6 - abs(L * math.sin(a))
        d.path(f"M{tip[0]:.0f},{tip[1]:.0f} L{ex:.0f},{ey:.0f}", f"{label} ray {k+1}",
               fill=NONE, stroke=REED_GRAD, strokeWidth=1.8, opacity=80, cap="round")
        if k % 3 == 1:
            d.shape("ellipse", f"{label} seed {k}", x=ex - 2, y=ey - 2, width=4, height=4,
                    fill="#5A7040", opacity=75, stroke=NONE)

for i, (x, top, lean) in enumerate([(196, 300, -14), (236, 240, 8), (272, 330, 18)]):
    reed(x, top, lean, f"Reed L{i+1}")
for i, (x, top, lean) in enumerate([(742, 262, -10), (788, 320, 10), (816, 210, 16)]):
    reed(x, top, lean, f"Reed R{i+1}")

# --- the head: profile lurk, dorsal surface breaking the water -----------------------
# facing left; only the snout ridge, eye boss and nostril bump stay dry.
# authored at model scale, then grown about (470,560) so the head commands the plate
K = 1.16
def sx(x): return 470 + (x - 470) * K
def sy(y): return 560 + (y - 560) * K
def sp(dd):
    toks, out, ex = re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), [], True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{sx(float(t)):.1f},"); ex = False
        else:
            out[-1] += f"{sy(float(t)):.1f}"; ex = True
    return " ".join(out)

HEAD = ("M688,602 C668,578 650,560 622,546 C600,536 582,530 566,526 "
        "C560,508 550,494 534,492 C520,490 508,496 502,508 "
        "C494,518 476,522 452,525 C415,530 372,534 338,537 "
        "C318,539 306,540 298,545 C296,536 288,530 280,532 "
        "C272,534 266,540 264,548 C254,556 252,568 260,574 "
        "C272,580 306,583 348,585 C440,590 560,596 688,602 Z")
d.path(sp(HEAD), "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=6)
# wet dorsal sheen along the ridge
d.path(sp("M272,552 C300,540 340,536 400,531 C450,526 488,517 516,500"),
       "Dorsal sheen", fill=NONE, stroke="#D8CC92", strokeWidth=3.5, opacity=45, cap="round")
# underside shade along the jaw where it slips under
d.path(sp("M270,572 C360,584 520,592 662,598"), "Jaw under-shade",
       fill=NONE, stroke="#2E2A18", strokeWidth=10, opacity=25, cap="round")

# the eye on its raised boss — the half inch that matters
d.path(sp("M512,506 C520,494 538,490 552,498"), "Brow crease",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Eye rim", x=sx(520), y=sy(498), width=26*K, height=20*K,
        fill="#2A2414", stroke=NONE)
d.shape("ellipse", "Iris", x=sx(524), y=sy(501), width=19*K, height=15*K, fill=IRIS_GRAD,
        stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Pupil", x=sx(531.5), y=sy(502.5), width=4*K, height=12*K,
        fill="#12100A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=sx(527), y=sy(503), width=4.5*K, height=4.5*K,
        fill="#FFF6DC", opacity=90, stroke=NONE)
# ear flap behind the boss
d.path(sp("M576,534 C586,538 594,546 598,556"), "Ear slit",
       fill=NONE, stroke=INK, strokeWidth=3.5, opacity=50, cap="round")
# nostril on the tip bump
d.shape("ellipse", "Nostril", x=sx(280), y=sy(538), width=9*K, height=7*K,
        fill="#16120A", stroke=NONE)
# the mouth line, riding just at the surface; the croc smile lifts at the hinge
d.path(sp("M264,568 C300,576 340,579 380,582 C470,588 570,594 646,597 C656,595 664,591 668,586"),
       "Mouth line", fill=NONE, stroke=INK, strokeWidth=5, opacity=70, cap="round")

# dorsal scutes: small sawtooth bumps standing on the ridge between boss and tip
for i, (x, y) in enumerate([(362,533),(392,530),(422,527),(452,525),(482,521)]):
    X, Y, e = sx(x), sy(y), 7*K
    d.path(f"M{X-e:.1f},{Y+3*K:.1f} L{X:.1f},{Y-e:.1f} L{X+e:.1f},{Y+3*K:.1f} Z",
           f"Dorsal scute {i+1}", fill="#7E7448", stroke=INK, strokeWidth=2)
# nuchal rosette on the nape, two staggered rows
for i, (x, y) in enumerate([(598,542),(622,550),(646,560),(612,560),(636,570),(600,566)]):
    X, Y, e = sx(x), sy(y), 7*K
    d.path(f"M{X-e:.1f},{Y+3*K:.1f} L{X:.1f},{Y-8*K:.1f} L{X+e:.1f},{Y+3*K:.1f} Z",
           f"Nuchal scute {i+1}", fill="#6E6440", stroke=INK, strokeWidth=2, opacity=95)
# scale texture on the snout top: faint cobble rows
for i, (x, y, w) in enumerate([(310,556,9),(345,552,9),(380,549,10),(415,545,10),(450,542,10),
                               (485,538,9),(330,570,8),(365,567,9),(400,564,9),(435,561,9),
                               (470,558,8),(505,555,8),(540,551,9),(555,570,9),(590,562,9),
                               (620,572,9),(510,575,8),(575,585,9),(620,588,8)]):
    w *= K
    d.shape("ellipse", f"Scale {i+1}", x=sx(x) - w/2, y=sy(y) - w*0.38, width=w, height=w*0.76,
            fill="#7E7448", opacity=40, stroke="#3A341E", strokeWidth=1.2)
# ISO pits: the delta's feelers, dotted along the jaws
for i, (x, y) in enumerate([(330,574),(400,581),(470,586),(540,591),(300,570),(610,594)]):
    d.shape("ellipse", f"ISO pit {i+1}", x=sx(x) - 3, y=sy(y) - 2.3, width=6, height=4.6,
            fill="#241F10", opacity=60, stroke=NONE)

# --- the water ---------------------------------------------------------------------------
wy = 600
wdx = math.sqrt(R * R - (wy - CY) ** 2)          # chord ends on the rim
x0, x1 = CX - wdx, CX + wdx
d.path(f"M{x0:.1f},{wy} C340,594 660,594 {x1:.1f},{wy} "
       f"A{R},{R} 0 0 1 {x0:.1f},{wy} Z", "Water", fill=WATER_GRAD, stroke=NONE)
# surface skin: a cool line of light where air meets water
d.path(f"M{x0 + 4:.1f},{wy} C340,594 660,594 {x1 - 4:.1f},{wy}",
       "Waterline light", fill=NONE, stroke="#C9D8BC", strokeWidth=3, opacity=45, cap="round")
# the drowned bulk: neck and shoulders ghosting away under the surface
d.path("M330,608 C420,624 560,628 660,612 C692,678 662,752 590,782 "
       "C520,808 430,792 380,742 C344,706 328,656 330,608 Z",
       "Head ghost", fill="#101B14", opacity=20, stroke=NONE)
d.path("M600,700 C650,690 700,694 740,710", "Ghost scute row",
       fill=NONE, stroke="#223226", strokeWidth=8, opacity=20, cap="round")
# ripples spreading from the snout tip and where the nape slips under
for i, (rx, ry, op) in enumerate([(55, 6, 45), (105, 10, 30), (160, 15, 18)]):
    d.shape("ellipse", f"Tip ripple {i+1}", x=265 - rx, y=606 - ry, width=rx * 2, height=ry * 2,
            fill=NONE, stroke="#BFD2B4", strokeWidth=2.5, opacity=op)
for i, (rx, ry, op) in enumerate([(50, 6, 35), (95, 10, 22)]):
    d.shape("ellipse", f"Nape ripple {i+1}", x=688 - rx, y=604 - ry, width=rx * 2, height=ry * 2,
            fill=NONE, stroke="#BFD2B4", strokeWidth=2, opacity=op)
# duckweed + drifting specks on the skin of the water
for i, (x, y, w) in enumerate([(240,700,9),(300,760,7),(720,730,8),(790,680,7),(640,790,6),
                               (360,820,7),(560,700,5),(440,780,6),(790,720,5),(180,660,6)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Duckweed {i+1}", x=x - w/2, y=y - w/3, width=w, height=w*0.66,
            fill="#6A8258", opacity=55, stroke=NONE)
for i, dd in enumerate(["M200,700 C320,694 420,696 460,700", "M540,748 C640,742 740,744 800,750",
                        "M260,830 C380,824 500,826 560,830"]):
    d.path(dd, f"Water streak {i+1}", fill=NONE, stroke="#8AA088",
           strokeWidth=3, opacity=18, cap="round")

# --- caption ---------------------------------------------------------------------------
r1 = d.text("NILE CROCODILE", "Name", x=500, y=938, size=54, font="Virelai Sans",
            color="#DFE8CC", justify="center")
LINE2, SZ2, TRK = "CROCODYLUS NILOTICUS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=974, size=SZ2, font="Virelai Sans",
           color="#9FB08A", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for rr, lim in ((r1, 800), (r, 760)):
    b = find(layers, rr["id"])["bounds"]
    print("caption bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= lim and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("nile-crocodile-V1R00")
