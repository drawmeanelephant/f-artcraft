#!/usr/bin/env python3
"""Stackdodge — mascot portrait V1R00.
Dodge-stacking theorist tanking the third consecutive Gruul wipe:
spreadsheet carried as a shield, a helm with three gem sockets and
not one of them filled, parse board telling a truth he will not read.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Stackdodge — Mascot Portrait", 1000, 1000)

INK = "#221C24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0F1418"}, {"offset": 1, "color": "#090B0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5450"}, {"offset": 0.7, "color": "#2A3C3C"},
    {"offset": 1, "color": "#161F22"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#243233"}, {"offset": 1, "color": "#121A1C"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#AFC4BC"}, {"offset": 0.7, "color": "#7E948C"},
    {"offset": 1, "color": "#566A64"}]}}
HELM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#96A2B4"}, {"offset": 1, "color": "#5A6678"}]}}
SHEET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDF2E2"}, {"offset": 1, "color": "#C8D4B8"}]}}
BOARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#39424A"}, {"offset": 1, "color": "#232A30"}]}}
GREEN = "#7FD08A"
RED = "#D06058"
GOLD = "#E0C070"
GRID = "#7A9478"
CHALK = "#C8D2CE"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

def star4(cx, cy, s, label, **kw):
    r = s * 0.22
    d.path(f"M{cx},{cy-s} Q{cx+r},{cy-r} {cx+s},{cy} Q{cx+r},{cy+r} "
           f"{cx},{cy+s} Q{cx-r},{cy+r} {cx-s},{cy} Q{cx-r},{cy-r} "
           f"{cx},{cy-s} Z", label, **kw)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7FA89C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DED4", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(190,240,8),(802,234,7),(152,522,9),(842,540,8),
                               (254,768,7),(748,754,9),(130,392,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,822,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#33484A", opacity=50, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E1214",
       strokeWidth=4, opacity=70)

# --- the parse board: diminishing returns, diminishing hope -------------------------
d.path(rot_rect_path(252, 350, 244, 218, -5), "Parse board",
       fill=BOARD_GRAD, stroke=INK, strokeWidth=5, join="round")
hx, hy = rot_pt(252, 350, 252, 262, -5)
d.path(rot_rect_path(hx, hy, 228, 26, -5), "Board bar",
       fill="#2A3238", stroke=NONE)
t = d.text("PARSES", "Board title", x=hx, y=hy + 6, size=13,
           font="Virelai Sans", color=CHALK, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "board title tilt", ids=[t["id"]], angle=5,
          origin=[hx, hy])
# four parse rows: name squiggle + performance bar, Stackdodge last and red
for i, (ly, blen, col) in enumerate([(302, 148, GREEN), (330, 122, GREEN),
                                     (358, 96, GREEN), (386, 34, RED)]):
    nx, ny = rot_pt(252, 350, 178, ly, -5)
    if i == 3:
        t = d.text("STACKDODGE", "Parse shame", x=nx + 24, y=ny + 4, size=7,
                   font="Virelai Sans", color=RED, justify="center")
        if t and t.get("id"):
            d.cmd("object.rotate", "shame tilt", ids=[t["id"]], angle=5,
                  origin=[nx, ny])
    else:
        d.path(rot_rect_path(nx, ny, 52, 9, -5), f"Name squig {i+1}",
               fill="#7E8A8E", opacity=70, stroke=NONE)
    bx, by = rot_pt(252, 350, 214 + blen / 2, ly, -5)
    d.path(rot_rect_path(bx, by, blen, 13, -5), f"Parse bar {i+1}",
           fill=col, opacity=85 if col == GREEN else 95, stroke=NONE)
# diminishing-returns curve inset, flattening out like the argument
ax1, ay1 = rot_pt(252, 350, 168, 446, -5)
ax2, ay2 = rot_pt(252, 350, 336, 446, -5)
ax3, ay3 = rot_pt(252, 350, 168, 408, -5)
d.path(f"M{ax1:.0f},{ay1:.0f} L{ax2:.0f},{ay2:.0f} M{ax1:.0f},{ay1:.0f} "
       f"L{ax3:.0f},{ay3:.0f}", "DR axes", fill=NONE, stroke="#6E7A80",
       strokeWidth=2.5, cap="round")
c0 = rot_pt(252, 350, 168, 444, -5); c1 = rot_pt(252, 350, 210, 418, -5)
c2 = rot_pt(252, 350, 280, 410, -5); c3 = rot_pt(252, 350, 334, 408, -5)
d.path(f"M{c0[0]:.0f},{c0[1]:.0f} C{c1[0]:.0f},{c1[1]:.0f} "
       f"{c2[0]:.0f},{c2[1]:.0f} {c3[0]:.0f},{c3[1]:.0f}", "DR curve",
       fill=NONE, stroke=GOLD, strokeWidth=3, cap="round")

# --- the wipe slate: third consecutive -----------------------------------------------
d.path(rot_rect_path(742, 226, 176, 118, 6), "Wipe slate",
       fill=BOARD_GRAD, stroke=INK, strokeWidth=5, join="round")
tx, ty = rot_pt(742, 226, 742, 190, 6)
t = d.text("WIPES", "Slate title", x=tx, y=ty, size=13,
           font="Virelai Sans", color=CHALK, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "slate tilt", ids=[t["id"]], angle=-6,
          origin=[tx, ty])
# three tally clusters — letters can't fail us here
for g in range(3):
    gx, gy = 700 + g * 42, 240
    for k in range(4):
        p1 = rot_pt(742, 226, gx + k * 8, gy - 14, 6)
        p2 = rot_pt(742, 226, gx + k * 8 + 2, gy + 16, 6)
        d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
               f"Tally {g+1}-{k+1}", fill=NONE, stroke=CHALK,
               strokeWidth=3, cap="round", opacity=85)
    p1 = rot_pt(742, 226, gx - 6, gy + 14, 6)
    p2 = rot_pt(742, 226, gx + 30, gy - 12, 6)
    d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
           f"Tally {g+1}-x", fill=NONE, stroke=RED, strokeWidth=3,
           cap="round", opacity=85)

# --- latency denial, in a pill --------------------------------------------------------
d.shape("rectangle", "Lag pill", x=584, y=126, width=120, height=36,
        fill="#2A3238", stroke=INK, strokeWidth=3, radius=18)
for i, hgt in enumerate([10, 16, 22]):
    d.shape("rectangle", f"Lag bar {i+1}", x=598 + i * 12,
            y=152 - hgt, width=8, height=hgt, fill=RED, stroke=NONE,
            radius=2)
t = d.text("LAG", "Lag text", x=668, y=150, size=14,
           font="Virelai Sans", color=RED, justify="center")

# --- the spreadsheet shield: grid paper as a kite shield ------------------------------
# shield silhouette around (396,586), tilted into the fight
SCX, SCY, SDEG = 396, 590, -10
d.shape("ellipse", "Shield shadow", x=320, y=688, width=170, height=18,
        fill="#06080A", opacity=50, stroke=NONE)
d.path(rot_rect_path(SCX, SCY, 196, 236, SDEG), "Sheet shield",
       fill=SHEET_GRAD, stroke=INK, strokeWidth=6, join="round")
# column headers A B C D, letters only so Virelai carries them
for i, col in enumerate(["A", "B", "C", "D"]):
    px, py = rot_pt(SCX, SCY, SCX - 66 + i * 44, SCY - 96, SDEG)
    d.path(rot_rect_path(px, py, 40, 18, SDEG), f"Col hd {col}",
           fill="#8FA88A", opacity=85, stroke=NONE)
    t = d.text(col, f"Col letter {col}", x=px, y=py + 5, size=11,
               font="Virelai Sans", color="#2E3A2E", justify="center")
    if t and t.get("id"):
        d.cmd("object.rotate", f"col {col} tilt", ids=[t["id"]],
              angle=-SDEG, origin=[px, py])
# gridlines
for i in range(4):
    gy = SCY - 70 + i * 40
    p1 = rot_pt(SCX, SCY, SCX - 88, gy, SDEG)
    p2 = rot_pt(SCX, SCY, SCX + 88, gy, SDEG)
    d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
           f"Grid h {i+1}", fill=NONE, stroke=GRID, strokeWidth=2,
           opacity=80)
for i in range(3):
    gx = SCX - 44 + i * 44
    p1 = rot_pt(SCX, SCY, gx, SCY - 84, SDEG)
    p2 = rot_pt(SCX, SCY, gx, SCY + 104, SDEG)
    d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
           f"Grid v {i+1}", fill=NONE, stroke=GRID, strokeWidth=2,
           opacity=80)
# the cell where the build broke: highlighted, questioned
cx0, cy0 = rot_pt(SCX, SCY, SCX + 22, SCY + 24, SDEG)
d.path(rot_rect_path(cx0, cy0, 40, 34, SDEG), "Bad cell", fill=RED,
       opacity=45, stroke=RED, strokeWidth=2)
t = d.text("?", "Bad cell mark", x=cx0, y=cy0 + 8, size=18,
           font="Virelai Sans", color=RED, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "cell tilt", ids=[t["id"]], angle=-SDEG,
          origin=[cx0, cy0])
# sheet tab label
tx0, ty0 = rot_pt(SCX, SCY, SCX - 50, SCY + 122, SDEG)
t = d.text("DODGE", "Sheet tab", x=tx0, y=ty0, size=10,
           font="Virelai Sans", color="#4E5E48", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "tab tilt", ids=[t["id"]], angle=-SDEG,
          origin=[tx0, ty0])

# --- Stackdodge: high IQ, low situational awareness -------------------------------------
d.shape("ellipse", "Dodge shadow", x=430, y=686, width=240, height=22,
        fill="#06080A", opacity=55, stroke=NONE)
# pennant hand up: the Phase II flag nobody asked for
d.path("M640,556 C664,512 676,470 682,430", "Flag arm ink", fill=NONE,
       stroke=INK, strokeWidth=36, cap="round")
d.path("M640,556 C664,512 676,470 682,430", "Flag arm", fill=NONE,
       stroke="#7E948C", strokeWidth=26, cap="round")
d.path("M682,432 L694,320", "Flag pole", fill=NONE, stroke="#6E5E44",
       strokeWidth=7, cap="round")
d.path("M694,318 L816,330 L694,364 Z", "Pennant", fill=GOLD,
       stroke=INK, strokeWidth=4, join="round")
t = d.text("PHASE II", "Pennant text", x=730, y=345, size=10,
           font="Virelai Sans", color="#5E4E30", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "pennant tilt", ids=[t["id"]], angle=-8,
          origin=[730, 343])
# stocky body
d.path("M540,470 C610,470 656,524 656,592 C656,662 610,700 540,700 "
       "C470,700 424,662 424,592 C424,524 470,470 540,470 Z",
       "Dodge body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=468, y=506, width=90, height=46,
        fill="#FFFFFF", opacity=13, stroke=NONE)
# pauldrons: armor he has, sockets he does not
d.shape("ellipse", "Pauldron L", x=414, y=496, width=66, height=52,
        fill=HELM_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pauldron R", x=610, y=500, width=60, height=48,
        fill=HELM_GRAD, stroke=INK, strokeWidth=5)
# the helm: dome + brow band + nasal, three sockets and every one empty
d.path("M452,486 C452,404 628,404 628,486 L628,494 L452,494 Z",
       "Helm dome", fill=HELM_GRAD, stroke=INK, strokeWidth=6,
       join="round")
d.path("M470,452 C500,432 580,432 610,452", "Dome hi", fill=NONE,
       stroke="#C4CEDC", strokeWidth=4, cap="round", opacity=60)
d.path(rot_rect_path(540, 494, 180, 16, 0), "Brow band",
       fill="#4E5A6C", stroke=INK, strokeWidth=4)
d.path("M536,494 L544,494 L544,540 L536,540 Z", "Nasal",
       fill="#4E5A6C", stroke=INK, strokeWidth=3)
for i, sx in enumerate([486, 540, 594]):
    d.shape("ellipse", f"Socket rim {i+1}", x=sx - 15, y=438,
            width=30, height=30, fill=GOLD, stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Socket hole {i+1}", x=sx - 9, y=444,
            width=18, height=18, fill="#1A222C", stroke=NONE)
# face: determined, looking at the incoming phase instead of the meter
d.shape("ellipse", "Eye L", x=492, y=524, width=28, height=30,
        fill="#2A2020", stroke=NONE)
d.shape("ellipse", "Eye R", x=560, y=524, width=28, height=30,
        fill="#2A2020", stroke=NONE)
d.shape("ellipse", "Glint L", x=498, y=530, width=8, height=8,
        fill="#EAF0EC", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=566, y=530, width=8, height=8,
        fill="#EAF0EC", opacity=85, stroke=NONE)
d.path("M490,506 L522,500 M560,500 L592,506", "Brow set", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M516,580 C532,588 552,588 566,578", "Grin", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# planted feet
d.shape("ellipse", "Foot L", x=480, y=690, width=44, height=18,
        fill="#566A64", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=560, y=690, width=44, height=18,
        fill="#566A64", stroke=INK, strokeWidth=3)

# --- captions ----------------------------------------------------------------------
d.text("STACKDODGE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4EEE8", justify="center")
r = d.text("DODGE-STACKING THEORIST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9EBCB0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("059.stackdodge-V1R00")
