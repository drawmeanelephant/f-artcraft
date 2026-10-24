#!/usr/bin/env python3
"""APH-017 Jpegsey Artifactor — aphorism plate V1R00. A gilt museum frame
holding a portrait made of visible 8x8 blocks — the compression artifacts
are the picture: displaced blocks, wrong-hue ringing, corners sanded off,
one block fallen out entirely onto the mat. Blur cited as atmosphere.
Museum plaque: Q = 12. Sepia-olive plate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-017 Jpegsey Artifactor — Aphorism Plate", 1000, 1000)

INK = "#262014"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1A12"}, {"offset": 1, "color": "#0A0A06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#44422E"}, {"offset": 0.7, "color": "#26241A"},
    {"offset": 1, "color": "#12110B"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C860"}, {"offset": 0.5, "color": "#B8862E"},
    {"offset": 1, "color": "#7A5418"}]}}
MAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E4638"}, {"offset": 1, "color": "#2A2620"}]}}
CREAM = "#EAE0C4"
FAINT = "#9A8E66"

# block palette — the image, such as it is
PAL = {
    ".": "#8AA0A8",  # sky/background
    "D": "#5E4A3A",  # hair
    "F": "#C8A882",  # face
    "E": "#3A2E26",  # features
    "M": "#A86A5A",  # mouth
    "S": "#7A8A90",  # shoulders
}
GRID = [
    ". . D D D D . .",
    ". D D D D D D .",
    ". D F F F F D .",
    ". D F E F E D .",
    ". . F F F F . .",
    ". . F M M F . .",
    ". . . F F . . .",
    ". S S S S S S .",
]
# blocks that got displaced by the last save — (col, row) -> (dx, dy)
DISPLACED = {(5, 2): (7, 4), (1, 5): (-6, 3), (6, 6): (5, -6)}
# ringing artifacts: wrong hue entirely
WRONG = {(0, 4): "#8A5A6E", (7, 3): "#6E7A4E", (2, 7): "#5A6E7A"}
# corners sanded off — heavy fade
FADED = {(0, 0), (7, 0), (0, 7), (7, 7), (0, 1), (7, 6)}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A8984E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCA0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(202, 218, 7), (796, 212, 8), (162, 500, 6),
                               (844, 492, 7), (244, 744, 6), (760, 736, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7A7050", opacity=35, stroke=NONE)
# museum spotlight
d.shape("ellipse", "Spotlight", x=320, y=180, width=360, height=440,
        fill="#E8DCB0", opacity=10, stroke=NONE)
# floor shadow under the frame
d.shape("ellipse", "Floor shadow", x=320, y=640, width=400, height=44,
        fill="#000000", opacity=35, stroke=NONE)

# --- the gilt frame ------------------------------------------------------------
d.shape("rectangle", "Frame shadow", x=306, y=206, width=408, height=448,
        radius=6, fill="#000000", opacity=40, stroke=NONE)
d.shape("rectangle", "Frame", x=296, y=196, width=408, height=448,
        radius=6, fill=GOLD_GRAD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Frame bevel", x=310, y=210, width=380, height=420,
        radius=4, fill=NONE, stroke="#F4E4A0", strokeWidth=3, opacity=60)
d.shape("rectangle", "Frame inner", x=318, y=218, width=364, height=404,
        radius=3, fill=MAT_GRAD, stroke=INK, strokeWidth=3)
# corner rosettes — gilded and slightly smeared
for cx, cy in [(310, 210), (690, 210), (310, 630), (690, 630)]:
    d.shape("ellipse", f"Rosette {cx}-{cy}", x=cx - 11, y=cy - 11,
            width=22, height=22, fill="#E8C860", stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"Rosette dot {cx}-{cy}", x=cx - 4, y=cy - 4,
            width=8, height=8, fill="#8A6220", stroke=NONE)

# --- the 8x8 masterpiece --------------------------------------------------------
BX, BY, BS = 332, 252, 42
for row_i, row in enumerate(GRID):
    for col_i, cell in enumerate(row.split()):
        color = WRONG.get((col_i, row_i), PAL[cell])
        dx, dy = DISPLACED.get((col_i, row_i), (0, 0))
        op = 30 if (col_i, row_i) in FADED else 92
        d.shape("rectangle", f"Block {row_i}-{col_i}",
                x=BX + col_i * BS + dx, y=BY + row_i * BS + dy,
                width=BS - 1, height=BS - 1, fill=color, opacity=op,
                stroke=NONE)
# ghost seams — the block grid never truly hides
for k in range(1, 8):
    d.path(f"M{BX + k * BS},{BY} L{BX + k * BS},{BY + 8 * BS}",
           f"V seam {k}", fill=NONE, stroke="#0E0C08", strokeWidth=1,
           opacity=35)
    d.path(f"M{BX},{BY + k * BS} L{BX + 8 * BS},{BY + k * BS}",
           f"H seam {k}", fill=NONE, stroke="#0E0C08", strokeWidth=1,
           opacity=35)
# the blur, cited as atmosphere
d.shape("ellipse", "Atmosphere 1", x=380, y=300, width=200, height=140,
        fill="#D8CCA0", opacity=14, stroke=NONE)
d.shape("ellipse", "Atmosphere 2", x=470, y=450, width=180, height=110,
        fill="#8AA0A8", opacity=12, stroke=NONE)

# the block that fell out — original state reclassified
d.path(rot_rect_path(648, 668, 40, 40, -14), "Fallen block",
       fill="#C8A882", stroke=INK, strokeWidth=3)
d.path("M632,700 Q648,708 666,700", "Fallen dust", fill=NONE,
       stroke=CREAM, strokeWidth=2, opacity=30, dash=[3, 6], cap="round")

# mosquito noise ringing the frame
for i, (nx, ny, nr) in enumerate([(282, 300, 3), (714, 260, 4), (724, 420, 3),
                                  (278, 470, 3), (290, 560, 4), (716, 560, 3),
                                  (400, 182, 3), (560, 180, 3), (480, 656, 3)]):
    d.shape("ellipse", f"Noise {i+1}", x=nx - nr, y=ny - nr,
            width=nr * 2, height=nr * 2, fill="#C8B87E", opacity=45,
            stroke=NONE)

# museum plaque
d.shape("rectangle", "Plaque", x=402, y=672, width=196, height=34,
        radius=4, fill="#3A3018", stroke="#C9A868", strokeWidth=2)
r = d.text("Q = 12 · EDITION ∞", "Plaque text", x=500, y=695, size=13,
           font="Virelai Sans", color="#C9A868", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "plaque tracking", ids=[r["id"]], tracking=40)

# --- aphorism line + name + role --------------------------------------------------
r = d.text("COMPRESS ONCE MORE:", "Key line 1", x=500, y=738,
           size=22, font="Virelai Sans", color="#D8CCA0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("THE ARTIFACT IS THE ART NOW.", "Key line 2", x=500, y=772,
           size=22, font="Virelai Sans", color="#D8CCA0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("JPEGSEY ARTIFACTOR", "Name", x=500, y=905, size=52,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("LOSSY BECAME THE HOUSE STYLE", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#9A8E66", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-017-jpegsey-artifactor-V1R00")
