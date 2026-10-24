#!/usr/bin/env python3
"""Quiet Surplus — mascot portrait V1R00.
A small surplus-certified mascot beside a silent server rack, holding the
ethernet cable that isn't connected to anything. Telemetry reads the quiet
as headroom; the quiet disagrees. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Quiet Surplus — Mascot Portrait", 1000, 1000)

INK = "#1E2422"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12201E"}, {"offset": 1, "color": "#060C0B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#44605A"}, {"offset": 0.7, "color": "#283E38"},
    {"offset": 1, "color": "#101E1A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#22352F"}, {"offset": 1, "color": "#0C1614"}]}}
RACK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#39454E"}, {"offset": 1, "color": "#1A2228"}]}}
BAY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A343C"}, {"offset": 1, "color": "#141C22"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9FBCC0"}, {"offset": 0.7, "color": "#6E9298"},
    {"offset": 1, "color": "#44666C"}]}}
FACE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2A2E"}, {"offset": 1, "color": "#0E1618"}]}}
CABLE = "#3A464E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E857A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4DCD2", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#344E46", opacity=45, stroke=NONE)

# --- floor -------------------------------------------------------------------
d.path("M187,740 L813,740 A420,420 0 0 1 187,740 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M187,740 L813,740", "Floor line", fill=NONE, stroke="#0A1310",
       strokeWidth=4, opacity=70)

# --- the silent rack --------------------------------------------------------------
RX = 560   # rack left edge
d.shape("ellipse", "Rack shadow", x=RX-16, y=724, width=250, height=24,
        fill="#060C0A", opacity=45, stroke=NONE)
d.shape("rectangle", "Rack", x=RX, y=255, width=220, height=470,
        fill=RACK, stroke=INK, strokeWidth=6, radius=8)
# top status strip: nothing to report
d.shape("rectangle", "Status strip", x=RX+16, y=272, width=188, height=30,
        fill="#0C1418", stroke=INK, strokeWidth=3, radius=4)
d.text("ALL QUIET · CAPACITY PLENTY", "Status text", x=RX+24, y=291, size=11,
       font="Virelai Sans", color="#5E7A72", justify="left")
# bays: identical dark slots, LEDs that have nothing to say
for i in range(6):
    by = 320 + i * 62
    d.shape("rectangle", f"Bay {i+1}", x=RX+14, y=by, width=192, height=44,
            fill=BAY, stroke=INK, strokeWidth=3, radius=4)
    # slot lines
    d.path(f"M{RX+30},{by+16} L{RX+140},{by+16} M{RX+30},{by+28} L{RX+140},{by+28}",
           f"Bay {i+1} vents", fill=NONE, stroke="#0E161A", strokeWidth=3,
           opacity=80)
    # LED — every one dark except the single resigned amber on bay three
    led = "#3A4A48" if i != 2 else "#8A6A30"
    op = 70 if i != 2 else 90
    d.shape("ellipse", f"LED {i+1}", x=RX+168, y=by+18, width=8, height=8,
            fill=led, stroke=NONE, opacity=op)
# the empty port the cable used to answer to
d.shape("rectangle", "Empty port", x=RX+30, y=664, width=36, height=26,
        fill="#080F12", stroke="#3E4E56", strokeWidth=3, radius=3)
for i in range(4):
    d.path(f"M{RX+36+i*7},670 L{RX+36+i*7},684", f"Port pin {i+1}",
           fill=NONE, stroke="#3E4E56", strokeWidth=2, opacity=60)
# sticky note certifying the misreading
d.path(rot_rect_path(RX+150, 640, 74, 54, 6), "Sticky note",
       fill="#D8C884", stroke=INK, strokeWidth=3)
nt = d.text("slack", "Sticky text", x=RX+126, y=646, size=16,
            font="Bradley Hand", color="#5A5030", justify="left")
if nt and nt.get("id"):
    d.cmd("object.rotate", "sticky rot", ids=[nt["id"]], angle=6,
          origin=[RX+150, 640])

# a second rack in the gloom, further down the aisle, just as silent
d.shape("rectangle", "Far rack", x=196, y=430, width=120, height=290,
        fill="#14201C", stroke="#26382F", strokeWidth=4, radius=6, opacity=70)
for i in range(4):
    d.path(f"M212,{478+i*58} L300,{478+i*58} M212,{492+i*58} L300,{492+i*58}",
           f"Far bay {i+1}", fill=NONE, stroke="#0C1512", strokeWidth=3,
           opacity=60)

# --- the mascot: small, certified, unbothered ---------------------------------------
MX = 400   # body centreline
d.shape("ellipse", "Mascot shadow", x=MX-78, y=722, width=160, height=22,
        fill="#060C0A", opacity=45, stroke=NONE)
# feet
d.shape("ellipse", "Foot L", x=MX-52, y=704, width=44, height=20,
        fill="#3A565C", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=MX+8, y=704, width=44, height=20,
        fill="#3A565C", stroke=INK, strokeWidth=4)
# body: a soft little tower of surplus
d.path(f"M{MX-72},710 C{MX-80},600 {MX-78},510 {MX-58},478 "
       f"C{MX-40},452 {MX+40},452 {MX+58},478 "
       f"C{MX+78},510 {MX+80},600 {MX+72},710 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=6)
# face plate: dark glass, two calm eyes
d.shape("ellipse", "Face", x=MX-50, y=492, width=100, height=78,
        fill=FACE, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Eye L", x=MX-30, y=516, width=15, height=19,
        fill="#CFE8DC", stroke=NONE)
d.shape("ellipse", "Eye R", x=MX+15, y=516, width=15, height=19,
        fill="#CFE8DC", stroke=NONE)
d.shape("ellipse", "Pupil L", x=MX-25, y=524, width=6, height=7,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=MX+20, y=524, width=6, height=7,
        fill=INK, stroke=NONE)
# the small contented mouth of a thing that has never complained
d.path(f"M{MX-12},552 C{MX-4},558 {MX+4},558 {MX+12},552",
       "Mouth", fill=NONE, stroke="#CFE8DC", strokeWidth=3, cap="round",
       opacity=85)
# body sheen
d.shape("ellipse", "Body sheen", x=MX-56, y=480, width=40, height=20,
        fill="#D8F0E8", opacity=25, stroke=NONE)
# chest badge: what telemetry filed him as
d.shape("rectangle", "Badge", x=MX-44, y=592, width=88, height=34,
        fill="#E4DCC2", stroke=INK, strokeWidth=3, radius=6)
d.text("SPARE", "Badge text", x=MX-30, y=615, size=16,
       font="Virelai Sans", color="#5A5038", justify="left")
# a tiny idle antenna on top
d.path(f"M{MX+20},452 L{MX+30},428", "Antenna", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Antenna tip", x=MX+24, y=418, width=12, height=12,
        fill="#8A6A30", stroke=INK, strokeWidth=3)

# --- the disconnected cable ---------------------------------------------------------
# it leaves the plug, droops, and coils on the floor — going nowhere
d.path(f"M{MX+62},602 C{MX+96},652 {MX+122},698 {MX+150},714 "
       f"C{MX+190},730 {MX+230},726 {MX+260},714",
       "Cable droop", fill=NONE, stroke=CABLE, strokeWidth=9, cap="round")
# coil on the floor
d.path(f"M{MX+150},718 C{MX+186},700 {MX+236},700 {MX+268},716 "
       f"C{MX+292},728 {MX+270},738 {MX+230},736 C{MX+196},734 {MX+180},726 {MX+196},718",
       "Cable coil", fill=NONE, stroke=CABLE, strokeWidth=8, cap="round",
       opacity=90)
# the arm holding the plug up for inspection
d.path(f"M{MX+62},640 C{MX+76},632 {MX+80},622 {MX+74},608",
       "Arm", fill=NONE, stroke="#54727A", strokeWidth=18, cap="round")
d.shape("ellipse", "Hand", x=MX+56, y=596, width=26, height=24,
        fill=BODY, stroke=INK, strokeWidth=4)
# the RJ45 plug in hand, contacts out, clip down — unmistakably unplugged
pl = d.path(rot_rect_path(MX+74, 594, 34, 24, -30), "Plug body",
            fill="#5A6870", stroke=INK, strokeWidth=4)
d.path(rot_rect_path(MX+88, 584, 14, 18, -30), "Plug nose",
       fill="#74828A", stroke=INK, strokeWidth=3)
for i in range(3):
    d.path(rot_rect_path(MX+92+i*4.4, 586-i*2.3, 3, 12, -30), f"Contact {i+1}",
           fill="#C8A84A", stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("QUIET SURPLUS", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCE8DA", justify="center")
r = d.text("UNREPORTED LOAD", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9CBCB0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("320.quiet-surplus-V1R00")
