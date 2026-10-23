#!/usr/bin/env python3
"""Goblin shark — field-guide plate V1R00. Profile facing left: elongated
flattened rostrum, jaws slingshot mid-protrusion, pale pink-grey skin over
a blackwater indigo plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; rostrum and caudal tips stay inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Goblin Shark — Field Plate", 1000, 1000)

INK = "#2B2440"          # deep indigo-plum
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0A0E1E"}, {"offset": 1, "color": "#03050D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46589A"}, {"offset": 0.55, "color": "#232F63"},
    {"offset": 1, "color": "#0C1230"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E3C2BC"}, {"offset": 0.45, "color": "#C39AA0"},
    {"offset": 1, "color": "#8A6B7E"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B88A92"}, {"offset": 1, "color": "#7E5E72"}]}}
JAW_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDD6CE"}, {"offset": 1, "color": "#B0888C"}]}}
ROSTRUM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E9CCC4"}, {"offset": 1, "color": "#A87E8A"}]}}

# --- backdrop + blackwater plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo outer", x=52, y=12, width=896, height=896,
        fill="#5C72B8", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate halo inner", x=66, y=26, width=868, height=868,
        fill="#7E94CE", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A3560", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#93A6DC", strokeWidth=3, opacity=45)
# cold haze + marine snow
d.shape("ellipse", "Haze 1", x=180, y=160, width=260, height=140, fill="#7E94CE", opacity=14, stroke=NONE)
d.shape("ellipse", "Haze 2", x=540, y=620, width=260, height=140, fill="#46589A", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(190,290,7),(780,250,6),(165,460,8),(835,440,7),(230,690,6),
                               (755,715,8),(145,380,5),(860,560,6),(400,110,6),(610,105,7),
                               (300,160,5),(700,170,6),(330,820,6),(660,825,5),(500,96,5),
                               (210,600,4),(820,330,5)]):
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#C9D4F0", opacity=40, stroke=NONE)

# --- shadow + far-side fins -----------------------------------------------------
d.shape("ellipse", "Cast shadow", x=330, y=610, width=380, height=46,
        fill="#0A0F28", opacity=45, stroke=NONE)
# far pectoral fin, darker, hanging below the throat
d.path("M418,492 C448,524 476,566 488,604 C490,612 482,616 474,610 "
       "C442,588 416,542 410,508 Z",
       "Pectoral fin far", fill="#6E5266", stroke=INK, strokeWidth=4)
# pelvic fin on the lower mid-body
d.path("M562,580 C584,598 612,606 632,596 C638,590 632,578 616,574 "
       "C596,568 574,570 562,580 Z",
       "Pelvic fin", fill=FIN_GRAD, stroke=INK, strokeWidth=4)
# anal fin, small flap near the tail underside
d.path("M688,562 C698,586 726,592 744,578 C748,570 742,558 728,554 "
       "C710,548 696,552 688,562 Z",
       "Anal fin", fill=FIN_GRAD, stroke=INK, strokeWidth=4)

# --- caudal fin: long upper lobe, short lower lobe -------------------------------
d.path("M796,496 C840,456 868,430 894,416 C890,440 856,486 812,514 "
       "C834,530 850,548 854,562 C836,556 812,540 802,522 "
       "C798,514 796,506 796,496 Z",
       "Caudal fin", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
# dorsal fins: small, rounded, set far back
d.path("M598,392 C606,360 648,350 668,372 C676,382 668,394 650,398 "
       "C632,402 610,400 598,392 Z",
       "Dorsal fin 1", fill=FIN_GRAD, stroke=INK, strokeWidth=5)
d.path("M698,428 C706,404 740,398 756,414 C762,422 756,434 740,438 "
       "C724,442 708,438 698,428 Z",
       "Dorsal fin 2", fill=FIN_GRAD, stroke=INK, strokeWidth=5)

# --- body: soft flabby spindle, translucent skin ---------------------------------
d.path("M400,398 C470,372 620,376 720,434 C760,456 792,480 802,504 "
       "C806,514 806,522 802,528 C742,568 642,596 546,586 "
       "C478,578 430,540 412,496 C404,470 398,430 400,398 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6, opacity=94)
# internal gloom + dorsal sheen (translucent — the skin reads semi-clear)
d.shape("ellipse", "Body gloom", x=480, y=460, width=220, height=110,
        fill="#5E4660", opacity=26, stroke=NONE)
d.path("M420,404 C500,382 630,386 716,438", "Dorsal sheen", fill=NONE,
       stroke="#F4E4DE", strokeWidth=13, opacity=28, cap="round")
d.path("M440,560 C510,584 620,582 700,552", "Belly shade", fill=NONE,
       stroke="#5E4660", strokeWidth=12, opacity=30, cap="round")
# faint spinal hint
d.path("M430,470 C520,462 640,478 762,514", "Spine hint", fill=NONE,
       stroke="#6E5266", strokeWidth=5, opacity=35, cap="round")
# near pectoral fin over the body
d.path("M444,498 C492,512 542,542 568,580 C572,588 564,594 554,590 "
       "C510,572 462,540 440,512 Z",
       "Pectoral fin", fill=FIN_GRAD, stroke=INK, strokeWidth=5)

# --- rostrum: the long flat blade ------------------------------------------------
d.path("M442,368 C380,352 258,330 172,316 C166,315 166,321 172,324 "
       "C260,348 382,374 444,392 Z",
       "Rostrum", fill=ROSTRUM_GRAD, stroke=INK, strokeWidth=5)
# rostrum ridge + ampullae pores along the underside
d.path("M436,376 C370,358 262,338 186,324", "Rostrum ridge", fill=NONE,
       stroke="#F4E4DE", strokeWidth=4, opacity=45, cap="round")
for i, t in enumerate([0.15, 0.27, 0.39, 0.51, 0.63, 0.75, 0.87]):
    x = 420 + (190 - 420) * t
    y = 386 + (326 - 386) * t + 6
    d.shape("ellipse", f"Rostrum pore {i+1}", x=x-3, y=y-3, width=6, height=6,
            fill="#5E4660", opacity=55, stroke=NONE)

# --- the slingshot jaw, mid-protrusion -------------------------------------------
# throat membrane sagging between head and the thrown-forward jaw
d.path("M296,486 C330,506 376,512 412,502 C420,498 418,490 410,490 "
       "C372,496 330,492 300,474 Z",
       "Throat membrane", fill="#C39AA0", opacity=55, stroke=NONE)
# protruded jaw: an elongated tube thrust forward under the rostrum
d.path("M424,430 C384,414 322,406 272,416 C256,420 250,436 254,452 "
       "C258,472 264,484 282,492 C326,504 392,498 424,482 "
       "C428,464 426,446 424,430 Z",
       "Jaw unit", fill=JAW_GRAD, stroke=INK, strokeWidth=5)
# mouth: dark oval on the front face of the tube
d.path("M276,424 C288,428 294,442 294,456 C294,470 288,482 276,488 "
       "C264,482 258,464 262,446 C264,434 268,428 276,424 Z",
       "Mouth", fill="#2E1E2E", stroke=INK, strokeWidth=4)
# needle teeth ringing the mouth rim, fanned forward
teeth = [(280,426,-16,-8),(288,432,-18,-4),(292,444,-19,-1),(292,454,-19,2),
         (290,464,-18,6),(285,474,-16,9),(279,482,-13,11),
         (268,424,-13,-9),(262,434,-15,-7),(258,446,-16,-3),(258,458,-16,2),
         (261,470,-14,7),(268,480,-12,10)]
for j, (tx, ty, ddx, ddy) in enumerate(teeth):
    d.path(f"M{tx},{ty} l{ddx},{ddy}", f"Tooth {j+1}", fill=NONE,
           stroke="#F2E6E0", strokeWidth=3.5, cap="round")
# jaw shading + stretched-ligament creases at the hinge
d.path("M300,486 C340,494 388,490 420,476", "Jaw shade", fill=NONE,
       stroke="#8A6B7E", strokeWidth=5, opacity=45, cap="round")
d.path("M430,444 C438,456 440,472 434,488", "Ligament crease 1", fill=NONE,
       stroke="#8A6B7E", strokeWidth=4, opacity=40, cap="round")
d.path("M436,436 C446,450 448,470 440,490", "Ligament crease 2", fill=NONE,
       stroke="#8A6B7E", strokeWidth=4, opacity=30, cap="round")

# --- head details ------------------------------------------------------------------
# eye: small, dark, low on the head
d.shape("ellipse", "Eye", x=448, y=424, width=18, height=16,
        fill="#1E1420", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=454, y=427, width=5, height=5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# five gill slits behind the head, angled back
for i in range(5):
    gx = 470 + i * 22
    d.path(f"M{gx},416 C{gx-4},438 {gx+2},462 {gx+12},482",
           f"Gill slit {i+1}", fill=NONE, stroke="#6E5266",
           strokeWidth=4.5, opacity=60, cap="round")
# skin speckles
for i, (x, y, w) in enumerate([(470,410,6),(540,396,5),(610,420,6),(680,450,5),
                               (530,540,6),(610,560,5),(470,520,5),(700,510,4)]):
    d.shape("ellipse", f"Skin fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6B7E", opacity=45, stroke=NONE)

# --- name ---------------------------------------------------------------------------
d.text("GOBLIN SHARK", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#A9B8E4", justify="center")

d.finish("goblin-shark-V1R00")
