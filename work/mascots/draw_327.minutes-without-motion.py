#!/usr/bin/env python3
"""Minutes Without Motion — mascot portrait V1R00.
The mascot seated at the Service Continuity Listening Board table, pen
over the minute pad, a status display reading GREEN glowing on the wall
behind. Two more chairs, both empty. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Minutes Without Motion — Mascot Portrait", 1000, 1000)

INK = "#26222C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161A22"}, {"offset": 1, "color": "#0E1218"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E7A84"}, {"offset": 0.7, "color": "#4C5860"},
    {"offset": 1, "color": "#242E34"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C4650"}, {"offset": 1, "color": "#181E24"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B4BCC8"}, {"offset": 0.72, "color": "#8A94A4"},
    {"offset": 1, "color": "#5A6270"}]}}
TABLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A5240"}, {"offset": 1, "color": "#342A22"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E5C46"}, {"offset": 1, "color": "#101C16"}]}}
PAPER = "#EDE6D2"
GREEN = "#8FE0A8"
CHAIR = "#3E4650"

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8696A0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4DEE4", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(192,236,8),(804,234,7),(160,522,9),(836,546,8),
                               (254,766,7),(748,752,9),(136,394,6),(862,396,7),
                               (396,114,7),(610,114,8),(336,820,6),(666,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#505C64", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#10161C",
       strokeWidth=4, opacity=70)

# --- the status display: Green, as ever --------------------------------------------------
d.shape("ellipse", "Screen glow", x=270, y=120, width=460, height=210,
        fill="#4E8A66", opacity=14, stroke=NONE)
d.shape("rectangle", "Display bezel", x=330, y=158, width=340, height=118,
        fill="#1A1E24", stroke=INK, strokeWidth=6, radius=14)
d.shape("rectangle", "Display screen", x=346, y=172, width=308, height=90,
        fill=SCREEN_GRAD, stroke="#0C120E", strokeWidth=3, radius=8)
d.text("GREEN", "Status word", x=500, y=238, size=52, font="Virelai Sans",
       color=GREEN, justify="center")
d.shape("ellipse", "Screen sheen", x=370, y=178, width=180, height=18,
        fill="#FFFFFF", opacity=10, stroke=NONE)
d.shape("ellipse", "LED", x=344, y=280, width=10, height=10, fill=GREEN,
        stroke=NONE, opacity=90)
# faint scanlines across the screen
for i, sy in enumerate([186, 206, 226, 246]):
    d.path(f"M352,{sy} L648,{sy}", f"Scanline {i+1}", fill=NONE,
           stroke="#0E1A12", strokeWidth=2, opacity=35)

# --- the two other chairs, kept warm for testimony --------------------------------------
for lbl, cx in [("Chair L", 246), ("Chair R", 754)]:
    d.shape("ellipse", lbl + " shadow", x=cx - 60, y=676, width=120, height=16,
            fill="#0C1014", opacity=40, stroke=NONE)
    d.path(f"M{cx-44},560 C{cx-44},520 {cx-30},498 {cx},498 C{cx+30},498 "
           f"{cx+44},520 {cx+44},560 L{cx+44},640 L{cx-44},640 Z",
           lbl + " back", fill=CHAIR, stroke=INK, strokeWidth=5, join="round")
    d.path(f"M{cx-30},520 C{cx-16},510 {cx+16},510 {cx+30},520",
           lbl + " back hi", fill=NONE, stroke="#5E6A76", strokeWidth=4,
           opacity=60, cap="round")

# --- the minute-taker, seated -------------------------------------------------------------
d.shape("ellipse", "Chair own shadow", x=400, y=676, width=200, height=18,
        fill="#0C1014", opacity=45, stroke=NONE)
# own chair back just visible behind the shoulders
d.path("M420,566 C420,516 448,494 500,494 C552,494 580,516 580,566 L580,620 "
       "L420,620 Z", "Own chair", fill=CHAIR, stroke=INK, strokeWidth=5,
       join="round")
# body: calm bell, shoulders level, hands to the pad
d.path("M500,380 C578,380 622,448 628,560 L630,640 L370,640 L372,560 "
       "C378,448 422,380 500,380 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=420, y=410, width=96, height=42,
        fill="#FFFFFF", opacity=13, stroke=NONE)
# cardigan seam + buttons
d.path("M500,470 L500,624", "Seam", fill=NONE, stroke="#62687A",
       strokeWidth=4, opacity=70)
for i, by in enumerate([500, 542, 584]):
    d.shape("ellipse", f"Button {i+1}", x=494, y=by, width=11, height=11,
            fill="#C9B06A", stroke=INK, strokeWidth=2)

# face: level eyes, the patience of someone archiving the room
d.shape("ellipse", "Eye L", x=444, y=470, width=26, height=26,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye L glint", x=450, y=474, width=8, height=8,
        fill="#FFFFFF", stroke=NONE)
d.shape("ellipse", "Eye R", x=530, y=470, width=26, height=26,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R glint", x=536, y=474, width=8, height=8,
        fill="#FFFFFF", stroke=NONE)
# level mouth — testimony received, classification unmoved
d.path("M470,532 C482,537 518,537 530,532", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.shape("ellipse", "Cheek L", x=430, y=512, width=26, height=13,
        fill="#8A8E9E", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=544, y=512, width=26, height=13,
        fill="#8A8E9E", opacity=45, stroke=NONE)
# the small headset of a listener: band + one earpiece
d.path("M428,436 C444,410 472,398 500,398 C528,398 556,410 572,436",
       "Headset band", fill=NONE, stroke="#3A4048", strokeWidth=8, cap="round")
d.shape("ellipse", "Earpiece", x=564, y=432, width=24, height=30,
        fill="#3A4048", stroke=INK, strokeWidth=4)
d.path("M574,462 C572,492 560,510 552,522", "Mic boom", fill=NONE,
       stroke="#3A4048", strokeWidth=5, cap="round")
d.shape("ellipse", "Mic", x=542, y=516, width=18, height=13,
        fill="#3A4048", stroke=INK, strokeWidth=3)

# --- the board table ----------------------------------------------------------------------
d.shape("ellipse", "Table shadow", x=180, y=686, width=640, height=22,
        fill="#0C1014", opacity=40, stroke=NONE)
d.path("M196,600 L804,600 L790,700 L210,700 Z", "Table", fill=TABLE_GRAD,
       stroke=INK, strokeWidth=6, join="round")
d.path("M196,600 L804,600", "Table edge", fill=NONE, stroke="#8A6E52",
       strokeWidth=5, opacity=80)
d.path("M240,640 L760,640 M234,672 L766,672", "Table grain", fill=NONE,
       stroke="#241C16", strokeWidth=3, opacity=40)
# modesty panel line
d.path("M260,616 L740,616", "Panel line", fill=NONE, stroke="#1E1712",
       strokeWidth=3, opacity=50)

# the minute pad under the pen: every word filed, nothing changed
d.path("M400,586 L560,578 L566,634 L406,642 Z", "Minute pad", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
for i, ly in enumerate([594, 606, 618, 630]):
    d.path(f"M416,{ly} L{546 - i*6},{ly - 6}", f"Minute line {i+1}",
           fill=NONE, stroke="#9A9276", strokeWidth=3, opacity=85)
# arms: right holds the pen mid-stroke, left steadies the pad
d.path("M586,560 C606,576 616,592 616,608", "Arm R", fill=NONE,
       stroke="#8A94A4", strokeWidth=20, cap="round")
d.path("M634,542 L604,608 L614,614 L644,548 Z", "Pen", fill="#2A3038",
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Pen nib", x=628, y=532, width=12, height=12,
        fill="#C9B06A", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand R", x=596, y=596, width=34, height=22,
        fill="#B4BCC8", stroke=INK, strokeWidth=4)
d.path("M414,566 C398,584 392,600 394,614", "Arm L", fill=NONE,
       stroke="#8A94A4", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand L", x=384, y=602, width=34, height=22,
        fill="#B4BCC8", stroke=INK, strokeWidth=4)

# the water glass nobody touches
d.path("M664,588 L700,588 L694,638 L670,638 Z", "Glass", fill="#9AB8C4",
       stroke=INK, strokeWidth=4, opacity=55, join="round")
d.path("M667,606 L697,606", "Water line", fill=NONE, stroke="#C8DEE6",
       strokeWidth=3, opacity=60)
# a stack of prior minutes, already closed
d.path("M238,612 L336,606 L340,634 L242,640 Z", "Minutes stack", fill="#D8CEB4",
       stroke=INK, strokeWidth=4, join="round")
d.path("M244,618 L332,613 M246,626 L334,621", "Stack lines", fill=NONE,
       stroke="#9A9276", strokeWidth=2.5, opacity=80)
d.path("M250,634 L330,630", "Stack edge", fill=NONE, stroke="#B4AA8E",
       strokeWidth=4, opacity=80)

# --- captions ---------------------------------------------------------------------------
d.text("MINUTES WITHOUT MOTION", "Name", x=500, y=930, size=44,
       font="Virelai Sans", color="#DDE6EA", justify="center")
r = d.text("SILENCE, FULLY DESCRIBED", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8B6C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("327.minutes-without-motion-V1R00")
