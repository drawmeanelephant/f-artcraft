#!/usr/bin/env python3
"""Servicey Unavailabelle — mascot portrait V1R00.
Mascot resting beside a humming server; status line reads 503, Retry-After
set three days out. 1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Servicey Unavailabelle — Mascot Portrait", 1000, 1000)

INK = "#26202E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131018"}, {"offset": 1, "color": "#07060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E4468"}, {"offset": 0.7, "color": "#342E48"},
    {"offset": 1, "color": "#1E1A2E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2440"}, {"offset": 1, "color": "#141024"}]}}
SERVER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A5478"}, {"offset": 1, "color": "#322C48"}]}}
SERVICEY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2CDA4"}, {"offset": 0.72, "color": "#D9A878"},
    {"offset": 1, "color": "#B37E54"}]}}
PILLOW = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A80B0"}, {"offset": 1, "color": "#565078"}]}}
MASK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4468"}, {"offset": 1, "color": "#2E2848"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E6494", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D0EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,231,7),(157,524,9),(837,543,8),
                               (247,767,7),(753,749,9),(133,393,6),(865,391,7),
                               (391,113,7),(613,111,8),(333,823,6),(666,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#443C60", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#100C1E",
       strokeWidth=4, opacity=70)

# --- humming server tower -------------------------------------------------------
d.shape("ellipse", "Server shadow", x=590, y=668, width=230, height=28,
        fill="#0A0616", opacity=50, stroke=NONE)
d.shape("rectangle", "Server", x=600, y=330, width=200, height=345,
        fill=SERVER, stroke=INK, strokeWidth=6, radius=12)
# hum ticks on the left flank
for i, (y, l) in enumerate([(380,26),(440,34),(500,26),(560,34),(620,26)]):
    d.path(f"M{582-l},{y} C{582-l-8},{y-8} {582-l-8},{y+8} {582-l},{y+16}",
           f"Hum {i+1}", fill=NONE, stroke="#9A8EC8", strokeWidth=4,
           cap="round", opacity=55)
# status display
d.shape("rectangle", "Status screen", x=618, y=352, width=164, height=86,
        fill="#171226", stroke=INK, strokeWidth=4, radius=6)
d.text("STATUS 503", "Status 503", x=632, y=378, size=16, font="Virelai Sans",
       color="#E89A62", justify="left")
d.text("RETRY-AFTER:", "Retry label", x=632, y=400, size=11,
       font="Virelai Sans", color="#8E84B4", justify="left")
d.text("SUN (+3D)", "Retry date", x=632, y=420, size=13,
       font="Virelai Sans", color="#E8D8A8", justify="left")
# drive bays + LEDs
for i in range(3):
    d.shape("rectangle", f"Bay {i+1}", x=618, y=462+i*52, width=164, height=40,
            fill="#3A3454", stroke=INK, strokeWidth=3, radius=5)
    d.shape("ellipse", f"Bay LED {i+1}", x=762, y=474+i*52, width=10, height=10,
            fill="#7EE0A8" if i < 2 else "#E8C25E", stroke=NONE)
    d.shape("rectangle", f"Bay slot {i+1}", x=630, y=478+i*52, width=90, height=6,
            fill="#221E38", stroke=NONE, radius=3)
# feet
d.shape("rectangle", "Foot L", x=620, y=675, width=30, height=20,
        fill="#322C48", stroke=INK, strokeWidth=4, radius=5)
d.shape("rectangle", "Foot R", x=750, y=675, width=30, height=20,
        fill="#322C48", stroke=INK, strokeWidth=4, radius=5)

# --- OUT OF OFFICE tent sign ------------------------------------------------------
d.path("M535,636 L580,636 L597,700 L518,700 Z", "OOO sign", fill="#E8DCC0",
       stroke=INK, strokeWidth=4, join="round")
d.text("OUT OF", "Sign line 1", x=541, y=668, size=10, font="Virelai Sans",
       color="#6A5A40", justify="left")
d.text("OFFICE", "Sign line 2", x=543, y=684, size=10, font="Virelai Sans",
       color="#6A5A40", justify="left")

# --- Servicey, reclining: head on pillow, mask pushed up ---------------------------
d.shape("ellipse", "Serv shadow", x=215, y=668, width=320, height=30,
        fill="#0A0616", opacity=50, stroke=NONE)
# pillow under the head
d.path("M225,640 C215,605 255,585 305,585 C360,585 395,608 390,645 "
       "C385,672 240,672 225,640 Z",
       "Pillow", fill=PILLOW, stroke=INK, strokeWidth=5)
d.path("M245,620 C270,608 320,606 350,618", "Pillow crease", fill=NONE,
       stroke="#443E66", strokeWidth=4, cap="round", opacity=60)
# reclined body: long bean, head up at left
d.path("M300,555 C360,540 430,555 470,585 C510,615 520,650 505,675 "
       "C480,705 380,705 335,690 C300,678 282,640 288,600 "
       "C290,580 292,562 300,555 Z",
       "Serv body", fill=SERVICEY, stroke=INK, strokeWidth=6)
# belly highlight + underside shade
d.shape("ellipse", "Body hi", x=340, y=580, width=130, height=45,
        fill="#FFFFFF", opacity=16, stroke=NONE)
d.path("M310,672 C360,688 440,688 490,668 C440,680 360,680 310,672 Z",
       "Body shade", fill="#8A5E42", opacity=45, stroke=NONE)
# head dome
d.path("M272,555 C240,540 228,500 240,470 C252,440 285,425 315,435 "
       "C345,445 358,478 350,508 C342,540 305,570 272,555 Z",
       "Serv head", fill=SERVICEY, stroke=INK, strokeWidth=6)
# sleep mask pushed up on the forehead
d.path("M246,468 C250,442 275,428 305,432 C330,436 342,452 342,470 "
       "C320,458 268,456 246,468 Z",
       "Sleep mask", fill=MASK, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Mask strap", x=238, y=464, width=10, height=18,
        fill=MASK, stroke=INK, strokeWidth=3)
# face: content closed eyes, small smile, tiny fang-free grin
d.path("M272,498 C278,505 288,505 294,498", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M308,500 C314,507 324,507 330,500", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M288,524 C300,532 318,532 330,524", "Smile", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# blush
d.shape("ellipse", "Blush", x=320, y=512, width=20, height=11,
        fill="#E89A7E", opacity=50, stroke=NONE)
# stubby foot + resting arm
d.shape("ellipse", "Foot", x=490, y=640, width=34, height=40,
        fill="#B37E54", stroke=INK, strokeWidth=4)
d.path("M420,600 C440,610 450,628 446,648", "Resting arm", fill=NONE,
       stroke="#B37E54", strokeWidth=15, cap="round")
# drifting z's
d.text("z", "Z1", x=220, y=420, size=26, font="Virelai Sans",
       color="#B4A8D8", justify="left")
d.text("z", "Z2", x=196, y=382, size=34, font="Virelai Sans",
       color="#B4A8D8", justify="left")
d.text("z", "Z3", x=168, y=336, size=44, font="Virelai Sans",
       color="#B4A8D8", justify="left")

# --- captions ------------------------------------------------------------------
d.text("SERVICEY UNAVAILABELLE", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#D8D0EC", justify="center")
r = d.text("SYSTEM VACATION SCHEDULER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A094CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("503.servicey-unavailabelle-V1R00")
