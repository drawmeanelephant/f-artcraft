#!/usr/bin/env python3
"""Bactrian camel — field plate V1R00. Full-body profile facing right across
a cold Gobi dune field: twin humps on a deep barrel body, the long S-neck
carrying a small head, double-row lashes on the eye, shaggy winter fringe
down the throat and belly, breath fogging in minus-forty air. A distant
caravan walks the far dune crest. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bactrian Camel — Field Plate", 1000, 1000)

INK = "#2A1E10"   # warm dark ink, never pure black
PCX, PCY, PR = 500, 460, 420

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#141610"), (1, "#060705"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#DCD8C6"), (0.42, "#B0A88E"),
                 (0.75, "#7C7358"), (1, "#463F2C"))
DUNE_GRAD  = lin(0, 450, 0, 540, (0, "#B4A684"), (1, "#7E7050"))
FLOOR_GRAD = lin(0, 685, 0, 880, (0, "#9E8F6C"), (1, "#4A3E26"))
BODY_GRAD  = rad((0, "#B8895A"), (0.55, "#8E6236"), (1, "#54381C"))
LEG_GRAD   = lin(0, 540, 0, 690, (0, "#6E4A28"), (1, "#3A2510"))
SHAG = "#3E2A14"

# --- backdrop + cold Gobi plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#DCD8C6", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A321E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0EAD2", strokeWidth=3, opacity=40)
# low winter sun, weak and far
d.shape("ellipse", "Sun glow", x=160, y=170, width=300, height=280,
        fill=rad((0, "#F0EAD0", 40), (0.6, "#E8E0C4", 15), (1, "#E8E0C4", 0)), stroke=NONE)
d.shape("ellipse", "Sun core", x=290, y=290, width=48, height=48,
        fill="#F4EFDC", opacity=55, stroke=NONE)
# wind-driven streaks + spindrift
for i, dd in enumerate(["M160,360 C370,340 650,346 840,368",
                        "M120,470 C350,452 660,458 880,480",
                        "M190,580 C410,564 640,568 810,584"]):
    d.path(dd, f"Wind band {i+1}", fill=NONE, stroke="#EAE4D0",
           strokeWidth=16, opacity=9, cap="round")
for i, dd in enumerate(["M210,410 C430,394 640,398 800,414",
                        "M250,520 C460,506 630,510 770,522"]):
    d.path(dd, f"Wind line {i+1}", fill=NONE, stroke="#F0EADA",
           strokeWidth=4.5, opacity=22, cap="round")
for i, (x, y, w) in enumerate([(250,210,5),(430,150,4),(640,130,5),(790,210,4),(180,390,5),
                               (840,370,5),(330,280,4),(700,320,4),(150,520,5),(860,510,4)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Spindrift {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4F0E4", opacity=45, stroke=NONE)

# --- far dune: a pale crest the caravan walks, ends tapered inside the disc --------------
d.path("M118,486 C260,452 430,442 620,452 C760,458 850,470 882,482 "
       "L878,540 C700,556 420,554 240,544 L124,536 Z",
       "Far dune", fill=DUNE_GRAD, opacity=60, stroke=NONE)
d.path("M124,486 C260,452 430,442 620,452 C760,458 850,470 878,482",
       "Dune crest", fill=NONE, stroke="#EAE0C0", strokeWidth=4,
       opacity=45, cap="round")

# --- the caravan: tiny two-humped silhouettes marching right along the crest -------------
def caravan(x, y, s, i):
    """Far-line camel: body bump, two humps, neck-head tick, leg ticks."""
    d.shape("ellipse", f"Caravan body {i}", x=x, y=y-10*s, width=22*s, height=12*s,
            fill="#4E3E22", opacity=80, stroke=NONE)
    d.shape("ellipse", f"Caravan hump {i}a", x=x+4*s, y=y-15*s, width=7*s, height=7*s,
            fill="#4E3E22", opacity=80, stroke=NONE)
    d.shape("ellipse", f"Caravan hump {i}b", x=x+11*s, y=y-15*s, width=7*s, height=7*s,
            fill="#4E3E22", opacity=80, stroke=NONE)
    d.path(f"M{x+20*s:.0f},{y-8*s:.0f} C{x+24*s:.0f},{y-14*s:.0f} {x+26*s:.0f},{y-18*s:.0f} "
           f"{x+27*s:.0f},{y-20*s:.0f}",
           f"Caravan neck {i}", fill=NONE, stroke="#4E3E22",
           strokeWidth=3.5, opacity=80, cap="round")
    for j in range(3):
        lx = x + 4*s + j*6*s
        d.path(f"M{lx:.0f},{y-4*s:.0f} L{lx:.0f},{y+2*s:.0f}",
               f"Caravan leg {i}-{j}", fill=NONE, stroke="#4E3E22",
               strokeWidth=2.5, opacity=80, cap="round")

for i, (x, s) in enumerate([(180, 1.0), (235, 0.9), (288, 1.05), (345, 0.95),
                            (400, 1.0), (452, 0.85), (500, 0.9)]):
    caravan(x, 468 + (i % 3) * 2, s, i+1)

# --- near ground: cold sand closing on the disc's own arc ---------------------------------
fy = 685
fxl, fxr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fxl:.1f},{fy} C320,{fy-14} 560,{fy+6} 780,{fy-8} L{fxr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fxl:.1f},{fy} Z",
       "Ground", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fxl+6:.1f},{fy-2} C320,{fy-16} 560,{fy+4} 780,{fy-10} L{fxr-6:.1f},{fy-2}",
       "Ground crest", fill=NONE, stroke="#E4D8B4", strokeWidth=3.5,
       opacity=45, cap="round")
# snow patching the near ground — minus-forty country
for i, (x, y, w) in enumerate([(210,710,90),(380,742,70),(600,716,110),(740,760,80),
                               (300,800,120),(520,830,100),(680,806,80)]):
    if on_disc(x + w/2, y, 20):
        d.shape("ellipse", f"Snow patch {i+1}", x=x, y=y, width=w, height=w*0.28,
                fill="#ECEAE0", opacity=45, stroke=NONE)
# frost-hard ripples in the sand
for i, (y, pad) in enumerate([(715, 30), (745, 45), (780, 60)]):
    xl, xr = rim_x(y, -1) + pad, rim_x(y, 1) - pad
    xm = (xl + xr) / 2
    d.path(f"M{xl:.0f},{y} C{xm-50},{y-7} {xm+50},{y+7} {xr:.0f},{y}",
           f"Ripple {i+1}", fill=NONE, stroke="#6E5E3C", strokeWidth=3.5,
           opacity=30 - i * 6, cap="round")

# --- tail first: a thin switch hanging off the rump -----------------------------------------
d.path("M382,438 C368,472 362,512 366,548 C368,562 374,570 382,572 "
       "C376,556 374,536 378,514 C382,486 388,462 394,444 Z",
       "Tail", fill=SHAG, stroke=INK, strokeWidth=2.5)

# --- legs: thick columns on broad two-toed feet ----------------------------------------------
for i, (x0, w0, x1, w1, tone) in enumerate([
        (560, 36, 552, 24, "near"),  # front near
        (600, 30, 608, 22, "far"),   # front far
        (432, 30, 424, 22, "far"),   # rear far
        (470, 36, 478, 24, "near")]):# rear near
    fill = LEG_GRAD if tone == "near" else "#4E3418"
    d.path(f"M{x0-w0//2},536 L{x0+w0//2},536 L{x1+w1//2},684 L{x1-w1//2},684 Z",
           f"Leg {tone} {i+1}", fill=fill, stroke=INK, strokeWidth=4)
    # broad pad foot with the two toes hinted
    d.path(f"M{x1-w1//2-4},678 L{x1+w1//2+6},678 L{x1+w1//2+8},690 L{x1-w1//2-6},690 Z",
           f"Foot {tone} {i+1}", fill="#2A1A0C", stroke=INK, strokeWidth=2.5)
    d.path(f"M{x1+2},678 L{x1+2},688", f"Toe cleft {tone} {i+1}", fill=NONE,
           stroke="#4E3A20", strokeWidth=1.5, opacity=60)

# --- the barrel body + S-neck + small head, one mass ------------------------------------------
BODY = ("M754,330 "                          # muzzle tip
        "C748,316 734,308 716,306 "          # face front up to the brow
        "C702,304 692,310 686,320 "          # poll
        "C664,352 642,398 620,446 "          # back edge of the S-neck
        "C608,470 598,482 588,490 "          # neck base into the chest
        "C576,470 566,436 560,400 "          # up the front-hump slope
        "C556,382 548,372 532,370 "          # FRONT HUMP peak
        "C514,368 504,378 500,392 "          # down into the saddle dip
        "C494,378 484,370 468,372 "          # REAR HUMP peak
        "C448,374 432,388 420,408 "          # rear hump slope
        "C402,416 390,428 386,446 "          # rump round
        "C382,478 388,510 402,532 "          # rear edge down
        "C440,550 510,556 570,552 "          # underline, belly sagging
        "C600,548 612,538 618,524 "          # belly to chest front
        "C636,480 660,430 684,384 "          # front edge of the S-neck up
        "C696,364 706,350 718,342 "          # into the jaw
        "C732,336 746,332 754,330 Z")        # chin back to the muzzle
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# neck's long face catches the low sun; belly and hump dips go dark
d.path("M612,470 C640,430 668,380 692,340", "Neck light", fill=NONE,
       stroke="#D8B88C", strokeWidth=8, opacity=35, cap="round")
d.path("M492,392 C502,384 512,378 524,376", "Hump dip shade", fill=NONE,
       stroke="#3E2A14", strokeWidth=8, opacity=35, cap="round")
d.path("M440,548 C500,556 560,556 600,548", "Belly shade", fill=NONE,
       stroke="#3A2812", strokeWidth=9, opacity=30, cap="round")
d.path("M420,430 C480,470 540,510 590,540", "Barrel shade", fill=NONE,
       stroke="#54381C", strokeWidth=14, opacity=18, cap="round")

# --- winter shag: fringe along the throat, belly hem, hump tops ------------------------------
for i, dd in enumerate(["M614,500 C618,514 626,524 636,530",
                        "M630,470 C634,486 642,496 650,502",
                        "M646,440 C650,456 658,466 666,472",
                        "M662,408 C666,424 674,434 682,440"]):
    d.path(dd, f"Throat shag {i+1}", fill=NONE, stroke=SHAG,
           strokeWidth=5, opacity=55, cap="round")
for i, dd in enumerate(["M450,548 C452,560 458,568 466,572",
                        "M480,552 C482,564 488,572 496,576",
                        "M510,554 C512,566 518,574 526,578",
                        "M540,554 C542,566 548,572 556,576"]):
    d.path(dd, f"Belly shag {i+1}", fill=NONE, stroke=SHAG,
           strokeWidth=4.5, opacity=50, cap="round")
# hump tufts on the peaks
for i, (x, y) in enumerate([(528, 372), (466, 374)]):
    d.path(f"M{x-10},{y+8} L{x-4},{y-6} L{x+2},{y+4} L{x+8},{y-4} L{x+13},{y+8}",
           f"Hump tuft {i+1}", fill=NONE, stroke=SHAG, strokeWidth=5,
           opacity=60, cap="round")
# a short mane ridge on the back of the neck
d.path("M640,400 C628,428 612,456 596,478", "Nape shag", fill=NONE,
       stroke=SHAG, strokeWidth=6, opacity=45, cap="round")

# --- face: small head, heavy-lidded eye with the double lash rows ----------------------------
d.shape("ellipse", "Nostril slit", x=740, y=322, width=12, height=7,
        fill="#1A1008", stroke=NONE)
d.path("M734,344 C724,350 712,352 702,349", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# the eye — and the famous two rows of lashes, upper and lower
d.path("M694,326 C703,318 716,318 723,326 C716,333 703,333 694,326 Z",
       "Eye", fill=rad((0, "#5E3A18"), (0.75, "#241404"), (1, "#0E0804")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=707, y=322, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
for i, (x0, y0, dx, dy) in enumerate([(696,320,-5,-7),(704,317,-3,-8),(713,317,0,-8),(721,320,4,-7)]):
    d.path(f"M{x0},{y0} L{x0+dx},{y0+dy}", f"Upper lash {i+1}", fill=NONE,
           stroke=INK, strokeWidth=2.5, opacity=80, cap="round")
for i, (x0, y0, dx, dy) in enumerate([(700,331,-4,6),(709,333,0,7),(718,331,4,6)]):
    d.path(f"M{x0},{y0} L{x0+dx},{y0+dy}", f"Lower lash {i+1}", fill=NONE,
           stroke=INK, strokeWidth=2, opacity=75, cap="round")
# ear: small and furry, tucked on the poll
d.path("M682,318 C672,308 658,306 648,312 C654,324 668,328 678,324 Z",
       "Ear", fill="#6E4A28", stroke=INK, strokeWidth=3)

# --- minus-forty evidence: breath fogging ahead of the muzzle ----------------------------------
for i, (x, y, w, o) in enumerate([(772,316,34,28),(790,300,52,20),(812,284,66,13)]):
    assert on_disc(x + w/2, y + 10, 8), (x, y)
    d.shape("ellipse", f"Breath {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#ECF0EE", opacity=o, stroke=NONE)

# --- rim over everything so decor closes under it ------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A321E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0EAD2", strokeWidth=3, opacity=28)

# --- name -------------------------------------------------------------------------------------
r1 = d.text("BACTRIAN CAMEL", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#EDE4C4", justify="center")

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

d.finish("bactrian-camel-V1R00")
