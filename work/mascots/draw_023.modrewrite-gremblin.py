#!/usr/bin/env python3
"""Modrewrite Gremblin — mascot portrait V1R00. URL Reality Warper.
A gremlin nested inside a .htaccess file, burst through a torn hole;
rewrite rules coil around it as a self-pointing loop arrow and a string
of trailing slashes. Chaotic neutral.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Modrewrite Gremblin — Mascot Portrait", 1000, 1000)

INK = "#26221C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A241C"}, {"offset": 1, "color": "#0A0E0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DEEAD4"}, {"offset": 0.7, "color": "#ACC0A4"},
    {"offset": 1, "color": "#6E8870"}]}}
FILE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EEDA"}, {"offset": 1, "color": "#D6CBA4"}]}}
GREM_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8BC58"}, {"offset": 0.75, "color": "#7E9640"},
    {"offset": 1, "color": "#58722E"}]}}
COIL = "#B0542E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5C7A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4F0DC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(208,222,8),(786,218,7),(176,524,9),(822,532,8),
                               (252,764,7),(748,748,9),(148,396,6),(850,388,7),
                               (396,110,7),(604,116,8),(336,816,6),(662,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7A9678", opacity=42, stroke=NONE)

# --- the .htaccess file ---------------------------------------------------------
d.shape("ellipse", "File shadow", x=352, y=726, width=310, height=22,
        fill="#4E6248", opacity=40, stroke=NONE)
d.shape("rectangle", "File sheet", x=352, y=318, width=296, height=412,
        fill=FILE_GRAD, stroke=INK, strokeWidth=6)
# dog-eared corner
d.path("M598,318 L648,318 L648,368 Z", "Dogear",
       fill="#C9BD94", stroke=INK, strokeWidth=4, join="round")
# header tab
r = d.text(".HTACCESS", "File tab", x=384, y=352, size=15,
           font="Virelai Sans", color="#5C5240", justify="left")
# rewrite rule lines; two highlighted as the live ones
d.shape("rectangle", "Rule highlight", x=372, y=402, width=236, height=20,
        radius=4, fill=COIL, opacity=22, stroke=NONE)
d.path("M384,414 L560,414", "Rule 1", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=80)
for i, yy in enumerate([442, 460, 602, 620, 638]):
    d.path(f"M384,{yy} L{560 - (i % 3) * 36},{yy}", f"Rule {i+2}",
           fill=NONE, stroke="#6E6450", strokeWidth=3.5, opacity=75)
# a rule that escapes — its line runs off the sheet edge and curls
d.path("M384,566 C430,566 470,562 520,570 C580,580 640,586 690,566 "
       "C730,550 744,516 730,488", "Runaway rule", fill=NONE,
       stroke=COIL, strokeWidth=4.5, cap="round", opacity=85)

# --- torn hole: the gremblin's door ----------------------------------------------
d.path("M436,506 L452,470 L482,452 L520,448 L552,462 L570,492 "
       "L566,528 L540,552 L500,560 L464,550 L442,528 Z",
       "Torn hole", fill="#171A12", stroke=INK, strokeWidth=4, join="round")
# torn paper flaps around the hole
d.path("M436,506 L414,494 L446,478 Z M570,492 L592,482 L566,468 Z "
       "M500,560 L492,584 L518,566 Z", "Torn flaps",
       fill=FILE_GRAD, stroke=INK, strokeWidth=3, join="round")

# --- the gremblin, nested in the hole ---------------------------------------------
# ears: big pointed, sticking out past the tear
d.path("M452,470 C420,436 388,424 356,430 C382,452 402,480 428,502 Z",
       "Ear L", fill=GREM_GRAD, stroke=INK, strokeWidth=4.5, join="round")
d.path("M552,462 C586,430 620,420 650,428 C622,450 600,476 574,498 Z",
       "Ear R", fill=GREM_GRAD, stroke=INK, strokeWidth=4.5, join="round")
d.path("M436,478 C416,456 396,444 380,442", "Ear L inner", fill=NONE,
       stroke="#4A5E26", strokeWidth=3, cap="round", opacity=80)
d.path("M568,470 C588,450 610,438 626,436", "Ear R inner", fill=NONE,
       stroke="#4A5E26", strokeWidth=3, cap="round", opacity=80)
# head filling the hole
d.shape("ellipse", "Gremblin head", x=448, y=448, width=110, height=104,
        fill=GREM_GRAD, stroke=INK, strokeWidth=5)
# head tuft
d.path("M496,452 C492,436 500,424 512,420 C508,434 512,442 520,448",
       "Tuft", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# wide chaotic eyes, mismatched
d.shape("ellipse", "Eye L white", x=466, y=478, width=26, height=26,
        fill="#F6F2E2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye R white", x=512, y=474, width=22, height=24,
        fill="#F6F2E2", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=476, y=486, width=11, height=11,
        fill="#241E18", stroke=NONE)
d.shape("ellipse", "Pupil R", x=520, y=482, width=9, height=9,
        fill="#241E18", stroke=NONE)
d.shape("ellipse", "Glint L", x=479, y=488, width=4, height=4,
        fill="#FFFFFF", stroke=NONE)
d.shape("ellipse", "Glint R", x=522, y=484, width=3.5, height=3.5,
        fill="#FFFFFF", stroke=NONE)
# the toothy grin — zigzag mouth
d.path("M466,522 C486,540 524,540 544,518 C540,540 528,552 505,553 "
       "C484,552 470,540 466,522 Z", "Grin", fill="#241E18",
       stroke=INK, strokeWidth=3.5, join="round")
d.path("M480,528 L488,540 L496,530 M514,530 L522,540 L530,526",
       "Teeth", fill=NONE, stroke="#F6F2E2", strokeWidth=3, cap="round")
# clawed hands gripping the torn edge
d.path("M438,528 C424,532 414,544 412,558", "Arm L", fill=NONE,
       stroke="#7E9640", strokeWidth=14, cap="round")
d.shape("ellipse", "Claw L", x=398, y=548, width=28, height=20,
        fill="#92A848", stroke=INK, strokeWidth=3.5)
d.path("M404,552 L398,562 M412,556 L408,566 M420,556 L418,566",
       "Claws L", fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")
d.path("M566,520 C582,522 594,532 598,546", "Arm R", fill=NONE,
       stroke="#7E9640", strokeWidth=14, cap="round")
d.shape("ellipse", "Claw R", x=590, y=536, width=28, height=20,
        fill="#92A848", stroke=INK, strokeWidth=3.5)
d.path("M596,542 L592,552 M604,546 L602,556 M612,546 L612,556",
       "Claws R", fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")
# tail: curls out below the file and ends in a redirect arrowhead
d.path("M560,716 C620,724 664,712 678,678 C688,652 676,632 652,630",
       "Tail", fill=NONE, stroke="#7E9640", strokeWidth=15, cap="round")
d.path("M652,630 L668,622 L664,640 Z", "Tail arrow",
       fill="#7E9640", stroke=INK, strokeWidth=3, join="round")

# --- coiled rewrite rules -----------------------------------------------------------
# orbit arrow around the hole — the rule rewrites itself
d.path("M414,420 C400,340 450,282 530,278 C620,274 690,330 692,412 "
       "C694,470 664,512 616,530", "Loop coil", fill=NONE,
       stroke=COIL, strokeWidth=5, cap="round", opacity=80)
d.path("M616,530 L634,540 L612,546 Z", "Loop head",
       fill=COIL, stroke=INK, strokeWidth=2.5, join="round")
# trailing slashes coiled around the left side — a curved string of "/" marks
for i in range(6):
    t = i / 5
    a = math.radians(215 - t * 65)          # arc hugging the sheet's left edge
    cx, cy, rr = 500, 470, 215
    x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
    d.path(f"M{x - 7:.0f},{y + 10:.0f} L{x + 7:.0f},{y - 10:.0f}",
           f"Slash {i+1}", fill=NONE, stroke="#8A4A2C", strokeWidth=5,
           cap="round", opacity=78 - i * 4)
# stray flags and sparks
d.path("M272,318 L288,306 M280,340 L294,334", "Sparks L", fill=NONE,
       stroke=COIL, strokeWidth=3.5, cap="round", opacity=60)
d.path("M676,470 L692,458 M684,492 L698,486", "Sparks R", fill=NONE,
       stroke=COIL, strokeWidth=3.5, cap="round", opacity=60)

# --- name + role -------------------------------------------------------------------
d.text("MODREWRITE GREMBLIN", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#E6EFDC", justify="center")
r = d.text("URL REALITY WARPER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8BE9C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("023.modrewrite-gremblin-V1R00")
