#!/usr/bin/env python3
"""Porty McBankrupt — mascot portrait V1R00.
An RJ45 port with dollar-sign eyes and a SmartNet badge that still
glows on the fumes of legacy trust. The patch cable lies unplugged at
its feet under a cobweb, price tag still attached; a PAST DUE notice
rests nearby. Bankruptcy is the primary power source.
1000x1000. Gradients + translucent shading, never flat fills.
Dollar signs are set in Source Sans 3 (Virelai carries no figures)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Porty McBankrupt — Mascot Portrait", 1000, 1000)

INK = "#221C22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1318"}, {"offset": 1, "color": "#07090D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3C4A58"}, {"offset": 0.7, "color": "#26323E"},
    {"offset": 1, "color": "#131A22"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#212E3A"}, {"offset": 1, "color": "#10161C"}]}}
SHELL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8B4C4"}, {"offset": 0.7, "color": "#6E7C90"},
    {"offset": 1, "color": "#48525F"}]}}
MOUTH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#18222C"}, {"offset": 1, "color": "#080D12"}]}}
PIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0D88A"}, {"offset": 1, "color": "#B8923E"}]}}
COIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4DC8E"}, {"offset": 1, "color": "#B08A3A"}]}}
GLOW = "#7FE0D8"

def rp(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E94A8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C2D4E2", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(188,238,8),(804,234,7),(150,518,9),(844,536,8),
                               (252,766,7),(750,754,9),(128,392,6),(866,396,7),
                               (390,110,7),(618,110,8),(336,820,6),(664,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E3E4C", opacity=55, stroke=NONE)

# --- cobwebs in the quiet corners ----------------------------------------------------
d.path("M152,240 Q196,192 252,166 M186,190 Q208,214 240,228 "
       "M152,240 L252,166 M198,234 L212,182", "Cobweb L",
       fill=NONE, stroke="#9AAEC2", strokeWidth=1.5, opacity=35)
d.path("M808,182 Q782,216 758,250 M782,190 Q774,222 780,254",
       "Cobweb R", fill=NONE, stroke="#9AAEC2", strokeWidth=1.5,
       opacity=30)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080D10",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Body shadow", x=310, y=688, width=330, height=26,
        fill="#04080A", opacity=60, stroke=NONE)

# --- the overdue notice, face-down on the floor ---------------------------------
PX, PY, PD = 246, 726, -9
d.path(rot_rect_path(PX, PY, 118, 80, PD), "Notice paper",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#E4DCC4"}, {"offset": 1, "color": "#C0B69A"}]}},
       stroke=INK, strokeWidth=3)
t = d.text("PAST DUE", "Notice stamp", x=PX, y=PY - 4, size=15,
           font="Virelai Sans", color="#A84E42", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "notice tilt", ids=[t["id"]], angle=-PD,
          origin=[PX, PY])
q0 = rp(PX, PY, PX - 34, PY + 16, PD); q1 = rp(PX, PY, PX + 34, PY + 16, PD)
d.path(f"M{q0[0]:.0f},{q0[1]:.0f} L{q1[0]:.0f},{q1[1]:.0f}",
       "Notice underline", fill=NONE, stroke="#A84E42", strokeWidth=3,
       opacity=80)

# --- the patch cable, unplugged so long it grew a web -----------------------------
d.path("M788,710 C756,694 726,698 704,682 C686,668 668,674 656,688",
       "Cable", fill=NONE, stroke="#8A7648", strokeWidth=16,
       cap="round")
d.path("M788,710 C756,694 726,698 704,682 C686,668 668,674 656,688",
       "Cable hi", fill=NONE, stroke="#C8AE6A", strokeWidth=6,
       cap="round", opacity=60)
# the plug head, latch up, going nowhere
PPX, PPY, PPD = 648, 688, -32
d.path(rot_rect_path(PPX, PPY, 62, 44, PPD), "Plug head",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#C4D2DC"}, {"offset": 1, "color": "#8A9AA8"}]}},
       stroke=INK, strokeWidth=3, opacity=88)
lp = rp(PPX, PPY, PPX - 6, PPY - 30, PPD)
d.path(rot_rect_path(lp[0], lp[1], 30, 12, PPD), "Plug latch",
       fill="#9AAABA", stroke=INK, strokeWidth=2)
# price tag still tied to the latch
d.path(f"M{lp[0]:.0f},{lp[1]:.0f} C{lp[0]+22:.0f},{lp[1]-26:.0f} "
       f"{lp[0]+42:.0f},{lp[1]-30:.0f} {lp[0]+56:.0f},{lp[1]-26:.0f}",
       "Tag string", fill=NONE, stroke="#8A8272", strokeWidth=2)
TX, TY, TD = lp[0] + 66, lp[1] - 32, 14
d.path(rot_rect_path(TX, TY, 46, 30, TD), "Price tag",
       fill="#E4D8B4", stroke=INK, strokeWidth=2.5)
tt = d.text("$", "Tag price", x=TX, y=TY + 7, size=18,
            font="Source Sans 3", color="#6E5426", justify="center")
if tt and tt.get("id"):
    d.cmd("object.rotate", "tag tilt", ids=[tt["id"]], angle=-TD,
          origin=[TX, TY])
# web strands pinning the plug to the floor
d.path("M612,704 C630,684 654,678 676,688 M622,712 C640,700 662,698 682,704",
       "Plug web", fill=NONE, stroke="#9AAEC2", strokeWidth=1.5,
       opacity=45)

# --- the port itself -----------------------------------------------------------------
# feet first, planted in insolvency
d.shape("ellipse", "Foot L", x=372, y=656, width=62, height=24,
        fill="#3E4854", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=516, y=656, width=62, height=24,
        fill="#3E4854", stroke=INK, strokeWidth=4)
# stub arms, slightly raised like fees are about to be explained
d.path("M326,470 C296,478 280,500 276,524", "Arm L", fill=NONE,
       stroke=INK, strokeWidth=40, cap="round")
d.path("M326,470 C296,478 280,500 276,524", "Arm L skin", fill=NONE,
       stroke="#66748A", strokeWidth=30, cap="round")
d.path("M614,470 C644,478 660,500 664,524", "Arm R", fill=NONE,
       stroke=INK, strokeWidth=40, cap="round")
d.path("M614,470 C644,478 660,500 664,524", "Arm R skin", fill=NONE,
       stroke="#66748A", strokeWidth=30, cap="round")
# housing: a chunky jack, wider at the base for that load-bearing look
d.path("M330,656 L322,382 C322,368 332,358 346,358 L594,358 "
       "C608,358 618,368 618,382 L610,656 Z", "Housing",
       fill=SHELL_GRAD, stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "Shell hi", x=352, y=376, width=110, height=150,
        fill="#FFFFFF", opacity=12, stroke=NONE)
d.shape("ellipse", "Shell lo shade", x=520, y=540, width=90, height=110,
        fill="#141C24", opacity=20, stroke=NONE)
# status LEDs astride the top rim: one blinks with capitalist rage, one dead
d.shape("ellipse", "LED A halo", x=357, y=343, width=26, height=26,
        fill="#D86A52", opacity=30, stroke=NONE)
d.shape("ellipse", "LED A", x=361, y=347, width=18, height=18,
        fill="#D86A52", stroke=INK, strokeWidth=3)
d.shape("ellipse", "LED B", x=569, y=347, width=18, height=18,
        fill="#2A3238", stroke=INK, strokeWidth=3)
# the brow ledge over the socket
d.path(rot_rect_path(470, 432, 236, 22, 0), "Brow ledge",
       fill="#3E4854", stroke=INK, strokeWidth=4, join="round")
d.path("M360,426 L580,426", "Ledge hi", fill=NONE, stroke="#9AAABA",
       strokeWidth=2.5, opacity=60)
# socket mouth: dark opening, eight gold pins like teeth
d.shape("rectangle", "Socket", x=372, y=452, width=196, height=144,
        fill=MOUTH_GRAD, stroke=INK, strokeWidth=5, radius=12)
for i in range(8):
    d.shape("rectangle", f"Pin {i+1}", x=386 + i * 22, y=460,
            width=10, height=30, fill=PIN_GRAD, stroke=INK,
            strokeWidth=2, radius=3)
# residual link glow dying at the bottom of the throat
d.shape("ellipse", "Link glow", x=412, y=564, width=120, height=18,
        fill="#D8A83E", opacity=22, stroke=NONE)
# dollar-sign eyes: two coins where the link lights should be
for i, ex in enumerate([418, 524]):
    d.shape("ellipse", f"Eye {i+1}", x=ex - 26, y=362, width=52,
            height=52, fill=COIN_GRAD, stroke=INK, strokeWidth=4)
    t = d.text("$", f"Dollar {i+1}", x=ex, y=399, size=30,
               font="Source Sans 3", color="#54400F", justify="center")
# the glowing SmartNet badge, lanyarded off the left shoulder
d.path("M330,452 C344,490 356,524 368,556", "Lanyard", fill=NONE,
       stroke="#3A4A5E", strokeWidth=4)
d.shape("ellipse", "Badge glow 1", x=324, y=550, width=120, height=90,
        fill=GLOW, opacity=14, stroke=NONE)
d.shape("ellipse", "Badge glow 2", x=342, y=564, width=84, height=62,
        fill=GLOW, opacity=18, stroke=NONE)
d.path(rot_rect_path(384, 594, 96, 60, -6), "SmartNet badge",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#1C4642"}, {"offset": 1, "color": "#0E2A28"}]}},
       stroke=GLOW, strokeWidth=3)
t = d.text("SMARTNET", "Badge text", x=384, y=588, size=12,
           font="Virelai Sans", color=GLOW, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "badge tilt", ids=[t["id"]], angle=6,
          origin=[384, 594])
sx, sy = rp(384, 594, 416, 608, -6)
d.shape("ellipse", "Badge dot", x=sx - 4, y=sy - 4, width=8, height=8,
        fill=GLOW, stroke=NONE)
qx, qy = rp(384, 594, 352, 606, -6)
t = d.text("ACTIVE", "Badge sub", x=qx + 12, y=qy + 2, size=8,
           font="Source Sans 3", color="#9ADED8", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "badge sub tilt", ids=[t["id"]], angle=6,
          origin=[qx + 12, qy])

# --- captions ----------------------------------------------------------------------
d.text("PORTY MCBANKRUPT", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E2EAF0", justify="center")
r = d.text("LOAD-BEARING INSOLVENCY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A0BACC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("064.porty-mcbankrupt-V1R00")
