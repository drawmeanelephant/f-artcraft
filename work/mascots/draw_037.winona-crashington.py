#!/usr/bin/env python3
"""Winona Crashington — mascot portrait V1R00. Blue Screen Muse of the
Millennial Interface: the ceremonial ghost of Windows 95 instability,
holding a fractured CRT like a mirror, a stack of AOL trial CDs beside
her. Teal-desktop plate on a deep navy night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Winona Crashington — Mascot Plate", 1000, 1000)

INK = "#241E18"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#10222A"}, {"offset": 1, "color": "#050C0F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E7C78"}, {"offset": 0.62, "color": "#28524F"},
    {"offset": 1, "color": "#142B2D"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0CEAE"}, {"offset": 0.75, "color": "#DCA987"},
    {"offset": 1, "color": "#C08A66"}]}}
HAIR_GRAD = {"gradient": {"kind": "linear", "start": [0, 240], "end": [0, 470], "stops": [
    {"offset": 0, "color": "#4A3423"}, {"offset": 0.5, "color": "#2E2118"},
    {"offset": 1, "color": "#1B130E"}]}}
DRESS_GRAD = {"gradient": {"kind": "linear", "start": [0, 450], "end": [0, 810], "stops": [
    {"offset": 0, "color": "#3557CC"}, {"offset": 0.5, "color": "#21368F"},
    {"offset": 1, "color": "#131F5C"}]}}
BEIGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0D2AE"}, {"offset": 1, "color": "#A89478"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#1B3A55"}, {"offset": 1, "color": "#081521"}]}}
CD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDF1F4"}, {"offset": 0.55, "color": "#B9C2C9"},
    {"offset": 1, "color": "#8A959E"}]}}
DLG_GRAD = {"gradient": {"kind": "linear", "start": [0, 150], "end": [0, 260], "stops": [
    {"offset": 0, "color": "#D8D4CC"}, {"offset": 1, "color": "#B4B0A6"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0A2E9E"}, {"offset": 1, "color": "#061864"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#3F8A84", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0C1C1E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BFE0D8", strokeWidth=3, opacity=28)
# desktop-teal patina + flecks
d.shape("ellipse", "Patina 1", x=200, y=380, width=230, height=150,
        fill="#2A5A55", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=590, width=220, height=140,
        fill="#4E948C", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(215,330,5),(795,340,6),(185,560,5),(845,575,5),
                               (265,760,5),(735,765,6),(160,450,5),(852,430,5),
                               (430,120,5),(605,130,6),(330,150,4),(700,190,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#CFE8DF", opacity=30, stroke=NONE)
# faint CRT scanlines drifting down the plate
for j, yy in enumerate((210, 470, 700)):
    d.path(f"M160,{yy} L840,{yy}", f"Plate scanline {j+1}",
           fill=NONE, stroke="#DFF2EC", strokeWidth=1, opacity=5)
# ghost arcs on the dark backdrop
d.path("M930,140 A110,110 0 0 0 835,55", "Ghost arc TR",
       fill=NONE, stroke="#4E8A80", strokeWidth=14, opacity=10, cap="round")
d.path("M70,760 A125,125 0 0 0 185,880", "Ghost arc BL",
       fill=NONE, stroke="#4E8A80", strokeWidth=10, opacity=8, cap="round")

# --- floating error dialog, upper left ----------------------------------------------
d.shape("rectangle", "Dialog shadow", x=178, y=158, width=216, height=108,
        radius=6, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Dialog body", x=170, y=150, width=216, height=108,
        radius=6, fill=DLG_GRAD, stroke="#4A463E", strokeWidth=3)
d.shape("rectangle", "Dialog titlebar", x=170, y=150, width=216, height=22,
        radius=6, fill=BAR_GRAD, stroke=NONE)
d.path("M182,161 L262,161", "Dialog title text",
       fill=NONE, stroke="#E8ECF2", strokeWidth=4, cap="round", opacity=85)
d.shape("rectangle", "Dialog close", x=362, y=154, width=18, height=14,
        radius=2, fill="#C8C4BC", stroke="#4A463E", strokeWidth=1.5)
d.path("M366,157 L376,165 M376,157 L366,165", "Dialog close X",
       fill=NONE, stroke="#4A463E", strokeWidth=2, cap="round")
# warning triangle + bang, built from shapes (no glyph risk)
d.path("M204,224 L218,192 L232,224 Z", "Warning triangle",
       fill="#E8C33C", stroke="#7A5C14", strokeWidth=2.5)
d.path("M217,199 L219,199 L219,213 L217,213 Z", "Bang stem",
       fill="#241E18", stroke=NONE)
d.shape("ellipse", "Bang dot", x=216, y=216, width=4, height=4,
        fill="#241E18", stroke=NONE)
# message lines + OK button
d.path("M246,196 L360,196 M246,208 L340,208", "Dialog message lines",
       fill=NONE, stroke="#5A564C", strokeWidth=4, cap="round", opacity=80)
d.shape("rectangle", "OK button", x=272, y=226, width=66, height=22,
        radius=3, fill="#C8C4BC", stroke="#4A463E", strokeWidth=2)
d.text("OK", "OK label", x=305, y=243, size=12, font="Virelai Sans",
       color="#241E18", justify="center")

# --- the taskbar, low inside the plate ------------------------------------------------
d.shape("rectangle", "Taskbar", x=300, y=792, width=400, height=26,
        radius=4, fill=DLG_GRAD, stroke="#4A463E", strokeWidth=2.5, opacity=92)
d.shape("ellipse", "Start orb", x=310, y=798, width=14, height=14,
        fill="#2E8B3A", stroke="#14521E", strokeWidth=2)
for i, xx in enumerate((340, 430, 520)):
    d.shape("rectangle", f"Taskbar tab {i+1}", x=xx, y=798, width=78, height=14,
            radius=2, fill="#B4B0A6", stroke="#5A564C", strokeWidth=1.5)
    d.path(f"M{xx+7},{805} L{xx+40},{805}", f"Tab label {i+1}",
           fill=NONE, stroke="#5A564C", strokeWidth=3, cap="round")
# clock block, right end
d.shape("rectangle", "Clock tray", x=636, y=798, width=54, height=14,
        radius=2, fill="#B4B0A6", stroke="#5A564C", strokeWidth=1.5)
d.path("M644,805 L676,805", "Clock line",
       fill=NONE, stroke="#5A564C", strokeWidth=3, cap="round")

# --- AOL trial CD stack, lower left ----------------------------------------------------
for i, yy in enumerate((742, 734, 726)):
    d.shape("ellipse", f"CD stack {i+1}", x=205, y=yy, width=160, height=26,
            fill=CD_GRAD, stroke="#5A646C", strokeWidth=2)
# top disc face with rainbow sheen
d.shape("ellipse", "CD top", x=197, y=710, width=176, height=32,
        fill=CD_GRAD, stroke="#5A646C", strokeWidth=2.5)
d.path("M215,722 A74,14 0 0 1 300,714", "CD sheen warm",
       fill=NONE, stroke="#E8A0B0", strokeWidth=3, opacity=55, cap="round")
d.path("M225,730 A80,14 0 0 1 340,722", "CD sheen cool",
       fill=NONE, stroke="#88C8E8", strokeWidth=3, opacity=55, cap="round")
d.shape("ellipse", "CD label ring", x=248, y=718, width=74, height=16,
        fill="#DDE4E8", stroke="#8A959E", strokeWidth=1.5)
d.shape("ellipse", "CD hole", x=274, y=722, width=22, height=8,
        fill="#28524F", stroke="#5A646C", strokeWidth=1.5)
d.text("AOL", "CD label", x=285, y=728, size=11, font="Virelai Sans",
       color="#2A4A8A", justify="center")

# --- Winona ---------------------------------------------------------------------------
# bob hair mass behind the head
d.path("M480,236 C560,236 606,296 600,384 C597,444 580,486 560,502 "
       "C566,450 560,404 548,372 C520,388 460,392 424,374 "
       "C408,408 404,452 412,500 C386,480 372,430 372,376 "
       "C372,296 408,236 480,236 Z",
       "Bob hair", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
d.path("M430,260 C470,246 530,248 566,276 C530,262 470,262 434,278 Z",
       "Hair sheen", fill="#8A6242", opacity=45, stroke=NONE)
# barrette, teal
d.path(rot_rect_path(556, 300, 34, 10, 24), "Barrette",
       fill="#3FA08C", stroke=INK, strokeWidth=2.5)
# neck
d.path("M456,452 L456,496 L516,496 L516,448 C500,462 472,462 456,452 Z",
       "Neck", fill="#D9A67F", stroke=INK, strokeWidth=3)
d.path("M456,458 C474,470 500,470 516,458 L516,448 C500,462 472,462 456,452 Z",
       "Neck shade", fill="#8A5C3E", opacity=35, stroke=NONE)
# face
d.path("M486,300 C544,300 572,342 570,390 C568,438 536,470 486,470 "
       "C436,470 404,438 402,390 C400,342 428,300 486,300 Z",
       "Face", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# bangs sweeping over the forehead
d.path("M404,352 C420,308 452,286 490,284 C540,282 570,312 572,354 "
       "C556,330 536,318 512,318 C520,336 516,352 504,360 "
       "C500,340 486,326 466,326 C470,344 464,358 450,364 "
       "C448,344 432,336 420,342 C412,346 406,350 404,352 Z",
       "Bangs", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
# smudged eyeliner — theatrical, tired
d.shape("ellipse", "Liner smudge L", x=424, y=392, width=52, height=26,
        fill="#3A2C28", opacity=28, stroke=NONE)
d.shape("ellipse", "Liner smudge R", x=500, y=392, width=52, height=26,
        fill="#3A2C28", opacity=28, stroke=NONE)
# eyes gazing right, toward the mirror
for side, ex in (("L", 446), ("R", 522)):
    d.shape("ellipse", f"Eye white {side}", x=ex - 21, y=376, width=42, height=24,
            fill="#F4EDE4", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=442, y=380, width=16, height=16,
        fill="#3E6E8E", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Iris R", x=520, y=380, width=16, height=16,
        fill="#3E6E8E", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Pupil L", x=447, y=384, width=7, height=7,
        fill="#18120E", stroke=NONE)
d.shape("ellipse", "Pupil R", x=525, y=384, width=7, height=7,
        fill="#18120E", stroke=NONE)
d.shape("ellipse", "Eye glint L", x=444, y=382, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=522, y=382, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# heavy upper lash lines
d.path("M424,378 C434,368 456,366 468,376", "Lash L",
       fill=NONE, stroke="#18120E", strokeWidth=5, cap="round")
d.path("M502,376 C514,366 536,368 546,378", "Lash R",
       fill=NONE, stroke="#18120E", strokeWidth=5, cap="round")
# mascara bleed ticks below
d.path("M434,412 L432,418 M452,414 L451,420", "Mascara bleed L",
       fill=NONE, stroke="#3A2C28", strokeWidth=2, opacity=45, cap="round")
d.path("M516,414 L515,420 M534,412 L533,418", "Mascara bleed R",
       fill=NONE, stroke="#3A2C28", strokeWidth=2, opacity=45, cap="round")
# brows: one arched high, one flat — mid-monologue
d.path("M424,352 C436,340 458,338 470,348", "Brow L",
       fill=NONE, stroke="#241812", strokeWidth=5, cap="round")
d.path("M502,358 C516,352 534,352 546,356", "Brow R",
       fill=NONE, stroke="#241812", strokeWidth=4, cap="round")
# nose, lips, beauty mark
d.path("M486,392 C482,404 480,412 484,418", "Nose",
       fill=NONE, stroke="#A07050", strokeWidth=3, cap="round")
d.path("M462,436 C472,430 482,432 486,436 C490,432 502,430 512,436 "
       "C502,448 472,448 462,436 Z",
       "Lips", fill="#A84A4A", stroke="#6A2A28", strokeWidth=2)
d.shape("ellipse", "Beauty mark", x=524, y=430, width=6, height=6,
        fill="#3A2C28", stroke=NONE)

# --- gown: the blue screen, worn ------------------------------------------------------------
# left arm hangs first (behind gown edge), presenting a CD
d.path("M398,540 C372,580 358,630 352,678 C362,690 380,690 390,680 "
       "C394,632 404,590 416,556 Z",
       "Arm L", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# the gown: bell silhouette BSOD blue
d.path("M486,462 C556,462 596,510 610,590 C620,660 630,740 622,792 "
       "C560,814 412,814 352,792 C344,740 354,660 364,590 "
       "C378,510 416,462 486,462 Z",
       "Gown", fill=DRESS_GRAD, stroke=INK, strokeWidth=5)
d.path("M560,500 C596,560 616,690 612,786 C592,798 566,806 540,808 "
       "C568,720 574,590 560,500 Z",
       "Gown shade", fill="#0E173E", opacity=45, stroke=NONE)
d.path("M352,756 C420,780 552,780 622,756 L622,792 C560,814 412,814 352,792 Z",
       "Hem shade", fill="#0B1338", opacity=40, stroke=NONE)
# pixel collar: a row of white squares — the dropdown menu of her neckline
for i in range(7):
    d.shape("rectangle", f"Collar px {i+1}", x=436 + i * 16, y=462 + (6 if i in (0, 6) else 0),
            width=13, height=13, fill="#E8ECF2", stroke=INK, strokeWidth=2)
# glitch pixels on the skirt
for i, (x, y, o) in enumerate([(430, 640, 45), (540, 700, 40), (470, 740, 35),
                               (585, 620, 38), (400, 700, 42)]):
    d.shape("rectangle", f"Glitch px {i+1}", x=x, y=y, width=9, height=9,
            fill="#DCE4F4", opacity=o, stroke=NONE)
# left hand holding a single trial CD up at her side
d.shape("ellipse", "Hand L", x=346, y=664, width=32, height=28,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "CD held", x=316, y=640, width=76, height=76,
        fill=CD_GRAD, stroke=INK, strokeWidth=3)
d.path("M326,668 A28,28 0 0 1 352,644", "CD held sheen",
       fill=NONE, stroke="#E8A0B0", strokeWidth=3, opacity=60, cap="round")
d.shape("ellipse", "CD held hole", x=344, y=668, width=20, height=20,
        fill="#28524F", stroke=INK, strokeWidth=2)
# right arm raised, cradling the CRT mirror
d.path("M560,470 C612,438 652,402 678,360 C692,358 706,372 704,388 "
       "C676,436 634,478 588,506 C572,496 562,484 560,470 Z",
       "Arm R", fill=DRESS_GRAD, stroke=INK, strokeWidth=4)
d.path("M668,356 C682,350 698,356 704,370 C700,384 686,392 674,388 "
       "C664,380 662,366 668,356 Z",
       "Hand R", fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)

# --- the fractured CRT, held like a mirror ------------------------------------------------
crx, cry = 706, 268
d.path(rot_rect_path(crx, cry, 196, 158, -7), "CRT body",
       fill=BEIGE_GRAD, stroke=INK, strokeWidth=5)
d.path(rot_rect_path(crx - 6, cry - 6, 148, 106, -7), "CRT screen bezel",
       fill="#8A7C64", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(crx - 8, cry - 8, 130, 88, -7), "CRT glass",
       fill=SCREEN_GRAD, stroke=INK, strokeWidth=2)
# her reflected face in the dark glass — a pale, warped ghost
d.shape("ellipse", "CRT reflection", x=650, y=222, width=66, height=52,
        fill="#9CC4D8", opacity=25, stroke=NONE)
d.shape("ellipse", "CRT eye L", x=662, y=240, width=8, height=6,
        fill="#E8F2F8", opacity=45, stroke=NONE)
d.shape("ellipse", "CRT eye R", x=686, y=240, width=8, height=6,
        fill="#E8F2F8", opacity=45, stroke=NONE)
# crack web radiating from the lower-left corner of the glass
for i, (x2, y2) in enumerate([(700, 208), (726, 226), (736, 258), (676, 196), (652, 196)]):
    d.path(f"M640,282 L{x2},{y2}", f"Crack {i+1}",
           fill=NONE, stroke="#D8E4E8", strokeWidth=2.5, opacity=65, cap="round")
d.path("M640,282 L668,262 M668,262 L690,266", "Crack fork",
       fill=NONE, stroke="#E8F0F4", strokeWidth=1.5, opacity=55, cap="round")
d.shape("ellipse", "Crack impact", x=634, y=276, width=12, height=12,
        fill="#E8F0F4", opacity=40, stroke=NONE)
# bezel buttons + power LED
for i, xx in enumerate((758, 774)):
    d.shape("rectangle", f"CRT btn {i+1}", x=xx, y=306, width=12, height=8,
            radius=2, fill="#9C8E74", stroke=INK, strokeWidth=1.5)
d.shape("ellipse", "CRT LED", x=794, y=306, width=8, height=8,
        fill="#4AC85A", stroke="#1E5E28", strokeWidth=1.5)
d.shape("ellipse", "CRT LED glow", x=790, y=302, width=16, height=16,
        fill="#4AC85A", opacity=30, stroke=NONE)
# vents on the CRT crown
for i in range(4):
    d.path(f"M{676 + i * 18},{190 + i * 1.5} L{688 + i * 18},{189 + i * 1.5}",
           f"CRT vent {i+1}", fill=NONE, stroke="#8A7C64",
           strokeWidth=3, opacity=70, cap="round")

# --- hourglass cursor, forever waiting ------------------------------------------------------
hx, hy = 662, 640
d.shape("ellipse", "Cursor aura", x=hx - 16, y=hy - 22, width=58, height=70,
        fill="#9CC4D8", opacity=10, stroke=NONE)
d.path(f"M{hx},{hy} L{hx+26},{hy} L{hx+13},{hy+16} L{hx+26},{hy+40} "
       f"L{hx},{hy+40} L{hx+13},{hy+16} Z",
       "Hourglass", fill="#E8E4DA", stroke=INK, strokeWidth=3)
d.path(f"M{hx+4},{hy+34} L{hx+13},{hy+24} L{hx+22},{hy+34} Z",
       "Hourglass sand", fill="#B08A3C", stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("WINONA CRASHINGTON", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#DFEAE4", justify="center")
r = d.text("BLUE SCREEN MUSE OF THE MILLENNIAL INTERFACE", "Role",
           x=500, y=968, size=22, font="Virelai Sans",
           color="#9FC4BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=70)

d.finish("037.winona-crashington-V1R00")
