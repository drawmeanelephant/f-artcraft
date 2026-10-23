#!/usr/bin/env python3
"""Mod Maria — mascot portrait V1R00.
Headset moderator at a terminal mid-review-queue, wellness.pdf link
waiting on screen. 1000x1000. House style: gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mod Maria — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161022"}, {"offset": 1, "color": "#0A0712"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E5480"}, {"offset": 0.7, "color": "#403A5C"},
    {"offset": 1, "color": "#221E36"}]}}
DESK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C3654"}, {"offset": 1, "color": "#1E1A30"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2C9C0"}, {"offset": 0.7, "color": "#D89E98"},
    {"offset": 1, "color": "#B07472"}]}}
HAIR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3444"}, {"offset": 1, "color": "#2E1E2C"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#20323C"}, {"offset": 1, "color": "#101E24"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F5CE7E"}, {"offset": 1, "color": "#B57E3D"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E74A8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D2EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A4266", opacity=45, stroke=NONE)

# --- desk ----------------------------------------------------------------------
d.shape("ellipse", "Desk", x=170, y=615, width=660, height=130,
        fill=DESK, stroke=NONE, opacity=92)
d.shape("ellipse", "Maria shadow", x=330, y=660, width=190, height=34,
        fill="#0A0714", opacity=55, stroke=NONE)

# --- monitor + review queue -----------------------------------------------------
# stand
d.path("M712,540 L712,596 M672,596 L752,596", "Stand", fill=NONE,
       stroke=INK, strokeWidth=10, cap="round", join="round")
# bezel + screen
d.shape("rectangle", "Monitor", x=600, y=360, width=224, height=180,
        fill="#1C1626", stroke=INK, strokeWidth=6, radius=10)
d.shape("rectangle", "Screen", x=614, y=374, width=196, height=152,
        fill=SCREEN, stroke=NONE, radius=5)
# warm spill from screen onto desk
d.path("M614,526 L810,526 L780,590 L640,590 Z", "Screen spill",
       fill="#F0C878", opacity=10, stroke=NONE)
# queue header
d.shape("rectangle", "Queue header", x=614, y=374, width=196, height=24,
        fill="#2E4250", stroke=NONE, radius=5)
d.text("REVIEW QUEUE", "Queue title", x=712, y=390, size=11,
       font="Virelai Sans", color="#BFE0E8", justify="center")
# queue rows: flag + item bar; row 2 flagged amber, row 3 open
rows = [(412, "#8FA8B2", "#3A5260"), (438, "#F0C878", "#5A4630"),
        (464, "#8FA8B2", "#3A5260"), (490, "#8FA8B2", "#3A5260")]
for i, (y, flag, bar) in enumerate(rows):
    d.path(f"M626,{y} L626,{y+12} L638,{y+6} Z", f"Flag {i+1}",
           fill=flag, stroke=NONE)
    d.shape("rectangle", f"Item {i+1}", x=646, y=y+1, width=152, height=11,
            fill=bar, stroke=NONE, radius=3)
# the wellness link in the footer
d.text("↳ wellness.pdf", "Wellness link", x=712, y=518, size=10,
       font="Virelai Sans", color="#8FD8C8", justify="center")
d.path("M678,522 L746,522", "Link underline", fill=NONE,
       stroke="#8FD8C8", strokeWidth=1.5, opacity=70)

# --- Maria ----------------------------------------------------------------------
# legs under desk edge
d.shape("ellipse", "Shoe L", x=380, y=676, width=34, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=442, y=676, width=34, height=15, fill=INK, stroke=NONE)
d.path("M394,650 L392,678", "Leg L", fill=NONE, stroke="#B07472",
       strokeWidth=13, cap="round")
d.path("M452,650 L456,678", "Leg R", fill=NONE, stroke="#A86A68",
       strokeWidth=13, cap="round")
# body
d.path("M430,470 C488,470 514,518 511,572 C508,624 478,654 430,654 "
       "C382,654 352,624 349,572 C346,518 372,470 430,470 Z",
       "Maria body", fill=BODY, stroke=INK, strokeWidth=6)
d.path("M396,632 C424,644 466,644 492,630 C466,638 422,638 396,632 Z",
       "Body shadow", fill="#A86A68", opacity=45, stroke=NONE)
# hair cap + bun
d.path("M376,480 C370,430 396,398 430,398 C464,398 490,430 484,480 "
       "C472,462 456,452 430,452 C404,452 388,462 376,480 Z",
       "Hair", fill=HAIR, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Bun", x=368, y=418, width=30, height=28,
        fill=HAIR, stroke=INK, strokeWidth=4)
# headset: band + earpad + mic boom
d.path("M388,442 C394,414 412,402 430,402 C448,402 466,414 472,442",
       "Headset band", fill=NONE, stroke="#5E5480", strokeWidth=8, cap="round")
d.shape("ellipse", "Earpad L", x=382, y=452, width=20, height=26,
        fill="#3E3654", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Earpad R", x=458, y=452, width=20, height=26,
        fill="#3E3654", stroke=INK, strokeWidth=4)
d.path("M470,470 C486,484 494,498 492,512", "Mic boom", fill=NONE,
       stroke="#3E3654", strokeWidth=5, cap="round")
d.shape("ellipse", "Mic", x=484, y=508, width=14, height=12,
        fill="#3E3654", stroke=INK, strokeWidth=3)
# face: eyes on the screen, tired-warm
d.shape("ellipse", "Eye L", x=414, y=498, width=15, height=19, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=452, y=498, width=15, height=19, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=418, y=502, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=456, y=502, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Cheek L", x=398, y=524, width=22, height=13,
        fill="#E88C84", opacity=55, stroke=NONE)
d.shape("ellipse", "Cheek R", x=462, y=524, width=22, height=13,
        fill="#E88C84", opacity=55, stroke=NONE)
d.path("M426,546 C434,550 444,550 452,544", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# warm screen light on her face
d.shape("ellipse", "Face glow", x=452, y=486, width=62, height=54,
        fill="#F5CE7E", opacity=10, stroke=NONE)
# arm to keyboard
d.path("M504,560 C540,570 568,578 596,584", "Arm keys", fill=NONE,
       stroke="#D89E98", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand keys", x=590, y=578, width=18, height=14,
        fill="#F2C9C0", stroke=INK, strokeWidth=3)
# keyboard
d.path("M560,600 L700,600 L716,634 L544,634 Z", "Keyboard",
       fill="#2A2438", stroke=INK, strokeWidth=4, join="round")
for i, x in enumerate(range(566, 700, 22)):
    d.path(f"M{x},612 L{x+14},612", f"Key {i+1}", fill=NONE,
           stroke="#4A4262", strokeWidth=3, opacity=80)

# --- mug -------------------------------------------------------------------------
d.shape("rectangle", "Mug", x=300, y=600, width=42, height=46,
        fill="#7E74A8", stroke=INK, strokeWidth=4, radius=6)
d.path("M342,610 C356,610 356,632 342,632", "Mug handle", fill=NONE,
       stroke=INK, strokeWidth=5)
d.path("M314,590 C314,580 320,578 320,568 M330,592 C330,582 336,580 336,570",
       "Steam", fill=NONE, stroke="#D8D2EC", strokeWidth=3, opacity=50, cap="round")

# --- captions ----------------------------------------------------------------------
d.text("MOD MARIA", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#E4DEF2", justify="center")
r = d.text("REVIEW QUEUE MODERATOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89CCC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("438.mod-maria-V1R00")
