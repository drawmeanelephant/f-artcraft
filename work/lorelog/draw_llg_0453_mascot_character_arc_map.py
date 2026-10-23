#!/usr/bin/env python3
"""LLG-0453 Mascot Character Arc Map — V1R00. Five corridor mascots around a
central filing cabinet: Kindy (lantern, Form 12-A), Bricky (two screens,
notebook), 404sy (sitemap dissolving into void), Datty (YAML, vanishing keys),
Boily (cracked casing, steam). 1000x1000, archive-parchment plate on dark."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LLG-0453 Mascot Character Arc Map", 1000, 1000)

INK = "#3A2A22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241C2A"}, {"offset": 1, "color": "#110C16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9C9A4"}, {"offset": 0.72, "color": "#A8916B"},
    {"offset": 1, "color": "#6E5B40"}]}}

def rr(x, y, w, h, r):
    return (f"M{x+r},{y} H{x+w-r} A{r},{r} 0 0 1 {x+w},{y+r} V{y+h-r} "
            f"A{r},{r} 0 0 1 {x+w-r},{y+h} H{x+r} A{r},{r} 0 0 1 {x},{y+h-r} "
            f"V{y+r} A{r},{r} 0 0 1 {x+r},{y} Z")

def body(cx, top, w, h, grad, label, eye_dy=0.32, r=None):
    """Capsule mascot body + eyes. Returns eye line y."""
    r = r if r is not None else w * 0.45
    d.path(rr(cx - w/2, top, w, h, r), f"{label} body", fill=grad,
           stroke=INK, strokeWidth=4)
    ey = top + h * eye_dy
    d.shape("ellipse", f"{label} eye L", x=cx - w*0.17 - 5, y=ey - 6,
            width=10, height=12, fill="#2A1C16", stroke=NONE)
    d.shape("ellipse", f"{label} eye R", x=cx + w*0.17 - 5, y=ey - 6,
            width=10, height=12, fill="#2A1C16", stroke=NONE)
    d.shape("ellipse", f"{label} glint L", x=cx - w*0.17 - 3, y=ey - 4,
            width=3, height=3, fill="#FFFFFF", opacity=85, stroke=NONE)
    d.shape("ellipse", f"{label} glint R", x=cx + w*0.17 - 3, y=ey - 4,
            width=3, height=3, fill="#FFFFFF", opacity=85, stroke=NONE)
    return ey

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54462E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFE3C4", strokeWidth=3, opacity=55)
# archive patina
d.shape("ellipse", "Patina 1", x=170, y=150, width=240, height=150,
        fill="#8C7852", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=680, width=260, height=140,
        fill="#8C7852", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,8),(780,250,7),(160,540,9),(820,540,8),
                               (260,780,7),(740,760,9),(140,420,6),(860,410,7),
                               (410,120,7),(600,115,8),(350,840,6),(660,830,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A3C", opacity=40, stroke=NONE)

# --- central filing cabinet ---------------------------------------------------
CAB_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6B6058"}, {"offset": 1, "color": "#3E3730"}]}}
d.path(rr(415, 470, 170, 210, 10), "Cabinet", fill=CAB_GRAD,
       stroke=INK, strokeWidth=5)
d.shape("ellipse", "Cabinet shade", x=420, y=475, width=160, height=60,
        fill="#FFFFFF", opacity=8, stroke=NONE)
for i, dy in enumerate([485, 545, 605]):
    d.path(rr(432, dy, 136, 50, 5), f"Drawer {i+1}", fill="#574D44",
           stroke=INK, strokeWidth=3)
    d.path(rr(478, dy+10, 44, 14, 3), f"Drawer {i+1} label",
           fill="#D9C9A4", stroke=INK, strokeWidth=2)
    d.shape("rectangle", f"Drawer {i+1} pull", x=488, y=dy+30, width=24,
            height=6, fill="#2E2620", stroke=NONE)
# cabinet top: one proud form poking out
d.path(rr(455, 436, 64, 40, 4), "Top form", fill="#E8DCC0",
       stroke=INK, strokeWidth=3)
d.shape("rectangle", "Top form line", x=464, y=448, width=46, height=4,
        fill="#8A7A5E", stroke=NONE)
d.shape("rectangle", "Top form line 2", x=464, y=458, width=34, height=4,
        fill="#8A7A5E", stroke=NONE)

# --- Kindy (left, at a desk, freezing Form 12-A, lantern) ---------------------
KINDY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2D48A"}, {"offset": 1, "color": "#C79A4E"}]}}
# desk
d.path(rr(215, 640, 180, 18, 4), "Kindy desk top", fill="#5E4A34",
       stroke=INK, strokeWidth=4)
d.shape("rectangle", "Kindy desk leg L", x=228, y=658, width=14, height=66,
        fill="#4A3A28", stroke=NONE)
d.shape("rectangle", "Kindy desk leg R", x=368, y=658, width=14, height=66,
        fill="#4A3A28", stroke=NONE)
# Form 12-A on desk
d.path(rr(300, 598, 62, 44, 4), "Form 12-A", fill="#E8DCC0",
       stroke=INK, strokeWidth=3)
d.text("12-A", "Form 12-A label", x=331, y=610, size=16, font="Virelai Sans",
       color=INK, justify="center")
d.shape("rectangle", "Form line 1", x=308, y=624, width=46, height=3,
        fill="#8A7A5E", stroke=NONE)
d.shape("rectangle", "Form line 2", x=308, y=632, width=34, height=3,
        fill="#8A7A5E", stroke=NONE)
# Kindy behind the desk
body(250, 560, 84, 104, KINDY_GRAD, "Kindy")
# little clerk visor
d.path("M214,556 H286 L278,540 H222 Z", "Kindy visor", fill="#3E5732",
       stroke=INK, strokeWidth=3)
# lantern held to the left
LANT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF3C2"}, {"offset": 1, "color": "#E8A33D"}]}}
d.shape("ellipse", "Lantern glow", x=150, y=560, width=86, height=86,
        fill="#FFDF8A", opacity=30, stroke=NONE)
d.shape("ellipse", "Lantern glass", x=166, y=576, width=54, height=54,
        fill=LANT_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Lantern flame", x=184, y=596, width=18, height=22,
        fill="#FFF6D8", stroke=NONE)
d.path("M178,576 Q193,552 208,576", "Lantern bail", fill=NONE,
       stroke=INK, strokeWidth=3)
d.shape("rectangle", "Lantern base", x=172, y=628, width=42, height=8,
        fill=INK, stroke=NONE)
# arm from Kindy to lantern
d.path("M216,600 Q196,596 186,604", "Kindy arm", fill=NONE,
       stroke="#C79A4E", strokeWidth=9, cap="round")

# --- Bricky (right top, between two screens, notebook) ------------------------
BRICK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E08A72"}, {"offset": 1, "color": "#A8543E"}]}}
SCR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C4A5E"}, {"offset": 1, "color": "#1E2836"}]}}
# two screens flanking
for i, sx in enumerate([592, 786]):
    d.path(rr(sx, 300, 88, 66, 6), f"Screen {i+1}", fill=SCR_GRAD,
           stroke=INK, strokeWidth=4)
    d.shape("rectangle", f"Screen {i+1} glow", x=sx+8, y=310, width=72,
            height=8, fill="#9FC4E8", opacity=45, stroke=NONE)
    d.shape("rectangle", f"Screen {i+1} line2", x=sx+8, y=324, width=50,
            height=6, fill="#6E8CAA", opacity=40, stroke=NONE)
    d.shape("rectangle", f"Screen {i+1} line3", x=sx+8, y=336, width=62,
            height=6, fill="#6E8CAA", opacity=30, stroke=NONE)
    d.shape("rectangle", f"Screen {i+1} stand", x=sx+36, y=366, width=16,
            height=18, fill="#2E2620", stroke=NONE)
# bricky body — literally brick-squared shoulders
body(736, 356, 88, 116, BRICK_GRAD, "Bricky", r=14)
# mortar lines
d.shape("rectangle", "Bricky mortar 1", x=700, y=412, width=72, height=4,
        fill="#7C3A2A", opacity=70, stroke=NONE)
d.shape("rectangle", "Bricky mortar 2", x=700, y=442, width=72, height=4,
        fill="#7C3A2A", opacity=70, stroke=NONE)
d.shape("rectangle", "Bricky mortar v", x=732, y=412, width=4, height=30,
        fill="#7C3A2A", opacity=70, stroke=NONE)
# notebook tucked under arm
d.path(rr(690, 448, 44, 54, 4), "Bricky notebook", fill="#E8DCC0",
       stroke=INK, strokeWidth=3)
d.shape("rectangle", "Notebook band", x=690, y=462, width=44, height=6,
        fill="#A8543E", stroke=NONE)

# --- 404sy (left top, sitemap dissolving into a void) --------------------------
FY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2D6E2"}, {"offset": 1, "color": "#7E9AAE"}]}}
VOID_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#120D18"}, {"offset": 0.8, "color": "#241C2E"},
    {"offset": 1, "color": "#A8916B"}]}}
# the void upper-left, fading out through the plate edge is avoided — keep inside
d.shape("ellipse", "Void", x=150, y=130, width=200, height=200,
        fill=VOID_GRAD, stroke=NONE)
# dissolving sitemap: sheet held out, particles escaping toward the void
body(300, 330, 80, 108, FY_GRAD, "404sy")
d.path(rr(216, 380, 66, 78, 5), "Sitemap sheet", fill="#E8DCC0",
       stroke=INK, strokeWidth=3)
# sitemap diagram on the sheet
d.shape("ellipse", "Site node root", x=238, y=392, width=12, height=12,
        fill="#5A6E82", stroke=NONE)
d.path("M244,404 L232,424 M244,404 L256,424 M244,404 L244,428", "Site links",
       fill=NONE, stroke="#5A6E82", strokeWidth=2)
for i, (nx, ny) in enumerate([(226, 424), (250, 424), (238, 432)]):
    d.shape("ellipse", f"Site node {i+1}", x=nx, y=ny, width=10, height=10,
            fill="#5A6E82", stroke=NONE)
# dissolve particles marching into the void
for i, (px, py, pw, op) in enumerate([(252, 360, 9, 80), (240, 336, 8, 70),
                                      (230, 312, 7, 60), (222, 288, 7, 52),
                                      (216, 262, 6, 44), (212, 238, 5, 36),
                                      (208, 214, 5, 28), (206, 192, 4, 20)]):
    d.shape("ellipse", f"Dissolve {i+1}", x=px, y=py, width=pw, height=pw,
            fill="#E8DCC0", opacity=op, stroke=NONE)
d.path("M282,418 Q300,428 318,418", "404sy frown", fill=NONE,
       stroke="#33455A", strokeWidth=3, cap="round")

# --- Datty (right bottom, YAML doc, malformed keys disappearing) --------------
DATTY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8C69A"}, {"offset": 1, "color": "#648A58"}]}}
body(722, 566, 82, 108, DATTY_GRAD, "Datty")
# YAML document held out front
d.path(rr(788, 588, 74, 92, 5), "YAML doc", fill="#EDE4CC",
       stroke=INK, strokeWidth=3)
d.text("---", "YAML fence", x=825, y=604, size=13, font="Virelai Sans",
       color="#6A5C40", justify="center")
for i, (ly, lw) in enumerate([(614, 52), (626, 40), (638, 56)]):
    d.shape("rectangle", f"YAML line {i+1}", x=798, y=ly, width=lw, height=4,
            fill="#8A7A5E", stroke=NONE)
# malformed keys vanishing off the doc (strikethrough + fading glyphs)
for i, (kx, ky, op) in enumerate([(858, 560, 70), (872, 538, 55),
                                   (884, 516, 40), (894, 494, 26)]):
    d.shape("rectangle", f"Lost key {i+1}", x=kx, y=ky, width=16, height=5,
            fill="#B03A2E", opacity=op, stroke=NONE)
    d.shape("rectangle", f"Lost key d{i+1}", x=kx+4, y=ky-4, width=5,
            height=13, fill="#B03A2E", opacity=op, stroke=NONE)
# red pencil in hand
d.path("M700,650 L668,690", "Datty pencil", fill=NONE,
       stroke="#B03A2E", strokeWidth=7, cap="round")
d.path("M668,690 L662,700 L672,696 Z", "Pencil tip", fill="#3A2A22",
       stroke=NONE)

# --- Boily (front center, cracked casing, steam, screaming fan) ----------------
BOILY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8985E"}, {"offset": 1, "color": "#A8502E"}]}}
HOT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFD98A"}, {"offset": 1, "color": "#E86A3A"}]}}
# tower casing
d.path(rr(440, 690, 120, 128, 10), "Boily casing", fill=BOILY_GRAD,
       stroke=INK, strokeWidth=5)
# crack in the casing
d.path("M468,700 L482,730 L470,752 L488,780", "Casing crack", fill=NONE,
       stroke="#3A1E12", strokeWidth=5, cap="round")
# inner glow through the crack
d.path("M472,706 L482,728 L474,748 L486,772", "Crack glow", fill=NONE,
       stroke="#FFD98A", strokeWidth=2, opacity=80, cap="round")
# face on the casing
d.shape("ellipse", "Boily eye L", x=505, y=712, width=12, height=15,
        fill="#2A1C16", stroke=NONE)
d.shape("ellipse", "Boily eye R", x=532, y=712, width=12, height=15,
        fill="#2A1C16", stroke=NONE)
d.path("M502,748 Q524,762 548,746", "Boily grimace", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# screaming fan, front-bottom of casing
d.shape("ellipse", "Fan housing", x=452, y=762, width=52, height=52,
        fill="#3E2E24", stroke=INK, strokeWidth=3)
for i, ang in enumerate([0, 90, 180, 270]):
    import math
    a = math.radians(ang + 30)
    x1 = 478 + math.cos(a) * 18
    y1 = 788 + math.sin(a) * 18
    d.path(f"M478,788 L{x1:.0f},{y1:.0f}", f"Fan blade {i+1}", fill=NONE,
           stroke="#C9B68E", strokeWidth=6, cap="round")
d.shape("ellipse", "Fan hub", x=472, y=782, width=12, height=12,
        fill=HOT_GRAD, stroke=NONE)
# fan motion arcs
d.path("M450,768 A42,42 0 0 1 508,770", "Fan spin 1", fill=NONE,
       stroke="#E8DCC0", strokeWidth=3, opacity=45, cap="round")
d.path("M448,806 A42,42 0 0 0 506,808", "Fan spin 2", fill=NONE,
       stroke="#E8DCC0", strokeWidth=3, opacity=45, cap="round")
# steam venting from the top crack
for i, (sx, sy, sw, sh, op) in enumerate([(500, 660, 40, 30, 45),
                                          (478, 626, 52, 38, 36),
                                          (512, 588, 62, 44, 27),
                                          (486, 546, 74, 50, 18)]):
    d.shape("ellipse", f"Steam {i+1}", x=sx, y=sy, width=sw, height=sh,
            fill="#EFE3C4", opacity=op, stroke=NONE)
# heat shimmer around Boily
d.shape("ellipse", "Boily heat halo", x=415, y=665, width=170, height=170,
        fill="#E86A3A", opacity=12, stroke=NONE)

# --- name + role ----------------------------------------------------------------
d.text("CHARACTER ARC MAP", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#EFE3C4", justify="center")
d.text("T H E   A R C H I V E ' S   N E R V O U S   S Y S T E M", "Role",
       x=500, y=968, size=20, font="Virelai Sans", color="#B8A67E",
       justify="center")

d.finish("llg-0453-mascot-character-arc-map-V1R00")
