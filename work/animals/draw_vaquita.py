#!/usr/bin/env python3
"""Vaquita — field-guide plate V1R00. Full-body profile of the tiny porpoise,
gliding right under soft light rays: pale grey body, tall triangular dorsal
fin, dark eye-ring and the dark lip "smile". Sea-green plate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Vaquita — Field Plate", 1000, 1000)

INK = "#2E3A3E"   # slate, not black
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#0F2A2C"}, {"offset": 1, "color": "#051214"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E2F2EA"}, {"offset": 0.7, "color": "#AAD5C3"},
    {"offset": 1, "color": "#74A895"}]}}
SAND_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#C9CFAE"}, {"offset": 1, "color": "#8E9878"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#6F7E86"}, {"offset": 0.45, "color": "#AEBCC1"},
    {"offset": 1, "color": "#EEF3F2"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#5E6C74"}, {"offset": 1, "color": "#8E9CA3"}]}}
FLUKE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E6C74"}, {"offset": 1, "color": "#94A2A8"}]}}
RAY_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#FFFFFF", "opacity": 0.30}, {"offset": 1, "color": "#FFFFFF", "opacity": 0}]}}
RING_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A464C"}, {"offset": 1, "color": "#1E272B"}]}}

# --- backdrop + plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E8576", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEF8F3", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=180, width=220, height=130, fill="#8FC2AE", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=600, width=220, height=120, fill="#8FC2AE", opacity=18, stroke=NONE)
# light rays slanting down from the surface: tops ride the disc's arc, bottoms tuck under the sand
import math
def rim_y(x):
    return 460 - math.sqrt(420**2 - (x - 500)**2)
for i, (x0, x1, b0, b1, o) in enumerate([(380, 420, 450, 540, 70), (470, 520, 560, 660, 60),
                                         (560, 590, 650, 730, 50)]):
    d.path(f"M{x0},{rim_y(x0):.1f} A420,420 0 0 1 {x1},{rim_y(x1):.1f} L{b1},778 L{b0},778 Z",
           f"Light ray {i+1}", fill=RAY_GRAD, opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(250,320,8),(760,250,7),(180,520,7),(820,420,8),(410,120,7),
                               (610,118,8),(300,700,6),(700,710,6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#5F9483", opacity=35, stroke=NONE)

# --- sandy shallows: closes on the disc's own arc ----------------------------------------
d.path("M217,770 C380,752 620,752 783,770 A420,420 0 0 1 217,770 Z",
       "Sand", fill=SAND_GRAD, stroke=NONE)
d.path("M236,768 C390,752 610,752 764,768", "Sand light", fill=NONE,
       stroke="#EEF1DC", strokeWidth=4, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(320,800,26),(470,792,18),(610,806,22),(400,836,14),(560,840,16)]):
    d.shape("ellipse", f"Ripple {i+1}", x=x, y=y, width=w*2, height=w/3,
            fill="#7C8667", opacity=30, stroke=NONE)
# eelgrass rising from the sand
for i, (x, h, lean) in enumerate([(258,120,-14),(276,90,8),(722,110,12),(742,80,-8),(704,70,6)]):
    d.path(f"M{x},776 C{x+lean},{776-h*0.4} {x-lean},{776-h*0.7} {x+lean},{776-h}",
           f"Eelgrass {i+1}", fill=NONE, stroke="#5E8C5C", strokeWidth=6, opacity=60, cap="round")
# re-stroke the rim over the sand so the plate edge stays continuous
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#4E8576", strokeWidth=6)
d.shape("ellipse", "Plate inner ring over sand", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEF8F3", strokeWidth=3, opacity=40)
d.shape("ellipse", "Vaquita shadow", x=300, y=760, width=400, height=24, fill="#4E5A44", opacity=25, stroke=NONE)

# --- flukes (behind the tail stock) ---------------------------------------------------------
# porpoise flukes are horizontal: in profile they read as two slim blades, far one raised
d.path("M240,462 C216,448 186,432 154,426 C168,448 200,464 240,470 Z",
       "Fluke far", fill="#5E6C74", stroke=INK, strokeWidth=4, opacity=85)
d.path("M240,466 C212,468 180,474 146,488 C176,496 212,488 240,478 Z",
       "Fluke near", fill=FLUKE_GRAD, stroke=INK, strokeWidth=5)

# --- far pectoral flipper, peeking below the belly ------------------------------------------
d.path("M628,540 C614,566 598,584 576,594 C588,570 598,550 602,536 Z",
       "Flipper far", fill="#5E6C74", opacity=70, stroke=NONE)

# --- dorsal fin: proportionally tall, triangular ---------------------------------------------
d.path("M458,394 C488,356 510,322 534,296 C548,326 558,360 568,380 Z",
       "Dorsal fin", fill=FIN_GRAD, stroke=INK, strokeWidth=6)
d.path("M482,378 C502,352 518,330 532,310", "Dorsal sheen", fill=NONE,
       stroke="#DDE6E8", strokeWidth=4, opacity=35, cap="round")

# --- body: stocky, blunt-headed, tapering to the tail stock ------------------------------------
d.path("M776,482 C778,430 742,392 680,378 C600,362 482,366 402,392 "
       "C340,412 290,436 236,458 L236,474 "
       "C286,490 340,520 414,540 C502,562 624,560 696,538 "
       "C748,522 774,508 776,482 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# countershading + sheen
d.path("M420,530 C510,552 624,550 696,532 C640,542 520,544 420,530 Z",
       "Belly glow", fill="#FFFFFF", opacity=30, stroke=NONE)
d.path("M690,390 C620,374 500,378 410,402", "Back sheen", fill=NONE,
       stroke="#E6EEF0", strokeWidth=7, opacity=35, cap="round")
d.path("M400,412 C340,432 300,448 252,466", "Stock sheen", fill=NONE,
       stroke="#E6EEF0", strokeWidth=4, opacity=25, cap="round")
d.shape("ellipse", "Melon light", x=704, y=400, width=58, height=32, fill="#FFFFFF", opacity=22, stroke=NONE)

# --- identity markings: dark lip patch, mouth-to-flipper line, eye-ring ---------------------------
# the smile: a dark lip patch that curves up toward the eye
d.path("M777,482 C774,502 754,516 722,514 C704,513 692,505 690,494 "
       "C710,502 732,502 748,497 C762,492 772,487 777,482 Z",
       "Lip patch", fill=RING_GRAD, stroke=NONE)
d.path("M775,486 C758,500 728,504 700,494", "Mouth line", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M700,494 C694,491 690,486 688,480", "Smile tick", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M716,514 C694,522 672,530 652,536", "Chin line", fill=NONE,
       stroke="#3A464C", strokeWidth=5, opacity=55, cap="round")
# eye-ring: the vaquita's dark "mascara"
d.path("M706,460 C710,444 732,438 748,446 C760,452 760,468 746,474 "
       "C730,480 704,476 706,460 Z", "Eye ring", fill=RING_GRAD, stroke=NONE, opacity=92)
d.shape("ellipse", "Eye", x=724, y=452, width=13, height=12, fill="#0E1416", stroke=NONE)
d.shape("ellipse", "Eye glint", x=727, y=454, width=5, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M712,442 C724,434 740,434 752,440", "Brow light", fill=NONE,
       stroke="#E6EEF0", strokeWidth=3, opacity=40, cap="round")

# --- near pectoral flipper -------------------------------------------------------------------
d.path("M664,526 C656,560 640,586 614,602 C610,578 620,550 632,532 Z",
       "Flipper near", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M652,534 C646,556 636,576 622,590", "Flipper sheen", fill=NONE,
       stroke="#DDE6E8", strokeWidth=3, opacity=35, cap="round")

# --- a few bubbles trailing from the blowhole -----------------------------------------------
for i, (x, y, w) in enumerate([(676,350,12),(690,314,9),(678,280,14),(694,240,8),(682,204,11)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=22, stroke="#FFFFFF", strokeWidth=1.5)

# --- name ----------------------------------------------------------------------------------
d.text("VAQUITA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#D6ECE2", justify="center")

d.finish("vaquita-V1R00")
