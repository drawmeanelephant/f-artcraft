#!/usr/bin/env python3
"""Drift Lapel — mascot portrait V1R00.
A mascot in a navy blazer, a small warm head above the collar. One lapel
carries a column of accreted pins; a heavy lanyard drops to a glowing access
badge. Behind it a door stands ajar, light already through — the badge swipes
doors its wearer never approached. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Drift Lapel — Mascot Portrait", 1000, 1000)

INK = "#241A18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1626"}, {"offset": 1, "color": "#0B080F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9A8468"}, {"offset": 0.7, "color": "#6E5C44"},
    {"offset": 1, "color": "#3A2E20"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4030"}, {"offset": 1, "color": "#201812"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2438"}, {"offset": 1, "color": "#191220"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFD2AE"}, {"offset": 0.72, "color": "#D4AB82"},
    {"offset": 1, "color": "#B08155"}]}}
BLAZER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38466A"}, {"offset": 1, "color": "#1E2740"}]}}
LAPEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#45547E"}, {"offset": 1, "color": "#2A3556"}]}}
BADGE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4DC9A"}, {"offset": 0.75, "color": "#D9B25E"},
    {"offset": 1, "color": "#A87E36"}]}}
LIGHT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4D894"}, {"offset": 1, "color": "#C89B4E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A8906A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EADFC2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4A34", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120C08",
       strokeWidth=4, opacity=70)

# --- the door, ajar, upper left -------------------------------------------------
# light spilling through the gap first, so the slab sits on it
d.shape("ellipse", "Door light pool", x=150, y=676, width=230, height=30,
        fill="#F0CE8A", opacity=20, stroke=NONE)
d.path("M252,240 L322,240 L322,680 L252,680 Z", "Door gap light",
       fill=LIGHT_GRAD, stroke=NONE, opacity=85)
d.path("M252,240 L296,258 L296,662 L252,680 Z", "Door light fold",
       fill="#FFF2CC", opacity=35, stroke=NONE)
# the slab itself, swung open toward us
d.path("M252,240 L196,266 L196,652 L252,680 Z", "Door slab",
       fill=DOOR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Door knob", x=206, y=452, width=10, height=10,
        fill="#C8A45E", stroke=INK, strokeWidth=2.5)
# swipe reader on the jamb, woken by the badge
d.shape("rectangle", "Reader", x=330, y=430, width=18, height=30,
        fill="#2A2030", stroke=INK, strokeWidth=3, radius=4)
d.shape("ellipse", "Reader light", x=335, y=437, width=8, height=8,
        fill="#7AE08A", stroke=NONE)
d.path("M356,432 C366,440 366,454 356,462 M368,424 C384,438 384,468 368,482",
       "Swipe waves", fill=NONE, stroke="#8AE89A", strokeWidth=4,
       cap="round", opacity=70)

# --- the mascot: a small head over a very authoritative blazer -------------------
d.shape("ellipse", "Mascot halo", x=330, y=270, width=400, height=460,
        fill="#F0D089", opacity=8, stroke=NONE)
d.shape("ellipse", "Mascot shadow", x=370, y=688, width=300, height=24,
        fill="#0E0806", opacity=45, stroke=NONE)

# blazer body: broad shoulders tapering to the floor
d.path("M370,695 C366,600 372,512 408,462 C436,426 564,426 592,462 "
       "C628,512 634,600 630,695 Z", "Blazer", fill=BLAZER_GRAD,
       stroke=INK, strokeWidth=6)
# sleeve seams
d.path("M404,480 C392,540 388,620 390,680 M596,480 C608,540 612,620 610,680",
       "Sleeve seams", fill=NONE, stroke="#141C30", strokeWidth=4, opacity=75)
# shoulder sheen
d.shape("ellipse", "Shoulder sheen", x=408, y=448, width=120, height=40,
        fill="#FFFFFF", opacity=12, stroke=NONE)

# shirt V under the lapels + tie
d.path("M462,442 L538,442 L500,556 Z", "Shirt V", fill="#E4DCCA",
       stroke=INK, strokeWidth=4)
d.path("M491,452 L509,452 L514,470 L500,545 L486,470 Z", "Tie",
       fill="#7E2F34", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Tie knot", x=489, y=441, width=22, height=17,
        fill="#944044", stroke=INK, strokeWidth=3.5)

# lapels: folded back from the shirt V
d.path("M408,462 C428,478 452,520 476,566 L428,600 C408,556 396,506 396,478 Z",
       "Left lapel", fill=LAPEL_GRAD, stroke=INK, strokeWidth=5)
d.path("M592,462 C572,478 548,520 524,566 L572,600 C592,556 604,506 604,478 Z",
       "Right lapel", fill=LAPEL_GRAD, stroke=INK, strokeWidth=5)
d.path("M412,470 C428,486 446,516 464,550", "Left lapel crease",
       fill=NONE, stroke="#5E6E9E", strokeWidth=3, opacity=60)
d.path("M588,470 C572,486 554,516 536,550", "Right lapel crease",
       fill=NONE, stroke="#5E6E9E", strokeWidth=3, opacity=60)

# the accreted pins climbing the left lapel — one per survived migration
for i, (x, y, w, c) in enumerate([(414,486,9,"#E8B84A"),(420,506,8,"#C8C0B0"),
                                  (427,526,9,"#E8B84A"),(434,546,7,"#B8734A"),
                                  (441,562,8,"#E8B84A"),(449,578,7,"#C8C0B0"),
                                  (457,592,8,"#E8B84A")]):
    d.shape("ellipse", f"Pin {i+1}", x=x, y=y, width=w, height=w,
            fill=c, stroke=INK, strokeWidth=1.8)
d.path("M410,478 L422,478 M416,472 L416,484", "Newest pin sparkle",
       fill=NONE, stroke="#FFF0C0", strokeWidth=2.5, cap="round", opacity=85)

# connector ring where the lanyard meets the badge
d.shape("ellipse", "Badge ring", x=490, y=556, width=20, height=20,
        fill=NONE, stroke="#5E2A30", strokeWidth=7)

# --- heavy lanyard + the access badge ---------------------------------------------
# thick ribbon around the neck, dropping to the badge over the lapels
d.path("M452,438 C468,472 478,528 484,570", "Lanyard left", fill=NONE,
       stroke="#5E2A30", strokeWidth=17, cap="round")
d.path("M548,438 C532,472 522,528 516,570", "Lanyard right", fill=NONE,
       stroke="#5E2A30", strokeWidth=17, cap="round")
d.path("M452,438 C468,472 478,528 484,570", "Lanyard sheen L", fill=NONE,
       stroke="#8A4450", strokeWidth=4, cap="round", opacity=70)
d.path("M548,438 C532,472 522,528 516,570", "Lanyard sheen R", fill=NONE,
       stroke="#8A4450", strokeWidth=4, cap="round", opacity=70)

# badge glow + the badge itself
d.shape("ellipse", "Badge glow", x=430, y=548, width=140, height=140,
        fill="#F0D089", opacity=22, stroke=NONE)
d.shape("rectangle", "Badge", x=452, y=568, width=96, height=112,
        fill=BADGE_GRAD, stroke=INK, strokeWidth=5, radius=10)
d.path("M452,588 L548,588", "Badge stripe", fill=NONE, stroke="#7A5A24",
       strokeWidth=5, opacity=80)
d.shape("ellipse", "Badge photo", x=478, y=602, width=44, height=44,
        fill="#8A6E3E", stroke=INK, strokeWidth=3)
d.path("M489,636 C489,624 511,624 511,636 M500,610 C506,610 510,615 510,621 "
       "C510,627 506,631 500,631 C494,631 490,627 490,621 C490,615 494,610 500,610",
       "Badge silhouette", fill=NONE, stroke="#3A2C14", strokeWidth=4,
       cap="round")
d.text("ACCESS", "Badge label", x=500, y=666, size=13, font="Virelai Sans",
       color="#3A2C14", justify="center")

# --- head above the collar: quiet, credentialled ----------------------------------
d.shape("ellipse", "Head", x=438, y=330, width=124, height=118,
        fill=HEAD_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Head sheen", x=456, y=342, width=46, height=26,
        fill="#FFFFFF", opacity=18, stroke=NONE)
# calm, knowing eyes — the face of attire that has read the room
d.path("M462,398 C470,392 480,392 488,398 M512,398 C520,392 530,392 538,398",
       "Eyes", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M488,424 C496,428 504,428 512,424", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")

# --- dust motes in the door light ---------------------------------------------------
for i, (x, y, w) in enumerate([(268,320,5),(288,420,4),(260,540,5),(300,560,4),
                               (240,380,4),(350,470,5),(620,300,5),(680,380,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0DCAE", opacity=45, stroke=NONE)

# --- captions -----------------------------------------------------------------------
d.text("DRIFT LAPEL", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#EFE4CC", justify="center")
r = d.text("THE DOORS OPEN EITHER WAY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4AE88", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("259.drift-lapel-V1R00")
