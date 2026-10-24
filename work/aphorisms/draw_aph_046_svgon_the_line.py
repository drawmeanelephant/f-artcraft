#!/usr/bin/env python3
"""APH-046 Svgon The Line — aphorism plate V1R00. One immaculate bezier
in full editor chrome — anchors, control handles, dashed tangents — with
a jeweler's loupe proving the edge is still smooth at 3200%, while a
cheap 600 DPI printout of the same curve sits slashed in the corner.
Blueprint plate, cyan stroke, amber handles. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-046 Svgon The Line — Aphorism Plate", 1000, 1000)

INK = "#0A1420"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14222F"}, {"offset": 1, "color": "#070D14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#27465C"}, {"offset": 0.7, "color": "#16293A"},
    {"offset": 1, "color": "#0B1722"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D4AE"}, {"offset": 0.65, "color": "#CDB88E"},
    {"offset": 1, "color": "#A88F60"}]}}
CHIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A5A72"}, {"offset": 1, "color": "#1E3446"}]}}
CURVE = "#7AD8E8"
CURVE_HI = "#D8F4FA"
CURVE_LO = "#2E7A90"
AMBER = "#E8B45A"
NODE = "#F0E8D8"
RED = "#B04038"
CREAM = "#E8F0F2"
KEY = "#B8DCE4"
FAINT = "#7A9AAC"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A7A9C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9AC8DC", strokeWidth=3, opacity=35)
# blueprint grid, faint — the geometry underneath
for i, gx in enumerate(range(200, 900, 100)):
    d.path(f"M{gx},110 L{gx},820", f"Grid v{i}", fill=NONE,
           stroke="#3A5A72", strokeWidth=1, opacity=14)
for i, gy in enumerate(range(160, 800, 100)):
    d.path(f"M150,{gy} L850,{gy}", f"Grid h{i}", fill=NONE,
           stroke="#3A5A72", strokeWidth=1, opacity=14)
d.shape("ellipse", "Patina 1", x=210, y=170, width=200, height=110,
        fill="#33536A", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#33536A", opacity=14, stroke=NONE)

# --- the insult: a 600 DPI printout, slashed -------------------------------------
# sepia paper, slightly askew, bottom left
d.path(rot_rect_path(271, 682, 170, 130, -6), "Printout shadow",
       fill="#000000", opacity=30, stroke=NONE)
d.path(rot_rect_path(265, 675, 170, 130, -6), "Printout",
       fill=PAPER_GRAD, stroke="#6E5A38", strokeWidth=3)
# jagged staircase where the smooth curve should be
t = math.radians(-6); c_, s_ = math.cos(t), math.sin(t)
def px(dx, dy):  # rotate an offset around the printout center (265,675)
    return 265 + dx * c_ - dy * s_, 675 + dx * s_ + dy * c_
steps = [(-60, 32), (-47, 26), (-34, 26), (-21, 20), (-8, 20), (5, 14),
         (18, 8), (31, 8), (44, 1), (57, -6)]
for i, (dx, dy) in enumerate(steps):
    x, y = px(dx, dy)
    d.path(rot_rect_path(x, y, 14, 14, -6), f"Jaggy {i+1}",
           fill="#8A8478", opacity=80, stroke="#5A5448", strokeWidth=1)
# tilted tag pinned to the printout corner — digits in Source Sans 3
d.path(rot_rect_path(190, 590, 82, 30, -6), "DPI tag",
       fill=CHIP_GRAD, stroke="#6E5A38", strokeWidth=2.5)
d.text("600 DPI", "DPI tag text", x=190, y=596, size=13,
       font="Source Sans 3", color="#E4D4AE", justify="center")
# the verdict: red circle-slash across the whole page
d.shape("ellipse", "Slash ring", x=190, y=618, width=150, height=120,
        fill=NONE, stroke=RED, strokeWidth=7, opacity=85)
d.path("M205,730 L328,626", "Slash bar", fill=NONE, stroke=RED,
       strokeWidth=7, cap="round", opacity=85)
d.shape("ellipse", "Slash ring ghost", x=194, y=622, width=150, height=120,
        fill=NONE, stroke=RED, strokeWidth=3, opacity=30)

# --- the perfect bezier ------------------------------------------------------------
# curve: M300,480 C420,545 520,260 720,320
CURVE_D = "M300,480 C420,545 520,260 720,320"
# glow + body + hot core — a neon tube of pure mathematics
d.path(CURVE_D, "Curve glow", fill=NONE, stroke=CURVE, strokeWidth=24,
       cap="round", opacity=18)
d.path(CURVE_D, "Curve body", fill=NONE, stroke=CURVE_LO, strokeWidth=13,
       cap="round")
d.path(CURVE_D, "Curve mid", fill=NONE, stroke=CURVE, strokeWidth=8,
       cap="round")
d.path(CURVE_D, "Curve core", fill=NONE, stroke=CURVE_HI, strokeWidth=3,
       cap="round")
# editor chrome: dashed tangents to the control points
d.path("M300,480 L420,545", "Tangent A", fill=NONE, stroke=AMBER,
       strokeWidth=2, dash=[6, 6], opacity=80)
d.path("M720,320 L520,260", "Tangent B", fill=NONE, stroke=AMBER,
       strokeWidth=2, dash=[6, 6], opacity=80)
# control handles: amber rings
d.shape("ellipse", "Ctrl A", x=414, y=539, width=12, height=12,
        fill="#16293A", stroke=AMBER, strokeWidth=3)
d.shape("ellipse", "Ctrl B", x=514, y=254, width=12, height=12,
        fill="#16293A", stroke=AMBER, strokeWidth=3)
# anchor squares at the endpoints
for i, (ax, ay) in enumerate([(300, 480), (720, 320)]):
    d.path(rot_rect_path(ax, ay, 15, 15, 45), f"Anchor {i+1}",
           fill=NODE, stroke=INK, strokeWidth=2.5)

# --- the loupe: still smooth at 3200% -----------------------------------------------
LX, LY, LR = 585, 335, 88
# handle first, tucked under the glass
d.path(f"M{LX + 62},{LY + 62} L{LX + 118},{LY + 118}", "Loupe handle",
       fill=NONE, stroke="#4A7A9C", strokeWidth=14, cap="round")
d.path(f"M{LX + 62},{LY + 62} L{LX + 112},{LY + 112}", "Handle sheen",
       fill=NONE, stroke="#7AB8D8", strokeWidth=4, cap="round",
       opacity=60)
# glass
d.shape("ellipse", "Loupe glass", x=LX - LR, y=LY - LR, width=2 * LR,
        height=2 * LR, fill="#FFFFFF", opacity=8, stroke=NONE)
# magnified curve segment crossing the glass — the same arc, razor smooth
d.path("M517,376 C560,350 620,326 666,313", "Zoom curve glow",
       fill=NONE, stroke=CURVE, strokeWidth=44, cap="round", opacity=18)
d.path("M517,376 C560,350 620,326 666,313", "Zoom curve body",
       fill=NONE, stroke=CURVE_LO, strokeWidth=32, cap="round")
d.path("M517,376 C560,350 620,326 666,313", "Zoom curve mid",
       fill=NONE, stroke=CURVE, strokeWidth=22, cap="round")
d.path("M517,376 C560,350 620,326 666,313", "Zoom curve core",
       fill=NONE, stroke=CURVE_HI, strokeWidth=8, cap="round")
# faint magnified grid inside the glass
for i, off in enumerate([-40, 0, 40]):
    d.path(f"M{LX + off},{LY - 70} L{LX + off},{LY + 70}",
           f"Zoom grid v{i}", fill=NONE, stroke="#9AC8DC",
           strokeWidth=1, opacity=18)
    d.path(f"M{LX - 70},{LY + off} L{LX + 70},{LY + off}",
           f"Zoom grid h{i}", fill=NONE, stroke="#9AC8DC",
           strokeWidth=1, opacity=18)
# rim
d.shape("ellipse", "Loupe rim", x=LX - LR, y=LY - LR, width=2 * LR,
        height=2 * LR, fill=NONE, stroke="#9AC8DC", strokeWidth=9)
d.shape("ellipse", "Rim sheen", x=LX - LR + 14, y=LY - LR + 12,
        width=60, height=26, fill="#FFFFFF", opacity=22, stroke=NONE)
# zoom chip — digits in Source Sans 3
d.shape("rectangle", "Zoom chip", x=LX - 118, y=LY - 108, width=86,
        height=30, radius=7, fill=CHIP_GRAD, stroke="#4A7A9C",
        strokeWidth=2.5)
d.text("3200%", "Zoom text", x=LX - 75, y=LY - 87, size=14,
       font="Source Sans 3", color=AMBER, justify="center")

# faint echo arc: the same curve again, zoomed out of existence — still crisp
d.path("M270,540 C420,600 560,230 760,295", "Echo curve", fill=NONE,
       stroke=CURVE, strokeWidth=3, cap="round", opacity=14)

# --- aphorism line + name + role -----------------------------------------------------
r = d.text("CRISP AT ANY SIZE.", "Key line", x=500, y=768, size=24,
           font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=140)

d.text("SVGON THE LINE", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("ANYTHING BELOW 600 DPI IS A SMEAR", "Role", x=500, y=950,
           size=18, font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    # Virelai Sans has no digit glyphs — byte-range fallback for "600"
    d.cmd("text.setStyle", "role digits", ids=[r["id"]], start=15, end=18,
          font="Source Sans 3")
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=150)

d.finish("aph-046-svgon-the-line-V1R00")
