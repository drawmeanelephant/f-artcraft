#!/usr/bin/env python3
"""Care Coverage Wisp — mascot portrait V1R00.
A wisp assembled almost entirely of approach: translucent, hovering at
desk height beside a hunched silhouette, extending a hand of smoke that
brushes the shoulder. What she touches registers as temperature, not
weight — contact, later logged as care. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Care Coverage Wisp — Mascot Portrait", 1000, 1000)

INK = "#262038"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1E30"}, {"offset": 1, "color": "#0A0B16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E5E80"}, {"offset": 0.7, "color": "#323C5C"},
    {"offset": 1, "color": "#171C30"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C4462"}, {"offset": 1, "color": "#131830"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#54423A"}, {"offset": 1, "color": "#31241F"}]}}
WISP = "#C4D6F0"
WISP_HI = "#E8F1FC"
FIG = "#181226"
PAPER = "#E4DCC8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7C8AB0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6DEF2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(206,238,7),(804,240,8),(164,530,8),(836,552,7),
                               (258,764,8),(744,752,7),(144,398,6),(856,402,7),
                               (400,118,7),(608,116,8),(342,822,6),(666,818,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3C4870", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0818",
       strokeWidth=4, opacity=70)

# --- the desk, right side ----------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=630, y=692, width=200, height=26,
        fill="#060410", opacity=50, stroke=NONE)
d.shape("rectangle", "Desk leg L", x=618, y=596, width=18, height=104,
        fill=DESK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Desk leg R", x=818, y=596, width=18, height=104,
        fill=DESK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Desktop", x=584, y=576, width=300, height=22,
        radius=6, fill=DESK_GRAD, stroke=INK, strokeWidth=5)
# the check-in form and its unchecked line items — coverage, recorded
d.shape("rectangle", "Intake form", x=600, y=540, width=76, height=40,
        radius=3, fill=PAPER, stroke=INK, strokeWidth=3)
for i, y in enumerate([550, 560, 570]):
    d.path(f"M608,{y} L656,{y}", f"Form line {i+1}", fill=NONE,
           stroke="#8A8272", strokeWidth=2.5, opacity=80)
d.shape("rectangle", "Form checkbox", x=660, y=548, width=9, height=9,
        fill=NONE, stroke=INK, strokeWidth=2.5)
# mug of something long cold
d.shape("rectangle", "Mug", x=760, y=552, width=26, height=26,
        radius=5, fill="#5E5470", stroke=INK, strokeWidth=3)
d.path("M786,558 C796,560 796,570 786,572", "Mug handle", fill=NONE,
       stroke=INK, strokeWidth=3.5)

# --- the hunched silhouette at the desk ---------------------------------------------
# seated figure, head bowed over the work — the floor remains unchanged
d.shape("ellipse", "Figure shadow", x=640, y=690, width=180, height=22,
        fill="#060410", opacity=45, stroke=NONE)
d.path("M688,700 C676,660 672,620 688,590 C700,568 726,556 752,560 "
       "C786,566 806,592 812,626 C818,658 816,680 818,700 Z",
       "Figure body", fill=FIG, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Figure head", x=700, y=500, width=72, height=74,
        fill=FIG, stroke=INK, strokeWidth=5)
# cold rim where the light leans in from the wisp side
d.path("M692,592 C704,570 728,558 752,562", "Figure rim",
       fill=NONE, stroke="#6A7EA8", strokeWidth=4, cap="round", opacity=50)

# --- the wisp: approach, assembled ---------------------------------------------------
# hover shadow, slight and displaced — she does not rest on anything
d.shape("ellipse", "Wisp shadow", x=270, y=676, width=200, height=22,
        fill="#060410", opacity=30, stroke=NONE)
# ambient cold glow behind her
d.shape("ellipse", "Wisp glow", x=210, y=250, width=330, height=380,
        fill=WISP, opacity=8, stroke=NONE)
# trailing skirt: tapering curls of vapor below the body
d.path("M300,560 C280,600 296,632 280,660 C272,674 258,678 250,670 "
       "C244,662 252,652 262,654",
       "Wisp trail 1", fill=NONE, stroke=WISP, strokeWidth=9,
       cap="round", opacity=35)
d.path("M360,580 C352,616 366,646 354,670 C346,682 332,684 326,676 "
       "C322,668 330,660 338,662",
       "Wisp trail 2", fill=NONE, stroke=WISP, strokeWidth=7,
       cap="round", opacity=30)
# body: layered translucency, denser at the core
d.path("M300,300 C250,320 224,376 232,436 C240,506 276,560 330,578 "
       "C390,594 448,566 470,512 C492,458 480,394 446,352 "
       "C410,308 350,284 300,300 Z",
       "Wisp body", fill=WISP, stroke=NONE, opacity=26)
d.path("M312,330 C272,350 254,392 260,438 C268,496 296,540 340,554 "
       "C388,568 432,544 450,500 C468,454 458,404 430,368 "
       "C400,334 352,314 312,330 Z",
       "Wisp core", fill=WISP_HI, stroke=NONE, opacity=34)
# head suggestion: a lighter swell, two closed eyes — she witnesses
d.shape("ellipse", "Wisp head", x=290, y=278, width=140, height=120,
        fill=WISP_HI, opacity=30, stroke=NONE)
d.path("M322,352 C332,346 344,346 352,352", "Eye L", fill=NONE,
       stroke="#2A3050", strokeWidth=4, cap="round", opacity=45)
d.path("M378,352 C388,346 400,346 408,352", "Eye R", fill=NONE,
       stroke="#2A3050", strokeWidth=4, cap="round", opacity=45)
# rim of cold light along her lit edge
d.path("M296,306 C254,326 232,376 240,432 C246,486 272,534 312,560",
       "Wisp rim", fill=NONE, stroke=WISP_HI, strokeWidth=5,
       cap="round", opacity=55)

# --- the arm of smoke, extended but not gripping ------------------------------------
# a reach made of puffs, thinning as it crosses the desk air
for i, (cx, cy, r, op) in enumerate([(480,470,26,38),(530,484,22,34),
                                     (576,502,18,30),(622,522,15,26),
                                     (656,542,12,22)]):
    d.shape("ellipse", f"Arm puff {i+1}", x=cx-r, y=cy-r, width=2*r, height=2*r,
            fill=WISP, opacity=op, stroke=NONE)
d.path("M462,468 C530,486 600,514 658,542", "Arm thread", fill=NONE,
       stroke=WISP_HI, strokeWidth=6, cap="round", opacity=40)
# finger-hint curls at the tip — a hand that does not grip
d.path("M656,544 C674,548 688,556 696,566", "Finger 1", fill=NONE,
       stroke=WISP_HI, strokeWidth=4.5, cap="round", opacity=45)
d.path("M654,550 C668,560 676,570 678,580", "Finger 2", fill=NONE,
       stroke=WISP_HI, strokeWidth=4, cap="round", opacity=35)

# --- contact: the slight chill on the shoulder, later logged --------------------------
for i, (x, y, s) in enumerate([(704,572,9),(716,562,7),(694,582,6)]):
    d.path(f"M{x-s},{y} L{x+s},{y} M{x},{y-s} L{x},{y+s}", f"Chill {i+1}",
           fill=NONE, stroke=WISP_HI, strokeWidth=3, cap="round", opacity=75)

# --- captions ----------------------------------------------------------------------
d.text("CARE COVERAGE WISP", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DEE8F6", justify="center")
r = d.text("CONTACT, COUNTED AS CARE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FB0D4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("241.care-coverage-wisp-V1R00")
