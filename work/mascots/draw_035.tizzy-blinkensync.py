#!/usr/bin/env python3
"""Tizzy Blinkensync — mascot portrait V1R00. UI Ghost:
a translucent little specter flickering on the home screen of a phone
that never shipped — rows of preinstalled app icons behind her, a
loading bar stalled mid-sync. She is drawn twice, main pass plus an
offset echo, with scanline slices cutting through. Cold indigo plate
on a deep-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Tizzy Blinkensync — Mascot Plate", 1000, 1000)

INK = "#221C30"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#101226"}, {"offset": 1, "color": "#05060E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A68A0"}, {"offset": 0.6, "color": "#2A3E6C"},
    {"offset": 1, "color": "#121B38"}]}}
PHONE_GRAD = {"gradient": {"kind": "linear", "start": [0, 130], "end": [0, 810], "stops": [
    {"offset": 0, "color": "#3A3E52"}, {"offset": 1, "color": "#1C1E2E"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#BEE2F0"}, {"offset": 0.65, "color": "#7EB4D8"},
    {"offset": 1, "color": "#4A7CAE"}]}}
GHOST_FILL = "#E8F6FA"
GHOST_EDGE = "#9FD4E4"
GLITCH_R = "#E06A8A"
GLITCH_B = "#5AD0E8"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#4A68A0", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#141024", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D4E8", strokeWidth=3, opacity=28)
d.shape("ellipse", "Screen bloom", x=340, y=330, width=340, height=300,
        fill="#8FC8E8", opacity=14, stroke=NONE)
d.shape("ellipse", "Patina 1", x=600, y=160, width=220, height=130,
        fill="#2A3E6C", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=150, y=640, width=240, height=130,
        fill="#0E1430", opacity=26, stroke=NONE)
for i, (x, y, w) in enumerate([(218,346,5),(792,338,6),(174,540,5),(844,548,5),
                               (264,756,5),(724,760,6),(154,452,5),(852,648,5),
                               (432,126,5),(602,128,6),(338,152,4),(698,200,5),
                               (246,664,4),(670,716,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8DCF0", opacity=28, stroke=NONE)
# ghost sync-arcs on the dark backdrop
d.path("M936,168 A105,105 0 0 0 838,62", "Ghost arc TR",
       fill=NONE, stroke="#4A68A0", strokeWidth=14, opacity=10, cap="round")
d.path("M74,772 A120,120 0 0 0 186,876", "Ghost arc BL",
       fill=NONE, stroke="#4A68A0", strokeWidth=10, opacity=8, cap="round")

# --- the phone that never shipped ------------------------------------------------------
d.shape("ellipse", "Phone shadow", x=320, y=790, width=370, height=40,
        fill="#060810", opacity=45, stroke=NONE)
d.shape("rectangle", "Phone body", x=326, y=128, width=348, height=680,
        radius=44, fill=PHONE_GRAD, stroke=INK, strokeWidth=6)
d.shape("rectangle", "Phone edge light", x=334, y=140, width=20, height=640,
        radius=10, fill="#8A90B0", opacity=25, stroke=NONE)
# earpiece + a front sensor dot that never saw a face
d.shape("rectangle", "Earpiece", x=462, y=146, width=76, height=10, radius=5,
        fill="#14161F", stroke=NONE)
d.shape("ellipse", "Sensor", x=552, y=143, width=16, height=16,
        fill="#14161F", stroke="#3A3E52", strokeWidth=2)
# the screen — still glowing for nobody
d.shape("rectangle", "Screen", x=352, y=168, width=296, height=560,
        radius=12, fill=SCREEN_GRAD, stroke="#101420", strokeWidth=4)
# status bar: signal arcs, time (digits -> Source Sans 3), battery
for j, hh in enumerate((6, 10, 14)):
    d.shape("rectangle", f"Signal {j+1}", x=366 + j * 9, y=190 - hh,
            width=6, height=hh, radius=2, fill="#1E3450", opacity=80,
            stroke=NONE)
d.shape("ellipse", "Wifi dot", x=404, y=182, width=8, height=8,
        fill="#1E3450", opacity=80, stroke=NONE)
d.text("4:04", "Clock", x=560, y=192, size=14, font="Source Sans 3",
       color="#1E3450", justify="left")
d.shape("rectangle", "Battery", x=618, y=182, width=24, height=12, radius=3,
        fill=NONE, stroke="#1E3450", strokeWidth=2)
d.shape("rectangle", "Battery fill", x=621, y=185, width=10, height=6,
        radius=2, fill="#1E3450", opacity=80, stroke=NONE)

# --- rows of preinstalled app icons ------------------------------------------------------
ICONS = [
    ("#4E8EC8", "gear"), ("#58A87C", "chat"), ("#C88A4E", "mail"),
    ("#A05A8E", "globe"),
    ("#5A78C8", "photo"), ("#B85A6E", "music"), ("#4EA8B8", "map"),
    ("#8E8EC8", "clock"),
    ("#6A9E5E", "store"), ("#C86A5A", "news"), ("#7E6AB8", "cloud"),
    ("#B8A04E", "notes"),
]
GX0, GY0, GAP, IS = 382, 226, 66, 52
for i, (col, glyph) in enumerate(ICONS):
    cx = GX0 + (i % 4) * GAP
    cy = GY0 + (i // 4) * GAP + (i // 4) * 14
    never = i in (2, 6, 10)   # never-installed apps sit dimmer
    d.shape("rectangle", f"Icon {i+1}", x=cx, y=cy, width=IS, height=IS,
            radius=14, fill=col, opacity=95 if not never else 45,
            stroke=INK, strokeWidth=2.5)
    ix, iy = cx + IS / 2, cy + IS / 2
    if glyph == "gear":
        d.shape("ellipse", f"Icon {i+1} g", x=int(ix - 10), y=int(iy - 10),
                width=20, height=20, fill=NONE, stroke="#F0E8D8",
                strokeWidth=4)
    elif glyph == "chat":
        d.path(f"M{ix - 12},{iy - 8} L{ix + 12},{iy - 8} L{ix + 12},{iy + 4} "
               f"L{ix - 2},{iy + 4} L{ix - 8},{iy + 10} L{ix - 8},{iy + 4} "
               f"L{ix - 12},{iy + 4} Z", f"Icon {i+1} g",
               fill="#F0E8D8", opacity=90, stroke=NONE)
    elif glyph == "mail":
        d.path(f"M{ix - 13},{iy - 8} L{ix + 13},{iy - 8} L{ix + 13},{iy + 8} "
               f"L{ix - 13},{iy + 8} Z M{ix - 13},{iy - 8} L{ix},{iy + 2} "
               f"L{ix + 13},{iy - 8}", f"Icon {i+1} g",
               fill=NONE, stroke="#F0E8D8", strokeWidth=3)
    elif glyph == "globe":
        d.shape("ellipse", f"Icon {i+1} g", x=int(ix - 11), y=int(iy - 11),
                width=22, height=22, fill=NONE, stroke="#F0E8D8",
                strokeWidth=3)
        d.path(f"M{ix - 11},{iy} L{ix + 11},{iy} M{ix},{iy - 11} "
               f"C{ix - 6},{iy - 4} {ix - 6},{iy + 4} {ix},{iy + 11} "
               f"M{ix},{iy - 11} C{ix + 6},{iy - 4} {ix + 6},{iy + 4} "
               f"{ix},{iy + 11}", f"Icon {i+1} g2",
               fill=NONE, stroke="#F0E8D8", strokeWidth=2)
    elif glyph == "photo":
        d.path(f"M{ix - 12},{iy + 8} L{ix - 3},{iy - 6} L{ix + 4},{iy + 2} "
               f"L{ix + 12},{iy - 6} L{ix + 12},{iy + 8} Z",
               f"Icon {i+1} g", fill="#F0E8D8", opacity=90, stroke=NONE)
    elif glyph == "music":
        d.path(f"M{ix - 4},{iy + 8} L{ix - 4},{iy - 8} L{ix + 10},{iy - 10} "
               f"L{ix + 10},{iy + 4}", f"Icon {i+1} g",
               fill=NONE, stroke="#F0E8D8", strokeWidth=3.5)
        d.shape("ellipse", f"Icon {i+1} g2", x=int(ix - 10), y=int(iy + 4),
                width=9, height=7, fill="#F0E8D8", stroke=NONE)
    elif glyph == "map":
        d.path(f"M{ix - 12},{iy - 8} L{ix - 4},{iy - 12} L{ix + 4},{iy - 8} "
               f"L{ix + 12},{iy - 12} L{ix + 12},{iy + 8} L{ix + 4},{iy + 12} "
               f"L{ix - 4},{iy + 8} L{ix - 12},{iy + 12} Z",
               f"Icon {i+1} g", fill="#F0E8D8", opacity=85, stroke=NONE)
    elif glyph == "clock":
        d.shape("ellipse", f"Icon {i+1} g", x=int(ix - 11), y=int(iy - 11),
                width=22, height=22, fill=NONE, stroke="#F0E8D8",
                strokeWidth=3)
        d.path(f"M{ix},{iy} L{ix},{iy - 7} M{ix},{iy} L{ix + 5},{iy + 3}",
               f"Icon {i+1} g2", fill=NONE, stroke="#F0E8D8",
               strokeWidth=3, cap="round")
    elif glyph == "store":
        d.path(f"M{ix - 12},{iy - 4} L{ix - 12},{iy - 10} L{ix + 12},{iy - 10} "
               f"L{ix + 12},{iy - 4} M{ix - 12},{iy - 4} C{ix - 12},{iy + 2} "
               f"{ix - 4},{iy + 2} {ix - 4},{iy - 4} C{ix - 4},{iy + 2} "
               f"{ix + 4},{iy + 2} {ix + 4},{iy - 4} C{ix + 4},{iy + 2} "
               f"{ix + 12},{iy + 2} {ix + 12},{iy - 4} M{ix - 8},{iy + 4} "
               f"L{ix - 8},{iy + 12} L{ix + 8},{iy + 12} L{ix + 8},{iy + 4}",
               f"Icon {i+1} g", fill=NONE, stroke="#F0E8D8", strokeWidth=2.5)
    elif glyph == "news":
        for k, lw2 in enumerate((22, 22, 14)):
            d.shape("rectangle", f"Icon {i+1} g{k}", x=int(ix - 11),
                    y=int(iy - 8 + k * 7), width=lw2, height=4, radius=2,
                    fill="#F0E8D8", opacity=90, stroke=NONE)
    elif glyph == "cloud":
        d.path(f"M{ix - 10},{iy + 6} C{ix - 16},{iy + 6} {ix - 16},{iy - 2} "
               f"{ix - 10},{iy - 2} C{ix - 9},{iy - 9} {ix + 1},{iy - 10} "
               f"{ix + 5},{iy - 5} C{ix + 12},{iy - 5} {ix + 13},{iy + 6} "
               f"{ix + 6},{iy + 6} Z", f"Icon {i+1} g",
               fill="#F0E8D8", opacity=90, stroke=NONE)
    elif glyph == "notes":
        d.shape("rectangle", f"Icon {i+1} g", x=int(ix - 10), y=int(iy - 12),
                width=20, height=24, radius=3, fill=NONE,
                stroke="#F0E8D8", strokeWidth=3)
        d.path(f"M{ix - 5},{iy - 5} L{ix + 5},{iy - 5} M{ix - 5},{iy} "
               f"L{ix + 5},{iy} M{ix - 5},{iy + 5} L{ix + 2},{iy + 5}",
               f"Icon {i+1} g2", fill=NONE, stroke="#F0E8D8",
               strokeWidth=2.5, cap="round")

# one glitching icon — chromatic echoes shivering off it
for j, (col, ox) in enumerate(((GLITCH_R, -6), (GLITCH_B, 6))):
    d.shape("rectangle", f"Glitch echo {j+1}", x=GX0 + 1 * GAP + ox,
            y=GY0 + 2 * GAP + 28, width=IS, height=IS, radius=14,
            fill=NONE, stroke=col, strokeWidth=2.5, opacity=70)

# --- the stalled sync bar ------------------------------------------------------------------
d.shape("rectangle", "Sync well", x=392, y=636, width=216, height=26,
        radius=13, fill="#1E3450", opacity=85, stroke=NONE)
d.shape("rectangle", "Sync fill", x=396, y=640, width=148, height=18,
        radius=9, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#7EC8E8"}, {"offset": 1, "color": "#3E8EC0"}]}},
        stroke=NONE)
# the fill's ragged stalled edge
d.shape("rectangle", "Sync stall", x=540, y=640, width=10, height=18,
        fill="#1E3450", opacity=70, stroke=NONE)
d.text("SYNCING 68%", "Sync label", x=420, y=684, size=15,
       font="Source Sans 3", color="#D8E8F0", justify="left")
for j, dx in enumerate((0, 12, 24)):
    d.shape("ellipse", f"Ellipsis {j+1}", x=506 + dx, y=672, width=6,
            height=6, fill="#D8E8F0", opacity=90 - j * 30, stroke=NONE)

# --- Tizzy, flickering ----------------------------------------------------------------------
def ghost(dx, dy, op, edge_op, label):
    """The little specter, pass or echo. Dome head, wavy hem, hopeful eyes."""
    d.path(f"M{500 + dx},{330 + dy} C{552 + dx},{330 + dy} {578 + dx},{368 + dy} "
           f"{578 + dx},{420 + dy} L{578 + dx},{508 + dy} "
           f"C{566 + dx},{496 + dy} {556 + dx},{496 + dy} {546 + dx},{508 + dy} "
           f"C{536 + dx},{496 + dy} {526 + dx},{496 + dy} {516 + dx},{508 + dy} "
           f"C{506 + dx},{496 + dy} {496 + dx},{496 + dy} {486 + dx},{508 + dy} "
           f"C{476 + dx},{496 + dy} {466 + dx},{496 + dy} {456 + dx},{508 + dy} "
           f"C{446 + dx},{496 + dy} {436 + dx},{496 + dy} {422 + dx},{508 + dy} "
           f"L{422 + dx},{420 + dy} C{422 + dx},{368 + dy} {448 + dx},{330 + dy} "
           f"{500 + dx},{330 + dy} Z",
           f"{label} body", fill=GHOST_FILL, opacity=op,
           stroke=GHOST_EDGE, strokeWidth=4)
    # stubby hopeful arms
    d.path(f"M{424 + dx},{440 + dy} C{404 + dx},{446 + dy} {396 + dx},{462 + dy} "
           f"{398 + dx},{476 + dy} C{410 + dx},{478 + dy} {422 + dx},{466 + dy} "
           f"{428 + dx},{452 + dy} Z", f"{label} arm L",
           fill=GHOST_FILL, opacity=op, stroke=GHOST_EDGE, strokeWidth=3)
    d.path(f"M{576 + dx},{440 + dy} C{596 + dx},{446 + dy} {604 + dx},{462 + dy} "
           f"{602 + dx},{476 + dy} C{590 + dx},{478 + dy} {578 + dx},{466 + dy} "
           f"{572 + dx},{452 + dy} Z", f"{label} arm R",
           fill=GHOST_FILL, opacity=op, stroke=GHOST_EDGE, strokeWidth=3)
    # eyes — wide, hopeful, a little lost
    d.shape("ellipse", f"{label} eye L", x=462 + dx, y=398 + dy,
            width=26, height=34, fill="#1E2A40", opacity=min(op + 15, 100),
            stroke=NONE)
    d.shape("ellipse", f"{label} eye R", x=512 + dx, y=398 + dy,
            width=26, height=34, fill="#1E2A40", opacity=min(op + 15, 100),
            stroke=NONE)
    d.shape("ellipse", f"{label} glint L", x=468 + dx, y=404 + dy,
            width=9, height=9, fill="#FFFFFF", opacity=90, stroke=NONE)
    d.shape("ellipse", f"{label} glint R", x=518 + dx, y=404 + dy,
            width=9, height=9, fill="#FFFFFF", opacity=90, stroke=NONE)
    # small hopeful smile
    d.path(f"M{482 + dx},{452 + dy} C{492 + dx},{462 + dy} {508 + dx},{462 + dy} "
           f"{518 + dx},{452 + dy}", f"{label} smile",
           fill=NONE, stroke="#1E2A40", strokeWidth=4.5, opacity=edge_op,
           cap="round")
    # blush flickers in and out
    d.shape("ellipse", f"{label} blush L", x=448 + dx, y=440 + dy,
            width=20, height=12, fill="#E08AA0", opacity=int(op * 0.5),
            stroke=NONE)
    d.shape("ellipse", f"{label} blush R", x=532 + dx, y=440 + dy,
            width=20, height=12, fill="#E08AA0", opacity=int(op * 0.5),
            stroke=NONE)

# the echo — half a frame behind, shifted right and down
ghost(14, 10, 26, 40, "Echo")
# chromatic shiver on the echo's edge
d.path("M592,400 C596,436 596,470 592,506", "Echo fringe R",
       fill=NONE, stroke=GLITCH_R, strokeWidth=3, opacity=45, cap="round")
d.path("M408,410 C404,444 404,474 408,504", "Echo fringe L",
       fill=NONE, stroke=GLITCH_B, strokeWidth=3, opacity=45, cap="round")
# the main pass — she is *almost* here
ghost(0, 0, 68, 80, "Tizzy")
# scanline slices where the render skips her — screen color cutting through
for j, (sy, sh) in enumerate([(388, 7), (430, 5), (472, 8), (512, 5)]):
    d.shape("rectangle", f"Flicker slice {j+1}", x=408, y=sy, width=186,
            height=sh, fill="#8FC0DC", opacity=55, stroke=NONE)
# her glow on the screen
d.shape("ellipse", "Ghost glow", x=390, y=330, width=220, height=210,
        fill="#CFEAF6", opacity=16, stroke=NONE)

# home indicator that never gets swiped
d.shape("rectangle", "Home bar", x=452, y=708, width=96, height=7,
        radius=4, fill="#1E3450", opacity=70, stroke=NONE)
# soft reflection sweeping the glass
d.path("M380,170 L470,170 L400,726 L356,726 Z", "Glass reflection",
       fill="#FFFFFF", opacity=8, stroke=NONE)

# stray glitch motes on the plate around the phone
for i, (x, y, w, col) in enumerate([(292,300,10,GLITCH_B),(700,360,8,GLITCH_R),
                                    (286,560,8,GLITCH_R),(706,540,10,GLITCH_B),
                                    (310,220,7,GLITCH_R),(694,660,8,GLITCH_B)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("rectangle", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill=col, opacity=40, stroke=NONE)

# --- name + role ----------------------------------------------------------------------------
d.text("TIZZY BLINKENSYNC", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#DCEAF6", justify="center")
r = d.text("UI GHOST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FC0DC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("035.tizzy-blinkensync-V1R00")
