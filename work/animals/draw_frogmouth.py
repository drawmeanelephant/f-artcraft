#!/usr/bin/env python3
"""Tawny frogmouth — field-guide plate V1R00. Bolt upright doing its best
broken-branch impression: a huge flat frog-mouth beak pointing skyward,
orange eyes narrowed to judgemental slits, bark-mottled silver-grey plumage.
Moonlit night-forest plate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tawny Frogmouth — Field Plate", 1000, 1000)
rng = random.Random(41)   # fixed seed: same mottling every run

INK = "#24211C"
CX, CY, R = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def disc_x(y, side, r=420):
    return CX + side*math.sqrt(r*r - (y - CY)**2)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#152019"), (1, "#050A08"))
PLATE_GRAD = rad((0, "#DEE4DA"), (0.62, "#A2AEA4"), (1, "#5F6E64"))
PLUME_GRAD = rad((0, "#A8A397"), (0.6, "#7E7969"), (1, "#4E4A40"))
WING_GRAD  = lin(0, 480, 0, 780, (0, "#6E695C"), (1, "#45413A"))
BEAK_GRAD  = lin(0, 300, 0, 560, (0, "#55504A"), (1, "#221E19"))
IRIS_GRAD  = rad((0, "#F6B04A"), (0.6, "#DE7E20"), (1, "#96480E"))
LID_GRAD   = lin(0, 430, 0, 510, (0, "#8A8474"), (1, "#5E594D"))
BRANCH_GRAD = lin(0, 720, 0, 820, (0, "#6E5C48"), (1, "#3A2F24"))

# --- backdrop + night-forest plate ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(140,150,4),(250,80,3),(80,380,5),(900,120,4),(940,340,3),
                               (870,560,4),(110,660,3),(180,900,4),(830,880,4),(950,720,3)]):
    d.shape("ellipse", f"Night mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#BCD8C4", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A584C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8EEE4", strokeWidth=3, opacity=50)
# moon glow high-left + blurred trunk shadows down the plate
d.shape("ellipse", "Moon glow", x=190, y=120, width=200, height=200,
        fill="#F4F6EC", opacity=16, stroke=NONE)
d.shape("ellipse", "Moon", x=240, y=160, width=96, height=96,
        fill=rad((0, "#F8FAF0"), (1, "#D8DCC8")), opacity=85, stroke=NONE)
for i, (x, w, o) in enumerate([(170,42,20),(300,26,14),(690,34,16),(790,48,20)]):
    d.shape("ellipse", f"Trunk shade {i+1}", x=x, y=90, width=w, height=680,
            fill="#3E4C42", opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(210,330,7),(780,300,6),(150,520,8),(840,500,7),(330,140,6),
                               (620,130,6),(250,680,6),(760,660,7),(420,110,5)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A685C", opacity=38, stroke=NONE)

# --- the perch: a broken limb, both ends closing on the disc arc ------------------
xL, xR = disc_x(742, -1), disc_x(738, 1)
bL, bR = disc_x(792, -1), disc_x(796, 1)
d.path(f"M{xL:.1f},742 C360,730 470,736 560,730 C660,724 760,726 {xR:.1f},738 "
       f"A{R},{R} 0 0 1 {bR:.1f},796 C660,788 340,780 {bL:.1f},792 "
       f"A{R},{R} 0 0 1 {xL:.1f},742 Z",
       "Perch", fill=BRANCH_GRAD, stroke=INK, strokeWidth=5)
d.path(f"M{xL+8:.1f},740 C360,728 470,734 560,728 C660,722 760,724 {xR-8:.1f},736",
       "Perch top light", fill=NONE, stroke="#A89478", strokeWidth=4, opacity=45, cap="round")
# broken stub sprouting off the limb
d.path("M646,742 C660,712 674,692 692,682 L702,696 C688,706 676,726 668,748 Z",
       "Limb stub", fill=BRANCH_GRAD, stroke=INK, strokeWidth=4)
d.path("M692,682 L712,668 L706,690 Z", "Stub break", fill="#8E7A60", stroke=INK, strokeWidth=3)
for i, dd in enumerate(["M240,756 C320,750 400,754 470,760", "M540,758 C620,750 700,748 780,754",
                        "M300,776 C380,772 440,774 500,778"]):
    d.path(dd, f"Bark groove {i+1}", fill=NONE, stroke="#241D16", strokeWidth=3, opacity=45, cap="round")

# --- body: one upright mottled stump, base sitting on the perch --------------------
# leans a hair right of centre — the branch impersonation
d.path("M505,352 C580,352 636,410 648,498 C660,584 650,680 632,748 "
       "C600,762 400,764 366,748 C348,680 342,584 354,498 "
       "C366,410 430,352 505,352 Z",
       "Body", fill=PLUME_GRAD, stroke=INK, strokeWidth=7)
# flank wing folds
d.path("M372,540 C352,610 348,690 362,748 C392,734 408,668 408,596 C396,570 384,552 372,540 Z",
       "Wing fold L", fill=WING_GRAD, stroke=INK, strokeWidth=4)
d.path("M632,530 C652,600 654,680 640,746 C612,730 598,664 600,592 C612,566 622,546 632,530 Z",
       "Wing fold R", fill=WING_GRAD, stroke=INK, strokeWidth=4)
# long bark streaks — the camouflage
for i, (x0, y0, x1, y1) in enumerate([(420,560,412,730),(460,580,458,742),(500,590,500,748),
                                      (540,580,546,742),(584,560,594,728),(390,600,382,720),
                                      (616,590,624,716)]):
    d.path(f"M{x0},{y0} C{x0-4},{(y0+y1)/2} {x1+4},{(y0+y1)/2} {x1},{y1}",
           f"Bark streak {i+1}", fill=NONE, stroke="#3A362E", strokeWidth=5, opacity=35, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(438,570,432,700),(480,600,478,730),(522,600,526,730),(566,570,572,700)]):
    d.path(f"M{x0},{y0} C{x0-3},{(y0+y1)/2} {x1+3},{(y0+y1)/2} {x1},{y1}",
           f"Bark streak light {i+1}", fill=NONE, stroke="#CFC8B4", strokeWidth=4, opacity=30, cap="round")
# seeded mottle: tawny + charcoal blotches over the whole body
def inside_body(x, y):
    if y < 360 or y > 745:
        return False
    half = 100 if y < 500 else 145
    return abs(x - 502) < half
n = 0
while n < 60:
    x, y = rng.uniform(350, 655), rng.uniform(370, 745)
    if not inside_body(x, y) or (400 < x < 600 and 430 < y < 560):
        continue
    w = rng.uniform(6, 18); h = w * rng.uniform(0.5, 1.1)
    col = rng.choice(["#3A342C", "#3A342C", "#C8B99E", "#5E594D"])
    d.shape("ellipse", f"Mottle {n+1}", x=round(x,1), y=round(y,1), width=round(w,1), height=round(h,1),
            fill=col, opacity=rng.randint(25, 48), stroke=NONE)
    n += 1
# shoulders lighter at the "neck"
d.path("M410,430 C450,404 560,404 598,432", "Neck light", fill=NONE,
       stroke="#DCD6C4", strokeWidth=10, opacity=22, cap="round")

# --- the head: crown dome flowing straight into the huge beak -------------------------
# the beak is the branch tip: a tall flat kite, tip hooked a touch right
d.path("M500,318 C516,310 532,316 538,332 "
       "C566,416 592,462 600,490 C590,514 570,534 548,546 "
       "C530,554 514,558 500,560 C486,558 470,554 452,546 "
       "C430,534 410,514 400,490 C408,462 434,416 466,336 "
       "C472,320 486,312 500,318 Z",
       "Beak", fill=BEAK_GRAD, stroke=INK, strokeWidth=6)
# culmen ridge + cutting-edge lines along both sides of the kite
d.path("M505,346 C514,398 516,476 506,550", "Culmen", fill=NONE,
       stroke="#8A8478", strokeWidth=5, opacity=45, cap="round")
d.path("M472,348 C442,424 418,466 402,490", "Tomium L", fill=NONE,
       stroke="#0E0C09", strokeWidth=4, opacity=55, cap="round")
d.path("M532,348 C560,424 584,466 598,490", "Tomium R", fill=NONE,
       stroke="#0E0C09", strokeWidth=4, opacity=55, cap="round")
# the gape: a wide flat mouth line sweeping cheek to cheek under the eyes
d.path("M388,548 C440,566 560,566 612,548", "Gape", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M400,556 C450,572 550,572 600,556", "Gape lip", fill=NONE,
       stroke="#B8A88E", strokeWidth=3, opacity=45, cap="round")
# rictal bristles fanning at the beak corners, staying inside the silhouette
for i, (x0, y0, x1, y1) in enumerate([(404,496,356,474),(406,506,358,498),(408,514,362,520),
                                      (596,496,644,472),(594,506,642,496),(592,514,638,518)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{y0-6} {(x0+x1)/2},{y1-4} {x1},{y1}",
           f"Rictal {i+1}", fill=NONE, stroke="#4E4A40", strokeWidth=2.5, opacity=60, cap="round")

# --- eyes: orange slivers half-buried under heavy lids — the judgement --------------
for side, cx in (("L", 424), ("R", 578)):
    cy = 520
    d.shape("ellipse", f"Socket {side}", x=cx-40, y=cy-34, width=80, height=68,
            fill="#55504A", opacity=40, stroke=NONE)
    # lower crescent of orange iris — only the bottom half survives the lid
    d.path(f"M{cx-30},{cy+4} A30,30 0 0 1 {cx+30},{cy+4} Z",
           f"Iris {side}", fill=IRIS_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil slit {side}", x=cx-5, y=cy-6, width=10, height=18,
            fill="#140F08", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=cx-12, y=cy-2, width=8, height=6,
            fill="#FFFFFF", opacity=70, stroke=NONE)
    # the lid: a heavy drooping chord that carries the deadpan
    d.path(f"M{cx-32},{cy-8} C{cx-14},{cy-20} {cx+16},{cy-20} {cx+32},{cy-8} "
           f"C{cx+18},{cy+2} {cx-18},{cy+2} {cx-32},{cy-8} Z",
           f"Lid {side}", fill=LID_GRAD, stroke=INK, strokeWidth=4)
    d.path(f"M{cx-32},{cy-8} C{cx-12},{cy-20} {cx+14},{cy-20} {cx+32},{cy-8}",
           f"Lid edge {side}", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# fine brow furrows over the lids
for i, (x0, x1) in enumerate([(396,452),(550,606)]):
    for k in range(3):
        y = 486 - k*9
        d.path(f"M{x0+8},{y} Q{(x0+x1)/2},{y-10} {x1-8},{y}", f"Brow furrow {i*3+k+1}",
               fill=NONE, stroke="#3A362E", strokeWidth=3, opacity=35, cap="round")

# crown texture: short strokes following the dome, tucked inside the silhouette
for i, (x0, y0, x1, y1) in enumerate([(392,420,384,396),(416,396,410,372),(586,396,592,372),(610,420,618,396)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{(y0+y1)/2-6} {(x0+x1)/2},{(y0+y1)/2+4} {x1},{y1}",
           f"Crown stub {i+1}", fill=NONE, stroke="#55504A", strokeWidth=5, opacity=55, cap="round")

# toes gripping the limb
for i, x in enumerate([446, 462, 478, 522, 538, 554]):
    d.shape("ellipse", f"Toe {i+1}", x=x-7, y=734, width=14, height=18,
            fill="#55504A", stroke=INK, strokeWidth=3)

# --- name ------------------------------------------------------------------------------
d.text("TAWNY FROGMOUTH", "Name", x=500, y=960, size=44, font="Virelai Sans",
       color="#D4DCD0", justify="center")

d.finish("frogmouth-V1R00")
