#!/usr/bin/env python3
"""LIM-0446 Climate Cliff — limerick plate V1R00. The hardened wall splits
the plate: dry towers on the left under a hovering capital crown, the
neighborhood drowning on the right where rooftops poke through the flood
and a lifeboat collects its toll from a raised hand. Storm-green palette.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0446 Climate Cliff — Limerick Plate", 1000, 1000)

INK = "#20262A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D1418"}, {"offset": 1, "color": "#060B0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5E56"}, {"offset": 0.7, "color": "#2A3E38"},
    {"offset": 1, "color": "#121E1A"}]}}
WALL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A96A0"}, {"offset": 0.6, "color": "#5E6A74"},
    {"offset": 1, "color": "#38414A"}]}}
TOWER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5E66"}, {"offset": 1, "color": "#26333A"}]}}
WATER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A6E78"}, {"offset": 1, "color": "#16333C"}]}}
CLIFF = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9AA6B0"}, {"offset": 1, "color": "#5A646E"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2D27E"}, {"offset": 1, "color": "#C89A3E"}]}}
BOAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E09A58"}, {"offset": 1, "color": "#8A5230"}]}}
ICE = "#E8F0EA"
SOFT = "#A4C0B4"
AMBER = "#F0C878"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7EA89E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E8E0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(180, 190, 8), (830, 180, 7), (140, 400, 9),
                               (858, 420, 8), (390, 100, 7), (620, 100, 8),
                               (160, 620, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A5048", opacity=45, stroke=NONE)

# --- left: the protected side -----------------------------------------------------
# warm shaft of light falling on the hardened units
d.path("M230,150 L350,150 L395,740 L230,740 Z", "Dry light",
       fill="#E8D8A8", opacity=8, stroke=NONE)
d.shape("ellipse", "Dry ground", x=140, y=712, width=300, height=44,
        fill="#1A2824", opacity=85, stroke=NONE)
# protected towers, windows lit
d.shape("rectangle", "Tower 1", x=190, y=400, width=86, height=330,
        fill=TOWER, stroke=INK, strokeWidth=4)
d.path("M190,400 L276,400 L276,382 L190,382 Z", "Tower 1 roof",
       fill="#38454C", stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Tower 2", x=300, y=350, width=76, height=380,
        fill=TOWER, stroke=INK, strokeWidth=4)
d.path("M300,350 L376,350 L376,332 L300,332 Z", "Tower 2 roof",
       fill="#38454C", stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Low block", x=140, y=520, width=56, height=210,
        fill=TOWER, stroke=INK, strokeWidth=4)
for i, (wx, wy) in enumerate([(206, 424), (232, 424), (258, 424), (206, 468),
                              (232, 468), (258, 468), (206, 512), (258, 512),
                              (206, 556), (232, 556), (258, 600), (206, 644),
                              (316, 378), (342, 378), (316, 422), (342, 422),
                              (316, 466), (342, 466), (316, 510), (342, 554),
                              (316, 598), (342, 642), (152, 544), (168, 588),
                              (152, 632)]):
    d.shape("rectangle", f"Window {i+1}", x=wx, y=wy, width=14, height=18,
            fill=AMBER, opacity=75, stroke=NONE)
# the crown hovering over protected capital
d.shape("ellipse", "Crown glow", x=240, y=170, width=130, height=110,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F2D27E", "opacity": 0.25},
            {"offset": 1, "color": "#F2D27E", "opacity": 0}]}},
        stroke=NONE)
crown_ids = []
def crown_add(res):
    if res and res.get("id"):
        crown_ids.append(res["id"])
crown_add(d.path("M258,250 L258,212 L282,234 L304,204 L326,234 L350,212 "
                 "L350,250 Z", "Crown", fill=GOLD, stroke=INK,
                 strokeWidth=3.5, join="round"))
for i, cx in enumerate([266, 304, 342]):
    crown_add(d.shape("ellipse", f"Crown jewel {i+1}", x=cx - 4, y=228,
                      width=8, height=8, fill="#E86A5E", stroke=INK,
                      strokeWidth=1.5))
if crown_ids:
    d.call("transform", {"ids": crown_ids, "rotate": 6,
                         "origin": [304, 228]}, "tilt crown")
# coin glints trickling down toward the towers
for i, (cx, cy, op) in enumerate([(316, 296, 70), (286, 316, 55),
                                  (338, 322, 60), (306, 342, 45)]):
    d.shape("ellipse", f"Coin glint {i+1}", x=cx, y=cy, width=9,
            height=9, fill=GOLD, opacity=op, stroke=NONE)

# --- the wall, splitting the plate --------------------------------------------------
d.shape("rectangle", "Sea wall", x=436, y=330, width=92, height=480,
        fill=WALL, stroke=INK, strokeWidth=5)
# cap course + seams + bolts
d.shape("rectangle", "Wall cap", x=430, y=322, width=104, height=22,
        radius=4, fill="#9AA6B0", stroke=INK, strokeWidth=4)
for i, sy in enumerate([420, 510, 600, 690]):
    d.path(f"M436,{sy} L528,{sy}", f"Wall seam {i+1}", fill=NONE,
           stroke="#38414A", strokeWidth=3, opacity=60)
for i, (bx, by) in enumerate([(452, 372), (504, 372), (452, 452),
                              (504, 452), (452, 542), (504, 542),
                              (452, 632), (504, 632), (452, 722),
                              (504, 722)]):
    d.shape("ellipse", f"Bolt {i+1}", x=bx, y=by, width=9, height=9,
            fill="#38414A", opacity=80, stroke=NONE)
# placard on the dry face
plac_ids = []
def plac_add(res):
    if res and res.get("id"):
        plac_ids.append(res["id"])
plac_add(d.shape("rectangle", "Sector placard", x=448, y=560, width=68,
                 height=44, radius=4, fill="#E8E0CC", stroke=INK,
                 strokeWidth=3))
plac_add(d.text("SECTOR", "Placard 1", x=482, y=580, size=11,
                font="Virelai Sans", color="#3A4438", justify="center"))
plac_add(d.text("A-OK", "Placard 2", x=482, y=597, size=11,
                font="Virelai Sans", color="#3A4438", justify="center"))
# sandbags piled at the dry base
for i, (sx, sy, sw) in enumerate([(380, 762, 52), (330, 770, 46),
                                  (300, 736, 40), (352, 730, 44),
                                  (404, 736, 40)]):
    d.shape("ellipse", f"Sandbag {i+1}", x=sx, y=sy, width=sw, height=26,
            fill="#6E6A52", stroke=INK, strokeWidth=2.5, opacity=95)

# --- Cliff, tiny atop his wall ------------------------------------------------------
# concrete-block body
d.shape("rectangle", "Cliff body", x=452, y=250, width=60, height=74,
        radius=6, fill=CLIFF, stroke=INK, strokeWidth=4)
d.path("M482,250 L482,324", "Block seam", fill=NONE, stroke="#5A646E",
       strokeWidth=2, opacity=60)
# anxious eyes + flat mouth
d.shape("ellipse", "Cliff eye L", x=466, y=282, width=9, height=11,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Cliff eye R", x=490, y=282, width=9, height=11,
        fill=INK, stroke=NONE)
d.path("M470,308 Q482,302 494,308", "Cliff mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# hard hat
d.path("M450,254 C450,232 514,232 514,254 L514,258 L450,258 Z",
       "Hard hat", fill=GOLD, stroke=INK, strokeWidth=3.5, join="round")
d.path("M472,238 L472,252 M492,238 L492,252", "Hat ridges", fill=NONE,
       stroke="#C89A3E", strokeWidth=3, cap="round")
# arm gesturing down at the drowning side
d.path("M512,290 C538,300 556,318 564,340", "Cliff arm", fill=NONE,
       stroke="#5A646E", strokeWidth=13, cap="round")
d.shape("ellipse", "Cliff hand", x=556, y=334, width=18, height=18,
        fill="#9AA6B0", stroke=INK, strokeWidth=3)

# --- right: the drowning side --------------------------------------------------------
# rain slanting in over the flood zone
for i, (rx, ry) in enumerate([(560, 200), (610, 160), (660, 210),
                              (710, 170), (760, 200), (776, 176),
                              (590, 260), (640, 290), (700, 250),
                              (750, 280), (800, 240), (840, 290)]):
    d.path(f"M{rx},{ry} l-10,26", f"Rain {i+1}", fill=NONE,
           stroke="#6FB3C0", strokeWidth=2.5, opacity=35, cap="round")
# submerged rooftops poking through the waterline
d.path("M588,700 L588,624 L634,586 L680,624 L680,700 Z", "Drowned house 1",
       fill="#4A5C55", stroke=INK, strokeWidth=4, join="round")
d.path("M612,586 L612,560 L626,560 L626,580", "Chimney 1", fill="#4A5C55",
       stroke=INK, strokeWidth=3)
d.path("M634,586 L634,548 M624,556 L644,556", "Antenna", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.path("M748,724 L748,664 L798,630 L848,664 L848,724 Z",
       "Drowned house 2", fill="#43544E", stroke=INK, strokeWidth=4,
       join="round")
d.shape("ellipse", "Roof window", x=786, y=656, width=20, height=20,
        fill=AMBER, opacity=55, stroke=INK, strokeWidth=2)
# a raised hand out of the water, reaching for the boat
d.path("M560,690 C560,664 566,646 574,634 C570,622 574,610 582,608 "
       "C590,606 594,614 592,624 C596,616 604,616 606,624 C608,632 "
       "602,640 596,646 C590,656 588,672 588,690 Z",
       "Raised hand", fill="#8A94A0", stroke=INK, strokeWidth=3.5,
       join="round")
# flood water: scalloped surface, closed on the disc's own arc — no rim leak
d.path("M528,655 Q558,638 588,655 Q618,672 648,655 Q678,638 708,655 "
       "Q738,672 768,655 Q798,638 828,655 Q850,668 862,656 "
       "A420,420 0 0 1 604,848 L528,812 Z",
       "Flood", fill=WATER, opacity=88, stroke="#6FB3C0",
       strokeWidth=4, join="round")
# whitecaps + drifting debris
for i, (wx, wy, ww) in enumerate([(560, 656, 26), (660, 652, 30),
                                  (760, 654, 26), (830, 660, 22)]):
    d.path(f"M{wx},{wy} Q{wx + ww/2},{wy - 12} {wx + ww},{wy}",
           f"Whitecap {i+1}", fill=NONE, stroke="#BFE4E8", strokeWidth=3,
           opacity=70, cap="round")
d.shape("rectangle", "Debris plank", x=690, y=700, width=46, height=10,
        fill="#5A4A3A", opacity=80, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Debris float", x=810, y=716, width=20, height=12,
        fill="#5A4A3A", opacity=80, stroke=INK, strokeWidth=2)
# water lapping at the wall's wet base
d.path("M528,700 Q544,688 560,700 M528,720 Q546,708 564,720",
       "Wall lap", fill=NONE, stroke="#6FB3C0", strokeWidth=3.5,
       opacity=60, cap="round")

# --- the lifeboat, mid-water, charging ----------------------------------------------
boat_ids = []
def boat_add(res):
    if res and res.get("id"):
        boat_ids.append(res["id"])
# hull riding the waterline
boat_add(d.path("M640,600 L826,600 L800,652 L668,652 Z", "Boat hull",
                fill=BOAT, stroke=INK, strokeWidth=4, join="round"))
boat_add(d.path("M656,652 L800,652", "Waterline", fill=NONE,
                stroke="#6FB3C0", strokeWidth=4, opacity=70))
# cabin with the toll slot
boat_add(d.shape("rectangle", "Boat cabin", x=706, y=556, width=72,
                 height=46, radius=6, fill="#3E4A54", stroke=INK,
                 strokeWidth=4))
boat_add(d.shape("rectangle", "Toll slot", x=724, y=570, width=36,
                 height=18, radius=3, fill="#141C20", stroke=AMBER,
                 strokeWidth=2.5))
boat_add(d.text("TOLL", "Toll label", x=742, y=597, size=11,
                font="Virelai Sans", color=AMBER, justify="center"))
# a coin dropping toward the slot
boat_add(d.shape("ellipse", "Toll coin", x=735, y=536, width=14,
                 height=14, fill=GOLD, stroke=INK, strokeWidth=2))
boat_add(d.path("M758,542 C764,552 764,562 758,570", "Coin motion",
                fill=NONE, stroke=GOLD, strokeWidth=2, opacity=50))
# pennant on the bow — cheerful and indefensible
boat_add(d.path("M648,600 L648,562", "Flag pole", fill=NONE,
                stroke=INK, strokeWidth=3))
boat_add(d.path("M648,562 L682,571 L648,582 Z", "Flag", fill=AMBER,
                stroke=INK, strokeWidth=2))
if boat_ids:
    d.call("transform", {"ids": boat_ids, "rotate": 3,
                         "origin": [732, 626]}, "tilt boat")
# wake rings around the hull
d.path("M656,668 Q716,684 784,672 M622,682 Q716,706 816,686",
       "Wake", fill=NONE, stroke="#6FB3C0", strokeWidth=3, opacity=45,
       cap="round")

# --- name + key line + role ------------------------------------------------------
r = d.text("THE LIFEBOAT STILL CHARGES THE CALL", "Key line", x=500,
           y=899, size=22, font="Virelai Sans", color=SOFT,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=130)
d.text("CLIMATE CLIFF", "Name", x=500, y=945, size=56,
       font="Virelai Sans", color=ICE, justify="center")
r = d.text("SURVIVAL AS ASSET CLASS", "Role", x=500, y=977,
           size=19, font="Virelai Sans", color="#7A948A",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0446-climate-cliff-V1R00")
