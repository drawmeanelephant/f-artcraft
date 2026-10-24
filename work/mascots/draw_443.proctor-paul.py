#!/usr/bin/env python3
"""Proctor Paul — mascot portrait V1R00.
Paul looming over a student at a computer; a dashboard tile reads out
the engagement score. 1000x1000. House style: gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Proctor Paul — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1626"}, {"offset": 1, "color": "#060A14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5C84"}, {"offset": 0.7, "color": "#32406A"},
    {"offset": 1, "color": "#1A2240"}]}}
DESK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38466E"}, {"offset": 1, "color": "#1C2544"}]}}
PAUL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8D9C4"}, {"offset": 0.7, "color": "#C4A98C"},
    {"offset": 1, "color": "#9A7E62"}]}}
STUDENT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9FAED0"}, {"offset": 0.7, "color": "#7484AC"},
    {"offset": 1, "color": "#4E5C82"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E4258"}, {"offset": 1, "color": "#16222E"}]}}
JACKET = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3F56"}, {"offset": 1, "color": "#2C2438"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E84B4", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9D4EE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5078", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=625, width=660, height=130,
        fill=DESK, stroke=NONE, opacity=92)
d.shape("ellipse", "Desk shadow", x=240, y=672, width=240, height=30,
        fill="#060A16", opacity=55, stroke=NONE)
d.shape("ellipse", "Paul shadow", x=560, y=690, width=180, height=32,
        fill="#060A16", opacity=55, stroke=NONE)

# --- engagement dashboard tile, upper right ----------------------------------------
d.shape("ellipse", "Tile glow", x=640, y=196, width=230, height=120,
        fill="#7E94D4", opacity=9, stroke=NONE)
d.shape("rectangle", "Tile", x=652, y=212, width=206, height=96,
        fill="#101A2E", stroke="#4A5E8E", strokeWidth=4, radius=12)
# eye icon
d.path("M672,254 C682,240 702,240 712,254 C702,268 682,268 672,254 Z",
       "Eye icon", fill="#2E3C5E", stroke="#8FA8D8", strokeWidth=3)
d.shape("ellipse", "Eye pupil", x=688, y=248, width=10, height=12,
        fill="#C9D4EE", stroke=NONE)
d.text("ENGAGEMENT", "Tile label", x=724, y=248, size=12,
       font="Virelai Sans", color="#8FA8D8", justify="left")
d.text("68%", "Tile score", x=724, y=288, size=30,
       font="Virelai Sans", color="#F0C878", justify="left")
# meter bar under the score
d.shape("rectangle", "Meter bg", x=724, y=296, width=110, height=6,
        fill="#2E3C5E", stroke=NONE, radius=3)
d.shape("rectangle", "Meter fill", x=724, y=296, width=75, height=6,
        fill="#F0C878", stroke=NONE, radius=3)

# --- the student at the computer -----------------------------------------------------
# desk bar
d.shape("rectangle", "Desk", x=238, y=560, width=250, height=18,
        fill="#3E4A70", stroke=INK, strokeWidth=4, radius=5)
d.path("M252,578 L246,660 M474,578 L480,660", "Desk legs", fill=NONE,
       stroke=INK, strokeWidth=8, cap="round")
# laptop on the desk
d.shape("rectangle", "Laptop screen", x=372, y=476, width=104, height=72,
        fill=SCREEN, stroke=INK, strokeWidth=5, radius=6)
d.shape("ellipse", "Screen glow", x=384, y=490, width=60, height=40,
        fill="#8FB4E8", opacity=18, stroke=NONE)
d.path("M364,548 L488,548 L498,562 L354,562 Z", "Laptop base",
       fill="#4A5878", stroke=INK, strokeWidth=4, join="round")
# student: small hunched figure, back mostly to us, face half-turned
d.shape("ellipse", "Student body", x=278, y=486, width=96, height=112,
        fill=STUDENT, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Student head", x=292, y=434, width=66, height=62,
        fill=STUDENT, stroke=INK, strokeWidth=5)
# hunch shadow + hair
d.path("M300,452 C310,436 340,434 352,450 C340,444 314,444 300,452 Z",
       "Hair", fill="#3A3050", stroke=NONE, opacity=90)
d.shape("ellipse", "Student eye", x=346, y=466, width=10, height=12,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Student glint", x=349, y=469, width=3, height=3,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Student cheek", x=340, y=484, width=16, height=9,
        fill="#C98A9A", opacity=45, stroke=NONE)
# arm reaching keyboard
d.path("M364,540 C390,546 410,548 428,550", "Student arm", fill=NONE,
       stroke="#7484AC", strokeWidth=11, cap="round")
d.shape("ellipse", "Student hand", x=422, y=544, width=16, height=13,
        fill="#9FAED0", stroke=INK, strokeWidth=3)
# legs under desk
d.path("M310,590 L306,650", "Student leg", fill=NONE, stroke="#4E5C82",
       strokeWidth=12, cap="round")
d.shape("ellipse", "Student shoe", x=292, y=644, width=30, height=14,
        fill=INK, stroke=NONE)

# --- Paul, looming behind -------------------------------------------------------------
# legs
d.path("M624,660 L620,696", "Paul leg L", fill=NONE, stroke="#9A7E62",
       strokeWidth=14, cap="round")
d.path("M668,660 L672,696", "Paul leg R", fill=NONE, stroke="#8A6E56",
       strokeWidth=14, cap="round")
d.shape("ellipse", "Paul shoe L", x=604, y=690, width=34, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Paul shoe R", x=660, y=690, width=34, height=15, fill=INK, stroke=NONE)
# tall body
d.path("M646,388 C706,388 734,442 731,510 C728,586 698,668 646,668 "
       "C594,668 564,586 561,510 C558,442 586,388 646,388 Z",
       "Paul body", fill=PAUL, stroke=INK, strokeWidth=6)
# jacket
d.path("M598,470 C606,560 622,620 646,660 C670,620 686,560 694,470 "
       "C672,486 620,486 598,470 Z",
       "Jacket", fill=JACKET, stroke=INK, strokeWidth=4, join="round")
# lanyard + badge
d.path("M620,470 L646,540 L672,470", "Lanyard", fill=NONE,
       stroke="#C04038", strokeWidth=4, join="round")
d.shape("rectangle", "Badge card", x=632, y=536, width=28, height=36,
        fill="#D9D2BC", stroke=INK, strokeWidth=3, radius=3)
d.shape("ellipse", "Badge photo", x=639, y=542, width=14, height=12,
        fill="#5A6A88", stroke=NONE)
# face: half-lidded oversight, looking down-left at the student
d.shape("ellipse", "Eye L", x=606, y=456, width=17, height=21, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=662, y=456, width=17, height=21, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=610, y=460, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=666, y=460, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
# heavy lids + flat mouth
d.path("M602,448 L628,452", "Lid L", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M658,452 L684,448", "Lid R", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=592, y=490, width=26, height=15,
        fill="#B46A5E", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=674, y=490, width=26, height=15,
        fill="#B46A5E", opacity=45, stroke=NONE)
d.path("M628,516 L664,516", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# arms crossed low
d.path("M574,540 C610,556 660,560 716,546", "Cross arm 1", fill=NONE,
       stroke="#C4A98C", strokeWidth=14, cap="round")
d.path("M716,562 C676,574 620,572 578,558", "Cross arm 2", fill=NONE,
       stroke="#B89A7E", strokeWidth=14, cap="round")
# sightline: faint beam from Paul's gaze to the laptop
d.path("M600,478 L470,500 M600,486 L470,522", "Sightline", fill=NONE,
       stroke="#8FA8D8", strokeWidth=2, opacity=22)

# --- captions ---------------------------------------------------------------------------
d.text("PROCTOR PAUL", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#D8E0F4", justify="center")
r = d.text("ENGAGEMENT SCORE MONITOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9CACCf", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("443.proctor-paul-V1R00")
