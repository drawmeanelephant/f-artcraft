#!/usr/bin/env python3
"""Afterimage Clerk — mascot portrait V1R00.
Clerk with visor and feather duster, dusting the clean silhouette on an
archive shelf where a proof packet used to sit — its ghost outline lingers.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Afterimage Clerk — Mascot Portrait", 1000, 1000)

INK = "#2A2326"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16202E"}, {"offset": 1, "color": "#0A0F16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E6A78"}, {"offset": 0.7, "color": "#33484F"},
    {"offset": 1, "color": "#1E2E36"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3D46"}, {"offset": 1, "color": "#16242C"}]}}
SHELF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6B5540"}, {"offset": 1, "color": "#4A3828"}]}}
PACKET = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9BCA0"}, {"offset": 1, "color": "#9C8C6E"}]}}
VEST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#55606E"}, {"offset": 0.75, "color": "#3E4654"},
    {"offset": 1, "color": "#2A3038"}]}}
SHIRT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DCD4BE"}, {"offset": 1, "color": "#B0A68C"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2DAB8"}, {"offset": 1, "color": "#CFA880"}]}}
TROUSER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4654"}, {"offset": 1, "color": "#232830"}]}}
SHOE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E322C"}, {"offset": 1, "color": "#1E1614"}]}}
GHOST = "#9BF0C4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E707C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE0DC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(205,230,7),(782,215,6),(195,540,6),(815,545,7),
                               (245,758,7),(758,752,7),(138,398,6),(860,396,6),
                               (365,140,7),(635,136,6),(312,812,6),(690,808,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5C64", opacity=45, stroke=NONE)

# --- floor band closed on the disc's own arc ----------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#101C22",
       strokeWidth=4, opacity=65)

# --- archive shelf with dusty packets and one absence --------------------------
# shelf plank, right half of the disc
d.shape("rectangle", "Shelf", x=428, y=430, width=390, height=18,
        fill=SHELF_GRAD, stroke=INK, strokeWidth=5, radius=4)
d.path("M448,448 L470,448 L459,472 Z", "Shelf bracket L",
       fill="#3A2C20", stroke=INK, strokeWidth=4, join="round")
d.path("M776,448 L798,448 L787,472 Z", "Shelf bracket R",
       fill="#3A2C20", stroke=INK, strokeWidth=4, join="round")

def packet(x, y, w, h, label, dust=True):
    d.shape("rectangle", f"{label} body", x=x, y=y, width=w, height=h,
            fill=PACKET, stroke=INK, strokeWidth=4, radius=7)
    d.path(f"M{x+5},{y+7} L{x+w/2},{y+h*0.42} L{x+w-5},{y+7}",
           f"{label} flap", fill=NONE, stroke=INK, strokeWidth=3, join="round", opacity=75)
    d.path(f"M{x+8},{y+h-14} L{x+w-8},{y+h-14}",
           f"{label} rule", fill=NONE, stroke="#7A6C52", strokeWidth=3, opacity=60)
    if dust:
        for j, (dx, dy, s) in enumerate([(6, -2, 5), (w*0.45, -4, 4), (w-9, -2, 5)]):
            d.shape("ellipse", f"{label} dust {j+1}", x=x+dx-s/2, y=y+dy-s/2,
                    width=s, height=s, fill="#8A7C62", opacity=55, stroke=NONE)

packet(448, 350, 72, 80, "Packet A")
packet(538, 366, 60, 64, "Packet B")
packet(724, 348, 76, 82, "Packet C")

# the empty space: dust-free silhouette on the shelf top + ghost outline
d.shape("rectangle", "Clean spot", x=614, y=424, width=92, height=6,
        fill="#D8CBA8", opacity=75, stroke=NONE, radius=3)
d.shape("ellipse", "Ghost glow", x=600, y=330, width=120, height=105,
        fill=GHOST, opacity=12, stroke=NONE)
# afterimage: dashed echo of the missing packet, doubled slightly offset
d.shape("rectangle", "Ghost echo", x=620, y=336, width=80, height=88,
        fill=NONE, stroke=GHOST, strokeWidth=3, dash=[10, 9], opacity=30, radius=8)
d.shape("rectangle", "Ghost outline", x=614, y=342, width=80, height=88,
        fill=NONE, stroke=GHOST, strokeWidth=3.5, dash=[10, 9], opacity=75, radius=8)
d.path("M620,350 L654,376 L688,350", "Ghost flap", fill=NONE,
       stroke=GHOST, strokeWidth=3, dash=[7, 7], opacity=55)
# sparkles where it was
for i, (x, y, s) in enumerate([(606, 330, 12), (700, 352, 9), (664, 316, 8)]):
    d.path(f"M{x},{y-s} L{x},{y+s} M{x-s},{y} L{x+s},{y}",
           f"Sparkle {i+1}", fill=NONE, stroke=GHOST, strokeWidth=3,
           cap="round", opacity=60)
# cobweb bridging the gap edge — nobody's disturbed it
d.path("M598,372 C606,392 610,410 612,426", "Cobweb", fill=NONE,
       stroke="#B8C4C0", strokeWidth=2, opacity=35)
# stray dust motes in the air
for i, (x, y, s) in enumerate([(575, 300, 4), (630, 260, 3), (700, 300, 4), (590, 420, 3)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=s*2, height=s*2,
            fill="#C8D4CE", opacity=30, stroke=NONE)

# --- the clerk, visor on, duster raised ----------------------------------------
d.shape("ellipse", "Figure shadow", x=236, y=722, width=210, height=26,
        fill="#16242C", opacity=60, stroke=NONE)
# legs + shoes
d.path("M308,575 C302,620 298,660 296,702", "Leg L",
       fill=NONE, stroke="#3E4654", strokeWidth=34, cap="round")
d.path("M342,575 C348,620 354,660 360,702", "Leg R",
       fill=NONE, stroke="#3E4654", strokeWidth=34, cap="round")
d.shape("rectangle", "Shoe L", x=262, y=696, width=72, height=32,
        fill=SHOE, stroke=INK, strokeWidth=5, radius=13)
d.shape("rectangle", "Shoe R", x=332, y=696, width=72, height=32,
        fill=SHOE, stroke=INK, strokeWidth=5, radius=13)
# waistcoat over shirt
d.path("M276,575 C268,505 274,452 296,430 C316,412 352,412 372,430 "
       "C392,452 398,505 390,575 C360,588 306,588 276,575 Z",
       "Vest", fill=VEST, stroke=INK, strokeWidth=6, join="round")
d.path("M296,430 L334,470 L372,430", "Shirt collar", fill=NONE, stroke=INK,
       strokeWidth=4, join="round")
d.shape("ellipse", "Shirt V", x=316, y=430, width=36, height=44,
        fill=SHIRT, stroke=NONE)
d.path("M334,470 L334,570", "Vest placket", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=55)
for i, y in enumerate([492, 522, 552]):
    d.shape("ellipse", f"Vest button {i+1}", x=330, y=y, width=8, height=8,
            fill="#1A1E24", stroke=NONE)
# left arm down, holding a folded docket
d.path("M292,442 C272,478 266,540 274,600", "Sleeve L",
       fill=NONE, stroke="#4A5462", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand L", x=262, y=592, width=30, height=26,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M236,596 L290,588 L296,624 L242,632 Z", "Docket",
       fill="#D8CBA8", stroke=INK, strokeWidth=3.5, join="round")
d.path("M246,606 L282,601 M248,616 L284,611", "Docket lines", fill=NONE,
       stroke="#8A7C62", strokeWidth=2.5, opacity=70)
# right arm raised toward the shelf gap
d.path("M372,442 C402,428 424,412 440,392", "Sleeve R",
       fill=NONE, stroke="#4A5462", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand R", x=428, y=378, width=30, height=26,
        fill=SKIN, stroke=INK, strokeWidth=4)
# feather duster: handle + plume fanning over the empty spot
d.path("M446,386 L522,326", "Duster handle", fill=NONE,
       stroke="#7A5C3E", strokeWidth=8, cap="round")
for i, (x2, y2) in enumerate([(560, 296), (575, 306), (588, 322), (578, 282), (598, 306)]):
    d.path(f"M522,326 C{538 + i*4},{310 - i*2} {x2 - 12},{y2 + 6} {x2},{y2}",
           f"Plume {i+1}", fill=NONE, stroke="#C8A96E", strokeWidth=7,
           cap="round", opacity=80)
for i, (x2, y2) in enumerate([(566, 302), (582, 316), (592, 296)]):
    d.path(f"M524,330 C{544 + i*5},{316 - i*3} {x2 - 10},{y2 + 8} {x2},{y2}",
           f"Plume dark {i+1}", fill=NONE, stroke="#8A6C42", strokeWidth=4,
           cap="round", opacity=60)
# dust puffs kicked up at the shelf edge
d.shape("ellipse", "Dust puff 1", x=598, y=316, width=22, height=16,
        fill="#C8D4CE", opacity=30, stroke=NONE)
d.shape("ellipse", "Dust puff 2", x=614, y=300, width=14, height=11,
        fill="#C8D4CE", opacity=25, stroke=NONE)

# head, eyes lifted to the gap
d.shape("ellipse", "Head", x=276, y=318, width=108, height=96,
        fill=SKIN, stroke=INK, strokeWidth=6)
# clerk's eyeshade visor, translucent green, brim toward the shelf
d.path("M292,336 C320,326 360,324 392,334 L392,352 C360,342 320,344 292,352 Z",
       "Visor", fill="#63B07E", opacity=50, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Eye L", x=312, y=356, width=14, height=16, fill="#2A2024", stroke=NONE)
d.shape("ellipse", "Eye R", x=346, y=356, width=14, height=16, fill="#2A2024", stroke=NONE)
d.shape("ellipse", "Glint L", x=317, y=358, width=4, height=4, fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=351, y=358, width=4, height=4, fill="#FFFFFF", opacity=80, stroke=NONE)
d.path("M308,342 C314,336 324,335 330,338", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round", opacity=75)
# quiet, resigned mouth
d.path("M316,392 C326,396 340,396 348,391", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek", x=352, y=376, width=18, height=9,
        fill="#D98C7A", opacity=35, stroke=NONE)

# --- name + role ---------------------------------------------------------------
d.text("AFTERIMAGE CLERK", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#DCE8E4", justify="center")
d.text(" ".join("KEEPER OF THE ABSENT PROOF"), "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#8FB8AC", justify="center")

d.finish("432.afterimage-clerk-V1R00")
