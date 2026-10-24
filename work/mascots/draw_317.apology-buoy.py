#!/usr/bin/env python3
"""Apology Buoy — mascot portrait V1R00.
A brightly banded, hollow buoy riding the dark water at unaltered height over
the wreck it was deployed above. No tether; the dashed line below finds nothing.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Apology Buoy — Mascot Portrait", 1000, 1000)

INK = "#23211F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0B1E2A"}, {"offset": 1, "color": "#04090F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#31505E"}, {"offset": 0.7, "color": "#1E343E"},
    {"offset": 1, "color": "#0E1C24"}]}}
WATER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#24404E"}, {"offset": 1, "color": "#0A141C"}]}}
WATER_FRONT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16262E"}, {"offset": 1, "color": "#081018"}]}}
BUOY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4984A"}, {"offset": 0.65, "color": "#E06428"},
    {"offset": 1, "color": "#A83818"}]}}
BAND = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EEDA"}, {"offset": 1, "color": "#D8C9A8"}]}}
WRECK = "#122029"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7080", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BED6DE", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#28444E", opacity=45, stroke=NONE)

# faint mist streaks in the air above the water
for i, (x, y, w) in enumerate([(170,300,150),(620,250,190),(240,420,120),(660,380,150)]):
    d.shape("ellipse", f"Mist {i+1}", x=x, y=y, width=w, height=10,
            fill="#9FBEC8", opacity=8, stroke=NONE)

# --- wreckage on/under the water ------------------------------------------------
# half-sunk crate, right
d.path(rot_rect_path(715, 615, 130, 90, -18), "Sunken crate",
       fill=WRECK, stroke="#223840", strokeWidth=4)
d.path("M660,600 L766,560 M660,615 L772,575", "Crate slats", fill=NONE,
       stroke="#223840", strokeWidth=3, opacity=70)
# broken mast, left
d.path("M238,655 L262,448 L274,450 L256,655 Z", "Broken mast",
       fill=WRECK, stroke="#223840", strokeWidth=3, join="round")
d.path("M262,448 L252,420 M262,448 L278,424", "Mast splinters", fill=NONE,
       stroke="#223840", strokeWidth=3, cap="round")
# drifting plank
d.path(rot_rect_path(350, 640, 120, 22, 9), "Drift plank",
       fill=WRECK, stroke="#223840", strokeWidth=3)
# a lost shipping drum, mostly under
d.shape("ellipse", "Drum top", x=790, y=620, width=66, height=26,
        fill=WRECK, stroke="#223840", strokeWidth=3)
d.path("M790,633 L790,652 C800,664 846,664 856,652 L856,633",
       "Drum body", fill=WRECK, stroke="#223840", strokeWidth=3)

# --- the water itself ------------------------------------------------------------
d.path("M125,650 L875,650 A420,420 0 0 1 125,650 Z", "Sea", fill=WATER,
       stroke=NONE)
d.path("M125,650 L875,650", "Waterline", fill=NONE, stroke="#3E5E6C",
       strokeWidth=4, opacity=70)
# foreground swell, closing on the disc arc below
d.path("M178,730 L822,730 A420,420 0 0 1 178,730 Z", "Front swell",
       fill=WATER_FRONT, stroke=NONE, opacity=80)
# wave crest arcs on the surface
for i, (x, y, w) in enumerate([(200,652,60),(330,646,44),(560,648,52),
                               (680,654,40),(800,650,56),(430,660,38)]):
    d.path(f"M{x},{y} C{x+w*0.3},{y-9} {x+w*0.7},{y-9} {x+w},{y}",
           f"Crest {i+1}", fill=NONE, stroke="#7AA2B0", strokeWidth=3,
           cap="round", opacity=45)

# --- the apology buoy -------------------------------------------------------------
BX, BY = 500, 580   # ring centre, riding high on the waterline
# warm halo — the brightest thing in a dark sea
d.shape("ellipse", "Buoy halo", x=BX-150, y=BY-128, width=300, height=256,
        fill="#F4984A", opacity=10, stroke=NONE)
# soft reflection on the water
d.shape("ellipse", "Buoy reflection", x=424, y=664, width=170, height=24,
        fill="#E06428", opacity=18, stroke=NONE)
d.shape("ellipse", "Buoy shadow water", x=408, y=656, width=200, height=28,
        fill="#060D12", opacity=35, stroke=NONE)
# dashed line where a tether should be — it finds nothing
d.path("M500,690 L500,790", "No tether", fill=NONE, stroke="#5E8290",
       strokeWidth=3, dash=[2, 10], cap="round", opacity=30)
# ring: outer ellipse, slightly squashed for perspective
d.shape("ellipse", "Buoy ring", x=BX-118, y=BY-97, width=236, height=194,
        fill=BUOY, stroke=INK, strokeWidth=6)
# four white grab-straps over the ring, rotated about the centre
for i, deg in enumerate([0, 90, 45, -45]):
    d.path(rot_rect_path(BX, BY, 232, 38, deg), f"Band {i+1}",
           fill=BAND, stroke=INK, strokeWidth=4)
# hollow core — dark water shows straight through
d.shape("ellipse", "Buoy hollow", x=BX-58, y=BY-49, width=116, height=98,
        fill="#0C1A22", stroke=INK, strokeWidth=6)
d.shape("ellipse", "Hollow sheen", x=BX-44, y=BY-40, width=66, height=32,
        fill="#3A5A66", opacity=40, stroke=NONE)
# the whole message, chalked inside the hollow it can't fill
d.text("SORRY", "Sorry stencil", x=500, y=592, size=19,
       font="Virelai Sans", color="#E4D8B8", justify="center")
# wet sheen on the top-left of the ring
d.path("M412,528 C432,498 472,484 508,484 C474,492 442,510 424,538 Z",
       "Ring sheen", fill="#FADEC0", opacity=40, stroke=NONE)
# foam where the ring meets the water
for i, (x, y, w) in enumerate([(405,642,28),(450,652,20),(548,650,24),
                               (592,642,18)]):
    d.shape("ellipse", f"Foam {i+1}", x=x, y=y, width=w, height=w*0.5,
            fill="#CFE4E8", opacity=35, stroke=NONE)
# ripple rings spreading out
for i, (x, y, w) in enumerate([(380,668,90),(560,672,110),(330,676,60)]):
    d.path(f"M{x},{y} C{x+w*0.25},{y-8} {x+w*0.75},{y-8} {x+w},{y}",
           f"Ripple {i+1}", fill=NONE, stroke="#8AB4C0", strokeWidth=2.5,
           cap="round", opacity=35)

# --- captions ------------------------------------------------------------------
d.text("APOLOGY BUOY", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4DCC2", justify="center")
r = d.text("SURFACE STABILIZATION", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9DB8C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("317.apology-buoy-V1R00")
