#!/usr/bin/env python3
"""Genny Compileheart — mascot portrait V1R00.
Build-time oracle watching emerge output scroll on the terminal, a
hand-marked make.conf sheet in her paws, case fans spinning through
the long gentoo-purple night. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Genny Compileheart — Mascot Portrait", 1000, 1000)

INK = "#221C24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E0B16"}, {"offset": 1, "color": "#060509"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5D5082"}, {"offset": 0.7, "color": "#433A62"},
    {"offset": 1, "color": "#26203C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C2740"}, {"offset": 1, "color": "#161222"}]}}
TERM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161B20"}, {"offset": 1, "color": "#0B0E12"}]}}
TOWER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4452"}, {"offset": 1, "color": "#22262E"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EBD6CC"}, {"offset": 0.7, "color": "#C49E94"},
    {"offset": 1, "color": "#947068"}]}}
HOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7C66A0"}, {"offset": 1, "color": "#4E3F6E"}]}}
GREEN = "#7FD08A"
GREEN_DIM = "#558E60"
AMBER = "#E8B86A"
PAPER = "#E4DCC6"
VIOLET = "#B090E8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8579AE", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CEC6E2", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(190,240,8),(802,234,7),(152,522,9),(842,540,8),
                               (254,768,7),(748,754,9),(130,392,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,822,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#49406E", opacity=50, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#100D18",
       strokeWidth=4, opacity=70)

# --- the terminal: emerge output mid-scroll -------------------------------------
d.shape("ellipse", "Term shadow", x=380, y=688, width=400, height=24,
        fill="#08080E", opacity=55, stroke=NONE)
d.path("M430,540 L456,540 L462,700 L424,700 Z", "Term leg L",
       fill="#2A2438", stroke=INK, strokeWidth=5, join="round")
d.path("M726,540 L752,540 L758,700 L720,700 Z", "Term leg R",
       fill="#2A2438", stroke=INK, strokeWidth=5, join="round")
d.shape("rectangle", "Terminal", x=360, y=226, width=440, height=310,
        fill=TERM_GRAD, stroke=INK, strokeWidth=7, radius=12)
# titlebar
d.shape("rectangle", "Term bar", x=372, y=238, width=416, height=30,
        fill="#232A32", stroke=NONE, radius=6)
d.text("GENNY@OCTARINE — EMERGE", "Term title", x=384, y=258, size=12,
       font="Virelai Sans", color="#8E9AA6", justify="left")
for i, bx in enumerate([748, 764, 780]):
    d.shape("ellipse", f"Term dot {i+1}", x=bx, y=246, width=10, height=10,
            fill="#4E5A66", stroke=NONE)
# the scroll: green okays, white ebuilds, amber estimate.
# Virelai Sans has no digits — every line carries numbers, so Source Sans 3.
lines = [("% emerge -avuDN @world", "#C8D2DC"),
         (">>> Emerging (1 of 47) sys-devel/gcc", GREEN),
         (">>> Jobs: 2 of 47", GREEN_DIM),
         ("[ebuild   R   ] app-editors/emacs", "#A9B8C4"),
         ("[ebuild     U ] x11-libs/gtk+", "#A9B8C4"),
         ("[ebuild     U ] dev-libs/elfutils", "#A9B8C4"),
         (">>> Compiling (6 of 47) dev-lang/rust", GREEN),
         ("[#############      ]", AMBER),
         ("ETA: about six hours. worth it.", AMBER)]
for i, (txt, col) in enumerate(lines):
    d.text(txt, f"Log {i+1}", x=384, y=296+i*26, size=13,
           font="Source Sans 3", color=col, justify="left")
# the cursor still believes
d.shape("rectangle", "Log cursor", x=384, y=506, width=9, height=15,
        fill=GREEN, opacity=80, stroke=NONE)
# green spill of the scroll onto the bezel
d.shape("ellipse", "Term glow", x=430, y=290, width=300, height=200,
        fill=GREEN, opacity=6, stroke=NONE)

# --- the tower: two case fans spinning -------------------------------------------
d.shape("ellipse", "Tower shadow", x=190, y=688, width=160, height=20,
        fill="#08080E", opacity=50, stroke=NONE)
d.path("M196,430 L336,430 L346,702 L186,702 Z", "Tower case",
       fill=TOWER_GRAD, stroke=INK, strokeWidth=6, join="round")
# front LED strip
d.shape("rectangle", "LED strip", x=206, y=448, width=8, height=230,
        fill=VIOLET, stroke=NONE, radius=4, opacity=80)
d.shape("rectangle", "LED glow", x=200, y=442, width=20, height=242,
        fill=VIOLET, stroke=NONE, radius=8, opacity=15)
for fi, cy in enumerate([488, 606]):
    # fan well + blades mid-spin + dashed spin arcs
    d.shape("ellipse", f"Fan well {fi+1}", x=228, y=cy-52, width=104,
            height=104, fill="#161A20", stroke=INK, strokeWidth=4)
    d.path(f"M280,{cy} C280,{cy-16} 298,{cy-18} 300,{cy-8} C302,{cy+2} "
           f"288,{cy+4} 280,{cy} M280,{cy} C264,{cy} 262,{cy-18} "
           f"272,{cy-20} C282,{cy-22} 284,{cy-8} 280,{cy} "
           f"M280,{cy} C280,{cy+16} 262,{cy+18} 260,{cy+8} "
           f"C258,{cy-2} 272,{cy-4} 280,{cy} M280,{cy} C296,{cy} "
           f"298,{cy+18} 288,{cy+20} C278,{cy+22} 276,{cy+8} 280,{cy} Z",
           f"Fan blades {fi+1}", fill="#56606E", stroke=INK,
           strokeWidth=3, join="round")
    d.shape("ellipse", f"Fan hub {fi+1}", x=274, y=cy-6, width=12,
            height=12, fill="#3A414C", stroke=INK, strokeWidth=2)
    d.path(f"M244,{cy-40} C256,{cy-56} 304,{cy-56} 316,{cy-40}",
           f"Spin arc {fi+1}a", fill=NONE, stroke=VIOLET, strokeWidth=3,
           cap="round", dash=[4, 10], opacity=60)
    d.path(f"M244,{cy+40} C256,{cy+56} 304,{cy+56} 316,{cy+40}",
           f"Spin arc {fi+1}b", fill=NONE, stroke=VIOLET, strokeWidth=3,
           cap="round", dash=[4, 10], opacity=60)
# power button, softly lit — the machine has been at this a while
d.shape("ellipse", "Power button", x=300, y=660, width=18, height=18,
        fill="#2C3138", stroke=INK, strokeWidth=3)
d.path("M309,664 L309,670 M305,666 C305,672 313,672 313,666",
       "Power glyph", fill=NONE, stroke=VIOLET, strokeWidth=2.5,
       cap="round", opacity=90)

# --- the mug: eight hours means tea -------------------------------------------------
d.shape("ellipse", "Mug shadow", x=478, y=688, width=72, height=14,
        fill="#08080E", opacity=50, stroke=NONE)
d.path("M496,646 C486,640 486,628 496,624", "Mug handle", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M498,636 L544,636 L540,700 L502,700 Z", "Mug", fill=HOOD_GRAD,
       stroke=INK, strokeWidth=5, join="round")
d.path("M504,650 L540,650", "Tea line", fill=NONE, stroke="#3E3054",
       strokeWidth=4, opacity=80)
# steam: the patience of warm liquid
d.path("M514,622 C508,610 518,602 512,592", "Steam 1", fill=NONE,
       stroke="#CFC4DC", strokeWidth=3, cap="round", opacity=55)
d.path("M532,622 C526,608 538,600 532,588", "Steam 2", fill=NONE,
       stroke="#CFC4DC", strokeWidth=3, cap="round", opacity=45)

# --- Genny Compileheart: oracle at the altar of slow binaries ----------------------
d.shape("ellipse", "Genny shadow", x=580, y=686, width=200, height=22,
        fill="#08080E", opacity=50, stroke=NONE)
# hood bunched behind her shoulders
d.path("M596,486 C600,444 636,414 682,414 C728,414 764,444 768,486 "
       "C748,462 724,450 682,450 C640,450 616,462 596,486 Z",
       "Hood", fill=HOOD_GRAD, stroke=INK, strokeWidth=6, join="round")
# body: cozy pear, leaning a degree toward the light
d.path("M682,470 C744,470 780,528 780,600 C780,662 736,694 682,694 "
       "C628,694 584,662 584,600 C584,528 620,470 682,470 Z",
       "Genny body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=620, y=508, width=90, height=48,
        fill="#FFFFFF", opacity=14, stroke=NONE)
# hoodie hem + drawstrings
d.path("M588,640 C630,656 734,656 776,640", "Hoodie hem", fill=NONE,
       stroke=HOOD_GRAD, strokeWidth=22, opacity=85)
d.path("M668,560 L666,596 M696,560 L698,596", "Drawstrings", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=80)
# face lifted to the terminal: eyes up-left, pupils catching green
d.shape("ellipse", "Eye L", x=634, y=514, width=26, height=30,
        fill="#2C2430", stroke=NONE)
d.shape("ellipse", "Eye R", x=704, y=514, width=26, height=30,
        fill="#2C2430", stroke=NONE)
d.shape("ellipse", "Glint L", x=638, y=518, width=8, height=8,
        fill=GREEN, opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=708, y=518, width=8, height=8,
        fill=GREEN, opacity=85, stroke=NONE)
d.path("M664,556 C672,563 692,563 700,556", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=622, y=548, width=24, height=12,
        fill="#C98A80", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=716, y=548, width=24, height=12,
        fill="#C98A80", opacity=45, stroke=NONE)
# a small heart pin at the hood's peak — the compileheart
d.path("M682,398 C674,388 660,390 660,402 C660,412 672,420 682,428 "
       "C692,420 704,412 704,402 C704,390 690,388 682,398 Z",
       "Heart pin", fill="#D4687A", stroke=INK, strokeWidth=3,
       join="round")

# --- the make.conf sheet, held up like scripture ----------------------------------
d.path(rot_rect_path(682, 620, 150, 104, -4), "make.conf sheet",
       fill=PAPER, stroke=INK, strokeWidth=4, join="round")
d.text("MAKE.CONF", "Sheet title", x=622, y=584, size=12,
       font="Virelai Sans", color="#5E5240", justify="left")
d.path("M616,592 L744,588", "Sheet rule", fill=NONE, stroke="#8E846C",
       strokeWidth=2, opacity=80)
# USE flags: ticked boxes — letters only, Virelai-safe
flags = [("X", True), ("GTK", True), ("ALSA", True),
         ("-SYSTEMD", False)]
for i, (flag, on) in enumerate(flags):
    fy = 598 + i * 15
    d.shape("rectangle", f"Flag box {i+1}", x=618, y=fy, width=12,
            height=12, fill="#D8D0B8", stroke=INK, strokeWidth=2)
    if on:
        d.path(f"M620,{fy+6} L624,{fy+10} L629,{fy+2}", f"Flag tick {i+1}",
               fill=NONE, stroke="#4E7E4A", strokeWidth=3, cap="round",
               join="round")
    else:
        d.path(f"M620,{fy+3} L628,{fy+9} M628,{fy+3} L620,{fy+9}",
               f"Flag cross {i+1}", fill=NONE, stroke="#A04A3E",
               strokeWidth=3, cap="round")
    d.text(flag, f"Flag name {i+1}", x=636, y=fy+11, size=11,
           font="Virelai Sans", color="#4E4636", justify="left")
# the penciled verdict in the margin
d.path("M720,616 C726,610 736,612 738,618 C740,626 730,632 724,628 "
       "M726,644 L738,642", "Sheet scrawl", fill=NONE, stroke="#8E7E5E",
       strokeWidth=2.5, cap="round", opacity=80)
# her paws under the sheet's lower edge
d.shape("ellipse", "Paw L", x=610, y=664, width=26, height=18,
        fill="#C9A096", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Paw R", x=724, y=660, width=26, height=18,
        fill="#C9A096", stroke=INK, strokeWidth=3)

# --- captions ----------------------------------------------------------------------
d.text("GENNY COMPILEHEART", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E8E2F4", justify="center")
r = d.text("BUILD-TIME ORACLE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AFA4CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("028.genny-compileheart-V1R00")
