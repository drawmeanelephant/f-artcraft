#!/usr/bin/env python3
"""APH-031 Melody Errorflood — motivational-poster aphorism plate V1R00.
A NOTIFICATIONS ON poster: inside the gilt card, a speaker blasts sound
arcs that harden into a brick wall mid-flight; a single unlit chime bell
hangs muted beside the barrage; error triangles ride the air like eighth
notes. Plum club-poster night, hot magenta and amber. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-031 Melody Errorflood — Motivational Poster", 1000, 1000)

INK = "#140C18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241226"}, {"offset": 1, "color": "#0C0812"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E2E54"}, {"offset": 0.7, "color": "#2A1830"},
    {"offset": 1, "color": "#140C18"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241A28"}, {"offset": 1, "color": "#100C14"}]}}
SPK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A5462"}, {"offset": 1, "color": "#332E3A"}]}}
CONE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A8494"}, {"offset": 0.6, "color": "#4A4452"},
    {"offset": 1, "color": "#241F2C"}]}}
BRICK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#96443A"}, {"offset": 1, "color": "#5E2620"}]}}
BELL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6878"}, {"offset": 1, "color": "#413C48"}]}}
GOLD = "#C8A858"
FRAME = "#B8AC8A"
HEAD = "#F0E8DC"
PUNCH = "#DCC8C0"
CREAM = "#F0E8DC"
FAINT = "#9A8AA8"
WAVE = "#E85A9A"
WAVE_SOFT = "#B86A9A"
AMBER = "#E8A850"
ERR = "#E86A5A"
BELL = "#5E5866"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E4A7A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0B0D8", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#5C3A66", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#5C3A66", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7A5A88", opacity=35, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#3A2E42", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# headline
r = d.text("NOTIFICATIONS ON", "Headline", x=500, y=PY + 64,
           size=34, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=60)
d.path("M350,244 L472,244 M528,244 L650,244", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 244, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- the blast zone glow --------------------------------------------------------------
d.shape("ellipse", "Blast glow", x=340, y=330, width=330, height=180,
        fill=WAVE, opacity=9, stroke=NONE)

# --- the speaker, mid-blast --------------------------------------------------------------
SPK_X, SPK_Y, SPK_W, SPK_H = 292, 372, 62, 92
d.shape("ellipse", "Speaker shadow", x=SPK_X - 6, y=SPK_Y + SPK_H - 2,
        width=SPK_W + 12, height=11, fill="#000000", opacity=35,
        stroke=NONE)
d.shape("rectangle", "Speaker cab", x=SPK_X, y=SPK_Y, width=SPK_W,
        height=SPK_H, radius=5, fill=SPK_GRAD, stroke="#1C1822",
        strokeWidth=3)
# grille line
d.path(f"M{SPK_X + 7},{SPK_Y + 7} L{SPK_X + SPK_W - 7},{SPK_Y + 7}",
       "Cab sheen", fill=NONE, stroke="#7A7484", strokeWidth=2,
       opacity=55)
# two drivers: woofer below, tweeter above
d.shape("ellipse", "Woofer", x=SPK_X + 10, y=SPK_Y + 40,
        width=SPK_W - 20, height=SPK_W - 20, fill=CONE_GRAD,
        stroke="#1C1822", strokeWidth=2.5)
d.shape("ellipse", "Woofer dome", x=SPK_X + 26, y=SPK_Y + 56,
        width=10, height=10, fill="#8A8494", stroke=NONE)
d.shape("ellipse", "Tweeter", x=SPK_X + 19, y=SPK_Y + 14,
        width=SPK_W - 38, height=SPK_W - 38, fill=CONE_GRAD,
        stroke="#1C1822", strokeWidth=2)
d.shape("ellipse", "Tweeter dome", x=SPK_X + 27, y=SPK_Y + 22,
        width=8, height=8, fill="#8A8494", stroke=NONE)
# excursion lines: the cab is kicking
d.path(f"M{SPK_X - 10},{SPK_Y + 14} L{SPK_X - 20},{SPK_Y + 8} "
       f"M{SPK_X - 8},{SPK_Y + SPK_H - 14} L{SPK_X - 18},{SPK_Y + SPK_H - 8}",
       "Kick lines", fill=NONE, stroke=WAVE, strokeWidth=2.5,
       cap="round", opacity=60)

# --- sound arcs that square off into brick ------------------------------------------------
SRC_X, SRC_Y = SPK_X + SPK_W - 4, SPK_Y + 60    # wave source at the woofer
def arc(r, sweep_deg, label, color, wdt, op):
    a = math.radians(sweep_deg)
    x1 = SRC_X + r * math.cos(a); y1 = SRC_Y - r * math.sin(a)
    x2 = SRC_X + r * math.cos(a); y2 = SRC_Y + r * math.sin(a)
    mx = SRC_X + r
    d.path(f"M{x1:.0f},{y1:.0f} Q{mx + r * 0.42:.0f},{SRC_Y:.0f} "
           f"{x2:.0f},{y2:.0f}", label, fill=NONE, stroke=color,
           strokeWidth=wdt, cap="round", opacity=op)

arc(52, 38, "Wave 1", WAVE, 3, 80)
arc(88, 34, "Wave 2", WAVE, 4, 65)
arc(124, 30, "Wave 3", WAVE_SOFT, 5, 50)
# the last arc loses its curve and becomes mortar
arc(160, 24, "Wave 4", WAVE_SOFT, 6, 38)
for i, (yy, wdt) in enumerate([(336, 5), (390, 6), (444, 5)]):
    d.path(f"M{SRC_X + 168},{yy} L{SRC_X + 186},{yy}",
           f"Squaring {i+1}", fill=NONE, stroke=WAVE_SOFT,
           strokeWidth=wdt, cap="round", opacity=32)

# --- the wall the sound becomes ----------------------------------------------------------
WL_X, WL_Y, WL_W, WL_H = 612, 320, 108, 150
d.shape("ellipse", "Wall shadow", x=WL_X - 10, y=WL_Y + WL_H - 4,
        width=WL_W + 20, height=12, fill="#000000", opacity=35,
        stroke=NONE)
BW, BH, GAP = 32, 16, 4
for row in range(7):
    off = (BW / 2 + GAP / 2) if row % 2 else 0
    for col in range(4):
        bx = WL_X + off + col * (BW + GAP)
        if bx + BW > WL_X + WL_W:
            continue
        by = WL_Y + row * (BH + GAP)
        d.shape("rectangle", f"Brick {row}.{col}", x=bx, y=by,
                width=BW, height=BH, radius=1.5, fill=BRICK_GRAD,
                stroke="#2A100C", strokeWidth=1.5)
# impact: chips flying off the wall's struck face
for i, (cx, cy, w, h, deg) in enumerate([(600, 352, 12, 6, -30),
                                          (594, 402, 10, 5, 20),
                                          (604, 448, 11, 6, -42)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Chip {i+1}",
           fill="#8A4038", opacity=70, stroke=NONE)
# the wall's mortar still hums, faintly magenta
d.path(f"M{WL_X},{WL_Y + 40} L{WL_X},{WL_Y + 130}", "Hum edge",
       fill=NONE, stroke=WAVE, strokeWidth=2, opacity=35)

# --- the unlit chime bell, muted ------------------------------------------------------------
BCX, BTOPY = 505, 322
# hanging cord
d.path(f"M{BCX},288 L{BCX},{BTOPY}", "Bell cord", fill=NONE,
       stroke=FRAME, strokeWidth=2, opacity=60)
# dome + skirt + rim, all asleep
d.path(f"M{BCX - 20},{BTOPY + 38} "
       f"C{BCX - 22},{BTOPY + 10} {BCX - 10},{BTOPY} {BCX},{BTOPY} "
       f"C{BCX + 10},{BTOPY} {BCX + 22},{BTOPY + 10} {BCX + 20},{BTOPY + 38} "
       f"Z", "Bell body", fill=BELL_GRAD, stroke="#26222C",
       strokeWidth=2.5, opacity=80)
d.path(f"M{BCX - 26},{BTOPY + 38} Q{BCX},{BTOPY + 48} {BCX + 26},{BTOPY + 38}",
       "Bell rim", fill=NONE, stroke="#26222C", strokeWidth=3,
       opacity=80)
d.shape("ellipse", "Clapper", x=BCX - 5, y=BTOPY + 42, width=10,
        height=10, fill="#4A4452", stroke="#26222C", strokeWidth=2)
# where its sound rings would be: two faint dashed arcs, struck out
d.path(f"M{BCX - 40},{BTOPY + 10} Q{BCX - 52},{BTOPY + 24} {BCX - 40},{BTOPY + 38}",
       "Mute arc L", fill=NONE, stroke=BELL, strokeWidth=2,
       opacity=40, dash=[4, 5])
d.path(f"M{BCX + 40},{BTOPY + 10} Q{BCX + 52},{BTOPY + 24} {BCX + 40},{BTOPY + 38}",
       "Mute arc R", fill=NONE, stroke=BELL, strokeWidth=2,
       opacity=40, dash=[4, 5])
d.path(f"M{BCX - 56},{BTOPY + 44} L{BCX + 56},{BTOPY + 4}",
       "Mute slash", fill=NONE, stroke=ERR, strokeWidth=2.5,
       cap="round", opacity=65)

# --- error symbols floating like musical notes ----------------------------------------------
def err_note(cx, cy, s, deg, label, op):
    # eighth-note whose head is a warning triangle
    d.path(rot_rect_path(cx, cy - 16 * s, 3.5 * s, 34 * s, deg),
           f"{label} stem", fill=WAVE, opacity=op, stroke=NONE)
    # flag
    t = math.radians(deg)
    fx = cx + math.sin(t) * 16 * s + 2 * s
    fy = cy - 16 * s - math.cos(t) * 16 * s
    d.path(f"M{fx:.0f},{fy:.0f} q{10 * s},{2 * s} {9 * s},{12 * s}",
           f"{label} flag", fill=NONE, stroke=WAVE,
           strokeWidth=3 * s, cap="round", opacity=op)
    # triangle head
    tr = 10 * s
    pts = [(cx, cy - tr), (cx + tr * 0.95, cy + tr * 0.7),
           (cx - tr * 0.95, cy + tr * 0.7)]
    ds = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    d.path(ds, f"{label} head", fill=ERR, opacity=op, stroke="#7A2018",
           strokeWidth=1.5)
    d.text("!", f"{label} bang", x=cx, y=cy + tr * 0.45, size=9 * s,
           font="Source Sans 3", color="#FFE8E0", justify="center")

err_note(432, 322, 1.0, -8, "Note 1", 85)
err_note(560, 292, 0.85, 10, "Note 2", 75)
err_note(612, 296, 0.7, -14, "Note 3", 65)
err_note(392, 300, 0.75, 6, "Note 4", 60)

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("THE CHIME WAS BEAUTIFUL.", "Punchline 1", x=500,
           y=PY + PH - 58, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch1 tracking", ids=[r["id"]], tracking=90)
r = d.text("THE SYSTEM HAS STOPPED RESPONDING.", "Punchline 2", x=500,
           y=PY + PH - 32, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch2 tracking", ids=[r["id"]], tracking=70)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("MELODY ERRORFLOOD", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE CHIME WAS BEAUTIFUL", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-031-melody-errorflood-V1R00")
