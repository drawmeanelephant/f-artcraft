#!/usr/bin/env python3
"""Friendrick the Extant — mascot portrait V1R00.
A pale residual process still pinging beside a TOP 8 grid of empty profile
slots, one of them forever loading; his clipboard is nonfunctional, but
spiritually heavy. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Friendrick the Extant — Mascot Portrait", 1000, 1000)

INK = "#23202A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1210"}, {"offset": 1, "color": "#050807"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#27382F"}, {"offset": 0.7, "color": "#16201A"},
    {"offset": 1, "color": "#0A0F0C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B2620"}, {"offset": 1, "color": "#0A0F0C"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8D0E0"}, {"offset": 0.72, "color": "#9AA4BE"},
    {"offset": 1, "color": "#707C98"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#1C2E28"}, {"offset": 0.7, "color": "#12201C"},
    {"offset": 1, "color": "#0A1210"}]}}
PHOS = "#9FD8B0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8A78", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D0C0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#32443A", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080C0A",
       strokeWidth=4, opacity=70)

# --- the TOP 8 grid: eight slots, all of them empty --------------------------------
px, py = 506, 190
d.shape("ellipse", "Panel glow", x=px - 30, y=py + 60, width=360, height=340,
        fill=PHOS, opacity=6, stroke=NONE)
d.shape("rectangle", "Panel bezel", x=px, y=py, width=300, height=400,
        fill="#1A2220", stroke=INK, strokeWidth=6, radius=18)
d.shape("rectangle", "Panel screen", x=px + 14, y=py + 14, width=272,
        height=372, fill=SCREEN_GRAD, stroke="#32443A", strokeWidth=3,
        radius=12)
# header: TOP 8 — the digit set in Source Sans 3 (Virelai carries no figures)
t = d.text("TOP 8", "Panel title", x=px + 150, y=py + 52, size=26,
           font="Source Sans 3", color=PHOS, justify="center")
if t and t.get("id"):
    d.cmd("text.setStyle", "title tracking", ids=[t["id"]], tracking=180)
d.path(f"M{px+40},{py+68} L{px+260},{py+68}", "Header rule", fill=NONE,
       stroke="#32443A", strokeWidth=2, opacity=80)

# profile slots: 2 rows x 4 cols; ghost silhouettes in seven, a spinner in one
sx, sy, sw, sh, gap = px + 26, py + 88, 54, 62, 12
for r2 in range(2):
    for c in range(4):
        x = sx + c * (sw + gap)
        y = sy + r2 * (sh + 34)
        n = r2 * 4 + c
        d.shape("rectangle", f"Slot {n+1}", x=x, y=y, width=sw, height=sh,
                fill="#14201C", stroke="#3E524A", strokeWidth=2.5,
                radius=8, dash=[5, 4])
        if n == 6:
            # the slot that never resolves: a loading arc, mid-turn
            d.path(f"M{x+27},{y+12} A15,15 0 1 1 {x+17},{y+20}",
                   "Slot spinner", fill=NONE, stroke=PHOS, strokeWidth=3.5,
                   cap="round", opacity=85)
            d.shape("ellipse", "Spinner hub", x=x+23, y=y+27, width=8,
                    height=8, fill=PHOS, opacity=50, stroke=NONE)
        else:
            # the emptied profile: head + shoulders, faded to a rumour
            hx = x + sw / 2
            d.shape("ellipse", f"Slot head {n+1}", x=hx - 10, y=y + 10,
                    width=20, height=20, fill="#6E8478", opacity=25,
                    stroke=NONE)
            d.path(f"M{hx-16},{y+sh-8} C{hx-16},{y+sh-26} {hx+16},{y+sh-26} "
                   f"{hx+16},{y+sh-8}", f"Slot shoulders {n+1}", fill=NONE,
                   stroke="#6E8478", strokeWidth=8, opacity=25, cap="round")
        # name bar under each slot: text that used to be there
        d.shape("rectangle", f"Name bar {n+1}", x=x + 6, y=y + sh + 8,
                width=sw - 12, height=8, fill="#2A3830", stroke=NONE,
                radius=4, opacity=80)

# the greyed button that still offers to connect
d.shape("rectangle", "Add button", x=px + 92, y=py + 348, width=116,
        height=28, fill="#222E2A", stroke="#3E524A", strokeWidth=2.5,
        radius=14, dash=[4, 4])
d.text("ADD FRIEND", "Add label", x=px + 150, y=py + 367, size=11,
       font="Source Sans 3", color="#5A7466", justify="center")

# scanlines: the screen remembers being a screen
for i, yy in enumerate(range(py + 84, py + 340, 34)):
    d.path(f"M{px+16},{yy} L{px+284},{yy}", f"Scanline {i+1}", fill=NONE,
           stroke="#0A1410", strokeWidth=2, opacity=40)

# --- Friendrick: a residual process, still courteous ---------------------------------
d.shape("ellipse", "Body shadow", x=252, y=682, width=230, height=24,
        fill="#060A08", opacity=55, stroke=NONE)
d.path("M366,336 C470,336 524,424 522,536 C520,634 460,698 366,698 "
       "C272,698 214,634 212,536 C210,424 262,336 366,336 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7, opacity=94)
# dissolution at the base: small squares of him, leaving slowly
for i, (x, y, w, o) in enumerate([(252,676,12,45),(282,688,9,35),(452,682,11,40),
                                  (478,668,8,30),(316,694,7,28)]):
    d.shape("rectangle", f"Residue {i+1}", x=x, y=y, width=w, height=w,
            fill="#9AA4BE", opacity=o, stroke=NONE, radius=2)
d.shape("ellipse", "Belly light", x=290, y=520, width=160, height=140,
        fill="#E4EAF6", opacity=20, stroke=NONE)
d.shape("ellipse", "Head sheen", x=278, y=360, width=170, height=56,
        fill="#FFFFFF", opacity=12, stroke=NONE)
d.path("M226,470 C212,540 222,612 258,660", "Flank shade", fill=NONE,
       stroke="#5C6884", strokeWidth=16, opacity=30, cap="round")

# he still pings: a small antenna and three arcs of hope
d.path("M366,336 L366,308", "Antenna", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.shape("ellipse", "Ping dot", x=360, y=298, width=12, height=12,
        fill=PHOS, stroke=INK, strokeWidth=2.5)
for i, r in enumerate([22, 34]):
    d.path(f"M{366-r},{308} A{r},{r} 0 0 1 {366+r},{308}", f"Ping {i+1}",
           fill=NONE, stroke=PHOS, strokeWidth=3, cap="round",
           opacity=55 - i * 18)

# the face: gentle, wistful, pointed at the grid
for i, cx2 in enumerate([330, 412]):
    d.shape("ellipse", f"Eye {i+1}", x=cx2 - 13, y=446, width=26, height=30,
            fill="#1E161C", stroke=NONE)
    d.shape("ellipse", f"Glint {i+1}", x=cx2 - 6, y=452, width=7, height=7,
            fill="#FFFFFF", opacity=85, stroke=NONE)
# brows: the beginning of an apology
d.path("M314,428 C324,420 338,418 348,424", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=80)
d.path("M396,424 C406,418 420,420 428,428", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=80)
# the smile that may return a 404
d.path("M334,512 C356,530 384,530 404,514", "Smile", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")

# --- the clipboard: nonfunctional, spiritually heavy ----------------------------------
# arm cradles it against the chest
bx, by, bang = 470, 560, 9
d.path("M446,540 C476,552 492,566 500,586", "Arm", fill=NONE,
       stroke="#9AA4BE", strokeWidth=24, cap="round")
d.path(rot_rect_path(bx + 6, by + 8, 110, 140, bang), "Board shadow",
       fill="#060A08", opacity=40, stroke=NONE)
d.path(rot_rect_path(bx, by, 110, 140, bang), "Clipboard",
       fill="#6B4A36", stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(bx, by + 4, 88, 116, bang), "Clip paper",
       fill="#D8CCB0", stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Clip", x=bx - 12, y=by - 74, width=26, height=18,
        fill="#8A6A2E", stroke=INK, strokeWidth=3)
# one faint 404 and a column of boxes no one checks
d.text("404", "Paper note", x=bx - 30, y=by - 40, size=15,
       font="Source Sans 3", color="#8A7A64", justify="left")
for i, yy in enumerate([by - 16, by + 6, by + 28]):
    d.shape("rectangle", f"Checkbox {i+1}", x=bx - 30, y=yy, width=10,
            height=10, fill=NONE, stroke="#8A7A64", strokeWidth=2, radius=2)
    d.path(f"M{bx-14},{yy+7} L{bx+30},{yy+7}", f"Check line {i+1}",
           fill=NONE, stroke="#B0A488", strokeWidth=2, opacity=60)
d.shape("ellipse", "Hand", x=490, y=576, width=42, height=34,
        fill="#AAB4CC", stroke=INK, strokeWidth=4)
# a cursor, still hovering over the smile — someone has tried
d.path("M408,538 L408,564 L416,557 L421,568 L426,566 L421,555 L430,555 Z",
       "Cursor", fill="#D8DEE8", stroke=INK, strokeWidth=2.5,
       join="round", opacity=90)

# --- captions -------------------------------------------------------------------------
d.text("FRIENDRICK THE EXTANT", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#DCE8DC", justify="center")
r = d.text("RESIDUAL RECONCILIATION PROCESS", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#9DB8A4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("301.friendrick-the-extant-V1R00")
