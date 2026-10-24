#!/usr/bin/env python3
"""Boily McPlaterton — mascot portrait V1R00.
A rounded boiler-bot with a cracked casing venting steam, chest fan
spinning flat out, amber advisory beacon lit on his crown. One stub arm
mops his brow; a wall thermometer on the right already reads 93C.
Worried but holding together — mostly.
1000x1000. House style: gradients + translucent shading, never flat fills.
Digits are set in Source Sans 3 (Virelai carries no figures).
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Boily McPlaterton — Mascot Portrait", 1000, 1000)

INK = "#1C1A20"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#11161D"}, {"offset": 1, "color": "#06090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4A52"}, {"offset": 0.7, "color": "#232D34"},
    {"offset": 1, "color": "#10161B"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2B353C"}, {"offset": 1, "color": "#10161B"}]}}
CASE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D4D9E0"}, {"offset": 0.65, "color": "#9AA1AE"},
    {"offset": 1, "color": "#5F6875"}]}}
FAN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#39424C"}, {"offset": 1, "color": "#171C22"}]}}
AMBER_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFCE6E"}, {"offset": 0.6, "color": "#F0963C"},
    {"offset": 1, "color": "#C05E1E"}]}}
GAUGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE4CC"}, {"offset": 1, "color": "#C6B888"}]}}
HOT = "#E2703A"
STEEL = "#9AA1AE"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A6E7A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8C0CC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193, 233, 8), (801, 230, 7), (157, 524, 9),
                               (837, 544, 8), (247, 766, 7), (753, 749, 9),
                               (133, 393, 6), (864, 391, 7), (391, 113, 7),
                               (613, 110, 8), (333, 823, 6), (665, 821, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#46545C", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0F13",
       strokeWidth=4, opacity=70)

# --- wall thermometer, already in the red ----------------------------------------
tx, ty, tw, th = 706, 240, 66, 240
d.path(rot_rect_path(tx + tw / 2 + 4, ty + th / 2 + 5, tw, th, 0),
       "Gauge shadow", fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Gauge body", x=tx, y=ty, width=tw, height=th,
        radius=12, fill=GAUGE_GRAD, stroke=INK, strokeWidth=5)
# tick rail + mercury column, red past the line
d.shape("rectangle", "Gauge tube", x=tx + 26, y=ty + 22, width=14,
        height=180, radius=7, fill="#F4ECD8", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Mercury", x=tx + 28, y=ty + 44, width=10,
        height=156, radius=5, fill="#C0392B", stroke=NONE)
d.shape("ellipse", "Mercury bulb", x=tx + 20, y=ty + 188, width=26,
        height=26, fill="#C0392B", stroke=INK, strokeWidth=3)
for i, gy in enumerate([ty + 40, ty + 74, ty + 108, ty + 142, ty + 176]):
    d.path(f"M{tx + 44},{gy} L{tx + 54},{gy}", f"Gauge tick {i+1}",
           fill=NONE, stroke=INK, strokeWidth=2.5, opacity=70)
# 93C label under the gauge — digits in Source Sans 3
d.text("93\u00B0C", "Gauge reading", x=tx + tw / 2, y=ty + th + 30, size=20,
       font="Source Sans 3", color=HOT, justify="center")
# red-zone marker at the top tick
d.path(f"M{tx + 44},{ty + 40} L{tx + 60},{ty + 40}", "Red zone", fill=NONE,
       stroke="#C0392B", strokeWidth=4)

# --- Boily: the boiler-bot ---------------------------------------------------------
bx, by, bw, bh = 318, 268, 250, 410
# feet
for lbl, fx in [("Foot L", 346), ("Foot R", 492)]:
    d.shape("ellipse", lbl, x=fx, y=668, width=74, height=34,
            fill="#6E7684", stroke=INK, strokeWidth=4)
# body casing: rounded slab, slightly wider at the hips
d.path(f"M{bx + 8},{by + 40} C{bx + 8},{by + 12} {bx + 40},{by} {bx + 76},{by} "
       f"L{bx + bw - 76},{by} C{bx + bw - 40},{by} {bx + bw - 8},{by + 12} "
       f"{bx + bw - 8},{by + 40} L{bx + bw},{by + bh - 60} "
       f"C{bx + bw},{by + bh - 16} {bx + bw - 36},{by + bh} {bx + bw - 72},{by + bh} "
       f"L{bx + 72},{by + bh} C{bx + 36},{by + bh} {bx},{by + bh - 16} "
       f"{bx},{by + bh - 60} Z",
       "Casing", fill=CASE_GRAD, stroke=INK, strokeWidth=6)
# casing shading: right side falls off, top sheen
d.path(f"M{bx + bw - 60},{by + 20} C{bx + bw - 20},{by + 30} {bx + bw - 14},{by + 60} "
       f"{bx + bw - 12},{by + 120} L{bx + bw - 12},{by + bh - 90} "
       f"C{bx + bw - 50},{by + bh - 40} {bx + bw - 40},{by + 160} {bx + bw - 60},{by + 20} Z",
       "Side shade", fill="#4A525E", opacity=30, stroke=NONE)
d.shape("ellipse", "Top sheen", x=bx + 42, y=by + 16, width=150, height=36,
        fill="#FFFFFF", opacity=18, stroke=NONE)
# corner bolts
for i, (cx2, cy2) in enumerate([(bx + 26, by + 30), (bx + bw - 26, by + 30),
                                (bx + 26, by + bh - 26), (bx + bw - 26, by + bh - 26)]):
    d.shape("ellipse", f"Bolt {i+1}", x=cx2 - 6, y=cy2 - 6, width=12, height=12,
            fill="#6E7684", stroke=INK, strokeWidth=2.5)
    d.path(f"M{cx2 - 3},{cy2} L{cx2 + 3},{cy2}", f"Bolt slot {i+1}",
           fill=NONE, stroke=INK, strokeWidth=2)

# the crack: a zigzag splitting the upper-left casing
d.path(f"M{bx + 30},{by + 44} L{bx + 62},{by + 78} L{bx + 46},{by + 112} "
       f"L{bx + 84},{by + 150} L{bx + 64},{by + 188}", "Crack", fill=NONE,
       stroke="#14100F", strokeWidth=6, cap="round", join="round")
d.path(f"M{bx + 34},{by + 44} L{bx + 66},{by + 78} L{bx + 50},{by + 112} "
       f"L{bx + 88},{by + 150} L{bx + 68},{by + 188}", "Crack lip", fill=NONE,
       stroke="#E8EDF2", strokeWidth=2, opacity=50, cap="round", join="round")

# steam venting out of the crack: two lazy S-curls
def steam(x0, y0, drift, label, op):
    d.path(f"M{x0},{y0} C{x0 - 18},{y0 - 34} {x0 + drift},{y0 - 56} "
           f"{x0 + drift - 10},{y0 - 88} C{x0 + drift - 24},{y0 - 110} "
           f"{x0 + drift + 16},{y0 - 128} {x0 + drift + 8},{y0 - 152}",
           f"{label} steam", fill=NONE, stroke="#F2F6F8",
           strokeWidth=14, opacity=op, cap="round")
    d.path(f"M{x0 + 2},{y0} C{x0 - 14},{y0 - 32} {x0 + drift + 2},{y0 - 54} "
           f"{x0 + drift - 6},{y0 - 84} C{x0 + drift - 18},{y0 - 104} "
           f"{x0 + drift + 18},{y0 - 122} {x0 + drift + 10},{y0 - 144}",
           f"{label} steam core", fill=NONE, stroke="#FFFFFF",
           strokeWidth=6, opacity=min(100, op + 18), cap="round")

steam(bx + 56, by + 112, -30, "Crack steam 1", 34)
steam(bx + 78, by + 172, -46, "Crack steam 2", 26)

# --- crown beacon: the advisory warning ------------------------------------------
bcx, bcy = bx + bw / 2, by - 26
d.shape("ellipse", "Beacon glow", x=bcx - 64, y=bcy - 74, width=128,
        height=110, fill="#F0963C", opacity=14, stroke=NONE)
d.shape("rectangle", "Beacon base", x=bcx - 30, y=bcy + 8, width=60,
        height=16, radius=6, fill="#4A4238", stroke=INK, strokeWidth=4)
d.path(f"M{bcx - 26},{bcy + 10} C{bcx - 26},{bcy - 22} {bcx - 14},{bcy - 34} "
       f"{bcx},{bcy - 34} C{bcx + 14},{bcy - 34} {bcx + 26},{bcy - 22} "
       f"{bcx + 26},{bcy + 10} Z",
       "Beacon dome", fill=AMBER_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Beacon hot spot", x=bcx - 10, y=bcy - 28, width=14,
        height=12, fill="#FFE9BC", opacity=80, stroke=NONE)
# radiating ticks
for i, (dx, dy, ln) in enumerate([(-52, -46, 16), (0, -64, 18), (52, -46, 16)]):
    a = math.atan2(dy, dx)
    d.path(f"M{bcx + dx},{bcy + dy} L{bcx + dx + math.cos(a) * ln:.0f},{bcy + dy + math.sin(a) * ln:.0f}",
           f"Beacon ray {i+1}", fill=NONE, stroke="#F0A050", strokeWidth=5,
           opacity=70, cap="round")

# --- the face: worried, overheated ------------------------------------------------
for i, cx in enumerate([bx + 78, bx + 166]):
    d.shape("ellipse", f"Eye {i+1}", x=cx - 15, y=by + 108, width=30,
            height=34, fill="#16121A", stroke=NONE)
    d.shape("ellipse", f"Glint {i+1}", x=cx - 7, y=by + 114, width=8,
            height=8, fill="#FFFFFF", opacity=85, stroke=NONE)
# brows pinch inward — thermal anxiety
d.path(f"M{bx + 58},{by + 92} C{bx + 72},{by + 82} {bx + 88},{by + 82} {bx + 98},{by + 90}",
       "Brow L", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path(f"M{bx + 148},{by + 90} C{bx + 158},{by + 82} {bx + 174},{by + 82} {bx + 188},{by + 92}",
       "Brow R", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# a little wavy anxious mouth
d.path(f"M{bx + 92},{by + 168} C{bx + 102},{by + 160} {bx + 110},{by + 176} {bx + 122},{by + 168} "
       f"C{bx + 134},{by + 160} {bx + 142},{by + 176} {bx + 154},{by + 168}",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# flushed cheeks — he's running hot
for lbl, cx in [("Flush L", bx + 44), ("Flush R", bx + 186)]:
    d.shape("ellipse", lbl, x=cx - 16, y=by + 150, width=32, height=18,
            fill=HOT, opacity=30, stroke=NONE)
# one heroic sweat bead
d.path(f"M{bx + 200},{by + 60} C{bx + 210},{by + 76} {bx + 212},{by + 84} {bx + 212},{by + 92} "
       f"C{bx + 212},{by + 102} {bx + 206},{by + 108} {bx + 198},{by + 108} "
       f"C{bx + 190},{by + 108} {bx + 186},{by + 100} {bx + 188},{by + 90} "
       f"C{bx + 190},{by + 82} {bx + 194},{by + 70} {bx + 200},{by + 60} Z",
       "Sweat", fill="#BEE0F0", stroke=INK, strokeWidth=3, opacity=90)

# --- chest fan: spinning at high speed ---------------------------------------------
fcx, fcy, fr = bx + bw / 2, by + 288, 62
d.shape("ellipse", "Fan recess", x=fcx - fr, y=fcy - fr, width=2 * fr,
        height=2 * fr, fill=FAN_GRAD, stroke=INK, strokeWidth=5)
# blades: three fat comma arcs mid-spin
for i in range(3):
    a0 = math.radians(i * 120 + 18)
    pts = []
    for k in range(7):
        t = k / 6
        r = fr * (0.28 + 0.58 * t)
        a = a0 + t * math.radians(78)
        pts.append((fcx + r * math.cos(a), fcy + r * math.sin(a)))
    s = "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:])
    # close the blade back along a shorter arc
    for k in range(7):
        t = 1 - k / 6
        r = fr * (0.28 + 0.44 * t)
        a = a0 + t * math.radians(78) + math.radians(10)
        s += " L%.1f,%.1f" % (fcx + r * math.cos(a), fcy + r * math.sin(a))
    s += " Z"
    d.path(s, f"Fan blade {i+1}", fill="#7E8896", stroke=INK,
           strokeWidth=2.5, opacity=92)
d.shape("ellipse", "Fan hub", x=fcx - 15, y=fcy - 15, width=30, height=30,
        fill="#AAB2BE", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hub cap", x=fcx - 5, y=fcy - 5, width=10, height=10,
        fill=INK, stroke=NONE)
# grille ring + spin blur arcs
d.shape("ellipse", "Fan ring", x=fcx - fr, y=fcy - fr, width=2 * fr,
        height=2 * fr, fill=NONE, stroke="#4A525E", strokeWidth=4)
for i, rr in enumerate([fr + 12, fr + 24]):
    a0 = 40 + i * 160
    a1 = a0 + 120
    p0 = (fcx + rr * math.cos(math.radians(a0)), fcy + rr * math.sin(math.radians(a0)))
    p1 = (fcx + rr * math.cos(math.radians(a1)), fcy + rr * math.sin(math.radians(a1)))
    d.path(f"M{p0[0]:.0f},{p0[1]:.0f} A{rr},{rr} 0 0 1 {p1[0]:.0f},{p1[1]:.0f}",
           f"Spin arc {i+1}", fill=NONE, stroke="#C8D4DE", strokeWidth=4,
           opacity=50 - i * 15, cap="round")

# vents under the fan, exhaling heat
for i in range(4):
    vy = by + 372 + i * 14
    d.path(f"M{bx + 74},{vy} L{bx + bw - 74},{vy}", f"Vent {i+1}",
           fill=NONE, stroke="#4A525E", strokeWidth=5, cap="round",
           opacity=80)

# --- arms: one mopping the brow, one dangling in despair -----------------------------
d.path(f"M{bx + bw - 20},{by + 160} C{bx + bw + 32},{by + 140} {bx + bw + 40},{by + 98} "
       f"{bx + bw + 16},{by + 66}", "Arm brow", fill=NONE, stroke=STEEL,
       strokeWidth=28, cap="round")
d.shape("ellipse", "Hand brow", x=bx + bw - 22, y=by + 46, width=40,
        height=34, fill="#B0B8C4", stroke=INK, strokeWidth=4)
# the rag, already damp
d.path(rot_rect_path(bx + bw - 30, by + 58, 30, 24, -14), "Rag",
       fill="#D8CCB0", stroke=INK, strokeWidth=3, opacity=90)
d.path(f"M{bx + 18},{by + 210} C{bx - 20},{by + 250} {bx - 28},{by + 300} "
       f"{bx - 20},{by + 344}", "Arm dangle", fill=NONE, stroke=STEEL,
       strokeWidth=28, cap="round")
d.shape("ellipse", "Hand dangle", x=bx - 44, y=by + 332, width=40,
        height=34, fill="#B0B8C4", stroke=INK, strokeWidth=4)

# --- captions ----------------------------------------------------------------------
d.text("BOILY MCPLATERTON", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E0E8EC", justify="center")
r = d.text("A HEAT ADVISORY WARNING", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9DB4BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("004.boily-mcplaterton-V1R00")
