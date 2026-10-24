#!/usr/bin/env python3
"""Haikool Breeze — mascot portrait V1R00. Minimalist Haunter:
a whispery translucent wisp resting beneath the Deskbar of a clean
empty desktop, one replicant window still blinking in the corner.
Haiku/BeOS lineage: leaf menu button, tray clock, thread-quiet calm.
Cool slate plate on a deep blue-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Haikool Breeze — Mascot Plate", 1000, 1000)

INK = "#2B2620"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#131B24"}, {"offset": 1, "color": "#070B10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A9BBC7"}, {"offset": 0.62, "color": "#7D92A1"},
    {"offset": 1, "color": "#4B5E6B"}]}}
DESKBAR_GRAD = {"gradient": {"kind": "linear", "start": [0, 112], "end": [0, 172], "stops": [
    {"offset": 0, "color": "#CBD4DC"}, {"offset": 0.5, "color": "#9AA8B4"},
    {"offset": 1, "color": "#7C8B98"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "start": [0, 122], "end": [0, 162], "stops": [
    {"offset": 0, "color": "#A9C97E"}, {"offset": 1, "color": "#5E8C58"}]}}
GHOST_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4FAFD"}, {"offset": 0.55, "color": "#D3E3EC"},
    {"offset": 1, "color": "#9FB9C9"}]}}
REPL_GRAD = {"gradient": {"kind": "linear", "start": [0, 618], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#DCE6EE"}, {"offset": 1, "color": "#A9BCCA"}]}}
AMBER_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6C35C"}, {"offset": 1, "color": "#D8871E"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#9FB4C2", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E1A14", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6E2EA", strokeWidth=3, opacity=34)
# desktop patina + flecks
d.shape("ellipse", "Patina 1", x=540, y=560, width=270, height=160,
        fill="#C2D0DA", opacity=13, stroke=NONE)
d.shape("ellipse", "Patina 2", x=180, y=200, width=240, height=150,
        fill="#5E7280", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(210,340,5),(800,330,6),(175,540,6),(845,545,5),
                               (255,760,5),(735,765,6),(150,450,5),(860,620,5),
                               (425,120,5),(605,130,6),(330,155,4),(700,215,5),
                               (240,640,4),(655,700,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4ECF2", opacity=36, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M935,150 A105,105 0 0 0 845,60", "Ghost arc TR",
       fill=NONE, stroke="#4C6070", strokeWidth=14, opacity=10, cap="round")
d.path("M75,770 A120,120 0 0 0 185,875", "Ghost arc BL",
       fill=NONE, stroke="#4C6070", strokeWidth=10, opacity=8, cap="round")

# --- the empty desktop: one faint closed window, far left -------------------------
d.shape("rectangle", "Dormant window", x=150, y=235, width=150, height=104,
        radius=6, fill=NONE, stroke="#D8E4EC", strokeWidth=3, opacity=13)
d.path("M150,258 L300,258", "Dormant window title rule",
       fill=NONE, stroke="#D8E4EC", strokeWidth=3, opacity=13)

# --- deskbar, top-right of the desktop --------------------------------------------
d.shape("rectangle", "Deskbar shadow", x=316, y=122, width=428, height=56,
        radius=9, fill="#22303C", opacity=35, stroke=NONE)
d.shape("rectangle", "Deskbar", x=310, y=114, width=428, height=56,
        radius=9, fill=DESKBAR_GRAD, stroke="#39434D", strokeWidth=3)
# leaf menu button (Haiku feather-leaf)
d.shape("rectangle", "Leaf button", x=320, y=122, width=50, height=40,
        radius=6, fill="#B4BFC9", stroke="#4A545E", strokeWidth=2)
d.path("M336,152 C334,138 344,128 358,126 C358,142 350,152 336,152 Z",
       "Leaf blade", fill=LEAF_GRAD, stroke="#40603C", strokeWidth=2)
d.path("M338,150 C344,142 350,134 356,128", "Leaf vein",
       fill=NONE, stroke="#40603C", strokeWidth=1.5, cap="round")
# window entries: two tabs, the second is hers — still lit
d.shape("rectangle", "Entry closed", x=380, y=126, width=128, height=30,
        radius=4, fill="#8795A1", stroke="#4A545E", strokeWidth=2, opacity=70)
d.path("M390,142 L448,142", "Entry closed title",
       fill=NONE, stroke="#5A646E", strokeWidth=3, cap="round", opacity=70)
d.shape("rectangle", "Entry lit", x=516, y=126, width=128, height=30,
        radius=4, fill="#E2EAF0", stroke="#4A545E", strokeWidth=2)
d.path("M526,142 L574,142", "Entry lit title",
       fill=NONE, stroke="#6A7682", strokeWidth=3, cap="round")
d.shape("ellipse", "Entry lit dot", x=628, y=136, width=8, height=8,
        fill=AMBER_GRAD, stroke=NONE)
# tray separator + replicant stub + analog clock (no digits)
d.path("M660,124 L660,160", "Tray separator",
       fill=NONE, stroke="#4A545E", strokeWidth=2, opacity=60)
d.shape("ellipse", "Tray stub", x=672, y=135, width=10, height=10,
        fill="#B0BCC6", stroke="#4A545E", strokeWidth=1.5)
d.shape("ellipse", "Tray clock face", x=692, y=128, width=32, height=32,
        fill="#E8EEF2", stroke="#4A545E", strokeWidth=2)
d.path("M708,144 L708,134 M708,144 L716,148", "Clock hands",
       fill=NONE, stroke="#39434D", strokeWidth=2.5, cap="round")

# --- the replicant, still blinking, lower left -------------------------------------
rx, ry = 208, 616
d.shape("ellipse", "Replicant glow", x=rx - 16, y=ry - 14, width=118, height=104,
        fill="#F0C87A", opacity=12, stroke=NONE)
d.shape("rectangle", "Replicant", x=rx, y=ry, width=86, height=76,
        radius=8, fill=REPL_GRAD, stroke="#4A545E", strokeWidth=3, opacity=88)
d.shape("rectangle", "Replicant title", x=rx + 5, y=ry + 5, width=76, height=16,
        radius=4, fill="#8795A1", stroke=NONE, opacity=80)
d.shape("ellipse", "Blink glow", x=rx + 26, y=ry + 32, width=36, height=36,
        fill="#F6C35C", opacity=22, stroke=NONE)
d.shape("ellipse", "Blink dot", x=rx + 36, y=ry + 42, width=16, height=16,
        fill=AMBER_GRAD, stroke="#8A5A14", strokeWidth=2)
d.path(f"M{rx+12},{ry+64} L{rx+30},{ry+64}", "Replicant base tick",
       fill=NONE, stroke="#5A646E", strokeWidth=3, cap="round", opacity=70)

# --- Haikool: the wisp beneath the deskbar ------------------------------------------
# soft presence glow first, then the body
d.shape("ellipse", "Wisp aura", x=392, y=396, width=240, height=300,
        fill="#EAF3F8", opacity=12, stroke=NONE)
d.shape("ellipse", "Wisp aura core", x=436, y=430, width=150, height=210,
        fill="#EAF3F8", opacity=10, stroke=NONE)
GHOST = ("M500,412 C566,412 612,470 614,548 "
         "C615,610 600,648 586,668 "
         "L566,646 L548,676 L528,644 L508,678 L488,644 L468,672 L448,640 L430,662 "
         "C406,636 392,596 394,540 C397,462 440,412 500,412 Z")
d.path(GHOST, "Wisp body", fill=GHOST_GRAD, stroke="#DCE9F0",
       strokeWidth=3, opacity=78)
# inner volume: head dome highlight + hem shade
d.shape("ellipse", "Wisp dome light", x=448, y=428, width=118, height=84,
        fill="#FFFFFF", opacity=30, stroke=NONE)
d.path("M430,636 C470,652 540,652 584,632 L586,668 L566,646 L548,676 L528,644 "
       "L508,678 L488,644 L468,672 L448,640 L430,662 Z",
       "Wisp hem shade", fill="#8FA9BB", opacity=38, stroke=NONE)
# thread wisps drifting off her hem — she is thread-per-window
for i, (x, y, w, h, o) in enumerate([(416,712,10,26,30),(512,714,9,30,26),
                                     (604,688,8,22,24)]):
    assert on_disc(x + w / 2, y + h / 2, 8), (x, y)
    d.shape("ellipse", f"Thread wisp {i+1}", x=x, y=y, width=w, height=h,
            fill="#D3E3EC", opacity=o, stroke=NONE)
# serene closed eyes — she only crashes when noticed
d.path("M462,514 Q476,524 490,514", "Eye L (closed)",
       fill=NONE, stroke="#33505C", strokeWidth=4.5, cap="round")
d.path("M524,514 Q538,524 552,514", "Eye R (closed)",
       fill=NONE, stroke="#33505C", strokeWidth=4.5, cap="round")
# the whisper: a small soft mouth, mid-haiku
d.path("M497,556 Q507,562 517,556", "Mouth",
       fill=NONE, stroke="#33505C", strokeWidth=4, cap="round", opacity=80)
# faint cool cheeks
d.shape("ellipse", "Cheek L", x=444, y=536, width=24, height=12,
        fill="#8FB4C8", opacity=26, stroke=NONE)
d.shape("ellipse", "Cheek R", x=540, y=536, width=24, height=12,
        fill="#8FB4C8", opacity=26, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("HAIKOOL BREEZE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DCE8EE", justify="center")
r = d.text("MINIMALIST HAUNTER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FB2BE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=220)

d.finish("029.haikool-breeze-V1R00")
