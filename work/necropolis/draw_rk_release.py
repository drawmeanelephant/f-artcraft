#!/usr/bin/env python3
"""rc-release.sh — The Cortege. Necropolis plate V1R00.
A funeral procession out of the opened gates: four black-plumed pallbearers
shouldering the zip-sealed reliquary — the one canonical distribution —
while a bent bearer carries the deprecated multi-tier coffins off to a side
crypt marked NOT FOR RELEASE. Black plumage, archive linen, ceremony.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Release — Necropolis Plate", 1000, 1000)

INK = "#14181C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1214"}, {"offset": 1, "color": "#05070A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3C4A4E"}, {"offset": 0.7, "color": "#1E282C"},
    {"offset": 1, "color": "#0C1214"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3438"}, {"offset": 1, "color": "#10161A"}]}}
IRON = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A444A"}, {"offset": 1, "color": "#1A2126"}]}}
IRON_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3238"}, {"offset": 1, "color": "#141A1E"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#545E60"}, {"offset": 1, "color": "#2C3436"}]}}
STONE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4244"}, {"offset": 1, "color": "#1C2426"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C89A4E"}, {"offset": 1, "color": "#7A5424"}]}}
GOLD_LT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0B868"}, {"offset": 1, "color": "#9A6E30"}]}}
LINEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D8BC"}, {"offset": 1, "color": "#B8A87E"}]}}
BLACK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#262230"}, {"offset": 1, "color": "#100E16"}]}}
COFFIN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4438"}, {"offset": 1, "color": "#28221C"}]}}
WAX = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A03228"}, {"offset": 1, "color": "#5C140F"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D0AE84"}, {"offset": 1, "color": "#9A724F"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E6E72", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCD8D6", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#46565A", opacity=35, stroke=NONE)

# --- dead yew, left edge --------------------------------------------------------
d.path("M196,700 L190,505 C189,478 184,455 176,436 C190,452 198,470 202,492 "
       "C208,468 220,448 236,435 C222,458 214,482 212,505 L208,700 Z",
       "Yew trunk", fill="#1A2024", stroke="#0A0E10", strokeWidth=3, join="round")
d.path("M196,560 C180,545 166,538 152,534 M198,520 C212,502 226,492 242,488 "
       "M194,470 C184,452 174,442 162,436", "Yew branches", fill=NONE,
       stroke="#1A2024", strokeWidth=5, cap="round")

# --- the opened gates --------------------------------------------------------------
d.path("M305,198 L695,198 L695,222 L305,222 Z", "Lintel", fill=STONE_DK,
       stroke=INK, strokeWidth=4, join="round")
# carved roundel on the lintel
d.shape("ellipse", "Lintel roundel", x=484, y=196, width=32, height=32,
        fill=STONE, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Roundel eye L", x=492, y=206, width=5, height=6,
        fill="#14181C", stroke=NONE)
d.shape("ellipse", "Roundel eye R", x=503, y=206, width=5, height=6,
        fill="#14181C", stroke=NONE)
d.path("M496,217 L504,217", "Roundel mouth", fill=NONE, stroke="#14181C",
       strokeWidth=2)
# posts
for side, px in [("L", 318), ("R", 648)]:
    d.path(f"M{px},700 L{px},222 L{px+34},222 L{px+34},700 Z", f"Post {side}",
           fill=IRON, stroke=INK, strokeWidth=4, join="round")
# gate leaves swung open inward
d.path("M352,238 L448,286 L448,650 L352,700 Z", "Gate leaf L", fill=IRON_DK,
       opacity=85, stroke=INK, strokeWidth=4, join="round")
for t in (0.3, 0.6, 0.9):
    xt = 352 + 96*t; xb = 352 + 96*t
    d.path(f"M{xt:.0f},{238+48*t:.0f} L{xb:.0f},{700-50*t:.0f}",
           f"Leaf L bar {t}", fill=NONE, stroke="#0C1014", strokeWidth=6)
d.path("M352,460 L448,452", "Leaf L rail", fill=NONE, stroke="#0C1014",
       strokeWidth=6)
d.path("M648,238 L556,284 L556,648 L648,700 Z", "Gate leaf R", fill=IRON_DK,
       opacity=85, stroke=INK, strokeWidth=4, join="round")
for t in (0.3, 0.6, 0.9):
    xt = 648 - 92*t; xb = 648 - 92*t
    d.path(f"M{xt:.0f},{238+46*t:.0f} L{xb:.0f},{700-52*t:.0f}",
           f"Leaf R bar {t}", fill=NONE, stroke="#0C1014", strokeWidth=6)
d.path("M648,460 L556,450", "Leaf R rail", fill=NONE, stroke="#0C1014",
       strokeWidth=6)
# a crow keeping the ceremony on the left post
d.shape("ellipse", "Crow body", x=322, y=172, width=24, height=14,
        fill="#0C0A10", stroke=NONE)
d.shape("ellipse", "Crow head", x=340, y=166, width=11, height=11,
        fill="#0C0A10", stroke=NONE)
d.path("M349,170 L358,173 L349,176 Z", "Crow beak", fill="#0C0A10", stroke=NONE)
d.path("M322,179 L312,186 L324,184 Z", "Crow tail", fill="#0C0A10", stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080C0E",
       strokeWidth=4, opacity=70)

# --- the side crypt: NOT FOR RELEASE ------------------------------------------------
d.path("M712,480 L778,418 L844,480 Z", "Crypt pediment", fill=STONE,
       stroke=INK, strokeWidth=4, join="round")
d.path("M722,480 L834,480 L834,700 L722,700 Z", "Crypt body", fill=STONE_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M726,492 L736,492 L736,700 L726,700 Z M820,492 L830,492 L830,700 "
       "L820,700 Z", "Pilasters", fill=STONE, stroke=INK, strokeWidth=2,
       join="round")
d.path("M753,700 L753,578 C753,554 803,554 803,578 L803,700 Z", "Crypt door",
       fill="#0A0E10", stroke=INK, strokeWidth=4, join="round")
d.path("M766,580 L766,698 M790,580 L790,698", "Door bars", fill=NONE,
       stroke="#22282C", strokeWidth=4)
# the verdict plaque over the door — letters only, so Virelai is safe
d.path("M736,498 L820,498 L820,546 L736,546 Z", "Plaque", fill="#C8BFA6",
       stroke=INK, strokeWidth=3, join="round")
d.text("NOT FOR", "Plaque L1", x=778, y=522, size=13, font="Virelai Sans",
       color="#241E18", justify="center")
d.text("RELEASE", "Plaque L2", x=778, y=540, size=13, font="Virelai Sans",
       color="#241E18", justify="center")
d.shape("ellipse", "Crypt shadow", x=716, y=688, width=130, height=16,
        fill="#030608", opacity=55, stroke=NONE)

# --- the deprecated: a bent bearer carrying off the tiered coffins -------------------
# small stacked coffins riding his back
d.path("M670,520 L670,486 L682,468 L734,472 L742,488 L742,520 Z",
       "Tiered coffin 1", fill=COFFIN, stroke=INK, strokeWidth=4, join="round")
d.path("M676,468 L676,442 L686,428 L726,431 L732,444 L732,468 Z",
       "Tiered coffin 2", fill=COFFIN, stroke=INK, strokeWidth=4, join="round")
d.path("M682,468 L682,428 L688,420 L716,422 L720,432 L720,468 Z",
       "Tiered coffin 3", fill=COFFIN, stroke=INK, strokeWidth=4, join="round")
# the hunched bearer, head down, walking right
d.path("M694,560 C692,538 706,524 722,526 L740,566 L736,648 L704,648 Z",
       "Bearer hunch", fill=BLACK, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Bearer head", x=710, y=530, width=30, height=34,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M710,540 C708,524 738,522 738,542 L736,536 C730,530 718,530 714,536 Z",
       "Bearer cap", fill=BLACK, stroke=INK, strokeWidth=3, join="round")
d.path("M706,648 L700,692 M732,648 L742,692", "Bearer legs", fill=NONE,
       stroke="#0E0C12", strokeWidth=12, cap="round")
d.path("M690,686 L710,686 L710,696 L690,696 Z", "Bearer boot L",
       fill="#0C0A10", stroke=INK, strokeWidth=3, join="round")
d.path("M734,686 L754,686 L754,696 L734,696 Z", "Bearer boot R",
       fill="#0C0A10", stroke=INK, strokeWidth=3, join="round")

# --- the cortege: four pallbearers under the reliquary --------------------------------
d.shape("ellipse", "Cortege shadow", x=340, y=684, width=340, height=18,
        fill="#030608", opacity=55, stroke=NONE)

def pallbearer(x, i):
    # coat
    d.path(f"M{x-21},516 C{x-27},540 {x-25},580 {x-23},650 L{x+23},650 "
           f"C{x+25},580 {x+27},540 {x+21},516 Z", f"Bearer {i} coat",
           fill=BLACK, stroke=INK, strokeWidth=4, join="round")
    # legs mid-stride + boots
    d.path(f"M{x-13},652 L{x-22},690 M{x+13},652 L{x+24},690",
           f"Bearer {i} legs", fill=NONE, stroke="#0E0C12", strokeWidth=12,
           cap="round")
    d.path(f"M{x-32},684 L{x-12},684 L{x-12},694 L{x-32},694 Z",
           f"Bearer {i} boot B", fill="#0C0A10", stroke=INK, strokeWidth=3,
           join="round")
    d.path(f"M{x+14},684 L{x+34},684 L{x+34},694 L{x+14},694 Z",
           f"Bearer {i} boot F", fill="#0C0A10", stroke=INK, strokeWidth=3,
           join="round")
    # head tucked under the load, plumed cap
    d.shape("ellipse", f"Bearer {i} head", x=x-16, y=478, width=32, height=38,
            fill=SKIN, stroke=INK, strokeWidth=4)
    d.path(f"M{x-18},490 C{x-18},470 {x+18},470 {x+18},490 L{x+14},484 "
           f"C{x+8},478 {x-8},478 {x-14},484 Z", f"Bearer {i} cap",
           fill=BLACK, stroke=INK, strokeWidth=3, join="round")
    # arm raised to the pole
    d.path(f"M{x-16},528 C{x-26},514 {x-28},502 {x-24},492",
           f"Bearer {i} arm", fill=NONE, stroke="#1A1626", strokeWidth=10,
           cap="round")
    d.shape("ellipse", f"Bearer {i} hand", x=x-30, y=482, width=15, height=13,
            fill=SKIN, stroke=INK, strokeWidth=3)

for i, bx in enumerate([378, 460, 542, 624], start=1):
    pallbearer(bx, i)

# the carry pole across all four shoulders
d.path("M322,486 L678,486", "Carry pole", fill=NONE, stroke="#4A3820",
       strokeWidth=9, cap="round")

# --- the zip-sealed reliquary ---------------------------------------------------------
# body + arched lid
d.path("M336,486 L336,444 L664,444 L664,486 Z", "Reliquary body", fill=GOLD,
       stroke=INK, strokeWidth=5, join="round")
d.path("M336,444 C336,415 360,398 395,398 L605,398 C640,398 664,415 664,444 Z",
       "Reliquary lid", fill=GOLD_LT, stroke=INK, strokeWidth=5, join="round")
# archive linen straps around the chest
for i, sx in enumerate([404, 588]):
    d.path(f"M{sx},400 L{sx+12},400 L{sx+12},486 L{sx},486 Z",
           f"Linen strap {i+1}", fill=LINEN, opacity=90, stroke="#8A7454",
           strokeWidth=2, join="round")
    d.shape("ellipse", f"Strap knot {i+1}", x=sx+1, y=462, width=10, height=10,
            fill="#A89878", stroke="#8A7454", strokeWidth=2)
# the ZIP: a sealed track across the front face with its pull
d.path("M348,452 L652,452 M348,460 L652,460", "Zip tracks", fill=NONE,
       stroke="#54381A", strokeWidth=4)
for x in range(356, 652, 10):
    d.path(f"M{x},452 L{x},460", f"Zip tooth {x}", fill=NONE,
           stroke="#E0B868", strokeWidth=3)
d.path("M626,456 L642,456 L640,476 L630,476 Z", "Zip pull", fill=GOLD_LT,
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Pull hole", x=633, y=466, width=4, height=5,
        fill="#54381A", stroke=NONE)
# wax seal of the canonical registry
d.shape("ellipse", "Registry seal", x=442, y=458, width=18, height=18,
        fill=WAX, stroke=INK, strokeWidth=3)
# mourning plumes standing on the lid
for i, (px, sweep) in enumerate([(372, -14), (444, -8), (556, 8), (628, 14)]):
    d.path(f"M{px},398 C{px-12+sweep},380 {px-8+sweep},358 {px+6+sweep},348 "
           f"C{px+2+sweep},368 {px+8+sweep},384 {px+12},398 Z",
           f"Plume {i+1}", fill="#100E16", stroke="#262230", strokeWidth=2,
           join="round")

# --- captions ------------------------------------------------------------------
d.text("RC-RELEASE", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DFE6E4", justify="center")
r = d.text("THE CANONICAL RELIQUARY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A4B4B2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-release-V1R00")
