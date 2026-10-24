#!/usr/bin/env python3
"""Revival Pocket — mascot portrait V1R00.
The anomaly, cordoned while still warm: a mascot keeps witness beside an
obsolete terminal that boots only inside the taped square — third socket
of the grey power strip, the record says. Outside the tape its twin sits
dead, and the pocket's whole testimony is two lines tall.
1000x1000. Gradients + translucent shading, no flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Revival Pocket — Mascot Portrait", 1000, 1000)

INK = "#3A2C20"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131B22"}, {"offset": 1, "color": "#06090D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#42505B"}, {"offset": 0.7, "color": "#28333C"},
    {"offset": 1, "color": "#161E25"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2D3740"}, {"offset": 1, "color": "#1A2129"}]}}
GLOW_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8B25C", "opacity": 0.22},
    {"offset": 0.65, "color": "#E8B25C", "opacity": 0.08},
    {"offset": 1, "color": "#E8B25C", "opacity": 0}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D9D2BC"}, {"offset": 0.6, "color": "#A29B85"},
    {"offset": 1, "color": "#7E7867"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E8A62"}, {"offset": 0.55, "color": "#1E3A28"},
    {"offset": 1, "color": "#0E1811"}]}}
DEAD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C343E"}, {"offset": 1, "color": "#181F27"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D3B494"}, {"offset": 0.7, "color": "#AC8966"},
    {"offset": 1, "color": "#7C5E42"}]}}
STRIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9AA0A8"}, {"offset": 1, "color": "#62666F"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    assert math.hypot(x - PCX, y - PCY) <= PR - pad, (x, y)

def rrect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#42505B", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5B7080", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8C4CE", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(200,250,7),(800,240,8),(160,470,8),(840,480,7),
                               (265,765,6),(735,770,7),(135,360,6),(865,350,6),
                               (400,105,7),(605,100,8),(320,150,5),(690,145,6)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#55656F", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M131,660 L869,660 A420,420 0 0 1 131,660 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M131,660 L869,660", "Floor line", fill=NONE, stroke="#10151B",
       strokeWidth=4, opacity=70)

# --- the warm pocket, inside the tape ------------------------------------------
d.shape("ellipse", "Pocket glow", x=190, y=490, width=640, height=340,
        fill=GLOW_GRAD, stroke=NONE)

# --- dead twin, outside the perimeter -------------------------------------------
d.path(rrect(155, 545, 115, 123, 10), "Dead terminal",
       fill=DEAD_GRAD, stroke="#0E1318", strokeWidth=4)
d.path(rrect(167, 558, 91, 66, 6), "Dead screen", fill="#0A0E12",
       stroke="#232C36", strokeWidth=3)
d.path("M180,570 L225,610 M228,566 L196,618", "Screen crack", fill=NONE,
       stroke="#3A4652", strokeWidth=2.5, opacity=60, cap="round")
d.path(rrect(170, 668, 85, 14, 4), "Dead base", fill=DEAD_GRAD,
       stroke="#0E1318", strokeWidth=4)
# cold rim where the pocket's warmth almost reaches it
d.path("M268,556 C272,590 270,636 262,664", "Dead rim light", fill=NONE,
       stroke="#5A6B78", strokeWidth=3.5, opacity=45, cap="round")
# its plug lies loose on the floor, unplugged
d.path("M250,688 C272,700 288,712 296,726", "Dead cord", fill=NONE,
       stroke="#1C232B", strokeWidth=5, cap="round")
d.path(rrect(290, 720, 20, 13, 3), "Dead plug", fill="#1C232B",
       stroke="#0E1318", strokeWidth=2.5)

# --- caution tape: the surveyed perimeter ----------------------------------------
TAPE = "#E0B83C"
def tape_edge(x0, y0, x1, y1, label):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"{label}", fill=NONE,
           stroke=TAPE, strokeWidth=9, opacity=95)
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    a = math.radians(50)
    sx, sy = ux * math.cos(a) - uy * math.sin(a), ux * math.sin(a) + uy * math.cos(a)
    n = max(1, int(L / 30))
    for i in range(1, n + 1):
        cx, cy = x0 + dx * i / (n + 1), y0 + dy * i / (n + 1)
        d.path(f"M{cx - sx*6:.1f},{cy - sy*6:.1f} L{cx + sx*6:.1f},{cy + sy*6:.1f}",
               f"{label} hazard {i}", fill=NONE, stroke="#2A2118",
               strokeWidth=3.5, opacity=80, cap="round")

tape_edge(275, 688, 725, 688, "Tape back")
tape_edge(250, 780, 750, 780, "Tape front")
tape_edge(275, 688, 250, 780, "Tape left")
tape_edge(725, 688, 750, 780, "Tape right")

# --- screen light spill on the floor --------------------------------------------
d.shape("ellipse", "Screen spill", x=295, y=645, width=240, height=70,
        fill="#9FE8B8", opacity=13, stroke=NONE)

# --- the live terminal ------------------------------------------------------------
d.shape("ellipse", "Terminal shadow", x=300, y=690, width=230, height=18,
        fill="#0C1014", opacity=50, stroke=NONE)
d.path(rrect(320, 484, 192, 170, 12), "Terminal body",
       fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# vents on the crown — it runs hot while it runs at all
for i in range(4):
    d.path(f"M{400 + i*22},494 L{412 + i*22},494", f"Vent {i+1}",
           fill=NONE, stroke="#6E6858", strokeWidth=4, cap="round", opacity=80)
# bezel + live screen
d.path(rrect(338, 502, 152, 108, 8), "Bezel", fill="#8E8878",
       stroke=INK, strokeWidth=4)
d.path(rrect(346, 510, 136, 92, 6), "Screen", fill=SCREEN_GRAD, stroke="#0C130E",
       strokeWidth=3)
# phosphor: three settled lines and a cursor that believes
for i, (x1, x2, ty) in enumerate([(356, 424, 524), (356, 448, 536), (356, 408, 548)]):
    d.path(f"M{x1},{ty} L{x2},{ty}", f"Screen line {i+1}", fill=NONE,
           stroke="#9FE8B8", strokeWidth=3.5, cap="round", opacity=60)
d.path(rrect(356, 562, 10, 9, 1), "Cursor", fill="#9FE8B8",
       stroke=NONE, opacity=80)
d.shape("ellipse", "Glass glare", x=352, y=512, width=70, height=30,
        fill="#FFFFFF", opacity=10, stroke=NONE)
# foot + base slab
d.path("M368,654 L462,654 L478,684 L352,684 Z", "Terminal foot",
       fill=BODY_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path(rrect(348, 684, 136, 16, 5), "Terminal base", fill="#8E8878",
       stroke=INK, strokeWidth=4)

# --- cable run: terminal down to the strip ----------------------------------------
d.path("M470,700 C500,708 528,716 552,724", "Terminal cord", fill=NONE,
       stroke="#4A3E30", strokeWidth=5, cap="round")

# --- grey power strip, third socket occupied --------------------------------------
d.shape("ellipse", "Strip shadow", x=462, y=738, width=190, height=12,
        fill="#0C1014", opacity=45, stroke=NONE)
d.path(rrect(468, 722, 178, 20, 7), "Power strip", fill=STRIP_GRAD,
       stroke=INK, strokeWidth=3.5)
for i, sx in enumerate([492, 528, 564, 600]):
    d.path(rrect(sx, 727, 20, 11, 3), f"Socket {i+1}", fill="#3A3D44",
           stroke="#26282E", strokeWidth=2)
    d.shape("ellipse", f"Socket {i+1} hole L", x=sx + 4, y=730, width=3.5,
            height=5, fill="#16171B", stroke=NONE)
    d.shape("ellipse", f"Socket {i+1} hole R", x=sx + 12, y=730, width=3.5,
            height=5, fill="#16171B", stroke=NONE)
# the plug, seated in socket three like doctrine requires
d.path(rrect(561, 711, 26, 18, 4), "The third plug", fill="#2E2A24",
       stroke=INK, strokeWidth=3)
d.path("M552,724 C556,718 560,714 564,712", "Plug lead", fill=NONE,
       stroke="#4A3E30", strokeWidth=4.5, cap="round")
# strip lamp, amber and certain
d.shape("ellipse", "Strip lamp glow", x=622, y=724, width=18, height=14,
        fill="#E8B25C", opacity=30, stroke=NONE)
d.path(rrect(626, 727, 10, 8, 2), "Strip lamp", fill="#E8B25C",
       stroke=INK, strokeWidth=2)
# strip's own cord exits the pocket — the lifeline runs to the dead zone
d.path("M646,734 C690,742 728,752 762,748", "Strip cord a", fill=NONE,
       stroke="#4A3E30", strokeWidth=5, cap="round", opacity=80)
d.path("M762,748 C778,746 788,742 796,736", "Strip cord b", fill=NONE,
       stroke="#4A3E30", strokeWidth=5, cap="round", opacity=45)
for x, y in [(646, 734), (796, 736)]:
    on_disc(x, y, 8)

# --- the mascot, keeping witness ---------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=575, y=700, width=160, height=16,
        fill="#0C1014", opacity=50, stroke=NONE)
d.shape("ellipse", "Ear L", x=592, y=532, width=26, height=24,
        fill="#AC8966", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Ear R", x=678, y=532, width=26, height=24,
        fill="#AC8966", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Body", x=582, y=548, width=132, height=152,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# feet
d.shape("ellipse", "Foot L", x=598, y=688, width=36, height=22,
        fill="#8A6B4C", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Foot R", x=660, y=688, width=36, height=22,
        fill="#8A6B4C", stroke=INK, strokeWidth=3.5)
# belly patch, soft
d.shape("ellipse", "Belly", x=612, y=626, width=74, height=62,
        fill="#E4CBA8", opacity=55, stroke=NONE)
# eyes, wide, turned toward the machine that breathes
d.shape("ellipse", "Eye L", x=606, y=592, width=24, height=30,
        fill="#33241C", stroke=NONE)
d.shape("ellipse", "Eye R", x=652, y=592, width=24, height=30,
        fill="#33241C", stroke=NONE)
d.shape("ellipse", "Glint L", x=611, y=598, width=6, height=7,
        fill="#FFF8E8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=657, y=598, width=6, height=7,
        fill="#FFF8E8", opacity=90, stroke=NONE)
# the small careful smile of the locally saved
d.path("M632,648 C642,656 654,656 664,648", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# phosphor rim light down the side that faces the screen
d.path("M590,578 C583,612 586,654 600,686", "Rim light", fill=NONE,
       stroke="#9FE8B8", strokeWidth=4, opacity=30, cap="round")

# --- the intake form, dropped on the floor of the pocket ---------------------------
d.path("M332,708 L428,712 L422,742 L326,738 Z", "Intake form",
       fill="#E8DFC8", stroke="#9A8F72", strokeWidth=2.5, opacity=90)
for i, (x0, x1, ty) in enumerate([(342, 402, 718), (342, 388, 728)]):
    d.path(f"M{x0},{ty} L{x1},{ty+1}", f"Form line {i+1}", fill=NONE,
           stroke="#8A8064", strokeWidth=3, cap="round", opacity=70)
d.path("M398,730 L414,731", "Form tick", fill=NONE, stroke="#8A8064",
       strokeWidth=3, cap="round", opacity=45)

# --- motes, warm inside, cold without ----------------------------------------------
for i, (x, y, w) in enumerate([(330,560,4),(700,560,5),(560,470,4),(430,530,4)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Warm mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0D8A8", opacity=45, stroke=NONE)
for i, (x, y, w) in enumerate([(200,300,5),(820,320,5),(160,560,5),(840,600,4),(450,190,4),(620,200,5)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Cold mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#9FB8C4", opacity=35, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("REVIVAL POCKET", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F2E3C2", justify="center")
r = d.text("IT WORKS WHERE I'M STANDING", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C0AE8E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("287.revival-pocket-V1R00")
