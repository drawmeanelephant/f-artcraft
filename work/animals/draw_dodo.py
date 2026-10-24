#!/usr/bin/env python3
"""Dodo — field-guide plate V1R00. Plump profile facing left on a lost-island
shore: the great hooked beak with its pale sheath and dark tip, a hunched
round body, a useless little folded wing, the pompom of curled tail plumes,
and stout legs planted in the sand. Lagoon horizon, trade-wind streaks,
foam line on the beach. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dodo — Field Plate", 1000, 1000)
rng = random.Random(11)

INK = "#2A2118"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0A2422"), (1, "#04100E"))
PLATE_GRAD = rad((0, "#EDF2DA"), (0.65, "#B7D2C0"), (1, "#6E9584"))
PLUME_GRAD = rad((0, "#9A8A72"), (0.6, "#66584A"), (1, "#3A322A"))
BEAK_GRAD = lin(320, 380, 430, 480, (0, "#E4D49C"), (0.55, "#C4AC70"), (1, "#8F7A48"))
SAND_GRAD = lin(0, 730, 0, 880, (0, "#F4E6BE"), (1, "#C4A374"))
SEA_GRAD = lin(0, 620, 0, 730, (0, "#7FB5A4"), (1, "#55877A"))
LEG = "#C89B58"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + lost-island plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#B7D2C0", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7364", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F8EC", strokeWidth=3, opacity=50)

# trade-wind streaks high in the plate
for i, dd in enumerate(["M200,210 C360,190 540,192 700,214",
                        "M260,280 C400,264 560,266 710,286",
                        "M180,345 C320,330 470,330 620,348"]):
    d.path(dd, f"Wind streak {i+1}", fill=NONE, stroke="#F0F6E4",
           strokeWidth=5, opacity=20, cap="round")
# small drifting clouds
for i, (x, y, w) in enumerate([(240,150,90),(620,120,110),(430,105,70),(740,300,80),(150,420,60)]):
    d.shape("ellipse", f"Cloud {i+1}", x=x, y=y, width=w, height=w*0.28,
            fill="#F6F9EC", opacity=26, stroke=NONE)

# --- lagoon band behind the beach -----------------------------------------------------
d.path("M196,676 C380,648 620,648 804,676 C620,704 380,704 196,676 Z",
       "Lagoon", fill=SEA_GRAD, opacity=80, stroke=NONE)
assert on_disc(196, 676, 4) and on_disc(804, 676, 4)
# distant swell lines
for i, dd in enumerate(["M220,668 C360,656 640,656 780,668",
                        "M260,690 C400,680 600,680 740,690"]):
    d.path(dd, f"Swell {i+1}", fill=NONE, stroke="#DFF0E4",
           strokeWidth=3, opacity=45, cap="round")

# --- beach floor, closing on the disc's own arc -----------------------------------------
d.path("M206,706 C390,690 610,690 794,706 A420,420 0 0 1 206,706 Z",
       "Beach", fill=SAND_GRAD, stroke="#A5854F", strokeWidth=4)
assert on_disc(206, 706, 4) and on_disc(794, 706, 4)
# foam line where the lagoon meets the sand
d.path("M240,700 C400,688 600,688 760,700", "Foam", fill=NONE,
       stroke="#FBFDF4", strokeWidth=6, opacity=65, cap="round")
# sand flecks + a half-buried shell
for i, (x, y, w) in enumerate([(290,740,8),(680,736,9),(420,760,7),(590,758,8),(350,792,7),(640,790,8),(480,820,6)]):
    d.shape("ellipse", f"Sand fleck {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#A5854F", opacity=40, stroke=NONE)
d.path("M305,772 C310,762 322,760 328,768 C330,776 324,782 314,782 "
       "C306,780 302,777 305,772 Z", "Shell", fill="#F6ECD2",
       stroke="#B08E58", strokeWidth=2.5)
d.path("M310,772 C314,768 320,768 324,772", "Shell rib", fill=NONE,
       stroke="#B08E58", strokeWidth=2, opacity=70, cap="round")

# === the dodo ============================================================================
# --- tail plumes: the famous curl, behind the body -----------------------------------------
for i, (p0, p1, p2, p3, w, col) in enumerate([
        ((644, 468), (712, 416), (732, 350), (692, 330), 24, "#5A4E3E"),
        ((636, 476), (714, 442), (752, 392), (726, 362), 19, "#6E5F4C"),
        ((626, 484), (682, 476), (726, 452), (724, 420), 14, "#8A7A62")]):
    s = (f"M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}")
    d.path(s, f"Tail plume {i+1}", fill=NONE, stroke=col,
           strokeWidth=w, opacity=92, cap="round")
    # spiral tip flick
    d.path(f"M{p3[0]},{p3[1]} q-14,-4 -16,-18", f"Plume flick {i+1}",
           fill=NONE, stroke=col, strokeWidth=w*0.45, cap="round")

# --- far leg -----------------------------------------------------------------------------
d.path("M548,652 L544,722 C543,732 550,738 558,736 L568,732 L566,654 Z",
       "Far leg", fill="#A07C44", stroke=INK, strokeWidth=3)
d.path("M540,728 C528,732 518,736 512,742 M540,728 L540,744 "
       "M540,728 C552,732 562,736 568,742",
       "Far toes", fill=NONE, stroke="#8A6C3C", strokeWidth=5, cap="round")

# --- body: the great plump teardrop ---------------------------------------------------------
d.path("M412,392 "
       "C374,404 346,438 334,480 "        # chest front falling to the breast
       "C322,522 326,572 348,614 "        # breast rounding under
       "C370,656 420,682 480,690 "        # belly bottom
       "C540,698 606,692 646,668 "        # under the rear
       "C678,648 692,608 688,564 "        # rear rising
       "C684,522 668,478 636,448 "        # back sweeping up
       "C606,420 566,402 522,396 "        # shoulders into the neck
       "C486,390 446,386 412,392 Z",      # nape back to the throat
       "Body", fill=PLUME_GRAD, stroke=INK, strokeWidth=6)
# belly light + back shade
d.shape("ellipse", "Belly light", x=380, y=560, width=220, height=120,
        fill="#B8A88E", opacity=25, stroke=NONE)
d.path("M440,410 C520,396 610,420 660,470", "Back shade", fill=NONE,
       stroke="#241C12", strokeWidth=14, opacity=22, cap="round")
# breast feather scallops
for i in range(8):
    x = 360 + i * 34
    y = 585 + (i % 2) * 14
    d.path(f"M{x},{y} q14,16 30,10", f"Breast scallop {i+1}", fill=NONE,
           stroke="#4A3E30", strokeWidth=3, opacity=35, cap="round")
# flank flecks
for i, (x, y, w) in enumerate([(430,480,16),(500,500,14),(570,480,15),(610,540,12),(460,540,12)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#3A3226", opacity=25, stroke=NONE)

# --- folded wing: the useless little flag ----------------------------------------------------
d.path("M500,470 C540,462 580,472 602,498 C616,520 616,548 602,568 "
       "C580,584 544,586 518,572 C494,558 484,530 490,504 "
       "C492,490 495,478 500,470 Z",
       "Wing", fill="#4E4234", stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M512,500 C540,492 572,498 592,518",
                        "M508,530 C536,522 566,528 586,546",
                        "M512,558 C534,552 558,556 574,568"]):
    d.path(dd, f"Wing feather {i+1}", fill=NONE, stroke="#7A6A50",
           strokeWidth=4, opacity=60, cap="round")

# --- near leg + foot on the sand ---------------------------------------------------------
d.path("M470,656 L462,724 C461,734 468,740 478,738 L488,734 L490,658 Z",
       "Near leg", fill=LEG, stroke=INK, strokeWidth=3)
# scaly leg banding
for i, y in enumerate([676, 692, 708]):
    d.path(f"M466,{y} L484,{y}", f"Leg band {i+1}", fill=NONE,
           stroke="#8A6C3C", strokeWidth=2.5, opacity=60, cap="round")
d.path("M462,730 C450,734 438,738 430,744 M462,730 L460,748 "
       "M462,730 C474,734 486,738 494,744",
       "Near toes", fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# --- head + the great beak --------------------------------------------------------------
# head: small dome sunk into the shoulders
d.path("M360,372 C360,344 380,324 408,322 C436,320 458,338 462,364 "
       "C465,384 456,402 438,410 C416,418 390,412 374,396 "
       "C364,388 360,380 360,372 Z",
       "Head", fill=PLUME_GRAD, stroke=INK, strokeWidth=5)
# bald face patch
d.shape("ellipse", "Face patch", x=352, y=348, width=56, height=50,
        fill="#A8967A", opacity=60, stroke=NONE)

# beak: huge sheath, hooked tip
d.path("M382,364 C352,364 322,376 300,398 C282,416 272,440 270,462 "
       "C269,474 276,482 287,480 C298,476 308,466 318,456 "
       "C342,434 372,418 398,408 C410,398 412,382 404,372 "
       "C398,366 390,364 382,364 Z",
       "Beak", fill=BEAK_GRAD, stroke=INK, strokeWidth=5)
# dark hooked tip
d.path("M270,462 C272,450 278,440 288,432 C294,444 296,458 292,470 "
       "C288,478 278,480 272,476 C269,472 269,468 270,462 Z",
       "Beak tip", fill="#5E4A26", stroke=INK, strokeWidth=3)
# sheath ridge + nostril slit + gape line
d.path("M310,404 C336,386 366,374 394,370", "Beak ridge", fill=NONE,
       stroke="#F4E8BC", strokeWidth=4, opacity=60, cap="round")
d.path("M342,388 C356,380 372,376 386,376", "Nostril", fill=NONE,
       stroke="#4A3A1E", strokeWidth=4, opacity=70, cap="round")
d.path("M298,434 C326,416 360,402 394,394", "Gape", fill=NONE,
       stroke="#5E4A26", strokeWidth=3, opacity=60, cap="round")

# eye: mild, unhurried
d.shape("ellipse", "Eye", x=396, y=352, width=18, height=17,
        fill="#161008", stroke=NONE)
d.shape("ellipse", "Eye glint", x=400, y=355, width=5, height=5,
        fill="#FFF8E0", opacity=85, stroke=NONE)
# head feather tufts
for i, dd in enumerate(["M400,326 C394,340 392,352 394,362",
                        "M420,328 C416,340 414,352 416,362",
                        "M438,336 C434,346 432,356 434,364"]):
    d.path(dd, f"Head tuft {i+1}", fill=NONE, stroke="#4A4034",
           strokeWidth=4, opacity=55, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#1E3630", strokeWidth=6)

# --- name ----------------------------------------------------------------------------------
d.text("DODO", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EDF5E6", justify="center")

d.finish("dodo-V1R00")
