#!/usr/bin/env python3
"""APH-008 Cssandra Cascade — aphorism plate V1R00. A specificity war as
concentric frames: ghosted HTML/BODY ancestors, then DIV < .CASCADE <
#SPECIFICITY in escalating, clashing colors, the innermost frame rotated
— it renders, but chooses a different understanding. An !IMPORTANT
hammer descends on the whole hierarchy. Cool indigo plate, hot accents.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-008 Cssandra Cascade — Aphorism Plate", 1000, 1000)

INK = "#241A2E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181426"}, {"offset": 1, "color": "#07060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#32304E"}, {"offset": 0.7, "color": "#1B1932"},
    {"offset": 1, "color": "#0D0B1A"}]}}
STEEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8E4F4"}, {"offset": 0.55, "color": "#A8A0C8"},
    {"offset": 1, "color": "#5E5680"}]}}
HAMMER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F08A5E"}, {"offset": 0.55, "color": "#C45038"},
    {"offset": 1, "color": "#7E2A1E"}]}}
TEAL = "#46C0AE"
AMBER = "#E8A43C"
VIOLET = "#B06AD8"
HOT = "#E05A3A"
CREAM = "#E8E2F0"
FAINT = "#8A90B8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5AA8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8AEE0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(200, 220, 7), (795, 230, 8), (165, 500, 6),
                               (838, 505, 7), (245, 745, 6), (758, 735, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E5488", opacity=35, stroke=NONE)

# --- ancestor frames: the DOM above, barely holding on ------------------------
d.shape("rectangle", "HTML frame", x=195, y=185, width=610, height=500,
        radius=6, fill=NONE, stroke=FAINT, strokeWidth=3, opacity=30,
        dash=[12, 9])
d.text("HTML", "HTML tag", x=211, y=205, size=13, font="Virelai Sans",
       color="#5E6488", justify="left")
d.shape("rectangle", "BODY frame", x=218, y=222, width=564, height=430,
        radius=6, fill=NONE, stroke=FAINT, strokeWidth=3.5, opacity=40,
        dash=[12, 9])
d.text("BODY", "BODY tag", x=234, y=642, size=13, font="Virelai Sans",
       color="#767CA8", justify="left")

# --- the specificity war: nested frames, each more specific, none agreeing -----
def frame(x, y, w, h, color, label, score, opacity, rot=0, suffix=""):
    if rot:
        cx, cy = x + w / 2, y + h / 2
        d.path(rot_rect_path(cx, cy, w, h, rot), f"{label} fill{suffix}",
               fill=color, opacity=10, stroke=NONE)
        d.path(rot_rect_path(cx, cy, w, h, rot), f"{label} frame{suffix}",
               fill=NONE, stroke=color, strokeWidth=6)
    else:
        d.shape("rectangle", f"{label} fill{suffix}", x=x, y=y, width=w,
                height=h, radius=6, fill=color, opacity=10, stroke=NONE)
        d.shape("rectangle", f"{label} frame{suffix}", x=x, y=y, width=w,
                height=h, radius=6, fill=NONE, stroke=color, strokeWidth=6)
    d.text(label, f"{label} label{suffix}", x=x + 14, y=y + 26, size=14,
           font="Virelai Sans", color=color, justify="left")
    d.text(score, f"{label} score{suffix}", x=x + w - 14 - len(score) * 8,
           y=y + h - 14, size=12, font="Virelai Sans", color=color,
           justify="left")

frame(230, 230, 540, 385, TEAL, "DIV", "0-0-1", 10)
frame(282, 272, 446, 300, AMBER, ".CASCADE", "0-1-0", 10)
frame(334, 314, 352, 222, VIOLET, "#SPECIFICITY", "1-0-0", 10)
# innermost: the inline style — rotated, saturated, winning ugly
frame(380, 352, 260, 158, HOT, "STYLE", "INLINE", 14, rot=-3)

# crack along the innermost frame's struck corner
d.path("M618,346 L632,362 L624,378 L640,392", "Impact crack", fill=NONE,
       stroke=HOT, strokeWidth=3.5, opacity=85, cap="round")

# impact starburst where the hammer lands
for ang in [-95, -55, -15, 25, 65]:
    a = math.radians(ang)
    x1 = 618 + math.cos(a) * 14
    y1 = 352 + math.sin(a) * 14
    x2 = 618 + math.cos(a) * 44
    y2 = 352 + math.sin(a) * 44
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Spark {ang}",
           fill=NONE, stroke="#F4C06A", strokeWidth=4, opacity=80,
           cap="round")
d.shape("ellipse", "Impact flash", x=596, y=330, width=46, height=46,
        fill="#F4E4A0", opacity=35, stroke=NONE)

# --- the !IMPORTANT hammer, descending ----------------------------------------
for i, (hx, hy, hl) in enumerate([(735, 210, 26), (752, 224, 26),
                                  (769, 238, 26)]):
    a = math.radians(-50)
    d.path(f"M{hx},{hy} L{hx + math.cos(a) * hl:.0f},{hy + math.sin(a) * hl:.0f}",
           f"Hammer motion {i+1}", fill=NONE, stroke=CREAM, strokeWidth=3.5,
           opacity=50, cap="round")
# handle into the head
d.path(rot_rect_path(678, 252, 140, 16, -50), "Hammer handle",
       fill=STEEL_GRAD, stroke=INK, strokeWidth=3)
# head: a flat verdict
d.shape("rectangle", "Hammer head", x=596, y=290, width=124, height=62,
        radius=6, fill=HAMMER_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Head sheen", x=604, y=296, width=108, height=12,
        radius=5, fill="#F8C8A8", opacity=55, stroke=NONE)
r = d.text("!IMPORTANT", "Head label", x=658, y=330, size=15,
           font="Virelai Sans", color="#F8E8D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "head tracking", ids=[r["id"]], tracking=30)

# --- aphorism line + name + role ------------------------------------------------
r = d.text("OVERRIDE FOLLOWS OVERRIDE —", "Key line 1", x=500, y=722,
           size=22, font="Virelai Sans", color="#C8BEE0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("SPECIFICITY WON.", "Key line 2", x=500, y=756,
           size=22, font="Virelai Sans", color="#C8BEE0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("CSSANDRA CASCADE", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("SPECIFICITY HIERARCHY STABLE", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#9A8EC0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-008-cssandra-cascade-V1R00")
