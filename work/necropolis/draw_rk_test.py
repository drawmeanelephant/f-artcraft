#!/usr/bin/env python3
"""rc-test.sh — The Three Trials. Necropolis plate V1R00.
Three test plots dug side by side in three different landscape styles —
crypt, busy, sterile — an inspector with a very long checklist walking the
row, multi-pass, verifying each fixture grave before the whole suite is
allowed to rest. Clipboard, spade, three flags.
1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-Test — Necropolis Plate", 1000, 1000)

INK = "#201C10"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121108"}, {"offset": 1, "color": "#070705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#484A36"}, {"offset": 0.7, "color": "#222418"},
    {"offset": 1, "color": "#101108"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33301F"}, {"offset": 1, "color": "#14120A"}]}}
SOIL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E5038"}, {"offset": 1, "color": "#302617"}]}}
PIT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A140B"}, {"offset": 1, "color": "#060402"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#736C58"}, {"offset": 1, "color": "#403A2C"}]}}
STONE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#544E40"}, {"offset": 1, "color": "#28241A"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46402E"}, {"offset": 1, "color": "#1E1A10"}]}}
FLAG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8482E"}, {"offset": 1, "color": "#7E241C"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAE0C4"}, {"offset": 1, "color": "#BDB08A"}]}}
WEED = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E7040"}, {"offset": 1, "color": "#2E3A1E"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C9A87E"}, {"offset": 1, "color": "#8E6B48"}]}}
BOARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5C42"}, {"offset": 1, "color": "#3A2C1C"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9AA0A8"}, {"offset": 1, "color": "#4E545C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A6A50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCCAB0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#565838", opacity=35, stroke=NONE)

# --- crypt wall + night air -----------------------------------------------------
d.path("M150,370 C350,362 650,362 850,370", "Wall seam", fill=NONE,
       stroke="#0A0904", strokeWidth=4, opacity=40)
d.path("M170,300 C300,290 420,296 540,288", "Mist", fill=NONE,
       stroke="#8A8E78", strokeWidth=10, opacity=10, cap="round")
for i, (x, y, w) in enumerate([(300,240,4),(520,220,3),(680,250,3),
                               (430,430,4),(460,470,3)]):
    d.shape("ellipse", f"Firefly {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E48A", opacity=50, stroke=NONE)

# --- the dead tree behind the row, limbs reaching over the plots -------------------
d.path("M338,702 C336,640 334,576 348,512", "Tree trunk", fill=NONE,
       stroke="#17130C", strokeWidth=13, cap="round")
d.path("M348,512 C352,548 344,606 340,650", "Trunk light", fill=NONE,
       stroke="#3E3626", strokeWidth=4, opacity=45, cap="round")
d.path("M346,560 C380,540 412,514 438,478", "Limb R1", fill=NONE,
       stroke="#17130C", strokeWidth=7, cap="round")
d.path("M438,478 C452,462 468,452 484,448", "Twig R1a", fill=NONE,
       stroke="#17130C", strokeWidth=3, cap="round")
d.path("M438,478 C436,460 442,444 452,432", "Twig R1b", fill=NONE,
       stroke="#17130C", strokeWidth=3, cap="round")
d.path("M344,538 C316,516 292,496 268,464", "Limb L1", fill=NONE,
       stroke="#17130C", strokeWidth=7, cap="round")
d.path("M268,464 C252,452 238,448 224,446", "Twig L1a", fill=NONE,
       stroke="#17130C", strokeWidth=3, cap="round")
d.path("M268,464 C262,446 262,432 268,418", "Twig L1b", fill=NONE,
       stroke="#17130C", strokeWidth=3, cap="round")
d.path("M348,512 C352,490 350,466 342,444", "Limb top", fill=NONE,
       stroke="#17130C", strokeWidth=5, cap="round")
# an owl keeping the score on the right limb
d.shape("ellipse", "Owl body", x=452, y=444, width=22, height=30,
        fill="#17130C", stroke=NONE)
d.path("M454,448 L452,440 L460,444 M468,444 L474,440 L472,448",
       "Owl ears", fill=NONE, stroke="#17130C", strokeWidth=3, cap="round",
       join="round")
d.shape("ellipse", "Owl eye L", x=458, y=452, width=4, height=4,
        fill="#C8C49A", opacity=80, stroke=NONE)
d.shape("ellipse", "Owl eye R", x=466, y=452, width=4, height=4,
        fill="#C8C49A", opacity=80, stroke=NONE)
# roots gripping the floor line
d.path("M330,700 C322,694 314,692 306,694 M350,700 C358,694 366,692 374,694",
       "Roots", fill=NONE, stroke="#17130C", strokeWidth=4, cap="round")

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0804",
       strokeWidth=4, opacity=70)

def flag(x, label, h=66):
    d.path(f"M{x},{700-h} L{x},700", f"{label} pole", fill=NONE,
           stroke="#3A3628", strokeWidth=4, cap="round")
    d.path(f"M{x},{700-h} L{x+32},{700-h+9} L{x},{700-h+18} Z", label,
           fill=FLAG, stroke=INK, strokeWidth=3, join="round")

def pit(cx, label, skew=0):
    """Dug plot: spoil heap on the floor line, dark open cut in front."""
    # spoil mound behind
    d.path(f"M{cx-60},702 C{cx-54},668 {cx-22},650 {cx+8},652 "
           f"C{cx+42},654 {cx+58},674 {cx+60},702 Z", f"{label} heap",
           fill=SOIL, stroke=INK, strokeWidth=4, join="round")
    for i, (ox, oy, w) in enumerate([(-32,-34,9),(0,-42,7),(30,-28,8)]):
        d.shape("ellipse", f"{label} clod {i+1}", x=cx+ox, y=700+oy,
                width=w, height=w, fill="#241C10", opacity=70, stroke=NONE)
    # the open cut, drawn flat into the floor band
    d.path(f"M{cx-58+skew},706 L{cx+58+skew},706 L{cx+44+skew},760 "
           f"L{cx-44+skew},760 Z", f"{label} cut", fill=PIT, stroke=INK,
           strokeWidth=4, join="round")
    # cut rim light on the near edge + depth shading inside
    d.path(f"M{cx-58+skew},706 L{cx+58+skew},706", f"{label} rim",
           fill=NONE, stroke="#6E5F42", strokeWidth=3, opacity=70)
    d.path(f"M{cx-40+skew},726 L{cx+40+skew},726", f"{label} shade",
           fill=NONE, stroke="#020202", strokeWidth=6, opacity=50)

# --- plot 1: the crypt fixture — kerbed, headstoned, fenced ------------------------
pit(245, "Crypt plot")
# stone kerb frame around the cut: four rails leaving the opening bare
d.path("M177,702 L313,702 L295,712 L195,712 Z", "Kerb back", fill=STONE,
       stroke=INK, strokeWidth=3, join="round")
d.path("M177,702 L195,712 L205,754 L195,766 Z", "Kerb left", fill=STONE_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M313,702 L295,766 L285,754 L295,712 Z", "Kerb right", fill=STONE_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M195,766 L295,766 L285,754 L205,754 Z", "Kerb front", fill=STONE,
       stroke=INK, strokeWidth=3, join="round")
# gothic headstone behind the heap
d.path("M222,664 L222,548 C222,524 238,510 254,510 C270,510 284,524 284,548 "
       "L284,664 Z", "Crypt headstone", fill=STONE_DK, stroke=INK,
       strokeWidth=4, join="round")
d.path("M234,566 L272,566 M234,582 L272,582 M238,598 L268,598",
       "Headstone lines", fill=NONE, stroke="#2E2A20", strokeWidth=3,
       opacity=60)
# wrought-iron spikes behind the stone
for i, fx in enumerate([196, 208, 298, 310]):
    d.path(f"M{fx},700 L{fx},{644- (i%2)*10}", f"Iron spike {i+1}", fill=NONE,
           stroke="#1C1A12", strokeWidth=3, cap="round")
    d.path(f"M{fx-3},{646-(i%2)*10} L{fx},{638-(i%2)*10} "
           f"L{fx+3},{646-(i%2)*10}", f"Iron tip {i+1}", fill=NONE,
           stroke="#1C1A12", strokeWidth=3)
flag(300, "Crypt flag")

# --- plot 2: the busy fixture — overgrown, cluttered ------------------------------
pit(440, "Busy plot", skew=6)
# weeds and tufts all over the heap
for i, (x0, x1) in enumerate([(386,382),(404,408),(468,472),(488,484),
                              (424,420),(452,458)]):
    d.path(f"M{x0},700 C{x0-4},688 {x1+2},682 {x1},674", f"Weed {i+1}",
           fill=NONE, stroke="#4E6034", strokeWidth=3, cap="round")
# mushrooms on the heap's shoulder
d.path("M396,668 C396,658 414,658 414,668 Z", "Mushroom 1 cap", fill="#8A4A34",
       stroke=INK, strokeWidth=2)
d.path("M402,668 L408,668 L408,680 L402,680 Z", "Mushroom 1 stem",
       fill=PARCH, stroke=INK, strokeWidth=2)
d.path("M468,674 C468,666 482,666 482,674 Z", "Mushroom 2 cap", fill="#8A4A34",
       stroke=INK, strokeWidth=2)
d.path("M472,674 L478,674 L478,682 L472,682 Z", "Mushroom 2 stem",
       fill=PARCH, stroke=INK, strokeWidth=2)
# a leaning plank jammed into the heap
d.path(rot_rect_path(508, 618, 15, 108, 24), "Leaning plank", fill=STONE_DK,
       stroke=INK, strokeWidth=3, join="round")
# a trowel dropped in the spoil
d.path("M436,676 L460,668", "Trowel handle", fill=NONE, stroke="#5A4230",
       strokeWidth=4, cap="round")
d.path("M460,668 L474,664 L470,678 L456,680 Z", "Trowel blade", fill=STEEL,
       stroke=INK, strokeWidth=2, join="round")
flag(500, "Busy flag")

# --- plot 3: the sterile fixture — surveyed, stringed, level -----------------------
pit(635, "Sterile plot")
# survey pegs + taut string rectangle around the cut
pegs = [(575, 668), (695, 668), (585, 700), (685, 700)]
for i, (px, py) in enumerate(pegs):
    d.path(f"M{px},{py} L{px},{py+22}", f"Peg {i+1}", fill=NONE,
           stroke="#E4E0D0", strokeWidth=4, cap="round")
d.path("M575,672 L695,672 M585,696 L685,696 M577,672 L587,696 M693,672 "
       "L683,696", "String frame", fill=NONE, stroke="#D8D4C4", strokeWidth=1,
       opacity=80)
# a level laid across the front rim
d.path(rot_rect_path(638, 764, 96, 10, -3), "Level", fill=STONE_DK,
       stroke=INK, strokeWidth=2, join="round")
d.shape("ellipse", "Level bubble", x=634, y=760, width=10, height=6,
        fill="#B8D8A0", opacity=80, stroke=INK, strokeWidth=1)
flag(690, "Sterile flag")

# --- the inspector at the row's end, checklist unrolled to the floor ----------------
# boots
d.path("M742,686 L774,686 L774,696 L742,696 Z", "Boot L", fill="#141008",
       stroke=INK, strokeWidth=3, join="round")
d.path("M784,686 L816,686 L816,696 L784,696 Z", "Boot R", fill="#141008",
       stroke=INK, strokeWidth=3, join="round")
# robe, facing left down the row
d.path("M732,692 C730,624 736,546 750,494 C758,462 774,444 794,444 "
       "C814,444 828,464 832,496 C838,550 840,626 836,692 Z",
       "Robe", fill=ROBE, stroke=INK, strokeWidth=5, join="round")
for i, x in enumerate([758, 786, 812]):
    d.path(f"M{x},506 C{x+2},570 {x-2},636 {x},686", f"Fold {i+1}",
           fill=NONE, stroke="#141008", strokeWidth=3, opacity=50)
# head + peaked cap
d.shape("ellipse", "Head", x=772, y=384, width=42, height=46,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M770,404 C766,382 782,368 798,368 C814,368 824,384 820,404 "
       "C810,394 782,394 770,404 Z", "Cap crown", fill=ROBE, stroke=INK,
       strokeWidth=3, join="round")
d.path("M768,402 L754,406 C752,401 756,397 762,396 L770,396 Z",
       "Cap peak", fill="#2A2416", stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Eye", x=777, y=410, width=5, height=5,
        fill="#241812", stroke=NONE)
# spade over the right shoulder: haft up past the head, blade catching light
d.path("M810,470 C822,450 832,430 838,408", "Spade haft", fill=NONE,
       stroke="#5A4230", strokeWidth=5, cap="round")
d.path("M830,410 C828,392 834,378 844,372 C854,378 858,392 854,408 "
       "C848,416 836,418 830,410 Z", "Spade blade", fill=STEEL, stroke=INK,
       strokeWidth=3, join="round")
# left arm out to the clipboard
d.path("M756,496 C734,504 714,516 698,530", "Arm L", fill=NONE,
       stroke="#3A3424", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand L", x=686, y=528, width=16, height=14,
        fill=SKIN, stroke=INK, strokeWidth=3)
# the clipboard
d.path(rot_rect_path(668, 512, 56, 70, -10), "Clipboard", fill=BOARD,
       stroke=INK, strokeWidth=4, join="round")
d.path(rot_rect_path(664, 508, 44, 56, -10), "Clip sheet", fill=PARCH,
       stroke=INK, strokeWidth=2, join="round")
for i, (x0, y0, x1, y1) in enumerate([(652,492,680,487),(648,506,676,501),
                                      (644,520,672,515)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Clip line {i+1}", fill=NONE,
           stroke="#8A7A58", strokeWidth=2, opacity=80)
# the very long checklist: unrolls off the board, sags, pools on the floor
d.path("M650,540 C628,560 610,586 604,616 C598,648 606,676 630,690 "
       "C654,702 690,702 716,696", "Checklist", fill=NONE, stroke="#E8DCBC",
       strokeWidth=14, cap="round")
# check marks running down the strip — multi-pass, multi-tick
for i, (tx, ty) in enumerate([(634,568),(616,600),(608,634),(618,664),
                              (644,684),(676,690)]):
    d.path(f"M{tx},{ty} l4,5 l7,-9", f"Check {i+1}", fill=NONE,
           stroke="#5E7040", strokeWidth=2, cap="round", join="round")
# the strip's far end curls
d.path("M716,696 C736,690 748,680 750,668", "Checklist curl", fill=NONE,
       stroke="#E8DCBC", strokeWidth=10, cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-TEST", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E0DCC8", justify="center")
r = d.text("THREE FIXTURES, ONE VERDICT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8A68C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-test-V1R00")
