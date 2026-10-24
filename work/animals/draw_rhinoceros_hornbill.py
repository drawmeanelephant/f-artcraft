#!/usr/bin/env python3
"""Rhinoceros hornbill — field plate V1R00. Side profile perched on a mossy
fig limb: the huge yellow-orange bill carrying the upswept casque, a black
body with a sheen of slate, the white banded tail hanging down the limb face,
a red eye under bristled lashes. A ripe fig hangs mid-air off the bill tip —
the toss-and-catch the species is famous for. Dipterocarp plate, fig-drop
mood — canopy gloom, leaf sprays from the rim, dappled amber light.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Rhinoceros Hornbill — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E140E"   # warm dark ink, never pure black

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
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def rim_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0B120B"), (1, "#030503"))
PLATE_GRAD = rad((0, "#8CA468"), (0.55, "#50683C"), (1, "#1D2E18"))
LIMB_GRAD  = lin(0, 640, 0, 880, (0, "#6E5238"), (0.5, "#46321E"), (1, "#261A0E"))
BODY_GRAD  = lin(500, 330, 560, 700, (0, "#424A50"), (0.5, "#262C32"), (1, "#14181C"))
WING_GRAD  = lin(560, 430, 620, 660, (0, "#363E46"), (0.6, "#1E242A"), (1, "#10141A"))
BILL_GRAD  = lin(430, 360, 205, 420,
                 (0, "#D2681E"), (0.35, "#E8862E"), (0.7, "#F2B03E"), (1, "#F6C86A"))
TAIL_GRAD  = lin(640, 630, 720, 790, (0, "#F4F0E2"), (0.7, "#DDD6C0"), (1, "#B4AA8E"))

# --- backdrop + dipterocarp plate ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#7E9462", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#16220F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2B4", strokeWidth=3, opacity=30)

# dappled amber light through a canopy gap, upper left, fading before the rim
d.shape("ellipse", "Canopy light", x=230, y=110, width=380, height=240,
        fill=rad((0, "#E8DCA0", 26), (0.6, "#E8DCA0", 10), (1, "#E8DCA0", 0)), stroke=NONE)
d.shape("ellipse", "Light pool 2", x=560, y=280, width=240, height=150,
        fill=rad((0, "#D8D094", 14), (1, "#D8D094", 0)), stroke=NONE)

# leaf sprays hanging in from the top rim — dipterocarp canopy
for i, (x, y, s) in enumerate([(195, 205, 1), (290, 145, -1), (755, 155, 1), (805, 225, -1)]):
    assert on_disc(x, y, 20), (x, y)
    for k in range(3):
        lx, ly = x + k * 24 * s, y + k * 15
        d.path(f"M{lx},{ly} C{lx + 16*s},{ly - 9} {lx + 30*s},{ly + 2} {lx + 34*s},{ly + 17} "
               f"C{lx + 18*s},{ly + 20} {lx + 4*s},{ly + 11} {lx},{ly} Z",
               f"Leaf {i*3+k+1}", fill="#1A2912", opacity=55, stroke=NONE)
# a liana swaying down the right side
d.path("M790,180 C782,230 796,290 810,340 C818,372 816,404 804,428",
       "Liana", fill=NONE, stroke="#263318", strokeWidth=5, opacity=45, cap="round")
# drifting motes in the light shaft
for i, (x, y, w) in enumerate([(300, 240, 5), (370, 180, 4), (430, 250, 5),
                               (250, 330, 4), (600, 330, 4), (700, 400, 5)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0E4B0", opacity=40, stroke=NONE)

# --- the fig limb: a mossy bough across the lower third, arc-closed --------------
ly_l, ly_r = 712, 652
xl, xr = rim_x(ly_l, -1), rim_x(ly_r, 1)
d.path(f"M{xl:.1f},{ly_l} C300,700 420,706 540,690 C640,678 760,662 {xr:.1f},{ly_r} "
       f"A{PR},{PR} 0 0 1 {xl:.1f},{ly_l} Z", "Fig limb", fill=LIMB_GRAD, stroke=NONE)
# sunlit top edge of the limb
d.path(f"M{xl + 8:.1f},{ly_l} C300,700 420,706 540,690 C640,678 760,662 {xr - 8:.1f},{ly_r}",
       "Limb rim light", fill=NONE, stroke="#A88A58", strokeWidth=4, opacity=40, cap="round")
# moss pad along the perch line
d.path(f"M300,700 C400,706 520,696 620,680", "Moss pad", fill=NONE,
       stroke="#5E7A3A", strokeWidth=9, opacity=45, cap="round")
for i, (x, y) in enumerate([(340, 702), (430, 704), (540, 690), (640, 678), (730, 664)]):
    d.path(f"M{x},{y} l-3,-14 M{x + 5},{y} l2,-11 M{x - 6},{y + 2} l-6,-9",
           f"Moss tuft {i+1}", fill=NONE, stroke="#6E8A44", strokeWidth=2.5,
           opacity=55, cap="round")
# bark fissures down the limb face
for i, dd in enumerate(["M260,760 C400,748 560,752 720,742",
                        "M320,810 C450,800 580,806 690,798"]):
    d.path(dd, f"Bark seam {i+1}", fill=NONE, stroke="#241708",
           strokeWidth=5, opacity=40, cap="round")

# ripe figs growing straight off the limb — cauliflory cluster, right side
for i, (x, y, w) in enumerate([(716, 636, 34), (762, 622, 40), (800, 646, 30), (742, 662, 26)]):
    d.shape("ellipse", f"Fig {i+1}", x=x - w / 2, y=y - w / 2, width=w, height=w,
            fill=rad((0, "#D8643E"), (0.7, "#B0402A"), (1, "#7E2418")), stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"Fig eye {i+1}", x=x - 4, y=y + w * 0.3, width=8, height=5,
            fill="#5E1A10", opacity=60, stroke=NONE)
    d.path(f"M{x},{y - w / 2} l0,-10", f"Fig stem {i+1}", fill=NONE,
           stroke="#4A5E2A", strokeWidth=3, cap="round")

# the bird's contact shadow on the limb
d.shape("ellipse", "Perch shadow", x=430, y=668, width=260, height=30,
        fill=rad((0, "#1A0E04", 50), (1, "#1A0E04", 0)), stroke=NONE)

# === the hornbill =================================================================
# white tail hanging down the limb face, black band across it
d.path("M618,640 C640,660 668,700 690,738 C700,756 710,772 716,782 "
       "C700,784 680,780 664,768 C640,750 620,712 608,672 Z",
       "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=4)
d.path("M652,704 C664,722 680,746 694,764", "Tail band", fill=NONE,
       stroke="#1A1E22", strokeWidth=13, opacity=85, cap="round")
d.path("M628,660 C646,684 666,716 684,750", "Tail feather split", fill=NONE,
       stroke="#B4AA8E", strokeWidth=3, opacity=60, cap="round")

# body — upright perch, breast forward, crown rising to the nape
d.path("M450,314 C500,328 548,368 578,415 C615,470 645,540 640,600 "
       "C637,622 628,638 614,650 C560,668 480,662 435,622 "
       "C395,582 385,520 395,470 C400,430 420,390 442,352 "
       "C444,336 446,324 450,314 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# breast light — the front edge catching the canopy gap
d.path("M400,470 C392,520 398,575 428,615", "Breast light", fill=NONE,
       stroke="#6E7A82", strokeWidth=10, opacity=35, cap="round")
# white belly/vent patch before the tail
d.path("M555,624 C585,632 608,644 616,656 C585,664 545,662 522,650 "
       "C534,640 546,630 555,624 Z",
       "Vent patch", fill="#EDE8D8", opacity=90, stroke="#8E8672", strokeWidth=2)

# folded wing — slate-black rows of scalloped coverts, weather made of feathers
d.path("M560,432 C600,470 625,540 620,605 C618,632 608,652 592,660 "
       "C560,650 538,610 532,560 C528,510 538,465 560,432 Z",
       "Wing", fill=WING_GRAD, stroke=INK, strokeWidth=5)
for row, (yy, w0) in enumerate([(500, 62), (545, 66), (590, 60)]):
    for j in range(3):
        x = 545 + j * (w0 / 2.2) + (row % 2) * 14
        d.path(f"M{x - 16},{yy} Q{x},{yy + 14} {x + 16},{yy}",
               f"Covert {row*3+j+1}", fill=NONE, stroke="#4E5A64",
               strokeWidth=4, opacity=55, cap="round")
# pale tips on the secondaries — short streaks along the wing's lower edge
for i, (x0, y0) in enumerate([(566, 622), (582, 634), (596, 644)]):
    d.path(f"M{x0},{y0} C{x0 + 6},{y0 + 8} {x0 + 14},{y0 + 13} {x0 + 24},{y0 + 15}",
           f"Wing tip {i+1}", fill=NONE, stroke="#E8E2D0", strokeWidth=4,
           opacity=55, cap="round")

# legs + zygodactyl feet gripping the limb's top edge
for i, (x, y) in enumerate([(480, 660), (545, 668)]):
    d.path(f"M{x},{y} C{x - 4},{y + 14} {x - 2},{y + 24} {x + 2},{y + 30}",
           f"Leg {i+1}", fill=NONE, stroke="#5E6668", strokeWidth=8, cap="round")
    fx, fy = x + 2, y + 30
    for k, (tx, ty) in enumerate([(-18, 6), (-6, 10), (8, 10), (18, 4)]):
        d.path(f"M{fx},{fy} C{fx + tx*0.5},{fy + 4} {fx + tx*0.8},{fy + ty*0.7} {fx + tx},{fy + ty}",
               f"Toe {i*4+k+1}", fill=NONE, stroke="#5E6668",
               strokeWidth=5, cap="round")

# head — a strokeless fill merging into the body's crown; the silhouette
# is carried by the body outline above and the bill's back edge in front
d.path("M452,318 C470,314 492,320 504,336 C514,352 512,372 500,388 "
       "C486,404 464,412 444,412 C428,410 416,400 412,386 "
       "C408,366 414,340 430,328 C438,322 444,320 452,318 Z",
       "Head", fill=lin(460, 315, 470, 410, (0, "#3A4148"), (1, "#1A1E24")),
       stroke=NONE)

# === the bill + casque: one silhouette, the species signature ======================
d.path("M448,322 C416,296 390,278 356,270 C322,262 292,258 270,262 "
       "C251,265 243,276 247,293 C251,307 263,319 282,330 "
       "C296,338 306,344 313,353 C282,368 246,389 206,410 "
       "C195,415 192,423 199,429 C250,438 320,441 370,437 "
       "C400,434 418,429 428,420 C434,396 440,356 448,322 Z",
       "Bill and casque", fill=BILL_GRAD, stroke=INK, strokeWidth=5)
# casque colour zone — the redder mass riding the rear of the bill
d.path("M444,324 C416,300 392,284 362,276 C334,268 306,264 282,268 "
       "C270,270 264,278 266,290 C284,288 308,292 334,302 "
       "C372,316 414,324 444,324 Z",
       "Casque flush", fill="#B04A1E", opacity=75, stroke=NONE)
# casque horn sheen — the upturned front tip catching light
d.path("M270,264 C258,268 251,278 254,290", "Horn light", fill=NONE,
       stroke="#F6C86A", strokeWidth=5, opacity=70, cap="round")
# culmen ridge light down the blade
d.path("M308,360 C272,374 240,392 212,406", "Culmen light", fill=NONE,
       stroke="#F8D88A", strokeWidth=4, opacity=55, cap="round")
# tomium seam + the tip's dark nail
d.path("M335,431 C290,433 245,431 205,423", "Tomium", fill=NONE,
       stroke="#8A3A14", strokeWidth=3, opacity=55, cap="round")
d.path("M206,410 C196,415 193,423 199,429 C211,433 221,433 229,431 "
       "C221,425 213,418 206,410 Z", "Bill tip nail", fill="#8A3A14", opacity=60, stroke=NONE)
# the seam where the casque's front foot lands on the mandible
d.path("M313,352 C340,362 375,368 420,372", "Casque seam", fill=NONE,
       stroke="#8A3A14", strokeWidth=3.5, opacity=60, cap="round")
# nostril slit at the casque foot
d.path("M352,352 C364,350 376,352 384,358", "Nostril", fill=NONE,
       stroke="#6E2A10", strokeWidth=4, opacity=70, cap="round")

# lower mandible — smaller blade tucked under the upper bill's rear half
d.path("M425,420 C390,428 350,434 315,434 C308,434 306,440 314,444 "
       "C345,452 390,450 415,440 C422,435 425,428 425,420 Z",
       "Lower bill", fill=lin(420, 420, 330, 450, (0, "#E8A040"), (1, "#B06020")),
       stroke=INK, strokeWidth=3.5)
# gape line running back under the eye
d.path("M315,438 C360,444 405,442 428,432", "Gape", fill=NONE,
       stroke="#7E3010", strokeWidth=3, opacity=60, cap="round")

# bare skin + the red eye under bristled lashes
d.shape("ellipse", "Eye skin", x=400, y=348, width=40, height=36,
        fill="#C8D2D6", opacity=30, stroke=NONE)
d.shape("ellipse", "Iris", x=408, y=354, width=22, height=22,
        fill=rad((0, "#D84030"), (1, "#8E1E14")), stroke="#5E140C", strokeWidth=2)
d.shape("ellipse", "Pupil", x=414, y=360, width=10, height=10,
        fill="#120A08", stroke=NONE)
d.shape("ellipse", "Glint", x=412, y=357, width=5, height=5,
        fill="#FFF6DC", opacity=85, stroke=NONE)
for i, (a) in enumerate([-75, -45, -18]):
    r_ = math.radians(a)
    x0, y0 = 419 + 16 * math.cos(r_), 360 + 16 * math.sin(r_)
    d.path(f"M{x0:.1f},{y0:.1f} L{x0 + 10 * math.cos(r_):.1f},{y0 + 10 * math.sin(r_):.1f}",
           f"Lash {i+1}", fill=NONE, stroke="#10141A", strokeWidth=3, cap="round")

# throat pouch shade under the bill base
d.path("M424,430 C440,450 452,470 456,492", "Throat shade", fill=NONE,
       stroke="#101418", strokeWidth=12, opacity=30, cap="round")

# === the dropped fig — mid-air below the bill tip, falling streaks clear of it ====
fx, fy = 252, 508
d.shape("ellipse", "Dropped fig", x=fx - 15, y=fy - 15, width=30, height=30,
        fill=rad((0, "#D8643E"), (0.7, "#B0402A"), (1, "#7E2418")), stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Dropped fig eye", x=fx - 4, y=fy + 8, width=8, height=5,
        fill="#5E1A10", opacity=60, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(236, 452, 242, 474), (258, 458, 260, 480)]):
    d.path(f"M{x0},{y0} C{x0 + 4},{y0 + 8} {x1 - 3},{y1 - 6} {x1},{y1}",
           f"Fall streak {i+1}", fill=NONE, stroke="#E8DCA0",
           strokeWidth=2.5, opacity=45, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#121C0A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2B4", strokeWidth=3, opacity=25)

# --- name -------------------------------------------------------------------------
r1 = d.text("RHINOCEROS HORNBILL", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#E2E8C0", justify="center")

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

d.finish("rhinoceros-hornbill-V1R00")
