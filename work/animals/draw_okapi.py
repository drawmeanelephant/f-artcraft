#!/usr/bin/env python3
"""Okapi — field-guide plate V1R00. Head/bust portrait: dark velvety face,
white muzzle, big ears, ossicones, striped chest nod to the famous legs.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; every accent was checked to land inside."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Okapi — Field Plate", 1000, 1000)

INK = "#3A2417"          # deep warm umber, not black
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241611"}, {"offset": 1, "color": "#100906"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E3C2"}, {"offset": 0.7, "color": "#D9C49A"},
    {"offset": 1, "color": "#B08F60"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E4428"}, {"offset": 0.65, "color": "#4E2E19"},
    {"offset": 1, "color": "#32190C"}]}}
NECK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E2E19"}, {"offset": 1, "color": "#2E1709"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A3520"}, {"offset": 1, "color": "#381D0E"}]}}
INNER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DDB98C"}, {"offset": 1, "color": "#9C6B42"}]}}
CREAM_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4EAD2"}, {"offset": 1, "color": "#D6BE98"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6B42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F7EDD6", strokeWidth=3, opacity=55)
# plate patina: warm blotches + speckles
d.shape("ellipse", "Patina 1", x=210, y=630, width=180, height=115, fill="#C4A878", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=650, y=180, width=160, height=95, fill="#C4A878", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(190,250,9),(800,230,8),(160,540,8),(840,600,9),
                               (300,130,7),(695,130,8),(260,760,8),(735,765,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#8A6B42", opacity=40, stroke=NONE)

# --- ears (behind head) ---------------------------------------------------------
d.path("M398,372 C332,328 262,302 210,312 C212,352 260,404 396,428 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M602,372 C668,328 738,302 790,312 C788,352 740,404 604,428 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=7)
d.path("M382,378 C334,348 288,326 248,330 C256,362 296,398 384,412 Z",
       "Inner ear L", fill=INNER_GRAD, stroke=NONE)
d.path("M618,378 C666,348 712,326 752,330 C744,362 704,398 616,412 Z",
       "Inner ear R", fill=INNER_GRAD, stroke=NONE)
d.path("M382,368 C330,332 268,310 224,316", "Ear shade L",
       fill=NONE, stroke="#241108", strokeWidth=6, opacity=40, cap="round")
d.path("M618,368 C670,332 732,310 776,316", "Ear shade R",
       fill=NONE, stroke="#241108", strokeWidth=6, opacity=40, cap="round")

# --- ossicones (behind head) ----------------------------------------------------
d.path("M470,302 C466,282 466,262 472,250 C476,241 486,240 490,248 "
       "C494,262 494,284 492,304 Z",
       "Ossicone L", fill=NECK_GRAD, stroke=INK, strokeWidth=5)
d.path("M530,302 C534,282 534,262 528,250 C524,241 514,240 510,248 "
       "C506,262 506,284 508,304 Z",
       "Ossicone R", fill=NECK_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Ossicone cap L", x=469, y=237, width=22, height=15, fill="#241108", stroke=NONE)
d.shape("ellipse", "Ossicone cap R", x=509, y=237, width=22, height=15, fill="#241108", stroke=NONE)
d.path("M473,239 C468,231 462,227 456,227", "Tuft L1", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M483,237 C482,229 479,223 475,219", "Tuft L2", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M527,239 C532,231 538,227 544,227", "Tuft R1", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M517,237 C518,229 521,223 525,219", "Tuft R2", fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# --- bust: neck + shoulders (behind head) ---------------------------------------
d.path("M382,824 C375,750 390,670 432,580 C446,552 468,540 500,540 "
       "C532,540 554,552 568,580 C610,670 625,750 618,824 "
       "C580,844 420,844 382,824 Z",
       "Bust", fill=NECK_GRAD, stroke=INK, strokeWidth=7)
# neck sheen + side shadow (tops hide under the head)
d.path("M468,585 C455,665 447,745 448,810", "Neck sheen",
       fill=NONE, stroke="#8A5A34", strokeWidth=18, opacity=25, cap="round")
d.path("M566,590 C580,670 588,750 586,810", "Neck shadow",
       fill=NONE, stroke="#1E0F06", strokeWidth=20, opacity=30, cap="round")

# --- head ------------------------------------------------------------------------
d.path("M500,296 C556,296 600,328 614,386 C626,436 616,494 588,546 "
       "C566,588 540,622 500,630 C460,622 434,588 412,546 "
       "C384,494 374,436 386,386 C400,328 444,296 500,296 Z",
       "Head", fill=FACE_GRAD, stroke=INK, strokeWidth=8)
# forehead sheen + cheek shading + pale cheek marks
d.shape("ellipse", "Brow sheen", x=445, y=315, width=110, height=38,
        fill="#E8B87A", opacity=12, stroke=NONE)
d.shape("ellipse", "Cheek shade L", x=384, y=420, width=44, height=90,
        fill="#241108", opacity=25, stroke=NONE)
d.shape("ellipse", "Cheek shade R", x=572, y=420, width=44, height=90,
        fill="#241108", opacity=25, stroke=NONE)
d.shape("ellipse", "Cheek pale L", x=400, y=492, width=34, height=50,
        fill="#C89B6A", opacity=15, stroke=NONE)
d.shape("ellipse", "Cheek pale R", x=566, y=492, width=34, height=50,
        fill="#C89B6A", opacity=15, stroke=NONE)
# poll whorl between the ossicones
d.path("M488,300 C492,291 496,288 500,288 C504,288 508,291 512,300",
       "Poll whorl", fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# --- cream muzzle ------------------------------------------------------------------
d.path("M500,506 C540,506 566,532 566,568 C566,604 538,626 500,628 "
       "C462,626 434,604 434,568 C434,532 460,506 500,506 Z",
       "Muzzle", fill=CREAM_GRAD, stroke=NONE)
d.shape("ellipse", "Muzzle shade", x=452, y=586, width=96, height=34,
        fill="#B99A6E", opacity=30, stroke=NONE)
# nostrils + mouth + philtrum
d.path("M448,552 C450,542 460,536 470,538", "Nostril L",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M552,552 C550,542 540,536 530,538", "Nostril R",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M462,600 C480,612 520,612 538,600", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M500,586 C499,592 499,596 500,600", "Philtrum",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=60, cap="round")

# --- eyes: big, dark, lashed ---------------------------------------------------------
d.shape("ellipse", "Eye L", x=424, y=436, width=34, height=40, fill="#180C05", stroke=NONE)
d.shape("ellipse", "Eye R", x=542, y=436, width=34, height=40, fill="#180C05", stroke=NONE)
d.shape("ellipse", "Glint L", x=432, y=444, width=8, height=8, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=550, y=444, width=8, height=8, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M420,442 C432,430 452,428 466,436", "Lid L", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
d.path("M534,436 C548,428 568,430 580,442", "Lid R", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
d.path("M424,436 C416,430 410,424 406,416", "Lash L1", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M422,448 C414,444 407,440 402,434", "Lash L2", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M576,436 C584,430 590,424 594,416", "Lash R1", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M578,448 C586,444 593,440 598,434", "Lash R2", fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# --- chin shadow where jaw meets neck ------------------------------------------------
d.shape("ellipse", "Chin shadow", x=455, y=622, width=90, height=32,
        fill="#1E0F06", opacity=35, stroke=NONE)

# --- striped chest: the famous markings hinted on the bust --------------------------
d.path("M445,705 C475,688 525,688 555,705 C585,752 592,795 588,838 "
       "C560,846 440,846 412,838 C408,795 415,752 445,705 Z",
       "Chest patch", fill=CREAM_GRAD, stroke=NONE)
for i, (x1, y1, x2, y2) in enumerate([(444,730,556,732),(437,760,563,762),
                                     (430,790,570,792),(422,822,578,824)]):
    xm = (x1+x2)/2
    d.path(f"M{x1},{y1} C{xm-20},{y1+8} {xm+20},{y2+8} {x2},{y2}",
           f"Chest stripe {i+1}", fill=NONE, stroke="#3A2415",
           strokeWidth=13, opacity=90, cap="round")

# --- name ----------------------------------------------------------------------------
d.text("OKAPI", "Name", x=500, y=960, size=60, font="Virelai Sans",
       color="#EADFC0", justify="center")

d.finish("okapi-V1R00")
