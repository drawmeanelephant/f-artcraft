#!/usr/bin/env python3
"""Gentle Rollback — mascot portrait V1R00.
A soft caretaker mascot draping a quilted apology blanket over a reverted
server tower while the downgrade script runs on its front panel; a 'sorry'
tag hangs from the hem and a lullaby note drifts off its smoothing hand.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Gentle Rollback — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A0F08"}, {"offset": 1, "color": "#0A0604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A5E46"}, {"offset": 0.7, "color": "#5E4230"},
    {"offset": 1, "color": "#33241A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3828"}, {"offset": 1, "color": "#221610"}]}}
SERVER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6458"}, {"offset": 1, "color": "#463E36"}]}}
BLANKET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D09580"}, {"offset": 0.6, "color": "#AE6E5C"},
    {"offset": 1, "color": "#8A5448"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E0C09A"}, {"offset": 0.7, "color": "#C09A70"},
    {"offset": 1, "color": "#96714E"}]}}
KERCHIEF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A6A8E"}, {"offset": 1, "color": "#57496B"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#B08A62", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCBC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4832", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140C08",
       strokeWidth=4, opacity=70)

# --- gentle scene halo ----------------------------------------------------------
d.shape("ellipse", "Scene halo", x=270, y=290, width=500, height=390,
        fill="#F0B06A", opacity=9, stroke=NONE)

# --- the reverted server tower ----------------------------------------------------
d.shape("ellipse", "Server shadow", x=560, y=684, width=260, height=22,
        fill="#0E0806", opacity=45, stroke=NONE)
d.shape("rectangle", "Server tower", x=560, y=288, width=240, height=412,
        fill=SERVER_GRAD, stroke=INK, strokeWidth=5, radius=16)
# drive bays peeking above the blanket
d.shape("rectangle", "Bay slot 1", x=584, y=300, width=192, height=10,
        fill="#2A2620", opacity=85, stroke=NONE, radius=5)
d.shape("rectangle", "Bay slot 2", x=584, y=314, width=140, height=9,
        fill="#2A2620", opacity=70, stroke=NONE, radius=4)
# power LED, still on, still sorry
d.shape("ellipse", "LED glow", x=764, y=298, width=20, height=20,
        fill="#E8A84E", opacity=25, stroke=NONE)
d.shape("ellipse", "Power LED", x=770, y=304, width=8, height=8,
        fill="#E8A84E", stroke=NONE)
# downgrade terminal on the lower front panel, below the blanket hem
d.shape("rectangle", "Terminal bezel", x=588, y=596, width=196, height=90,
        fill="#10161C", stroke=INK, strokeWidth=3, radius=8)
d.shape("rectangle", "Terminal screen", x=596, y=604, width=180, height=74,
        fill="#18222C", stroke=NONE, radius=4)
d.text("downgrade.sh", "Script name", x=686, y=622, size=13,
       font="Virelai Sans", color="#A8C898", justify="center")
d.shape("rectangle", "Progress track", x=606, y=636, width=160, height=10,
        fill="#0E1418", stroke="#3A4A44", strokeWidth=2, radius=5)
d.shape("rectangle", "Progress fill", x=606, y=636, width=88, height=10,
        fill="#C87A5A", stroke=NONE, radius=5)
d.path("M698,641 L706,637 L706,645 Z M708,641 L716,637 L716,645 Z",
       "Rollback chevrons", fill="#E8B08A", stroke=NONE)
# version digits must be Source Sans 3 — Virelai Sans has no digit glyphs
d.text("v2.4 -> v2.3", "Version", x=686, y=672, size=12,
       font="Source Sans 3", color="#9AB88E", justify="center")

# --- the mascot: soft caretaker ---------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=300, y=684, width=200, height=20,
        fill="#0E0806", opacity=45, stroke=NONE)
d.shape("ellipse", "Body", x=310, y=500, width=180, height=190,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Belly shade", x=340, y=560, width=130, height=110,
        fill="#8A6444", opacity=30, stroke=NONE)
for x in (335, 420):
    d.shape("ellipse", f"Foot {x}", x=x, y=676, width=64, height=26,
            fill="#96714E", stroke=INK, strokeWidth=4)
# raised arm reaching the blanket's top corner (blanket drawn over the grip)
d.path("M452,548 C474,506 492,446 501,392", "Arm raised", fill=NONE,
       stroke="#C09A70", strokeWidth=20, cap="round")
d.shape("ellipse", "Raised hand", x=492, y=372, width=22, height=20,
        fill="#C09A70", stroke=INK, strokeWidth=3.5)
# head + kerchief
d.shape("ellipse", "Head", x=330, y=356, width=132, height=130,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M332,396 C336,352 366,336 396,336 C426,336 456,352 460,396 "
       "C440,378 352,378 332,396 Z", "Kerchief", fill=KERCHIEF_GRAD,
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Kerchief knot", x=448, y=386, width=16, height=14,
        fill="#57496B", stroke=INK, strokeWidth=3)
d.path("M460,394 C470,400 474,410 472,420", "Kerchief tail", fill=NONE,
       stroke="#57496B", strokeWidth=7, cap="round")
# face: eyes closed, unhurried
d.path("M352,424 C360,432 372,432 380,424", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M412,424 C420,432 432,432 440,424", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M384,448 C392,456 402,456 410,448", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Blush L", x=346, y=436, width=18, height=10,
        fill="#C8846A", opacity=55, stroke=NONE)
d.shape("ellipse", "Blush R", x=428, y=436, width=18, height=10,
        fill="#C8846A", opacity=55, stroke=NONE)

# --- the quilted apology blanket, draped over the server ---------------------------
d.path("M505,368 C545,330 600,320 664,322 L800,322 "
       "C818,322 828,336 828,356 L828,516 "
       "C818,552 798,552 788,522 C778,552 758,552 748,522 "
       "C738,552 718,552 708,522 C698,552 678,552 668,522 "
       "C658,552 638,552 628,522 C618,552 598,552 588,522 "
       "C578,552 558,552 548,522 C538,548 516,548 510,524 "
       "L514,430 C516,402 512,384 505,368 Z",
       "Apology blanket", fill=BLANKET_GRAD, stroke=INK, strokeWidth=5)
# quilt patches, quilted from prior announcements
for i, (x, y, w, h, c, o) in enumerate([
        (560, 348, 70, 44, "#E0B088", 50), (690, 338, 64, 46, "#A8B890", 45),
        (632, 414, 72, 46, "#B06058", 45), (748, 412, 66, 46, "#E4D0A8", 50),
        (560, 478, 72, 40, "#A87A88", 45), (706, 478, 60, 40, "#C89858", 40)]):
    d.shape("rectangle", f"Patch {i+1}", x=x, y=y, width=w, height=h,
            fill=c, opacity=o, stroke="#F0D8C0", strokeWidth=1.5, radius=8)
# stitched seams following the drape
for i, x in enumerate([604, 686, 766]):
    d.path(f"M{x},326 C{x-2},390 {x-2},460 {x},536", f"Seam V{i+1}",
           fill=NONE, stroke="#F0D8C0", strokeWidth=2.5, opacity=50)
for i, y in enumerate([398, 468]):
    d.path(f"M516,{y-4} C640,{y-8} 760,{y-8} 826,{y}", f"Seam H{i+1}",
           fill=NONE, stroke="#F0D8C0", strokeWidth=2.5, opacity=50)
# one patch is a heart
d.path("M660,376 C656,370 648,372 648,379 C648,385 660,392 660,392 "
       "C660,392 672,385 672,379 C672,372 664,370 660,376 Z",
       "Heart patch", fill="#B86058", stroke=NONE)
# fingers over the held corner
d.shape("ellipse", "Grip", x=494, y=362, width=24, height=18,
        fill="#C09A70", stroke=INK, strokeWidth=3.5)

# --- the 'sorry' tag, tied to the hem ---------------------------------------------
d.path("M540,548 C534,560 528,570 520,578", "Tag string", fill=NONE,
       stroke=INK, strokeWidth=2.5)
d.shape("rectangle", "Sorry tag", x=480, y=578, width=58, height=26,
        fill="#E8DCC8", stroke=INK, strokeWidth=2.5, radius=6)
d.text("sorry", "Tag text", x=509, y=596, size=13,
       font="Virelai Sans", color="#5A4632", justify="center")

# --- smoothing arm over the blanket + lullaby notes ---------------------------------
d.path("M468,572 C496,556 522,528 542,500", "Arm smoothing", fill=NONE,
       stroke="#C09A70", strokeWidth=18, cap="round")
d.shape("ellipse", "Smoothing hand", x=534, y=490, width=20, height=17,
        fill="#C09A70", stroke=INK, strokeWidth=3.5)
d.path("M548,478 C562,470 578,468 592,471", "Stroke arc 1", fill=NONE,
       stroke="#F0D0B8", strokeWidth=3, cap="round", opacity=60)
d.path("M544,506 C558,499 574,497 586,499", "Stroke arc 2", fill=NONE,
       stroke="#F0D0B8", strokeWidth=3, cap="round", opacity=45)
# lullaby notes drifting off, paced to the progress bar
for i, (cx, cy, o) in enumerate([(462, 316, 75), (430, 288, 55)]):
    d.path(rot_rect_path(cx, cy, 16, 11, -15), f"Note head {i+1}",
           fill="#F0C898", opacity=o, stroke=NONE)
    d.path(f"M{cx+8},{cy-4} L{cx+8},{cy-32} C{cx+16},{cy-28} "
           f"{cx+20},{cy-22} {cx+20},{cy-14}", f"Note stem {i+1}",
           fill=NONE, stroke="#F0C898", strokeWidth=3, cap="round",
           opacity=o)

# --- stray warm motes ---------------------------------------------------------------
for i, (x, y, w) in enumerate([(300,430,6),(250,540,5),(530,300,5),(840,470,6),
                               (220,640,6),(830,620,5),(460,250,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0C898", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("GENTLE ROLLBACK", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E2CE", justify="center")
r = d.text("THE APOLOGY LANDS FIRST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A884", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("263.gentle-rollback-V1R00")
