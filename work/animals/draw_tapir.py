#!/usr/bin/env python3
"""Tapir — field-guide plate V1R00. Malayan tapir, full-body profile facing
left: the black-and-white saddle is the composition, the drooping prehensile
snout the signature. Night-jungle palette, misty sage plate.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tapir — Field Plate", 1000, 1000)

INK = "#1F2027"
CX, CY, R = 500, 460, 420          # plate disc
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2E26"}, {"offset": 1, "color": "#09110D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6ECDD"}, {"offset": 0.7, "color": "#C2CFB7"},
    {"offset": 1, "color": "#8D9E84"}]}}
GROUND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E9070"}, {"offset": 1, "color": "#56684C"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#50525F"}, {"offset": 0.65, "color": "#2D2E37"},
    {"offset": 1, "color": "#18181E"}]}}
FUR_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26272E"}, {"offset": 1, "color": "#141418"}]}}
SADDLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FCFAF4"}, {"offset": 0.68, "color": "#E4DFD3"},
    {"offset": 1, "color": "#B7B1A3"}]}}
SNOUT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#454752"}, {"offset": 1, "color": "#22232A"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9BB08C"}, {"offset": 1, "color": "#6E8462"}]}}

def chord_x(y, r):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7058", strokeWidth=6)
d.shape("ellipse", "Patina 1", x=170, y=170, width=240, height=140, fill="#A7B79C", opacity=10, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=200, width=230, height=130, fill="#A7B79C", opacity=10, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,8),(770,250,7),(160,520,9),(840,520,8),(140,420,6),
                               (860,400,7),(400,120,7),(600,115,8),(300,200,6),(700,180,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#6F8266", opacity=40, stroke=NONE)

# misty jungle leaves behind the animal (all well inside the disc)
def leaf(cx, cy, L, W, deg, label, op):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    def P(u, v): return (cx + u*c - v*s, cy + u*s + v*c)
    a, b = P(-L/2, 0), P(L/2, 0)
    c1, c2 = P(-L/6, -W), P(L/4, -W*0.8)
    c3, c4 = P(L/4, W*0.8), P(-L/6, W)
    d.path("M%.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f C%.0f,%.0f %.0f,%.0f %.0f,%.0f Z" % (
        *a, *c1, *c2, *b, *c3, *c4, *a), label, fill=LEAF_GRAD, stroke=NONE, opacity=op)
    m1, m2 = P(-L/2 + 10, 0), P(L/2 - 14, 0)
    d.path("M%.0f,%.0f L%.0f,%.0f" % (*m1, *m2), f"{label} vein", fill=NONE,
           stroke="#E6ECDD", strokeWidth=3, opacity=op, cap="round")

for i, (x, y, L, W, deg, op) in enumerate([
        (215, 330, 190, 46, -60, 38), (270, 250, 170, 40, -35, 30), (190, 450, 150, 36, -95, 28),
        (790, 320, 190, 46, -120, 38), (730, 240, 170, 40, -145, 30), (815, 450, 150, 36, -85, 28)]):
    leaf(x, y, L, W, deg, f"Leaf {i+1}", op)
# fireflies
for i, (x, y, w) in enumerate([(360,190,10),(640,160,8),(560,250,7),(430,300,6),(700,330,9)]):
    d.shape("ellipse", f"Firefly glow {i+1}", x=x - w, y=y - w, width=w*3, height=w*3,
            fill="#F4E9A2", opacity=18, stroke=NONE)
    d.shape("ellipse", f"Firefly {i+1}", x=x, y=y, width=w, height=w, fill="#FFF6C4", opacity=80, stroke=NONE)

# forest floor: wavy top, closed on the disc's own arc so it cannot leak
gy = 742
xl, xr = chord_x(gy, R)
d.path(f"M{xl:.1f},{gy} C330,722 420,752 520,736 C620,722 720,748 {xr:.1f},{gy} "
       f"A{R},{R} 0 0 1 {xl:.1f},{gy} Z",
       "Forest floor", fill=GROUND_GRAD, stroke=NONE, opacity=85)
d.path("M260,762 C360,752 460,770 560,760 C640,752 700,764 760,758", "Floor light",
       fill=NONE, stroke="#B9C9AA", strokeWidth=5, opacity=30, cap="round")
# grass tufts on the floor
for i, (x, y) in enumerate([(240,748),(300,740),(800,745),(740,738),(560,734)]):
    d.path(f"M{x},{y} Q{x-6},{y-26} {x-16},{y-40} M{x+4},{y} Q{x+6},{y-30} {x+2},{y-48} "
           f"M{x+8},{y} Q{x+16},{y-22} {x+28},{y-34}", f"Grass {i+1}",
           fill=NONE, stroke="#53664A", strokeWidth=4, opacity=70, cap="round")
# re-ink the rim over the floor
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#5E7058", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F5EC", strokeWidth=3, opacity=55)

# --- ground shadow --------------------------------------------------------------
d.shape("ellipse", "Tapir shadow", x=350, y=752, width=440, height=34,
        fill="#2E3A2A", opacity=35, stroke=NONE)

# --- far legs (behind the body) -------------------------------------------------
d.path("M456,640 C452,690 454,730 452,766 L498,768 C498,732 500,690 504,646 Z",
       "Far foreleg", fill=FUR_FAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M648,640 C656,690 662,730 664,764 L708,766 C706,728 704,688 700,646 Z",
       "Far hind leg", fill=FUR_FAR_GRAD, stroke=INK, strokeWidth=5)
for i, x in enumerate([452, 664]):
    d.path(f"M{x},{766} C{x+8},{756} {x+38},{756} {x+46},{768} Z", f"Far hoof {i+1}",
           fill="#3A3B44", stroke=INK, strokeWidth=4)

# --- tail stub --------------------------------------------------------------------
d.path("M806,520 C822,524 830,540 826,556 C818,552 810,544 804,536 Z", "Tail",
       fill="#D9D3C6", stroke=INK, strokeWidth=4)

# --- body barrel: the white saddle ------------------------------------------------
d.path("M480,400 C560,382 660,380 725,398 C795,416 822,492 810,566 "
       "C798,632 742,668 660,674 C570,680 480,676 420,656 "
       "C370,640 360,470 400,428 C420,412 450,404 480,400 Z",
       "Saddle", fill=SADDLE_GRAD, stroke=INK, strokeWidth=7)
d.path("M520,404 C600,388 690,390 742,414", "Back sheen", fill=NONE,
       stroke="#FFFFFF", strokeWidth=12, opacity=45, cap="round")
d.path("M520,654 C590,664 680,660 740,640", "Belly shade", fill=NONE,
       stroke="#8E8778", strokeWidth=16, opacity=30, cap="round")
d.path("M770,440 C796,480 800,540 786,590", "Rump shade", fill=NONE,
       stroke="#9C9586", strokeWidth=12, opacity=30, cap="round")
# soft shadow cast by the black shoulder onto the white
d.path("M494,410 C486,476 490,566 514,668", "Shoulder cast", fill=NONE,
       stroke="#8E8778", strokeWidth=18, opacity=28, cap="round")

# --- hind thigh + near hind leg (black) -------------------------------------------
d.path("M628,676 C618,628 650,588 712,580 C760,575 798,584 812,590 "
       "C808,640 784,682 758,708 C750,730 748,750 748,768 L690,770 "
       "C692,742 690,716 676,700 C660,690 640,686 628,676 Z",
       "Hind thigh", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
d.path("M664,598 C712,586 760,584 796,594", "Thigh sheen", fill=NONE,
       stroke="#8B8FA3", strokeWidth=6, opacity=40, cap="round")
d.path("M744,690 C736,712 730,736 728,760", "Hock light", fill=NONE,
       stroke="#8B8FA3", strokeWidth=4, opacity=30, cap="round")

# --- neck, shoulder, near foreleg (black) -----------------------------------------
d.path("M330,432 C370,410 430,402 480,400 C470,470 474,566 500,674 "
       "C486,680 472,684 464,692 C458,720 458,746 460,768 L402,770 "
       "C404,742 400,712 392,690 C362,668 340,630 330,590 "
       "C322,540 316,470 330,432 Z",
       "Forequarters", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
d.path("M350,424 C392,410 436,404 470,404", "Crest sheen", fill=NONE,
       stroke="#8B8FA3", strokeWidth=7, opacity=40, cap="round")
d.path("M440,520 C452,580 466,630 480,668", "Shoulder sheen", fill=NONE,
       stroke="#8B8FA3", strokeWidth=6, opacity=28, cap="round")
d.path("M420,700 C424,722 426,744 428,762", "Shin light", fill=NONE,
       stroke="#8B8FA3", strokeWidth=4, opacity=30, cap="round")

# near hooves with toe splits
for i, (x, w) in enumerate([(400, 62), (688, 62)]):
    d.path(f"M{x},{770} C{x+6},{756} {x+w-6},{756} {x+w},{770} Z", f"Hoof {i+1}",
           fill="#4A4C57", stroke=INK, strokeWidth=4)
    for k in (1, 2):
        xx = x + w*k/3
        d.path(f"M{xx:.0f},761 L{xx:.0f},770", f"Hoof {i+1} split {k}", fill=NONE,
               stroke=INK, strokeWidth=3, cap="round")

# --- ear (behind head) ----------------------------------------------------------
d.path("M318,410 C300,378 304,342 328,334 C352,328 366,364 358,410 Z",
       "Ear", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M314,386 C308,358 318,340 330,338 C346,336 356,360 356,388", "Ear rim",
       fill=NONE, stroke="#F2EEE4", strokeWidth=5, cap="round")
d.path("M326,400 C318,378 322,356 332,352 C342,352 348,374 344,400 Z", "Inner ear",
       fill="#15151A", opacity=70, stroke=NONE)

# --- head ----------------------------------------------------------------------
d.path("M372,446 C360,410 330,394 300,396 C268,398 240,414 218,436 "
       "C204,450 194,470 192,488 C196,516 220,544 256,562 "
       "C292,580 340,588 368,576 C386,556 388,484 372,446 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
d.path("M228,420 C256,398 296,390 330,398", "Crown sheen", fill=NONE,
       stroke="#8B8FA3", strokeWidth=7, opacity=40, cap="round")
d.path("M262,556 C300,578 340,580 362,566", "Jaw shade", fill=NONE,
       stroke="#0E0E12", strokeWidth=10, opacity=35, cap="round")
d.shape("ellipse", "Cheek light", x=286, y=470, width=70, height=60,
        fill="#6A6D7E", opacity=22, stroke=NONE)

# lower lip + mouth under the snout
d.path("M200,514 C214,532 234,546 256,552", "Mouth", fill=NONE,
       stroke="#0E0E12", strokeWidth=5, opacity=80, cap="round")

# --- prehensile snout ---------------------------------------------------------------
d.path("M234,426 C202,438 172,454 150,476 C136,490 130,508 136,522 "
       "C144,532 158,528 162,516 C170,500 188,492 210,496 "
       "C220,498 228,502 236,506 Z",
       "Snout", fill=SNOUT_GRAD, stroke=INK, strokeWidth=6)
d.path("M226,434 C198,444 172,458 154,478", "Snout sheen", fill=NONE,
       stroke="#9195A8", strokeWidth=5, opacity=45, cap="round")
for i, (a, b) in enumerate([((206,440),(206,494)), ((186,448),(186,494)), ((168,460),(170,500))]):
    d.path("M%d,%d Q%d,%d %d,%d" % (a[0], a[1], (a[0]+b[0])//2 - 8, (a[1]+b[1])//2, b[0], b[1]),
           f"Snout wrinkle {i+1}", fill=NONE, stroke="#0E0E12", strokeWidth=3,
           opacity=55, cap="round")
d.shape("ellipse", "Nostril", x=136, y=508, width=11, height=9, fill="#0E0E12", opacity=85, stroke=NONE)

# --- eye: small, dark, glinting ---------------------------------------------------
d.shape("ellipse", "Eye ring", x=250, y=432, width=34, height=26, fill="#6A6D7E", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye", x=257, y=437, width=20, height=16, fill="#3A2416", stroke="#0E0E12", strokeWidth=2)
d.shape("ellipse", "Pupil", x=262, y=440, width=10, height=10, fill="#0B0705", stroke=NONE)
d.shape("ellipse", "Glint", x=263, y=440, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M252,436 C260,430 274,430 282,436", "Brow", fill=NONE,
       stroke="#0E0E12", strokeWidth=4, cap="round")

# --- name ----------------------------------------------------------------------
d.text("TAPIR", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DCE6D6", justify="center")

d.finish("tapir-V1R00")
