#!/usr/bin/env python3
"""APH-036 Whistlin Winstinct — motivational-poster aphorism plate V1R00.
A THE FUTURE IS NOW poster: a boot window whose dream-blue glass fades to
dead gray, frosted UI shards drifting loose, and a commented-out line of
code pinned like a butterfly specimen. Vista before the storm.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-036 Whistlin Winstinct — Motivational Poster", 1000, 1000)

INK = "#0C1220"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A2438"}, {"offset": 1, "color": "#070B14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3C4C6E"}, {"offset": 0.7, "color": "#20293F"},
    {"offset": 1, "color": "#0C1220"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#242E48"}, {"offset": 1, "color": "#11152A"}]}}
WIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38445F"}, {"offset": 1, "color": "#1B2138"}]}}
SCR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6FB4E8"}, {"offset": 0.5, "color": "#66789A"},
    {"offset": 1, "color": "#3E4456"}]}}
SPEC_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A2238"}, {"offset": 1, "color": "#10162A"}]}}
GOLD = "#E8C470"
FRAME = "#B0C2DC"
HEAD = "#EEF2FA"
PUNCH = "#D0D6EA"
FAINT = "#8690AC"
GLASS_F = "#BFE0F4"
GLASS_S = "#D6E8F8"
CLOUD = "#0E1626"
BLUE = "#7FB8DC"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54648E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCD0F0", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=190, y=180, width=210, height=120,
        fill="#36456A", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=630, width=210, height=110,
        fill="#36456A", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(220, 275, 7), (788, 260, 8), (168, 480, 6),
                               (836, 478, 7), (255, 660, 6), (752, 662, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E5E8E", opacity=35, stroke=NONE)
# shard glints scattered on the plate, future debris
for i, (x, y, op) in enumerate([(268, 218, 42), (292, 210, 30),
                                 (706, 585, 42), (728, 592, 30)]):
    d.path(rot_rect_path(x, y, 10, 4, 30), f"Glint {i+1}", fill=GLASS_S,
           opacity=op, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#3C4868", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# incoming storm, still far off
d.shape("ellipse", "Cloud 1", x=PX + 40, y=PY + 30, width=170, height=14,
        fill=CLOUD, opacity=40, stroke=NONE)
d.shape("ellipse", "Cloud 2", x=PX + 340, y=PY + 26, width=180, height=12,
        fill=CLOUD, opacity=32, stroke=NONE)

# kicker + headline
r = d.text("VISTA BEFORE THE STORM", "Kicker", x=500, y=PY + 44, size=12,
           font="Virelai Sans", color=GOLD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "kicker tracking", ids=[r["id"]], tracking=280)
r = d.text("THE FUTURE IS NOW", "Headline", x=500, y=PY + 82,
           size=32, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=15)
d.path("M350,258 L472,258 M528,258 L650,258", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 258, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- glass shards adrift, off the shattered screen -----------------------------------
def shard(pts, label, fop, sop):
    p = "M" + " L".join(f"{x},{y}" for x, y in pts) + " Z"
    d.path(p, label, fill=GLASS_F, opacity=fop, stroke=GLASS_S,
           strokeWidth=1.5)

shard([(322, 292), (382, 272), (396, 336), (336, 358)], "Shard 1", 22, 40)
shard([(618, 296), (676, 278), (688, 344), (630, 366)], "Shard 2", 20, 38)
shard([(340, 408), (398, 392), (414, 458), (356, 476)], "Shard 3", 18, 34)
shard([(600, 428), (658, 444), (646, 502), (588, 486)], "Shard 4", 16, 30)
shard([(356, 268), (374, 258), (382, 276), (364, 286)], "Chip 1", 30, 50)
shard([(656, 256), (676, 246), (684, 266), (664, 276)], "Chip 2", 28, 48)
shard([(300, 372), (316, 366), (322, 382), (306, 388)], "Chip 3", 26, 44)
# hairline fracture trails where the shards tore free
d.path("M340,344 C320,338 306,330 296,318", "Fracture 1", fill=NONE,
       stroke=GLASS_S, strokeWidth=1, dash=[3, 4], cap="round", opacity=28)
d.path("M662,330 C684,322 698,312 708,298", "Fracture 2", fill=NONE,
       stroke=GLASS_S, strokeWidth=1, dash=[3, 4], cap="round", opacity=26)

# --- the boot window, glass already going gray -------------------------------------------
WX, WY, WW, WH = 408, 316, 184, 128
d.shape("ellipse", "Window shadow", x=WX - 14, y=WY + WH + 8,
        width=WW + 28, height=12, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Boot window", x=WX, y=WY, width=WW, height=WH,
        radius=10, fill=WIN_GRAD, stroke="#0A0E1A", strokeWidth=3)
# title strip divider + dead traffic dots
d.path(f"M{WX + 3},{WY + 24} L{WX + WW - 3},{WY + 24}", "Title rule",
       fill=NONE, stroke="#4A5878", strokeWidth=1.5, opacity=70)
for i, c in enumerate(["#56627E", "#56627E", "#56627E"]):
    d.shape("ellipse", f"Dot {i+1}", x=WX + 10 + i * 13, y=WY + 9,
            width=7, height=7, fill=c, opacity=80, stroke=NONE)
d.text("boot.exe", "Window title", x=WX + WW/2 + 8, y=WY + 17, size=8,
       font="Source Sans 3", color=FAINT, justify="center")
# the screen: dream blue on top, gray where the dream ran out
SX, SY, SW, SH = WX + 12, WY + 32, WW - 24, WH - 46
d.shape("rectangle", "Screen", x=SX, y=SY, width=SW, height=SH,
        radius=6, fill=SCR_GRAD, stroke="#0A0C16", strokeWidth=2)
# frosted streak across the glass
d.path(f"M{SX + 8},{SY + 10} L{SX + SW - 10},{SY + 2} "
       f"L{SX + SW - 4},{SY + 16} L{SX + 12},{SY + 24} Z",
       "Frost streak", fill=GLASS_S, opacity=12, stroke=NONE)
# the spinner that will never resolve
d.path(f"M{SX + SW/2},{SY + 26} A14,14 0 1 1 {SX + SW/2 - 10},{SY + 36}",
       "Spinner arc", fill=NONE, stroke=GLASS_S, strokeWidth=2.5,
       dash=[5, 5], cap="round", opacity=60)
d.shape("ellipse", "Spinner hub", x=SX + SW/2 - 2, y=SY + 38,
        width=4, height=4, fill=GLASS_S, opacity=50, stroke=NONE)
# gray lower half: dead rows where the UI used to be
for i in range(3):
    d.shape("rectangle", f"Dead row {i+1}", x=SX + 12,
            y=SY + SH - 30 + i * 9, width=SW - 24 - i * 22, height=4,
            radius=2, fill="#5A6278", opacity=55 - i * 12, stroke=NONE)
# caret, still blinking in the blue part
d.shape("rectangle", "Caret", x=SX + 14, y=SY + 52, width=8, height=3,
        fill=HEAD, opacity=75, stroke=NONE)

# --- the specimen: commented-out code, pinned like a butterfly -------------------------------
BX, BY, BW, BH = 620, 448, 116, 62
d.shape("rectangle", "Specimen shadow", x=BX + 4, y=BY + 5, width=BW,
        height=BH, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Specimen case", x=BX, y=BY, width=BW, height=BH,
        radius=4, fill=SPEC_GRAD, stroke="#56678E", strokeWidth=1.5)
# spread wings
d.path(f"M{BX + 58},{BY + 20} L{BX + 26},{BY + 10} L{BX + 20},{BY + 26} "
       f"L{BX + 52},{BY + 30} Z", "Wing L", fill=GLASS_F, opacity=24,
       stroke=GLASS_S, strokeWidth=1.2)
d.path(f"M{BX + 58},{BY + 20} L{BX + 90},{BY + 10} L{BX + 96},{BY + 26} "
       f"L{BX + 64},{BY + 30} Z", "Wing R", fill=GLASS_F, opacity=24,
       stroke=GLASS_S, strokeWidth=1.2)
# the pin
d.shape("ellipse", "Pin", x=BX + 55, y=BY + 17, width=7, height=7,
        fill=GOLD, opacity=90, stroke="#8A6A2C", strokeWidth=1)
d.path(f"M{BX + 58},{BY + 24} L{BX + 58},{BY + 34}", "Pin shaft",
       fill=NONE, stroke=GOLD, strokeWidth=1, opacity=70)
d.text("// future.load()", "Specimen label", x=BX + BW/2, y=BY + 48,
       size=8, font="Source Sans 3", color=FAINT, justify="center")
d.text("SPECIMEN 036", "Specimen tag", x=BX + BW/2, y=BY + 10, size=6,
       font="Source Sans 3", color="#5A6688", justify="center")

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("GLASS UI. SHATTERED TIMELINES.", "Punchline", x=500,
           y=PY + PH - 34, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch tracking", ids=[r["id"]], tracking=80)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("WHISTLIN WINSTINCT", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=HEAD, justify="center")
r = d.text("GLASS UI SHATTERED TIMELINES", "Role", x=500, y=950,
           size=18, font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-036-whistlin-winstinct-V1R00")
