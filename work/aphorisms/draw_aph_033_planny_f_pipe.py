#!/usr/bin/env python3
"""APH-033 Planny F. PipeMD — motivational-poster aphorism plate V1R00.
A TEAMWORK poster: three steel pipes carry amber data packets into a CPU
scheduler die, which routes the single output pipe straight into a brick
wall; packets queue at the mortar and a terminal strip reports the
delivery script deleted in 2002. Industrial copper-umber plate, steel
pipes, phosphor-green terminal. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-033 Planny F. PipeMD — Motivational Poster", 1000, 1000)

INK = "#120D0A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221A14"}, {"offset": 1, "color": "#0C0906"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#524334"}, {"offset": 0.7, "color": "#2C221A"},
    {"offset": 1, "color": "#120D0A"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#261E17"}, {"offset": 1, "color": "#141009"}]}}
PIPE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#828E9A"}, {"offset": 0.5, "color": "#5A646E"},
    {"offset": 1, "color": "#363E46"}]}}
CHIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E5A50"}, {"offset": 1, "color": "#21332C"}]}}
DIE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#52766A"}, {"offset": 1, "color": "#2A4238"}]}}
BRICK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#96443A"}, {"offset": 1, "color": "#5E2620"}]}}
TERM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#18231E"}, {"offset": 1, "color": "#0E1512"}]}}
GOLD = "#D8A050"
FRAME = "#B8A888"
HEAD = "#F2EADC"
PUNCH = "#E2D4C2"
CREAM = "#F2EADC"
FAINT = "#9A8A74"
AMBER = "#E8A850"
GREEN = "#8FD8A0"
RUST = "#D86050"
PIN = "#8A7C64"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6B5A44", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C49A", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#5E4C3A", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#5E4C3A", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A42", opacity=35, stroke=NONE)
# stray lost packets leaking onto the plate
for i, (x, y, deg) in enumerate([(300, 200, 12), (700, 185, -8),
                                 (830, 380, 20), (195, 560, -15)]):
    d.path(rot_rect_path(x, y, 9, 9, deg), f"Stray packet {i+1}",
           fill=AMBER, opacity=30, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#4A3A28", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# kicker + headline
r = d.text("TEAMWORK", "Kicker", x=500, y=PY + 44, size=12,
           font="Virelai Sans", color=GOLD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "kicker tracking", ids=[r["id"]], tracking=280)
r = d.text("EVERYTHING IS LOCAL", "Headline", x=500, y=PY + 80,
           size=33, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=55)
d.path("M350,254 L472,254 M528,254 L650,254", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 254, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- the intake pipes, left ------------------------------------------------------
PIPE_X0, PIPE_X1 = 250, 444
for i, py in enumerate([304, 356, 408]):
    # pipe run
    d.shape("rectangle", f"Pipe {i+1}", x=PIPE_X0, y=py, width=PIPE_X1 - PIPE_X0,
            height=14, radius=7, fill=PIPE_GRAD, stroke="#1A1E22",
            strokeWidth=2)
    # flange ring where the pipe meets the chip
    d.shape("rectangle", f"Flange {i+1}", x=PIPE_X1 - 10, y=py - 4,
            width=10, height=22, radius=3, fill=PIPE_GRAD,
            stroke="#1A1E22", strokeWidth=2)
    # inlet collar at the card edge
    d.shape("rectangle", f"Collar {i+1}", x=PIPE_X0 - 4, y=py - 3,
            width=8, height=20, radius=2, fill="#2E363E",
            stroke="#1A1E22", strokeWidth=2)
    # sheen along the top of the bore
    d.path(f"M{PIPE_X0 + 8},{py + 4} L{PIPE_X1 - 16},{py + 4}",
           f"Sheen {i+1}", fill=NONE, stroke="#AAB6C0", strokeWidth=2,
           cap="round", opacity=45)

# amber packets mid-flight inside the pipes (drawn over the bore)
for i, (px, py, deg) in enumerate([(300, 304, 0), (372, 304, 0),
                                    (330, 356, 0), (398, 356, 0),
                                    (286, 408, 0), (358, 408, 0)]):
    d.shape("rectangle", f"Packet {i+1}", x=px, y=py + 3, width=11,
            height=8, radius=2, fill=AMBER, opacity=90, stroke="#7A4A18",
            strokeWidth=1)
    d.path(f"M{px - 8},{py + 7} L{px - 3},{py + 7}", f"Packet tick {i+1}",
           fill=NONE, stroke=AMBER, strokeWidth=2, cap="round", opacity=55)

# --- the scheduler die --------------------------------------------------------------
CX, CY, CW, CH = 444, 292, 92, 158
d.shape("ellipse", "Chip shadow", x=CX - 6, y=CY + CH, width=CW + 12,
        height=10, fill="#000000", opacity=35, stroke=NONE)
# pins, top and bottom
for i in range(4):
    px = CX + 14 + i * 18
    d.shape("rectangle", f"Pin T{i+1}", x=px, y=CY - 10, width=7,
            height=10, radius=2, fill=PIN, stroke="#241E14",
            strokeWidth=1.5)
    d.shape("rectangle", f"Pin B{i+1}", x=px, y=CY + CH, width=7,
            height=10, radius=2, fill=PIN, stroke="#241E14",
            strokeWidth=1.5)
d.shape("rectangle", "Chip body", x=CX, y=CY, width=CW, height=CH,
        radius=8, fill=CHIP_GRAD, stroke="#101B16", strokeWidth=3)
d.shape("rectangle", "Chip die", x=CX + 14, y=CY + 20, width=CW - 28,
        height=CH - 40, radius=5, fill=DIE_GRAD, stroke="#16241E",
        strokeWidth=2)
d.text("SCHED", "Die label", x=CX + CW/2, y=CY + CH/2 - 6, size=13,
       font="Source Sans 3", color="#BFE8D2", justify="center")
d.text("planny·f", "Die etch", x=CX + CW/2, y=CY + CH/2 + 12, size=8,
       font="Source Sans 3", color="#7EA894", justify="center")
# routing traces on the die: in from the left, one out to the right
for i, py in enumerate([311, 363, 415]):
    ty = CY + 44 + i * 30
    d.path(f"M{CX + 16},{ty} L{CX + 34},{ty} L{CX + 44},{CY + CH/2}",
           f"Trace in {i+1}", fill=NONE, stroke=GREEN, strokeWidth=2,
           opacity=70)
d.path(f"M{CX + 44},{CY + CH/2} L{CX + 62},{CY + CH/2} L{CX + 74},{CY + CH/2}",
       "Trace out", fill=NONE, stroke=RUST, strokeWidth=2.5, opacity=80)
d.shape("ellipse", "Trace node", x=CX + 40, y=CY + CH/2 - 4, width=8,
        height=8, fill=GREEN, opacity=85, stroke=NONE)

# --- the output pipe, into the wall ----------------------------------------------------
OY = CY + CH/2 - 10                      # pipe centerline y=361
d.shape("rectangle", "Out pipe", x=CX + CW, y=OY, width=104, height=20,
        radius=0, fill=PIPE_GRAD, stroke="#1A1E22", strokeWidth=2)
d.path(f"M{CX + CW + 6},{OY + 5} L{CX + CW + 96},{OY + 5}", "Out sheen",
       fill=NONE, stroke="#AAB6C0", strokeWidth=2, cap="round", opacity=45)
# the packet that almost made it, jammed at the wall face
d.shape("rectangle", "Jammed packet", x=CX + CW + 92, y=OY + 5, width=10,
        height=10, radius=2, fill=RUST, opacity=90, stroke="#5E2018",
        strokeWidth=1)
# packets queued behind it, compressed
for i, qx in enumerate([CX + CW + 74, CX + CW + 58, CX + CW + 40]):
    d.shape("rectangle", f"Queued {i+1}", x=qx, y=OY + 6 - i, width=10,
            height=8, radius=2, fill=AMBER, opacity=85 - i * 12,
            stroke="#7A4A18", strokeWidth=1)

# --- the brick wall the pipe dead-ends into ----------------------------------------------
WL_X, WL_Y, WL_W, WL_H = 640, 292, 98, 158
d.shape("ellipse", "Wall shadow", x=WL_X - 10, y=WL_Y + WL_H - 4,
        width=WL_W + 20, height=12, fill="#000000", opacity=35,
        stroke=NONE)
BW, BH, GAP = 30, 16, 4
for row in range(8):
    off = (BW / 2 + GAP / 2) if row % 2 else 0
    for col in range(4):
        bx = WL_X + off + col * (BW + GAP)
        if bx + BW > WL_X + WL_W:
            continue
        by = WL_Y + row * (BH + GAP)
        d.shape("rectangle", f"Brick {row}.{col}", x=bx, y=by,
                width=BW, height=BH, radius=1.5, fill=BRICK_GRAD,
                stroke="#2A100C", strokeWidth=1.5)
# mortar seam where the pipe strikes
d.path(f"M{WL_X},{OY + 2} L{WL_X},{OY + 20}", "Struck mortar", fill=NONE,
       stroke=RUST, strokeWidth=3, opacity=60)
# spalled chips at the impact point
for i, (cx, cy, w, h, deg) in enumerate([(628, 336, 11, 5, -28),
                                          (624, 386, 9, 5, 18),
                                          (632, 412, 10, 5, -40)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Spall {i+1}",
           fill="#8A4038", opacity=70, stroke=NONE)

# --- the terminal strip: delivery failed silently -----------------------------------------
TX, TY, TW, TH = 268, 470, 464, 26
d.shape("rectangle", "Terminal", x=TX, y=TY, width=TW, height=TH,
        radius=6, fill=TERM_GRAD, stroke="#2E4038", strokeWidth=1.5)
d.shape("ellipse", "Term dot", x=TX + 10, y=TY + 9, width=8, height=8,
        fill=RUST, opacity=70, stroke=NONE)
d.text("> ./deliver.sh — EPIPE · target deleted 2002", "Term text",
       x=TX + 26, y=TY + 17, size=10, font="Source Sans 3",
       color=GREEN, justify="left")
d.shape("rectangle", "Term caret", x=TX + TW - 18, y=TY + 7, width=7,
        height=12, fill=GREEN, opacity=80, stroke=NONE)

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("THE KERNEL HEARD YOU.", "Punchline 1", x=500,
           y=PY + PH - 58, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch1 tracking", ids=[r["id"]], tracking=90)
r = d.text("IT SIMPLY CHOSE TO IGNORE THE REQUEST.", "Punchline 2", x=500,
           y=PY + PH - 32, size=19, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch2 tracking", ids=[r["id"]], tracking=25)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("PLANNY F. PIPEMD", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE KERNEL HEARD YOU", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-033-planny-f-pipe-V1R00")
