#!/usr/bin/env python3
"""Parvovirus-P — mascot portrait V1R00.
Overconfident safety surface: a grinning virus ball with commemorative
bandages wrapped on both arms, waving beside the chart, holding a
clipboard full of optimism. Drooping wellness-parade bunting overhead.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Parvovirus-P — Mascot Portrait", 1000, 1000)

INK = "#241E22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1416"}, {"offset": 1, "color": "#060A0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A524A"}, {"offset": 0.7, "color": "#24383A"},
    {"offset": 1, "color": "#121E20"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2E2C"}, {"offset": 1, "color": "#101A18"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCE8A0"}, {"offset": 0.7, "color": "#AAC66E"},
    {"offset": 1, "color": "#7C9852"}]}}
KNOB_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CEDE8E"}, {"offset": 1, "color": "#8AA458"}]}}
CLIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8A86E"}, {"offset": 1, "color": "#96753F"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EEDA"}, {"offset": 1, "color": "#D9D0B4"}]}}
BAND = "#E9DEC4"
BAND_DK = "#B8A77F"
STALK = "#7E9A4E"
STALK_HI = "#BCD582"
GOLD = "#D8B45E"
CX, CY, R = 500, 472, 152

def bez(p0, p1, p2, p3, t):
    mt = 1 - t
    return (mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0],
            mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1])

def bez_tan(p0, p1, p2, p3, t):
    mt = 1 - t
    x = 3*mt*mt*(p1[0]-p0[0]) + 6*mt*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    y = 3*mt*mt*(p1[1]-p0[1]) + 6*mt*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    l = math.hypot(x, y) or 1
    return (x/l, y/l)

def bandaged_arm(p0, p1, p2, p3, label, stripes=(0.28, 0.52, 0.76)):
    dd = f"M{p0[0]},{p0[1]} C{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}"
    d.path(dd, f"{label} ink", fill=NONE, stroke=INK, strokeWidth=42,
           cap="round")
    d.path(dd, f"{label} shade", fill=NONE, stroke="#7A6848",
           strokeWidth=30, cap="round", opacity=35)
    d.path(dd, f"{label} wrap", fill=NONE, stroke=BAND, strokeWidth=30,
           cap="round")
    for i, t in enumerate(stripes):
        px, py = bez(p0, p1, p2, p3, t)
        tx, ty = bez_tan(p0, p1, p2, p3, t)
        nx, ny = -ty, tx
        d.path(f"M{px-nx*14:.0f},{py-ny*14:.0f} L{px+nx*14:.0f},{py+ny*14:.0f}",
               f"{label} seam {i+1}", fill=NONE, stroke=BAND_DK,
               strokeWidth=5, cap="round", opacity=80)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7FA87E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4DCC0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(186,236,8),(806,230,7),(148,516,9),(846,536,8),
                               (250,764,7),(752,750,9),(128,388,6),(866,396,7),
                               (388,108,7),(620,110,8),(336,818,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E4A44", opacity=50, stroke=NONE)

# --- abandoned wellness-parade bunting -------------------------------------------
# string ends anchored on the rim — anything past it leaks off the disc
d.path("M205,161 Q500,248 795,161", "Bunting string", fill=NONE,
       stroke="#5E7A6E", strokeWidth=3, opacity=70)
for i, t in enumerate([0.10, 0.24, 0.38, 0.52, 0.66, 0.80]):
    mt = 1 - t
    px = mt*mt*205 + 2*mt*t*500 + t*t*795
    py = mt*mt*161 + 2*mt*t*248 + t*t*161
    sag = 26 if i == 4 else 40
    col = ["#A86A6A", "#A8985E", "#6A9A8E", "#7A6A9A", "#A86A6A", "#6A9A8E"][i]
    d.path(f"M{px-16:.0f},{py:.0f} L{px+16:.0f},{py:.0f} L{px:.0f},{py+sag:.0f} Z",
           f"Pennant {i+1}", fill=col, opacity=75, stroke=INK, strokeWidth=2)
# one pennant gave up and fell to the floor
d.path("M228,724 L272,730 L246,756 Z", "Fallen pennant", fill="#A86A6A",
       opacity=80, stroke=INK, strokeWidth=2.5)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A1210",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Body shadow", x=372, y=726, width=270, height=26,
        fill="#050A0A", opacity=55, stroke=NONE)

# --- spikes: stalk + knob, bases tucked under the body ---------------------------
for i, ang in enumerate([250, 272, 295, 318, 341, 4, 55, 78, 102, 126,
                         152, 180, 236]):
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    x1, y1 = CX + ca*(R-36), CY + sa*(R-36)
    x2, y2 = CX + ca*(R+22), CY + sa*(R+22)
    kx, ky = CX + ca*(R+30), CY + sa*(R+30)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Stalk {i+1}",
           fill=NONE, stroke=STALK, strokeWidth=16, cap="round")
    d.path(f"M{x1+3:.0f},{y1+3:.0f} L{x2:.0f},{y2:.0f}", f"Stalk hi {i+1}",
           fill=NONE, stroke=STALK_HI, strokeWidth=7, cap="round",
           opacity=70)
    d.shape("ellipse", f"Knob {i+1}", x=kx-17, y=ky-17, width=34, height=34,
            fill=KNOB_GRAD, stroke=INK, strokeWidth=4)

# --- body -------------------------------------------------------------------------
d.shape("ellipse", "Body", x=CX-R, y=CY-R, width=2*R, height=2*R,
        fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=CX-96, y=CY-112, width=110, height=60,
        fill="#FFFFFF", opacity=15, stroke=NONE)
d.shape("ellipse", "Body lo shade", x=CX-70, y=CY+80, width=170, height=60,
        fill="#4E6434", opacity=25, stroke=NONE)

# --- commemorative medal: awarded posthumously to the function --------------------
d.path("M424,514 L414,552 L430,544 Z", "Medal ribbon L", fill="#A84E4E",
       stroke=INK, strokeWidth=3, join="round")
d.path("M440,514 L452,552 L434,544 Z", "Medal ribbon R", fill="#A84E4E",
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Medal", x=417, y=546, width=38, height=38,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0D48A"}, {"offset": 1, "color": "#A8843E"}]}},
        stroke=INK, strokeWidth=4)
d.path("M436,556 L436,570 M429,563 L443,563", "Medal cross", fill=NONE,
       stroke="#7A4E2E", strokeWidth=4, cap="round")

# --- bandaged arms ------------------------------------------------------------------
# left arm up in a wave (waves beside the chart)
bandaged_arm((408, 424), (376, 380), (352, 330), (338, 284), "Arm L")
# loose bandage tail flapping off the left wrist
d.path("M330,268 C316,258 304,262 300,248", "Bandage tail", fill=NONE,
       stroke=BAND, strokeWidth=10, cap="round")
d.shape("ellipse", "Hand L", x=320, y=252, width=42, height=38,
        fill=BAND, stroke=INK, strokeWidth=4)
# right arm reaches down to hold the clipboard
bandaged_arm((586, 512), (622, 542), (640, 560), (644, 548), "Arm R",
             stripes=(0.35, 0.65))
# tiny commemorative health-cross printed on each forearm
for cx_, cy_ in [(356, 346), (636, 552)]:
    d.path(f"M{cx_},{cy_-8} L{cx_},{cy_+8} M{cx_-8},{cy_} L{cx_+8},{cy_}",
           "Bandage cross", fill=NONE, stroke="#A85E5E", strokeWidth=4,
           cap="round", opacity=85)

# --- clipboard: full of optimism -----------------------------------------------------
CBX, CBY, CBD = 672, 640, -8
d.path(rot_rect_path(CBX, CBY, 178, 216, CBD), "Clipboard",
       fill=CLIP_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(CBX, CBY+16, 152, 168, CBD), "Clip paper",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(CBX, CBY-102, 58, 26, CBD), "Clip hinge",
       fill="#6E5A3A", stroke=INK, strokeWidth=3)
# checklist: one box ticked, one box forever pending
for i, ry in enumerate([-26, 14]):
    d.path(rot_rect_path(CBX - 52, CBY + 16 + ry, 22, 22, CBD),
           f"Check box {i+1}", fill="#F6F2E2", stroke=INK, strokeWidth=3)
    d.path(rot_rect_path(CBX + 30, CBY + 16 + ry, 62, 7, CBD),
           f"Line {i+1}", fill="#9A8E6E", stroke=NONE)
# the tick
t1 = (CBX - 60, CBY - 10); t2 = (CBX - 52, CBY - 2); t3 = (CBX - 40, CBY - 18)
def _r(x, y):
    a = math.radians(CBD); c, s = math.cos(a), math.sin(a)
    return (CBX + (x - CBX) * c - (y - CBY) * s,
            CBY + (x - CBX) * s + (y - CBY) * c)
p1, p2, p3 = _r(*t1), _r(*t2), _r(*t3)
d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f} "
       f"L{p3[0]:.0f},{p3[1]:.0f}", "Check tick", fill=NONE,
       stroke="#4E8A4E", strokeWidth=5, cap="round", join="round")
# clipboard title strip
t = d.text("WELLNESS", "Clip title", x=CBX, y=CBY - 36, size=11,
           font="Virelai Sans", color="#5E4E30", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "clip title tilt", ids=[t["id"]], angle=-CBD,
          origin=[CBX, CBY - 36])
# gripping hand on the board's top edge
d.shape("ellipse", "Hand R", x=612, y=520, width=44, height=40,
        fill=BAND, stroke=INK, strokeWidth=4)

# --- face: smiling through the loss -----------------------------------------------------
d.shape("ellipse", "Eye L", x=436, y=404, width=30, height=34,
        fill="#2A2222", stroke=NONE)
d.shape("ellipse", "Eye R", x=534, y=404, width=30, height=34,
        fill="#2A2222", stroke=NONE)
d.shape("ellipse", "Glint L", x=443, y=410, width=9, height=9,
        fill="#F2F6E8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=541, y=410, width=9, height=9,
        fill="#F2F6E8", opacity=90, stroke=NONE)
d.path("M430,388 C442,378 458,376 470,382", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M530,382 C542,376 558,378 570,388", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# the grin: wide, open, unbothered
d.path("M430,470 C446,532 554,532 570,470 C544,492 456,492 430,470 Z",
       "Grin", fill="#4E2A2A", stroke=INK, strokeWidth=5, join="round")
d.path("M438,478 C470,494 530,494 562,478", "Teeth", fill=NONE,
       stroke="#F2EEE0", strokeWidth=7, cap="round")
d.shape("ellipse", "Tongue", x=482, y=508, width=46, height=18,
        fill="#C47A6E", stroke=NONE)
d.shape("ellipse", "Blush L", x=404, y=462, width=30, height=16,
        fill="#C88A6E", opacity=45, stroke=NONE)
d.shape("ellipse", "Blush R", x=566, y=462, width=30, height=16,
        fill="#C88A6E", opacity=45, stroke=NONE)

# --- spores drifting off, relevance expired ----------------------------------------
for i, (x, y, w, o) in enumerate([(286,238,10,40),(742,300,8,35),(252,430,7,30),
                                  (780,470,9,35),(310,640,8,30),(700,690,7,30)]):
    d.shape("ellipse", f"Spore {i+1}", x=x, y=y, width=w, height=w,
            fill="#BCD582", opacity=o, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("PARVOVIRUS-P", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4F0DA", justify="center")
r = d.text("WE WARNED YOU", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8C89A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("061.parvovirus-p-V1R00")
