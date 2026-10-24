#!/usr/bin/env python3
"""Chupacabra — field-guide plate V1R00. The goatsucker at the edge of the
yard light: gaunt hairless quadruped, dorsal spikes, huge lamp-red eye,
head low and all appetite. Scrubland floor with a leaning fence post,
a mercury lamp burning on its pole, dust-floor closing on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Chupacabra — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#16111C"

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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#171020"), (1, "#070509"))
PLATE_GRAD = rad((0, "#B89464", None), (0.55, "#6E5638", None), (1, "#2E2316", None))
HIDE_GRAD = lin(0, 400, 0, 750, (0, "#9A92A2"), (0.55, "#6A6274"), (1, "#3C3542"))
HIDE_DARK = lin(0, 450, 0, 750, (0, "#5E5668"), (1, "#2C2630"))
DUST_GRAD = lin(0, 715, 0, 880, (0, "#6E5A36"), (1, "#2A2010"))

# --- backdrop + sodium-dusk plate ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#241A0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDDDBA", strokeWidth=3, opacity=40)

# the farm light: a mercury lamp on a leaning pole, upper right
d.path("M742,300 L748,300 L762,742 L754,742 Z", "Lamp pole",
       fill="#241C14", opacity=85, stroke=NONE)
d.path("M724,286 L768,286 L762,304 L730,304 Z", "Lamp head",
       fill="#3A2E1C", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Lamp glow", x=626, y=190, width=240, height=240,
        fill=rad((0, "#F6D98E", 85), (0.55, "#E8B860", 30), (1, "#E8B860", 0)),
        stroke=NONE)
d.shape("ellipse", "Lamp bulb", x=738, y=296, width=16, height=10, fill="#FBE8B8", opacity=95, stroke=NONE)
# the pool of light it throws on the dust
d.shape("ellipse", "Light pool", x=600, y=708, width=230, height=40,
        fill="#F2C96E", opacity=14, stroke=NONE)
# night haze bands
for i, (y, op, w_) in enumerate([(300, 14, 8), (370, 10, 6)]):
    d.path(f"M180,{y} C330,{y-12} 480,{y+10} 640,{y-4} C740,{y-10} 810,{y-4} 840,{y+2}",
           f"Haze {i+1}", fill=NONE, stroke="#EDDDBA", strokeWidth=w_, opacity=op, cap="round")

# --- dust floor: slight rise left, bottom closes on the disc arc ------------------
ly = 730
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C350,714 470,724 580,718 C680,712 760,722 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Dust floor", fill=DUST_GRAD, stroke=NONE)
d.path(f"M{CX-ldx+8:.1f},{ly-4} C350,712 470,720 580,714 C680,708 750,718 {CX+ldx-10:.1f},{ly-4}",
       "Dust light", fill=NONE, stroke="#EDDDBA", strokeWidth=4, opacity=30, cap="round")

# leaning fence post + two sagging wires, left
d.path("M238,742 L252,742 L246,626 L234,628 Z", "Fence post",
       fill="#2E2418", stroke=INK, strokeWidth=3)
d.path("M244,648 C330,672 420,676 500,668", "Wire 1",
       fill=NONE, stroke="#1E1810", strokeWidth=2.5, opacity=80, cap="round")
d.path("M244,684 C330,706 430,710 520,702", "Wire 2",
       fill=NONE, stroke="#1E1810", strokeWidth=2.5, opacity=70, cap="round")
# dry scrub tufts
for i, (x, y, h) in enumerate([(300, 736, 30), (452, 740, 24), (700, 736, 28), (640, 742, 20), (200, 742, 22)]):
    assert on_disc(x, y - h, 14), (x, y - h)
    for j, dx in enumerate([-8, -3, 3, 8]):
        d.path(f"M{x},{y} C{x+dx},{y-h*0.6} {x+dx*1.4},{y-h*0.9} {x+dx*1.6},{y-h}",
               f"Tuft {i+1}.{j+1}", fill=NONE, stroke="#3A2E18", strokeWidth=2.5, opacity=75, cap="round")

# --- the goatsucker: gaunt quadruped, head low, facing left -------------------------
# tail first: thin rat-tail hanging off the rump, clear of the hind leg
d.path("M618,534 C654,552 678,592 682,634 C684,662 678,686 666,700 "
       "C670,676 668,650 660,624 C650,590 632,562 608,548 Z",
       "Tail", fill=HIDE_DARK, stroke=INK, strokeWidth=4)
# far front leg (darker, behind)
d.path("M428,560 C434,610 440,660 444,706 L436,730 L448,732 L456,706 "
       "C458,656 456,606 452,560 Z", "Leg FL far", fill=HIDE_DARK, stroke=INK, strokeWidth=4)
# torso: deep chest, tucked waist, long back
d.path("M398,540 C404,498 444,474 504,472 C560,470 612,488 624,524 "
       "C632,556 616,590 572,602 C524,616 456,614 418,596 "
       "C398,580 392,560 398,540 Z",
       "Torso", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
# rib lines on the gaunt flank
for i, dd in enumerate(["M470,505 C466,530 466,556 472,580",
                        "M500,502 C496,530 496,558 502,584",
                        "M530,504 C527,530 527,556 532,580"]):
    d.path(dd, f"Rib {i+1}", fill=NONE, stroke="#4E4656", strokeWidth=4, opacity=55, cap="round")
# near legs
d.path("M402,570 C398,620 394,672 392,712 L382,736 L398,738 L406,712 "
       "C410,660 414,610 420,568 Z", "Leg FL near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M560,552 C588,570 606,610 606,652 C606,682 596,706 582,724 "
       "L568,738 L586,740 L602,724 C614,700 618,672 616,644 "
       "C618,606 604,572 578,550 Z",
       "Leg HL near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
# claws
for i, dd in enumerate(["M384,732 L396,724", "M394,734 L406,728",
                        "M588,736 L600,728", "M598,738 L608,732"]):
    d.path(dd, f"Claw {i+1}", fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")
# neck + head: long canine skull, muzzle dropped to the scent
d.path("M430,515 C412,500 388,494 366,500 C340,508 318,530 304,560 "
       "C296,578 292,594 296,604 C308,614 332,616 356,610 "
       "C386,602 414,582 428,558 C436,542 436,526 430,515 Z",
       "Head", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
# ears: bat ears swept back over the skull, not pricked up
d.path("M342,502 C340,474 350,450 370,434 C376,456 376,480 370,502 "
       "C360,506 350,506 342,502 Z",
       "Ear far", fill=HIDE_DARK, stroke=INK, strokeWidth=4)
d.path("M370,498 C370,464 382,436 406,418 C414,444 412,472 402,498 "
       "C392,504 378,504 370,498 Z",
       "Ear near", fill=HIDE_GRAD, stroke=INK, strokeWidth=4)
d.path("M384,478 C386,456 392,438 402,426", "Ear fold",
       fill=NONE, stroke="#4E4656", strokeWidth=3, opacity=70, cap="round")
# dorsal spikes: a sawtooth mane down the spine
d.path("M414,486 L430,458 L444,482 L464,452 L478,480 L498,450 L510,478 "
       "L532,454 L542,480 L564,458 L572,482 L594,466 L600,488 "
       "L604,498 L414,500 Z",
       "Spine ridge", fill="#241F2A", opacity=90, stroke=NONE)
# the lamp-red eye, huge for the skull, set low over the muzzle
d.shape("ellipse", "Eye", x=326, y=538, width=22, height=24,
        fill=rad((0, "#F6A03C", None), (0.55, "#C8441E", None), (1, "#6E1808", None)),
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=331, y=543, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
# nostril + lip line + overlong fangs
d.shape("ellipse", "Nostril", x=300, y=584, width=8, height=6, fill="#0C0A10", stroke=NONE)
d.path("M300,596 C316,606 340,608 362,602", "Lip",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M316,604 L322,622 L330,604 Z", "Fang near", fill="#EADFC8", stroke=INK, strokeWidth=2.5)
d.path("M338,606 L343,620 L350,605 Z", "Fang far", fill="#EADFC8", opacity=80, stroke=NONE)
# muzzle shading + shoulder gleam
d.path("M300,584 C312,570 330,562 348,562 C336,574 318,584 306,592 Z",
       "Muzzle shade", fill=HIDE_DARK, opacity=55, stroke=NONE)
d.path("M410,514 C440,494 480,484 522,484", "Back gleam",
       fill=NONE, stroke="#C9C2D2", strokeWidth=5, opacity=35, cap="round")
# contact shadow
d.shape("ellipse", "Shadow", x=380, y=730, width=240, height=16, fill="#241A0E", opacity=45, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C0806", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("CHUPACABRA", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#EAD9B8", justify="center")

d.finish("chupacabra-V1R00")
