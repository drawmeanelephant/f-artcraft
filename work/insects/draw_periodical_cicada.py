#!/usr/bin/env python3
"""Periodical cicada — field plate V1R00. Side view on a twig, the big red
compound eye prominent, translucent wings folded roof-like over the stout
black body with orange veins, a ghost of the shed nymph shell clinging below
the twig — seventeen years of silence, then this. Summer-green plate.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Periodical Cicada — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#140C08"
ORANGE = "#E8862A"

def lin(angle, *stops):
    return {"gradient": {"kind": "linear", "angle": angle, "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def linp(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1], "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": o, "color": c} for o, c in stops]}}

def disc_pt(deg, r=R):
    a = math.radians(deg)
    return (CX + r * math.cos(a), CY + r * math.sin(a))

# --- backdrop + summer-green plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#0E1608"), (1, "#040703")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#82A85C"), (0.6, "#4C6E34"), (1, "#243C16")),
        stroke="#2E441E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C2DCA0", strokeWidth=3, opacity=40)
# soft leaf-dapple light on the plate
for i, (x, y, w, h, op) in enumerate([(180, 200, 240, 140, 16), (620, 140, 200, 110, 14),
                                      (740, 420, 160, 120, 12), (240, 620, 180, 110, 10)]):
    d.shape("ellipse", f"Dapple {i+1}", x=x, y=y, width=w, height=h,
            fill="#D8ECB4", opacity=op, stroke=NONE)
# faint leaf silhouettes
for i, (x, y, w, h, op) in enumerate([(140, 320, 120, 60, 18), (720, 640, 130, 66, 16),
                                      (360, 130, 110, 52, 14)]):
    d.shape("ellipse", f"Leaf shadow {i+1}", x=x, y=y, width=w, height=h,
            fill="#1E3010", opacity=op, stroke=NONE)

# --- twig (closes on the disc arc) ------------------------------------------------
t0, t1 = disc_pt(155), disc_pt(28)
d.path(f"M{t0[0]:.1f},{t0[1]:.1f} C300,668 600,700 {t1[0]:.1f},{t1[1]:.1f} "
       f"A420,420 0 0 1 {t0[0]:.1f},{t0[1]:.1f} Z", "Twig",
       fill=lin(-90, (0, "#8A6E50"), (0.35, "#5E4A34"), (1, "#2E2114")),
       stroke="#1E140C", strokeWidth=5)
d.path(f"M{t0[0]+10:.0f},{t0[1]+8:.0f} C310,674 600,706 {t1[0]-12:.0f},{t1[1]+8:.0f}",
       "Twig top light", fill=NONE, stroke="#C8AC84", strokeWidth=4, opacity=45, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(180, 700, 320, 712), (380, 720, 520, 716),
                                      (580, 722, 720, 706), (240, 750, 400, 762),
                                      (480, 770, 640, 756), (700, 740, 800, 722)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2},{max(y0,y1)+8} {x1},{y1}", f"Twig furrow {i+1}",
           fill=NONE, stroke="#241708", strokeWidth=4, opacity=45, cap="round")
# a sprig of two leaves off the twig's right end
d.path("M760,668 C796,640 830,634 856,644 C834,672 800,682 760,668 Z", "Twig leaf 1",
       fill=lin(20, (0, "#7EA45A"), (1, "#3C5A28")), stroke="#22331C", strokeWidth=4)
d.path("M788,724 C822,726 848,742 856,768 C826,774 798,756 788,724 Z", "Twig leaf 2",
       fill=lin(60, (0, "#6E9450"), (1, "#33491F")), stroke="#22331C", strokeWidth=4)
d.path("M770,666 L844,650", "Leaf 1 vein", fill=NONE, stroke="#22331C",
       strokeWidth=3, opacity=55, cap="round")

# --- the shed nymph shell under the twig — seventeen years below -----------------
d.path("M306,676 C296,700 298,730 312,752 C322,764 338,764 346,750 "
       "C354,728 352,700 340,680 C330,668 314,666 306,676 Z", "Exuvia body",
       fill=rad((0, "#C8A87E"), (0.7, "#8A6E4E"), (1, "#5E4830")),
       opacity=62, stroke="#3E2C18", strokeWidth=3)
d.path("M300,676 C288,664 274,660 262,666 C272,678 288,684 300,676 Z", "Exuvia head",
       fill="#8A6E4E", opacity=62, stroke="#3E2C18", strokeWidth=3)
for j, (lx, ly) in enumerate([(296, 706), (300, 726), (336, 706), (332, 730)]):
    d.path(f"M{lx},{ly} L{lx - 12},{ly + 12}", f"Exuvia leg {j+1}", fill=NONE,
           stroke="#6E5638", strokeWidth=3, opacity=62, cap="round")
d.path("M310,690 C318,684 330,684 338,690", "Exuvia split", fill=NONE,
       stroke="#2E2010", strokeWidth=3, opacity=55, cap="round")

# contact shadow under the cicada
d.shape("ellipse", "Cicada shadow", x=330, y=636, width=340, height=30,
        fill="#0C1206", opacity=38, stroke=NONE)

# everything from here is the cicada; collect it so it can be nudged
CICADA = []
_call = d.call
def _capture(tool, args, label):
    r = _call(tool, args, label)
    if tool in ("draw_path", "draw_shape") and isinstance(r, dict) and "id" in r:
        CICADA.append(r["id"])
    return r
d.call = _capture

# --- far wing: the sliver that shows the roof fold ----------------------------------
d.path("M452,396 C560,380 680,420 762,494 C700,470 590,442 492,444 "
       "C466,438 452,420 452,396 Z", "Far wing",
       fill="#E8F2F0", opacity=45, stroke="#8AA0A0", strokeWidth=3)
d.path("M470,402 C570,390 670,428 744,488", "Far wing costa", fill=NONE,
       stroke="#C06818", strokeWidth=4, opacity=60, cap="round")

# --- legs (under the body, gripping the twig) -----------------------------------------
def leg(name, hip, knee, foot, far=False):
    col = "#1E1208" if far else "#4A2E14"
    op = 70 if far else 100
    hx, hy = hip; kx, ky = knee; fx, fy = foot
    d.path(f"M{hx},{hy} Q{(hx+kx)/2},{(hy+ky)/2 - 6} {kx},{ky} "
           f"Q{(kx+fx)/2 + 4},{(ky+fy)/2} {fx},{fy}", f"{name} ink",
           fill=NONE, stroke=INK, strokeWidth=9, cap="round", opacity=op)
    d.path(f"M{hx},{hy} Q{(hx+kx)/2},{(hy+ky)/2 - 6} {kx},{ky} "
           f"Q{(kx+fx)/2 + 4},{(ky+fy)/2} {fx},{fy}", name,
           fill=NONE, stroke=col, strokeWidth=5, cap="round", opacity=op)
    d.path(f"M{fx},{fy} L{fx - 6},{fy + 10}", f"{name} tarsus",
           fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=op)
    if not far:
        d.path(f"M{hx + 4},{hy + 2} Q{(hx+kx)/2 + 4},{(hy+ky)/2 - 8} {kx - 2},{ky - 2}",
               f"{name} amber edge", fill=NONE, stroke="#C87828", strokeWidth=3,
               opacity=60, cap="round")

leg("Far fore leg", (392, 560), (356, 612), (342, 668), far=True)
leg("Far hind leg", (560, 570), (540, 624), (546, 672), far=True)
# the cicada's fore femur is thick — digger's leg
d.path("M400,556 C382,570 368,596 366,622 C384,628 402,620 410,602 "
       "C416,584 414,566 400,556 Z", "Near fore femur",
       fill=linp(370, 556, 414, 622, (0, "#5E3A1A"), (1, "#2E1C0C")),
       stroke=INK, strokeWidth=4)
d.path("M376,610 C374,634 366,656 352,674", "Near fore tibia", fill=NONE,
       stroke="#4A2E14", strokeWidth=6, cap="round")
d.path("M352,674 L344,686", "Near fore tarsus", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
leg("Near mid leg", (470, 576), (452, 628), (436, 676))
leg("Near hind leg", (590, 570), (614, 622), (596, 674))

# --- body: stout black barrel ---------------------------------------------------------
d.path("M352,486 C346,452 372,428 412,424 C424,424 432,430 436,440 "
       "C560,430 650,470 672,540 C676,566 664,588 640,594 C540,616 430,606 380,568 "
       "C360,550 350,520 352,486 Z", "Body",
       fill=linp(400, 420, 620, 600, (0, "#3A2C20"), (0.5, "#221812"),
                 (1, "#0E0906")), stroke=INK, strokeWidth=6)
# abdomen segment bands
for j, (x, y0, y1) in enumerate([(470, 448, 592), (520, 452, 596), (570, 462, 592),
                                 (616, 476, 584)]):
    d.path(f"M{x},{y0} C{x + 14},{(y0+y1)/2 - 20} {x + 12},{(y0+y1)/2 + 30} {x},{y1}",
           f"Segment {j+1}", fill=NONE, stroke="#0A0604", strokeWidth=4,
           opacity=55, cap="round")
# warm dorsal sheen + orange marks behind the head (the magicicada pronotal patch)
d.path("M370,452 C440,430 560,440 640,486", "Dorsal sheen", fill=NONE,
       stroke="#8A6A48", strokeWidth=7, opacity=45, cap="round")
d.path("M428,434 C446,426 468,428 478,440 C470,452 448,456 434,448 Z",
       "Pronotal orange patch", fill="#C86E20", opacity=75, stroke=NONE)
d.path("M390,470 C420,458 460,458 490,468", "Thorax rim light", fill=NONE,
       stroke="#E8A860", strokeWidth=4, opacity=55, cap="round")

# --- near wing: translucent, folded roof-like over the back ----------------------------
WING = "M448,436 C540,402 660,430 780,514 C800,530 796,552 772,556 " \
       "C660,578 530,566 458,522 C432,500 430,464 448,436 Z"
d.path(WING, "Near wing", fill=linp(450, 420, 780, 560,
                                    (0, "#E4F0EE"), (0.55, "#C2D6D4"), (1, "#9AB4B4")),
       opacity=52, stroke="#5E7676", strokeWidth=4)
# glassy sheen bands on the membrane
d.path("M480,446 C580,424 680,452 758,516", "Wing sheen 1", fill=NONE,
       stroke="#FFFFFF", strokeWidth=8, opacity=30, cap="round")
d.path("M470,480 C560,460 650,484 724,538", "Wing sheen 2", fill=NONE,
       stroke="#FFFFFF", strokeWidth=5, opacity=22, cap="round")
# orange venation: thick costa, then long veins fanning to the trailing edge
d.path("M448,436 C540,402 660,430 780,514", "Costa", fill=NONE,
       stroke=ORANGE, strokeWidth=7, cap="round")
d.path("M448,436 C540,402 660,430 780,514", "Costa light", fill=NONE,
       stroke="#F2B060", strokeWidth=3, opacity=80, cap="round")
for j, (x0, y0, cx, cy, x1, y1) in enumerate([
        (500, 442, 560, 470, 600, 566),
        (540, 448, 620, 486, 668, 560),
        (585, 456, 680, 494, 736, 548),
        (630, 466, 720, 506, 772, 540)]):
    d.path(f"M{x0},{y0} Q{cx},{cy} {x1},{y1}", f"Long vein {j+1}", fill=NONE,
           stroke="#D8720F", strokeWidth=3.5, opacity=85, cap="round")
for j, (x, y) in enumerate([(560, 500), (610, 516), (660, 528)]):
    d.path(f"M{x},{y} L{x + 18},{y - 22}", f"Cross vein {j+1}", fill=NONE,
           stroke="#C06410", strokeWidth=3, opacity=70, cap="round")

# --- head: broad, with the huge red compound eye ---------------------------------------
d.path("M332,470 C330,436 352,412 388,408 C420,404 442,420 446,448 "
       "C448,476 432,500 402,508 C372,514 336,502 332,470 Z", "Head",
       fill=rad((0, "#4A3828"), (0.6, "#241A10"), (1, "#0E0805")),
       stroke=INK, strokeWidth=5)
# the big red eye, wrapped on the head's side
d.path("M344,462 C342,436 360,418 386,416 C404,420 414,436 410,458 "
       "C404,478 384,490 364,484 C350,478 342,472 344,462 Z", "Red eye",
       fill=rad((0, "#F04A34"), (0.55, "#C02418"), (1, "#6E0E08")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye glint", x=358, y=428, width=16, height=12,
        fill="#FFB8A0", opacity=80, stroke=NONE)
d.shape("ellipse", "Eye glint core", x=361, y=430, width=7, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# face sutures + short bristle antennae between the eyes
d.path("M398,428 C410,424 424,428 432,438", "Face suture", fill=NONE,
       stroke="#8A6A48", strokeWidth=3, opacity=55, cap="round")
d.path("M350,440 L332,428", "Far bristle", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M344,472 L324,470", "Near bristle", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")

d.call = _call
d.call("transform", {"ids": CICADA, "scale": 108, "origin": [500, 648]},
       "enlarge cicada on the twig")

# --- caption --------------------------------------------------------------------------
d.text("PERIODICAL CICADA", "Name", x=500, y=940, size=52, font="Virelai Sans",
       color="#E4EFC8", justify="center")
o = d.text("HEMIPTERA", "Order", x=500, y=975, size=22, font="Virelai Sans",
           color="#A8C284", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("periodical-cicada-V1R00")
