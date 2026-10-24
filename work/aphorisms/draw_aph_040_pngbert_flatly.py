#!/usr/bin/env python3
"""APH-040 Pngbert Flatly — aphorism plate V1R00. A diptych of one image
file: left panel, a crisp pixel landscape on a transparency checkerboard
with a marquee-selected hole cut clean through; right panel, the same
sprite reprocessed — jittered, desaturated, smearing out of its cells.
Lossless vs lossy, captioned accordingly. Slate-violet plate, editor
HUD chips. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

random.seed(40)

d = Draw()
d.new_doc("APH-040 Pngbert Flatly — Aphorism Plate", 1000, 1000)

INK = "#14101E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#211A30"}, {"offset": 1, "color": "#0D0A14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3C3252"}, {"offset": 0.7, "color": "#241D38"},
    {"offset": 1, "color": "#131022"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2438"}, {"offset": 1, "color": "#181426"}]}}
CHIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4268"}, {"offset": 1, "color": "#2E2848"}]}}
CHK_A, CHK_B = "#9A9EAA", "#6A6E7A"
CREAM = "#ECE6F4"
FAINT = "#948CB0"
KEY = "#CFC6E8"
AMBER = "#E8B45A"

# sprite palette: (cell top, cell bottom) per symbol — every pixel shaded
SKY = ("#7AD4E0", "#54A8BC")
SUN = ("#F4D06A", "#DBA03A")
MTN = ("#7E6FA6", "#54477A")
GRD = ("#8AC468", "#5E9040")
# the reprocessed palette: same hues wrung out
SM_SKY = ("#8AAAB0", "#6E8A90")
SM_SUN = ("#C8B080", "#A08858")
SM_MTN = ("#847A94", "#665E74")
SM_GRD = ("#8AA078", "#6A7E5C")

SPRITE = [
    "SSSSSSSSSSSS",
    "SSSSSSYYSSSS",
    "SSSSSYYYYSSS",
    "SSSSSSYYSSSS",
    "SSSSMMMMSSSS",
    "SSMMMMMMMSMS",
    "SMMMMMMMMMMS",
    "SMMMMMMMMMMS",
    "GGGGGGGGGGGG",
    "GGGGGGGGGGGG",
]
COLS, ROWS = 12, 10
HOLE = [(c, r) for r in (5, 6, 7) for c in (5, 6, 7, 8)]

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5C4E82", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B4A8DC", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=200, y=170, width=210, height=120,
        fill="#4A3E68", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=610, width=210, height=120,
        fill="#4A3E68", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(220, 280, 7), (790, 250, 8), (165, 480, 6),
                               (838, 470, 7), (255, 650, 6), (752, 660, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6C5C9A", opacity=35, stroke=NONE)

# --- left panel: the original --------------------------------------------------
PX, PY, PW, PH = 225, 200, 350, 380        # panel
d.shape("rectangle", "Panel shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, radius=12, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Panel", x=PX, y=PY, width=PW, height=PH,
        radius=12, fill=PANEL_GRAD, stroke="#5C4E82", strokeWidth=3)
# titlebar
for i, c in enumerate(["#C05A50", "#C89A4A", "#4CB868"]):
    d.shape("ellipse", f"Dot {i+1}", x=PX + 16 + i * 17, y=PY + 14,
            width=9, height=9, fill=c, opacity=85, stroke=NONE)
d.text("flatly_final.png", "Filename", x=PX + PW - 16, y=PY + 25,
       size=12, font="Source Sans 3", color=FAINT, justify="right")
d.path(f"M{PX},{PY + 38} L{PX + PW},{PY + 38}", "Titlebar rule",
       fill=NONE, stroke="#5C4E82", strokeWidth=2, opacity=70)

CELL = 24
GX, GY = PX + 31, PY + 76                  # grid origin inside panel
# checkerboard: the 1-cell ring around the sprite + the hole cells
for r in range(ROWS + 2):
    for c in range(COLS + 2):
        in_sprite = 1 <= c <= COLS and 1 <= r <= ROWS
        in_hole = (c - 1, r - 1) in HOLE
        if in_sprite and not in_hole:
            continue
        fill = CHK_A if (c + r) % 2 == 0 else CHK_B
        d.shape("rectangle", f"chk {c},{r}", x=GX + c * CELL,
                y=GY + r * CELL, width=CELL, height=CELL,
                fill=fill, stroke=NONE)
# the sprite: original proportions intact, every cell shaded
PAL = {"S": SKY, "Y": SUN, "M": MTN, "G": GRD}
for r in range(ROWS):
    for c in range(COLS):
        if (c, r) in HOLE:
            continue
        top, bot = PAL[SPRITE[r][c]]
        d.shape("rectangle", f"px {c},{r}", x=GX + (c + 1) * CELL,
                y=GY + (r + 1) * CELL, width=CELL, height=CELL,
                fill={"gradient": {"kind": "linear", "stops": [
                    {"offset": 0, "color": top},
                    {"offset": 1, "color": bot}]}},
                stroke="#14101E", strokeWidth=0.75, opacity=96)
# marquee ants around the transparent hole
hx, hy = GX + 6 * CELL, GY + 6 * CELL
d.shape("rectangle", "Marquee dark", x=hx, y=hy, width=4 * CELL,
        height=3 * CELL, fill=NONE, stroke="#14101E", strokeWidth=2,
        dash=[5, 5])
d.shape("rectangle", "Marquee light", x=hx + 2, y=hy + 2, width=4 * CELL - 4,
        height=3 * CELL - 4, fill=NONE, stroke="#ECE6F4", strokeWidth=1.5,
        dash=[5, 5], opacity=85)
# three pixels drifting out of the hole — transparency preserved
for i, (cx, cy, s, op) in enumerate([(545, 430, 14, 60), (586, 408, 11, 45),
                                     (620, 382, 9, 32)]):
    d.path(rot_rect_path(cx, cy, s, s, -18 - i * 8), f"Leak {i+1}",
           fill=MTN[0], opacity=op, stroke=NONE)
# zoom HUD chip on the panel corner — digits in Source Sans 3
d.shape("rectangle", "Zoom chip", x=PX - 14, y=PY + 54, width=74,
        height=30, radius=7, fill=CHIP_GRAD, stroke="#5C4E82",
        strokeWidth=2.5)
d.text("800%", "Zoom", x=PX + 23, y=PY + 75, size=14,
       font="Source Sans 3", color=AMBER, justify="center")
# panel gloss, up in the titlebar
d.shape("ellipse", "Panel gloss", x=PX + 40, y=PY + 8, width=170,
        height=10, fill="#FFFFFF", opacity=10, stroke=NONE)

# --- right panel: reprocessed ----------------------------------------------------
RX, RY = 700, 315        # panel center
RW, RH = 190, 230
d.path(rot_rect_path(RX + 6, RY + 8, RW, RH, 5), "Repro shadow",
       fill="#000000", opacity=30, stroke=NONE)
d.path(rot_rect_path(RX, RY, RW, RH, 5), "Repro panel",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#342030"},
           {"offset": 1, "color": "#1C1420"}]}},
       stroke="#7A4A58", strokeWidth=3)
SC = 13                  # smeared cell size
SPAL = {"S": SM_SKY, "Y": SM_SUN, "M": SM_MTN, "G": SM_GRD}
ox, oy = RX - COLS * SC / 2, RY - ROWS * SC / 2 - 8
for r in range(ROWS):
    for c in range(COLS):
        jx = random.uniform(-4.5, 4.5)
        jy = random.uniform(-3.5, 3.5)
        top, bot = SPAL[SPRITE[r][c]]
        d.path(rot_rect_path(ox + (c + 0.5) * SC + jx,
                             oy + (r + 0.5) * SC + jy,
                             SC + random.uniform(-2, 5),
                             SC + random.uniform(-2, 4),
                             random.uniform(-9, 9)),
               f"sm {c},{r}",
               fill={"gradient": {"kind": "linear", "stops": [
                   {"offset": 0, "color": top},
                   {"offset": 1, "color": bot}]}},
               stroke=NONE, opacity=50)
# macroblock artifacts: big pale squares squatting on the detail
for i, (cx, cy, s) in enumerate([(RX - 38, RY - 36, 30), (RX + 26, RY - 8, 36),
                                 (RX - 6, RY + 40, 26), (RX + 46, RY + 48, 22),
                                 (RX - 54, RY + 26, 22)]):
    d.path(rot_rect_path(cx, cy, s, s, 5), f"Artifact {i+1}",
           fill="#C8BCCF", opacity=18, stroke=NONE)
# ghost echo of the whole sprite, slid down-right
for r in range(ROWS):
    for c in range(0, COLS, 2):
        top, _ = SPAL[SPRITE[r][c]]
        d.shape("rectangle", f"echo {c},{r}",
                x=ox + c * SC + 26, y=oy + r * SC + 20,
                width=SC, height=SC, fill=top, opacity=13, stroke=NONE)

# --- caption chips -----------------------------------------------------------------
d.shape("rectangle", "Chip L", x=330, y=606, width=140, height=34,
        radius=17, fill=CHIP_GRAD, stroke="#5C4E82", strokeWidth=2.5)
d.text("LOSSLESS", "Chip L text", x=400, y=628, size=14,
       font="Source Sans 3", color=KEY, justify="center")
d.path(rot_rect_path(700, 623, 120, 34, 5), "Chip R",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#5A3040"},
           {"offset": 1, "color": "#381E2C"}]}},
       stroke="#7A4A58", strokeWidth=2.5)
d.text("LOSSY", "Chip R text", x=700, y=628, size=14,
       font="Source Sans 3", color="#D8A8B4", justify="center")

# --- aphorism line + name + role ----------------------------------------------------
r = d.text("PIXEL PURITY.", "Key line", x=500, y=752, size=24,
           font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=140)

d.text("PNGBERT FLATLY", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("DISCREET SUPERIORITY", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-040-pngbert-flatly-V1R00")
