#!/usr/bin/env python3
"""Variance Pastor — mascot portrait V1R00.
On a stage, a robed mascot blesses a trembling server rack; a dashboard
panel nearby shows the metric wobbling inside its tolerance band.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Variance Pastor — Mascot Portrait", 1000, 1000)

INK = "#2E211A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131824"}, {"offset": 1, "color": "#07090F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#76839B"}, {"offset": 0.7, "color": "#57627C"},
    {"offset": 1, "color": "#343D52"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5636"}, {"offset": 1, "color": "#3A291C"}]}}
RACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#424A58"}, {"offset": 1, "color": "#242A34"}]}}
UNIT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#525C6C"}, {"offset": 1, "color": "#39404E"}]}}
ROBE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E9D8"}, {"offset": 0.7, "color": "#DECBAF"},
    {"offset": 1, "color": "#B3997A"}]}}
STOLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9A45C"}, {"offset": 1, "color": "#96753A"}]}}
SCREEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E3440"}, {"offset": 1, "color": "#10202A"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E9F1EE"}, {"offset": 1, "color": "#BCCFCC"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#95A2B8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE4F0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#454F66", opacity=45, stroke=NONE)

# --- the stage: floor segment closed on the disc's own arc --------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Stage floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Stage edge", fill=NONE, stroke="#1C130C",
       strokeWidth=4, opacity=70)
d.path("M156,706 L844,706", "Stage edge light", fill=NONE, stroke="#C89A62",
       strokeWidth=2, opacity=45)
# plank seams running to the rim
for x, x2 in [(250,232),(350,338),(500,500),(650,662),(750,768)]:
    d.path(f"M{x},700 L{x2},848" if x == 500 else f"M{x},700 L{x2},840",
           f"Plank seam {x}", fill=NONE, stroke="#241810", strokeWidth=3,
           opacity=55)
# footlights along the stage front
for i, x in enumerate([280,390,500,610,720]):
    d.shape("ellipse", f"Footlight glow {i+1}", x=x-16, y=746, width=32,
            height=20, fill="#F0C878", opacity=22, stroke=NONE)
    d.shape("ellipse", f"Footlight {i+1}", x=x-5, y=748, width=10, height=10,
            fill="#F6DCA0", stroke="#8A6238", strokeWidth=2)

# --- dashboard panel: the metric inside its tolerance band ---------------------
d.shape("ellipse", "Screen glow", x=140, y=170, width=310, height=210,
        fill="#7AC8DC", opacity=10, stroke=NONE)
d.shape("rectangle", "Screen bezel", x=165, y=195, width=260, height=150,
        fill="#261E18", stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Screen", x=180, y=210, width=230, height=120,
        fill=SCREEN_GRAD, stroke="#0C161C", strokeWidth=3, radius=4)
# window chrome
for i, c in enumerate(["#B86A5C", "#E0A05C", "#84E2A4"]):
    d.shape("ellipse", f"Chrome dot {i+1}", x=192+i*14, y=218, width=7,
            height=7, fill=c, opacity=85, stroke=NONE)
# tolerance band + wobbling metric
d.shape("rectangle", "Tolerance band", x=186, y=252, width=218, height=46,
        fill="#3A5A68", opacity=25, stroke=NONE)
d.path("M186,252 L404,252 M186,298 L404,298", "Tolerance lines", fill=NONE,
       stroke="#4E7280", strokeWidth=2.5, opacity=70)
d.path("M190,278 C215,268 232,292 258,280 C284,268 302,294 328,282 "
       "C352,271 372,290 400,279", "Metric wave", fill=NONE,
       stroke="#A8E0EA", strokeWidth=4, cap="round")
d.shape("ellipse", "Metric dot glow", x=391, y=270, width=18, height=18,
        fill="#A8E0EA", opacity=35, stroke=NONE)
d.shape("ellipse", "Metric dot", x=396, y=275, width=9, height=9,
        fill="#D8F4F8", stroke=NONE)
# mini bars: forgiven wobbles, bottom right of the screen
for i, h in enumerate([10, 16, 7]):
    d.shape("rectangle", f"Mini bar {i+1}", x=360+i*13, y=315-h, width=8,
            height=h, fill="#6A94A0", opacity=80, stroke=NONE)

# --- the server rack, trembling ------------------------------------------------
d.shape("ellipse", "Rack wobble halo", x=615, y=375, width=210, height=340,
        fill="#7A8AA0", opacity=10, stroke=NONE)
d.shape("rectangle", "Rack body", x=645, y=390, width=150, height=310,
        fill=RACK_GRAD, stroke=INK, strokeWidth=5, radius=8)
# top status dome
d.shape("ellipse", "Rack dome", x=700, y=378, width=40, height=22,
        fill="#525C6C", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Dome light", x=715, y=382, width=10, height=10,
        fill="#F2C86A", stroke=NONE)
# five units with LEDs and vents
led = ["#84E2A4", "#84E2A4", "#F2C86A", "#84E2A4", "#84E2A4"]
for i in range(5):
    y = 402 + i*57
    d.shape("rectangle", f"Unit {i+1}", x=657, y=y, width=126, height=46,
            fill=UNIT_GRAD, stroke="#1E232C", strokeWidth=3, radius=4)
    d.shape("ellipse", f"LED {i+1}a", x=666, y=y+8, width=7, height=7,
            fill=led[i], stroke=NONE)
    d.shape("ellipse", f"LED {i+1}b", x=666, y=y+20, width=7, height=7,
            fill=led[i], opacity=55, stroke=NONE)
    d.path(f"M690,{y+12} L770,{y+12} M690,{y+22} L770,{y+22} M690,{y+32} L770,{y+32}",
           f"Vents {i+1}", fill=NONE, stroke="#2A3038", strokeWidth=2.5,
           opacity=80)
# tremble marks, both flanks
d.path("M612,450 C602,472 602,500 612,522 M596,436 C582,468 582,510 596,542",
       "Tremble L", fill=NONE, stroke="#C8D4E2", strokeWidth=4, cap="round",
       opacity=60)
d.path("M818,455 C828,477 828,505 818,527 M834,440 C848,472 848,514 834,546",
       "Tremble R", fill=NONE, stroke="#C8D4E2", strokeWidth=4, cap="round",
       opacity=60)
d.path("M618,600 C610,618 610,640 618,658 M820,604 C828,622 828,644 820,662",
       "Tremble low", fill=NONE, stroke="#C8D4E2", strokeWidth=3.5,
       cap="round", opacity=40)
# contact shadow
d.shape("ellipse", "Rack shadow", x=640, y=694, width=165, height=18,
        fill="#100C08", opacity=45, stroke=NONE)

# --- the Pastor -----------------------------------------------------------------
d.shape("ellipse", "Pastor halo", x=330, y=290, width=340, height=420,
        fill="#F0D8A8", opacity=9, stroke=NONE)
# robe body
d.path("M430,470 C415,520 405,610 400,700 L600,700 C595,610 585,520 570,470 "
       "C555,448 445,448 430,470 Z", "Robe", fill=ROBE_GRAD, stroke=INK,
       strokeWidth=6)
# robe shading: left highlight, hem shadow
d.path("M435,485 C425,540 418,620 415,690 C430,700 445,700 455,690 "
       "C450,620 448,540 452,485 Z", "Robe highlight", fill="#FFFFFF",
       opacity=14, stroke=NONE)
d.path("M410,660 C460,678 540,678 592,660 L600,700 L400,700 Z",
       "Hem shadow", fill="#8A7054", opacity=30, stroke=NONE)
# hood
d.path("M500,315 C562,315 590,360 583,408 C578,442 545,462 500,462 "
       "C455,462 422,442 417,408 C410,360 438,315 500,315 Z",
       "Hood", fill=ROBE_GRAD, stroke=INK, strokeWidth=6)
d.path("M435,350 C445,330 470,322 500,322 C470,330 450,345 442,372 Z",
       "Hood sheen", fill="#FFFFFF", opacity=18, stroke=NONE)
# face
d.shape("ellipse", "Face", x=448, y=348, width=104, height=96,
        fill="#F6E9D2", stroke="#8A7054", strokeWidth=3)
# serene closed eyes + small mouth
d.path("M466,392 C474,398 484,398 492,392 M508,392 C516,398 526,398 534,392",
       "Closed eyes", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M490,420 C496,424 504,424 510,420", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
# laminated runbook stole: two ribbons + the card
d.path("M468,452 L452,535", "Stole L", fill=NONE, stroke=STOLE_GRAD,
       strokeWidth=16, cap="round")
d.path("M532,452 L548,535", "Stole R", fill=NONE, stroke=STOLE_GRAD,
       strokeWidth=16, cap="round")
d.shape("rectangle", "Runbook card", x=458, y=530, width=84, height=66,
        fill=CARD_GRAD, stroke=INK, strokeWidth=4, radius=5)
for i, w in enumerate([60, 52, 58]):
    d.shape("rectangle", f"Card line {i+1}", x=470, y=546+i*12, width=w,
            height=5, fill="#5A6A66", opacity=75, stroke=NONE, radius=2)
d.path("M466,592 L500,534 L518,534 L484,592 Z", "Lamination sheen",
       fill="#FFFFFF", opacity=20, stroke=NONE)
# blessing arm toward the rack
d.path("M562,485 C595,468 618,448 642,422", "Blessing arm", fill=NONE,
       stroke="#DECBAF", strokeWidth=26, cap="round")

d.shape("ellipse", "Blessing hand", x=632, y=402, width=32, height=26,
        fill="#F6E9D2", stroke=INK, strokeWidth=4)
# blessing rays falling on the rack + static spark at the fingertip
d.path("M655,432 L672,448 M664,418 L686,428 M672,404 L696,408",
       "Blessing rays", fill=NONE, stroke="#F0D08A", strokeWidth=4,
       cap="round", opacity=75)
d.path("M646,396 L654,388 M640,388 L658,402", "Static spark", fill=NONE,
       stroke="#F2C86A", strokeWidth=3.5, cap="round")
# lowered arm + static discharge to the stage before touching the rack
d.path("M438,492 C424,530 426,560 434,584", "Low arm", fill=NONE,
       stroke="#DECBAF", strokeWidth=24, cap="round")
d.shape("ellipse", "Low hand", x=424, y=578, width=24, height=20,
        fill="#F6E9D2", stroke=INK, strokeWidth=4)
d.path("M436,600 L444,614 L434,626 L442,640", "Static to ground", fill=NONE,
       stroke="#F2C86A", strokeWidth=3.5, cap="round", opacity=80)
# contact shadow
d.shape("ellipse", "Pastor shadow", x=395, y=694, width=210, height=20,
        fill="#100C08", opacity=40, stroke=NONE)
# dust motes in the stage light
for i, (x, y, w) in enumerate([(300,300,6),(640,300,5),(560,255,5),(700,330,6),
                               (360,255,5),(455,280,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E0EA", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------
d.text("VARIANCE PASTOR", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#EAE2D2", justify="center")
r = d.text("MINISTER OF MEASURED LENIENCY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B0A48C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("251.variance-pastor-V1R00")
