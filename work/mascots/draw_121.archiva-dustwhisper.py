#!/usr/bin/env python3
"""Archiva Dustwhisper — mascot portrait V1R00.
The archive matriarch dusting ancient ledgers by lanternlight beside a
wide card catalog. 1000x1000. House style: gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Archiva Dustwhisper — Mascot Portrait", 1000, 1000)

INK = "#2E2226"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16121E"}, {"offset": 1, "color": "#08060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A3E52"}, {"offset": 0.7, "color": "#2E2536"},
    {"offset": 1, "color": "#15101C"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5636"}, {"offset": 1, "color": "#4A321E"}]}}
WOOD_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E422A"}, {"offset": 1, "color": "#382416"}]}}
SHAWL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5268"}, {"offset": 1, "color": "#463248"}]}}
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0DDBC"}, {"offset": 0.7, "color": "#D4B88E"},
    {"offset": 1, "color": "#A98862"}]}}
LEDGER_A = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4A3A"}, {"offset": 1, "color": "#462C22"}]}}
LEDGER_B = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A4A66"}, {"offset": 1, "color": "#3A2E44"}]}}
LEDGER_C = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5A50"}, {"offset": 1, "color": "#2E3C34"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C09A58"}, {"offset": 1, "color": "#7E5E30"}]}}
LAMP = "#F0B860"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A5A74", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCCFE4", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#443A50", opacity=45, stroke=NONE)

# faint shelf ghosts across the upper plate — the archive goes on forever
for i, y in enumerate((150, 205, 260)):
    d.path(f"M160,{y} L380,{y}", f"Ghost shelf L{i+1}", fill=NONE,
           stroke="#55486A", strokeWidth=7, opacity=28, cap="round")
    d.path(f"M620,{y} L840,{y}", f"Ghost shelf R{i+1}", fill=NONE,
           stroke="#55486A", strokeWidth=7, opacity=28, cap="round")

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=690, width=660, height=115,
        fill="#1C1626", opacity=85, stroke=NONE)
d.shape("ellipse", "Ledger shadow", x=215, y=712, width=170, height=30,
        fill="#070510", opacity=55, stroke=NONE)
d.shape("ellipse", "Archiva shadow", x=350, y=724, width=230, height=34,
        fill="#070510", opacity=55, stroke=NONE)
d.shape("ellipse", "Catalog shadow", x=580, y=716, width=260, height=32,
        fill="#070510", opacity=55, stroke=NONE)

# --- card catalog, wide and a little tired ---------------------------------------
d.shape("rectangle", "Catalog body", x=575, y=395, width=255, height=325,
        fill=WOOD, stroke=INK, strokeWidth=6, radius=8)
d.shape("rectangle", "Catalog top", x=565, y=380, width=275, height=24,
        fill=WOOD_DK, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Catalog base", x=568, y=712, width=269, height=18,
        fill=WOOD_DK, stroke=INK, strokeWidth=4, radius=4)
# drawer grid: 3 x 4 with tiny label frames and brass pulls
for r in range(4):
    for c in range(3):
        x = 590 + c*76
        y = 416 + r*72
        d.shape("rectangle", f"Drawer {r+1}-{c+1}", x=x, y=y, width=64, height=60,
                fill=WOOD_DK, stroke=INK, strokeWidth=3, radius=3)
        d.shape("rectangle", f"Label {r+1}-{c+1}", x=x+10, y=y+8, width=44, height=16,
                fill="#D8C9A4", stroke=INK, strokeWidth=2, radius=2)
        d.shape("ellipse", f"Pull {r+1}-{c+1}", x=x+24, y=y+34, width=16, height=9,
                fill=BRASS, stroke=INK, strokeWidth=2)
# one drawer left ajar — a misfiled card peeking out
d.path("M666,488 L730,480 L730,540 L666,548 Z", "Drawer ajar",
       fill=WOOD, stroke=INK, strokeWidth=4, join="round")
d.path("M688,470 L722,466 L722,486 L688,490 Z", "Misfiled card",
       fill="#E4D6B4", stroke=INK, strokeWidth=2)
# dust on the catalog top
d.shape("ellipse", "Top dust", x=585, y=374, width=235, height=14,
        fill="#B9A8C0", opacity=22, stroke=NONE)

# --- stack of ancient ledgers, lower left ------------------------------------------
d.path(rot_rect_path(298, 700, 168, 34, -2), "Ledger bottom",
       fill=LEDGER_C, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(292, 668, 152, 32, 3), "Ledger middle",
       fill=LEDGER_B, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(300, 636, 136, 30, -4), "Ledger top",
       fill=LEDGER_A, stroke=INK, strokeWidth=5, join="round")
# page blocks showing at the fore-edge of each
d.path(rot_rect_path(360, 700, 20, 26, -2), "Pages bottom",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(354, 668, 20, 24, 3), "Pages middle",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(358, 636, 18, 22, -4), "Pages top",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
# dust layer on the top ledger
d.shape("ellipse", "Ledger dust", x=252, y=612, width=104, height=16,
        fill="#CBBCD4", opacity=30, stroke=NONE)
# bookmark ribbon trailing out of the middle ledger
d.path("M228,676 C222,700 226,718 218,734", "Bookmark tail", fill=NONE,
       stroke="#A23E46", strokeWidth=6, cap="round")

# --- hanging lantern, upper left, the warm heart of the piece -----------------------
d.path("M330,64 L330,138", "Lantern chain", fill=NONE, stroke="#6A5A74",
       strokeWidth=4, dash=[8,7], cap="round")
d.shape("ellipse", "Lantern glow wide", x=170, y=140, width=330, height=290,
        fill=LAMP, opacity=10, stroke=NONE)
d.shape("ellipse", "Lantern glow tight", x=255, y=155, width=160, height=150,
        fill=LAMP, opacity=16, stroke=NONE)
d.shape("rectangle", "Lantern cap", x=312, y=136, width=36, height=14,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=4)
d.path("M306,150 L354,150 L364,216 L296,216 Z", "Lantern cage",
       fill="#3A2E1E", stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Lantern flame glow", x=316, y=162, width=28, height=44,
        fill=LAMP, opacity=85, stroke=NONE)
d.path("M330,196 C324,184 326,172 330,164 C334,172 336,184 330,196 Z",
       "Lantern flame", fill="#F8E2A8", stroke=NONE)
d.shape("rectangle", "Lantern base", x=300, y=214, width=60, height=12,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=4)

# --- Archiva herself: the matriarch in her shawl --------------------------------------
# body: a draped shawl bell from shoulders to hem
d.path("M436,420 C500,414 540,470 548,560 C554,640 546,700 534,726 "
       "L352,726 C340,700 332,640 338,560 C346,470 386,414 436,420 Z",
       "Shawl", fill=SHAWL, stroke=INK, strokeWidth=6)
# shawl hem fringe
d.path("M356,726 L366,742 M392,726 L398,742 M430,726 L434,742 "
       "M468,726 L470,742 M504,726 L500,742 M530,724 L524,738",
       "Fringe", fill=NONE, stroke="#463248", strokeWidth=6, cap="round")
# shawl trim band
d.path("M342,640 C380,656 500,656 544,640", "Shawl trim", fill=NONE,
       stroke="#8A6E88", strokeWidth=9, opacity=70, cap="round")
# collar / brooch where the shawl closes
d.shape("ellipse", "Brooch", x=430, y=452, width=26, height=22,
        fill=BRASS, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Brooch gem", x=437, y=457, width=12, height=12,
        fill="#7E94B4", stroke=INK, strokeWidth=2)
# head
d.shape("ellipse", "Head", x=392, y=320, width=106, height=98,
        fill=FACE, stroke=INK, strokeWidth=6)
# hair bun + wisp
d.shape("ellipse", "Bun", x=420, y=292, width=50, height=34,
        fill="#5E4A56", stroke=INK, strokeWidth=5)
d.path("M402,338 C398,318 410,308 424,308", "Hair L", fill=NONE,
       stroke="#5E4A56", strokeWidth=8, cap="round")
d.path("M486,338 C490,318 480,308 466,308", "Hair R", fill=NONE,
       stroke="#5E4A56", strokeWidth=8, cap="round")
# half-moon glasses on a chain
d.shape("ellipse", "Lens L", x=404, y=352, width=30, height=26,
        fill="#F4E4C8", opacity=35, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lens R", x=456, y=352, width=30, height=26,
        fill="#F4E4C8", opacity=35, stroke=INK, strokeWidth=4)
d.path("M434,364 L456,364", "Glasses bridge", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M486,368 C496,392 492,414 484,432", "Glasses chain", fill=NONE,
       stroke="#8A744E", strokeWidth=3, opacity=80)
# eyes behind the lenses — kindly, half-lidded
d.shape("ellipse", "Eye L", x=414, y=360, width=9, height=11, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=466, y=360, width=9, height=11, fill=INK, stroke=NONE)
d.path("M408,352 L430,350", "Lid L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M460,350 L482,352", "Lid R", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# cheeks + gentle smile
d.shape("ellipse", "Cheek L", x=398, y=384, width=24, height=13,
        fill="#B46A5E", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=466, y=384, width=24, height=13,
        fill="#B46A5E", opacity=40, stroke=NONE)
d.path("M428,398 C438,406 452,406 460,398", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# left arm cradling an index card, right arm raised with the feather duster
d.path("M380,520 C360,540 352,560 356,580", "Arm L", fill=NONE,
       stroke="#5E4A56", strokeWidth=15, cap="round")
d.shape("ellipse", "Hand L", x=350, y=574, width=20, height=17,
        fill="#D4B88E", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(386, 590, 52, 34, -8), "Index card",
       fill="#E4D6B4", stroke=INK, strokeWidth=3)
d.path("M368,584 L404,580 M368,594 L402,590", "Card lines", fill=NONE,
       stroke="#8A744E", strokeWidth=2, opacity=80)
d.path("M520,500 C552,478 566,458 572,438", "Arm R", fill=NONE,
       stroke="#5E4A56", strokeWidth=15, cap="round")
d.shape("ellipse", "Hand R", x=562, y=426, width=20, height=17,
        fill="#D4B88E", stroke=INK, strokeWidth=3)
# feather duster: stubby handle, wide plume brushing dust off the catalog top
d.path("M574,434 L622,392", "Duster handle", fill=NONE, stroke="#8A744E",
       strokeWidth=7, cap="round")
d.path("M622,392 C600,392 578,380 574,360 C596,366 608,370 616,376 "
       "C606,358 606,338 620,326 C628,346 636,358 642,366 "
       "C648,348 662,338 678,340 C668,360 664,372 662,382 "
       "C676,374 692,374 700,384 C684,398 654,400 622,392 Z",
       "Duster plume", fill="#B99AC0", stroke=INK, strokeWidth=4,
       join="round", opacity=95)
for i, (x1, y1, x2, y2) in enumerate([(606,378,586,364),(622,368,612,344),
                                    (644,372,648,348),(660,380,678,368)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Plume barb {i+1}", fill=NONE,
           stroke="#8E7196", strokeWidth=3, cap="round", opacity=80)
# dust kicked up where the plume meets the catalog top
d.shape("ellipse", "Dust puff", x=570, y=330, width=95, height=60,
        fill="#CBBCD4", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(566,318,7),(606,306,5),(640,296,6),
                               (700,316,5),(590,352,6),(660,336,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#CBBCD4", opacity=50, stroke=NONE)
d.path("M560,392 L588,378 M566,404 L596,396", "Dust streaks", fill=NONE,
       stroke="#CBBCD4", strokeWidth=3, opacity=35, cap="round")

# --- captions ---------------------------------------------------------------------------
d.text("ARCHIVA DUSTWHISPER", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E4D8EC", justify="center")
r = d.text("EVERY FRAGMENT HAS A PLACE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A898B8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("121.archiva-dustwhisper-V1R00")
