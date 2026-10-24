#!/usr/bin/env python3
"""sealward-proxy-9 — mascot portrait V1R00.
Custodian mascot pressing a seal beside a witness packet preserved only as a
ceremonial abstract in a vitrine. 1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("sealward-proxy-9 — Mascot Portrait", 1000, 1000)

INK = "#221C30"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1018"}, {"offset": 1, "color": "#05060A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4468"}, {"offset": 0.7, "color": "#282C48"},
    {"offset": 1, "color": "#181A2C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#242842"}, {"offset": 1, "color": "#101224"}]}}
ROBE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A7498"}, {"offset": 0.75, "color": "#48527A"},
    {"offset": 1, "color": "#303654"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0BC6E"}, {"offset": 1, "color": "#9A7A38"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE4CC"}, {"offset": 1, "color": "#CBBD9A"}]}}
WAX = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8504E"}, {"offset": 1, "color": "#8A2A30"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#606A9A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCD4EE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3C4262", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E1020",
       strokeWidth=4, opacity=70)

# --- the vitrine: witness packet preserved as ceremonial abstract ------------------
d.shape("ellipse", "Vitrine glow", x=555, y=180, width=260, height=330,
        fill="#C8B46A", opacity=10, stroke=NONE)
d.shape("rectangle", "Vitrine case", x=570, y=190, width=220, height=300,
        fill=NONE, stroke="#8A7440", strokeWidth=6, radius=8)
d.shape("rectangle", "Vitrine inner", x=582, y=202, width=196, height=276,
        fill="#1A1E30", stroke="#5E5230", strokeWidth=3, radius=6)
# inner velvet rays (ceremony)
for i in range(5):
    a = -60 + i*30
    import math
    x2 = 680 + 95*math.sin(math.radians(a))
    d.path(f"M680,300 L{x2:.0f},215", f"Ray {i+1}", fill=NONE,
           stroke="#5E5230", strokeWidth=2, opacity=45)
# the abstract packet: a ghost-outline envelope, translucent
d.path("M625,275 L735,275 L735,345 L625,345 Z", "Abstract packet",
       fill="#8A94C8", opacity=30, stroke="#A8B4DC", strokeWidth=4)
d.path("M625,275 L680,315 L735,275", "Abstract flap", fill=NONE,
       stroke="#A8B4DC", strokeWidth=3, opacity=60)
# soft inner blur where the contents would be
d.shape("ellipse", "Abstract blur", x=650, y=290, width=60, height=40,
        fill="#C4CCE8", opacity=22, stroke=NONE)
# chain drape across the case (do not touch)
d.path("M570,250 C640,285 720,285 790,250", "Chain", fill=NONE,
       stroke="#8A7440", strokeWidth=4, dash=[9,6], opacity=80)
# plaque
d.shape("rectangle", "Plaque", x=600, y=505, width=160, height=44,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=4)
d.text("WITNESS PACKET", "Plaque 1", x=614, y=524, size=12, font="Virelai Sans",
       color="#3E2E12", justify="left")
d.text("(CEREMONIAL ABSTRACT)", "Plaque 2", x=610, y=541, size=8,
       font="Virelai Sans", color="#5E4A22", justify="left")
# pedestal
d.path("M600,560 L760,560 L775,585 L585,585 Z", "Pedestal", fill="#343A58",
       stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Pedestal stem", x=655, y=585, width=50, height=80,
        fill="#343A58", stroke=INK, strokeWidth=4)
d.path("M635,665 L725,665 L735,690 L625,690 Z", "Pedestal foot",
       fill="#2A2E48", stroke=INK, strokeWidth=4, join="round")

# --- the document receiving its seal ------------------------------------------------
d.path("M390,555 L615,555 L630,620 L375,620 Z", "Desk top", fill="#3A3350",
       stroke=INK, strokeWidth=5, join="round")
d.path("M405,620 L392,700 M600,620 L613,700", "Desk legs", fill=NONE,
       stroke="#2A2440", strokeWidth=8, cap="round")
# document on the desk
d.path("M420,520 L575,520 L582,565 L413,565 Z", "Sealed doc",
       fill=PAPER, stroke=INK, strokeWidth=4, join="round")
for i, w in enumerate([120, 135, 100]):
    d.shape("rectangle", f"Doc line {i+1}", x=430, y=530+i*10, width=w, height=5,
            fill="#8A7E64", opacity=55, stroke=NONE)
# ribbon
d.path("M413,558 L582,558", "Ribbon", fill=NONE, stroke="#8A2A30",
       strokeWidth=5, opacity=80)
# fresh wax seal puddle
d.shape("ellipse", "Wax puddle", x=505, y=530, width=42, height=30,
        fill=WAX, stroke=INK, strokeWidth=3)
d.path("M512,540 C517,544 525,544 530,540 M515,550 L533,550", "Seal mark",
       fill=NONE, stroke="#F0D8C8", strokeWidth=2, opacity=80)

# --- Proxy-9: robed custodian pressing the seal ------------------------------------
d.shape("ellipse", "Proxy shadow", x=185, y=672, width=240, height=30,
        fill="#080A16", opacity=50, stroke=NONE)
# robed body
d.path("M310,430 C385,430 425,495 425,575 C425,650 380,705 310,705 "
       "C240,705 195,650 195,575 C195,495 235,430 310,430 Z",
       "Robe", fill=ROBE, stroke=INK, strokeWidth=6)
# sash + lanyard badge
d.path("M255,470 L375,470 L382,495 L262,495 Z", "Sash", fill="#3E3658",
       stroke=INK, strokeWidth=3, join="round", opacity=85)
d.path("M310,500 L310,545", "Lanyard", fill=NONE, stroke="#E0BC6E",
       strokeWidth=3)
d.shape("rectangle", "Badge", x=296, y=545, width=28, height=36,
        fill="#EDE4CC", stroke=INK, strokeWidth=3, radius=3)
d.text("P-9", "Badge text", x=302, y=570, size=11, font="Virelai Sans",
       color="#3E3658", justify="left")
# hood/cowl
d.path("M240,450 C240,390 270,360 310,360 C350,360 380,390 380,450 "
       "C355,432 265,432 240,450 Z", "Cowl", fill="#3E3658",
       stroke=INK, strokeWidth=5, join="round")
# face: careful, slightly apologetic — angled brows, steady eyes
d.shape("ellipse", "Face", x=268, y=425, width=85, height=75,
        fill="#8E98BC", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye L", x=288, y=455, width=15, height=18,
        fill="#221C30", stroke=NONE)
d.shape("ellipse", "Eye R", x=320, y=455, width=15, height=18,
        fill="#221C30", stroke=NONE)
d.path("M283,441 L301,437", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M320,437 L338,441", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M295,480 C303,485 317,485 325,480", "Sorry mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# arm reaching right, pressing the T-seal stamp down onto the wax
d.path("M415,535 C460,540 490,545 508,550", "Press arm", fill=NONE,
       stroke="#48527A", strokeWidth=16, cap="round")
# seal stamp: T-handle, pressed at the wax
d.shape("rectangle", "Stamp handle", x=508, y=492, width=36, height=14,
        fill="#5A4632", stroke=INK, strokeWidth=4, radius=6)
d.path("M522,506 L530,506 L532,529 L520,529 Z", "Stamp neck", fill="#5A4632",
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Stamp head", x=510, y=525, width=32, height=16,
        fill=BRASS, stroke=INK, strokeWidth=3)

# --- captions ------------------------------------------------------------------
d.text("SEALWARD PROXY-9", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#CCD4EE", justify="center")
r = d.text("WITNESS MARK CUSTODIAN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#98A4CE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("677.sealward-proxy-9-V1R00")
