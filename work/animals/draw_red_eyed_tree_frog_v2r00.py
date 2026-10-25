#!/usr/bin/env python3
"""Red-eyed tree frog — traditional American tattoo flash rendition V2R00.
Thick warm-black outlines (>=6pt, essential toes >=3pt), flat fills, limited
flash palette (green / red / orange / yellow / cream / black + one blue
flank accent), frog gripping a rain-wet stalk, ribbon banner beneath.
Rendition rules: no plate disc, flat is the point; everything inside the
60pt safe margin. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Red-eyed Tree Frog — Tattoo Flash V2R00", 1000, 1000)

INK    = "#1A1210"   # warm black
GREEN  = "#4CAE44"   # body green
GREEN_D = "#2E7A30"  # leaf/shade green
CREAM  = "#F6E8C0"   # flash-sheet skin tone
RED    = "#D82412"   # eye red
ORANGE = "#F08018"   # toe pads
YELLOW = "#F4C93A"   # banner
BLUE   = "#3A6EC8"   # flank accent

# --- field: flat cream flash sheet, faint vignette ------------------------------
d.shape("rectangle", "Field", x=0, y=0, width=1000, height=1000,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F8EFD8"}, {"offset": 1, "color": "#E4D2A8"}]}},
        stroke=NONE)
# thin device ring + classic sunburst dashes behind the frog
d.shape("ellipse", "Device ring", x=170, y=100, width=660, height=660,
        fill=NONE, stroke=INK, strokeWidth=4)
CXD, CYD = 500, 430
for i in range(24):
    a = math.radians(i * 15)
    r0, r1 = 342, 372
    x0, y0 = CXD + r0 * math.cos(a), CYD + r0 * math.sin(a)
    x1, y1 = CXD + r1 * math.cos(a), CYD + r1 * math.sin(a)
    d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Sunburst {i+1}",
           fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# --- the wet stalk: top-right to bottom-right behind the frog; the bottom
# end tucks behind the banner so nothing dangles under it ------------------
d.path("M596,150 C586,290 600,440 630,580 C646,660 658,712 668,742",
       "Stalk", fill=NONE, stroke=GREEN_D, strokeWidth=22, cap="round")
d.path("M590,160 C582,290 596,440 624,576", "Stalk sheen", fill=NONE,
       stroke="#7EC872", strokeWidth=5, cap="round", opacity=80)
# a leaf blade sweeping left from the stalk, seat for the frog
d.path("M640,580 C560,540 430,540 336,614 C350,684 470,714 560,688 "
       "C600,676 626,636 640,580 Z",
       "Leaf blade", fill=GREEN_D, stroke=INK, strokeWidth=6)
d.path("M628,588 C540,566 440,576 356,622", "Leaf rib", fill=NONE,
       stroke="#7EC872", strokeWidth=5, cap="round")
# rain beads standing on the stalk
for i, (x, y, w) in enumerate([(594, 250, 14), (604, 400, 11), (634, 560, 13)]):
    d.shape("ellipse", f"Bead {i+1}", x=x - w / 2, y=y - w / 2, width=w, height=w * 1.2,
            fill="#DFF4F0", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Bead glint {i+1}", x=x - w * 0.22, y=y - w * 0.3,
            width=w * 0.3, height=w * 0.22, fill="#FFFFFF", stroke=NONE)

# === the frog, side view clinging to the stalk ===================================
# hind thigh: the big folded dome, drawn first so the body sits over it
d.path("M470,470 C520,420 610,410 664,452 C708,486 716,548 686,596 "
       "C662,634 604,652 552,640 C500,628 458,560 470,470 Z",
       "Hind thigh", fill=GREEN, stroke=INK, strokeWidth=7)
# thigh fold line
d.path("M540,470 C590,470 640,500 658,548", "Thigh fold", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")

# body: dome from rounded snout over the back to the rump
d.path("M326,486 C330,436 360,392 410,366 C446,348 492,342 532,352 "
       "C584,364 626,400 650,448 C668,486 668,530 648,566 "
       "C620,616 552,640 478,634 C416,630 360,600 340,556 "
       "C328,530 324,508 326,486 Z",
       "Body", fill=GREEN, stroke=INK, strokeWidth=7)
# belly: flat cream underside
d.path("M348,520 C380,596 460,626 540,620 C596,616 636,590 648,556 "
       "C650,596 600,626 520,634 C440,640 372,606 352,556 "
       "C346,542 346,530 348,520 Z",
       "Belly", fill=CREAM, stroke=INK, strokeWidth=5)
# flank flash: blue patch with cream bars — the species' calling card
d.path("M500,470 C540,466 580,480 600,510 C606,540 596,566 570,578 "
       "C536,586 508,574 498,548 C490,522 490,494 500,470 Z",
       "Flank", fill=BLUE, stroke=INK, strokeWidth=5)
for k in range(3):
    x = 520 + k * 26
    d.path(f"M{x},486 C{x + 8},512 {x + 8},544 {x},566",
           f"Flank bar {k+1}", fill=NONE, stroke=CREAM, strokeWidth=6, cap="round")

# dorsal line separating back from flank
d.path("M420,392 C470,368 540,366 596,392", "Back line", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")

# === feet gripping the stalk — toes >=3pt, orange pads ===========================
# limbs are thick stroked members (ink under green); each toe curls to a pad
# ON the stalk, pads landing on both sides so the grip reads.
def limb(p0, p1, p2, w, label):
    d.path(f"M{p0[0]},{p0[1]} Q{p1[0]},{p1[1]} {p2[0]},{p2[1]}",
           f"{label} ink", fill=NONE, stroke=INK, strokeWidth=w + 8, cap="round")
    d.path(f"M{p0[0]},{p0[1]} Q{p1[0]},{p1[1]} {p2[0]},{p2[1]}",
           label, fill=NONE, stroke=GREEN, strokeWidth=w, cap="round")

def foot2(wx, wy, pads, label):
    for k, (tx, ty) in enumerate(pads):
        mx, my = (wx + tx) / 2, (wy + ty) / 2 - 12
        d.path(f"M{wx},{wy} Q{mx:.0f},{my:.0f} {tx},{ty}", f"{label} toe {k+1}",
               fill=NONE, stroke=INK, strokeWidth=9, cap="round")
        d.path(f"M{wx},{wy} Q{mx:.0f},{my:.0f} {tx},{ty}", f"{label} toe skin {k+1}",
               fill=NONE, stroke=GREEN, strokeWidth=4.5, cap="round")
    for k, (tx, ty) in enumerate(pads):
        d.shape("ellipse", f"{label} pad {k+1}", x=tx - 13, y=ty - 11,
                width=26, height=22, fill=ORANGE, stroke=INK, strokeWidth=3.5)

# foreleg reaches right-down to the wrist; toes clamp the stalk (~x 630-660 here)
limb((372, 540), (470, 610), (596, 630), 22, "Foreleg")
foot2(596, 630, [(622, 600), (654, 630), (668, 592)], "Forefoot")
# hind shank kicks back to the stalk lower down
limb((560, 596), (620, 650), (662, 688), 24, "Hind shank")
foot2(662, 688, [(628, 712), (664, 736), (694, 706)], "Hindfoot")

# === head: the one red eye facing us =============================================
# eye dome bulging off the crown
d.shape("ellipse", "Eye dome", x=352, y=316, width=92, height=88,
        fill=GREEN, stroke=INK, strokeWidth=6)
# the traffic-light iris
d.shape("ellipse", "Iris", x=362, y=326, width=72, height=68,
        fill=RED, stroke=INK, strokeWidth=5)
# vertical slit pupil
d.shape("ellipse", "Pupil", x=392, y=336, width=14, height=48,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye glint", x=374, y=338, width=14, height=12,
        fill="#FFFFFF", stroke=NONE)
# gold rim under the iris — classic flash catch
d.path("M366,382 C380,392 412,394 428,384", "Iris rim", fill=NONE,
       stroke=YELLOW, strokeWidth=4, cap="round")
# nostril + the quiet mouth line
d.shape("ellipse", "Nostril", x=336, y=452, width=12, height=9,
        fill=INK, stroke=NONE)
d.path("M330,500 C380,524 450,530 510,520", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M332,522 C352,532 372,538 392,540", "Jaw fold", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=70)

# === the ribbon banner ===========================================================
BY = 770                     # banner centreline
# folded wings first, then the face band over them
d.path(f"M250,{BY - 34} L160,{BY - 52} L196,{BY} L160,{BY + 52} L250,{BY + 34} Z",
       "Banner wing L", fill=YELLOW, stroke=INK, strokeWidth=6)
d.path(f"M750,{BY - 34} L840,{BY - 52} L804,{BY} L840,{BY + 52} L750,{BY + 34} Z",
       "Banner wing R", fill=YELLOW, stroke=INK, strokeWidth=6)
# fold creases
d.path(f"M250,{BY - 34} L236,{BY} L250,{BY + 34}", "Fold L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path(f"M750,{BY - 34} L764,{BY} L750,{BY + 34}", "Fold R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path(f"M226,{BY - 40} L774,{BY - 40} L774,{BY + 40} L226,{BY + 40} Z",
       "Banner face", fill=CREAM, stroke=INK, strokeWidth=6)
t = d.text("RED-EYED TREE FROG", "Banner text", x=500, y=BY + 17, size=46,
           font="Phosphate", color=INK, justify="center")
if t is None:
    t = d.text("RED-EYED TREE FROG", "Banner text", x=500, y=BY + 15, size=44,
               font="Virelai Sans", color=INK, justify="center")

sub = d.text("AGALYCHNIS CALLIDRYAS", "Subline", x=500, y=902, size=26,
             font="Virelai Sans", color=INK, justify="center")
if sub:
    d.cmd("text.setStyle", "Subline tracking", ids=[sub["id"]], tracking=220)
# small diamonds flanking the subline
for lab, x in (("L", 210), ("R", 790)):
    d.path(f"M{x},888 L{x + 12},900 L{x},912 L{x - 12},900 Z",
           f"Subline diamond {lab}", fill=INK, stroke=NONE)

d.finish("red-eyed-tree-frog-V2R00")
