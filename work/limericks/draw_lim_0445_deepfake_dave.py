#!/usr/bin/env python3
"""LIM-0445 Deepfake Dave — limerick plate V1R00. The evidence sways:
Dave offers a sample card to the synth node, whose monitor grows a face
out of pixels while the alibi reel plays; above, the scales of justice
tilt between two identical exhibits — the court can't tell which is true.
Teal render-farm palette. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0445 Deepfake Dave — Limerick Plate", 1000, 1000)

INK = "#1E2428"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1A18"}, {"offset": 1, "color": "#050D0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E6B66"}, {"offset": 0.7, "color": "#24463F"},
    {"offset": 1, "color": "#0F221F"}]}}
DAVE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A6EB8"}, {"offset": 0.7, "color": "#5E4A86"},
    {"offset": 1, "color": "#3A2E58"}]}}
CLAP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4450"}, {"offset": 1, "color": "#22262E"}]}}
MACHINE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4A54"}, {"offset": 1, "color": "#222A30"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14302C"}, {"offset": 1, "color": "#0A1C1A"}]}}
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0D0A8"}, {"offset": 1, "color": "#C09870"}]}}
ICE = "#DCF2EE"
SOFT = "#8FC4BA"
TEAL = "#7FE8D8"
RED = "#E86A5E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6FB3A8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE8E0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190, 210, 8), (805, 200, 7), (150, 480, 9),
                               (848, 550, 8), (225, 795, 7), (775, 775, 9),
                               (140, 350, 6), (860, 360, 7), (400, 108, 7),
                               (600, 105, 8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#356058", opacity=45, stroke=NONE)

# --- the scales of justice, swaying between two identical exhibits ---------------
sc_ids = []
def sc_add(res):
    if res and res.get("id"):
        sc_ids.append(res["id"])
# post + finial
sc_add(d.path("M430,148 L430,232", "Scale post", fill=NONE,
              stroke="#C9B98E", strokeWidth=5, cap="round"))
sc_add(d.shape("ellipse", "Scale finial", x=422, y=136, width=16,
               height=16, fill="#C9B98E", stroke=INK, strokeWidth=2))
# tilted beam — the evidence sways
sc_add(d.path("M330,196 L530,180", "Scale beam", fill=NONE,
              stroke="#C9B98E", strokeWidth=5, cap="round"))
# pan strings + dishes; Exhibit A hangs low, Exhibit B rides high
for i, (px, py) in enumerate([(330, 196), (530, 180)]):
    sc_add(d.path(f"M{px},{py} L{px - 26},{py + 52} M{px},{py} "
                  f"L{px + 26},{py + 52}", f"Strings {i+1}", fill=NONE,
                  stroke="#C9B98E", strokeWidth=2.5))
    sc_add(d.path(f"M{px - 34},{py + 52} A34,18 0 0 0 {px + 34},{py + 52} "
                  f"L{px - 34},{py + 52} Z", f"Pan {i+1}",
                  fill={"gradient": {"kind": "linear", "stops": [
                      {"offset": 0, "color": "#C9B98E"},
                      {"offset": 1, "color": "#8A7C56"}]}},
                  stroke=INK, strokeWidth=2.5, join="round"))
    # an identical face card rides each pan
    sc_add(d.shape("ellipse", f"Exhibit face {i+1}", x=px - 16,
                   y=py + 16, width=32, height=32, fill=FACE,
                   stroke=INK, strokeWidth=2))
    sc_add(d.shape("ellipse", f"Exhibit eye L{i+1}", x=px - 8,
                   y=py + 26, width=5, height=6, fill=INK, stroke=NONE))
    sc_add(d.shape("ellipse", f"Exhibit eye R{i+1}", x=px + 3,
                   y=py + 26, width=5, height=6, fill=INK, stroke=NONE))
    sc_add(d.path(f"M{px - 7},{py + 38} Q{px},{py + 42} {px + 7},{py + 38}",
                  f"Exhibit mouth {i+1}", fill=NONE, stroke=INK,
                  strokeWidth=2, cap="round"))
    sc_add(d.text("AB"[i], f"Exhibit tag {i+1}", x=px, y=py + 90,
                  size=13, font="Virelai Sans", color=SOFT,
                  justify="center"))
d.text("WHICH IS TRUE?", "Scales caption", x=430, y=330, size=13,
       font="Virelai Sans", color=SOFT, justify="center")

# --- synth node machine, right ---------------------------------------------------
d.shape("ellipse", "Machine shadow", x=560, y=762, width=240, height=24,
        fill="#050D0C", opacity=55, stroke=NONE)
d.shape("rectangle", "Synth node", x=566, y=560, width=230, height=205,
        radius=12, fill=MACHINE, stroke=INK, strokeWidth=5)
# fan with motion ticks
d.shape("ellipse", "Fan ring", x=586, y=586, width=76, height=76,
        fill="#18201F", stroke="#3E5A56", strokeWidth=4)
d.shape("ellipse", "Fan hub", x=613, y=613, width=22, height=22,
        fill=TEAL, stroke=INK, strokeWidth=2.5)
for i, (fx1, fy1, fx2, fy2) in enumerate([(624,596,624,606),(624,656,624,666),
                                         (596,624,606,624),(656,624,666,624)]):
    d.path(f"M{fx1},{fy1} L{fx2},{fy2}", f"Fan blade {i+1}", fill=NONE,
           stroke=TEAL, strokeWidth=5, cap="round", opacity=80)
# vent lines + label
for i in range(4):
    d.path(f"M688,{592 + i * 22} L772,{592 + i * 22}", f"Vent {i+1}",
           fill=NONE, stroke="#18201F", strokeWidth=8, cap="round")
d.shape("rectangle", "Node light", x=688, y=690, width=84, height=18,
        radius=9, fill="#18201F", stroke=NONE)
d.shape("rectangle", "Node light on", x=688, y=690, width=56, height=18,
        radius=9, fill=TEAL, opacity=85, stroke=NONE)
d.text("SYNTH NODE", "Node tag", x=681, y=738, size=13,
       font="Virelai Sans", color="#B8E0D6", justify="center")
# monitor rising off the machine: a face half-rendered into pixels
d.path("M676,560 L676,470", "Monitor neck", fill=NONE, stroke=INK,
       strokeWidth=12, cap="round")
d.shape("rectangle", "Monitor", x=576, y=250, width=220, height=220,
        radius=10, fill="#2A3438", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Monitor screen", x=590, y=264, width=192,
        height=192, radius=5, fill=SCREEN, stroke=NONE)
# face: left half smooth, right half pixelating away
d.shape("ellipse", "Render face", x=632, y=290, width=104, height=104,
        fill=FACE, stroke=NONE)
d.shape("ellipse", "Render eye", x=660, y=326, width=11, height=13,
        fill=INK, stroke=NONE)
d.path("M654,360 Q672,372 690,360", "Render mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# pixels drifting off the right edge of the face
for i, (px, py, pw, op) in enumerate([(724, 300, 12, 80), (740, 318, 9, 65),
                                     (730, 340, 11, 75), (748, 356, 8, 55),
                                     (722, 366, 10, 70), (744, 296, 7, 50),
                                     (752, 332, 9, 60)]):
    d.shape("rectangle", f"Pixel {i+1}", x=px, y=py, width=pw, height=pw,
            fill="#C09870", opacity=op, stroke=NONE)
# scan line mid-face
d.path("M632,342 L748,342", "Scan line", fill=NONE, stroke=TEAL,
       strokeWidth=3, opacity=80)
# render readout
d.shape("rectangle", "Render bar bg", x=606, y=430, width=150, height=10,
        radius=5, fill="#18201F", stroke=NONE)
d.shape("rectangle", "Render bar", x=606, y=430, width=110, height=10,
        radius=5, fill=TEAL, stroke=NONE)
d.text("RENDERING", "Render tag", x=681, y=420, size=11,
       font="Virelai Sans", color=TEAL, justify="center")

# --- the alibi reel, playing unattended on the left --------------------------------
alb_ids = []
def alb_add(res):
    if res and res.get("id"):
        alb_ids.append(res["id"])
alb_add(d.shape("rectangle", "Alibi player", x=150, y=316, width=140,
                height=104, radius=8, fill="#141F1E", stroke="#3E5A56",
                strokeWidth=4))
alb_add(d.shape("rectangle", "Alibi screen", x=160, y=328, width=120,
                height=62, radius=4, fill=SCREEN, stroke=NONE))
alb_add(d.path("M210,340 L244,358 L210,376 Z", "Play triangle",
                fill=TEAL, opacity=90, stroke=NONE))
alb_add(d.shape("rectangle", "Alibi bar bg", x=160, y=398, width=120,
                height=6, radius=3, fill="#2A3438", stroke=NONE))
alb_add(d.shape("rectangle", "Alibi bar", x=160, y=398, width=76,
                height=6, radius=3, fill=RED, stroke=NONE))
alb_add(d.text("ALIBI.MOV", "Alibi tag", x=220, y=414, size=10,
                font="Virelai Sans", color=SOFT, justify="center"))
if alb_ids:
    d.call("transform", {"ids": alb_ids, "rotate": -5,
                         "origin": [220, 368]}, "tilt alibi")

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=200, y=700, width=600, height=120,
        fill="#14201D", opacity=85, stroke=NONE)
d.shape("ellipse", "Dave shadow", x=250, y=780, width=210, height=26,
        fill="#050D0C", opacity=55, stroke=NONE)

# --- Dave: purple bean, clapperboard head, sample card ------------------------------
# body
d.shape("ellipse", "Dave body", x=272, y=560, width=190, height=220,
        fill=DAVE, stroke=INK, strokeWidth=5)
d.path("M300,640 C296,690 300,730 312,762", "Body sheen", fill=NONE,
       stroke="#B8A4E0", strokeWidth=8, opacity=25, cap="round")
# stubby feet
d.shape("ellipse", "Foot L", x=300, y=772, width=34, height=14,
        fill="#2E2444", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=398, y=772, width=34, height=14,
        fill="#2E2444", stroke=INK, strokeWidth=3)
# clapperboard head: slate bar with stripes, face below
clap_ids = []
def clap_add(res):
    if res and res.get("id"):
        clap_ids.append(res["id"])
clap_add(d.shape("rectangle", "Clap face", x=278, y=430, width=178,
                 height=108, radius=6, fill=CLAP, stroke=INK,
                 strokeWidth=5))
clap_add(d.shape("rectangle", "Clap slate", x=278, y=396, width=178,
                 height=38, radius=6, fill="#2E343E", stroke=INK,
                 strokeWidth=5))
for i in range(5):
    x0 = 288 + i * 36
    clap_add(d.path(f"M{x0},434 L{x0 + 18},396 L{x0 + 32},396 "
                    f"L{x0 + 14},434 Z", f"Slate stripe {i+1}",
                    fill="#D8DEE8", opacity=85, stroke=NONE))
# sleepy contented face on the slate head
clap_add(d.path("M310,478 q9,-8 18,0", "Dave eye L", fill=NONE,
                stroke="#C9C2E0", strokeWidth=4, cap="round"))
clap_add(d.path("M398,478 q9,-8 18,0", "Dave eye R", fill=NONE,
                stroke="#C9C2E0", strokeWidth=4, cap="round"))
clap_add(d.path("M340,504 Q366,520 392,504", "Dave smile", fill=NONE,
                stroke="#C9C2E0", strokeWidth=4, cap="round"))
if clap_ids:
    d.call("transform", {"ids": clap_ids, "rotate": 4,
                         "origin": [367, 484]}, "tilt clapperboard")
# left arm down at side, right arm offering the sample card
d.path("M286,620 C264,646 260,676 268,700", "Arm L", fill=NONE,
       stroke="#4E3E6E", strokeWidth=17, cap="round")
d.path("M452,600 C486,570 508,542 516,512", "Arm R", fill=NONE,
       stroke="#4E3E6E", strokeWidth=17, cap="round")
d.shape("ellipse", "Hand R", x=506, y=496, width=26, height=24,
        fill="#8A6EB8", stroke=INK, strokeWidth=3.5)
# the sample card: your face, politely acquired
card_ids = []
def card_add(res):
    if res and res.get("id"):
        card_ids.append(res["id"])
card_add(d.shape("rectangle", "Sample card", x=500, y=424, width=72,
                 height=80, radius=5, fill="#EDE6D4", stroke=INK,
                 strokeWidth=4))
card_add(d.shape("ellipse", "Sample face", x=516, y=438, width=40,
                 height=40, fill=FACE, stroke=INK, strokeWidth=2.5))
card_add(d.shape("ellipse", "Sample eye L", x=525, y=452, width=6,
                 height=7, fill=INK, stroke=NONE))
card_add(d.shape("ellipse", "Sample eye R", x=541, y=452, width=6,
                 height=7, fill=INK, stroke=NONE))
card_add(d.path("M528,468 Q536,474 544,468", "Sample mouth", fill=NONE,
                stroke=INK, strokeWidth=2.5, cap="round"))
card_add(d.text("SAMPLE", "Sample tag", x=536, y=496, size=9,
                font="Virelai Sans", color="#6E5F4A", justify="center"))
if card_ids:
    d.call("transform", {"ids": card_ids, "rotate": 6,
                         "origin": [536, 464]}, "tilt card")
# sampled data motes drifting from card to monitor
for i, (mx, my, mw, op) in enumerate([(560, 430, 8, 60), (580, 410, 7, 50),
                                      (598, 396, 7, 45), (612, 380, 6, 40)]):
    d.shape("rectangle", f"Mote {i+1}", x=mx, y=my, width=mw, height=mw,
            fill=TEAL, opacity=op, stroke=NONE)

# --- name + key line + role ------------------------------------------------------
r = d.text("THE COURT DOESN'T KNOW WHAT IS TRUE", "Key line", x=500,
           y=899, size=22, font="Virelai Sans", color=SOFT,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=120)
d.text("DEEPFAKE DAVE", "Name", x=500, y=945, size=56,
       font="Virelai Sans", color=ICE, justify="center")
r = d.text("THE COURT DOESN'T KNOW WHAT IS TRUE", "Role", x=500, y=977,
           size=19, font="Virelai Sans", color="#6A8E86",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0445-deepfake-dave-V1R00")
