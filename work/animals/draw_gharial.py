#!/usr/bin/env python3
"""Gharial — field-guide plate V1R00. Long head profile facing left, lying in
the shallows: the absurdly thin, tooth-studded snout run straight across the
disc, the male's bulbous ghara capping its tip, periscope eyes, keeled nuchal
and dorsal scutes on the neck and back sinking into murky river water.
Olive-bronze, river-murk palette.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gharial — Field Plate", 1000, 1000)

INK = "#24240F"
CX, CY = 500, 460                  # plate disc centre
WATER_Y = 578                      # river surface
DOWN = -90                         # linear gradient angle: top -> bottom
BG_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#262818"}, {"offset": 1, "color": "#0A0B06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E7E3C6"}, {"offset": 0.7, "color": "#BFB78D"},
    {"offset": 1, "color": "#857C52"}]}}
HEAD_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#9A9256"}, {"offset": 0.55, "color": "#73703A"},
    {"offset": 1, "color": "#4C4A24"}]}}
JAW_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#BDB27A"}, {"offset": 1, "color": "#857B47"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#858146"}, {"offset": 0.7, "color": "#5E5B2E"},
    {"offset": 1, "color": "#3C3A1B"}]}}
SCUTE_A = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#A39A5C"}, {"offset": 1, "color": "#5E5A2C"}]}}
SCUTE_B = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#8E8A4E"}, {"offset": 1, "color": "#4F4C24"}]}}
GHARA_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A39858"}, {"offset": 0.7, "color": "#76703A"},
    {"offset": 1, "color": "#4E4822"}]}}
REED_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#A8A274"}, {"offset": 1, "color": "#6E6A44"}]}}
TOOTH_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#FBF4DC"}, {"offset": 1, "color": "#CFC29A"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8DC8A"}, {"offset": 0.65, "color": "#B49A44"},
    {"offset": 1, "color": "#6E5A22"}]}}
WATER_GRAD = {"gradient": {"kind": "linear", "angle": DOWN, "stops": [
    {"offset": 0, "color": "#6F7A55"}, {"offset": 0.5, "color": "#4A5536"},
    {"offset": 1, "color": "#2B3220"}]}}

def chord_x(y, r):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A6240", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2EED6", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=150, width=250, height=150, fill="#A69E72", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=170, width=230, height=130, fill="#A69E72", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(780,300,7),(160,420,6),(850,420,7),(400,120,7),
                               (610,115,8),(270,200,6),(720,190,7),(300,350,6),(480,250,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#7C7448", opacity=40, stroke=NONE)
# far bank: a hazy sandbar sitting on the waterline, every vertex inside the disc
d.path(f"M150,{WATER_Y} C230,548 330,538 430,544 C560,552 700,536 850,{WATER_Y} Z",
       "Far sandbar", fill="#9E9468", opacity=30, stroke=NONE)
for i, (x0, x1, y) in enumerate([(190, 330, 552), (560, 760, 548)]):
    d.path(f"M{x0},{y} C{(2*x0+x1)/3:.0f},{y-6} {(x0+2*x1)/3:.0f},{y-6} {x1},{y}",
           f"Sandbar light {i+1}", fill=NONE, stroke="#F2EBCB", strokeWidth=3, opacity=30, cap="round")

# far reeds on the sandbar (behind the animal, soft)
for i, (x, top, lean, op) in enumerate([(196, 420, -14, 40), (218, 380, 6, 45), (240, 440, 18, 35),
                                        (262, 400, 26, 30), (700, 300, -10, 30), (724, 340, 8, 40),
                                        (748, 280, 20, 35), (772, 330, 30, 30), (796, 360, 12, 25)]):
    d.path(f"M{x},552 Q{x + lean*0.3:.0f},{(552+top)/2:.0f} {x+lean},{top}", f"Reed {i+1}",
           fill=NONE, stroke=REED_GRAD, strokeWidth=4, opacity=op, cap="round")
    d.path(f"M{x + lean - 3},{top + 10} C{x + lean - 6},{top - 6} {x + lean + 6},{top - 6} "
           f"{x + lean + 3},{top + 10} C{x + lean + 4},{top + 30} {x + lean - 4},{top + 30} {x + lean - 3},{top + 10} Z",
           f"Reed head {i+1}", fill="#7C744A", opacity=op, stroke=NONE)
# hazy low sun through the murk
for i, (rad, op) in enumerate([(130, 5), (105, 6), (82, 7), (62, 9), (44, 12)]):
    d.shape("ellipse", f"Sun haze {i+1}", x=430 - rad, y=250 - rad, width=2*rad, height=2*rad,
            fill="#FFFBE6", opacity=op, stroke=NONE)

# --- neck + back, closed on the disc's own arc (right) ---------------------------
rr = 412           # kept inside the rim so the body's stroke never crosses it
ry0, ry1 = 432, 690
bx0 = chord_x(ry0, rr)[1]; bx1 = chord_x(ry1, rr)[1]
d.path(f"M560,432 C600,404 650,392 702,398 C770,406 840,414 {bx0:.1f},{ry0} "
       f"A{rr},{rr} 0 0 1 {bx1:.1f},{ry1} "
       f"C790,664 700,612 652,580 C612,556 584,530 560,500 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# pale throat/belly band along the lower flank
d.path("M590,540 C640,580 720,624 820,650", "Belly band", fill=NONE,
       stroke="#C2B884", strokeWidth=26, opacity=35, cap="round")

# --- scutes ---------------------------------------------------------------------
def scute_path(cx, cy, w, h, k=0.28):
    """Rounded-square osteoderm; k = corner softness."""
    x0, x1, y0, y1 = cx - w/2, cx + w/2, cy - h/2, cy + h/2
    kx, ky = w*k, h*k
    return (f"M{x0+kx:.1f},{y0:.1f} L{x1-kx:.1f},{y0:.1f} Q{x1:.1f},{y0:.1f} {x1:.1f},{y0+ky:.1f} "
            f"L{x1:.1f},{y1-ky:.1f} Q{x1:.1f},{y1:.1f} {x1-kx:.1f},{y1:.1f} "
            f"L{x0+kx:.1f},{y1:.1f} Q{x0:.1f},{y1:.1f} {x0:.1f},{y1-ky:.1f} "
            f"L{x0:.1f},{y0+ky:.1f} Q{x0:.1f},{y0:.1f} {x0+kx:.1f},{y0:.1f} Z")

def back_y(x):
    """Approximate top contour of the body path (for scute placement)."""
    if x <= 702:
        return 398 + (702 - x) * 0.20
    return 398 + (x - 702) * 0.16

# flank scute rows, each row clamped inside the body edge and disc
n = 0
for ri, (y, w, h) in enumerate([(440, 26, 20), (464, 28, 22), (490, 30, 23), (517, 31, 24),
                                (545, 32, 24), (573, 32, 24)]):
    x_end = chord_x(y, rr)[1] - w*0.6
    x = 704 + (ri % 2) * (w/2 + 2)
    while x <= x_end:
        if y - h/2 > back_y(x) + 5:
            n += 1
            ww = w * (0.9 + 0.2 * ((n * 7) % 5) / 4)
            d.path(scute_path(x, y, ww, h, 0.38), f"Flank scute {n}",
                   fill=SCUTE_A if (ri + n) % 3 else SCUTE_B, stroke="#38361A", strokeWidth=2.5)
            d.path(f"M{x-ww*0.22:.0f},{y-h*0.14:.0f} L{x+ww*0.22:.0f},{y-h*0.14:.0f}",
                   f"Flank scute keel {n}", fill=NONE, stroke="#D2C990", strokeWidth=2.5,
                   opacity=45, cap="round")
        x += w + 3
# soft shadow pooling toward the belly so the rows read as a rounded flank
d.path("M690,560 C760,580 830,600 880,610", "Flank shade", fill=NONE,
       stroke="#2C2A12", strokeWidth=30, opacity=22, cap="round")
# dorsal crest: keeled ridges standing on the back contour (nuchal pair first)
for i, (x, h) in enumerate([(676, 20), (708, 26), (742, 22), (780, 18), (814, 18),
                            (848, 17), (882, 15)]):
    yb = back_y(x) + 4
    d.path(f"M{x-16},{yb+2} C{x-12},{yb-h*0.7:.0f} {x-4},{yb-h} {x+2},{yb-h} "
           f"C{x+8},{yb-h} {x+14},{yb-h*0.6:.0f} {x+16},{yb+2} Z",
           f"Dorsal scute {i+1}", fill=SCUTE_A, stroke=INK, strokeWidth=4)
    d.path(f"M{x-8},{yb-h*0.55:.0f} C{x-4},{yb-h*0.85:.0f} {x+2},{yb-h*0.9:.0f} {x+6},{yb-h*0.7:.0f}",
           f"Dorsal scute light {i+1}", fill=NONE, stroke="#E2D9A2", strokeWidth=3, opacity=45, cap="round")
d.path("M600,418 C650,392 720,392 800,404", "Back ridge light", fill=NONE,
       stroke="#E8DFA8", strokeWidth=6, opacity=22, cap="round")

# --- lower jaw (under the upper jaw) -------------------------------------------------
d.path("M152,488 C210,490 310,488 420,490 C520,492 600,502 652,514 "
       "C676,532 664,556 632,560 C560,552 460,526 360,518 "
       "C280,512 214,514 172,514 C150,512 142,500 152,488 Z",
       "Lower jaw", fill=JAW_GRAD, stroke=INK, strokeWidth=6)
d.path("M190,508 C280,506 380,512 470,522 C540,530 590,542 630,552", "Lower jaw shade",
       fill=NONE, stroke="#5E5730", strokeWidth=7, opacity=35, cap="round")

# --- upper jaw + skull --------------------------------------------------------------
d.path("M140,470 C140,448 158,438 186,440 C232,446 300,452 380,450 "
       "C460,448 520,440 558,422 C576,400 590,380 612,378 "
       "C640,376 664,388 694,396 C706,424 704,462 684,494 "
       "C668,506 652,508 640,508 C560,494 400,486 300,486 "
       "C230,486 190,490 162,492 C146,490 140,482 140,470 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# top light along the snout, skull table shading, cheek muscle shade
d.path("M190,446 C260,452 360,456 460,452 C510,448 540,440 560,428", "Snout light",
       fill=NONE, stroke="#E2D9A0", strokeWidth=6, opacity=35, cap="round")
d.path("M560,470 C600,486 640,494 676,488", "Cheek shade", fill=NONE,
       stroke="#3C3A1B", strokeWidth=12, opacity=30, cap="round")
d.path("M640,400 C664,410 684,420 692,436", "Skull edge shade", fill=NONE,
       stroke="#3C3A1B", strokeWidth=8, opacity=30, cap="round")
# fine scale wrinkles across the snout
for i, x in enumerate(range(250, 540, 36)):
    d.path(f"M{x},{456 if x < 460 else 448} C{x+4},{464} {x+4},{474} {x},{482}",
           f"Snout wrinkle {i+1}", fill=NONE, stroke="#4C4A24", strokeWidth=2, opacity=35, cap="round")
# skull bumps behind the eye
for i, (x, y, w) in enumerate([(632, 400, 14), (654, 408, 12), (620, 420, 10), (666, 428, 11)]):
    d.shape("ellipse", f"Skull bump {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#C3B97F", opacity=30, stroke=NONE)

# --- interdigitating teeth along the jaw seam ------------------------------------------
def seam_y(x):
    return 488 if x <= 420 else 488 + (x - 420) / 220 * 18

for i, x in enumerate(range(168, 600, 24)):
    lean = max(0, (260 - x) / 260) * 8          # front teeth splay forward
    y = seam_y(x)
    d.path(f"M{x-4:.0f},{y-3:.0f} L{x+4:.0f},{y-3:.0f} L{x - lean:.0f},{y+15:.0f} Z",
           f"Upper tooth {i+1}", fill=TOOTH_GRAD, stroke=INK, strokeWidth=2)
for i, x in enumerate(range(180, 590, 24)):
    lean = max(0, (260 - x) / 260) * 8
    y = seam_y(x)
    d.path(f"M{x-4:.0f},{y+5:.0f} L{x+4:.0f},{y+5:.0f} L{x - lean:.0f},{y-13:.0f} Z",
           f"Lower tooth {i+1}", fill=TOOTH_GRAD, stroke=INK, strokeWidth=2)

# --- the ghara: the male's pot-shaped nasal boss --------------------------------------
# pot-shaped, swelling straight out of the snout tip (base flares into the jaw)
d.path("M140,466 C136,440 146,414 166,404 C186,394 214,398 228,414 "
       "C238,426 240,440 248,448 C258,454 262,456 256,458 "
       "C230,460 190,462 160,470 Z",
       "Ghara", fill=GHARA_GRAD, stroke=INK, strokeWidth=6)
d.path("M156,420 C166,406 184,400 200,401", "Ghara light", fill=NONE,
       stroke="#EEE4B4", strokeWidth=5, opacity=45, cap="round")
d.path("M196,402 C204,416 206,436 202,456", "Ghara lobe", fill=NONE,
       stroke="#3C3A1B", strokeWidth=3, opacity=45, cap="round")
d.path("M150,450 C170,456 200,456 236,452", "Ghara base shade", fill=NONE,
       stroke="#3C3A1B", strokeWidth=6, opacity=30, cap="round")
d.shape("ellipse", "Nostril", x=168, y=404, width=14, height=8, fill="#1E1A0C", opacity=75, stroke=NONE)

# --- periscope eye on top of the head -------------------------------------------------
d.path("M586,400 C590,374 608,362 626,366 C642,370 648,388 640,402 Z",
       "Eye turret", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Iris", x=598, y=376, width=34, height=24, fill=IRIS_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=612, y=377, width=7, height=22, fill="#100E06", stroke=NONE)
d.shape("ellipse", "Glint", x=604, y=380, width=6, height=5, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M594,382 C604,368 626,366 638,378", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M598,400 C610,404 626,404 636,398", "Lower lid", fill=NONE,
       stroke="#3C3A1B", strokeWidth=3, opacity=60, cap="round")

# --- river: translucent murk over the submerged flank, closed on the disc arc ---------
wl, wr = chord_x(WATER_Y, rr)
d.path(f"M{wl:.1f},{WATER_Y} L{wr:.1f},{WATER_Y} A{rr},{rr} 0 0 1 {wl:.1f},{WATER_Y} Z",
       "River", fill=WATER_GRAD, opacity=78, stroke=NONE)
# snout reflection broken by ripples
for i, (x0, x1, y, op) in enumerate([(150, 640, 594, 30), (170, 600, 612, 22), (200, 560, 630, 15)]):
    d.path(f"M{x0},{y} C{(2*x0+x1)/3:.0f},{y+4} {(x0+2*x1)/3:.0f},{y-4} {x1},{y}",
           f"Reflection {i+1}", fill=NONE, stroke="#2E2A14", strokeWidth=10 - i*2,
           opacity=op, cap="round")
# surface light + ripples, all well inside the chord
d.path(f"M{wl+6:.1f},{WATER_Y} L{wr-6:.1f},{WATER_Y}", "Waterline light", fill=NONE,
       stroke="#E6E2B8", strokeWidth=3, opacity=50, cap="round")
for i, (x, y, w) in enumerate([(230,660,90),(420,680,120),(640,660,100),(320,730,110),
                               (560,750,90),(720,710,70),(450,800,80),(260,600,60),(700,600,80)]):
    d.path(f"M{x},{y} C{x+w*0.3:.0f},{y-5} {x+w*0.7:.0f},{y-5} {x+w},{y}",
           f"Ripple {i+1}", fill=NONE, stroke="#D8D6A8", strokeWidth=3, opacity=28, cap="round")
# wake rings where the body meets the surface
d.shape("ellipse", "Wake ring", x=600, y=WATER_Y - 8, width=260, height=22,
        fill=NONE, stroke="#E6E2B8", strokeWidth=3, opacity=30)

# --- name ----------------------------------------------------------------------
d.text("GHARIAL", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E2DDBE", justify="center")

d.finish("gharial-V1R00")
