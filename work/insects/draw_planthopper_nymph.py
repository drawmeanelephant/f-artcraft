#!/usr/bin/env python3
"""Planthopper nymph — field plate V1R00. A puff of wax with a plan:
three-quarter view mid-hop above a leaf, the abdomen tipped with a fan of
waxy filaments, pale green body wearing a translucent skirt, hind leg
extended mid-jump; leaf-green plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Planthopper Nymph — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#22401E"
WAX = "#FFF6E4"

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

# --- backdrop + leaf-green plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(-90, (0, "#0C1408"), (1, "#040703")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#94BC64"), (0.6, "#568040"), (1, "#26401C")),
        stroke="#2E4A20", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E4A4", strokeWidth=3, opacity=40)
# faint leaf-vein fan on the plate: midrib + veins, all inside the disc
d.path("M200,760 C330,600 480,420 700,220", "Plate midrib", fill=NONE,
       stroke="#3C6028", strokeWidth=6, opacity=25, cap="round")
for i, (x0, y0, cx, cy, x1, y1) in enumerate([
        (300, 640, 400, 560, 480, 560), (380, 540, 480, 470, 560, 460),
        (460, 440, 560, 370, 660, 350), (340, 600, 420, 560, 470, 610),
        (430, 480, 520, 460, 570, 490)]):
    d.path(f"M{x0},{y0} Q{cx},{cy} {x1},{y1}", f"Plate vein {i+1}", fill=NONE,
           stroke="#3C6028", strokeWidth=4, opacity=22, cap="round")
# dew specks
for i, (x, y, w) in enumerate([(230, 300, 10), (760, 260, 8), (820, 520, 9), (190, 520, 8),
                               (640, 160, 7), (300, 180, 8), (700, 700, 9), (400, 800, 7)]):
    d.shape("ellipse", f"Dew {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8F6DC", opacity=45, stroke=NONE)
d.shape("ellipse", "Dew glint", x=232, y=301, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)

# --- leaf blade the nymph launches from (closes on the disc arc) -------------------
l0, l1 = disc_pt(152), disc_pt(24)
d.path(f"M{l0[0]:.1f},{l0[1]:.1f} C300,676 620,700 {l1[0]:.1f},{l1[1]:.1f} "
       f"A420,420 0 0 1 {l0[0]:.1f},{l0[1]:.1f} Z", "Leaf blade",
       fill=lin(-90, (0, "#9CC470"), (0.4, "#5E8C42"), (1, "#2E4E22")),
       stroke="#203818", strokeWidth=5)
d.path(f"M{l0[0]+12:.0f},{l0[1]+8:.0f} C320,682 620,706 {l1[0]-14:.0f},{l1[1]+8:.0f}",
       "Leaf edge light", fill=NONE, stroke="#DCF0B8", strokeWidth=4, opacity=50, cap="round")
# leaf margin serrations along the top edge
for i, (x, y) in enumerate([(250, 672), (330, 668), (410, 668), (490, 672), (570, 678), (650, 686)]):
    d.path(f"M{x},{y} L{x + 14},{y - 6} L{x + 24},{y + 2}", f"Leaf serration {i+1}",
           fill=NONE, stroke="#2E4E22", strokeWidth=3, opacity=55, cap="round")
# where the hind foot just left the leaf: a scuffed print
d.shape("ellipse", "Launch print", x=300, y=664, width=46, height=14,
        fill="#2E4E22", opacity=40, stroke=NONE)

# soft shadow of the airborne nymph on the leaf
d.shape("ellipse", "Nymph shadow", x=360, y=652, width=190, height=22,
        fill="#14230C", opacity=30, stroke=NONE)

# everything from here is the nymph; collect it so it can be nudged
NYMPH = []
_call = d.call
def _capture(tool, args, label):
    r = _call(tool, args, label)
    if tool in ("draw_path", "draw_shape") and isinstance(r, dict) and "id" in r:
        NYMPH.append(r["id"])
    return r
d.call = _capture

# --- the wax fan: filaments radiating off the abdomen tip ------------------------------
TIPX, TIPY = 590, 480   # abdomen tip — the wax glands sit here
def filament(i, ang, L, curl, w=4):
    """One waxy filament: glow underlay, cream core, curled bead tip."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    x1, y1 = TIPX + ca * L, TIPY + sa * L
    cx, cy = TIPX + ca * L * 0.5 - sa * curl, TIPY + sa * L * 0.5 + ca * curl
    # soft glow underlay
    d.path(f"M{TIPX},{TIPY} Q{cx:.0f},{cy:.0f} {x1:.0f},{y1:.0f}", f"Wax glow {i}",
           fill=NONE, stroke=WAX, strokeWidth=w + 7, opacity=18, cap="round")
    d.path(f"M{TIPX},{TIPY} Q{cx:.0f},{cy:.0f} {x1:.0f},{y1:.0f}", f"Wax filament {i}",
           fill=NONE, stroke=WAX, strokeWidth=w, opacity=88, cap="round")
    # little hook curl + bead at the tip
    hx, hy = x1 - sa * curl * 0.4, y1 + ca * curl * 0.4
    d.path(f"M{x1:.0f},{y1:.0f} Q{hx:.0f},{hy:.0f} {x1 - ca*12:.0f},{y1 - sa*12 - 8:.0f}",
           f"Wax curl {i}", fill=NONE, stroke=WAX, strokeWidth=3, opacity=80, cap="round")
    d.shape("ellipse", f"Wax bead {i}", x=x1 - ca*12 - 11, y=y1 - sa*12 - 11,
            width=6, height=6, fill=WAX, opacity=80, stroke=NONE)

# fan: a peacock-tail burst over the back — longest up, shorter down
fan = [(-8, 150, 26), (-28, 190, 20), (-48, 215, 10), (-68, 225, -4),
       (-88, 220, -16), (-108, 200, -22), (-128, 170, -20), (-146, 138, -14),
       (8, 110, 30), (24, 80, 34)]
for i, (ang, L, curl) in enumerate(fan):
    filament(i, ang, L, curl)
# dense tuft right at the gland tip
for i, (ang, L) in enumerate([(-36, 90), (-60, 96), (-84, 92), (-110, 84)]):
    a = math.radians(ang)
    d.path(f"M{TIPX},{TIPY} L{TIPX + math.cos(a)*L:.0f},{TIPY + math.sin(a)*L:.0f}",
           f"Wax tuft {i}", fill=NONE, stroke=WAX, strokeWidth=6, opacity=55, cap="round")
d.shape("ellipse", "Wax gland", x=TIPX - 10, y=TIPY - 10, width=22, height=22,
        fill=rad((0, "#FFFDF4"), (1, "#E8DCB8")), stroke="#C8B888", strokeWidth=3)

# --- body: plump pale-green pear, three-quarter -----------------------------------------
d.path("M372,540 C366,496 400,462 452,454 C508,446 562,462 588,494 "
       "C604,514 602,540 584,556 C540,588 448,594 402,572 C384,562 374,552 372,540 Z",
       "Body", fill=linp(400, 450, 560, 590, (0, "#D8F0BC"), (0.55, "#A2CE82"),
                         (1, "#5E8A50")), stroke=INK, strokeWidth=5)
# translucent waxy skirt around the abdomen's lower edge
d.path("M396,560 C440,586 520,590 578,560 C566,594 540,616 496,620 "
       "C450,624 410,602 396,560 Z", "Wax skirt",
       fill="#FFF2DC", opacity=45, stroke="#D8C898", strokeWidth=3)
for j, x in enumerate([420, 460, 500, 540]):
    d.path(f"M{x},{586 + (x - 460) // 14} L{x - 6},{604}", f"Skirt fringe {j+1}",
           fill=NONE, stroke="#F0E0BC", strokeWidth=3.5, opacity=60, cap="round")
# segment arcs + sheen on the back
for j, (x, y0, y1) in enumerate([(430, 462, 560), (475, 458, 574), (520, 462, 578),
                                 (560, 474, 570)]):
    d.path(f"M{x},{y0} C{x + 10},{(y0+y1)/2 - 14} {x + 10},{(y0+y1)/2 + 14} {x},{y1}",
           f"Body segment {j+1}", fill=NONE, stroke="#4E7038", strokeWidth=3,
           opacity=45, cap="round")
d.path("M396,508 C420,474 470,458 520,462", "Back sheen", fill=NONE,
       stroke="#F4FCD8", strokeWidth=6, opacity=55, cap="round")
d.shape("ellipse", "Back gloss", x=410, y=462, width=110, height=40,
        fill="#FFFFFF", opacity=18, stroke=NONE)

# --- head: small, pointy frons, big eye for a nymph -------------------------------------
d.path("M344,548 C336,520 348,494 372,486 C392,486 404,500 404,522 "
       "C404,546 386,564 364,564 C354,562 346,556 344,548 Z", "Head",
       fill=rad((0, "#C4E4A4"), (0.65, "#86B468"), (1, "#4E7438")),
       stroke=INK, strokeWidth=4)
# pointed frons poking down-forward
d.path("M346,552 C332,562 322,576 320,592 C334,592 348,580 354,564 Z", "Frons",
       fill="#86B468", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye", x=352, y=500, width=24, height=28,
        fill=rad((0, "#8A6E3E"), (1, "#241808")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=357, y=505, width=6, height=6,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# rostrum fold + short antenna bristle
d.path("M360,560 C368,570 378,576 388,578", "Rostrum", fill=NONE,
       stroke="#3C6028", strokeWidth=3, opacity=60, cap="round")
d.path("M352,492 C336,478 322,472 308,470", "Antenna bristle", fill=NONE,
       stroke="#4E7438", strokeWidth=3, cap="round")
d.shape("ellipse", "Bristle tip", x=305, y=467, width=6, height=6,
        fill="#4E7438", stroke=NONE)

# --- legs mid-hop ----------------------------------------------------------------------
def leg(name, pts, w_ink, w_core, col="#3A6028", far=False):
    op = 65 if far else 100
    pstr = f"M{pts[0][0]},{pts[0][1]} " + " ".join(f"L{x},{y}" for x, y in pts[1:])
    d.path(pstr, f"{name} ink", fill=NONE, stroke=INK, strokeWidth=w_ink,
           cap="round", join="round", opacity=op)
    d.path(pstr, name, fill=NONE, stroke=col, strokeWidth=w_core,
           cap="round", join="round", opacity=op)

# hind jumping leg: extended straight, toe just off the leaf
leg("Hind leg", [(540, 560), (470, 600), (400, 634), (346, 660)], 10, 5.5)
d.path("M346,660 L334,664", "Hind toe", fill=NONE, stroke=INK, strokeWidth=3.5,
       cap="round")
# femur flare on the jumper
d.path("M540,560 C512,568 488,584 474,600 C492,608 516,602 534,588 "
       "C544,578 546,568 540,560 Z", "Hind femur",
       fill=linp(480, 560, 540, 610, (0, "#9EC47E"), (1, "#4E7438")),
       stroke=INK, strokeWidth=4)
# mid leg reaching forward-down, airborne
leg("Mid leg", [(430, 574), (416, 624), (444, 656)], 8, 4.5)
d.path("M444,656 L452,664", "Mid toe", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# fore leg tucked under the head
leg("Fore leg", [(386, 566), (400, 610), (384, 646)], 8, 4.5)
d.path("M384,646 L376,656", "Fore toe", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# far-side legs sketching behind
leg("Far hind leg", [(556, 548), (520, 588), (480, 612)], 8, 4, "#2E4E22", far=True)
leg("Far mid leg", [(450, 556), (456, 598), (478, 624)], 7, 4, "#2E4E22", far=True)

d.call = _call
d.call("transform", {"ids": NYMPH, "dx": -16, "dy": -10}, "nudge nymph")

# --- caption --------------------------------------------------------------------------
d.text("PLANTHOPPER NYMPH", "Name", x=500, y=938, size=48, font="Virelai Sans",
       color="#E8F2CC", justify="center")
o = d.text("HEMIPTERA", "Order", x=500, y=974, size=22, font="Virelai Sans",
           color="#B4CC8E", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Order tracking", ids=[o["id"]], tracking=400)

d.finish("planthopper-nymph-V1R00")
