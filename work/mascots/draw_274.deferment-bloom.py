#!/usr/bin/env python3
"""Deferment Bloom — mascot portrait V1R00.
The mascot offers a bouquet of moving targets while the schedule page
beside it is overgrown with blooms — the delay certified as a maturation
period, perennial, quarter over quarter. 1000x1000.
Gradients + translucent shading, no flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Deferment Bloom — Mascot Portrait", 1000, 1000)

INK = "#1E1A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1310"}, {"offset": 1, "color": "#060907"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#57624C"}, {"offset": 0.7, "color": "#3B4434"},
    {"offset": 1, "color": "#20251B"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4230"}, {"offset": 1, "color": "#1B2015"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCB896"}, {"offset": 0.7, "color": "#B48C64"},
    {"offset": 1, "color": "#886646"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE0BE"}, {"offset": 1, "color": "#D3C297"}]}}
ROSE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E09A92"}, {"offset": 1, "color": "#A85A54"}]}}
CORAL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D88A6E"}, {"offset": 1, "color": "#9E5238"}]}}
CREAM_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E4B4"}, {"offset": 1, "color": "#C4AC72"}]}}

def scallop(cx, cy, r, bumps=9, wob=0.14):
    pts = [(cx + r * (1 + (wob if i % 2 else -wob)) * math.cos(2 * math.pi * i / (2 * bumps)),
            cy + r * (1 + (wob if i % 2 else -wob)) * math.sin(2 * math.pi * i / (2 * bumps)))
           for i in range(2 * bumps)]
    m = [((pts[i][0] + pts[(i + 1) % len(pts)][0]) / 2,
          (pts[i][1] + pts[(i + 1) % len(pts)][1]) / 2) for i in range(len(pts))]
    out = f"M{m[0][0]:.1f},{m[0][1]:.1f} "
    for i in range(len(pts)):
        p = pts[(i + 1) % len(pts)]
        mm = m[(i + 1) % len(m)]
        out += f"Q{p[0]:.1f},{p[1]:.1f} {mm[0]:.1f},{mm[1]:.1f} "
    return out + "Z"

def target_bloom(cx, cy, r, grad, name):
    """A bloom grown as a moving target: petal ring, cream ring, bullseye."""
    d.path(scallop(cx, cy, r, 9, 0.15), f"{name} petals", fill=grad,
           stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"{name} ring", x=cx - r * 0.62, y=cy - r * 0.62,
            width=r * 1.24, height=r * 1.24, fill=CREAM_GRAD,
            stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"{name} inner", x=cx - r * 0.36, y=cy - r * 0.36,
            width=r * 0.72, height=r * 0.72, fill=grad,
            stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"{name} bullseye", x=cx - r * 0.16,
            y=cy - r * 0.16, width=r * 0.32, height=r * 0.32,
            fill="#E8C060", stroke=INK, strokeWidth=2)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A8460", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D4AC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#454E38", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#12150E",
       strokeWidth=4, opacity=70)

# --- the schedule page, on its little easel -----------------------------------------
# easel legs behind the page
d.path("M640,560 L610,700 M742,560 L772,700", "Easel legs", fill=NONE,
       stroke="#4E3A28", strokeWidth=9, cap="round")
d.path("M605,668 L777,668", "Easel ledge", fill=NONE, stroke="#4E3A28",
       strokeWidth=10, cap="round")
d.path(rot_rect_path(688, 486, 205, 265, 4), "Schedule page",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=4.5)
# the pin holding it
d.shape("ellipse", "Page pin", x=678, y=356, width=14, height=14,
        fill="#8A5038", stroke=INK, strokeWidth=2.5)
# ruled rows and deadline marks
for i, y in enumerate([400, 436, 472, 508, 544]):
    d.path(f"M612,{y} L762,{y + 4}", f"Page row {i+1}", fill=NONE,
           stroke="#A89878", strokeWidth=2.5, opacity=75)
for i, (x, y) in enumerate([(620, 394), (620, 430), (620, 466)]):
    d.shape("rectangle", f"Checkbox {i+1}", x=x, y=y, width=13, height=13,
            fill=NONE, stroke="#8A7858", strokeWidth=2.5, radius=2)
# a milestone circled, then moved — the dashed drift to the right
d.shape("ellipse", "Circled date", x=700, y=428, width=30, height=24,
        fill=NONE, stroke="#B05A4A", strokeWidth=3)
d.path("M712,452 C716,470 736,480 758,482", "Drift dash", fill=NONE,
       stroke="#B05A4A", strokeWidth=3, cap="round")
d.path("M752,475 L766,483 L750,491 Z", "Drift arrow", fill="#B05A4A",
       stroke=NONE)
# struck-through date — the deadline that was
d.path("M618,540 L658,548 M620,544 L654,540", "Struck date", fill=NONE,
       stroke="#8A7858", strokeWidth=3, cap="round")

# --- the overgrowth: vines take the page's left edge ------------------------------
d.path("M592,668 C580,620 590,570 602,530 C610,500 606,470 596,450",
       "Vine stem", fill=NONE, stroke="#4E7A42", strokeWidth=6,
       cap="round")
d.path("M602,530 C586,516 568,514 554,522 C560,536 578,542 602,530 Z",
       "Vine leaf 1", fill="#5E8A4E", stroke=INK, strokeWidth=3)
d.path("M598,478 C614,464 632,462 646,470 C640,484 622,490 598,478 Z",
       "Vine leaf 2", fill="#5E8A4E", stroke=INK, strokeWidth=3)
d.path("M594,596 C608,584 624,582 636,588 C632,602 614,608 594,596 Z",
       "Vine leaf 3", fill="#5E8A4E", stroke=INK, strokeWidth=3)
target_bloom(592, 442, 26, ROSE_GRAD, "Vine bloom 1")
target_bloom(600, 556, 22, CORAL_GRAD, "Vine bloom 2")
target_bloom(590, 648, 24, ROSE_GRAD, "Vine bloom 3")

# --- the mascot, offering -------------------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=280, y=668, width=230, height=20,
        fill="#0C0E08", opacity=45, stroke=NONE)
d.shape("ellipse", "Body", x=305, y=470, width=185, height=190,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for x in (315, 420):
    d.shape("ellipse", f"Foot {x}", x=x, y=650, width=58, height=24,
            fill="#886646", stroke=INK, strokeWidth=4)
for ex in (328, 466):
    d.shape("ellipse", f"Ear {ex}", x=ex - 11, y=330, width=26, height=24,
            fill="#B48C64", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Head", x=322, y=334, width=150, height=136,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# gentle hopeful eyes, a soft salesman's smile
d.shape("ellipse", "Eye L", x=356, y=390, width=15, height=19,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=418, y=390, width=15, height=19,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=360, y=394, width=5, height=5,
        fill="#FFF8E8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=422, y=394, width=5, height=5,
        fill="#FFF8E8", opacity=90, stroke=NONE)
d.path("M368,434 C380,446 400,448 414,438", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek", x=346, y=414, width=20, height=12,
        fill="#D08A7A", opacity=35, stroke=NONE)

# --- the bouquet of moving targets ------------------------------------------------------
# stems converge at the offering paw
for i, (bx, by) in enumerate([(468, 368), (512, 346), (552, 370),
                              (490, 394), (534, 398)]):
    d.path(f"M{bx},{by+24} C{bx-6},{by+70} 492,470 492,508",
           f"Stem {i+1}", fill=NONE, stroke="#5E8A4E", strokeWidth=4,
           cap="round")
# a leaf or two on the way up
d.path("M492,470 C478,458 462,458 452,466 C458,478 474,482 492,470 Z",
       "Bouquet leaf", fill="#5E8A4E", stroke=INK, strokeWidth=3)
# the wrap: a paper cone where the stems gather
d.path("M462,494 L522,494 L500,548 Z", "Bouquet wrap",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.path("M462,494 L500,548 L478,548 Z", "Wrap shade", fill="#B8A276",
       opacity=60, stroke=NONE)
# the target blooms themselves
target_bloom(468, 368, 30, ROSE_GRAD, "Target 1")
target_bloom(512, 346, 34, CORAL_GRAD, "Target 2")
target_bloom(552, 370, 28, ROSE_GRAD, "Target 3")
target_bloom(490, 394, 20, CORAL_GRAD, "Target 4")
target_bloom(534, 398, 18, ROSE_GRAD, "Target 5")
# motion marks — the targets have already moved twice this sprint
for i, (x, y) in enumerate([(422, 362), (592, 362), (442, 406)]):
    d.path(f"M{x},{y-16} C{x-8},{y-6} {x-8},{y+6} {x},{y+16}",
           f"Motion {i+1}", fill=NONE, stroke="#D8D4AC",
           strokeWidth=3, cap="round", opacity=60)
# the offering arm and paw gripping the wrap
d.path("M446,556 C462,540 476,524 488,512", "Offer arm", fill=NONE,
       stroke="#B48C64", strokeWidth=18, cap="round")
d.shape("ellipse", "Offer paw", x=472, y=492, width=40, height=32,
        fill="#DCB896", stroke=INK, strokeWidth=4)

# --- a volunteer bloom sprouting on the floor — perennial --------------------------------
d.path("M570,688 C570,676 572,668 576,660", "Floor stem", fill=NONE,
       stroke="#5E8A4E", strokeWidth=4, cap="round")
target_bloom(578, 652, 18, CORAL_GRAD, "Floor bloom")

# --- motes ------------------------------------------------------------------------------
for i, (x, y, w) in enumerate([(262,420,5),(244,580,6),(648,240,5),(836,470,6),
                               (224,640,5),(812,300,6),(356,240,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D08A", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("DEFERMENT BLOOM", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EEE8D0", justify="center")
r = d.text("THE DEADLINE, IN BLOOM", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#BCC490", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("274.deferment-bloom-V1R00")
