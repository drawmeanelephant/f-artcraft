#!/usr/bin/env python3
"""Tardigrade (water bear) — field-guide plate V1R00. Side view: segmented
barrel body, 4 stubby legs per side ending in claws, puckered mouth rings.
Petri-dish mood — the plate IS the specimen dish. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tardigrade — Field Plate", 1000, 1000)

INK = "#4A3B2E"   # warm dark brown, not black
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#152820"}, {"offset": 1, "color": "#060F0B"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0ECD4"}, {"offset": 0.7, "color": "#CBD3A6"},
    {"offset": 1, "color": "#93A274"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E8C0"}, {"offset": 0.62, "color": "#DEC98E"},
    {"offset": 1, "color": "#AAB176"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E9DCAC"}, {"offset": 1, "color": "#AC9F68"}]}}

# --- petri dish ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Dish", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8055", strokeWidth=6)
d.shape("ellipse", "Dish inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F1DC", strokeWidth=3, opacity=60)
# glass sheen arc on the rim
d.path("M210,220 C300,140 460,105 620,135", "Dish sheen",
       fill=NONE, stroke="#FFFFFF", strokeWidth=10, opacity=18, cap="round")
# agar patina + floating specks
d.shape("ellipse", "Agar blotch 1", x=160, y=200, width=240, height=140,
        fill="#A9B97E", opacity=22, stroke=NONE)
d.shape("ellipse", "Agar blotch 2", x=580, y=660, width=280, height=150,
        fill="#A9B97E", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(190,330,8),(770,250,7),(160,560,9),(810,540,8),
                               (250,760,7),(730,750,9),(140,430,6),(855,420,7),
                               (380,140,7),(600,120,8),(330,820,6),(680,820,7)]):
    d.shape("ellipse", f"Dish fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E8055", opacity=40, stroke=NONE)
# tiny air bubbles along the left of the dish
for i, (x, y, w) in enumerate([(200,610,16),(175,540,11),(195,460,20),(168,385,13)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=15, stroke=NONE)

# --- drop shadow under the animal --------------------------------------------
d.shape("ellipse", "Specimen shadow", x=280, y=680, width=500, height=46,
        fill="#3A4A2E", opacity=25, stroke=NONE)

# --- far-side legs (behind the body, only tips peek below the silhouette) -----
for i, lx in enumerate([495, 615, 735]):
    d.path(f"M{lx-16},610 C{lx-22},645 {lx-20},675 {lx-14},688 "
           f"C{lx-8},696 {lx+8},696 {lx+14},688 C{lx+20},675 {lx+22},645 {lx+16},610 Z",
           f"Far leg {i+1}", fill="#948E5C", stroke=INK, strokeWidth=4, opacity=80)

# --- body: silhouette path used twice — as the base fill, then as ink outline --
SILHOUETTE = ("M238,508 C234,445 268,400 325,392 "
              "C370,368 440,366 478,378 "
              "C515,362 590,360 632,380 "
              "C685,366 735,378 752,412 "
              "C782,450 792,505 788,555 "
              "C782,592 745,638 660,656 "
              "C590,668 480,672 400,664 "
              "C320,658 272,630 256,590 "
              "C242,565 236,538 238,508 Z")
d.path(SILHOUETTE, "Body fill", fill=BODY_GRAD, stroke=NONE)

# five overlapping segment ellipses (head + 4 trunk segments) inside the fill —
# each carries its own radial gradient, which is what reads as segmentation
segs = [
    ("Head",   242, 400, 190, 210),   # head, slightly smaller
    ("Seg 1",  345, 390, 200, 235),
    ("Seg 2",  470, 385, 210, 240),
    ("Seg 3",  595, 390, 180, 235),
    ("Rear",   680, 432, 100, 146),   # tapering rump
]
for name, x, y, w, h in segs:
    d.shape("ellipse", f"Body {name}", x=x, y=y, width=w, height=h,
            fill=BODY_GRAD, stroke=NONE)

# soft per-segment lower-right shade so the blobs read as separate rings
for i, (x, y, w, h) in enumerate([(350,470,190,150),(475,470,200,155),
                                  (600,470,180,150),(695,480,85,120)]):
    d.shape("ellipse", f"Seg shade {i+1}", x=x, y=y, width=w, height=h,
            fill="#8F9455", opacity=28, stroke=NONE)

# contents seen through the translucent cuticle
d.shape("ellipse", "Gut blob 1", x=400, y=470, width=90, height=70,
        fill="#B89E58", opacity=30, stroke=NONE)
d.shape("ellipse", "Gut blob 2", x=555, y=500, width=110, height=80,
        fill="#9AA85C", opacity=26, stroke=NONE)
d.shape("ellipse", "Gut blob 3", x=680, y=480, width=60, height=50,
        fill="#B89E58", opacity=24, stroke=NONE)

# belly shadow hugging the inside of the bottom edge
d.path("M300,625 C420,660 600,660 715,615 C600,645 420,645 300,625 Z",
       "Belly shadow", fill="#8F9455", opacity=35, stroke=NONE)

# --- silhouette outline (stroke only, over the segment fills) -----------------
d.path(SILHOUETTE, "Body outline", fill=NONE, stroke=INK, strokeWidth=7)

# crease arcs between segments
for i, cx in enumerate([418, 545, 668]):
    d.path(f"M{cx-14},400 Q{cx+12},505 {cx-10},622", f"Crease {i+1}",
           fill=NONE, stroke="#8A8450", strokeWidth=5, opacity=45, cap="round")

# sheen: broad soft highlight + a crisp arc under the top edge
d.shape("ellipse", "Body sheen", x=330, y=378, width=360, height=72,
        fill="#FFFFFF", opacity=17, stroke=NONE)
d.path("M285,435 C370,395 540,380 665,415", "Top sheen",
       fill=NONE, stroke="#FFFFFF", strokeWidth=9, opacity=28, cap="round")

# --- near-side legs: three under the trunk + one rear leg pointing back -------
def leg(lx, top, bot):
    d.path(f"M{lx-20},{top} C{lx-27},{top+28} {lx-25},{bot-22} {lx-17},{bot-8} "
           f"C{lx-9},{bot} {lx+9},{bot} {lx+17},{bot-8} "
           f"C{lx+25},{bot-22} {lx+27},{top+28} {lx+20},{top} Z",
           f"Leg {lx}", fill=LEG_GRAD, stroke=INK, strokeWidth=5)
    # claw pair at the tip
    d.path(f"M{lx-6},{bot-4} Q{lx-17},{bot+4} {lx-16},{bot+14}",
           f"Claw {lx}a", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
    d.path(f"M{lx+6},{bot-4} Q{lx+17},{bot+4} {lx+16},{bot+14}",
           f"Claw {lx}b", fill=NONE, stroke=INK, strokeWidth=4, cap="round")

leg(445, 632, 722)
leg(565, 640, 728)
leg(680, 632, 716)
# rear leg — angled backward like the real fourth pair
d.path("M742,598 C776,600 812,622 824,652 C832,674 826,692 804,694 "
       "C782,696 768,680 760,656 C754,636 736,614 742,598 Z",
       "Rear leg", fill=LEG_GRAD, stroke=INK, strokeWidth=5)
d.path("M812,682 Q824,690 826,702", "Rear claw a",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M796,690 Q806,700 806,710", "Rear claw b",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# --- face: puckered mouth rings + eyespot -------------------------------------
d.shape("ellipse", "Mouth outer", x=234, y=488, width=34, height=30,
        fill="#CBB87E", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Mouth mid", x=242, y=495, width=18, height=16,
        fill="#8F8052", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Mouth pore", x=248, y=500, width=8, height=7,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eyespot", x=305, y=452, width=9, height=9,
        fill="#3A3226", opacity=55, stroke=NONE)

# --- moss flecks on the agar near the feet -------------------------------------
for i, (x, y, w) in enumerate([(320,742,14),(505,752,11),(640,738,13),(380,760,9)]):
    d.shape("ellipse", f"Moss {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#5E8A4A", opacity=60, stroke=NONE)

# --- name ----------------------------------------------------------------------
d.text("TARDIGRADE", "Name", x=500, y=960, size=60, font="Virelai Sans",
       color="#E4ECD0", justify="center")

d.finish("tardigrade-V1R00")
