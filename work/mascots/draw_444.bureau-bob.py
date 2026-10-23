#!/usr/bin/env python3
"""Bureau Bob — mascot portrait V1R00.
Mascot between two screens: portal reporting success, caseworker screen
showing nothing. 1000x1000. House style: gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bureau Bob — Mascot Portrait", 1000, 1000)

INK = "#2E2530"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101C2C"}, {"offset": 1, "color": "#05090F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5878"}, {"offset": 0.7, "color": "#26394F"},
    {"offset": 1, "color": "#17253A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#243650"}, {"offset": 1, "color": "#141F30"}]}}
BEZEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5A6E"}, {"offset": 1, "color": "#2A3542"}]}}
PORTAL_SCR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E4A3E"}, {"offset": 1, "color": "#0E2A22"}]}}
CASEWORK_SCR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#232D38"}, {"offset": 1, "color": "#12181F"}]}}
SUIT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A6E92"}, {"offset": 0.75, "color": "#3E4E6E"},
    {"offset": 1, "color": "#2A3650"}]}}
FOLDER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EBD8A9"}, {"offset": 1, "color": "#C3A470"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54708F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4F0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,230,8),(805,240,7),(160,520,9),(835,545,8),
                               (245,770,7),(755,745,9),(130,390,6),(865,395,7),
                               (395,115,7),(605,110,8),(335,825,6),(660,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#465F7E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E1826",
       strokeWidth=4, opacity=70)

# --- portal screen (left): success ---------------------------------------------
d.shape("ellipse", "Portal glow", x=170, y=210, width=300, height=240,
        fill="#63C98E", opacity=12, stroke=NONE)
d.shape("rectangle", "Portal bezel", x=185, y=225, width=270, height=200,
        fill=BEZEL, stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Portal screen", x=200, y=240, width=240, height=150,
        fill=PORTAL_SCR, stroke="#0A1410", strokeWidth=3, radius=6)
d.shape("ellipse", "Check badge", x=225, y=258, width=52, height=52,
        fill="#63C98E", stroke=INK, strokeWidth=4)
d.path("M238,284 L249,295 L265,272", "Check mark", fill=NONE, stroke="#0E2A22",
       strokeWidth=6, cap="round", join="round")
d.text("UPLOAD SUCCEEDED", "Portal line 1", x=290, y=280, size=15,
       font="Virelai Sans", color="#9BE8BC", justify="left")
d.text("CASE #0444 FILED", "Portal line 2", x=290, y=302, size=13,
       font="Virelai Sans", color="#5FA87E", justify="left")
for i, w in enumerate([200, 160, 185]):
    d.shape("rectangle", f"Portal row {i+1}", x=214, y=330+i*16, width=w, height=7,
            fill="#3E7A5E", opacity=55, stroke=NONE, radius=3)
d.shape("rectangle", "Portal stand", x=300, y=425, width=40, height=55,
        fill=BEZEL, stroke=INK, strokeWidth=4)
d.path("M275,480 L365,480 L375,496 L265,496 Z", "Portal foot",
       fill=BEZEL, stroke=INK, strokeWidth=4)

# --- caseworker screen (right): nothing ----------------------------------------
d.shape("rectangle", "Case bezel", x=545, y=225, width=270, height=200,
        fill=BEZEL, stroke=INK, strokeWidth=5, radius=10)
d.shape("rectangle", "Case screen", x=560, y=240, width=240, height=150,
        fill=CASEWORK_SCR, stroke="#0A0E13", strokeWidth=3, radius=6)
d.path("M585,300 L585,272 L660,272 L660,300", "Empty window frame", fill=NONE,
       stroke="#3A4A5C", strokeWidth=4)
d.shape("ellipse", "Case spinner", x=600, y=315, width=26, height=26,
        fill=NONE, stroke="#4A5E74", strokeWidth=4)
d.text("NO RECORD FOUND", "Case line 1", x=640, y=322, size=14,
       font="Virelai Sans", color="#8A99A8", justify="left")
d.text("0 RESULTS", "Case line 2", x=640, y=344, size=12,
       font="Virelai Sans", color="#556575", justify="left")
for i, w in enumerate([190, 150]):
    d.shape("rectangle", f"Case row {i+1}", x=575, y=358+i*15, width=w, height=6,
            fill="#33404E", opacity=45, stroke=NONE, radius=3)
d.shape("rectangle", "Case stand", x=660, y=425, width=40, height=55,
        fill=BEZEL, stroke=INK, strokeWidth=4)
d.path("M635,480 L725,480 L735,496 L625,496 Z", "Case foot",
       fill=BEZEL, stroke=INK, strokeWidth=4)

# --- the handoff that never lands: case tag flies, wire dies -------------------
d.path("M455,320 C500,340 540,335 560,310", "Wire OK", fill=NONE,
       stroke="#63C98E", strokeWidth=4, dash=[8,7], cap="round", opacity=70)
d.path("M560,310 C572,298 578,300 585,305", "Wire fray", fill=NONE,
       stroke="#8A4A52", strokeWidth=4, dash=[2,6], cap="round", opacity=80)
# --- Bob: folder-headed clerk, deadpan -----------------------------------------
d.shape("ellipse", "Bob shadow", x=380, y=688, width=240, height=30,
        fill="#0A1220", opacity=45, stroke=NONE)
# body: navy suit blob
d.path("M500,520 C575,520 620,575 620,640 C620,690 575,712 500,712 "
       "C425,712 380,690 380,640 C380,575 425,520 500,520 Z",
       "Bob body", fill=SUIT, stroke=INK, strokeWidth=6)
# shirt V + tie
d.path("M465,545 L500,600 L535,545", "Shirt V", fill=NONE, stroke="#C9D4E4",
       strokeWidth=8, cap="round", join="round")
d.path("M493,596 L507,596 L505,668 L500,678 L495,668 Z", "Tie",
       fill="#8A3A44", stroke=INK, strokeWidth=3, join="round")
# stubby arms
d.path("M385,600 C360,610 352,638 362,660", "Arm L", fill=NONE,
       stroke="#3E4E6E", strokeWidth=18, cap="round")
d.path("M615,600 C640,610 648,638 638,660", "Arm R", fill=NONE,
       stroke="#3E4E6E", strokeWidth=18, cap="round")
# head: manila folder with tab
d.path("M425,385 L425,510 L575,510 L575,400 L545,400 L538,385 Z",
       "Folder head", fill=FOLDER, stroke=INK, strokeWidth=6, join="round")
d.path("M425,430 L575,430", "Folder crease", fill=NONE, stroke="#B0935E",
       strokeWidth=3, opacity=60)
# face on the folder: glasses, flat eyes, flat mouth
d.shape("ellipse", "Lens L", x=448, y=448, width=42, height=42,
        fill="#F5EDD8", opacity=35, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lens R", x=512, y=448, width=42, height=42,
        fill="#F5EDD8", opacity=35, stroke=INK, strokeWidth=4)
d.path("M490,469 L512,469", "Bridge", fill=NONE, stroke=INK, strokeWidth=4)
d.path("M448,462 C455,470 465,470 472,462", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M530,462 C537,470 547,470 554,462", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M480,496 L522,496", "Flat mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# stamp on folder corner
d.path("M520,478 L562,470 L566,492 L524,500 Z", "Red stamp", fill="#A8454E",
       opacity=75, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("BUREAU BOB", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#D2DFEE", justify="center")
r = d.text("RIGHTS IN STATUTE, NOT IN SOFTWARE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#93A9C2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("444.bureau-bob-V1R00")
