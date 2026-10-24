#!/usr/bin/env python3
"""rc-scan.sh — The Census of the Dead. Necropolis plate V1R00.
A census-taker with a great ledger walks between the graves at night,
comparing names — a flag planted on every orphan that exists in the ledger
but not in the ground, another on every unmarked dig: missing, orphaned,
digest mismatched. Ledger black and flag red.
1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-Scan — Necropolis Plate", 1000, 1000)

INK = "#13151C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0D1017"}, {"offset": 1, "color": "#060810"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4654"}, {"offset": 0.7, "color": "#1E242E"},
    {"offset": 1, "color": "#0E1218"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2F38"}, {"offset": 1, "color": "#10131A"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E7680"}, {"offset": 1, "color": "#3E434B"}]}}
STONE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E545E"}, {"offset": 1, "color": "#262B33"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3648"}, {"offset": 1, "color": "#1C1A26"}]}}
LEDGER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2118"}, {"offset": 1, "color": "#120D08"}]}}
PAGES = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8CCAE"}, {"offset": 1, "color": "#A89878"}]}}
FLAG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B03A2E"}, {"offset": 1, "color": "#7E241C"}]}}
MOON = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0ECD8"}, {"offset": 1, "color": "#B8B29A"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C0A078"}, {"offset": 1, "color": "#8A6644"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E5866", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C2CC", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A545E", opacity=35, stroke=NONE)

# --- night sky: moon, stars, mist -------------------------------------------------
d.shape("ellipse", "Moon glow", x=170, y=130, width=180, height=180,
        fill="#E8E4D0", opacity=10, stroke=NONE)
d.shape("ellipse", "Moon", x=200, y=158, width=120, height=120,
        fill=MOON, stroke=NONE)
d.shape("ellipse", "Moon mare 1", x=228, y=188, width=30, height=22,
        fill="#9A947E", opacity=45, stroke=NONE)
d.shape("ellipse", "Moon mare 2", x=268, y=216, width=20, height=14,
        fill="#9A947E", opacity=40, stroke=NONE)
for i, (x, y, w) in enumerate([(620,180,4),(700,240,3),(560,150,3),
                               (760,320,4),(480,200,3),(840,200,3)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8DCE4", opacity=55, stroke=NONE)
d.path("M170,470 C300,458 420,466 540,458", "Ground mist", fill=NONE,
       stroke="#7A8494", strokeWidth=10, opacity=12, cap="round")

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#05070B",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Graves shadow", x=190, y=690, width=330, height=14,
        fill="#020306", opacity=55, stroke=NONE)
d.shape("ellipse", "Taker shadow", x=610, y=690, width=170, height=16,
        fill="#020306", opacity=55, stroke=NONE)

# --- the graves ----------------------------------------------------------------------
def flag(x, label, h=64):
    d.path(f"M{x},{700-h} L{x},700", f"{label} pole", fill=NONE,
           stroke="#3A3F47", strokeWidth=4, cap="round")
    d.path(f"M{x},{700-h} L{x+34},{700-h+9} L{x},{700-h+18} Z", label,
           fill=FLAG, stroke=INK, strokeWidth=3, join="round")

# stone 1: plain rounded, name weathered off
d.path("M185,700 L185,600 C185,578 200,566 218,566 C236,566 251,578 251,600 "
       "L251,700 Z", "Stone 1", fill=STONE, stroke=INK, strokeWidth=4,
       join="round")
d.path("M197,612 L239,612 M199,628 L237,628", "Stone 1 name", fill=NONE,
       stroke="#2E333B", strokeWidth=3, opacity=60)
# stone 2: cross-topped, flagged — in the ledger but nameless here
d.path("M288,700 L288,562 L298,562 L298,546 L290,546 L290,534 L298,534 "
       "L298,516 L316,516 L316,534 L324,534 L324,546 L316,546 L316,562 "
       "L330,562 L330,700 Z", "Stone 2", fill=STONE_DK, stroke=INK,
       strokeWidth=4, join="round")
flag(338, "Flag 2")
# stone 3: leaning hard, long past keeping
d.path(rot_rect_path(432, 634, 62, 132, -14), "Stone 3", fill=STONE_DK,
       opacity=85, stroke=INK, strokeWidth=4, join="round")
d.path(rot_rect_path(432, 620, 36, 4, -14), "Stone 3 mark", fill="#2E333B",
       opacity=60, stroke=NONE, join="round")
# an unmarked dig: bare mound, flagged — in the ground but not the ledger
d.path("M500,700 C506,672 540,660 578,664 C604,668 618,682 620,700 Z",
       "Unmarked dig", fill=STONE_DK, stroke=INK, strokeWidth=4,
       join="round")
for i, (x, y, w) in enumerate([(530,676,9),(560,670,7),(592,682,8)]):
    d.shape("ellipse", f"Mound clod {i+1}", x=x, y=y, width=w, height=w,
            fill="#20242C", opacity=70, stroke=NONE)
flag(586, "Flag 3")
# stone 4: low stub behind the mound, flagged on its far side
d.path("M468,700 L468,652 C468,640 476,634 486,634 C496,634 504,640 504,652 "
       "L504,700 Z", "Stone 4", fill=STONE_DK, opacity=80, stroke=INK,
       strokeWidth=3, join="round")
flag(250, "Flag 1")
# night grass
for i, (x0, y0, x1, y1) in enumerate([(170,700,166,690),(262,700,264,690),
                                      (400,700,396,688),(640,700,644,690),
                                      (830,700,828,692)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Grass {i+1}", fill=NONE,
           stroke="#39424E", strokeWidth=3, cap="round", opacity=70)

# --- the census-taker -------------------------------------------------------------------
# walking left, ledger held toward the graves, quill mid-tally
# boots
d.path("M648,688 L684,688 L684,698 L648,698 Z", "Boot rear", fill="#0E0C10",
       stroke=INK, strokeWidth=3, join="round")
d.path("M700,684 L734,684 L738,696 L702,696 Z", "Boot front", fill="#0E0C10",
       stroke=INK, strokeWidth=3, join="round")
# robe, hem kicked by the stride
d.path("M640,690 C634,620 640,540 656,480 C664,448 682,434 706,434 "
       "C730,434 746,450 750,482 C758,548 758,624 752,690 L712,690 "
       "C700,668 692,648 690,628 L686,690 Z", "Robe", fill=ROBE,
       stroke=INK, strokeWidth=5, join="round")
# robe folds
for i, (x0, x1) in enumerate([(666,662),(700,698),(728,724)]):
    d.path(f"M{x0},500 C{x0+4},560 {x1-4},620 {x1},682", f"Fold {i+1}",
           fill=NONE, stroke="#12101A", strokeWidth=3, opacity=55)
# head + census hat
d.shape("ellipse", "Head", x=680, y=388, width=48, height=50,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M674,404 C670,384 684,368 704,368 C724,368 736,384 732,404 Z",
       "Hat crown", fill=ROBE, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Hat brim", x=656, y=398, width=96, height=16,
        fill=ROBE, stroke=INK, strokeWidth=4)
# one eye on the graves
d.shape("ellipse", "Eye", x=686, y=420, width=6, height=6,
        fill="#241A12", stroke=NONE)
# left arm out, presenting the ledger to the row
d.path("M664,494 C630,500 600,514 580,534", "Arm L", fill=NONE,
       stroke="#322E40", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand L", x=566, y=528, width=20, height=16,
        fill=SKIN, stroke=INK, strokeWidth=3)
# the great ledger: black cover, open pages, names in faint columns
d.path("M462,538 L562,506 L572,566 L472,598 Z", "Ledger pages",
       fill=PAGES, stroke=INK, strokeWidth=4, join="round")
d.path("M458,542 L562,508 L562,516 L460,550 Z M458,542 L472,598 "
       "L472,606 L456,548 Z", "Ledger cover", fill=LEDGER, stroke=INK,
       strokeWidth=3, join="round")
d.path("M517,522 L527,568", "Ledger spine", fill=NONE, stroke=INK,
       strokeWidth=3)
for i, t in enumerate([0.25, 0.45, 0.65]):
    x0 = 480 + 34 * t
    d.path(f"M{478+int(30*t)},{544-int(10*t)} L{506+int(30*t)},{534-int(10*t)}",
           f"Names L {i+1}", fill=NONE, stroke="#7A6C50", strokeWidth=2,
           opacity=70)
    d.path(f"M{530+int(28*t)},{524-int(10*t)} L{556+int(10*t)},{514-int(6*t)}",
           f"Names R {i+1}", fill=NONE, stroke="#7A6C50", strokeWidth=2,
           opacity=70)
# right arm raised, quill mid-tally
d.path("M744,486 C762,470 770,450 766,430", "Arm R", fill=NONE,
       stroke="#322E40", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand R", x=754, y=420, width=18, height=16,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.path("M766,424 L788,392", "Quill", fill=NONE, stroke="#C8CBD0",
       strokeWidth=4, cap="round")
d.path("M782,400 C790,388 800,384 806,388 C800,398 792,404 784,406 Z",
       "Quill feather", fill="#C8CBD0", opacity=85, stroke=INK,
       strokeWidth=2, join="round")
# lantern at the belt — the only warm thing out here
d.shape("ellipse", "Lantern glow", x=706, y=560, width=90, height=90,
        fill="#F0C868", opacity=14, stroke=NONE)
d.path("M734,548 L748,548 L748,584 L734,584 Z", "Lantern", fill=LEDGER,
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Lantern flame", x=738, y=560, width=6, height=12,
        fill="#F0C868", opacity=90, stroke=NONE)
d.path("M734,548 C734,540 748,540 748,548", "Lantern bail", fill=NONE,
       stroke=INK, strokeWidth=2)

# --- captions ------------------------------------------------------------------
d.text("RC-SCAN", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#D6DCE4", justify="center")
r = d.text("CENSUS OF THE DEAD", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#96A0AC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-scan-V1R00")
