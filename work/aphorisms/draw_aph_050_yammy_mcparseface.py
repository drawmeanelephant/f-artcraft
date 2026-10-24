#!/usr/bin/env python3
"""APH-050 Yammy McParseface — aphorism plate V1R00. A house whose walls
are literal YAML lines: labeled bars stacked to their indent. The
foundation line is set one indent too deep — shown solid where it
landed, ghosted where it belonged — and the whole right wall above it
shears off along a crack, window pane dropped, flames already licking
the wreckage. Trailing spaces drift off the bad line like curses.
Stormy slate plate, warm wood, red error. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-050 Yammy McParseface — Aphorism Plate", 1000, 1000)

INK = "#1C242E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131A24"}, {"offset": 1, "color": "#06090E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#384452"}, {"offset": 0.7, "color": "#1F2832"},
    {"offset": 1, "color": "#0F141B"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C49A68"}, {"offset": 0.6, "color": "#96683E"},
    {"offset": 1, "color": "#5E3E22"}]}}
ROOF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5A48"}, {"offset": 1, "color": "#4E2E24"}]}}
BAD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B04A38"}, {"offset": 1, "color": "#6E281E"}]}}
FIRE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4C06A"}, {"offset": 0.55, "color": "#E8833A"},
    {"offset": 1, "color": "#A83618"}]}}
ERR = "#D84A38"
CREAM = "#E4E8EA"
FAINT = "#7E90A0"
KEY = "#A8C4D8"
GHOST = "#8AA0B8"

def rot_pts(cx, cy, pts, deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return [(cx + (x - cx) * c - (y - cy) * s,
             cy + (x - cx) * s + (y - cy) * c) for x, y in pts]

def poly(pts, label, **kw):
    ds = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return d.path(ds, label, **kw)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7488", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8C4D8", strokeWidth=3, opacity=40)
# plate patina
d.shape("ellipse", "Patina 1", x=200, y=185, width=200, height=120,
        fill="#4E5E6E", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=590, width=220, height=130,
        fill="#4E5E6E", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(208, 258, 7), (793, 250, 8), (158, 503, 6),
                               (844, 497, 7), (252, 736, 6), (760, 726, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E7488", opacity=35, stroke=NONE)

# floor shadow under the house
d.shape("ellipse", "Floor shadow", x=330, y=640, width=400, height=44,
        fill="#000000", opacity=32, stroke=NONE)

# --- indent guides: the levels the file agreed on ------------------------------
for gx in (415, 445):
    d.path(f"M{gx},352 L{gx},568", f"Indent guide {gx}", fill=NONE,
           stroke=GHOST, strokeWidth=1.5, opacity=30, dash=[3, 9])

# --- the roof -------------------------------------------------------------------
# left plane intact
poly([(365, 352), (500, 250), (500, 352)], "Roof left",
     fill=ROOF_GRAD, stroke=INK, strokeWidth=4)
# right plane has slid: rotated about its own middle, eave dipping
rp = rot_pts(567, 301, [(500, 250), (635, 352), (500, 352)], 13)
poly(rp, "Roof right", fill=ROOF_GRAD, stroke=INK, strokeWidth=4)
# gap flash where the planes parted
d.path("M500,252 L498,350", "Roof split", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=60)
# chimney, still smug on the intact slope
d.shape("rectangle", "Chimney", x=422, y=212, width=34, height=72,
        fill=ROOF_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Chimney lip", x=418, y=206, width=42, height=12,
        radius=3, fill=ROOF_GRAD, stroke=INK, strokeWidth=3)

# --- the walls: YAML lines, stacked to their indent ------------------------------
ROWS = [(360, "eaves:"), (390, "north_wall:"), (420, "lintel:"),
        (450, "pane:"), (480, "sill:"), (510, "stud:")]
# right halves shear: worse the lower you go
SHEAR = [(3, 2, 2), (5, 3, 3), (7, 4, 5), (9, 6, 7), (12, 9, 10),
         (15, 12, 12)]
for i, ((ry, label), (rot, dx, dy)) in enumerate(zip(ROWS, SHEAR)):
    # intact left half of the line
    d.shape("rectangle", f"Row {i} L", x=385, y=ry, width=115, height=24,
            fill=WOOD_GRAD, stroke=INK, strokeWidth=3)
    d.text(label, f"Row {i} key", x=392, y=ry + 16, size=9,
           font="Virelai Sans", color=INK, justify="left")
    # sheared right half — slid down-right, tilted
    cx, cy = 500 + 57.5 + dx, ry + 12 + dy
    rp = rot_pts(cx, cy, [(500 + dx, ry + dy), (615 + dx, ry + dy),
                          (615 + dx, ry + 24 + dy), (500 + dx, ry + 24 + dy)],
                 rot)
    poly(rp, f"Row {i} R", fill=WOOD_GRAD, stroke=INK, strokeWidth=3)

# the crack running down the shear seam
d.path("M502,356 L512,396 L496,436 L508,476 L498,516 L512,548",
       "Shear crack", fill=NONE, stroke="#0E141A", strokeWidth=4,
       opacity=80, cap="round")

# door and window on the intact left half, hugging the failing seam
d.shape("rectangle", "Door", x=455, y=478, width=40, height=62,
        radius=4, fill="#3A2A1A", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Door knob", x=485, y=506, width=6, height=6,
        fill=KEY, stroke=NONE)
d.shape("rectangle", "Window", x=448, y=398, width=38, height=36,
        radius=3, fill="#B8D0D8", stroke=INK, strokeWidth=3)
d.path("M467,398 L467,434 M448,416 L486,416", "Window mullions",
       fill=NONE, stroke=INK, strokeWidth=2)

# --- the bad line: foundation, one indent too deep -------------------------------
# where it belonged — dashed ghost
d.shape("rectangle", "Foundation ghost", x=385, y=540, width=230,
        height=24, fill=NONE, stroke=GHOST, strokeWidth=2.5,
        opacity=55, dash=[6, 6])
d.text("foundation:", "Ghost key", x=392, y=556, size=9,
       font="Virelai Sans", color=GHOST, justify="left")
# where it landed — solid, red-hot wrong
d.shape("rectangle", "Foundation bad", x=455, y=540, width=160, height=24,
        fill=BAD_GRAD, stroke="#F0A08A", strokeWidth=3)
d.text("foundation:", "Bad key", x=462, y=556, size=9,
       font="Virelai Sans", color="#F8E0D0", justify="left")
# the parse squiggle underneath
d.path("M458,572 Q470,578 482,572 T506,572 T530,572 T554,572 T578,572 "
       "T602,572", "Parse squiggle", fill=NONE, stroke=ERR,
       strokeWidth=2.5, opacity=90, cap="round")
# trailing spaces, drifting off the end like curses
for i, (tx, ty, tr, to) in enumerate([(627, 552, 4, 70), (640, 546, 3.5, 50),
                                     (652, 540, 3, 32), (663, 532, 2.5, 18)]):
    d.shape("ellipse", f"Trail space {i+1}", x=tx - tr, y=ty - tr,
            width=tr * 2, height=tr * 2, fill=ERR, opacity=to,
            stroke=NONE)

# --- the wreckage, already burning -------------------------------------------------
# fallen window pane
d.path(rot_rect_path(662, 592, 44, 38, -22), "Fallen pane",
       fill="#B8D0D8", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(662, 592, 44, 5, -22), "Pane bar h", fill=INK,
       stroke=NONE)
d.path(rot_rect_path(662, 592, 5, 38, -22), "Pane bar v", fill=INK,
       stroke=NONE)
# broken studs
d.path(rot_rect_path(618, 622, 58, 12, 30), "Broken stud 1",
       fill=WOOD_GRAD, stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(560, 636, 46, 12, -14), "Broken stud 2",
       fill=WOOD_GRAD, stroke=INK, strokeWidth=2.5)
# firelight
d.shape("ellipse", "Fire glow", x=560, y=560, width=190, height=110,
        fill="#E8833A", opacity=18, stroke=NONE)
# flames licking the collapsed corner
def flame(cx, base, h, label):
    w = h * 0.42
    d.path(f"M{cx},{base} C{cx - w},{base - h * 0.35} "
           f"{cx - w * 0.5},{base - h * 0.75} {cx},{base - h} "
           f"C{cx + w * 0.5},{base - h * 0.75} {cx + w},{base - h * 0.35} "
           f"{cx},{base} Z", label, fill=FIRE_GRAD, stroke="#7E2810",
           strokeWidth=3)
flame(640, 640, 78, "Flame 1")
flame(690, 646, 56, "Flame 2")
flame(598, 632, 48, "Flame 3")
# inner licks
d.path("M640,640 C632,622 634,608 640,596 C646,608 648,622 640,640 Z",
       "Flame 1 core", fill="#F8DCA0", opacity=85, stroke=NONE)
# embers
for i, (ex, ey, er) in enumerate([(630, 545, 3.5), (662, 528, 3),
                                  (688, 555, 3.5), (645, 505, 2.5),
                                  (702, 515, 2.5)]):
    d.shape("ellipse", f"Ember {i+1}", x=ex - er, y=ey - er,
            width=er * 2, height=er * 2, fill="#F4B060", opacity=75,
            stroke=NONE)

# --- aphorism line + name + role ------------------------------------------------
r = d.text("ONE INDENT WRONG", "Key line 1", x=500, y=722,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("AND I BURN YOUR HOUSE DOWN.", "Key line 2", x=500, y=756,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("YAMMY MCPARSEFACE", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("ONE INDENT WRONG", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-050-yammy-mcparseface-V1R00")
