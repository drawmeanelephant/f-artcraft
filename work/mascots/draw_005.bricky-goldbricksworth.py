#!/usr/bin/env python3
"""Bricky Goldbricksworth — mascot portrait V1R00.
A goldbrick block of a clerk drafting forms by lanternlight at his desk,
filing cabinet on the left and a malfunctioning radiator clanking on the
right. Cheerfully inert: placid eyes, small content smile, pen mid-stroke.
Lantern glow pools over the desk. Night-office palette, warm dark ink.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Bricky Goldbricksworth — Mascot Portrait", 1000, 1000)

INK = "#241812"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1512"}, {"offset": 1, "color": "#050807"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A3E26"}, {"offset": 0.7, "color": "#282012"},
    {"offset": 1, "color": "#120E08"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#322814"}, {"offset": 1, "color": "#120E08"}]}}
BRICK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8925E"}, {"offset": 0.65, "color": "#B0653A"},
    {"offset": 1, "color": "#7C3E20"}]}}
MORTAR = "#5A3218"
METAL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6B6A58"}, {"offset": 0.55, "color": "#4E4D3E"},
    {"offset": 1, "color": "#2E2D24"}]}}
RAD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A7B5E"}, {"offset": 0.55, "color": "#5E5240"},
    {"offset": 1, "color": "#363024"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A4E2A"}, {"offset": 0.6, "color": "#543318"},
    {"offset": 1, "color": "#33200F"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E4C2"}, {"offset": 0.65, "color": "#DEC99E"},
    {"offset": 1, "color": "#BDA275"}]}}
FLAME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE9AE"}, {"offset": 0.55, "color": "#F0A848"},
    {"offset": 1, "color": "#C0661E"}]}}
AMBER = "#F0B45A"
BRASS = "#8A6A2E"
CREAM = "#F0E2C4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6038", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C890", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193, 233, 8), (801, 230, 7), (157, 524, 9),
                               (837, 544, 8), (247, 766, 7), (753, 749, 9),
                               (133, 393, 6), (864, 391, 7), (391, 113, 7),
                               (613, 110, 8), (333, 823, 6), (665, 821, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4C2E", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0906",
       strokeWidth=4, opacity=70)

# --- filing cabinet, left ---------------------------------------------------------
cx0, cy0, cw, ch = 188, 360, 116, 330
d.shape("ellipse", "Cabinet shadow", x=cx0 - 10, y=cy0 + ch - 4, width=cw + 20,
        height=20, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Cabinet body", x=cx0, y=cy0, width=cw, height=ch,
        radius=6, fill=METAL_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Cabinet top lip", x=cx0 - 4, y=cy0 - 8, width=cw + 8,
        height=14, radius=4, fill="#7A7962", stroke=INK, strokeWidth=3)
for j, dy in enumerate([cy0 + 16, cy0 + 116, cy0 + 216]):
    open_ = (j == 1)
    d.shape("rectangle", f"Drawer {j+1}", x=cx0 + 10, y=dy, width=cw - 20,
            height=86, radius=4, fill="#54533F" if not open_ else "#454430",
            stroke=INK, strokeWidth=3)
    d.shape("rectangle", f"Drawer label {j+1}", x=cx0 + 32, y=dy + 12,
            width=52, height=18, radius=2, fill="#C9BD96",
            stroke=INK, strokeWidth=2)
    d.path(f"M{cx0 + 38},{dy + 56} L{cx0 + 78},{dy + 56}", f"Drawer pull {j+1}",
           fill=NONE, stroke="#8A8970", strokeWidth=6, cap="round")
# the middle drawer rides open on a wedge of stale forms
d.path(f"M{cx0 + 12},{cy0 + 118} L{cx0 + cw - 12},{cy0 + 118} "
       f"L{cx0 + cw - 20},{cy0 + 96} L{cx0 + 20},{cy0 + 96} Z",
       "Drawer gap", fill="#1A1812", stroke=INK, strokeWidth=2.5)
for i, (px, pr) in enumerate([(cx0 + 30, -6), (cx0 + 56, 2), (cx0 + 80, 8)]):
    d.path(rot_rect_path(px, cy0 + 98, 40, 26, pr), f"Stuck form {i+1}",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2)
# a toppled pencil cup on the cabinet top
d.path(rot_rect_path(cx0 + 82, cy0 - 20, 34, 30, -24), "Pencil cup",
       fill="#6E5A3A", stroke=INK, strokeWidth=3)
for i, (dx_, deg) in enumerate([(-6, -40), (2, -18), (10, -52)]):
    d.path(f"M{cx0 + 78 + dx_},{cy0 - 30} L{cx0 + 78 + dx_ + 14 * math.cos(math.radians(deg)):.0f},"
           f"{cy0 - 30 + 14 * math.sin(math.radians(deg)):.0f}",
           f"Pencil {i+1}", fill=NONE, stroke="#C9A05A", strokeWidth=3.5,
           cap="round")

# --- radiator, right: malfunctioning ----------------------------------------------
rx0, ry0, rw, rh = 690, 470, 128, 222
d.shape("ellipse", "Rad shadow", x=rx0 - 8, y=ry0 + rh - 2, width=rw + 16,
        height=18, fill="#000000", opacity=30, stroke=NONE)
# feed pipe from the floor
d.path(f"M{rx0 + 18},{ry0 + rh} L{rx0 + 18},{ry0 + rh - 24} "
       f"Q{rx0 + 18},{ry0 + rh - 40} {rx0 + 34},{ry0 + rh - 40} L{rx0 + 34},{ry0 + 8}",
       "Feed pipe", fill=NONE, stroke="#5E5240", strokeWidth=12, cap="round")
# finned columns
for i in range(6):
    fx = rx0 + 6 + i * (rw / 6)
    d.path(f"M{fx + 4},{ry0 + 20} C{fx - 4},{ry0 + 60} {fx - 4},{ry0 + rh - 60} "
           f"{fx + 4},{ry0 + rh - 14} L{fx + rw / 6 - 6},{ry0 + rh - 14} "
           f"C{fx + rw / 6 + 2},{ry0 + rh - 60} {fx + rw / 6 + 2},{ry0 + 60} "
           f"{fx + rw / 6 - 6},{ry0 + 20} Z",
           f"Rad fin {i+1}", fill=RAD_GRAD, stroke=INK, strokeWidth=3)
# top rail + valve
d.shape("rectangle", "Rad rail", x=rx0, y=ry0, width=rw, height=18,
        radius=6, fill="#6E6250", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Valve wheel", x=rx0 + rw - 8, y=ry0 - 22, width=30,
        height=14, fill="#8A6A3A", stroke=INK, strokeWidth=3)
d.path(f"M{rx0 + rw + 7},{ry0 - 8} L{rx0 + rw + 7},{ry0 + 6}", "Valve stem",
       fill=NONE, stroke=INK, strokeWidth=4)
# the malfunction: a leaking joint spits steam and clanks
jx, jy = rx0 + 26, ry0 + 40
d.path(f"M{jx},{jy} C{jx - 16},{jy - 26} {jx - 6},{jy - 44} {jx - 20},{jy - 58}",
       "Rad steam", fill=NONE, stroke="#F2F0E8", strokeWidth=9, opacity=30,
       cap="round")
d.path(f"M{jx + 2},{jy} C{jx - 10},{jy - 22} {jx - 2},{jy - 38} {jx - 14},{jy - 50}",
       "Rad steam core", fill=NONE, stroke="#FFFFFF", strokeWidth=4,
       opacity=40, cap="round")
for i, (dx_, dy_) in enumerate([(30, -26), (46, -14), (38, 6)]):
    d.path(f"M{jx + dx_},{jy + dy_} L{jx + dx_ + 10},{jy + dy_ - 8}",
           f"Clank {i+1}", fill=NONE, stroke="#E8C890", strokeWidth=4,
           opacity=65, cap="round")
# a drip about to fall + the one that already did
d.shape("ellipse", "Drip", x=jx + 8, y=jy + 58, width=8, height=12,
        fill="#A8C8D8", stroke=NONE, opacity=80)
d.shape("ellipse", "Puddle", x=jx - 18, y=ry0 + rh - 6, width=52, height=12,
        fill="#4A6270", opacity=50, stroke=NONE)

# --- lantern glow behind Bricky (drawn before him so he sits inside it) -------------
lx, ly = 636, 520
d.shape("ellipse", "Lantern glow", x=lx - 200, y=ly - 180, width=400,
        height=370, fill=AMBER, opacity=8, stroke=NONE)
d.shape("ellipse", "Lantern glow core", x=lx - 90, y=ly - 88, width=180,
        height=176, fill=AMBER, opacity=13, stroke=NONE)

# --- Bricky: a goldbrick that shows up ----------------------------------------------
kx0, ky0, kw, kh = 400, 330, 190, 300
# body: a big soft-cornered brick
d.shape("rectangle", "Body", x=kx0, y=ky0, width=kw, height=kh, radius=26,
        fill=BRICK_GRAD, stroke=INK, strokeWidth=6)
# mortar courses: two horizontals, staggered verticals
d.path(f"M{kx0 + 4},{ky0 + 104} L{kx0 + kw - 4},{ky0 + 104}", "Course 1",
       fill=NONE, stroke=MORTAR, strokeWidth=4, opacity=75)
d.path(f"M{kx0 + 4},{ky0 + 208} L{kx0 + kw - 4},{ky0 + 208}", "Course 2",
       fill=NONE, stroke=MORTAR, strokeWidth=4, opacity=75)
for i, vx in enumerate([kx0 + 62, kx0 + 128]):
    d.path(f"M{vx},{ky0 + 104} L{vx},{ky0 + 208}", f"Joint top {i+1}",
           fill=NONE, stroke=MORTAR, strokeWidth=4, opacity=75)
for i, vx in enumerate([kx0 + 95]):
    d.path(f"M{vx},{ky0 + 208} L{vx},{ky0 + kh - 4}", f"Joint bot {i+1}",
           fill=NONE, stroke=MORTAR, strokeWidth=4, opacity=75)
# worn edges: pale chips + one hairline crack that means nothing to him
d.path(f"M{kx0 + 30},{ky0 + 6} L{kx0 + 58},{ky0 + 6}", "Edge chip 1",
       fill=NONE, stroke="#E8B07E", strokeWidth=3, opacity=60, cap="round")
d.path(f"M{kx0 + kw - 66},{ky0 + kh - 8} L{kx0 + kw - 38},{ky0 + kh - 8}",
       "Edge chip 2", fill=NONE, stroke="#E8B07E", strokeWidth=3,
       opacity=60, cap="round")
d.path(f"M{kx0 + kw - 24},{ky0 + 40} L{kx0 + kw - 36},{ky0 + 66} "
       f"L{kx0 + kw - 22},{ky0 + 88}", "Hairline", fill=NONE,
       stroke=MORTAR, strokeWidth=2.5, opacity=60, cap="round", join="round")
# soft volume: top sheen + bottom shade
d.shape("ellipse", "Top sheen", x=kx0 + 30, y=ky0 + 12, width=120,
        height=26, fill="#FFFFFF", opacity=15, stroke=NONE)
d.shape("ellipse", "Base shade", x=kx0 + 20, y=ky0 + kh - 44, width=kw - 40,
        height=32, fill="#5E3018", opacity=30, stroke=NONE)

# face: cheerfully inert — level eyes, tiny placid smile
for i, cx in enumerate([kx0 + 62, kx0 + 128]):
    d.shape("ellipse", f"Eye {i+1}", x=cx - 13, y=ky0 + 56, width=26,
            height=30, fill="#1E1410", stroke=NONE)
    d.shape("ellipse", f"Glint {i+1}", x=cx - 6, y=ky0 + 62, width=7,
            height=7, fill="#FFFFFF", opacity=85, stroke=NONE)
# level brows — nothing is on fire, officially
d.path(f"M{kx0 + 40},{ky0 + 44} C{kx0 + 52},{ky0 + 38} {kx0 + 68},{ky0 + 38} {kx0 + 78},{ky0 + 44}",
       "Brow L", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path(f"M{kx0 + 108},{ky0 + 44} C{kx0 + 118},{ky0 + 38} {kx0 + 134},{ky0 + 38} {kx0 + 144},{ky0 + 44}",
       "Brow R", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path(f"M{kx0 + 72},{ky0 + 88} C{kx0 + 86},{ky0 + 98} {kx0 + 104},{ky0 + 98} {kx0 + 116},{ky0 + 88}",
       "Smile", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# rosy brick cheeks
for lbl, cx in [("Cheek L", kx0 + 34), ("Cheek R", kx0 + 156)]:
    d.shape("ellipse", lbl, x=cx - 14, y=ky0 + 80, width=28, height=16,
            fill="#D87A50", opacity=35, stroke=NONE)

# --- the desk ----------------------------------------------------------------------
dx0, dy0, dw, dh = 310, 590, 372, 108
d.shape("ellipse", "Desk shadow", x=dx0 - 14, y=dy0 + dh - 4, width=dw + 28,
        height=22, fill="#000000", opacity=35, stroke=NONE)
# desktop slab + front panel
d.shape("rectangle", "Desk top", x=dx0 - 10, y=dy0 - 16, width=dw + 20,
        height=26, radius=8, fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Desk front", x=dx0, y=dy0 + 8, width=dw, height=dh - 8,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#5E3C1E"}, {"offset": 1, "color": "#33200F"}]}},
        stroke=INK, strokeWidth=4)
# a modesty-panel drawer with a dull brass pull
d.shape("rectangle", "Desk drawer", x=dx0 + 120, y=dy0 + 40, width=130,
        height=44, radius=5, fill="#4A2E14", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Drawer pull", x=dx0 + 178, y=dy0 + 56, width=16,
        height=10, fill=BRASS, stroke=INK, strokeWidth=2)

# the form he's drafting — flat on the desk, pen touching it
fx, fy = dx0 + 66, dy0 - 22
d.path(rot_rect_path(fx + 3, fy + 4, 96, 64, -6), "Form shadow",
       fill="#000000", opacity=25, stroke=NONE)
d.path(rot_rect_path(fx, fy, 96, 64, -6), "Form", fill=PAPER_GRAD,
       stroke=INK, strokeWidth=3)
t = math.radians(-6); c_, s_ = math.cos(t), math.sin(t)
for k in range(3):
    lw = 62 - k * 8
    ox = -20 + k * 16
    lx, lyy = fx - ox * s_, fy + ox * c_
    d.path(rot_rect_path(lx, lyy, lw, 3, -6),
           f"Form line {k+1}", fill=INK, opacity=50, stroke=NONE)
d.text("FORM", "Form title", x=fx, y=fy - 20, size=10,
       font="Virelai Sans", color=INK, justify="center")

# Bricky's arms reach the desk: left rests, right holds the pen
d.path(f"M{kx0 + 30},{ky0 + 230} C{kx0 - 10},{ky0 + 252} {dx0 + 20},{dy0 - 40} "
       f"{dx0 + 44},{dy0 - 26}", "Arm L", fill=NONE, stroke="#B0653A",
       strokeWidth=26, cap="round")
d.shape("ellipse", "Hand L", x=dx0 + 30, y=dy0 - 44, width=36, height=30,
        fill="#C87848", stroke=INK, strokeWidth=4)
d.path(f"M{kx0 + kw - 30},{ky0 + 228} C{kx0 + kw + 8},{ky0 + 252} {fx + 60},{fy - 60} "
       f"{fx + 46},{fy - 34}", "Arm R", fill=NONE, stroke="#B0653A",
       strokeWidth=26, cap="round")
d.shape("ellipse", "Hand R", x=fx + 34, y=fy - 44, width=36, height=30,
        fill="#C87848", stroke=INK, strokeWidth=4)
# the pen: a dipped nib mid-stroke
d.path(f"M{fx + 62},{fy - 58} L{fx + 44},{fy - 6}", "Pen shaft", fill=NONE,
       stroke="#3A2A18", strokeWidth=4.5, cap="round")
d.path(f"M{fx + 44},{fy - 6} L{fx + 40},{fy + 4} L{fx + 48},{fy - 2} Z",
       "Nib", fill=BRASS, stroke=INK, strokeWidth=2)
# ink pot at the desk's left corner
d.shape("ellipse", "Ink pot", x=dx0 + 8, y=dy0 - 34, width=30, height=26,
        fill="#2A2E38", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Ink mouth", x=dx0 + 13, y=dy0 - 32, width=20, height=8,
        fill="#10121A", stroke=INK, strokeWidth=2)

# --- the lantern, right end of the desk ----------------------------------------------
d.shape("ellipse", "Lantern shadow", x=lx - 30, y=dy0 - 12, width=60,
        height=14, fill="#000000", opacity=30, stroke=NONE)
# base, glass chimney, flame, cap, handle
d.shape("ellipse", "Lantern base", x=lx - 24, y=ly + 44, width=48, height=20,
        fill=BRASS, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Lantern foot", x=lx - 20, y=ly + 56, width=40,
        height=10, radius=3, fill="#6E5224", stroke=INK, strokeWidth=3)
d.path(f"M{lx - 16},{ly + 44} C{lx - 22},{ly + 10} {lx - 14},{ly - 14} "
       f"{lx - 8},{ly - 22} L{lx + 8},{ly - 22} C{lx + 14},{ly - 14} "
       f"{lx + 22},{ly + 10} {lx + 16},{ly + 44} Z",
       "Chimney", fill={"gradient": {"kind": "radial", "stops": [
           {"offset": 0, "color": "#FFE9AE", "opacity": 0.85},
           {"offset": 0.7, "color": "#F0B45A", "opacity": 0.4},
           {"offset": 1, "color": "#8A6A3A", "opacity": 0.25}]}},
       stroke=INK, strokeWidth=3)
d.path(f"M{lx},{ly + 20} C{lx - 9},{ly + 8} {lx - 4},{ly - 4} {lx},{ly - 12} "
       f"C{lx + 4},{ly - 4} {lx + 9},{ly + 8} {lx},{ly + 20} Z",
       "Flame", fill=FLAME_GRAD, stroke=NONE)
d.shape("ellipse", "Flame core", x=lx - 3, y=ly + 4, width=7, height=12,
        fill="#FFF3CC", opacity=90, stroke=NONE)
d.shape("rectangle", "Lantern cap", x=lx - 14, y=ly - 34, width=28,
        height=12, radius=4, fill=BRASS, stroke=INK, strokeWidth=3)
d.path(f"M{lx - 10},{ly - 34} C{lx - 16},{ly - 52} {lx + 16},{ly - 52} "
       f"{lx + 10},{ly - 34}", "Lantern handle", fill=NONE, stroke=BRASS,
       strokeWidth=5, cap="round")
# light pool on the desktop
d.shape("ellipse", "Desk light pool", x=dx0 + 160, y=dy0 - 22, width=220,
        height=26, fill=AMBER, opacity=16, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("BRICKY GOLDBRICKSWORTH", "Name", x=500, y=930, size=46,
       font="Virelai Sans", color="#EFE0BC", justify="center")
r = d.text("COMPLIANCE MASCOT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C2A068", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("005.bricky-goldbricksworth-V1R00")
