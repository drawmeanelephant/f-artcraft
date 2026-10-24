#!/usr/bin/env python3
"""Agent McCrisp — mascot portrait V1R00.
A Northern Spy in a trenchcoat lined with cinnamon shavings, filing
records away in a shadowed silo. Stealth operative.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Agent McCrisp — Mascot Portrait", 1000, 1000)

INK = "#2C211C"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#171009"}, {"offset": 1, "color": "#070403"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C4634"}, {"offset": 0.7, "color": "#3A2A1E"},
    {"offset": 1, "color": "#1C120C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#4A3626"}, {"offset": 1, "color": "#241812"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C85A48"}, {"offset": 0.7, "color": "#A83C30"},
    {"offset": 1, "color": "#7A2A24"}]}}
COAT_GRAD = {"gradient": {"kind": "linear", "start": [0, 430], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#6E6248"}, {"offset": 1, "color": "#3C3524"}]}}
HAT_GRAD = {"gradient": {"kind": "linear", "start": [0, 340], "end": [0, 430], "stops": [
    {"offset": 0, "color": "#5A4632"}, {"offset": 1, "color": "#34281C"}]}}
FOLDER = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 60], "stops": [
    {"offset": 0, "color": "#E8CFA0"}, {"offset": 1, "color": "#C2A472"}]}}
CINN = "#B4683A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A5E44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8BF98", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,240,8),(800,232,7),(160,520,9),(832,545,8),
                               (246,764,7),(754,748,9),(134,392,6),(862,392,7),
                               (392,114,7),(612,112,8),(334,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#54402C", opacity=45, stroke=NONE)

# --- silo interior: curved wall seams, ribs, rivets ------------------------------
# wall seams bow outward like riveted plates
d.path("M215,140 C185,330 185,540 215,720", "Wall seam L", fill=NONE,
       stroke="#241811", strokeWidth=5, opacity=60)
d.path("M785,140 C815,330 815,540 785,720", "Wall seam R", fill=NONE,
       stroke="#241811", strokeWidth=5, opacity=60)
for i, (x, y) in enumerate([(212,220),(204,330),(204,450),(212,570),(788,220),
                            (796,330),(796,450),(788,570)]):
    d.shape("ellipse", f"Rivet {i+1}", x=x-4, y=y-4, width=8, height=8,
            fill="#6A4E34", opacity=70, stroke=NONE)
# light shaft from the overhead hatch
d.path("M420,64 L580,64 L660,700 L340,700 Z", "Light shaft",
       fill="#E8C88A", opacity=10, stroke=NONE)
d.path("M452,64 L548,64 L590,700 L410,700 Z", "Light shaft core",
       fill="#F2D8A0", opacity=9, stroke=NONE)
# dust motes drifting in the shaft
for i, (x, y, w, o) in enumerate([(430,200,6,50),(520,170,5,45),(470,300,7,55),
                                  (560,330,5,40),(440,430,6,45),(580,470,5,40),
                                  (500,540,6,50)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0D9A8", opacity=o, stroke=NONE)
# a ladder climbing into shadow, far left
for i in range(6):
    y = 250 + i*62
    d.path(f"M150,{y} L196,{y}", f"Rung {i+1}", fill=NONE, stroke="#4A3626",
           strokeWidth=5, opacity=60)
d.path("M150,220 L150,640 M196,220 L196,640", "Ladder rails", fill=NONE,
       stroke="#4A3626", strokeWidth=5, opacity=60)
# stenciled bay mark, half lost to shadow
d.text("BAY 7", "Bay stencil", x=640, y=250, size=30, font="Virelai Sans",
       color="#5A4530", justify="left")

# --- floor of the silo, closed on the disc's arc ---------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#1E130D",
       strokeWidth=4, opacity=60)

# --- filing drawer sunk into the wall, one tray open ------------------------------
d.shape("ellipse", "Cabinet shadow", x=640, y=676, width=190, height=24,
        fill="#120A06", opacity=50, stroke=NONE)
d.shape("rectangle", "Cabinet", x=650, y=480, width=160, height=200,
        fill="#3C2E20", stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Drawer top", x=662, y=496, width=136, height=52,
        fill="#2C211A", stroke=INK, strokeWidth=4, radius=5)
d.shape("rect", "Drawer pull", x=706, y=514, width=48, height=14,
        fill="#8A6A48", stroke=INK, strokeWidth=3, radius=6)
# open lower drawer with record cards
d.shape("rectangle", "Drawer open", x=630, y=568, width=168, height=56,
        fill="#4E3C28", stroke=INK, strokeWidth=5, radius=5)
for i, (x, h) in enumerate([(648,26),(664,32),(680,22),(696,30),(712,26),(728,34),(748,24)]):
    d.shape("rectangle", f"Card {i+1}", x=x, y=568-h, width=14, height=h,
            fill="#E4CFA4", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Drawer face", x=630, y=624, width=168, height=50,
        fill="#34281C", stroke=INK, strokeWidth=4, radius=5)
d.shape("rectangle", "Drawer label", x=694, y=636, width=40, height=16,
        fill="#C2A472", stroke=INK, strokeWidth=3, radius=3)

# --- Agent McCrisp ----------------------------------------------------------------
d.shape("ellipse", "McCrisp shadow", x=335, y=672, width=250, height=30,
        fill="#120A06", opacity=50, stroke=NONE)
# trenchcoat body: belted, hem flaring to the floor line
d.path("M430,470 C510,470 570,530 580,610 C585,650 582,676 576,690 "
       "L350,690 C344,676 341,650 346,610 C356,530 360,470 430,470 Z",
       "Coat", fill=COAT_GRAD, stroke=INK, strokeWidth=6, join="round")
# coat shading on the shadow side
d.path("M352,600 C360,540 380,505 410,490 L400,690 L360,690 C350,660 348,630 352,600 Z",
       "Coat shade", fill="#28221A", opacity=50, stroke=NONE)
# belt
d.path("M352,606 L578,606 L578,634 L352,634 Z", "Belt", fill="#2A221A",
       stroke=INK, strokeWidth=4)
d.shape("rectangle", "Buckle", x=445, y=606, width=40, height=28,
        fill="#A8865A", stroke=INK, strokeWidth=4, radius=4)
# right arm extended, slipping a record card into the open drawer
d.path("M566,540 C610,545 640,555 662,570", "Arm R", fill=NONE,
       stroke="#5A5040", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand R", x=656, y=560, width=26, height=22,
        fill="#B44A3C", stroke=INK, strokeWidth=4)
# the record card mid-filing
d.shape("rectangle", "Filed card", x=668, y=540, width=52, height=34,
        fill="#EDDCB4", stroke=INK, strokeWidth=3, radius=3)
d.path("M676,552 L712,552 M676,562 L704,562", "Card lines", fill=NONE,
       stroke="#8A6A48", strokeWidth=2, opacity=80)
# left hand holding the manila folder at the chest
d.shape("rectangle", "Folder", x=300, y=560, width=120, height=88,
        fill=FOLDER, stroke=INK, strokeWidth=4, radius=5)
d.path("M300,578 L420,578", "Folder seam", fill=NONE, stroke="#9A7E52",
       strokeWidth=3, opacity=80)
d.shape("rectangle", "Folder tab", x=320, y=548, width=52, height=16,
        fill=FOLDER, stroke=INK, strokeWidth=3, radius=3)
d.text("N-SPY", "Tab text", x=328, y=561, size=12, font="Virelai Sans",
       color="#6A4E2C", justify="left")
d.shape("ellipse", "Hand L", x=312, y=580, width=30, height=24,
        fill="#B44A3C", stroke=INK, strokeWidth=4)

# collar popped: trench wings around the jaw
d.path("M358,505 L400,440 L436,470 L400,540 Z", "Collar L",
       fill="#5A5040", stroke=INK, strokeWidth=5, join="round")
d.path("M560,505 L520,440 L486,470 L522,540 Z", "Collar R",
       fill="#5A5040", stroke=INK, strokeWidth=5, join="round")
# face: the Northern Spy under the brim
d.shape("ellipse", "Face", x=392, y=380, width=140, height=130,
        fill=FACE_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Face hi", x=414, y=398, width=48, height=22,
        fill="#F4C9A8", opacity=25, stroke=NONE)
# shadow band the brim casts over the eyes
d.path("M392,436 C420,424 504,424 532,436 L532,452 C504,440 420,440 392,452 Z",
       "Brim shadow", fill="#4A1410", opacity=45, stroke=NONE)
# wary operative eyes under the shadow
d.shape("ellipse", "Eye L", x=420, y=450, width=22, height=26,
        fill="#F4E4D4", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=428, y=460, width=9, height=11,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=482, y=450, width=22, height=26,
        fill="#F4E4D4", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil R", x=486, y=460, width=9, height=11,
        fill=INK, stroke=NONE)
d.path("M416,438 C426,430 440,429 448,434", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M478,432 C490,426 504,429 510,437", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# small flat unreadable mouth
d.path("M446,494 C458,490 470,490 480,494", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# cinnamon shavings curling out of the collar lining
def curl(x, y, s, label):
    segs = [(10,-8,22,-2,18,10), (-3,9,-16,10,-18,2), (-1,-6,8,-9,12,-4)]
    p = f"M{x},{y} " + " ".join(f"c{a*s},{b} {c*s},{dd} {e*s},{f}"
                               for a, b, c, dd, e, f in segs)
    d.path(p, label, fill=NONE, stroke=CINN, strokeWidth=5, cap="round")
curl(388, 470, 1, "Cinnamon curl 1")
curl(414, 492, 1, "Cinnamon curl 2")
curl(532, 464, -1, "Cinnamon curl 3")
curl(506, 490, -1, "Cinnamon curl 4")
# shavings spilling down the coat's front edge
curl(452, 560, 1, "Cinnamon curl 5")
curl(486, 576, -1, "Cinnamon curl 6")
# one caught on the folder's edge
curl(396, 556, 1, "Cinnamon curl 7")

# fedora: brim + creased crown
d.path("M350,400 C400,378 520,378 566,398 C574,402 572,412 562,412 "
       "L352,414 C342,412 342,404 350,400 Z",
       "Brim", fill=HAT_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M396,392 C398,336 414,312 460,310 C506,308 524,336 526,392 "
       "C500,402 424,402 396,392 Z",
       "Crown", fill=HAT_GRAD, stroke=INK, strokeWidth=5, join="round")
# crown crease + band
d.path("M462,314 C474,330 476,356 470,378", "Crease", fill=NONE,
       stroke="#241A12", strokeWidth=4, opacity=70)
d.path("M398,376 C430,386 492,386 524,376 L524,392 C492,402 430,402 398,392 Z",
       "Hat band", fill="#241A12", stroke=NONE, opacity=85)

# --- captions -------------------------------------------------------------------
d.text("AGENT MCCRISP", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E4CFA4", justify="center")
r = d.text("STEALTH OPERATIVE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B09A72", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("221.mccrisp-agent-V1R00")
