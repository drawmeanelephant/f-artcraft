#!/usr/bin/env python3
"""Sriracha Sentinel — mascot portrait V1R00.
Crested sentinel on spire watch: arched window with night sky, shelves
of recipe jars singed by thermal bursts, chili-tipped spear and
flame-marked shield. 1000x1000. House style: gradients + translucency."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Sriracha Sentinel — Mascot Portrait", 1000, 1000)

INK = "#2E2024"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#120A0C"}, {"offset": 1, "color": "#060304"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A3E30"}, {"offset": 0.7, "color": "#4E2622"},
    {"offset": 1, "color": "#261312"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#463028"}, {"offset": 1, "color": "#1E1210"}]}}
SKY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16263E"}, {"offset": 1, "color": "#0A1018"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E4A42"}, {"offset": 1, "color": "#3A2A26"}]}}
SHELF = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A362A"}, {"offset": 1, "color": "#2A1C14"}]}}
JAR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9B087"}, {"offset": 1, "color": "#8A6E48"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EED9BC"}, {"offset": 0.7, "color": "#CFA982"},
    {"offset": 1, "color": "#A1764E"}]}}
STEEL_H = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6262"}, {"offset": 1, "color": "#443A3C"}]}}
SHIELD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A03E30"}, {"offset": 1, "color": "#5E2420"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#B05E44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0D0B8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,235,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E3028", opacity=45, stroke=NONE)

# --- arched spire window with night sky -------------------------------------------
d.path("M640,420 L640,230 C640,180 700,150 730,150 C760,150 820,180 820,230 L820,420 Z",
       "Window sky", fill=SKY, stroke=INK, strokeWidth=6)
d.path("M640,420 L640,230 C640,180 700,150 730,150 C760,150 820,180 820,230 L820,420",
       "Window frame", fill=NONE, stroke=INK, strokeWidth=8, join="round")
d.path("M730,152 L730,420 M640,300 L820,300", "Window mullions", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=85)
# moon + stars in the window
d.shape("ellipse", "Moon", x=672, y=200, width=44, height=44,
        fill="#E8DCC0", stroke=NONE, opacity=90)
d.shape("ellipse", "Moon shade", x=684, y=196, width=36, height=40,
        fill=SKY["gradient"]["stops"][0]["color"], stroke=NONE, opacity=85)
for i, (x, y, w) in enumerate([(756,215,5),(780,255,4),(660,325,4),(795,345,5),(700,255,3)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0E8D0", opacity=80, stroke=NONE)
# stone sill
d.shape("rectangle", "Window sill", x=622, y=418, width=216, height=22,
        fill=STONE, stroke=INK, strokeWidth=4, radius=4)

# --- storage shelves with recipe jars, top shelf singed ------------------------------
for i, sy in enumerate([300, 400, 500]):
    d.shape("rectangle", f"Shelf {i+1}", x=170, y=sy, width=160, height=16,
            fill=SHELF, stroke=INK, strokeWidth=4, radius=3)
    for j in range(3):
        jx = 182 + j*50
        d.shape("rectangle", f"Jar {i+1}{j+1}", x=jx, y=sy-44, width=34, height=44,
                fill=JAR, stroke=INK, strokeWidth=3, radius=5)
        d.shape("rectangle", f"Jar lid {i+1}{j+1}", x=jx+4, y=sy-52, width=26, height=10,
                fill="#5E3A2A", stroke=INK, strokeWidth=2, radius=3)
        d.shape("rectangle", f"Jar label {i+1}{j+1}", x=jx+7, y=sy-30, width=20, height=14,
                fill="#E8DCC0", stroke="#6E5C3C", strokeWidth=1)
# charred edge on the top shelf + embers + smoke
d.path("M170,300 L330,300 L330,310 C300,306 290,314 260,310 C230,306 210,318 170,312 Z",
       "Singe mark", fill="#14100C", stroke=NONE, opacity=85)
for i, (x, y, w, o) in enumerate([(200,296,7,90),(248,293,6,80),(300,295,8,85),(222,290,4,70)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8722E", opacity=o, stroke=NONE)
d.path("M235,280 C228,255 240,240 232,215", "Smoke wisp", fill=NONE,
       stroke="#8A8078", strokeWidth=4, cap="round", opacity=30)

# --- floor ---------------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR, stroke=NONE)
d.shape("ellipse", "Sentinel shadow", x=440, y=676, width=190, height=30,
        fill="#0A0505", opacity=55, stroke=NONE)

# --- chili-tipped spear ------------------------------------------------------------------
d.path("M668,330 L668,682", "Spear shaft", fill=NONE, stroke="#5E3E28",
       strokeWidth=9, cap="round")
d.path("M668,330 C660,300 668,278 692,272 C680,290 680,310 690,330 "
       "C680,336 672,336 668,330 Z",
       "Chili tip", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#D9482E"}, {"offset": 1, "color": "#8A1E16"}]}},
       stroke=INK, strokeWidth=3, join="round")
d.path("M688,278 C690,268 696,264 704,264", "Chili stem", fill=NONE,
       stroke="#5E8A4A", strokeWidth=5, cap="round")

# --- the sentinel -------------------------------------------------------------------------
# legs + shoes
d.path("M505,650 L500,684", "Leg L", fill=NONE, stroke="#A1764E",
       strokeWidth=13, cap="round")
d.path("M555,650 L560,684", "Leg R", fill=NONE, stroke="#966E46",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Shoe L", x=484, y=678, width=32, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=548, y=678, width=32, height=15, fill=INK, stroke=NONE)
# body
d.path("M530,455 C595,455 628,502 624,558 C620,622 586,658 530,658 "
       "C474,658 442,622 438,558 C434,502 465,455 530,455 Z",
       "Sentinel body", fill=BODY, stroke=INK, strokeWidth=6)
# chest sash: crossed guard strap
d.path("M470,548 C486,596 505,630 530,652 C555,630 574,596 590,548 "
       "C570,562 490,562 470,548 Z",
       "Guard sash", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#6E3A30"}, {"offset": 1, "color": "#46201C"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.path("M470,548 L590,548", "Sash top", fill=NONE, stroke="#C9A03E",
       strokeWidth=3, opacity=70)
# helmet dome + nose guard + rooster plume
d.path("M478,470 L478,442 C478,418 500,406 530,406 C560,406 582,418 582,442 L582,470 Z",
       "Helmet", fill=STEEL_H, stroke=INK, strokeWidth=5, join="round")
d.path("M486,412 C510,368 562,356 600,378 C566,380 528,392 502,420 Z",
       "Rooster plume", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#D9482E"}, {"offset": 1, "color": "#8A1E16"}]}},
       stroke=INK, strokeWidth=3, join="round")
d.path("M526,470 L526,492 L534,492 L534,470 Z", "Nose guard",
       fill=STEEL_H, stroke=INK, strokeWidth=3)
# stern face: flat lids, level mouth
d.shape("ellipse", "Eye L", x=498, y=504, width=14, height=16, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=548, y=504, width=14, height=16, fill=INK, stroke=NONE)
d.path("M496,500 L514,500 M546,500 L564,500", "Lids", fill=NONE,
       stroke="#B98E62", strokeWidth=4, cap="round")
d.path("M494,488 L512,486 M546,486 L564,488", "Brows flat", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M512,540 L548,540", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# right hand gripping the spear
d.path("M600,556 C626,556 648,548 662,540", "Arm spear", fill=NONE,
       stroke="#CFA982", strokeWidth=12, cap="round")
d.shape("ellipse", "Grip hand", x=654, y=530, width=20, height=18,
        fill="#EED9BC", stroke=INK, strokeWidth=3)
# left arm + round shield with flame
d.path("M462,556 C432,568 418,590 420,612", "Arm shield", fill=NONE,
       stroke="#C9A87E", strokeWidth=12, cap="round")
d.shape("ellipse", "Shield", x=380, y=586, width=92, height=104,
        fill=SHIELD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Shield rim", x=390, y=596, width=72, height=84,
        fill=NONE, stroke="#C9A03E", strokeWidth=3, opacity=80)
d.path("M426,646 C416,634 416,620 426,610 C424,620 432,624 430,632 "
       "C438,626 438,618 436,610 C444,620 444,636 426,646 Z",
       "Shield flame", fill="#E8722E", stroke="#B0451E", strokeWidth=2)

# --- captions ---------------------------------------------------------------------------
d.text("SRIRACHA SENTINEL", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0D0B8", justify="center")
r = d.text("SPICE GUARDIAN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C98E72", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("214.sriracha-sentinel-V1R00")
