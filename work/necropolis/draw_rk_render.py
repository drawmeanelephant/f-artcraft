#!/usr/bin/env python3
"""rc-render.sh — The Resurrection. Necropolis plate V1R00.
Markdown corpses on stone slabs rise as luminous HTML pages — what lives
in /bones/ may yet render again — wrapped in theme like grave-clothes of
CSS, each standing a little straighter than it did in life.
1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-Render — Necropolis Plate", 1000, 1000)

INK = "#161A20"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1218"}, {"offset": 1, "color": "#06080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E585E"}, {"offset": 0.7, "color": "#232A30"},
    {"offset": 1, "color": "#10151A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E343A"}, {"offset": 1, "color": "#12161A"}]}}
SLAB = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E747A"}, {"offset": 1, "color": "#3E444A"}]}}
SLAB_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5056"}, {"offset": 1, "color": "#262C32"}]}}
PAGE_DEAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A8E92"}, {"offset": 1, "color": "#5A5E62"}]}}
PAGE_RISEN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF8E0"}, {"offset": 0.75, "color": "#F0D9A0"},
    {"offset": 1, "color": "#C9A45E"}]}}
LINEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D8B8"}, {"offset": 1, "color": "#C4B48E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E686E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D0D4", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#525E64", opacity=35, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080B0E",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Slab L shadow", x=180, y=686, width=260, height=18,
        fill="#030405", opacity=55, stroke=NONE)
d.shape("ellipse", "Slab R shadow", x=520, y=686, width=280, height=18,
        fill="#030405", opacity=55, stroke=NONE)

# --- left slab: a corpse of markdown, still lying ------------------------------------
d.path("M200,640 L420,640 L420,700 L200,700 Z", "Slab L front", fill=SLAB_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M200,640 L420,640 L400,612 L220,612 Z", "Slab L top", fill=SLAB,
       stroke=INK, strokeWidth=4, join="round")
# the dead page: flat, dim, sigils of a plainer faith
d.path(rot_rect_path(312, 622, 130, 78, -8), "Dead page", fill=PAGE_DEAD,
       stroke=INK, strokeWidth=4, join="round")
for i, (dx, dy, w) in enumerate([(-40,-18,52),(-40,-4,80),(-40,10,64)]):
    d.path(rot_rect_path(312+dx+w/2, 622+dy, w, 4, -8), f"Dead line {i+1}",
           fill="#3E444A", opacity=70, stroke=NONE)
d.text("#", "Markdown sigil", x=280, y=612, size=16, font="Source Sans 3",
       color="#3E444A", justify="center")
# the lid that was eased aside
d.path(rot_rect_path(180, 668, 150, 26, -14), "Slab L lid", fill=SLAB_DK,
       stroke=INK, strokeWidth=4, join="round")

# --- right slab: the place it lay, now empty ---------------------------------------
d.path("M540,652 L780,652 L780,700 L540,700 Z", "Slab R front", fill=SLAB_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M540,652 L780,652 L756,622 L564,622 Z", "Slab R top", fill=SLAB,
       stroke=INK, strokeWidth=4, join="round")
# faint outline where the body lay
d.path(rot_rect_path(660, 636, 128, 70, 0), "Impression", fill=NONE,
       stroke="#2A3036", strokeWidth=3, opacity=60, join="round")
# grave-clothes left behind on the slab
d.path(rot_rect_path(596, 640, 74, 12, 10), "Shed cloth 1", fill=LINEN,
       opacity=50, stroke=INK, strokeWidth=2, join="round")
d.path(rot_rect_path(716, 646, 60, 10, -16), "Shed cloth 2", fill=LINEN,
       opacity=40, stroke=INK, strokeWidth=2, join="round")

# --- resurrection light -------------------------------------------------------------
d.shape("ellipse", "Glory", x=440, y=200, width=420, height=420,
        fill="#F0C868", opacity=16, stroke=NONE)
d.shape("ellipse", "Core glow", x=540, y=300, width=220, height=240,
        fill="#F8E4AE", opacity=22, stroke=NONE)
# rays leaning heavenward
for i, (x0, w_, op) in enumerate([(560,10,25),(610,14,32),(668,10,22),
                                  (720,8,18)]):
    d.path(f"M{x0},600 L{x0+w_/2},300 L{x0+w_},600 Z", f"Ray {i+1}",
           fill="#F0C868", opacity=op, stroke=NONE)

# --- the risen page ------------------------------------------------------------------
# a second page mid-rise behind, still climbing, still dim
d.path(rot_rect_path(468, 510, 92, 120, -24), "Rising page", fill=PAGE_DEAD,
       opacity=80, stroke=INK, strokeWidth=4, join="round")
d.path(rot_rect_path(468, 510, 60, 5, -24), "Rising line", fill="#3E444A",
       opacity=60, stroke=NONE, join="round")
# standing straighter than it did in life: upright, luminous
d.path("M592,560 L592,330 L640,330 L672,360 L672,560 Z", "Risen page",
       fill=PAGE_RISEN, stroke=INK, strokeWidth=5, join="round")
# folded corner
d.path("M640,330 L640,362 L672,362 Z", "Fold", fill="#C9A45E", stroke=INK,
       strokeWidth=3, join="round")
# reborn content: brighter ruled lines
for i, y in enumerate([386, 402, 418, 434]):
    d.path(f"M606,{y} L656,{y}", f"Live line {i+1}", fill=NONE,
           stroke="#8A6E3E", strokeWidth=3, opacity=65, cap="round")
d.text("<>", "Markup sigil", x=631, y=470, size=17, font="Source Sans 3",
       color="#8A6E3E", justify="center")
# grave-clothes of CSS: theme wrapped around the risen form
d.path("M590,404 C614,394 650,394 674,404 L674,418 C650,408 614,408 590,418 Z",
       "Theme band 1", fill=LINEN, stroke=INK, strokeWidth=3,
       opacity=85, join="round")
d.path("M590,492 C616,482 652,482 674,492 L674,506 C652,496 616,496 590,506 Z",
       "Theme band 2", fill=LINEN, stroke=INK, strokeWidth=3,
       opacity=85, join="round")
# trailing ends, still unwinding
d.path("M674,412 C700,410 716,420 724,436", "Band tail 1", fill=NONE,
       stroke="#C4B48E", strokeWidth=7, cap="round")
d.path("M590,500 C570,504 558,516 556,532", "Band tail 2", fill=NONE,
       stroke="#C4B48E", strokeWidth=6, cap="round")

# --- motes of light -----------------------------------------------------------------
for i, (x, y, w) in enumerate([(560,290,6),(700,330,5),(520,380,4),
                               (740,420,5),(660,270,4),(580,240,5),
                               (720,540,4)]):
    d.path(f"M{x-w},{y} L{x+w},{y} M{x},{y-w} L{x},{y+w}", f"Mote {i+1}",
           fill=NONE, stroke="#F0D9A0", strokeWidth=3, opacity=80,
           cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-RENDER", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DDE2E6", justify="center")
r = d.text("WHAT RENDERS AGAIN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA6AE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-render-V1R00")
