#!/usr/bin/env python3
"""Gregwar Cache Wizard — mascot portrait V1R00.
Cache Misalignment Sorcerer: robed wizard whose staff is a stack of
mismatched image dimensions, thumbnails nested inside thumbnails.
Obsessive and haunted. 1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Gregwar Cache Wizard — Mascot Portrait", 1000, 1000)

INK = "#2A2230"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1626"}, {"offset": 1, "color": "#0B0812"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C5478"}, {"offset": 0.7, "color": "#38314E"},
    {"offset": 1, "color": "#1C1830"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A6E"}, {"offset": 1, "color": "#281C40"}]}}
ROBE_DK = "#1E1430"
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EDDFC2"}, {"offset": 1, "color": "#C9AE84"}]}}
BEARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8C4D4"}, {"offset": 1, "color": "#7E7A92"}]}}
GLOW = "#E8C25A"
FRAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8CFA8"}, {"offset": 1, "color": "#9A8F6A"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A5036"}, {"offset": 1, "color": "#42301C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E5680", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CEC8E4", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2C2640", opacity=50, stroke=NONE)

# faint cache-grid ghosts: thumbnails tiled wrong, drifting off-register
for i, (x, y, w, h, o) in enumerate([(190,190,120,90,16),(700,170,96,120,14),
                                     (170,420,110,84,12),(740,430,88,110,15),
                                     (640,210,140,100,10)]):
    d.path(rot_rect_path(x+w/2, y+h/2, w, h, (i-2)*3), f"Ghost thumb {i+1}",
           fill=NONE, stroke="#8A82AC", strokeWidth=3, opacity=o)

# --- nested thumbnail cluster, upper left --------------------------------------
# variants nested inside one another, each slightly wrong
nx, ny = 250, 180
for i, (w, h) in enumerate([(180,140), (136,104), (96,72), (60,44)]):
    d.shape("rectangle", f"Nested {i+1}", x=nx, y=ny, width=w, height=h,
            fill=NONE, stroke=FRAME, strokeWidth=4, opacity=90-i*12)
    nx += 14; ny += 12
# innermost: a tiny corrupted portrait
d.shape("rectangle", "Nested core", x=nx, y=ny, width=40, height=30,
        fill="#4A4468", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Core head", x=nx+14, y=ny+6, width=12, height=12,
        fill="#B9ACD2", stroke=NONE)
d.path(f"M{nx+4},{ny+30} L{nx+4},{ny+20} L{nx+36},{ny+20} L{nx+36},{ny+30}",
       "Core shoulders", fill="#B9ACD2", stroke=NONE, opacity=90)
# diagonal crop slashes through the nest — resized from a resized
d.path("M236,320 L448,168", "Crop slash", fill=NONE, stroke=GLOW,
       strokeWidth=4, cap="round", opacity=55)
d.path("M228,336 L420,192", "Crop slash 2", fill=NONE, stroke=GLOW,
       strokeWidth=3, cap="round", opacity=35)

# --- ground -------------------------------------------------------------------
d.shape("ellipse", "Ground", x=230, y=700, width=540, height=88,
        fill="#14101E", opacity=75, stroke=NONE)

# --- gregwar: robed, haunted -----------------------------------------------------
# robe: wide bell silhouette
d.path("M500,430 C570,430 620,470 640,540 C662,616 676,690 686,742 "
       "L314,742 C324,690 338,616 360,540 C380,470 430,430 500,430 Z",
       "Robe", fill=ROBE, stroke=INK, strokeWidth=7)
# robe folds
d.path("M430,540 C440,600 436,660 428,720 M570,540 C560,600 564,660 572,720",
       "Robe folds", fill=NONE, stroke=ROBE_DK, strokeWidth=5, opacity=70)
# hem band stitched with tiny broken frames
d.path("M330,710 L670,710", "Hem line", fill=NONE, stroke="#9A8FBE",
       strokeWidth=4, opacity=60)
for i, x in enumerate([370, 440, 530, 600]):
    d.shape("rectangle", f"Hem frame {i+1}", x=x, y=716, width=26, height=18,
            fill=NONE, stroke="#9A8FBE", strokeWidth=3, opacity=55)

# head + haunted face
d.shape("ellipse", "Head", x=424, y=300, width=152, height=146,
        fill=FACE, stroke=INK, strokeWidth=7)
# wizard hat: tall cone, slightly bent, one band
d.path("M500,150 C540,190 566,250 574,318 L426,318 C434,250 460,190 500,150 Z",
       "Hat cone", fill=ROBE, stroke=INK, strokeWidth=6, join="round")
d.path("M500,150 C512,140 528,138 542,146 C530,150 520,158 514,168 Z",
       "Hat tip", fill=ROBE, stroke=INK, strokeWidth=5, join="round")
d.path("M430,290 L570,290 L574,318 L426,318 Z", "Hat band",
       fill="#32244C", stroke=INK, strokeWidth=5, join="round")
# brim
d.path("M404,318 C404,300 596,300 596,318 C596,336 404,336 404,318 Z",
       "Hat brim", fill=ROBE_DK, stroke=INK, strokeWidth=5)
# eyes: wide, sleepless — the cache never sleeps either
d.shape("ellipse", "Eye L", x=452, y=352, width=26, height=32, fill="#FBF4E2",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=522, y=352, width=26, height=32, fill="#FBF4E2",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=460, y=362, width=10, height=12, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Pupil R", x=530, y=362, width=10, height=12, fill=INK,
        stroke=NONE)
# dark rings under both eyes
d.path("M452,392 C460,398 472,398 478,392", "Ring L", fill=NONE,
       stroke="#A08A68", strokeWidth=4, cap="round", opacity=80)
d.path("M522,392 C528,398 540,398 548,392", "Ring R", fill=NONE,
       stroke="#A08A68", strokeWidth=4, cap="round", opacity=80)
d.path("M448,336 C458,328 470,327 478,331", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M522,331 C530,327 542,328 552,336", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M478,418 C488,412 512,412 522,418", "Thin mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# beard spilling from under the face
d.path("M436,420 C436,470 456,516 500,528 C544,516 564,470 564,420 "
       "C548,442 528,452 500,452 C472,452 452,442 436,420 Z",
       "Beard", fill=BEARD, stroke=INK, strokeWidth=6, join="round")
d.path("M470,470 C476,492 486,506 500,512 M530,470 C524,492 514,506 500,512",
       "Beard strands", fill=NONE, stroke="#6E6A84", strokeWidth=4,
       cap="round", opacity=80)

# --- the staff: a stack of mismatched image dimensions ---------------------------
# shaft
d.path("M700,180 L700,766", "Staff shaft", fill=NONE, stroke=WOOD,
       strokeWidth=16, cap="round")
# stacked dimension frames climbing the shaft, each askew
frames = [(700, 330, 150, 112, -6), (700, 272, 118, 92, 5),
          (700, 224, 92, 74, -4), (700, 184, 66, 54, 7)]
for i, (cx, cy, w, h, deg) in enumerate(frames):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Staff frame {i+1}",
           fill=NONE, stroke=FRAME, strokeWidth=6)
# dimension labels inside their frames — digits in Source Sans 3
d.text("640x480", "Dim label big", x=700, y=336, size=13,
       font="Source Sans 3", color="#D8CFA8", justify="center")
d.text("300x250", "Dim label mid", x=700, y=228, size=11,
       font="Source Sans 3", color="#C9BE92", justify="center")
# finial: the cached original, glowing amber, nested twice
d.shape("rectangle", "Finial outer", x=666, y=120, width=68, height=52,
        fill="#3A3054", stroke=GLOW, strokeWidth=4)
d.shape("rectangle", "Finial inner", x=676, y=129, width=48, height=34,
        fill="#54486E", stroke=GLOW, strokeWidth=3, opacity=90)
d.shape("ellipse", "Finial head", x=692, y=136, width=15, height=13,
        fill=GLOW, stroke=NONE, opacity=95)
# glow sparks around the finial, kept inside the rim
d.path("M650,134 L638,126 M752,140 L764,134 M700,108 L700,96 M654,178 L642,186 M748,182 L758,192",
       "Finial sparks", fill=NONE, stroke=GLOW, strokeWidth=4,
       cap="round", opacity=80)

# hand gripping the shaft
d.path("M600,540 C640,560 668,590 682,626", "Arm R", fill=NONE,
       stroke=ROBE, strokeWidth=30, cap="round")
d.shape("ellipse", "Hand R", x=676, y=614, width=34, height=28, fill=FACE,
        stroke=INK, strokeWidth=5)
d.path("M688,606 L712,606 M688,620 L712,620", "Grip lines", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=70)

# left hand pinching a loose thumbnail that escaped the stack
d.path("M400,540 C368,556 350,580 344,606", "Arm L", fill=NONE,
       stroke=ROBE, strokeWidth=30, cap="round")
d.shape("ellipse", "Hand L", x=328, y=598, width=30, height=24, fill=FACE,
        stroke=INK, strokeWidth=5)
d.path(rot_rect_path(316, 574, 56, 44, -14), "Loose thumb",
       fill="#E8DFC0", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Loose head", x=306, y=566, width=14, height=12,
        fill="#8A7CA8", stroke=NONE)
d.path("M294,604 L294,594 L334,594 L334,604", "Loose shoulders",
       fill="#8A7CA8", stroke=NONE)

# sleeves pooling over the wrists
d.path("M596,522 C624,540 640,560 650,584", "Sleeve R", fill=NONE,
       stroke=ROBE_DK, strokeWidth=14, cap="round", opacity=80)
d.path("M406,522 C382,538 366,558 356,580", "Sleeve L", fill=NONE,
       stroke=ROBE_DK, strokeWidth=14, cap="round", opacity=80)

# --- captions -------------------------------------------------------------------
d.text("GREGWAR CACHE WIZARD", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCD4EC", justify="center")
r = d.text("CACHE MISALIGNMENT SORCERER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89CC8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("012.gregwar-cache-wizard-V1R00")
