#!/usr/bin/env python3
"""Great auk — field-guide plate V1R00. Upright on a bare skerry, facing left
over the last egg: black above, cream below, white oval between eye and the
big grooved bill. North-Atlantic grey: mist bands, a dim sun, a distant
skerry on the sea line, rock floor closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Great Auk — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#10141C"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [dict({"offset": o, "color": c},
                           **({"opacity": p[0]} if p and p[0] is not None else {}))
                      for o, c, *p in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#131C28"), (1, "#05080E"))
PLATE_GRAD = rad((0, "#A8BCCB", None), (0.55, "#6B8093", None), (1, "#33445A", None))
BACK_GRAD = lin(0, 300, 0, 760, (0, "#3A4150"), (0.55, "#232833"), (1, "#12151D"))
BELLY_GRAD = lin(0, 380, 0, 760, (0, "#F2EBD8"), (0.6, "#DCD3B8"), (1, "#B4A88C"))
ROCK_GRAD = lin(0, 700, 0, 880, (0, "#6B7484"), (1, "#3A4250"))
EGG_GRAD = rad((0, "#F4E8C8", None), (0.7, "#DCC99C", None), (1, "#B09A6C", None))

# --- backdrop + North-Atlantic grey plate -------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#6B8093", opacity=4, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C2836", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EBF2", strokeWidth=3, opacity=40)

# dim sun through the murk, upper right
d.shape("ellipse", "Sun", x=640, y=150, width=110, height=110,
        fill=rad((0, "#F0ECD8", 80), (0.6, "#D8D0B4", 35), (1, "#D8D0B4", 0)),
        stroke=NONE)
# mist bands sliding across the sea line
for i, (y, op, w_) in enumerate([(560, 22, 10), (600, 16, 7), (635, 14, 5)]):
    d.path(f"M170,{y} C300,{y-14} 460,{y+10} 620,{y-4} C720,{y-12} 790,{y-6} 840,{y+2}",
           f"Mist {i+1}", fill=NONE, stroke="#E4EBF2", strokeWidth=w_, opacity=op, cap="round")
# the sea line itself
d.path("M150,652 C300,646 500,650 660,646 C750,644 820,648 850,650",
       "Sea line", fill=NONE, stroke="#C8D4E0", strokeWidth=4, opacity=30, cap="round")
# distant skerry on the line, left
d.path("M196,652 C200,630 214,616 236,612 C258,610 276,622 282,642 C284,648 284,652 284,652 Z",
       "Far skerry", fill="#2E3A4A", opacity=75, stroke=NONE)
d.path("M220,614 C232,610 246,610 256,616", "Skerry snow",
       fill=NONE, stroke="#E4EBF2", strokeWidth=4, opacity=40, cap="round")
# seabird flecks — razorbills off the rock
for i, (x, y) in enumerate([(300, 400), (346, 372), (720, 420), (680, 380)]):
    assert on_disc(x, y, 16), (x, y)
    d.path(f"M{x-9},{y} Q{x-3},{y-6} {x},{y} Q{x+3},{y-6} {x+9},{y}",
           f"Bird fleck {i+1}", fill=NONE, stroke="#1C2836", strokeWidth=3, opacity=60, cap="round")

# --- rock floor: slab top, bottom closes on the disc arc ------------------------
ly = 742
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C360,724 470,736 570,730 C660,725 730,734 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Skerry slab", fill=ROCK_GRAD, stroke=NONE)
# rock facets
d.path("M300,742 L380,742 L360,800 L270,790 Z", "Facet 1", fill="#4A5462", opacity=60, stroke=NONE)
d.path("M560,742 L680,742 L700,810 L580,800 Z", "Facet 2", fill="#4A5462", opacity=50, stroke=NONE)
d.path(f"M{CX-ldx+10:.1f},{ly-3} C360,722 470,732 570,726 C660,721 720,730 {CX+ldx-12:.1f},{ly-3}",
       "Slab light", fill=NONE, stroke="#E4EBF2", strokeWidth=4, opacity=35, cap="round")

# --- great auk: upright, facing left ---------------------------------------------
# the big grooved bill, deep and laterally compressed — drawn under the head
d.path("M466,322 C436,330 412,346 398,368 C392,378 390,388 394,396 "
       "C414,404 444,404 470,396 C488,388 496,368 494,346 C492,332 482,322 466,322 Z",
       "Bill", fill=BACK_GRAD, stroke=INK, strokeWidth=5)
# bill grooves, pale arcs up the bill face
for i, (x0, y0, x1, y1) in enumerate([(416, 358, 424, 388), (436, 346, 444, 390), (456, 338, 462, 390)]):
    d.path(f"M{x0},{y0} C{x0+4},{y0+10} {x1-4},{y1-10} {x1},{y1}",
           f"Bill groove {i+1}", fill=NONE, stroke="#C8CFD8", strokeWidth=3, opacity=55, cap="round")
# gape line
d.path("M402,386 C424,392 452,392 474,384", "Gape",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round")

# one silhouette: crown → nape → back → tail stub → legs → belly front → throat → chin
BODY = ("M478,296 C512,294 540,314 554,346 C566,372 570,404 570,436 "
        "C576,470 590,520 606,566 C620,608 632,660 636,706 "
        "L648,716 L640,724 C630,738 606,744 578,744 "
        "C540,744 506,736 486,714 C466,692 456,650 452,600 "
        "C448,540 446,480 448,430 C450,394 456,356 466,332 "
        "C470,318 472,306 478,296 Z")
d.path(BODY, "Auk", fill=BACK_GRAD, stroke=INK, strokeWidth=6)
# tail stub, cocked up behind
d.path("M610,700 C630,706 646,716 656,730 C644,730 630,726 618,718 Z",
       "Tail stub", fill=BACK_GRAD, stroke=INK, strokeWidth=5)

# cream front: throat → breast → belly, the auk's counter-shade
d.path("M462,388 C470,430 474,480 476,530 C478,596 486,660 510,706 "
       "C528,724 556,732 584,730 C560,720 540,700 528,668 "
       "C508,616 500,540 500,470 C500,430 496,402 486,384 "
       "C478,380 468,382 462,388 Z",
       "Belly", fill=BELLY_GRAD, opacity=95, stroke=NONE)
# the white oval patch between eye and bill — the great auk's badge
d.path("M452,348 C462,338 478,336 490,344 C498,352 498,366 490,374 "
       "C478,382 462,380 454,370 C448,362 448,354 452,348 Z",
       "Face patch", fill=BELLY_GRAD, opacity=90, stroke=NONE)
# eye, small and dark, set in the patch's upper edge
d.shape("ellipse", "Eye", x=474, y=346, width=14, height=14, fill="#0C0F14", stroke=NONE)
d.shape("ellipse", "Eye glint", x=477, y=349, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
# crown gloss
d.path("M478,300 C506,298 530,312 544,336", "Crown light",
       fill=NONE, stroke="#8A94A4", strokeWidth=5, opacity=45, cap="round")
# the tiny useless wing: a flipper laid on the flank
d.path("M540,470 C566,478 584,502 590,536 C594,566 590,600 578,626 "
       "C566,614 556,584 552,548 C548,518 542,492 540,470 Z",
       "Flipper", fill="#1A1E28", opacity=85, stroke=INK, strokeWidth=4)
d.path("M552,500 C564,530 568,566 564,596", "Flipper fold",
       fill=NONE, stroke="#3A4150", strokeWidth=3, opacity=60, cap="round")

# legs + splayed feet on the slab
d.path("M540,730 C536,714 540,702 552,698 C560,706 562,720 558,734 Z",
       "Leg L", fill="#1A1E28", stroke=INK, strokeWidth=4)
d.path("M520,736 C540,730 566,730 584,736 C574,744 548,748 524,746 "
       "C518,744 516,740 520,736 Z",
       "Foot", fill="#1A1E28", stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M530,738 L544,732", "M546,742 L560,734", "M562,742 L574,736"]):
    d.path(dd, f"Web {i+1}", fill=NONE, stroke="#0C0F14", strokeWidth=2, opacity=70, cap="round")
# contact shadow
d.shape("ellipse", "Auk shadow", x=500, y=738, width=140, height=14, fill="#1C2836", opacity=40, stroke=NONE)

# the last egg, pale on the rock in front of its feet
d.shape("ellipse", "Egg shadow", x=398, y=726, width=66, height=14, fill="#1C2836", opacity=40, stroke=NONE)
d.path("M430,640 C452,640 466,668 466,692 C466,716 450,734 430,734 "
       "C410,734 394,716 394,692 C394,668 408,640 430,640 Z",
       "Egg", fill=EGG_GRAD, stroke="#6E5F40", strokeWidth=4)
for i, (x, y, w) in enumerate([(418, 672, 6), (442, 692, 7), (426, 708, 5), (444, 664, 4)]):
    d.shape("ellipse", f"Egg fleck {i+1}", x=x, y=y, width=w, height=w, fill="#8A7448", opacity=55, stroke=NONE)
d.shape("ellipse", "Egg light", x=410, y=652, width=26, height=18, fill="#FFFFFF", opacity=25, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1018", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("GREAT AUK", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E4EAF0", justify="center")

d.finish("great-auk-V1R00")
