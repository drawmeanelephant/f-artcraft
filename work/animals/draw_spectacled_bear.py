#!/usr/bin/env python3
"""Spectacled bear — field plate V1R00. Three-quarter bust in Andean cloud
forest, one forepaw resting on a mossy branch, a small bromeliad beside it.
Cream facial markings asymmetric (one reference, not cartoon spectacles).
Dark coat lifted with warm translucent highlights. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Spectacled Bear — Field Plate", 1000, 1000)

INK = "#221610"
CX, CY, R = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#131B10"), (1, "#060904"))
PLATE_GRAD = rad((0, "#ACB691"), (0.62, "#75835D"), (1, "#41492E"))
COAT_GRAD  = rad((0, "#523B25"), (0.55, "#302011"), (1, "#160D07"))
FAR_GRAD   = rad((0, "#3A2812"), (1, "#150D06"))
MUZZLE     = lin(400, 430, 430, 560, (0, "#6E5032"), (1, "#3A2714"))
BRANCH_GRAD = lin(0, 676, 0, 740, (0, "#5E4A30"), (1, "#30200F"))
FLOOR_GRAD = lin(0, 770, 0, 880, (0, "#4A5230"), (1, "#232A14"))
CREAM = "#E9D8AE"

def on_disc(x, y, pad=10):
    return math.hypot(x - CX, y - CY) <= R - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#27301A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE4C2", strokeWidth=3, opacity=26)
for i, (x, y, w, o) in enumerate([(210, 240, 9, 34), (760, 210, 7, 32), (165, 470, 8, 30),
                                  (820, 590, 9, 34), (310, 170, 7, 30), (640, 150, 8, 32),
                                  (230, 660, 7, 30), (770, 700, 8, 28), (430, 130, 6, 28),
                                  (150, 590, 6, 28), (850, 400, 7, 30), (580, 800, 7, 28)]):
    assert on_disc(x + w / 2, y + w / 2), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E5A36", opacity=o, stroke=NONE)
# cloud-forest mist, behind the bear
for i, (x, y, w, h, o) in enumerate([(150, 250, 700, 60, 12), (220, 330, 560, 44, 10),
                                     (380, 180, 400, 50, 10), (140, 560, 380, 46, 9)]):
    d.shape("ellipse", f"Mist {i+1}", x=x, y=y, width=w, height=h,
            fill="#DFE8D2", opacity=o, stroke=NONE)

# --- forest floor: dark chord closing on the disc arc --------------------------
fy = 792
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C340,782 460,788 560,786 C660,784 720,788 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Forest floor", fill=FLOOR_GRAD, stroke=NONE)

# --- far ear (left, slightly smaller in 3/4) -----------------------------------
d.shape("ellipse", "Ear far", x=330, y=262, width=64, height=60, fill=FAR_GRAD,
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Ear far inner", x=346, y=278, width=30, height=28,
        fill="#0C0704", opacity=60, stroke=NONE)

# --- bust: shoulders mass -------------------------------------------------------
d.path("M248,780 C238,690 272,596 336,548 C362,530 396,518 434,512 "
       "C474,506 534,510 574,522 C640,540 700,582 726,650 "
       "C742,692 748,736 744,780 Z",
       "Shoulders", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# chest bib shadow + a hint of the pale chest mark low on the bust
d.path("M400,600 C440,640 520,660 580,650 C560,700 470,720 410,690 C390,660 388,625 400,600 Z",
       "Chest shade", fill="#140C06", opacity=35, stroke=NONE)
d.path("M430,640 C460,668 520,678 556,666 C544,700 480,714 442,692 C426,672 424,652 430,640 Z",
       "Chest bib", fill=CREAM, opacity=22, stroke=NONE)

# --- head ----------------------------------------------------------------------
# near ear (right, larger)
d.shape("ellipse", "Ear near", x=556, y=256, width=76, height=70, fill=COAT_GRAD,
        stroke=INK, strokeWidth=6)
d.shape("ellipse", "Ear near inner", x=582, y=282, width=24, height=20,
        fill="#0C0704", opacity=45, stroke=NONE)
d.path("M572,270 C584,260 604,260 618,272", "Ear near rim", fill=NONE,
       stroke="#8A6A44", strokeWidth=4, opacity=50, cap="round")

d.path("M478,268 C560,268 626,326 630,404 C634,462 600,514 534,542 "
       "C492,558 438,558 398,540 C342,516 314,462 322,394 "
       "C330,320 392,268 478,268 Z",
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
# crown + cheek fur texture
for i, dd in enumerate(["M390,292 C420,278 460,272 496,274", "M540,282 C574,296 600,320 616,350",
                        "M330,420 C334,448 346,472 364,492", "M600,470 C588,494 570,514 546,528",
                        "M414,540 L410,556", "M470,548 L469,564", "M524,540 L525,556"]):
    d.path(dd, f"Head fur {i+1}", fill=NONE, stroke="#6E5238", strokeWidth=4,
           opacity=35, cap="round")

# --- facial markings: one bear's pattern, asymmetric ----------------------------
# near (right) eye: full-ish cream crescent sweeping down the cheek
d.path("M528,352 C566,344 594,366 592,402 C590,436 566,458 534,456 "
       "C556,444 570,422 568,396 C566,372 550,356 528,352 Z",
       "Spectacle near", fill=CREAM, opacity=78, stroke=NONE)
# far (left) eye: thinner partial arc only, higher
d.path("M386,358 C410,350 434,360 440,382 C428,370 410,366 394,372 "
       "C384,368 382,362 386,358 Z",
       "Spectacle far", fill=CREAM, opacity=70, stroke=NONE)
# bridge: faint cream trace between the eyes, not a joined ring
d.path("M444,376 C470,368 500,364 524,366", "Bridge trace", fill=NONE,
       stroke=CREAM, strokeWidth=7, opacity=35, cap="round")
# pale muzzle patch + chin (asymmetric, heavier on the near side)
d.path("M410,452 C446,440 498,442 528,458 C552,470 560,494 548,514 "
       "C532,538 488,550 448,544 C410,538 388,514 392,486 "
       "C395,470 401,459 410,452 Z",
       "Muzzle patch", fill=CREAM, opacity=30, stroke=NONE)
d.path("M418,530 C450,548 506,550 534,532 C528,556 496,570 458,566 "
       "C432,562 418,548 418,530 Z",
       "Chin cream", fill=CREAM, opacity=45, stroke=NONE)

# --- muzzle ----------------------------------------------------------------------
d.path("M398,470 C428,452 482,452 516,470 C540,482 548,506 538,526 "
       "C524,548 486,560 450,554 C416,548 392,528 392,502 "
       "C392,488 394,477 398,470 Z",
       "Muzzle", fill=MUZZLE, stroke=NONE)
# nose: wide bear nose, tilted slightly to the 3/4
d.path("M424,462 C446,452 480,452 500,462 C514,470 516,486 506,496 "
       "C492,506 462,508 444,500 C428,492 418,476 424,462 Z",
       "Nose", fill=lin(430, 450, 470, 505, (0, "#33200F"), (1, "#0B0603")), stroke=NONE)
d.shape("ellipse", "Nose glint", x=446, y=464, width=22, height=8, fill="#CBB894",
        opacity=40, stroke=NONE)
for i, (x, y) in enumerate([(442, 482), (492, 484)]):
    d.shape("ellipse", f"Nostril {i+1}", x=x, y=y, width=12, height=8,
            fill="#060302", opacity=80, stroke=NONE)
# philtrum + mouth
d.path("M468,504 L466,522 M466,522 C452,534 432,536 418,528 M466,522 C480,536 502,538 516,530",
       "Mouth", fill=NONE, stroke="#160D06", strokeWidth=5, opacity=70, cap="round")

# --- eyes -------------------------------------------------------------------------
d.shape("ellipse", "Eye near", x=534, y=390, width=26, height=24, fill="#140B05",
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye far", x=398, y=392, width=20, height=18, fill="#140B05",
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye near glint", x=540, y=395, width=6, height=6, fill="#E9F2DC",
        opacity=90, stroke=NONE)
d.shape("ellipse", "Eye far glint", x=403, y=396, width=4, height=4, fill="#E9F2DC",
        opacity=80, stroke=NONE)
d.path("M522,378 C534,370 552,370 564,378", "Brow near", fill=NONE, stroke=INK,
       strokeWidth=5, opacity=60, cap="round")
d.path("M390,382 C400,376 414,376 424,382", "Brow far", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=50, cap="round")

# --- mossy branch across the lower disc --------------------------------------------
by = 694
bdx = math.sqrt(R * R - (by - CY) ** 2) * 0.86   # ends stay inside the rim
d.path(f"M{CX-bdx:.1f},{by} C300,{by-14} 480,{by-6} 620,{by-2} "
       f"C700,{by} 780,{by+6} {CX+bdx:.1f},{by+10} "
       f"L{CX+bdx:.1f},{by+38} C700,{by+34} 520,{by+28} 380,{by+32} "
       f"C290,{by+34} 210,{by+36} {CX-bdx:.1f},{by+40} Z",
       "Branch", fill=BRANCH_GRAD, stroke=INK, strokeWidth=5)
d.path(f"M{CX-bdx+6:.0f},{by+2} C320,{by-10} 500,{by-4} 640,{by} "
       f"C720,{by+2} 780,{by+6} {CX+bdx-8:.0f},{by+10}",
       "Branch top light", fill=NONE, stroke="#8A6E46", strokeWidth=5,
       opacity=55, cap="round")
# moss cushions on the branch top
for i, (x, w) in enumerate([(220, 60), (320, 84), (430, 56), (540, 92), (680, 70), (770, 54)]):
    d.shape("ellipse", f"Moss {i+1}", x=x, y=by - 18 - (i % 2) * 4, width=w, height=20,
            fill="#788A48", opacity=80, stroke=NONE)
    d.shape("ellipse", f"Moss light {i+1}", x=x + 8, y=by - 16 - (i % 2) * 4,
            width=w * 0.45, height=8, fill="#A6B868", opacity=50, stroke=NONE)
# a stub branch on the left
d.path("M268,700 C258,672 252,648 254,626 C262,646 272,668 284,692 Z",
       "Branch stub", fill=BRANCH_GRAD, stroke=INK, strokeWidth=4)

# --- forepaw resting over the branch -------------------------------------------------
# near foreleg drops from the right shoulder onto the log
d.path("M596,560 C636,566 664,600 672,648 C678,680 676,702 668,714 "
       "C646,724 612,722 596,708 C584,684 580,636 584,600 "
       "C586,580 590,568 596,560 Z",
       "Near foreleg", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# paw rolls over the log's front edge
d.path("M586,696 C606,684 646,682 668,694 C682,702 684,718 674,728 "
       "C656,742 616,742 598,730 C584,720 580,706 586,696 Z",
       "Paw", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# toe separations + short claws gripping over the front edge
for i, x in enumerate([604, 626, 648]):
    d.path(f"M{x},700 C{x-2},712 {x-2},722 {x+2},732", f"Toe {i+1}",
           fill=NONE, stroke=INK, strokeWidth=4, opacity=70, cap="round")
for i, x in enumerate([610, 632, 654]):
    d.path(f"M{x},722 C{x+1},730 {x+4},736 {x+8},738", f"Paw claw {i+1}",
           fill=NONE, stroke="#0E0804", strokeWidth=6, cap="round")

# --- bromeliad on the branch, right side ----------------------------------------------
bx, byy = 762, 672
def strap_leaf(ang, length, width, label, hi):
    """Broad strap leaf fanning from the rosette base at angle deg (0 = up)."""
    a = math.radians(ang)
    dx, dy = math.sin(a), -math.cos(a)
    nx, ny = -dy, dx
    tip = (bx + dx * length, byy + dy * length)
    m1 = (bx + dx * length * 0.55 + nx * width, byy + dy * length * 0.55 + ny * width)
    m2 = (bx + dx * length * 0.55 - nx * width, byy + dy * length * 0.55 - ny * width)
    d.path(f"M{bx},{byy} Q{m1[0]:.1f},{m1[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{m2[0]:.1f},{m2[1]:.1f} {bx},{byy} Z", label,
           fill=lin(bx, byy - length, bx, byy, (0, hi), (1, "#41502A")),
           stroke=INK, strokeWidth=3)
strap_leaf(-58, 58, 12, "Bromeliad leaf 1", "#7E9050")
strap_leaf(-28, 66, 13, "Bromeliad leaf 2", "#8CA05C")
strap_leaf(4, 62, 13, "Bromeliad leaf 3", "#7E9050")
strap_leaf(34, 60, 12, "Bromeliad leaf 4", "#8CA05C")
strap_leaf(62, 48, 11, "Bromeliad leaf 5", "#708448")
# red cup heart
d.path(f"M{bx-14},{byy-24} C{bx-8},{byy-46} {bx+14},{byy-46} {bx+20},{byy-24} "
       f"C{bx+13},{byy-10} {bx-7},{byy-10} {bx-14},{byy-24} Z",
       "Bromeliad heart", fill=rad((0, "#C45436"), (1, "#7E2C1C")), stroke=NONE)

# front veil of mist over the lower bust
d.shape("ellipse", "Front mist", x=180, y=600, width=520, height=54,
        fill="#DFE8D2", opacity=8, stroke=NONE)

# plate rim on top
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#1A2410", strokeWidth=6)

# --- name + second line --------------------------------------------------------
d.text("SPECTACLED BEAR", "Name", x=500, y=932, size=58, font="Virelai Sans",
       color="#E6EAC8", justify="center")
LINE2, SZ2, TRK = "TREMARCTOS ORNATUS", 22, 240
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#A8B384", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("spectacled-bear-V1R00")
