#!/usr/bin/env python3
"""APH-027 Comrade Kernelov — motivational-poster aphorism plate V1R00.
A Soviet worker-poster plate for the server farm: inside the gilt black
card, a gold sunburst rises behind a collective of identical red server
blades standing like workers, fists raised — while one pale blade, tagged
DEVIANT, is gently lifted out of the ranks. Hammer-and-circuit badge
under the headline. Red-gold, warm ink, never pure black. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-027 Comrade Kernelov — Motivational Poster", 1000, 1000)

INK = "#160C08"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A100A"}, {"offset": 1, "color": "#100604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A2416"}, {"offset": 0.7, "color": "#33150C"},
    {"offset": 1, "color": "#180A06"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E110A"}, {"offset": 1, "color": "#150806"}]}}
SUN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0BE6A"}, {"offset": 0.55, "color": "#D8913E"},
    {"offset": 1, "color": "#8A4A1E"}]}}
BLADE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C04A32"}, {"offset": 1, "color": "#7A2014"}]}}
DEV_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A9484"}, {"offset": 1, "color": "#5E584C"}]}}
TAG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D4AE"}, {"offset": 1, "color": "#BFA678"}]}}
GOLD = "#D8A848"
FRAME = "#C8B380"
HEAD = "#F0E2C0"
PUNCH = "#E0C898"
CREAM = "#F0E2C0"
FAINT = "#B08058"
LED = "#F0C060"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A4A28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0BE8A", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#7A3A20", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#7A3A20", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A5C30", opacity=35, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#3A1C10", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# headline
r = d.text("PROCESS EQUALITY", "Headline", x=500, y=PY + 64,
           size=34, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=55)

# --- hammer-and-circuit badge under the headline -----------------------------------
d.shape("ellipse", "Badge", x=464, y=238, width=72, height=72,
        fill=NONE, stroke=GOLD, strokeWidth=2.5, opacity=85)
d.shape("ellipse", "Badge inner", x=470, y=244, width=60, height=60,
        fill=NONE, stroke=GOLD, strokeWidth=1, opacity=45)
# hammer: handle + head, swung to 45 degrees
d.path(rot_rect_path(500, 274, 7, 34, 45), "Hammer handle",
       fill=GOLD, opacity=90, stroke=NONE)
d.path(rot_rect_path(489, 263, 22, 9, 45), "Hammer head",
       fill=GOLD, opacity=90, stroke=NONE)
# circuit trace crossing it the other way: angled line with node dots
d.path("M512,252 L512,266 L498,280 L498,294", "Circuit trace",
       fill=NONE, stroke="#E8C878", strokeWidth=2.5, cap="round",
       opacity=85)
for i, (nx, ny) in enumerate([(512, 252), (498, 294)]):
    d.shape("ellipse", f"Circuit node {i+1}", x=nx - 3, y=ny - 3,
            width=6, height=6, fill="#E8C878", opacity=85, stroke=NONE)

# --- the sunburst: wedges fanned up from behind the collective -----------------------
RAY_C = "#E8A850"
APEX_X, APEX_Y, RAY_R = 500, 508, 175
for i in range(9):
    ang = -160 + i * 17.5
    a1 = math.radians(ang - 3.2)
    a2 = math.radians(ang + 3.2)
    x1 = APEX_X + RAY_R * math.cos(a1)
    y1 = APEX_Y + RAY_R * math.sin(a1)
    x2 = APEX_X + RAY_R * math.cos(a2)
    y2 = APEX_Y + RAY_R * math.sin(a2)
    d.path(f"M{APEX_X},{APEX_Y} L{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} Z",
           f"Ray {i+1}", fill=RAY_C, opacity=18 if i % 2 else 26,
           stroke=NONE)
# the sun itself, half-sunk behind the collective's ground line
d.shape("ellipse", "Sun glow", x=385, y=315, width=230, height=230,
        fill=RAY_C, opacity=18, stroke=NONE)
d.shape("ellipse", "Sun", x=415, y=345, width=170, height=170,
        fill=SUN_GRAD, stroke="#B87A34", strokeWidth=3)

# --- the collective: identical blades, fists raised ----------------------------------
GROUND = 508
# ground strip the workers stand on
d.shape("rectangle", "Ground", x=PX + 24, y=GROUND, width=PW - 48,
        height=14, fill="#3A140C", stroke=NONE)
d.path(f"M{PX + 24},{GROUND} L{PX + PW - 24},{GROUND}", "Ground edge",
       fill=NONE, stroke=GOLD, strokeWidth=2, opacity=55)

BW, BH = 46, 118
CENTERS = [345, 407, 469, 531, 593]          # the five good blades
for i, cx in enumerate(CENTERS):
    bx, by = cx - BW / 2, GROUND - BH
    # blade shadow
    d.shape("ellipse", f"Shadow {i+1}", x=cx - 26, y=GROUND - 4,
            width=52, height=10, fill="#000000", opacity=30, stroke=NONE)
    # body
    d.shape("rectangle", f"Worker {i+1}", x=bx, y=by, width=BW,
            height=BH, radius=4, fill=BLADE_GRAD, stroke="#4A1008",
            strokeWidth=2.5)
    # top sheen
    d.path(f"M{bx + 6},{by + 6} L{bx + BW - 6},{by + 6}",
           f"Sheen {i+1}", fill=NONE, stroke="#E08058",
           strokeWidth=2, opacity=60)
    # LED eyes, all glowing the same gold — identical, as required
    for k in (-1, 1):
        d.shape("ellipse", f"Eye {i+1}.{k}", x=cx + k * 9 - 3,
                y=by + 15, width=6, height=6, fill=LED, stroke=NONE)
    d.shape("ellipse", f"Eyehalo {i+1}", x=cx - 14, y=by + 11,
            width=28, height=14, fill=LED, opacity=18, stroke=NONE)
    # vent ticks low on the body
    for k in range(3):
        tx = cx - 12 + k * 12
        d.path(f"M{tx},{by + BH - 22} L{tx},{by + BH - 12}",
               f"Vent {i+1}.{k}", fill=NONE, stroke="#4A1008",
               strokeWidth=2)
    # raised arm + fist; alternate sides so the line of arms marches
    side = -1 if i % 2 else 1
    ax, ay = cx + side * (BW / 2 - 4), by + 8
    fx, fy = cx + side * 20, by - 30
    d.path(f"M{ax},{ay} L{fx},{fy}", f"Arm {i+1}", fill=NONE,
           stroke="#7A2014", strokeWidth=7, cap="round")
    d.path(rot_rect_path(fx, fy - 6, 13, 13, 12 * side), f"Fist {i+1}",
           fill=GOLD, stroke="#4A1008", strokeWidth=1.5)

# --- the bourgeois deviation: pale, tilted, lifted out of line ------------------------
DCX, DCY, DTILT = 660, GROUND - BH / 2 - 12, 14
d.shape("ellipse", "Deviant shadow", x=DCX - 24, y=GROUND - 4,
        width=48, height=9, fill="#000000", opacity=20, stroke=NONE)
d.path(rot_rect_path(DCX, DCY, BW, BH, DTILT), "Deviant blade",
       fill=DEV_GRAD, stroke="#3E382E", strokeWidth=2.5)
# its dim eyes — no halo, no glow
for k in (-1, 1):
    ex = DCX + k * 9 - DTILT * 0.4
    ey = DCY - BH / 2 + 15 + k * DTILT * 0.16
    d.shape("ellipse", f"Deviant eye {k}", x=ex - 3, y=ey - 3,
            width=6, height=6, fill="#6A6A60", stroke=NONE)
# its arm hangs slack down the side instead of rising
d.path(rot_rect_path(DCX + 26, DCY + 18, 7, 34, DTILT + 24),
       "Deviant arm", fill="#6E6250", stroke="#3E382E",
       strokeWidth=1.5)
# faint extraction arc behind it — the path it is being lifted along
d.path("M620,438 C644,420 662,398 668,368", "Extraction arc",
       fill=NONE, stroke=GOLD, strokeWidth=2, cap="round", opacity=45)
d.path("M664,376 L670,362 L676,374", "Extraction arrow", fill=NONE,
       stroke=GOLD, strokeWidth=2, cap="round", opacity=45)
# the tag hanging off its top corner
d.path("M682,398 L692,418", "Tag string", fill=NONE, stroke=FRAME,
       strokeWidth=1.5, opacity=80)
d.path(rot_rect_path(700, 432, 58, 18, 8), "Deviant tag", fill=TAG_GRAD,
       stroke="#6E5A38", strokeWidth=1.5)
d.shape("ellipse", "Tag eyelet", x=688, y=412, width=6, height=6,
        fill=NONE, stroke="#6E5A38", strokeWidth=1.5)
d.text("DEVIANT", "Tag text", x=700, y=436, size=9,
       font="Source Sans 3", color="#4A3A22", justify="center")

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("CPU CYCLES REDISTRIBUTED", "Punchline 1", x=500,
           y=PY + PH - 58, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch1 tracking", ids=[r["id"]], tracking=95)
r = d.text("ACROSS THE COLLECTIVE.", "Punchline 2", x=500,
           y=PY + PH - 32, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch2 tracking", ids=[r["id"]], tracking=95)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("COMRADE KERNELOV", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("PROCESS EQUALITY LOGGED", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-027-comrade-kernelov-V1R00")
