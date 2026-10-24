#!/usr/bin/env python3
"""rc-showcase.sh — The Rehearsal. Necropolis plate V1R00.
A gallery of coffin-shaped display cases in a row, each open and lit, each
displaying the same test page dressed in a different template — the wake
rehearsed in every theme so no layout meets its maker unprepared. Velvet
linings, case-glass, spotlight. 1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Showcase — Necropolis Plate", 1000, 1000)

INK = "#241418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181016"}, {"offset": 1, "color": "#0A060A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E3A4A"}, {"offset": 0.7, "color": "#281E28"},
    {"offset": 1, "color": "#120C12"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#342430"}, {"offset": 1, "color": "#140E14"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3226"}, {"offset": 1, "color": "#241710"}]}}
WOOD_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#36241A"}, {"offset": 1, "color": "#160E08"}]}}
VELVET = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E2E3E"}, {"offset": 1, "color": "#4A1420"}]}}
VELVET_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E2230"}, {"offset": 1, "color": "#38101A"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C26A"}, {"offset": 1, "color": "#9A782E"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE2C6"}, {"offset": 1, "color": "#C4B490"}]}}
PALE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4F2EC"}, {"offset": 1, "color": "#D6D2C6"}]}}
NIGHT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3542"}, {"offset": 1, "color": "#1C1822"}]}}
BEAM = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0D890"}, {"offset": 1, "color": "#C8A44E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5468", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4D0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4858", opacity=35, stroke=NONE)

# --- the spotlight rail + beams ------------------------------------------------
d.path("M215,196 L785,196 L785,208 L215,208 Z", "Spot rail", fill=WOOD_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M218,196 L782,196", "Rail edge light", fill=NONE, stroke="#8A6E50",
       strokeWidth=2, opacity=55)
for i, cx in enumerate([270, 505, 740]):
    # lamp head
    d.path(f"M{cx-14},208 L{cx+14},208 L{cx+9},226 L{cx-9},226 Z",
           f"Lamp head {i+1}", fill=BRASS, stroke=INK, strokeWidth=3,
           join="round")
    d.shape("ellipse", f"Lamp lens {i+1}", x=cx-8, y=222, width=16, height=6,
            fill="#F8ECC0", opacity=90, stroke=NONE)
    # the beam: translucent cone down onto the case
    d.path(f"M{cx-9},228 L{cx-82},372 L{cx+82},372 L{cx+9},228 Z",
           f"Beam {i+1}", fill=BEAM, opacity=13, stroke=NONE)
    d.shape("ellipse", f"Beam pool {i+1}", x=cx-70, y=352, width=140,
            height=30, fill="#F0D890", opacity=10, stroke=NONE)
# dust motes in the beams
for i, (x, y, w) in enumerate([(252,290,4),(286,330,3),(492,300,4),(524,336,3),
                               (726,294,4),(758,332,3)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4E4B0", opacity=40, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A060A",
       strokeWidth=4, opacity=70)
for i, cx in enumerate([270, 505, 740]):
    d.shape("ellipse", f"Case shadow {i+1}", x=cx-85, y=686, width=170,
            height=16, fill="#060306", opacity=55, stroke=NONE)

# --- the display cases -------------------------------------------------------------
# coffin silhouette, standing: narrow head, wide shoulders, tapering foot
def coffin(cx, yt, yb, wt, ws, wb):
    ysh = yt + (yb - yt) * 0.26
    return (f"M{cx-wt/2},{yt} L{cx+wt/2},{yt} L{cx+ws/2},{ysh:.0f} "
            f"L{cx+wb/2},{yb} L{cx-wb/2},{yb} L{cx-ws/2},{ysh:.0f} Z")

def display_case(cx, idx, dress):
    yt, yb, wt, ws, wb = 380, 700, 92, 152, 112
    ysh = yt + (yb - yt) * 0.26
    # the open door, hinged on the left jamb, swung toward the viewer:
    # skewed coffin showing its velvet lining
    d.path(f"M{cx-wt/2},{yt} L{cx-wt/2-38},{yt+16} L{cx-ws/2-38},{ysh+12:.0f} "
           f"L{cx-wb/2-34},{yb-8} L{cx-wb/2},{yb} L{cx-ws/2},{ysh:.0f} Z",
           f"Case {idx} door", fill=VELVET_DK, stroke=INK, strokeWidth=4,
           join="round")
    d.path(f"M{cx-wt/2-10},{yt+18} L{cx-ws/2-30},{ysh+8:.0f} "
           f"L{cx-wb/2-26},{yb-22}", f"Case {idx} door seam", fill=NONE,
           stroke="#9E4452", strokeWidth=3, opacity=55)
    d.shape("ellipse", f"Case {idx} door pull", x=cx-ws/2-40, y=(yt+yb)/2-4,
            width=9, height=9, fill=BRASS, stroke=INK, strokeWidth=2)
    # case body + velvet interior
    d.path(coffin(cx, yt, yb, wt, ws, wb), f"Case {idx} body", fill=WOOD,
           stroke=INK, strokeWidth=5, join="round")
    d.path(coffin(cx, yt+16, yb-14, wt-16, ws-24, wb-18),
           f"Case {idx} lining", fill=VELVET, stroke=INK, strokeWidth=3,
           join="round")
    # velvet puffs: soft tufting
    for j, (px, py) in enumerate([(cx-34, ysh+46), (cx+34, ysh+46),
                                  (cx-38, yb-64), (cx+38, yb-64)]):
        d.shape("ellipse", f"Case {idx} tuft {j+1}", x=px-9, y=py-6, width=18,
                height=12, fill="#5E1A26", opacity=60, stroke=NONE)
    # brass mounts
    d.shape("ellipse", f"Case {idx} mount top", x=cx-10, y=yt+2, width=20,
            height=8, fill=BRASS, stroke=INK, strokeWidth=2)
    # the mounted page, same page in a different dress
    px, py, pw, ph = cx-44, 456, 88, 168
    dress(px, py, pw, ph, idx)
    # brass mount pins at the page's top corners
    for j, sx in enumerate([-1, 1]):
        d.shape("ellipse", f"Case {idx} pin {j+1}", x=px+pw/2+sx*(pw/2-8)-4,
                y=py+4, width=8, height=8, fill=BRASS, stroke=INK,
                strokeWidth=2)
    # case-glass: one diagonal sheen across the front
    d.path(f"M{cx-30},{446} L{cx+2},{446} L{cx-38},{636} L{cx-62},{636} Z",
           f"Case {idx} glass", fill="#FFFFFF", opacity=10, stroke=NONE)
    d.path(f"M{cx+14},{446} L{cx+26},{446} L{cx-12},{636} L{cx-20},{636} Z",
           f"Case {idx} glass 2", fill="#FFFFFF", opacity=7, stroke=NONE)
    # little brass gallery plaque on the floor line under each case
    d.shape("rectangle", f"Case {idx} plaque", x=cx-24, y=704, width=48,
            height=14, fill=BRASS, stroke=INK, strokeWidth=2, radius=2)
    d.path(f"M{cx-14},{711} L{cx+14},{711}", f"Case {idx} plaque line",
           fill=NONE, stroke="#5E4416", strokeWidth=2, opacity=80)

def page_lines(x, y, w, h, dark, light, accent, idx):
    """The same test page: header, title, four body lines, footer rule."""
    d.shape("rectangle", f"Page {idx} header", x=x+10, y=y+12, width=w-20,
            height=18, fill=accent, stroke=NONE, radius=1)
    d.path(f"M{x+18},{y+21} L{x+w-36},{y+21}", f"Page {idx} h title",
           fill=NONE, stroke=light, strokeWidth=2, opacity=85)
    for j, ty in enumerate([y+48, y+64, y+80, y+96]):
        d.path(f"M{x+12},{ty} L{x+w-12},{ty}", f"Page {idx} line {j+1}",
               fill=NONE, stroke=dark, strokeWidth=3, opacity=80)
    d.path(f"M{x+12},{y+112} L{x+w-32},{y+112}", f"Page {idx} short",
           fill=NONE, stroke=dark, strokeWidth=3, opacity=70)
    d.path(f"M{x+10},{y+h-14} L{x+w-10},{y+h-14}", f"Page {idx} footer",
           fill=NONE, stroke=accent if isinstance(accent, str) else light,
           strokeWidth=2, opacity=70)

def dress_ledger(x, y, w, h, idx):
    # template one — the old ledger: parchment, double gilt rule, ink band
    d.shape("rectangle", f"Page {idx}", x=x, y=y, width=w, height=h,
            fill=PARCH, stroke=INK, strokeWidth=3, radius=2)
    d.shape("rectangle", f"Page {idx} gilt outer", x=x+5, y=y+5, width=w-10,
            height=h-10, fill=NONE, stroke="#B8924A", strokeWidth=2)
    d.shape("rectangle", f"Page {idx} gilt inner", x=x+9, y=y+9, width=w-18,
            height=h-18, fill=NONE, stroke="#B8924A", strokeWidth=1)
    page_lines(x, y, w, h, "#4A3A28", "#E8DCBE", "#2E2018", idx)

def dress_pale(x, y, w, h, idx):
    # template two — the pale minimal: white field, one hairline, air
    d.shape("rectangle", f"Page {idx}", x=x, y=y, width=w, height=h,
            fill=PALE, stroke="#9A968A", strokeWidth=1, radius=1)
    d.path(f"M{x+8},{y+40} L{x+w-8},{y+40}", f"Page {idx} hairline",
           fill=NONE, stroke="#B4B0A4", strokeWidth=1)
    page_lines(x, y, w, h, "#6E6A5E", "#F4F2EC", "#8A867A", idx)

def dress_night(x, y, w, h, idx):
    # template three — the night theme: dark page, gilt rule, pale type
    d.shape("rectangle", f"Page {idx}", x=x, y=y, width=w, height=h,
            fill=NIGHT, stroke=INK, strokeWidth=3, radius=2)
    d.shape("rectangle", f"Page {idx} frame", x=x+5, y=y+5, width=w-10,
            height=h-10, fill=NONE, stroke="#C89A4A", strokeWidth=1)
    page_lines(x, y, w, h, "#B8B2C4", "#2A2430", "#C89A4A", idx)

display_case(270, 1, dress_ledger)
display_case(505, 2, dress_pale)
display_case(740, 3, dress_night)

# --- captions ------------------------------------------------------------------
d.text("RC-SHOWCASE", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4D8DC", justify="center")
r = d.text("EVERY THEME, ON PARADE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AE98A8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-showcase-V1R00")
