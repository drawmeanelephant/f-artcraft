#!/usr/bin/env python3
"""Deferential Spark — mascot portrait V1R00.
The improvement that learned humility before it learned force: a small
spark, dimmer-set at twenty percent since intake, mid-bow at the threshold.
Behind it a five-notch capacity meter with only the first notch lit, and a
wall dimmer parked at the low end. It knocked twice and filed the wait.
1000x1000. Gradients + translucent shading, no flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Deferential Spark — Mascot Portrait", 1000, 1000)

INK = "#33241A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1310"}, {"offset": 1, "color": "#0A0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E3F2C"}, {"offset": 0.7, "color": "#322A1E"},
    {"offset": 1, "color": "#1B1610"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3226"}, {"offset": 1, "color": "#201A12"}]}}
SPARK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4DC9C"}, {"offset": 0.65, "color": "#E0AC54"},
    {"offset": 1, "color": "#B57E32"}]}}
GLOW_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4C95C", "opacity": 0.20},
    {"offset": 0.6, "color": "#F4C95C", "opacity": 0.07},
    {"offset": 1, "color": "#F4C95C", "opacity": 0}]}}
KNOB_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A8E98"}, {"offset": 1, "color": "#4C5058"}]}}
PLATE_METAL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E5346"}, {"offset": 1, "color": "#3A332A"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    assert math.hypot(x - PCX, y - PCY) <= PR - pad, (x, y)

def rrect(x, y, w, h, r):
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")

def tr(cx, cy, deg, px, py):
    """Rotate local point (px,py) about (cx,cy) by deg (clockwise, y down)."""
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return (cx + px * c - py * s, cy + px * s + py * c)

def ellipse_path(cx, cy, rx, ry, deg=0):
    k = 0.5522847498
    raw = [(rx, 0), (rx, k * ry), (k * rx, ry), (0, ry),
           (-k * rx, ry), (-rx, k * ry), (-rx, 0),
           (-rx, -k * ry), (-k * rx, -ry), (0, -ry),
           (k * rx, -ry), (rx, -k * ry), (rx, 0)]
    pts = [tr(cx, cy, deg, px, py) for px, py in raw]
    s = "M%.1f,%.1f" % pts[0]
    for i in range(1, len(pts), 3):
        s += " C" + " ".join("%.1f,%.1f" % p for p in pts[i:i + 3])
    return s + " Z"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#4E3F2C", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6648", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C49A", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(205,255,7),(795,245,8),(165,475,8),(838,485,7),
                               (270,768,6),(730,772,7),(140,365,6),(862,355,6),
                               (400,108,7),(605,103,8),(325,152,5),(688,148,6)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A5B40", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M131,660 L869,660 A420,420 0 0 1 131,660 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M131,660 L869,660", "Floor line", fill=NONE, stroke="#141009",
       strokeWidth=4, opacity=70)

# --- the dimmer on the wall, parked at the low end --------------------------------
d.path(rrect(700, 268, 96, 128, 10), "Dimmer plate", fill=PLATE_METAL,
       stroke="#20180F", strokeWidth=4)
# tick arc around the knob: dim end upper-left, bright end upper-right
KX, KY, KR = 748, 338, 34
for i in range(7):
    a = math.radians(-150 + i * 20)
    x0 = KX + 44 * math.cos(a); y0 = KY + 44 * math.sin(a)
    lit = (i == 0)
    d.path(rot_rect_path(round(x0), round(y0), 12, 5, -150 + i * 20),
           f"Dimmer tick {i+1}", fill="#E8C060" if lit else "#6E6152",
           opacity=90 if lit else 55, stroke=NONE)
d.path("M712,352 L704,352", "Dimmer minus", fill=NONE, stroke="#8A7A5E",
       strokeWidth=4, cap="round", opacity=80)
d.path("M792,352 L784,352 M788,348 L788,356", "Dimmer plus", fill=NONE,
       stroke="#8A7A5E", strokeWidth=4, cap="round", opacity=80)
d.shape("ellipse", "Dimmer knob", x=KX - KR, y=KY - KR, width=KR * 2,
        height=KR * 2, fill=KNOB_GRAD, stroke=INK, strokeWidth=4)
# pointer at twenty percent — the first tick and no further
pa = math.radians(-150)
d.path(f"M{KX + 8 * math.cos(pa):.1f},{KY + 8 * math.sin(pa):.1f} "
       f"L{KX + 26 * math.cos(pa):.1f},{KY + 26 * math.sin(pa):.1f}",
       "Knob pointer", fill=NONE, stroke="#2A2016", strokeWidth=5,
       cap="round")
d.shape("ellipse", "Knob sheen", x=KX - 22, y=KY - 26, width=20, height=12,
        fill="#FFFFFF", opacity=20, stroke=NONE)

# --- capacity meter: five notches, one lit ----------------------------------------
MCX, MCY, MR = 470, 590, 168
for i in range(5):
    a = -150 + i * 30
    x = MCX + MR * math.cos(math.radians(a))
    y = MCY + MR * math.sin(math.radians(a))
    lit = (i == 0)
    d.path(rot_rect_path(round(x), round(y), 26, 9, a),
           f"Capacity notch {i+1}", fill="#E8C060" if lit else "#6E6152",
           opacity=85 if lit else 40, stroke=NONE)
# a whisper of the full halo — implied, never logged
d.path(f"M{MCX - MR}, {MCY} A{MR},{MR} 0 0 1 {MCX + MR},{MCY}",
       "Capacity arc", fill=NONE, stroke="#E8C060", strokeWidth=2,
       opacity=15, cap="round")

# --- the spark's dim glow ------------------------------------------------------------
d.shape("ellipse", "Spark glow", x=300, y=400, width=340, height=340,
        fill=GLOW_GRAD, stroke=NONE)

# --- motion of the bow: two ghost arcs still settling --------------------------------
for i, (ox, oy, op) in enumerate([(-46, -34, 22), (-80, -18, 12)]):
    d.path(ellipse_path(470 + ox, 600 + oy, 66, 88, 25), f"Bow ghost {i+1}",
           fill=NONE, stroke="#E8C060", strokeWidth=3, opacity=op)

# --- the mascot, mid-bow ------------------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=360, y=676, width=240, height=20,
        fill="#120D08", opacity=50, stroke=NONE)
# the pool of light it is permitted to make
d.shape("ellipse", "Floor light pool", x=330, y=640, width=290, height=70,
        fill="#E8C060", opacity=10, stroke=NONE)
# body: warm droplet leaning twenty-five degrees into the bow
d.path(ellipse_path(470, 600, 74, 96, 25), "Body",
       fill=SPARK_GRAD, stroke=INK, strokeWidth=5)
# flame tuft, already inclined
tpx, tpy = tr(470, 600, 25, 34, -104)
d.path(ellipse_path(tpx, tpy, 13, 22, 60), "Tuft",
       fill=SPARK_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Tuft glint", x=round(tpx - 5), y=round(tpy - 12),
        width=7, height=9, fill="#FFF4D8", opacity=70, stroke=NONE)
# spark rays off the tip — present, but only just
for i, (dx, dy) in enumerate([(30, -18), (34, 6), (18, -30)]):
    d.path(f"M{tpx + dx * .7:.1f},{tpy + dy * .7:.1f} "
           f"L{tpx + dx * 1.35:.1f},{tpy + dy * 1.35:.1f}",
           f"Tuft ray {i+1}", fill=NONE, stroke="#E8C060",
           strokeWidth=3, cap="round", opacity=55)
# belly warmth
bx, by = tr(470, 600, 25, 0, 42)
d.shape("ellipse", "Belly", x=round(bx - 38), y=round(by - 32),
        width=76, height=62, fill="#F8E8BC", opacity=45, stroke=NONE)
# the bowing arm, swept low and out
a0 = tr(470, 600, 25, 34, 16); a1 = tr(470, 600, 25, 96, 66)
am = tr(470, 600, 25, 62, 58)
d.path(f"M{a0[0]:.1f},{a0[1]:.1f} Q{am[0]:.1f},{am[1]:.1f} {a1[0]:.1f},{a1[1]:.1f}",
       "Bow arm", fill=NONE, stroke="#D8A458", strokeWidth=16, cap="round")
d.shape("ellipse", "Bow paw", x=round(a1[0] - 12), y=round(a1[1] - 10),
        width=26, height=22, fill="#F4DC9C", stroke=INK, strokeWidth=3.5)
# the other tucked politely behind
b0 = tr(470, 600, 25, -38, 10); b1 = tr(470, 600, 25, -52, 34)
d.path(f"M{b0[0]:.1f},{b0[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f}",
       "Tucked arm", fill=NONE, stroke="#B57E32", strokeWidth=14,
       cap="round")
# feet, planted for the duration of the apology
f1 = tr(470, 600, 25, -26, 92); f2 = tr(470, 600, 25, 30, 92)
for i, f in enumerate([f1, f2]):
    d.shape("ellipse", f"Foot {i+1}", x=round(f[0] - 18), y=round(f[1] - 9),
            width=38, height=20, fill="#B57E32", stroke=INK,
            strokeWidth=3.5)
# eyes closed in apology — soft downward arcs
for i, ex in enumerate([-28, 22]):
    e0 = tr(470, 600, 25, ex - 10, -14)
    e1 = tr(470, 600, 25, ex, -8)
    e2 = tr(470, 600, 25, ex + 10, -14)
    d.path(f"M{e0[0]:.1f},{e0[1]:.1f} Q{e1[0]:.1f},{e1[1]:.1f} {e2[0]:.1f},{e2[1]:.1f}",
           f"Eye {i+1}", fill=NONE, stroke=INK, strokeWidth=5,
           cap="round")
# the small careful mouth
m0 = tr(470, 600, 25, -8, 10); m1 = tr(470, 600, 25, 0, 16)
m2 = tr(470, 600, 25, 8, 10)
d.path(f"M{m0[0]:.1f},{m0[1]:.1f} Q{m1[0]:.1f},{m1[1]:.1f} {m2[0]:.1f},{m2[1]:.1f}",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# blush, faint — the apology is older than the change
for i, cx0 in enumerate([-44, 40]):
    p = tr(470, 600, 25, cx0, 4)
    d.shape("ellipse", f"Blush {i+1}", x=round(p[0] - 12),
            y=round(p[1] - 7), width=24, height=14, fill="#E88A5C",
            opacity=30, stroke=NONE)

# --- shed sparks, falling as quietly as it arrived ------------------------------------
for i, (x, y, s, op) in enumerate([(352, 486, 8, 45), (326, 540, 6, 35),
                                   (370, 432, 5, 55), (612, 500, 6, 30)]):
    on_disc(x, y, 8)
    d.path(f"M{x},{y - s} L{x + s * .6},{y} L{x},{y + s} L{x - s * .6},{y} Z",
           f"Shed spark {i+1}", fill="#E8C060", opacity=op, stroke=NONE)

# --- motes ----------------------------------------------------------------------------
for i, (x, y, w) in enumerate([(250, 340, 5), (830, 560, 5), (200, 600, 4),
                               (650, 250, 4), (310, 230, 4)]):
    on_disc(x + w / 2, y + w / 2, 8)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C49A", opacity=35, stroke=NONE)

# --- captions --------------------------------------------------------------------------
d.text("DEFERENTIAL SPARK", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#F4E4BC", justify="center")
r = d.text("BOWING AT TWENTY PERCENT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C9AE80", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("288.deferential-spark-V1R00")
