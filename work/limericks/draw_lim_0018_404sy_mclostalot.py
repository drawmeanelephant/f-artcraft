#!/usr/bin/env python3
"""LIM-0018 404Sy McLostalot — limerick plate V1R00. The phantom navigator:
a glowing portal that opens onto pure void, a sitemap sketched in dust
whose every branch dead-ends, breadcrumbs eaten mid-trail, a broken
anchor glyph, and 404sy mid-stride into nowhere with his upside-down
map. Warm dark ink, translucent routing lines fading into darkness.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0018 404Sy McLostalot — Limerick Plate", 1000, 1000)

INK = "#241A10"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E130B"}, {"offset": 1, "color": "#0D0805"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#55402A"}, {"offset": 0.7, "color": "#332517"},
    {"offset": 1, "color": "#1A1109"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0B468", "opacity": 0.38},
    {"offset": 0.55, "color": "#C8863E", "opacity": 0.18},
    {"offset": 1, "color": "#C8863E", "opacity": 0}]}}
VOID = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#150E08"}, {"offset": 1, "color": "#070402"}]}}
FRAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C89A5E"}, {"offset": 1, "color": "#7A5A30"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A6440"}, {"offset": 1, "color": "#4A3A20"}]}}
FACE = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8D6B0"}, {"offset": 1, "color": "#C4A87C"}]}}
MAP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8DCBC"}, {"offset": 1, "color": "#C4B48E"}]}}
DUST = "#8A7250"
CREAM = "#ECDCBE"
TAN = "#B08A5C"
NOPE = "#C24838"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5233", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4AC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(190, 236, 8), (802, 230, 7), (162, 522, 9),
                               (836, 540, 8), (244, 764, 7), (758, 748, 9),
                               (134, 392, 6), (862, 392, 7), (392, 112, 7),
                               (612, 112, 8), (336, 818, 6), (664, 814, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A3A26", opacity=45, stroke=NONE)

# --- ghost "404" hanging in the dark, barely there -------------------------------
g = d.text("404", "Ghost code", x=500, y=220, size=118,
           font="Source Sans 3", color="#6A5236", justify="center")
if g and g.get("id"):
    d.cmd("object.setProps", "ghost code fade", ids=[g["id"]], opacity=14)

# --- the sitemap drawn in dust: a branching tree that dies -----------------------
# root node top-center, three branches — every one dead-ending or looping
d.path("M500,268 L500,300", "Site root", fill=NONE, stroke=DUST,
       strokeWidth=3, opacity=50)
# branch left: two dead stubs
d.path("M500,300 C430,306 360,300 300,318", "Site L", fill=NONE,
       stroke=DUST, strokeWidth=3, opacity=45, dash=[9, 7])
d.path("M300,318 L256,318 M292,308 L300,318 L292,328", "Site L arrow",
       fill=NONE, stroke=DUST, strokeWidth=3, opacity=45)
d.path("M244,308 L266,330 M266,308 L244,330", "Site L X", fill=NONE,
       stroke=NOPE, strokeWidth=4, opacity=65, cap="round")
# branch right: splits again then dies twice
d.path("M500,300 C570,306 640,300 700,318", "Site R", fill=NONE,
       stroke=DUST, strokeWidth=3, opacity=45, dash=[9, 7])
d.path("M700,318 C730,322 748,334 756,352 M700,318 C726,310 748,308 768,310",
       "Site R forks", fill=NONE, stroke=DUST, strokeWidth=3, opacity=40)
d.path("M750,346 L772,368 M772,346 L750,368", "Site R X1", fill=NONE,
       stroke=NOPE, strokeWidth=4, opacity=65, cap="round")
d.path("M762,300 L784,322 M784,300 L762,322", "Site R X2", fill=NONE,
       stroke=NOPE, strokeWidth=4, opacity=65, cap="round")
# center branch: a redirect orphan looping back into itself forever
d.path("M500,300 C540,320 548,352 530,374 C516,392 496,388 492,370",
       "Redirect loop", fill=NONE, stroke=DUST, strokeWidth=3,
       opacity=50, dash=[9, 7])
d.path("M492,370 L490,358 M492,370 L504,368", "Redirect head", fill=NONE,
       stroke=DUST, strokeWidth=3, opacity=50)
# node dots where branches begin
for i, (nx, ny) in enumerate([(500, 300), (300, 318), (700, 318)]):
    d.shape("ellipse", f"Site node {i+1}", x=nx - 5, y=ny - 5, width=10,
            height=10, fill=DUST, opacity=55, stroke=NONE)

# --- the broken anchor glyph, upper left ------------------------------------------
# two chain-link halves pulled apart, spark in the gap
d.path("M196,420 C176,420 160,436 160,456 C160,476 176,492 196,492 "
       "L214,492", "Link half L", fill=NONE, stroke="#9A7E58",
       strokeWidth=11, opacity=70, cap="round")
d.path("M262,420 C282,420 298,436 298,456 C298,476 282,492 262,492 "
       "L244,492", "Link half R", fill=NONE, stroke="#9A7E58",
       strokeWidth=11, opacity=70, cap="round")
d.path("M232,442 L226,452 L236,458 L228,470", "Link spark", fill=NONE,
       stroke="#F0C070", strokeWidth=4, opacity=85, cap="round")
d.shape("ellipse", "Link spark dot", x=226, y=452, width=6, height=6,
        fill="#F0C070", opacity=80, stroke=NONE)

# --- the portal to nowhere ---------------------------------------------------------
# glow spilling out around and under the door
d.shape("ellipse", "Portal glow", x=330, y=360, width=340, height=400,
        fill=GLOW, stroke=NONE)
d.shape("ellipse", "Portal ground glow", x=370, y=680, width=260, height=56,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E8A858", "opacity": 0.30},
            {"offset": 1, "color": "#E8A858", "opacity": 0}]}},
        stroke=NONE)
# doorframe: arch top, open at the base
d.path("M436,668 L436,436 A64,64 0 0 1 564,436 L564,668",
       "Portal frame", fill=NONE, stroke=FRAME, strokeWidth=14,
       cap="round")
# the void inside — a door that opens on nothing
d.path("M436,668 L436,436 A64,64 0 0 1 564,436 L564,668 Z",
       "Portal void", fill=VOID, stroke=NONE)
# faint dust drifting inside the void
for i, (vx, vy, vw, vo) in enumerate([(472, 480, 5, 30), (516, 540, 4, 24),
                                      (492, 600, 5, 28), (524, 470, 4, 20),
                                      (462, 560, 4, 22), (506, 640, 5, 18)]):
    d.shape("ellipse", f"Void dust {i+1}", x=vx, y=vy, width=vw, height=vw,
            fill="#E8C890", opacity=vo, stroke=NONE)
# worn threshold step
d.shape("ellipse", "Portal step", x=420, y=656, width=160, height=22,
        fill="#1A1008", opacity=75, stroke=NONE)
# frame highlight catching the glow on the inner edge
d.path("M448,660 L448,444 A52,52 0 0 1 500,392", "Frame sheen", fill=NONE,
       stroke="#F0C88E", strokeWidth=3, opacity=55, cap="round")

# --- 404sy mid-stride into nowhere ---------------------------------------------------
# shadow on the threshold
d.shape("ellipse", "404sy shadow", x=596, y=676, width=130, height=22,
        fill="#0C0704", opacity=55, stroke=NONE)
# trailing leg, leading leg
d.path("M636,616 L622,672", "Leg L", fill=NONE, stroke="#3E3222",
       strokeWidth=15, cap="round")
d.path("M664,616 L684,666", "Leg R", fill=NONE, stroke="#3E3222",
       strokeWidth=15, cap="round")
d.shape("ellipse", "Boot L", x=600, y=662, width=34, height=16,
        fill="#2E2418", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Boot R", x=674, y=656, width=36, height=17,
        fill="#2E2418", stroke=INK, strokeWidth=4)
# coat, leaning into the step
d.path("M636,486 C680,478 710,510 714,560 C718,606 706,632 698,640 "
       "L614,632 C608,600 606,540 618,506 C622,494 628,488 636,486 Z",
       "Coat", fill=COAT, stroke=INK, strokeWidth=6, join="round")
d.path("M652,494 L646,626", "Coat seam", fill=NONE, stroke="#C9B47E",
       strokeWidth=3, opacity=50)
d.path("M618,624 L700,632", "Coat hem", fill=NONE, stroke="#C9B47E",
       strokeWidth=3, opacity=45)
# head, tipped up toward the void like it might explain itself
d.shape("ellipse", "Head", x=622, y=408, width=92, height=80,
        fill=FACE, stroke=INK, strokeWidth=5)
# traveller's cap, tipped
d.path("M624,428 C624,392 712,390 714,426 L700,426 C698,406 640,406 640,428 Z",
       "Cap", fill=COAT, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Cap button", x=662, y=396, width=12, height=9,
        fill=COAT, stroke=INK, strokeWidth=3)
# bewildered face: one round eye, one squint, raised brow
d.shape("ellipse", "Eye L", x=646, y=448, width=14, height=17, fill="#FBF6E8",
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=651, y=453, width=6, height=7, fill=INK,
        stroke=NONE)
d.path("M684,450 L704,452", "Eye R squint", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M640,436 C648,430 658,429 664,432", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.path("M682,432 C692,424 704,424 710,430", "Brow R raised", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.path("M650,474 C658,470 664,478 672,473 C680,468 686,476 694,472",
       "Uncertain mouth", fill=NONE, stroke=INK, strokeWidth=3,
       cap="round")
# arm extended, holding the upside-down map toward the portal
d.path("M618,540 C596,548 578,562 570,580", "Arm map", fill=NONE,
       stroke="#5A4826", strokeWidth=16, cap="round")
d.shape("ellipse", "Hand map", x=556, y=570, width=22, height=20,
        fill=FACE, stroke=INK, strokeWidth=4)
# the upside-down map, consulted at the door of nothing
d.path("M470,540 L584,514 L606,596 L490,622 Z", "Map sheet", fill=MAP,
       stroke=INK, strokeWidth=5, join="round")
d.path("M536,528 L560,608", "Map fold", fill=NONE, stroke="#B4A488",
       strokeWidth=2.5, opacity=70)
# route wandering to an X at the map's lower edge (its "top", held inverted)
d.path("M580,544 C556,540 538,552 542,570 C546,588 522,596 504,590",
       "Map route", fill=NONE, stroke="#8A94A0", strokeWidth=4,
       cap="round", dash=[7, 6])
d.path("M496,580 L516,600 M516,580 L496,600", "Map X", fill=NONE,
       stroke=NOPE, strokeWidth=5, cap="round")
# compass rose, N pointing down because the map is upside down
d.shape("ellipse", "Compass ring", x=554, y=566, width=30, height=30,
        fill=NONE, stroke="#8A94A0", strokeWidth=2.5, opacity=90)
d.path("M569,596 L563,578 L575,578 Z", "Compass needle", fill="#8A94A0",
       stroke=NONE, opacity=90)
t = d.text("N", "Compass N", x=569, y=574, size=10, font="Virelai Sans",
           color="#8A94A0", justify="center")
if t and t.get("id"):
    d.cmd("object.setProps", "compass N fade", ids=[t["id"]], opacity=80)
# the little question that follows him everywhere
d.text("?", "Question", x=742, y=398, size=40, font="Virelai Sans",
       color="#C9BCA0", justify="center")

# --- breadcrumbs: the trail eats itself ------------------------------------------------
# crumbs curve in from the lower left, fat and confident at first
crumbs = [(262, 700, 7, 80), (296, 716, 7, 78), (330, 726, 6, 72),
          (364, 730, 6, 66)]
for i, (cx, cy, cw, co) in enumerate(crumbs):
    d.shape("ellipse", f"Crumb {i+1}", x=cx, y=cy, width=cw, height=cw - 1,
            fill="#E4D4A8", opacity=co, stroke=NONE)
# then a half-eaten one, bitten mid-step
d.path("M398,732 A7,6 0 1 1 404,724 L400,728 L406,730 Z", "Bitten crumb",
       fill="#E4D4A8", opacity=55, stroke=NONE)
# then crumbs shrink and scatter — something got to them
for i, (cx, cy, cw, co) in enumerate([(420, 728, 4, 40), (436, 722, 3, 30),
                                      (450, 734, 3, 22)]):
    d.shape("ellipse", f"Crumb gone {i+1}", x=cx, y=cy, width=cw,
            height=cw, fill="#E4D4A8", opacity=co, stroke=NONE)
# a second redirect orphan curling near the rim, low in the plate
d.path("M196,640 C170,660 168,690 188,706 C204,718 222,712 226,696",
       "Orphan loop", fill=NONE, stroke=DUST, strokeWidth=3, opacity=40,
       dash=[8, 7])
d.path("M226,696 L228,684 M226,696 L214,694", "Orphan head", fill=NONE,
       stroke=DUST, strokeWidth=3, opacity=40)

# --- captions -------------------------------------------------------------------------
k1 = d.text("EVERY CLICK IS A GAMBLE,", "Key line 1", x=500, y=836,
            size=23, font="Virelai Sans", color="#C9AE82",
            justify="center")
k2 = d.text("DOWN A NEW NAVIGATION SHAMBLE.", "Key line 2", x=500,
            y=868, size=23, font="Virelai Sans", color="#C9AE82",
            justify="center")
for i, k in enumerate([k1, k2]):
    if k and k.get("id"):
        d.cmd("text.setStyle", f"key{i+1} tracking", ids=[k["id"]],
              tracking=140)
nm = d.text("404SY MCLOSTALOT", "Name", x=500, y=930, size=58,
            font="Virelai Sans", color=CREAM, justify="center")
# Virelai Sans has no digit glyphs: "404" falls back to Source Sans 3
if nm and nm.get("id"):
    d.cmd("text.setStyle", "name digit fallback", ids=[nm["id"]],
          start=0, end=3, font="Source Sans 3")
r = d.text("ROUTING SUCCESS CONFIRMED", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=190)

d.finish("lim-0018-404sy-mclostalot-V1R00")
