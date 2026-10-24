#!/usr/bin/env python3
"""MAP-72 Absentia — mascot portrait V1R00.
Ghost mascot appending a confident final sentence to an unchanged file.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("MAP-72 Absentia — Mascot Portrait", 1000, 1000)

INK = "#1E2A26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1614"}, {"offset": 1, "color": "#050B0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5E52"}, {"offset": 0.7, "color": "#283E36"},
    {"offset": 1, "color": "#16241E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#22382E"}, {"offset": 1, "color": "#0E1A14"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE4CC"}, {"offset": 1, "color": "#C9BC96"}]}}
GHOST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D4EEE2"}, {"offset": 0.7, "color": "#9AC4B0"},
    {"offset": 1, "color": "#5E8A76"}]}}
FOLDER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3E52"}, {"offset": 1, "color": "#2E2636"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8A76", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE8DC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(800,230,7),(158,524,9),(836,545,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,390,7),
                               (391,113,7),(614,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A5A4C", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1610",
       strokeWidth=4, opacity=70)

# --- exception-queue folder behind the document ----------------------------------
d.shape("rectangle", "Queue folder", x=500, y=330, width=250, height=180,
        fill=FOLDER, stroke=INK, strokeWidth=5, radius=8)
d.path("M500,338 L560,338 L575,355 L500,355 Z", "Folder tab",
       fill="#4A3E52", stroke=INK, strokeWidth=4, join="round")
d.text("EXCEPTION QUEUE", "Folder label", x=580, y=400, size=14,
       font="Virelai Sans", color="#7E7490", justify="left")
d.text("RE-ENTRY: ATTEMPTED", "Folder line 2", x=580, y=424, size=11,
       font="Virelai Sans", color="#5E5470", justify="left")

# --- the unchanged file, one confident sentence being appended ----------------------
d.shape("ellipse", "Doc shadow", x=445, y=660, width=320, height=30,
        fill="#081410", opacity=50, stroke=NONE)
d.path("M450,400 L745,415 L730,665 L435,650 Z", "Document",
       fill=PAPER, stroke=INK, strokeWidth=5, join="round")
# unchanged lines: faded, identical
for i in range(6):
    w = [250, 265, 240, 258, 200, 262][i]
    d.shape("rectangle", f"Line {i+1}", x=470, y=440+i*26, width=w, height=8,
            fill="#9A8E72", opacity=55, stroke=NONE, radius=4)
# gap, then the confident final sentence in fresh ink
d.shape("ellipse", "Line glow", x=455, y=588, width=250, height=34,
        fill="#8EE8B8", opacity=18, stroke=NONE)
d.shape("rectangle", "Final sentence", x=468, y=600, width=215, height=12,
        fill="#3E8A62", stroke=NONE, radius=6)
d.text("the file is complete.", "Final text", x=470, y=638, size=15,
       font="Virelai Sans", color="#2E5E46", justify="left")
# corner fold
d.path("M745,415 L716,418 L742,445 Z", "Page fold", fill="#C9BC96",
       stroke=INK, strokeWidth=3, join="round")

# --- MAP-72: the ghost clerk, pen in hand -------------------------------------------
d.shape("ellipse", "Ghost halo", x=180, y=230, width=280, height=300,
        fill="#B8E8D0", opacity=10, stroke=NONE)
# spectral body, wavy hem
d.path("M320,255 C395,255 435,315 435,390 L435,510 "
       "C420,495 405,525 390,510 C375,495 360,525 345,510 "
       "C330,495 315,525 300,510 C285,495 270,525 258,505 "
       "L258,390 C258,315 245,255 320,255 Z",
       "Ghost body", fill=GHOST, stroke=INK, strokeWidth=6, opacity=88)
# translucency cues: internal shade + highlight
d.shape("ellipse", "Ghost hi", x=285, y=290, width=110, height=45,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M272,470 C300,490 390,490 420,470", "Hem shade", fill=NONE,
       stroke="#5E8A76", strokeWidth=8, cap="round", opacity=40)
# vacant serene face
d.shape("ellipse", "Eye L", x=295, y=350, width=22, height=30,
        fill="#1E2A26", stroke=NONE)
d.shape("ellipse", "Eye R", x=375, y=350, width=22, height=30,
        fill="#1E2A26", stroke=NONE)
d.shape("ellipse", "Eye void L", x=300, y=358, width=8, height=8,
        fill="#8EE8B8", opacity=80, stroke=NONE)
d.shape("ellipse", "Eye void R", x=380, y=358, width=8, height=8,
        fill="#8EE8B8", opacity=80, stroke=NONE)
d.path("M325,415 C338,424 352,424 365,415", "Calm mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# arm extending to the document, holding a pen
d.path("M430,470 C465,490 495,520 520,555", "Pen arm", fill=NONE,
       stroke="#9AC4B0", strokeWidth=15, cap="round", opacity=90)
# the pen, nib on the final line
d.path("M520,548 L575,612 L565,622 L512,558 Z", "Pen", fill="#2E2636",
       stroke=INK, strokeWidth=4, join="round")
d.path("M565,622 L583,612 L575,612 Z", "Nib", fill="#E8C25E",
       stroke=INK, strokeWidth=3, join="round")
# spectral drips rising off the crown
d.path("M290,252 C282,232 292,215 285,198", "Drip L", fill=NONE,
       stroke="#9AC4B0", strokeWidth=8, cap="round", opacity=60)
d.path("M335,250 C340,228 330,212 338,192", "Drip R", fill=NONE,
       stroke="#9AC4B0", strokeWidth=8, cap="round", opacity=55)

# --- captions ------------------------------------------------------------------
d.text("MAP-72 ABSENTIA", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#CFE8DC", justify="center")
r = d.text("CLERK OF GOVERNED GAPS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8EB4A2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("672.map-72-absentia-V1R00")
