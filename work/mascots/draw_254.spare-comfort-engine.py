#!/usr/bin/env python3
"""Spare Comfort Engine — mascot portrait V1R00.
A small boiler engine humming beside a wall exhaust vent, a duct carrying
its warmth away; from a front slot it prints an endless receipt with a
little heart on it. The sincerity gauge reads low. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Spare Comfort Engine — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1008"}, {"offset": 1, "color": "#0A0604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A6A4E"}, {"offset": 0.7, "color": "#5E4430"},
    {"offset": 1, "color": "#332418"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A28"}, {"offset": 1, "color": "#221610"}]}}
ENGINE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D89A5E"}, {"offset": 0.7, "color": "#A86E3E"},
    {"offset": 1, "color": "#7A4A28"}]}}
STACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5632"}, {"offset": 1, "color": "#5E3A20"}]}}
DUCT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A6A52"}, {"offset": 1, "color": "#4E4234"}]}}
VENT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5C44"}, {"offset": 1, "color": "#3E3226"}]}}
DIAL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E4CC"}, {"offset": 1, "color": "#C4B090"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#B08A62", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCBC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4832", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140C08",
       strokeWidth=4, opacity=70)

# --- exhaust vent on the wall, upper right ----------------------------------------
d.shape("rectangle", "Vent frame", x=690, y=240, width=150, height=88,
        fill=VENT_GRAD, stroke=INK, strokeWidth=5, radius=10)
for i, y in enumerate([256, 272, 288, 304]):
    d.path(f"M704,{y} L826,{y}", f"Vent slat {i+1}", fill=NONE,
           stroke="#241C12", strokeWidth=5, opacity=85)
for i, (x, y) in enumerate([(700,250),(700,318),(830,250),(830,318)]):
    d.shape("ellipse", f"Vent screw {i+1}", x=x, y=y, width=7, height=7,
            fill="#2C241A", stroke=NONE)
# warmth waves rising off the vent
for i, x in enumerate([722, 765, 808]):
    d.path(f"M{x},236 C{x-7},222 {x+7},212 {x},198 C{x-7},184 {x+6},176 {x},166",
           f"Vent wave {i+1}", fill=NONE, stroke="#F0B86A", strokeWidth=4,
           cap="round", opacity=55-i*13)

# --- duct from the engine to the vent ----------------------------------------------
d.path("M610,478 C650,464 672,436 682,398 L696,334", "Duct", fill=NONE,
       stroke=DUCT_GRAD, strokeWidth=30, cap="round")
d.path("M610,478 C650,464 670,438 680,402", "Duct sheen", fill=NONE,
       stroke="#A8946E", strokeWidth=8, cap="round", opacity=50)
d.path("M652,452 L638,438 M676,404 L658,394", "Duct bands", fill=NONE,
       stroke="#3A2E20", strokeWidth=5, opacity=80)

# --- the engine: a little boiler, idling warm --------------------------------------
d.shape("ellipse", "Engine halo", x=290, y=380, width=400, height=340,
        fill="#F0B06A", opacity=10, stroke=NONE)
d.shape("ellipse", "Engine shadow", x=345, y=684, width=290, height=22,
        fill="#0E0806", opacity=45, stroke=NONE)
# stack + cap
d.shape("rectangle", "Stack", x=450, y=378, width=30, height=56,
        fill=STACK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Stack cap", x=442, y=370, width=46, height=14,
        fill=STACK_GRAD, stroke=INK, strokeWidth=4, radius=5)
# warm puffs from the stack
for i, (x, y, w, o) in enumerate([(452,340,26,40),(470,306,34,30),(452,272,42,20)]):
    d.shape("ellipse", f"Puff {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#E8C898", opacity=o, stroke=NONE)
# boiler body
d.path("M370,690 L370,510 C370,452 415,425 488,425 C561,425 605,452 605,510 "
       "L605,690 Z", "Boiler", fill=ENGINE_GRAD, stroke=INK, strokeWidth=6)
# top sheen + belly shade
d.shape("ellipse", "Boiler sheen", x=395, y=442, width=130, height=46,
        fill="#FFFFFF", opacity=16, stroke=NONE)
d.path("M385,640 C430,664 550,664 595,640 L600,690 L375,690 Z",
       "Belly shade", fill="#6E3E20", opacity=35, stroke=NONE)
# rivet seam
d.path("M378,498 L600,498", "Seam", fill=NONE, stroke="#6E4526",
       strokeWidth=3, opacity=60)
for i, x in enumerate(range(392, 596, 28)):
    d.shape("ellipse", f"Rivet {i+1}", x=x, y=493, width=8, height=8,
            fill="#8A5A34", stroke="#5A3520", strokeWidth=1.5)
# feet
for x in [405, 545]:
    d.shape("rectangle", f"Foot {x}", x=x, y=686, width=36, height=20,
            fill="#5E3A20", stroke=INK, strokeWidth=4, radius=7)

# --- face: the hum ------------------------------------------------------------------
d.path("M420,536 C428,542 438,542 446,536 M530,536 C538,542 548,542 556,536",
       "Closed eyes", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M480,566 C488,572 496,572 504,566 C510,562 516,562 522,566",
       "Hum mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# a little hum note drifting off, on the open side away from the duct
d.path("M370,545 C352,538 344,526 342,510", "Hum wave", fill=NONE,
       stroke="#F0C08A", strokeWidth=4, cap="round", opacity=60)
d.path(rot_rect_path(334, 494, 22, 14, -18), "Hum note head",
       fill="#F0C08A", opacity=80, stroke=NONE)
d.path("M344,488 L344,458 C352,462 356,468 357,476", "Hum note stem",
       fill=NONE, stroke="#F0C08A", strokeWidth=3.5, cap="round", opacity=80)

# --- the sincerity gauge: needle parked low -----------------------------------------
d.shape("ellipse", "Gauge rim", x=398, y=592, width=68, height=68,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Gauge face", x=405, y=599, width=54, height=54,
        fill=DIAL_GRAD, stroke="#6E5638", strokeWidth=3)
for i, (x1, y1, x2, y2) in enumerate([(414,630,420,630),(418,612,423,617),
                                     (447,608,445,614)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Tick {i+1}", fill=NONE,
           stroke="#6E5638", strokeWidth=3, cap="round")
d.path("M432,626 L416,640", "Needle", fill=NONE, stroke="#8A3A2A",
       strokeWidth=4.5, cap="round")
d.shape("ellipse", "Needle hub", x=427, y=621, width=10, height=10,
        fill="#8A3A2A", stroke=NONE)

# --- the receipt slot + the endless warmth receipt -----------------------------------
d.shape("rectangle", "Receipt slot", x=492, y=606, width=86, height=16,
        fill="#241A10", stroke=INK, strokeWidth=3.5, radius=6)
d.path("M535,622 C535,646 512,656 516,678 C519,694 536,702 552,696",
       "Receipt strip", fill=NONE, stroke="#F2E8D8", strokeWidth=26,
       cap="round")
d.path("M522,642 L548,642", "Receipt print", fill=NONE, stroke="#9A8E76",
       strokeWidth=4, opacity=80)
# a little heart printed on the hanging end
d.path("M540,672 C536,666 528,668 528,675 C528,681 540,688 540,688 "
       "C540,688 552,681 552,675 C552,668 544,666 540,672 Z",
       "Receipt heart", fill="#B86A5A", stroke=NONE)
# a spent receipt already on the floor
d.path(rot_rect_path(610, 690, 66, 26, 7), "Fallen receipt",
       fill="#E4D8C2", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(600, 684, 20, 6, 7), "Fallen print", fill=NONE,
       stroke="#9A8E76", strokeWidth=3, opacity=80)

# --- stray warmth motes ---------------------------------------------------------------
for i, (x, y, w) in enumerate([(330,430,6),(660,430,5),(300,540,5),(690,520,6),
                               (250,620,6),(740,620,5),(560,320,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0C898", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("SPARE COMFORT ENGINE", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#F0E2CE", justify="center")
r = d.text("ISSUER OF WARMTH RECEIPTS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A884", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("254.spare-comfort-engine-V1R00")
