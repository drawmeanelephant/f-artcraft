#!/usr/bin/env python3
"""Greenband Gregor — mascot portrait V1R00.
The ghost of the shifting baseline, unhurried, repainting a dashboard
gauge's tolerance band green in one continuous stroke. Under the wet
band, two earlier greens show through like a former shoreline; at the
right edge a sliver of red is still drying. He brings his own brush.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Greenband Gregor — Mascot Portrait", 1000, 1000)

INK = "#262433"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16241F"}, {"offset": 1, "color": "#080E0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E6E62"}, {"offset": 0.7, "color": "#2E4640"},
    {"offset": 1, "color": "#15201E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A4438"}, {"offset": 1, "color": "#101C18"}]}}
PANEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3448"}, {"offset": 1, "color": "#161C2C"}]}}
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2EDDC"}, {"offset": 0.75, "color": "#DCD2B6"},
    {"offset": 1, "color": "#B4A888"}]}}
GHOST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAF6F0"}, {"offset": 0.7, "color": "#B8DCD4"},
    {"offset": 1, "color": "#82B4B0"}]}}
GHOST_EDGE = "#3E5A58"
GREEN = "#4ED98E"
GREEN_DEEP = "#2C9E62"
RED = "#D4685E"
CAN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A6478"}, {"offset": 1, "color": "#323A4C"}]}}

# gauge geometry -------------------------------------------------------------
GCX, GCY, GR = 368, 486, 122          # dial center + zone-ring radius

def gp(deg, r=GR):
    t = math.radians(deg)
    return GCX + r * math.cos(t), GCY - r * math.sin(t)

def arc(a1, a2, r=GR):
    """arc from angle a1 down to a2 through the top (y-down coords)."""
    p1 = gp(a1, r); p2 = gp(a2, r)
    return f"M{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 0 1 {p2[0]:.1f},{p2[1]:.1f}"

def tick(deg, r1, r2):
    p1 = gp(deg, r1); p2 = gp(deg, r2)
    return f"M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A968A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E4D8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(196,240,8),(798,236,7),(162,524,9),(832,548,8),
                               (250,762,7),(750,746,9),(136,394,6),(862,396,7),
                               (396,114,7),(610,112,8),(336,820,6),(664,816,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A5A50", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#08100C",
       strokeWidth=4, opacity=70)

# --- the dashboard panel ---------------------------------------------------------
d.shape("ellipse", "Panel shadow", x=180, y=692, width=380, height=30,
        fill="#060A08", opacity=50, stroke=NONE)
d.shape("rectangle", "Panel foot L", x=222, y=700, width=54, height=26,
        fill="#1A2130", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Panel foot R", x=458, y=700, width=54, height=26,
        fill="#1A2130", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Panel", x=186, y=252, width=364, height=458,
        fill=PANEL, stroke="#4A5878", strokeWidth=6, radius=20)
d.path("M186,302 L550,302", "Panel titlebar", fill=NONE, stroke="#4A5878",
       strokeWidth=4)
for i, c in enumerate(("#E0705E", "#E8C05E", "#6AC88A")):
    d.shape("ellipse", f"Panel dot {i+1}", x=206 + i * 26, y=270, width=14, height=14,
            fill=c, stroke=NONE, opacity=85)
# dim status rows nobody scrolls to
for i, (y, w) in enumerate([(668, 130), (684, 96), (668, 0)]):
    if w:
        d.shape("rectangle", f"Panel row {i+1}", x=210, y=y, width=w, height=9,
                fill="#3A4A66", stroke=NONE, radius=4, opacity=80)
# a small LED already repainted, with the drip to prove it
d.shape("ellipse", "LED", x=508, y=664, width=16, height=16,
        fill=GREEN, stroke=INK, strokeWidth=3)
d.path("M514,682 C512,690 512,694 516,697 C520,694 519,688 517,682 Z",
       "LED drip", fill=GREEN, stroke=NONE, opacity=80)

# --- the gauge ---------------------------------------------------------------------
d.shape("ellipse", "Gauge rim", x=200, y=318, width=336, height=336,
        fill="#39415C", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Gauge face", x=216, y=334, width=304, height=304,
        fill=FACE, stroke=INK, strokeWidth=3)
# ticks, drawn first so the wet paint can swallow them
for i, a in enumerate((165, 140, 115, 90, 65, 40, 15)):
    d.path(tick(a, 136, 152), f"Tick {i+1}", fill=NONE, stroke="#8A8068",
           strokeWidth=4, cap="round")
# earlier bands, two repaints down, faint as a former shoreline
d.path(arc(96, 24, 138), "Old band 2", fill=NONE, stroke=GREEN_DEEP,
       strokeWidth=9, cap="round", opacity=16)
d.path(arc(88, 30, 146), "Old band 3", fill=NONE, stroke=GREEN_DEEP,
       strokeWidth=8, cap="round", opacity=10)
# the old green, muted — pre-Gregor tolerance
d.path(arc(170, 104), "Old band", fill=NONE, stroke="#7FAE8E",
       strokeWidth=30, cap="round", opacity=55)
# the red zone, mid-consumption: only a sliver remains
d.path(arc(26, 4), "Red remnant", fill=NONE, stroke=RED,
       strokeWidth=30, cap="round", opacity=90)
# Gregor's fresh stroke: wider than the marks ever were
d.path(arc(104, 16), "Fresh band", fill=NONE, stroke=GREEN,
       strokeWidth=30, cap="round", opacity=95)
d.path(arc(104, 16, 106), "Fresh band glint", fill=NONE, stroke="#EAFBF2",
       strokeWidth=5, cap="round", opacity=55)
d.shape("ellipse", "Band glow", x=378, y=338, width=170, height=120,
        fill=GREEN, opacity=14, stroke=NONE)
# the old boundary tick, ghosting through the paint
d.path(tick(48, 104, 140), "Old boundary", fill=NONE, stroke="#4A4238",
       strokeWidth=5, cap="round", opacity=45)
# wet drips off the new edge
d.path("M496,392 C492,402 491,410 496,414 C501,410 500,400 497,392 Z",
       "Band drip 1", fill=GREEN, stroke=NONE, opacity=85)
d.path("M462,376 C459,383 459,388 463,391 C467,388 466,381 464,376 Z",
       "Band drip 2", fill=GREEN, stroke=NONE, opacity=70)
# needle, unmoved — Gregor doesn't fix needles
tip = gp(30, 88)
d.path(f"M{GCX},{GCY} L{tip[0]:.1f},{tip[1]:.1f}", "Needle", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.shape("ellipse", "Needle hub", x=GCX - 13, y=GCY - 13, width=26, height=26,
        fill="#5A6478", stroke=INK, strokeWidth=4)
# glass glare
d.path("M268,392 C300,352 356,336 402,352", "Glass glare", fill=NONE,
       stroke="#FFFFFF", strokeWidth=10, cap="round", opacity=22)

# --- Gregor: the ghost of the baseline ---------------------------------------------
d.shape("ellipse", "Ghost shadow", x=560, y=700, width=280, height=32,
        fill="#060A08", opacity=45, stroke=NONE)
d.shape("ellipse", "Ghost glow", x=560, y=240, width=360, height=460,
        fill=GREEN, opacity=7, stroke=NONE)
# body: dome, soft sides, scalloped hem — generated, not typed
hem = ""
x_right, x_left, y_hem, dip = 824, 652, 652, 30
lobes = 6
step = (x_right - x_left) / lobes
x = x_right
for _ in range(lobes):
    hem += f" Q{x - step/2:.1f},{y_hem + dip} {x - step:.1f},{y_hem}"
    x -= step
d.path(f"M652,652 L652,412 C652,330 684,272 738,272 "
       f"C792,272 824,330 824,412 L824,652{hem} Z",
       "Gregor body", fill=GHOST, stroke=GHOST_EDGE, strokeWidth=5,
       opacity=93, join="round")
# a paler inner sheet — translucency, not flat
d.path("M684,610 L684,420 C684,352 706,312 738,312 C770,312 792,352 792,420 "
       "L792,610 C772,592 758,624 738,610 C718,596 704,624 684,610 Z",
       "Gregor inner", fill="#EAF6F0", opacity=35, stroke=NONE)
# face: the only unhurried presence in the building
d.shape("ellipse", "Gregor eye L", x=704, y=368, width=22, height=34,
        fill="#233044", stroke=NONE)
d.shape("ellipse", "Gregor eye R", x=754, y=368, width=22, height=34,
        fill="#233044", stroke=NONE)
d.shape("ellipse", "Gregor eye L gleam", x=709, y=374, width=8, height=10,
        fill="#BFE8DC", stroke=NONE, opacity=80)
d.shape("ellipse", "Gregor eye R gleam", x=759, y=374, width=8, height=10,
        fill="#BFE8DC", stroke=NONE, opacity=80)
d.path("M726,430 C734,437 748,437 756,430", "Gregor mouth", fill=NONE,
       stroke="#233044", strokeWidth=5, cap="round")
# brush arm reaching left to the wet edge of the band
bx, by = gp(14, GR + 8)   # brush tip on the band's wet end
d.path(f"M674,470 C620,452 570,440 {bx + 26:.0f},{by + 14:.0f}",
       "Brush arm", fill=NONE, stroke="#A8CCC6", strokeWidth=24,
       cap="round")
d.shape("ellipse", "Brush hand", x=bx + 8, y=by - 2, width=34, height=28,
        fill="#B8DCD4", stroke=GHOST_EDGE, strokeWidth=4)
# the brush: stubby handle, bristles loaded
d.path(f"M{bx + 22:.0f},{by + 10:.0f} L{bx + 4:.0f},{by - 26:.0f}",
       "Brush handle", fill=NONE, stroke="#8A5A38", strokeWidth=9,
       cap="round")
d.path(f"M{bx + 4:.0f},{by - 26:.0f} L{bx - 8:.0f},{by - 44:.0f} "
       f"L{bx - 14:.0f},{by - 24:.0f} Z", "Brush bristles",
       fill=GREEN, stroke=INK, strokeWidth=3, join="round")
# other hand: the can he brought himself
d.path("M800,520 C824,540 830,566 824,588", "Can arm", fill=NONE,
       stroke="#A8CCC6", strokeWidth=22, cap="round")
d.shape("ellipse", "Can hand", x=806, y=576, width=32, height=26,
        fill="#B8DCD4", stroke=GHOST_EDGE, strokeWidth=4)
d.shape("rectangle", "Paint can", x=792, y=596, width=64, height=66,
        fill=CAN, stroke=INK, strokeWidth=4, radius=8)
d.shape("ellipse", "Can paint", x=798, y=590, width=52, height=16,
        fill=GREEN, stroke=INK, strokeWidth=3)
d.path("M800,600 C806,612 806,624 800,632", "Can drip", fill=NONE,
       stroke=GREEN, strokeWidth=6, cap="round", opacity=85)
d.path("M792,600 C786,576 788,566 800,556", "Can handle", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# faint green shimmer where the hem passes the floor light
d.shape("ellipse", "Hem shimmer", x=640, y=636, width=200, height=26,
        fill=GREEN, opacity=12, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("GREENBAND GREGOR", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#DFF2E8", justify="center")
r = d.text("GHOST OF THE SHIFTING BASELINE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9EC4B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("232.greenband-gregor-V1R00")
