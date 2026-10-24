#!/usr/bin/env python3
"""Badgevine — mascot portrait V1R00.
A torso of accretion: lapels buried under credential badges, new vines
sprouting through them and climbing past the collar. Underneath, per the
teardown record, the original lapel is intact — and the name tag is
blank. 1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Badgevine — Mascot Portrait", 1000, 1000)

INK = "#2E2433"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2026"}, {"offset": 1, "color": "#0B0C12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#57605C"}, {"offset": 0.7, "color": "#3A423E"},
    {"offset": 1, "color": "#1A1E1C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4640"}, {"offset": 1, "color": "#141815"}]}}
SUIT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5264"}, {"offset": 1, "color": "#2C2E3E"}]}}
LAPEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E6278"}, {"offset": 1, "color": "#383A4C"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B9AE9C"}, {"offset": 1, "color": "#7A7060"}]}}
VINE = "#5E9A54"
VINE_HI = "#8CC477"
LEAF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7FBE6E"}, {"offset": 1, "color": "#3F7A3C"}]}}

def leaf(cx, cy, ang, s, label, op=100):
    """leaf s long, growing along ang degrees (0 = right, -90 = up)"""
    t = math.radians(ang)
    ux, uy = math.cos(t), math.sin(t)
    px, py = -uy, ux
    tip = (cx + ux * s, cy + uy * s)
    c1 = (cx + ux * s * 0.35 + px * s * 0.34, cy + uy * s * 0.35 + py * s * 0.34)
    c2 = (cx + ux * s * 0.8 + px * s * 0.22, cy + uy * s * 0.8 + py * s * 0.22)
    c3 = (cx + ux * s * 0.8 - px * s * 0.22, cy + uy * s * 0.8 - py * s * 0.22)
    c4 = (cx + ux * s * 0.35 - px * s * 0.34, cy + uy * s * 0.35 - py * s * 0.34)
    d.path(f"M{cx},{cy} C{c1[0]},{c1[1]} {c2[0]},{c2[1]} {tip[0]},{tip[1]} "
           f"C{c3[0]},{c3[1]} {c4[0]},{c4[1]} {cx},{cy} Z",
           label, fill=LEAF_GRAD, stroke=INK, strokeWidth=2.5, opacity=op)

def star(cx, cy, r, label, fill, op=100):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        t = math.radians(-90 + i * 36)
        pts.append(f"{'M' if i == 0 else 'L'}{cx + rr * math.cos(t):.1f},{cy + rr * math.sin(t):.1f}")
    d.path(" ".join(pts) + " Z", label, fill=fill, stroke=INK,
           strokeWidth=2.5, opacity=op)

def medal(cx, cy, ribbon, disc, label):
    d.path(f"M{cx-8},{cy-16} L{cx+8},{cy-16} L{cx+5},{cy-3} L{cx-5},{cy-3} Z",
           f"{label} ribbon", fill=ribbon, stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"{label} disc", x=cx-10, y=cy-3, width=20, height=20,
            fill=disc, stroke=INK, strokeWidth=2.5)

def shield(cx, cy, fill, label):
    d.path(f"M{cx-11},{cy-12} L{cx+11},{cy-12} L{cx+11},{cy+1} "
           f"C{cx+11},{cy+10} {cx+4},{cy+14} {cx},{cy+16} "
           f"C{cx-4},{cy+14} {cx-11},{cy+10} {cx-11},{cy+1} Z",
           label, fill=fill, stroke=INK, strokeWidth=2.5)

def pin(cx, cy, fill, label, w=28):
    d.shape("rectangle", label, x=cx-w/2, y=cy-4, width=w, height=8,
            radius=4, fill=fill, stroke=INK, strokeWidth=2.5)

GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0CC6A"}, {"offset": 1, "color": "#B8862E"}]}}
BRONZE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D09454"}, {"offset": 1, "color": "#8A5C2C"}]}}
SILVER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D4D8E2"}, {"offset": 1, "color": "#8E94A6"}]}}
ENAMEL_R = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D46A5E"}, {"offset": 1, "color": "#8E3A34"}]}}
ENAMEL_B = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E8CD4"}, {"offset": 1, "color": "#3C5088"}]}}
ENAMEL_G = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#74B076"}, {"offset": 1, "color": "#3C6C40"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#76847C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E0D4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(210,240,7),(800,244,8),(168,528,8),(834,556,7),
                               (258,762,8),(748,750,7),(146,400,6),(854,404,7),
                               (400,120,7),(610,118,8),(344,820,6),(664,816,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#424C44", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0A08",
       strokeWidth=4, opacity=70)

# --- the bust ---------------------------------------------------------------------
d.shape("ellipse", "Bust shadow", x=320, y=694, width=380, height=30,
        fill="#060410", opacity=50, stroke=NONE)
# blank head — what's underneath is not on file
d.shape("ellipse", "Head", x=447, y=208, width=130, height=148,
        fill=HEAD_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Head sheen", x=466, y=224, width=56, height=28,
        fill="#E8E0CE", opacity=13, stroke=NONE)
# collar
d.path("M452,352 L512,392 L572,352 L586,384 L512,434 L438,384 Z", "Collar",
       fill="#C9BFA8", stroke=INK, strokeWidth=4, join="round")
# jacket: shoulders rolling to the hem at the floor
d.path("M438,380 C380,392 340,420 322,470 C308,540 302,620 300,700 "
       "L724,700 C722,620 716,540 702,470 C684,420 644,392 586,380 "
       "L572,352 L512,392 L452,352 Z",
       "Jacket", fill=SUIT_GRAD, stroke=INK, strokeWidth=6, join="round")
# shirt wedge between the lapels
d.path("M480,388 L512,436 L544,388 L560,420 L512,520 L464,420 Z",
       "Shirt V", fill="#AFA78E", stroke=INK, strokeWidth=3, opacity=90)
# lapels
d.path("M452,352 L512,436 L470,560 L408,470 L420,392 Z",
       "Lapel L", fill=LAPEL_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M572,352 L512,436 L554,560 L616,470 L604,392 Z",
       "Lapel R", fill=LAPEL_GRAD, stroke=INK, strokeWidth=4, join="round")
# the blank name tag, intact beneath the accretion
d.shape("rectangle", "Blank name tag", x=330, y=560, width=64, height=22,
        radius=4, fill="#DDD6C2", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Name tag shade", x=356, y=560, width=38, height=22,
        radius=4, fill="#8E94A6", opacity=45, stroke=NONE)

# --- credential badges, dense on both lapels --------------------------------------
# left lapel field
medal(430, 412, ENAMEL_R, GOLD, "B1")
star(466, 452, 13, "B2", SILVER)
shield(438, 490, ENAMEL_B, "B3")
pin(452, 530, GOLD, "B4", 30)
medal(486, 500, ENAMEL_B, BRONZE, "B5")
star(424, 540, 11, "B6", GOLD)
# right lapel field — denser; the vine is thickest where function is thinnest
medal(594, 412, ENAMEL_G, SILVER, "B7")
shield(556, 456, ENAMEL_R, "B8")
star(590, 496, 13, "B9", GOLD)
pin(568, 530, SILVER, "B10", 32)
medal(614, 548, ENAMEL_R, BRONZE, "B11")
shield(548, 500, GOLD, "B12")
pin(596, 452, ENAMEL_B, "B13", 26)
# chest scatter, migrating off the lapels
star(368, 470, 11, "B14", BRONZE)
pin(660, 480, GOLD, "B15", 26)
medal(652, 560, ENAMEL_B, GOLD, "B16")
shield(382, 520, ENAMEL_G, "B17")
pin(424, 590, ENAMEL_R, "B18", 24)
star(640, 510, 10, "B19", SILVER)
# lower field: the accretion keeps spreading downward
medal(470, 618, ENAMEL_G, SILVER, "B20")
shield(560, 630, ENAMEL_B, "B21")
pin(352, 630, BRONZE, "B22", 22)
star(610, 640, 11, "B23", ENAMEL_R)
shield(664, 640, GOLD, "B24")
pin(520, 668, SILVER, "B25", 22)

# --- the vine: new growth out of the lapel ----------------------------------------
# main stem: rooted low on the chest, climbing the right lapel to the collar
d.path("M470,690 C500,640 480,600 520,560 C560,520 600,530 616,470 "
       "C628,424 612,392 634,352 C650,322 676,310 692,290",
       "Vine stem", fill=NONE, stroke=VINE, strokeWidth=7, cap="round")
d.path("M470,690 C500,640 480,600 520,560 C560,520 600,530 616,470 "
       "C628,424 612,392 634,352 C650,322 676,310 692,290",
       "Vine hi", fill=NONE, stroke=VINE_HI, strokeWidth=2.5, cap="round", opacity=70)
# second shoot, younger, reaching left across the shirt
d.path("M430,660 C420,610 444,580 430,540 C420,510 400,500 396,470",
       "Vine stem L", fill=NONE, stroke=VINE, strokeWidth=6, cap="round")
# tendril curls off the main stem
d.path("M616,470 C640,460 660,472 660,490 C660,504 646,510 636,502 "
       "C630,496 632,486 640,486",
       "Tendril", fill=NONE, stroke=VINE_HI, strokeWidth=3.5, cap="round", opacity=90)
# leaves along the stems
leaf(500, 640, -160, 34, "Leaf 1")
leaf(522, 556, -30, 36, "Leaf 2")
leaf(598, 528, 20, 34, "Leaf 3")
leaf(616, 462, -70, 32, "Leaf 4")
leaf(632, 388, -20, 30, "Leaf 5")
leaf(668, 318, -50, 30, "Leaf 6")
leaf(692, 292, -30, 26, "Leaf 7")
leaf(428, 596, -140, 30, "Leaf 8")
leaf(430, 536, -60, 28, "Leaf 9")
leaf(402, 486, -110, 26, "Leaf 10")
# two fresh sprouts on the badge field — a stripped lapel resprouts by Friday
leaf(560, 452, -60, 20, "Sprout 1", op=90)
leaf(452, 496, -30, 18, "Sprout 2", op=90)

# --- captions ----------------------------------------------------------------------
d.text("BADGEVINE", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E2E8DC", justify="center")
r = d.text("COMPETENCE BY VISUAL NOISE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FB4A0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("240.badgevine-V1R00")
