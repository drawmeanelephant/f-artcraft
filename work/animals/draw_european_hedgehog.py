#!/usr/bin/env python3
"""European hedgehog — field plate V1R00. A walking bristle on the night
round: domed spine mass in profile ambling left through the leaf litter,
pale fawn face under the prickle line, snout down on the trail of the
garden snail waiting ahead. Hedgerow plate, leaf-fall mood — bare bramble
canes on the crest, rust and wine leaves closing on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("European Hedgehog — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#181210"                    # warm dark ink, never pure black

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

# pointed vesica leaf blade with a mid-vein, rotated into place
def leaf(x, y, w, a, col, lab, op=90):
    t = math.radians(a); c, s = math.cos(t), math.sin(t)
    def rot(px, py):
        return (x + px * c - py * s, y + px * s + py * c)
    h = w * 0.42
    p0 = rot(-w / 2, 0); p1 = rot(0, -h / 2); p2 = rot(w / 2, 0); p3 = rot(0, h / 2)
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} "
           f"Q{p3[0]:.1f},{p3[1]:.1f} {p0[0]:.1f},{p0[1]:.1f} Z",
           lab, fill=col, opacity=op, stroke=NONE)
    va, vb = rot(-w * 0.38, 0), rot(w * 0.38, 0)
    d.path(f"M{va[0]:.0f},{va[1]:.0f} L{vb[0]:.0f},{vb[1]:.0f}",
           lab + " vein", fill=NONE, stroke="#3A2414", strokeWidth=2,
           opacity=45, cap="round")

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#161014"), (1, "#070405"))
PLATE_GRAD = rad((0, "#8A6E4E"), (0.5, "#4E3C2C"), (1, "#1E140E"))
FLOOR_GRAD = lin(0, 630, 0, 880, (0, "#34241A"), (1, "#140C08"))
SPINE     = rad((0, "#6E5844"), (0.55, "#4A3A2C"), (1, "#241A12"))
FUR       = rad((0, "#D8BA8E"), (0.65, "#B08E62"), (1, "#7E5E3E"))
LEAVES    = ["#B8642E", "#C89A3E", "#8E3830", "#9E5626", "#7E5A24"]

# --- backdrop + autumn dusk plate -----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(160,130,4),(840,140,5),(120,460,3),(880,520,4),
                               (190,740,4),(850,770,4),(280,160,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C8B8", opacity=26, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A6E4E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#241812", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0CCA8", strokeWidth=3, opacity=38)

# a thin amber moon riding low over the hedge
MX2, MY2 = 300, 200
d.shape("ellipse", "Moon glow", x=MX2-52, y=MY2-52, width=104, height=104,
        fill="#E8B06E", opacity=7, stroke=NONE)
d.shape("ellipse", "Moon", x=MX2-30, y=MY2-30, width=60, height=60,
        fill=rad((0, "#F2DCA8"), (0.75, "#E0B876"), (1, "#B8884E")), stroke=NONE)
d.shape("ellipse", "Moon shade", x=MX2-40, y=MY2-38, width=56, height=56,
        fill="#4E3C2C", opacity=55, stroke=NONE)
# last light low behind the hedge — a smothered amber dusk
d.shape("ellipse", "Dusk glow", x=240, y=380, width=540, height=280,
        fill=rad((0, "#E8A85E", 38), (0.55, "#E8A85E", 12), (1, "#E8A85E", 0)),
        stroke=NONE)
# hedgerow: bare bramble canes rising out of the floor (bases sink under it)
for i, (x0, y0, x1, y1, x2, y2) in enumerate([
        (210, 740, 196, 540, 224, 448), (310, 740, 330, 510, 306, 430),
        (430, 740, 420, 530, 448, 452), (600, 740, 616, 520, 592, 440),
        (720, 740, 700, 530, 730, 452), (800, 740, 812, 550, 796, 470)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{(y0+y1)/2-20} {(x1+x2)/2},{(y1+y2)/2} {x2},{y2}",
           f"Cane {i+1}", fill=NONE, stroke="#120C08", strokeWidth=5,
           opacity=90, cap="round")
# cane thorns + a few held leaves on the brambles
for i, (x, y, dx, dy) in enumerate([(206,560,-12,-4),(320,540,14,-6),(432,540,-12,-6),
                                    (608,560,14,-4),(712,556,-14,-6),(804,566,12,-4)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Thorn {i+1}", fill=NONE,
           stroke="#120C08", strokeWidth=3, opacity=80, cap="round")
for i, (x, y, a) in enumerate([(232,452,-30),(306,436,20),(596,442,-15),(726,456,35)]):
    leaf(x, y, 30, a, "#8E5426", f"Held leaf {i+1}", op=85)

# --- leaf-litter floor closing on the arc ----------------------------------------
fy = 660
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C260,646 400,656 540,648 C660,644 780,652 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+10:.1f},{fy-2} C260,644 400,652 540,646 C660,642 770,648 {fr-10:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#C8A06A", strokeWidth=4, opacity=26, cap="round")
# fallen leaves scattered over the litter
for i, (x, y, w, a) in enumerate([(230,700,44,-20),(330,760,40,25),(450,730,36,-35),
                                  (560,790,42,15),(660,720,38,-25),(760,770,40,30),
                                  (270,800,36,10),(390,700,34,-10),(520,690,32,40),
                                  (700,820,38,-15),(600,840,34,20),(180,760,32,-30)]):
    leaf(x, y, w, a, LEAVES[i % len(LEAVES)], f"Leaf {i+1}", op=80)

# --- the snail waiting on the trail, ahead left -----------------------------------
SNX, SNY = 218, 700
d.path(f"M{SNX-40},{SNY+16} C{SNX-30},{SNY+2} {SNX-8},{SNY-2} {SNX+14},{SNY} "
       f"C{SNX+32},{SNY+2} {SNX+38},{SNY+10} {SNX+32},{SNY+16} "
       f"C{SNX+12},{SNY+24} {SNX-22},{SNY+26} {SNX-40},{SNY+16} Z",
       "Snail body", fill=rad((0, "#B09A72"), (1, "#6E5840")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Snail shell", x=SNX-34, y=SNY-34, width=52, height=48,
        fill=rad((0, "#A87E4E"), (0.7, "#7E5A34"), (1, "#503A22")),
        stroke=INK, strokeWidth=3.5)
d.path(f"M{SNX-16},{SNY-10} a12,11 0 1 1 15,-9 a6.5,6 0 1 0 9,7",
       "Shell spiral", fill=NONE, stroke="#3E2C18", strokeWidth=3, cap="round")
for sgn in (-1, 1):
    d.path(f"M{SNX+18},{SNY+2} C{SNX+22+sgn*4},{SNY-12} {SNX+24+sgn*6},{SNY-20} {SNX+24+sgn*8},{SNY-26}",
           f"Eyestalk {sgn}", fill=NONE, stroke="#8A7454", strokeWidth=3.5, cap="round")
    d.shape("ellipse", f"Snail eye {sgn}", x=SNX+21+sgn*8, y=SNY-32,
            width=7, height=7, fill="#241A10", stroke=NONE)

# contact shadow under the hog
d.shape("ellipse", "Body shadow", x=300, y=676, width=430, height=52,
        fill="#060403", opacity=48, stroke=NONE)

# === the hedgehog: a walking dome of banded spines, profile left ==================
# body mound: the prickle dome sweeping from rump to the face line at the snout
DOME = ("M400,548 "                                   # brow where spines meet face
        "C420,480 470,432 540,422 "                   # dome front to crest
        "C618,412 680,442 712,502 "                   # crest over the rump
        "C732,540 736,586 722,630 "                   # rump curve down
        "C706,662 668,682 618,690 "                   # under-rump
        "C540,700 440,698 380,676 "                   # long low belly line
        "C360,670 350,658 350,642 "                   # chest tuck
        "C352,610 370,570 400,548 Z")                 # up the face to the brow
d.path(DOME, "Prickle dome", fill=SPINE, stroke=INK, strokeWidth=6)

# quill field: rows of banded strokes covering the dome, leaning rearward
import random
random.seed(7)
qn = 0
for row, (y, x0, x1, lean) in enumerate([
        (452, 480, 640, 0.5), (478, 440, 690, 0.45), (505, 415, 715, 0.4),
        (532, 405, 725, 0.35), (560, 410, 725, 0.3), (588, 415, 715, 0.25),
        (616, 425, 700, 0.2), (644, 445, 680, 0.15), (668, 470, 650, 0.1)]):
    n = max(3, int((x1 - x0) / 26))
    for j in range(n):
        qn += 1
        bx = x0 + j * 26 + random.uniform(-6, 6)
        by = y + random.uniform(-5, 5)
        col = "#D8C8A8" if (row * 7 + j) % 3 == 0 else "#1E160F"
        d.path(f"M{bx:.0f},{by:.0f} L{bx + 22 * lean + random.uniform(-4, 4):.0f},{by - 24:.0f}",
               f"Quill {qn}", fill=NONE, stroke=col, strokeWidth=3.4,
               opacity=85, cap="round")

# face: a broad pale fawn wedge from the brow down to the snout tip
d.path("M400,548 "                                   # brow
       "C376,560 356,586 346,616 "                   # face front
       "C336,646 318,662 296,668 "                   # snout bridge down
       "C282,672 268,674 260,668 "                   # nose tip
       "C254,662 258,652 272,650 "                   # under the nose
       "C306,644 340,646 372,662 "                   # jaw sweeping back
       "C390,670 410,678 432,682 "                   # throat into the belly line
       "C404,660 392,600 400,548 Z",                 # back edge up to the brow
       "Face", fill=FUR, stroke=INK, strokeWidth=5)
# parting line between prickles and the face
d.path("M400,548 C420,532 448,526 476,530", "Prickle line", fill=NONE,
       stroke="#241A12", strokeWidth=5, opacity=70, cap="round")
# pale nape highlight where the dusk catches the crest
d.path("M452,468 C510,436 600,434 666,478", "Crest light", fill=NONE,
       stroke="#E8C890", strokeWidth=7, opacity=28, cap="round")

# legs — little dark feet stepping under the skirt, drawn over the dome
for i, (x, y, s) in enumerate([(430,688,1),(510,696,1),(575,686,1),(385,680,0.85)]):
    d.path(f"M{x-16*s},{y+12} C{x-18*s},{y} {x-10*s},{y-10} {x},{y-12} "
           f"C{x+10*s},{y-10} {x+18*s},{y} {x+16*s},{y+12} "
           f"C{x+8*s},{y+18} {x-8*s},{y+18} {x-16*s},{y+12} Z",
           f"Foot {i+1}", fill="#2A2018", stroke=INK, strokeWidth=3)

# --- face furniture ----------------------------------------------------------------
d.shape("ellipse", "Eye", x=352, y=596, width=22, height=24,
        fill="#140E0A", stroke=NONE)
d.shape("ellipse", "Glint", x=358, y=602, width=6, height=6,
        fill="#FFFFFF", opacity=92, stroke=NONE)
# little ear half under the prickle line
d.path("M402,556 C408,540 424,534 436,542 C446,550 444,566 432,572 "
       "C418,578 404,570 402,556 Z", "Ear", fill="#6E5236",
       stroke=INK, strokeWidth=3.5)
# dark wet nose at the tip
d.path("M262,664 C254,658 254,648 264,646 C276,644 284,652 282,662 "
       "C280,670 268,670 262,664 Z", "Nose", fill="#1C1410", stroke=NONE)
# mouth line back under the jaw
d.path("M282,668 C306,664 330,662 348,662", "Mouth", fill=NONE,
       stroke="#5E422A", strokeWidth=3, opacity=80, cap="round")
# sniff whiskers reaching for the snail
for j, (y0, dy) in enumerate([(652, -6), (660, 2)]):
    d.path(f"M268,{y0} C246,{y0+dy} 230,{y0+dy+2} 216,{y0+dy}",
           f"Whisker {j+1}", fill=NONE, stroke="#C8B494",
           strokeWidth=2.5, opacity=60, cap="round")

# a straggler leaf riding the prickle dome — leaf-fall, after all
leaf(560, 452, 40, -25, "#C89A3E", "Riding leaf", op=95)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#120A08", strokeWidth=6)

# --- name --------------------------------------------------------------------------
r1 = d.text("EUROPEAN HEDGEHOG", "Name", x=500, y=962, size=44, font="Virelai Sans",
            color="#E4D4B8", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("european-hedgehog-V1R00")
