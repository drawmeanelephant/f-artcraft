#!/usr/bin/env python3
"""Manatee — field-guide plate V1R00. Full body, side profile drifting left:
barrel body, round paddle tail tilted toward the viewer, nailed flipper,
bristly whiskered muzzle. Warm grey hide with an algae-green back sheen;
calm lagoon plate with light rays and a seagrass bed closing on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Manatee — Field Plate", 1000, 1000)

INK = "#3A3632"
CX, CY, R = 500, 460, 420
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#123430"}, {"offset": 1, "color": "#061513"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4F0DA"}, {"offset": 0.65, "color": "#A9CDB4"},
    {"offset": 1, "color": "#6C9C88"}]}}
GRASS_BED_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#B8C79A"}, {"offset": 1, "color": "#7E9068"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#77736A"}, {"offset": 0.5, "color": "#A39D91"},
    {"offset": 1, "color": "#D2CABB"}]}}
TAIL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8A296"}, {"offset": 0.7, "color": "#857F74"},
    {"offset": 1, "color": "#625D55"}]}}
FLIPPER_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#8A847A"}, {"offset": 1, "color": "#5E5951"}]}}
MUZZLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C9C1B2"}, {"offset": 0.7, "color": "#A69F92"},
    {"offset": 1, "color": "#827B70"}]}}
ALGAE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E9A52"}, {"offset": 1, "color": "#5C7A44"}]}}
RAY_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#FFFFFF", "opacity": 0.32}, {"offset": 1, "color": "#FFFFFF", "opacity": 0}]}}
BLADE_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#8DB27A"}, {"offset": 1, "color": "#4F7A4C"}]}}

def rim_y(x):
    return CY - math.sqrt(R*R - (x - CX)**2)

def chord_x(y, r=R):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E8270", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0F8EC", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=170, width=240, height=130, fill="#C6DDC0", opacity=24, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=600, width=240, height=120, fill="#86AE98", opacity=18, stroke=NONE)
# surface shimmer: soft caustic ovals near the top of the disc
for i, (x, y, w, h) in enumerate([(330,110,120,18),(470,96,90,14),(580,118,110,16),(400,146,70,10),(540,150,80,12)]):
    d.shape("ellipse", f"Caustic {i+1}", x=x, y=y, width=w, height=h, fill="#FFFFFF", opacity=20, stroke=NONE)
# light rays: tops ride the disc arc, bottoms tuck under the seagrass bed
for i, (x0, x1, b0, b1, o) in enumerate([(300, 350, 340, 450, 60), (430, 490, 470, 590, 70),
                                         (560, 600, 620, 700, 55), (660, 690, 700, 760, 40)]):
    d.path(f"M{x0},{rim_y(x0):.1f} A420,420 0 0 1 {x1},{rim_y(x1):.1f} L{b1},770 L{b0},770 Z",
           f"Light ray {i+1}", fill=RAY_GRAD, opacity=o, stroke=NONE)
for i, (x, y, w) in enumerate([(190,320,7),(790,250,6),(160,520,7),(840,450,7),(260,220,6),
                               (720,190,6),(140,420,5),(860,560,5)]):
    d.shape("ellipse", f"Drift fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=40, stroke=NONE)

# --- seagrass bed: closes on the disc's own arc ------------------------------------
gl, gr = chord_x(758)
d.path(f"M{gl:.1f},758 C360,742 640,742 {gr:.1f},758 A420,420 0 0 1 {gl:.1f},758 Z",
       "Seagrass bed", fill=GRASS_BED_GRAD, stroke=NONE)
d.path(f"M{gl+20:.1f},757 C370,744 630,744 {gr-20:.1f},757", "Bed light", fill=NONE,
       stroke="#EEF2D8", strokeWidth=4, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(300,790,24),(450,782,18),(600,796,22),(380,826,14),(540,830,16),(680,812,12)]):
    d.shape("ellipse", f"Sand ripple {i+1}", x=x, y=y, width=w*2, height=w/3,
            fill="#6E7E58", opacity=30, stroke=NONE)
# seagrass blades: tapered ribbons swaying from the bed
def blade(label, x, h, lean, w=10, op=80):
    top = (x + lean, 754 - h)
    c1 = (x - lean*0.4, 754 - h*0.45)
    d.path(f"M{x - w/2:.0f},756 Q{c1[0] - w/2:.0f},{c1[1]:.0f} {top[0]:.0f},{top[1]:.0f} "
           f"Q{c1[0] + w/2:.0f},{c1[1]:.0f} {x + w/2:.0f},756 Z",
           label, fill=BLADE_GRAD, opacity=op, stroke=NONE)
for i, (x, h, lean) in enumerate([(232,110,-20),(250,150,16),(270,96,30),(292,70,-10),
                                  (700,90,-18),(722,140,20),(744,118,-26),(766,84,12)]):
    blade(f"Seagrass {i+1}", x, h, lean)
for i, (x, h, lean) in enumerate([(400,46,-10),(430,60,12),(560,52,-8),(590,40,10)]):
    blade(f"Seagrass low {i+1}", x, h, lean, w=8, op=60)
# re-stroke the rim over the bed so the plate edge stays continuous
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#4E8270", strokeWidth=6)
d.shape("ellipse", "Plate inner ring over bed", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0F8EC", strokeWidth=3, opacity=40)
d.shape("ellipse", "Manatee shadow", x=290, y=748, width=440, height=26, fill="#4E5E3E", opacity=24, stroke=NONE)

# --- far flipper, peeking below the belly -------------------------------------------
d.path("M352,540 C342,574 326,604 300,622 C296,600 312,566 326,540 Z",
       "Flipper far", fill="#5E5951", opacity=70, stroke=NONE)

# --- body + paddle tail: one silhouette, so the tail stock has no seam -----------------
# the paddle is a broad round spatula, tilted toward the viewer
d.path("M196,432 C206,396 244,374 292,368 C360,346 462,328 562,338 "
       "C646,348 708,378 752,414 C770,408 784,384 802,356 "
       "C830,322 878,322 894,362 C912,408 896,480 862,520 "
       "C836,550 796,552 780,526 C770,508 762,490 752,480 "
       "C716,502 664,524 602,536 C504,556 398,558 326,540 "
       "C280,530 244,520 220,508 C196,496 184,462 196,432 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# paddle tone: darker radial wash fading into the stock (no stroke, no seam)
d.path("M760,412 C776,404 786,384 802,356 C830,322 878,322 894,362 "
       "C912,408 896,480 862,520 C836,550 796,552 780,526 C770,508 764,494 760,484 "
       "C748,460 748,436 760,412 Z",
       "Tail paddle tone", fill=TAIL_GRAD, opacity=70, stroke=NONE)
d.path("M808,364 C836,340 868,342 882,370", "Tail rim light", fill=NONE,
       stroke="#E6E0D4", strokeWidth=5, opacity=40, cap="round")
for i, dd in enumerate(["M770,436 C806,418 842,400 874,392", "M774,452 C812,450 850,452 882,460",
                        "M772,466 C806,480 834,498 856,520"]):
    d.path(dd, f"Tail crease {i+1}", fill=NONE, stroke="#5A554D", strokeWidth=3, opacity=35, cap="round")
for i, (x, y, w, h) in enumerate([(840,376,22,14),(824,474,26,16),(862,430,16,12)]):
    d.shape("ellipse", f"Tail scar {i+1}", x=x, y=y, width=w, height=h,
            fill="#D8D0C2", opacity=28, stroke=NONE)
d.path("M820,348 C846,334 870,340 880,356", "Tail algae", fill=NONE,
       stroke="#6F8E48", strokeWidth=8, opacity=30, cap="round")
# algae-green back sheen: translucent wash + mottled patches along the spine
d.path("M300,374 C380,350 480,336 562,344 C640,352 700,380 744,414 "
       "C700,394 640,374 562,368 C470,362 380,372 300,392 Z",
       "Algae back wash", fill=ALGAE_GRAD, opacity=45, stroke=NONE)
for i, (x, y, w, h) in enumerate([(380,352,70,18),(470,340,90,20),(574,348,70,18),(650,370,54,16),(330,370,40,12)]):
    d.shape("ellipse", f"Algae patch {i+1}", x=x, y=y, width=w, height=h,
            fill="#6F8E48", opacity=32, stroke=NONE)
d.path("M330,372 C420,350 520,342 610,352", "Back sheen", fill=NONE,
       stroke="#EEF2E0", strokeWidth=6, opacity=30, cap="round")
# belly glow + girth shading
d.path("M330,532 C420,550 520,548 610,528 C560,544 420,548 330,532 Z",
       "Belly glow", fill="#FFFFFF", opacity=30, stroke=NONE)
d.path("M360,520 C460,536 560,530 660,508", "Belly shade", fill=NONE,
       stroke="#6A655C", strokeWidth=10, opacity=18, cap="round")
# skin wrinkles + pale boat-scar streaks (the manatee's life story)
for i, dd in enumerate(["M300,404 C292,436 294,470 306,502", "M318,398 C310,432 312,468 324,500",
                        "M690,400 C680,430 680,470 690,500", "M712,410 C704,436 704,466 712,490"]):
    d.path(dd, f"Wrinkle {i+1}", fill=NONE, stroke="#5E5951", strokeWidth=3, opacity=35, cap="round")
for i, dd in enumerate(["M520,372 C540,380 556,392 566,406", "M536,368 C556,376 572,388 582,402"]):
    d.path(dd, f"Old scar {i+1}", fill=NONE, stroke="#E2DACB", strokeWidth=3, opacity=45, cap="round")
for i, (x, y) in enumerate([(420,430),(480,410),(540,450),(600,420),(450,480),(620,470),(380,460),(660,440)]):
    d.shape("ellipse", f"Hide pore {i+1}", x=x, y=y, width=5, height=5, fill="#6A655C", opacity=35, stroke=NONE)

# --- head: bulbous whiskered muzzle ----------------------------------------------------
d.path("M300,392 C276,388 238,394 214,410 C186,428 176,462 190,488 "
       "C200,506 226,514 252,510 C280,506 300,486 304,458 C306,432 306,410 300,392 Z",
       "Muzzle pad", fill=MUZZLE_GRAD, stroke=NONE)
# hard outline only where the muzzle is the silhouette; a soft crease where it meets the face
d.path("M262,392 C244,394 226,400 214,410 C186,428 176,462 190,488 "
       "C200,506 226,514 252,510", "Muzzle outline", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M252,510 C280,506 300,486 304,458 C306,432 306,410 300,394", "Muzzle crease",
       fill=NONE, stroke="#5E5951", strokeWidth=4, opacity=40, cap="round")
d.path("M228,410 C252,400 278,398 296,402", "Muzzle light", fill=NONE,
       stroke="#F2ECE0", strokeWidth=6, opacity=40, cap="round")
# split upper lip + small lower lip
d.path("M200,478 C214,488 232,490 246,484", "Lip cleft", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M214,500 C226,512 248,516 268,508", "Lower lip", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=70, cap="round")
# nostrils on top of the snout
d.path("M206,420 C212,414 222,414 226,420", "Nostril front", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M232,410 C238,404 248,404 252,410", "Nostril back", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# whisker pores + bristles
for i, (x, y) in enumerate([(206,446),(220,440),(234,446),(214,462),(228,458),(242,462),
                            (256,450),(250,470),(236,474),(266,464),(262,434),(276,450)]):
    d.shape("ellipse", f"Whisker pore {i+1}", x=x - 2, y=y - 2, width=4, height=4,
            fill="#4E4A44", opacity=70, stroke=NONE)
for i, (x, y, dx, dy) in enumerate([(206,446,-22,-6),(214,462,-24,4),(220,440,-18,-14),
                                    (228,458,-26,12),(236,474,-20,18),(250,470,-10,24)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Bristle {i+1}", fill=NONE,
           stroke="#E8E2D4", strokeWidth=2, opacity=75, cap="round")
# small, mild eye
d.shape("ellipse", "Eye socket", x=314, y=416, width=30, height=22, fill="#5E5951", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye", x=322, y=421, width=13, height=12, fill="#1C1A18", stroke=NONE)
d.shape("ellipse", "Eye glint", x=325, y=423, width=5, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M316,420 C324,412 336,412 344,420", "Eye crease", fill=NONE,
       stroke="#5E5951", strokeWidth=3, opacity=60, cap="round")

# --- near flipper with three nails --------------------------------------------------------
d.path("M374,500 C384,530 380,570 360,598 C346,618 318,624 306,612 "
       "C296,600 312,580 326,560 C338,540 346,516 352,500 Z",
       "Flipper near", fill=FLIPPER_GRAD, stroke=NONE)
d.path("M374,500 C384,530 380,570 360,598 C346,618 318,624 306,612 "
       "C296,600 312,580 326,560 C338,540 346,516 352,500", "Flipper outline",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M352,500 C358,494 368,494 374,500", "Flipper armpit", fill=NONE,
       stroke="#5E5951", strokeWidth=3, opacity=45, cap="round")
d.path("M362,512 C366,540 360,566 346,588", "Flipper sheen", fill=NONE,
       stroke="#DDD6C8", strokeWidth=4, opacity=35, cap="round")
for i, (x, y) in enumerate([(310,600),(322,610),(336,612)]):
    d.shape("ellipse", f"Nail {i+1}", x=x - 5, y=y - 4, width=10, height=8,
            fill="#E6DCC6", opacity=90, stroke="#5E5951", strokeWidth=1.5)

# --- bubbles from the nostrils + a few lagoon fish ----------------------------------------
for i, (x, y, w) in enumerate([(214,386,12),(206,350,9),(220,318,14),(210,280,8),(222,246,11)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=22, stroke="#FFFFFF", strokeWidth=1.5)
for i, (x, y, s) in enumerate([(620,230,1.0),(668,250,0.8),(646,276,0.9)]):
    d.path(f"M{x},{y} C{x+10*s:.0f},{y-8*s:.0f} {x+26*s:.0f},{y-8*s:.0f} {x+34*s:.0f},{y} "
           f"L{x+44*s:.0f},{y-8*s:.0f} L{x+44*s:.0f},{y+8*s:.0f} L{x+34*s:.0f},{y} "
           f"C{x+26*s:.0f},{y+8*s:.0f} {x+10*s:.0f},{y+8*s:.0f} {x},{y} Z",
           f"Fish {i+1}", fill="#4E7A68", opacity=40, stroke=NONE)

# --- name ----------------------------------------------------------------------------------
d.text("MANATEE", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DCEBDF", justify="center")

d.finish("manatee-V1R00")
