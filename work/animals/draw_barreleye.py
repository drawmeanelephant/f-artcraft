#!/usr/bin/env python3
"""Barreleye — field-guide plate V1R00. Front-on: the transparent dome for a
head, two green barrel eyes floating loose inside the skull, dark mouth and
nares below, body tapering into the void. Deep-sea teal glow on near-black.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Barreleye — Field Plate", 1000, 1000)

INK = "#02100F"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#030A0E"}, {"offset": 1, "color": "#010203"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#12424A"}, {"offset": 0.6, "color": "#0A262E"},
    {"offset": 1, "color": "#040E14"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#16323A"}, {"offset": 0.6, "color": "#0C1E24"},
    {"offset": 1, "color": "#050D10"}]}}
DOME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A8A92"}, {"offset": 0.7, "color": "#1E565E"},
    {"offset": 1, "color": "#0E3238"}]}}
EYE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8F07E"}, {"offset": 0.55, "color": "#55C460"},
    {"offset": 1, "color": "#177A3E"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "start": [0, 560], "end": [0, 720], "stops": [
    {"offset": 0, "color": "#1E4A52"}, {"offset": 1, "color": "#0A1E24"}]}}
SILT_GRAD = {"gradient": {"kind": "linear", "start": [0, 720], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#0E2A30"}, {"offset": 1, "color": "#041014"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + near-void teal plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo outer", x=54, y=14, width=892, height=892,
        fill="#12424A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A2A30", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#2E6A72", strokeWidth=3, opacity=40)

# marine snow drifting down through the glow
for i, (x, y, w) in enumerate([(210,300,6),(770,250,5),(180,470,7),(830,450,6),(250,690,5),
                               (760,710,6),(160,560,4),(845,580,5),(410,110,5),(610,105,5),
                               (320,160,4),(700,170,5),(340,810,4),(670,820,5),(505,95,4),
                               (280,390,4),(735,340,4),(460,180,4)]):
    assert on_disc(x + w/2, y + w/2, 5), (x, y)
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#9AD4DC", opacity=45, stroke=NONE)
# faint bioluminescent pinpricks
for i, (x, y) in enumerate([(300,250),(725,290),(215,610),(790,640),(555,140),(375,745)]):
    d.shape("ellipse", f"Glow speck {i+1}", x=x, y=y, width=5, height=5,
            fill="#7EF0C8", opacity=60, stroke=NONE)

# --- abyssal silt band, closing on the disc's own arc -------------------------------
d.path("M194,748 C380,730 620,730 806,748 A420,420 0 0 1 194,748 Z",
       "Silt band", fill=SILT_GRAD, stroke="#08222A", strokeWidth=4)
d.path("M250,764 Q270,742 296,728", "Silt wisp L", fill=NONE,
       stroke="#1E4A52", strokeWidth=4, opacity=50, cap="round")
d.path("M750,766 Q730,742 704,726", "Silt wisp R", fill=NONE,
       stroke="#1E4A52", strokeWidth=4, opacity=50, cap="round")

# --- body: dark mass below and behind the dome, tapering into the void ---------------
d.path("M500,520 C600,520 668,565 690,640 C705,695 690,745 655,775 "
       "C610,810 550,822 500,822 C450,822 390,810 345,775 "
       "C310,745 295,695 310,640 C332,565 400,520 500,520 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# pectoral fins, small and translucent at the flanks
d.path("M318,640 C275,660 250,700 252,745 C290,735 322,705 335,668 Z",
       "Fin L", fill=FIN_GRAD, opacity=75, stroke=INK, strokeWidth=4)
d.path("M682,640 C725,660 750,700 748,745 C710,735 678,705 665,668 Z",
       "Fin R", fill=FIN_GRAD, opacity=75, stroke=INK, strokeWidth=4)
# body shading: faint flank sheen + belly falloff
d.shape("ellipse", "Flank sheen", x=360, y=560, width=280, height=90,
        fill="#3A8A92", opacity=14, stroke=NONE)
d.path("M360,760 C430,790 570,790 640,760 C600,800 540,815 500,815 "
       "C460,815 400,800 360,760 Z",
       "Belly shade", fill="#020B0D", opacity=40, stroke=NONE)

# --- mouth + nares under the dome ----------------------------------------------------
d.path("M455,600 C480,612 520,612 545,600", "Mouth", fill=NONE,
       stroke="#020B0D", strokeWidth=6, cap="round")
d.shape("ellipse", "Nare L", x=466, y=566, width=14, height=18, fill="#02100F", stroke=NONE)
d.shape("ellipse", "Nare R", x=520, y=566, width=14, height=18, fill="#02100F", stroke=NONE)

# --- the dome: the barrel eyes first, then the glass over them -----------------------
# dark interior mass inside the dome behind the eyes
d.shape("ellipse", "Skull interior", x=330, y=225, width=340, height=330,
        fill="#07191D", opacity=85, stroke=NONE)
# faint teal glow inside the dome behind the eyes
d.shape("ellipse", "Interior glow", x=370, y=265, width=260, height=250,
        fill="#1E565E", opacity=35, stroke=NONE)
# the two green barrel eyes, aimed up inside the dome
d.shape("ellipse", "Barrel eye L", x=415, y=300, width=72, height=150,
        fill=EYE_GRAD, stroke="#0A3A24", strokeWidth=4)
d.shape("ellipse", "Barrel eye R", x=513, y=300, width=72, height=150,
        fill=EYE_GRAD, stroke="#0A3A24", strokeWidth=4)
# barrel openings: dark rims at the top of each eye + retinal glint
d.shape("ellipse", "Barrel rim L", x=425, y=308, width=52, height=34,
        fill="#0E5A30", stroke="#062418", strokeWidth=3)
d.shape("ellipse", "Barrel rim R", x=523, y=308, width=52, height=34,
        fill="#0E5A30", stroke="#062418", strokeWidth=3)
d.shape("ellipse", "Retina L", x=435, y=314, width=30, height=20,
        fill="#BFFBC8", opacity=85, stroke=NONE)
d.shape("ellipse", "Retina R", x=535, y=314, width=30, height=20,
        fill="#BFFBC8", opacity=85, stroke=NONE)
# lower glow pooling in each barrel
d.shape("ellipse", "Eye base L", x=428, y=415, width=46, height=30,
        fill="#8FE86A", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye base R", x=526, y=415, width=46, height=30,
        fill="#8FE86A", opacity=30, stroke=NONE)

# the transparent dome itself, over everything it contains
d.shape("ellipse", "Dome", x=315, y=205, width=370, height=360,
        fill=DOME_GRAD, opacity=22, stroke="#7ED8DE", strokeWidth=5)
# glassy speculars on the dome
d.path("M365,290 C395,245 450,222 505,220", "Dome glare L", fill=NONE,
       stroke="#D8F6F8", strokeWidth=10, opacity=55, cap="round")
d.path("M622,300 C640,335 645,380 635,420", "Dome glare R", fill=NONE,
       stroke="#BEEEF2", strokeWidth=7, opacity=35, cap="round")
d.path("M370,470 C390,505 430,530 480,540", "Dome glare low", fill=NONE,
       stroke="#9AD4DC", strokeWidth=6, opacity=25, cap="round")
# dome seam where the transparency meets the skull base
d.path("M340,520 C420,560 580,560 660,520", "Dome seam", fill=NONE,
       stroke="#4AA8B0", strokeWidth=4, opacity=40, cap="round")

# --- name -----------------------------------------------------------------------------
d.text("BARRELEYE", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#BFE8E8", justify="center")

d.finish("barreleye-V1R00")
