#!/usr/bin/env python3
"""rc-pack.sh — The Embalmer. Necropolis plate V1R00.
A mortician's wrapping table: the rendered output lies on the slab half-wound
in tar-bandages, one pale corner of page still showing, while the great
canopic jar stands ready with its version tag and the niche shelf holds a
row of smaller jars — the exported JSON waiting their turn. Linen, glaze,
permanent ink. 1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Pack — Necropolis Plate", 1000, 1000)

INK = "#241A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#18100A"}, {"offset": 1, "color": "#0A0604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E4034"}, {"offset": 0.7, "color": "#2C231A"},
    {"offset": 1, "color": "#141009"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33291E"}, {"offset": 1, "color": "#161009"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6252"}, {"offset": 1, "color": "#3E362C"}]}}
STONE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E443A"}, {"offset": 1, "color": "#28221A"}]}}
LINEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8DCC0"}, {"offset": 1, "color": "#B8A87E"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A4A36"}, {"offset": 1, "color": "#2E2418"}]}}
JAR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8622E"}, {"offset": 1, "color": "#6E3416"}]}}
JAR_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A4A22"}, {"offset": 1, "color": "#4E2410"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D6B4"}, {"offset": 1, "color": "#B8A67E"}]}}
WAX = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A03228"}, {"offset": 1, "color": "#5C140F"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8B88E"}, {"offset": 1, "color": "#A8805C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6A50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD2BC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A5A44", opacity=35, stroke=NONE)
# faint wall seam across the crypt
d.path("M150,398 C350,390 650,390 850,398", "Wall seam", fill=NONE,
       stroke="#0E0A06", strokeWidth=4, opacity=35)

# --- wall niche: the row of exported JSON jars ---------------------------------
d.shape("ellipse", "Niche gloom", x=160, y=270, width=180, height=200,
        fill="#080503", opacity=50, stroke=NONE)
d.path("M165,385 L165,295 C165,258 195,238 230,238 C265,238 295,258 295,295 "
       "L295,385 Z", "Niche", fill="#0C0805", stroke="#2A2018", strokeWidth=4,
       join="round")
d.path("M152,385 L308,385 L308,398 L152,398 Z", "Niche ledge", fill=STONE_DK,
       stroke=INK, strokeWidth=3, join="round")
# three small jars waiting in a row, each tagged
def small_jar(cx, tag):
    d.path(f"M{cx-17},378 L{cx-17},330 C{cx-17},316 {cx-10},308 {cx-6},305 "
           f"L{cx-6},300 C{cx-11},295 {cx-11},286 {cx-5},282 C{cx-1},279 "
           f"{cx+1},279 {cx+5},282 C{cx+11},286 {cx+11},295 {cx+6},300 "
           f"L{cx+6},305 C{cx+10},308 {cx+17},316 {cx+17},330 L{cx+17},378 Z",
           f"{tag} jar", fill=JAR_DK, stroke=INK, strokeWidth=3, join="round")
    d.path(f"M{cx-14},340 C{cx-5},344 {cx+5},344 {cx+14},340", f"{tag} band",
           fill=NONE, stroke="#C8824A", strokeWidth=3, opacity=45)
    d.path(f"M{cx+4},306 C{cx+8},314 {cx+9},320 {cx+10},326", f"{tag} string",
           fill=NONE, stroke="#8A7454", strokeWidth=2)
    d.shape("rectangle", f"{tag} tag", x=cx+8, y=326, width=24, height=12,
            fill=PARCH, stroke=INK, strokeWidth=2, radius=2)
    d.text("json", f"{tag} tag text", x=cx+20, y=336, size=8,
           font="Source Sans 3", color="#2A1808", justify="center")

small_jar(192, "Niche jar 1")
small_jar(232, "Niche jar 2")
small_jar(272, "Niche jar 3")

# --- drying line: linen strips hanging from above --------------------------------
d.path("M468,170 C560,180 664,178 748,166", "Drying line", fill=NONE,
       stroke="#6A5A42", strokeWidth=3, opacity=85)
for i, (tx, ln) in enumerate([(502,88),(578,104),(652,80),(716,94)]):
    d.path(f"M{tx},{172+i%2} L{tx-5},{172+ln} C{tx-5},{176+ln} {tx+9},{178+ln} "
           f"{tx+9},{174+ln} L{tx+6},{174+i%2} Z", f"Hanging strip {i+1}",
           fill=LINEN, stroke="#8A7454", strokeWidth=2, opacity=90, join="round")
    d.path(f"M{tx+2},{180+i%2} L{tx},{168+ln}", f"Strip fold {i+1}", fill=NONE,
           stroke="#9A8862", strokeWidth=2, opacity=60)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0A08",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Table shadow", x=380, y=684, width=340, height=20,
        fill="#050302", opacity=55, stroke=NONE)
d.shape("ellipse", "Jar shadow", x=680, y=684, width=150, height=18,
        fill="#050302", opacity=55, stroke=NONE)
# a dropped coil of bandage on the floor
d.shape("ellipse", "Bandage coil", x=248, y=706, width=64, height=22,
        fill="#241C12", stroke="#A89878", strokeWidth=6)
d.path("M310,714 C330,718 346,716 358,710", "Coil tail", fill=NONE,
       stroke="#A89878", strokeWidth=5, cap="round")

# --- the wrapping table ---------------------------------------------------------
d.path("M405,578 L430,578 L430,695 L405,695 Z", "Table leg L", fill=STONE_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M640,578 L665,578 L665,695 L640,695 Z", "Table leg R", fill=STONE_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M378,545 L702,545 L702,578 L378,578 Z", "Slab", fill=STONE,
       stroke=INK, strokeWidth=5, join="round")
d.path("M384,552 L696,552", "Slab edge light", fill=NONE, stroke="#9A8E7A",
       strokeWidth=3, opacity=55)

# bowl of natron at the slab's near end
d.path("M392,546 C393,532 401,524 410,524 C419,524 427,532 428,546 Z",
       "Natron bowl", fill=STONE_DK, stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Natron salt", x=398, y=522, width=24, height=8,
        fill="#E8E0CC", opacity=85, stroke=NONE)

# --- the half-wound bundle: rendered output mid-embalming -------------------------
d.path("M470,550 C456,550 448,538 450,523 C452,507 465,498 482,497 L630,492 "
       "C652,491 666,503 667,521 C668,539 654,550 635,550 Z",
       "Bundle", fill=LINEN, stroke=INK, strokeWidth=5, join="round")
# the still-open corner: pale page of output showing
d.path("M470,548 C460,548 454,538 456,524 C458,512 468,503 482,501 L502,500 "
       "L502,549 L480,550 Z", "Open output", fill="#EFE6D0", stroke=INK,
       strokeWidth=3, join="round")
for i, ty in enumerate([514, 524, 534]):
    d.path(f"M463,{ty} L494,{ty-1}", f"Output line {i+1}", fill=NONE,
           stroke="#8A7E66", strokeWidth=2, opacity=85)
d.shape("rectangle", "Output thumb", x=466, y=504, width=18, height=8,
        fill="#C8B898", stroke="#8A7E66", strokeWidth=1, radius=1)
# tar-bandage wraps, wound diagonally over the rest
for i, (sx, yt, yb, col, op) in enumerate([
        (512,496,548,"#E8DCC0",95), (544,495,549,"#B8A87E",90),
        (576,494,549,"#E8DCC0",95), (608,493,549,"#B8A87E",90),
        (640,494,548,"#E8DCC0",95)]):
    d.path(f"M{sx},{yt} L{sx-18},{yb}", f"Wrap {i+1}", fill=NONE, stroke=col,
           strokeWidth=11, opacity=op)
# seam shading between wraps
d.path("M524,540 L640,536", "Wrap shadow", fill=NONE, stroke="#8A7454",
       strokeWidth=4, opacity=40)
# a loose strip end flopped over the slab's front edge
d.path("M560,548 C566,560 568,575 564,592", "Loose strip", fill=NONE,
       stroke="#D8CCA8", strokeWidth=9, cap="round")

# --- the embalmer, mid-wind ----------------------------------------------------
# boots
d.path("M292,684 L330,684 L330,694 L292,694 Z", "Boot L", fill="#1C1410",
       stroke=INK, strokeWidth=3, join="round")
d.path("M330,684 L368,684 L368,694 L330,694 Z", "Boot R", fill="#1C1410",
       stroke=INK, strokeWidth=3, join="round")
# robe
d.path("M296,482 C288,490 286,505 285,530 L280,688 L372,688 L366,528 "
       "C364,502 358,488 348,482 Z", "Robe", fill=ROBE, stroke=INK,
       strokeWidth=5, join="round")
# apron front panel
d.path("M310,514 L348,514 L354,686 L304,686 Z", "Apron", fill=LINEN,
       opacity=45, stroke="#8A7454", strokeWidth=2, join="round")
# head + linen coif
d.shape("ellipse", "Head", x=308, y=428, width=36, height=40,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M304,448 C302,424 316,411 328,411 C342,411 352,424 350,448 L344,444 "
       "C336,437 318,437 310,444 Z", "Coif", fill=LINEN, stroke=INK,
       strokeWidth=3, join="round")
d.path("M346,452 C352,464 354,476 351,488", "Coif tail", fill=NONE,
       stroke="#D8CCA8", strokeWidth=8, cap="round")
d.shape("ellipse", "Eye", x=332, y=446, width=5, height=5,
        fill="#241812", stroke=NONE)
# arms reaching to the roll
d.path("M340,505 C370,512 405,520 430,527", "Arm upper", fill=NONE,
       stroke="#4E4030", strokeWidth=12, cap="round")
d.path("M344,540 C375,546 405,543 430,537", "Arm lower", fill=NONE,
       stroke="#4E4030", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand upper", x=424, y=520, width=16, height=14,
        fill=SKIN, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand lower", x=425, y=531, width=16, height=14,
        fill=SKIN, stroke=INK, strokeWidth=3)
# the bandage roll in his hands
d.path("M434,515 L464,515 L464,545 L434,545 Z", "Bandage roll", fill=LINEN,
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Roll end", x=458, y=518, width=12, height=24,
        fill="#E8DCC0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Roll core", x=461, y=528, width=6, height=8,
        fill="#6A5A42", stroke=NONE)
# the strip feeding from roll to bundle
d.path("M462,524 C478,528 492,524 506,514", "Feed strip", fill=NONE,
       stroke="#E8DCC0", strokeWidth=6, cap="round")

# --- the great canopic jar, sealed and stamped ------------------------------------
d.path("M694,690 L694,560 C694,525 705,503 726,494 L726,486 C712,476 710,452 "
       "722,440 C734,428 766,428 778,440 C790,452 788,476 774,486 L774,494 "
       "C795,503 806,525 806,560 L806,690 Z", "Canopic jar", fill=JAR,
       stroke=INK, strokeWidth=5, join="round")
# glaze light + bands
d.path("M712,540 C710,580 710,640 714,678", "Glaze highlight", fill=NONE,
       stroke="#F0C090", strokeWidth=8, opacity=30, cap="round")
d.path("M700,548 C730,558 770,558 800,548", "Glaze band 1", fill=NONE,
       stroke="#E8A868", strokeWidth=4, opacity=40)
d.path("M698,606 C730,616 772,616 802,606", "Glaze band 2", fill=NONE,
       stroke="#E8A868", strokeWidth=4, opacity=35)
# lid seam + wax seal
d.path("M724,494 C740,500 762,500 776,494", "Lid seam", fill=NONE,
       stroke="#3E1E0E", strokeWidth=4, opacity=80)
d.shape("ellipse", "Wax seal", x=740, y=462, width=20, height=20,
        fill=WAX, stroke=INK, strokeWidth=3)
# the version tag in permanent ink — digits need Source Sans 3 (Virelai has none)
d.path("M748,494 C744,520 744,548 748,570", "Tag string", fill=NONE,
       stroke="#8A7454", strokeWidth=3)
d.shape("rectangle", "Version tag", x=722, y=570, width=56, height=30,
        fill=PARCH, stroke=INK, strokeWidth=3, radius=3)
d.text("2.4.1", "Version", x=750, y=591, size=15, font="Source Sans 3",
       color="#2A1808", justify="center")

# --- captions ------------------------------------------------------------------
d.text("RC-PACK", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8E0CE", justify="center")
r = d.text("EMBALMING THE OUTPUT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B0A488", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-pack-V1R00")
