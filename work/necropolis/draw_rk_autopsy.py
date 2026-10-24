#!/usr/bin/env python3
"""rc-autopsy.sh — The Dissection. Necropolis plate V1R00.
A shell script laid out on a marble slab under a surgeon's lamp, tagged
by the toe with its filename, its functions sectioned and pinned like
specimens in a catalog tray. Cause of death: none — it just wanted to
be understood. Steel, marble, and lamp white. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Autopsy — Necropolis Plate", 1000, 1000)

INK = "#1C2028"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10141C"}, {"offset": 1, "color": "#07090E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4C545E"}, {"offset": 0.7, "color": "#2C323C"},
    {"offset": 1, "color": "#141820"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#262C36"}, {"offset": 1, "color": "#10141A"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A8694"}, {"offset": 1, "color": "#424C58"}]}}
SHADE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A545F"}, {"offset": 1, "color": "#222A34"}]}}
MARBLE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DDE2E6"}, {"offset": 1, "color": "#AEB6BE"}]}}
MARBLE_EDGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B4BAC2"}, {"offset": 1, "color": "#7E8792"}]}}
PEDESTAL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A929C"}, {"offset": 1, "color": "#4E5660"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D6B4"}, {"offset": 1, "color": "#B8A67E"}]}}
TRAY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A6470"}, {"offset": 1, "color": "#333B46"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E8894", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D9DEE8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#525C68", opacity=35, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0B0D12",
       strokeWidth=4, opacity=70)
d.path("M240,758 C400,778 600,778 760,758", "Flagstone", fill=NONE,
       stroke="#333B46", strokeWidth=3, opacity=40)
d.shape("ellipse", "Slab shadow", x=240, y=684, width=520, height=24,
        fill="#04060A", opacity=55, stroke=NONE)

# --- the surgeon's lamp ------------------------------------------------------------
d.path("M500,60 L500,140", "Lamp cord", fill=NONE, stroke="#2A323C",
       strokeWidth=6)
d.path("M500,60 L500,140", "Cord highlight", fill=NONE, stroke="#8A95A2",
       strokeWidth=2, opacity=50)
# dome shade
d.path("M440,150 C440,118 560,118 560,150 L585,200 L415,200 Z",
       "Lamp shade", fill=SHADE, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Shade rim", x=415, y=192, width=170, height=26,
        fill=STEEL, stroke=INK, strokeWidth=4)
d.path("M455,148 C465,132 490,126 510,126", "Shade glint", fill=NONE,
       stroke="#A8B4C0", strokeWidth=4, opacity=60, cap="round")
# bulb + inner glow
d.shape("ellipse", "Bulb", x=480, y=200, width=40, height=24,
        fill="#FFF6DC", stroke=INK, strokeWidth=3)
# cone of lamplight falling on the slab
d.path("M430,214 L570,214 L700,560 L300,560 Z", "Light cone",
       fill="#FFF6DC", opacity=8, stroke=NONE)
d.path("M465,214 L535,214 L620,560 L380,560 Z", "Light core",
       fill="#FFF6DC", opacity=10, stroke=NONE)
d.shape("ellipse", "Light pool", x=330, y=536, width=340, height=60,
        fill="#FFF3D0", opacity=12, stroke=NONE)

# --- the morgue wall: faint vault drawers behind the slab ----------------------------
for i, (dx, dy) in enumerate([(185, 280), (185, 350), (185, 420),
                              (705, 280), (705, 350), (705, 420)]):
    d.shape("rectangle", f"Vault drawer {i+1}", x=dx, y=dy, width=130,
            height=56, fill=NONE, stroke="#0E1218", strokeWidth=4,
            opacity=45, radius=4)
    d.path(f"M{dx+50},{dy+28} L{dx+80},{dy+28}", f"Drawer pull {i+1}",
           fill=NONE, stroke="#0E1218", strokeWidth=4, opacity=50,
           cap="round")

# --- the marble slab ---------------------------------------------------------------
# top surface, slightly wider at the front
d.path("M310,540 L690,540 L730,615 L270,615 Z", "Slab top", fill=MARBLE,
       stroke=INK, strokeWidth=5, join="round")
# front edge
d.shape("rectangle", "Slab edge", x=270, y=615, width=460, height=30,
        fill=MARBLE_EDGE, stroke=INK, strokeWidth=5)
# pedestal
d.shape("rectangle", "Pedestal", x=440, y=645, width=120, height=48,
        fill=PEDESTAL, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Pedestal foot", x=420, y=688, width=160, height=14,
        fill=PEDESTAL, stroke=INK, strokeWidth=4, radius=3)
# marble veins on the top
d.path("M330,560 C400,568 430,552 500,560 C560,566 600,556 660,565",
       "Vein 1", fill=NONE, stroke="#8A929C", strokeWidth=2, opacity=45)
d.path("M350,592 C420,584 480,598 560,590 C610,585 640,592 690,588",
       "Vein 2", fill=NONE, stroke="#8A929C", strokeWidth=2, opacity=35)
d.path("M300,575 C330,580 345,572 370,578", "Vein 3", fill=NONE,
       stroke="#8A929C", strokeWidth=2, opacity=40)

# --- the script, laid out ------------------------------------------------------------
# long parchment printout with a gently waved edge, curled foot
d.path("M330,556 C360,548 400,552 440,550 C500,546 560,552 610,548 "
       "C630,547 644,550 648,556 L646,600 C600,606 540,600 480,604 "
       "C430,607 380,602 332,606 Z",
       "Script body", fill=PARCH, stroke=INK, strokeWidth=4, join="round")
# shebang + code rows as printed strokes (pre-blended inks, never transparent text)
rows = [
    (352, 560, 190, "#5A4A34"),
    (352, 570, 150, "#6E5C44"),
    (366, 580, 200, "#6E5C44"),
    (366, 590, 130, "#7A684E"),
    (352, 600, 170, "#8A7658"),
]
for i, (x, y, w, col) in enumerate(rows):
    d.path(f"M{x},{y} L{x+w},{y}", f"Code row {i+1}", fill=NONE,
           stroke=col, strokeWidth=3, opacity=90, cap="round")
# a function glyph mark on the sheet
d.text("}", "Brace mark", x=610, y=596, size=20, font="Virelai Sans",
       color="#5A4A34", justify="center")

# --- toe tag on the foot end -------------------------------------------------------------
d.path("M646,590 L690,606", "Tag string", fill=NONE, stroke="#8A7450",
       strokeWidth=2)
d.path("M688,596 L752,602 L748,634 L684,628 Z", "Toe tag", fill=PARCH,
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Tag eyelet", x=690, y=606, width=7, height=7,
        fill=NONE, stroke=INK, strokeWidth=2)
d.text("rc-autopsy.sh", "Tag name", x=716, y=622, size=10,
       font="Virelai Sans", color="#4A3826", justify="center")

# --- scalpel on the slab ------------------------------------------------------------------
d.path("M550,618 L630,612", "Scalpel handle", fill=NONE, stroke="#2A323C",
       strokeWidth=6, cap="round")
d.path("M630,612 L662,604 L634,620 Z", "Scalpel blade", fill=STEEL,
       stroke=INK, strokeWidth=2, join="round")
d.path("M560,615 L614,610", "Handle glint", fill=NONE, stroke="#A8B4C0",
       strokeWidth=2, opacity=60, cap="round")

# --- the catalog tray: sectioned functions, pinned -----------------------------------------
d.shape("ellipse", "Tray shadow", x=660, y=692, width=150, height=14,
        fill="#04060A", opacity=50, stroke=NONE)
d.path("M652,640 L792,640 L800,690 L644,690 Z", "Tray", fill=TRAY,
       stroke=INK, strokeWidth=4, join="round")
d.path("M660,650 L784,650 L788,682 L656,682 Z", "Tray bed",
       fill="#20262E", stroke=INK, strokeWidth=2)
# pinned specimens: two rows of sectioned function strips
for i, (sx, sy) in enumerate([(672, 658), (716, 658), (760, 658),
                              (682, 672), (728, 672), (770, 672)]):
    d.shape("rectangle", f"Specimen {i+1}", x=sx, y=sy, width=30, height=10,
            fill=PARCH, stroke=INK, strokeWidth=1, radius=1)
    d.shape("ellipse", f"Pin {i+1}", x=sx+12, y=sy-3, width=6, height=6,
            fill="#C8D0D8", stroke=INK, strokeWidth=1)
    d.path(f"M{sx+15},{sy+1} L{sx+15},{sy+9}", f"Pin stem {i+1}", fill=NONE,
           stroke="#8A929C", strokeWidth=1)

# --- captions ------------------------------------------------------------------
d.text("RC-AUTOPSY", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E2E6EC", justify="center")
r = d.text("SCRIPT DISSECTION", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA4B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-autopsy-V1R00")
