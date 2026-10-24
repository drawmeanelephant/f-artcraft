#!/usr/bin/env python3
"""Tufted deer — field-guide plate V1R00. The vampire deer: a delicate
charcoal-plum head, tall ears, a dark tuft falling over the forehead, two
tiny fangs below the lip. Dusk-dark plate, pale crescent moon, dead-bracken
band closing on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tufted Deer — Field Plate", 1000, 1000)

INK = "#1A0F16"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#160C18"}, {"offset": 1, "color": "#070408"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E3E58"}, {"offset": 0.6, "color": "#3C2640"},
    {"offset": 1, "color": "#20132A"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5A50"}, {"offset": 0.62, "color": "#4A3A34"},
    {"offset": 1, "color": "#2C221E"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "start": [0, 180], "end": [0, 380], "stops": [
    {"offset": 0, "color": "#5E4C44"}, {"offset": 1, "color": "#3A2C28"}]}}
MUZZLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54443C"}, {"offset": 1, "color": "#2E2420"}]}}
FANG_GRAD = {"gradient": {"kind": "linear", "start": [0, 640], "end": [0, 685], "stops": [
    {"offset": 0, "color": "#EDE3CC"}, {"offset": 1, "color": "#B8A67E"}]}}
BAND_GRAD = {"gradient": {"kind": "linear", "start": [0, 720], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#33203A"}, {"offset": 1, "color": "#1A0F20"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + dusk-dark plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5E3E58", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A1830", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8A6E90", strokeWidth=3, opacity=40)

# crescent moon, high left
d.shape("ellipse", "Moon haze", x=180, y=150, width=190, height=190,
        fill="#DCC6E4", opacity=10, stroke=NONE)
d.shape("ellipse", "Moon", x=215, y=185, width=120, height=120,
        fill="#E4D4EA", opacity=70, stroke=NONE)
d.shape("ellipse", "Moon bite", x=252, y=168, width=104, height=104,
        fill="#4A2E50", opacity=88, stroke=NONE)

# pale motes drifting in the dusk
for i, (x, y, w) in enumerate([(200,320,6),(760,240,6),(170,470,7),(830,440,6),(240,690,5),
                               (750,710,6),(150,560,5),(855,560,5),(400,110,5),(605,105,6),
                               (690,160,5),(335,805,5),(665,815,5)]):
    assert on_disc(x + w/2, y + w/2, 5), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#CBA8D4", opacity=40, stroke=NONE)
# thin cloud veils
for i, dd in enumerate(["M600,200 C680,185 760,190 820,205",
                        "M620,240 C690,228 760,232 810,244"]):
    d.path(dd, f"Cloud veil {i+1}", fill=NONE, stroke="#8A6E90",
           strokeWidth=9, opacity=22, cap="round")

# --- dead-bracken ground band, closing on the disc's own arc ----------------------
d.path("M194,748 C380,730 620,730 806,748 A420,420 0 0 1 194,748 Z",
       "Bracken band", fill=BAND_GRAD, stroke="#241428", strokeWidth=4)
for i, dd in enumerate(["M250,764 Q262,730 276,708", "M310,770 Q318,744 332,724",
                        "M694,768 Q686,738 672,716", "M742,762 Q734,734 720,714",
                        "M400,774 Q406,750 418,732", "M600,774 Q596,748 586,730"]):
    d.path(dd, f"Twig {i+1}", fill=NONE, stroke="#4A3250",
           strokeWidth=4, opacity=60, cap="round")

# --- ears: broad leaves angled out from the crown ----------------------------------
d.path("M402,360 C340,348 272,320 242,272 C228,250 238,230 262,232 "
       "C322,238 385,295 412,342 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path("M598,360 C660,348 728,320 758,272 C772,250 762,230 738,232 "
       "C678,238 615,295 588,342 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path("M392,348 C344,334 296,310 272,282 C304,290 358,318 398,340 Z",
       "Ear L inner", fill="#7A5560", opacity=45, stroke=NONE)
d.path("M608,348 C656,334 704,310 728,282 C696,290 642,318 602,340 Z",
       "Ear R inner", fill="#7A5560", opacity=45, stroke=NONE)

# slim neck tapering into the dusk, behind the jaw — a delicate bust
d.path("M445,610 C470,645 530,645 555,610 C575,690 585,745 575,795 "
       "C545,815 455,815 425,795 C415,745 425,690 445,610 Z",
       "Neck", fill=FUR_GRAD, opacity=45, stroke=NONE)

# --- head: delicate taper to the muzzle ---------------------------------------------
d.path("M500,320 C565,320 615,362 626,425 C636,485 622,552 588,608 "
       "C565,645 532,668 505,672 L495,672 C468,668 435,645 412,608 "
       "C378,552 364,485 374,425 C385,362 435,320 500,320 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# cheekbone light + taper shading down the muzzle
d.shape("ellipse", "Brow light", x=420, y=350, width=160, height=60,
        fill="#FFFFFF", opacity=10, stroke=NONE)
d.path("M438,560 C455,640 478,662 500,664 C522,662 545,640 562,560 "
       "C540,600 520,616 500,618 C480,616 460,600 438,560 Z",
       "Muzzle shade", fill=MUZZLE_GRAD, opacity=60, stroke=NONE)
# --- the tuft: dark forelock swept over the brow to a point --------------------------
d.path("M415,335 C450,295 520,282 572,302 C614,320 634,362 622,410 "
       "C614,440 600,464 580,482 C584,458 578,434 564,414 "
       "C560,442 550,464 534,478 C536,450 528,422 512,400 "
       "C500,424 484,436 466,440 C474,412 468,382 450,360 "
       "C436,348 424,340 415,335 Z",
       "Tuft main", fill="#241A1E", stroke=INK, strokeWidth=5)
d.path("M430,340 C418,372 424,410 446,434 C420,418 405,388 412,352 Z",
       "Tuft lock L", fill="#241A1E", stroke=INK, strokeWidth=4)
d.path("M450,342 C470,320 510,310 545,318", "Tuft sheen", fill=NONE,
       stroke="#4A3A44", strokeWidth=6, opacity=60, cap="round")

# --- face ---------------------------------------------------------------------------
# large dark eyes with a pale wet glint
d.shape("ellipse", "Eye L", x=398, y=470, width=36, height=42, fill="#140D10", stroke=NONE)
d.shape("ellipse", "Eye R", x=566, y=470, width=36, height=42, fill="#140D10", stroke=NONE)
d.shape("ellipse", "Eye ring L", x=394, y=466, width=44, height=50,
        fill=NONE, stroke="#6E5064", strokeWidth=2, opacity=50)
d.shape("ellipse", "Eye ring R", x=562, y=466, width=44, height=50,
        fill=NONE, stroke="#6E5064", strokeWidth=2, opacity=50)
d.shape("ellipse", "Glint L", x=406, y=478, width=9, height=9, fill="#F0E6F2", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=574, y=478, width=9, height=9, fill="#F0E6F2", opacity=90, stroke=NONE)
d.path("M390,462 C406,452 428,452 442,462", "Lid L", fill=NONE,
       stroke="#2A1E18", strokeWidth=5, cap="round")
d.path("M558,462 C574,452 596,452 610,462", "Lid R", fill=NONE,
       stroke="#2A1E18", strokeWidth=5, cap="round")

# small dark nose + mouth line
d.path("M482,622 C482,610 518,610 518,622 C518,636 508,644 500,644 "
       "C492,644 482,636 482,622 Z",
       "Nose", fill="#161014", stroke=NONE)
d.path("M500,644 C500,652 500,656 500,660 M500,660 C488,668 472,668 464,662 "
       "M500,660 C512,668 528,668 536,662",
       "Mouth", fill=NONE, stroke="#161014", strokeWidth=4, cap="round")

# the two tiny fangs below the lip
d.path("M452,652 L470,652 L463,682 C458,674 454,664 452,652 Z",
       "Fang L", fill=FANG_GRAD, stroke=INK, strokeWidth=3)
d.path("M548,652 L530,652 L537,682 C542,674 546,664 548,652 Z",
       "Fang R", fill=FANG_GRAD, stroke=INK, strokeWidth=3)

# --- name -----------------------------------------------------------------------------
d.text("TUFTED DEER", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DCC6DC", justify="center")

d.finish("tufted-deer-V1R00")
