#!/usr/bin/env python3
"""Jpegsey Artifactor — mascot portrait V1R00. Compression Goblin:
an endearing goblin whose silhouette has gone blocky at the seams from
one re-encode too many, squeezing a memory file beside the stack of
originals, a quality dial bolted to its pedestal and pinned at 70.
Chroma fringe + drifting artifact squares are hers, not the renderer's.
Sage goblin on a warm sand plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jpegsey Artifactor — Mascot Plate", 1000, 1000)

INK = "#2E2A22"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#171912"}, {"offset": 1, "color": "#080907"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B9AE94"}, {"offset": 0.62, "color": "#7E7559"},
    {"offset": 1, "color": "#4B4432"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 380], "end": [0, 720], "stops": [
    {"offset": 0, "color": "#9CB26E"}, {"offset": 0.55, "color": "#6E8A4E"},
    {"offset": 1, "color": "#4C6236"}]}}
BELLY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D4E0B2"}, {"offset": 1, "color": "#A4B878"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE4C8"}, {"offset": 1, "color": "#CFC29E"}]}}
BOX_GRAD = {"gradient": {"kind": "linear", "start": [0, 620], "end": [0, 740], "stops": [
    {"offset": 0, "color": "#4A5058"}, {"offset": 1, "color": "#2A2E34"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def stair(pts):
    """Closed staircase path through (x,y) points: only H/V segments,
    so every silhouette edge arrives as chunky lossy steps."""
    d_ = ["M%.0f,%.0f" % pts[0]]
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        d_.append("L%.0f,%.0f L%.0f,%.0f" % (x1, y0, x1, y1))
    d_.append("Z")
    return " ".join(d_)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#9AA184", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#201D14", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DDD4BC", strokeWidth=3, opacity=38)
# transparency-checker ghost patch, upper left of the plate
for r_ in range(4):
    for c_ in range(4):
        if (r_ + c_) % 2 == 0:
            x, y = 196 + c_ * 26, 196 + r_ * 26
            assert on_disc(x + 13, y + 13, 14), (x, y)
            d.shape("rectangle", f"Checker {r_}{c_}", x=x, y=y, width=26,
                    height=26, fill="#DCD4BE", opacity=11, stroke=NONE)
# patina + flecks
d.shape("ellipse", "Patina 1", x=560, y=140, width=260, height=150,
        fill="#C9C0A6", opacity=15, stroke=NONE)
d.shape("ellipse", "Patina 2", x=160, y=600, width=250, height=150,
        fill="#6A6248", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(200,330,6),(810,320,5),(170,540,7),(845,545,6),
                               (250,760,5),(740,760,6),(145,435,5),(860,610,5),
                               (430,112,5),(610,135,6),(320,150,4),(705,205,5),
                               (215,645,4),(875,445,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#EAE4D2", opacity=42, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M940,140 A100,100 0 0 0 845,55", "Ghost arc TR",
       fill=NONE, stroke="#5A6248", strokeWidth=14, opacity=10, cap="round")
d.path("M70,760 A120,120 0 0 0 180,880", "Ghost arc BL",
       fill=NONE, stroke="#5A6248", strokeWidth=10, opacity=8, cap="round")

# --- the memory-file stack --------------------------------------------------------
# five cards, each a little rotated; top card carries the photo icon
stack = [(620, 500, -9), (650, 478, -4), (600, 520, 6), (668, 512, 11)]
for i, (x, y, a) in enumerate(stack):
    r = d.shape("rectangle", f"Memory file {i+1}", x=x, y=y, width=170,
                height=120, radius=8, fill=PAPER_GRAD, stroke=INK,
                strokeWidth=4)
    if r and r.get("id"):
        d.cmd("object.rotate", f"file rot {i+1}", ids=[r["id"]],
              angle=a, origin=[x + 85, y + 60])
# top card: drawn upright, rotated -6
TX, TY = 610, 402
top_parts = []
def tshape(shape_, label, **kw):
    r = d.shape(shape_, label, **kw); top_parts.append(r); return r
def tpath(dd, label, **kw):
    r = d.path(dd, label, **kw); top_parts.append(r); return r
tshape("rectangle", "Top file", x=TX, y=TY, width=170, height=120, radius=8,
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
tshape("rectangle", "File header", x=TX, y=TY, width=170, height=22,
       radius=8, fill="#B8A87E", stroke=NONE)
tshape("rectangle", "Header mask", x=TX, y=TY + 14, width=170, height=10,
       fill="#B8A87E", stroke=NONE)
# the tiny picture inside: sky, sun, two mountains — a memory
tshape("rectangle", "Photo field", x=TX + 14, y=TY + 32, width=142, height=74,
       radius=4, fill="#9FC4D4", stroke="#6E5E44", strokeWidth=2)
tshape("ellipse", "Photo sun", x=TX + 118, y=TY + 40, width=18, height=18,
       fill="#F0C860", stroke=NONE)
tpath("M%d,%d L%d,%d L%d,%d Z" % (TX + 14, TY + 106, TX + 64, TY + 60,
                                  TX + 104, TY + 106), "Photo mt L",
      fill="#7A9464", stroke=NONE)
tpath("M%d,%d L%d,%d L%d,%d Z" % (TX + 62, TY + 106, TX + 108, TY + 52,
                                  TX + 156, TY + 106), "Photo mt R",
      fill="#5E7A50", stroke=NONE)
for r in top_parts:
    if r and r.get("id"):
        d.cmd("object.rotate", f"top rot {r['id']}", ids=[r["id"]],
              angle=-6, origin=[TX + 85, TY + 60])
for x, y in [(600, 390), (800, 400), (800, 650), (580, 660)]:
    assert on_disc(x, y, 0), (x, y)

# --- quality dial on its pedestal, pinned at 70 ------------------------------------
d.shape("rectangle", "Dial pedestal", x=628, y=640, width=168, height=102,
        radius=12, fill=BOX_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Dial face", x=652, y=656, width=72, height=72,
        fill="#E8E0C8", stroke=INK, strokeWidth=4)
# tick marks around a 270-degree sweep
DCX, DCY = 688, 692
for i in range(9):
    a = math.radians(-210 + i * 33.75)
    x0, y0 = DCX + 26 * math.cos(a), DCY + 26 * math.sin(a)
    x1, y1 = DCX + 32 * math.cos(a), DCY + 32 * math.sin(a)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (x0, y0, x1, y1), f"Dial tick {i+1}",
           fill=NONE, stroke="#6E5E44", strokeWidth=3, cap="round")
# needle at the 70 mark: -210 + 0.7*270 = -21 degrees
a70 = math.radians(-21)
d.path("M%.1f,%.1f L%.1f,%.1f" % (DCX, DCY,
       DCX + 24 * math.cos(a70), DCY + 24 * math.sin(a70)),
       "Dial needle", fill=NONE, stroke="#C84A3A", strokeWidth=5, cap="round")
d.shape("ellipse", "Dial hub", x=DCX - 6, y=DCY - 6, width=12, height=12,
        fill="#C84A3A", stroke=INK, strokeWidth=2)
# "Q·70" — the digit goes through Source Sans 3, not Virelai
d.text("Q", "Dial Q", x=756, y=678, size=16, font="Virelai Sans",
       color="#E8E0C8", justify="center")
d.text("70", "Dial 70", x=756, y=706, size=22, font="Source Sans 3",
       color="#E8E0C8", justify="center")
for x, y in [(628, 640), (796, 640), (796, 742), (628, 742)]:
    assert on_disc(x, y, 0), (x, y)

# --- chroma-fringe ghosts (color bleed from one encode too many) -------------------
SIL = [(360, 396), (404, 396), (438, 410), (460, 442), (468, 486),
       (476, 528), (468, 576), (476, 624), (462, 662), (424, 690),
       (398, 700), (322, 700), (292, 694), (258, 670), (248, 628),
       (254, 578), (244, 538), (252, 488), (244, 450), (262, 416),
       (304, 400)]
for dx, col, op in [(7, "#58C8D8", 20), (-7, "#D85A9A", 20)]:
    d.path(stair([(x + dx, y) for x, y in SIL]),
           f"Fringe {col}", fill=col, opacity=op, stroke=NONE)

# --- ground shadow -----------------------------------------------------------------
d.shape("ellipse", "Ground shadow", x=210, y=692, width=300, height=28,
        fill="#1C1E14", opacity=30, stroke=NONE)
d.shape("ellipse", "Stack shadow", x=590, y=632, width=230, height=20,
        fill="#1C1E14", opacity=22, stroke=NONE)

# --- Jpegsey: blocky little goblin ---------------------------------------------------
# ears first so the head overlaps their roots
earL = [(300, 424), (196, 380), (212, 470)]
earR = [(426, 422), (532, 388), (516, 472)]
d.path(stair(earL), "Ear L", fill="#6E8A4E", stroke=INK, strokeWidth=5, join="round")
d.path(stair(earR), "Ear R", fill="#6E8A4E", stroke=INK, strokeWidth=5, join="round")
d.path(stair([(284, 430), (230, 402), (238, 450)]), "Ear L inner",
       fill="#4C6236", opacity=80, stroke=NONE)
d.path(stair([(442, 428), (498, 404), (490, 450)]), "Ear R inner",
       fill="#4C6236", opacity=80, stroke=NONE)

# body
d.path(stair(SIL), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6, join="round")
# belly
d.shape("ellipse", "Belly", x=282, y=560, width=150, height=116,
        fill=BELLY_GRAD, opacity=70, stroke=NONE)
# sheen + base shade
d.shape("ellipse", "Head sheen", x=272, y=404, width=180, height=60,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M268,668 C320,692 400,692 452,666 C400,684 320,686 268,668 Z",
       "Base shade", fill="#3C4E28", opacity=35, stroke=NONE)
# faint 8x8 macroblock grid riding her lower right flank
for i in range(3):
    d.path("M%d,606 L%d,606" % (402 + 0 * i, 462 - i * 4), f"Block h{i}",
           fill=NONE, stroke="#3C4E28", strokeWidth=3, opacity=30)
d.path("M412,600 L456,600 M416,624 L460,624 M408,648 L452,648",
       "Block rows", fill=NONE, stroke="#3C4E28", strokeWidth=3, opacity=30)
d.path("M420,592 L420,664 M442,594 L442,664",
       "Block cols", fill=NONE, stroke="#3C4E28", strokeWidth=3, opacity=30)

# feet: blocky stubs
d.shape("rectangle", "Foot L", x=262, y=688, width=64, height=30, radius=8,
        fill="#5E7840", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Foot R", x=390, y=688, width=64, height=30, radius=8,
        fill="#5E7840", stroke=INK, strokeWidth=5)

# the file she's mid-squeeze on: already visibly smaller, artifact-dusted
sq = []
def sqshape(shape_, label, **kw):
    r = d.shape(shape_, label, **kw); sq.append(r); return r
def sqpath(dd, label, **kw):
    r = d.path(dd, label, **kw); sq.append(r); return r
sqshape("rectangle", "Squeeze file", x=464, y=556, width=110, height=80,
        radius=6, fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
sqshape("rectangle", "Squeeze photo", x=474, y=566, width=90, height=56,
        radius=3, fill="#9FC4D4", stroke="#6E5E44", strokeWidth=2)
sqpath("M474,622 L508,584 L536,622 Z", "Squeeze mt L",
       fill="#7A9464", stroke=NONE)
sqpath("M516,622 L546,576 L564,622 Z", "Squeeze mt R",
       fill="#5E7A50", stroke=NONE)
# the compression blocks crawling over it
for i, (x, y, c) in enumerate([(478, 570, "#58C8D8"), (524, 570, "#D85A9A"),
                               (500, 592, "#E8D860"), (546, 596, "#58C8D8"),
                               (486, 606, "#D85A9A")]):
    sqshape("rectangle", f"Artifact {i+1}", x=x, y=y, width=14, height=14,
            fill=c, opacity=38, stroke=NONE)
for r in sq:
    if r and r.get("id"):
        d.cmd("object.rotate", f"sq rot {r['id']}", ids=[r["id"]],
              angle=7, origin=[519, 596])

# arms: stubby staircase limbs hugging the file
d.path(stair([(238, 540), (200, 556), (206, 594), (246, 584)]),
       "Arm L", fill="#6E8A4E", stroke=INK, strokeWidth=5, join="round")
d.path(stair([(470, 560), (508, 576), (504, 606), (466, 592)]),
       "Arm R", fill="#6E8A4E", stroke=INK, strokeWidth=5, join="round")

# face: big endearing eyes, one riding a pixel higher than the other
for cx, cy, pw in [(322, 486, 46), (406, 478, 44)]:
    d.shape("ellipse", f"Eye white {cx}", x=cx - pw // 2, y=cy - 22,
            width=pw, height=44, fill="#F8F2E2", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil {cx}", x=cx - 7, y=cy - 2, width=17, height=17,
            fill="#2C2620", stroke=NONE)
    d.shape("ellipse", f"Glint {cx}", x=cx - 3, y=cy + 1, width=5, height=5,
            fill="#FFFFFF", opacity=90, stroke=NONE)
# soft worried-pleased brows
d.path("M300,458 C312,450 328,448 340,454", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M390,452 C402,444 418,444 428,450", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# little smile with one buck tooth — wobbly but fine with it
d.path("M322,552 C344,568 384,566 402,548", "Smile",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("rectangle", "Tooth", x=352, y=556, width=14, height=12, radius=2,
        fill="#F4EEDC", stroke=INK, strokeWidth=2)
# cheek artifact squares instead of blush — she blushes in macroblocks
d.shape("rectangle", "Cheek artifact L", x=272, y=528, width=16, height=16,
        fill="#D85A9A", opacity=30, stroke=NONE)
d.shape("rectangle", "Cheek artifact R", x=428, y=522, width=16, height=16,
        fill="#58C8D8", opacity=30, stroke=NONE)
# stray blocks drifting off her silhouette — loss, escaping
for i, (x, y, s, c, o) in enumerate([(488, 452, 12, "#58C8D8", 40),
                                     (504, 502, 9, "#D85A9A", 35),
                                     (236, 486, 10, "#D85A9A", 30),
                                     (220, 520, 8, "#58C8D8", 28),
                                     (492, 640, 10, "#E8D860", 30)]):
    assert on_disc(x, y, 8), (x, y)
    d.shape("rectangle", f"Drift block {i+1}", x=x, y=y, width=s, height=s,
            fill=c, opacity=o, stroke=NONE)

# --- name + role ---------------------------------------------------------------------
d.text("JPEGSEY ARTIFACTOR", "Name", x=500, y=930, size=50, font="Virelai Sans",
       color="#E8E0C8", justify="center")
r = d.text("COMPRESSION GOBLIN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B8AC8E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=220)

d.finish("017.jpegsey-artifactor-V1R00")
