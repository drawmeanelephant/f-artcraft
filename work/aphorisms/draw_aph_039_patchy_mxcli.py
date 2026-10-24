#!/usr/bin/env python3
"""APH-039 Patchy Mx.CLI — aphorism plate V1R00. A perfectly typeset
documentation page — double-ruled title, ruthlessly justified body,
footnote block squared away — standing on a foundation that is already
rot: a brick beam split by a crack and laced shut with amber sutures,
a post leaning, bricks mid-fall, mold blotches creeping. Footnotes
themselves have drifted off the page, still looking for a sentence.
Oxblood plate, bone paper, sickly green rot. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-039 Patchy Mx.CLI — Aphorism Plate", 1000, 1000)

INK = "#2A1A18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221418"}, {"offset": 1, "color": "#0C0709"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E3236"}, {"offset": 0.7, "color": "#2E1E22"},
    {"offset": 1, "color": "#160F11"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E8D2"}, {"offset": 0.65, "color": "#DFCFAE"},
    {"offset": 1, "color": "#BFA87E"}]}}
BRICK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A6A50"}, {"offset": 0.6, "color": "#74493A"},
    {"offset": 1, "color": "#4A2C22"}]}}
POST_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4A34"}, {"offset": 1, "color": "#3E2718"}]}}
ROT = "#7A9455"
THREAD = "#D8A846"
CREAM = "#EFE6D0"
FAINT = "#9A7E7A"
KEY = "#D8BFA8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A5A58", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8BFA8", strokeWidth=3, opacity=40)
# plate patina
d.shape("ellipse", "Patina 1", x=200, y=180, width=200, height=120,
        fill="#6E464A", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=595, width=220, height=130,
        fill="#6E464A", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(208, 258, 7), (795, 248, 8), (158, 502, 6),
                               (843, 498, 7), (250, 738, 6), (760, 728, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6058", opacity=35, stroke=NONE)

# floor shadow under the whole apparatus
d.shape("ellipse", "Floor shadow", x=270, y=648, width=480, height=44,
        fill="#000000", opacity=32, stroke=NONE)

# --- the pristine page ------------------------------------------------------------
d.shape("rectangle", "Page shadow", x=350, y=184, width=320, height=366,
        radius=3, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Page", x=340, y=175, width=320, height=373,
        radius=3, fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
# double rule framing the title
d.path("M365,196 L635,196", "Title rule top", fill=NONE, stroke=INK,
       strokeWidth=2.5, opacity=85)
d.path("M365,232 L635,232", "Title rule bottom", fill=NONE, stroke=INK,
       strokeWidth=2.5, opacity=85)
r = d.text("DOCUMENTATION", "Page title", x=500, y=222, size=15,
           font="Virelai Sans", color=INK, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "title tracking", ids=[r["id"]], tracking=60)
# ruthlessly justified body — every line the same length, forever
for k, ly in enumerate([252, 274, 296, 318, 340, 362]):
    d.shape("rectangle", f"Body line {k+1}", x=365, y=ly, width=270,
            height=8, radius=4, fill=INK, opacity=55, stroke=NONE)
# a centered subhead, then more of the same
d.shape("rectangle", "Subhead", x=430, y=392, width=140, height=9,
        radius=4, fill=INK, opacity=65, stroke=NONE)
for k, ly in enumerate([414, 436]):
    d.shape("rectangle", f"Body line b{k+1}", x=365, y=ly, width=270,
            height=8, radius=4, fill=INK, opacity=55, stroke=NONE)
# footnote block, squared away
d.path("M365,470 L445,470", "Footnote rule", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=70)
d.text("*", "Footnote mark", x=365, y=492, size=12,
       font="Virelai Sans", color=INK, justify="left")
d.shape("rectangle", "Footnote line", x=383, y=482, width=190, height=6,
        radius=3, fill=INK, opacity=45, stroke=NONE)
d.shape("rectangle", "Footnote line 2", x=383, y=496, width=140, height=6,
        radius=3, fill=INK, opacity=45, stroke=NONE)
# rot creeping up the page's bottom edge — the only unformatted element
d.shape("ellipse", "Page rot 1", x=560, y=505, width=60, height=26,
        fill=ROT, opacity=25, stroke=NONE)
d.shape("ellipse", "Page rot 2", x=390, y=512, width=45, height=18,
        fill=ROT, opacity=20, stroke=NONE)

# --- the foundation: brick beam, split, laced, leaning ------------------------------
# beam rows; the right end is already coming apart
BRICKS = [
    # (x, y, w, rot, label)
    (290, 545, 78, 0, "B1"), (372, 545, 78, 0, "B2"),
    (454, 545, 78, 0, "B3"), (536, 545, 78, 0, "B4"),
    (618, 545, 78, -3, "B5"),
    (300, 573, 78, 0, "B6"), (382, 573, 78, 0, "B7"),
    (464, 573, 78, 2, "B8"), (546, 573, 78, 5, "B9"),
    (628, 573, 78, 9, "B10"),
]
for bx, by, bw, brot, blab in BRICKS:
    if brot:
        d.path(rot_rect_path(bx + bw / 2, by + 13, bw, 26, brot),
               f"{blab} brick", fill=BRICK_GRAD, stroke=INK,
               strokeWidth=3)
    else:
        d.shape("rectangle", f"{blab} brick", x=bx, y=by, width=bw,
                height=26, radius=2, fill=BRICK_GRAD, stroke=INK,
                strokeWidth=3)
# mortar sheen on the intact left
d.shape("rectangle", "Beam sheen", x=292, y=548, width=240, height=8,
        fill="#C49A78", opacity=30, stroke=NONE)
# the crack: down through B4/B9 and out the bottom
d.path("M565,545 L552,562 L572,573 L548,590 L560,602", "Beam crack",
       fill=NONE, stroke="#140A08", strokeWidth=5, cap="round")
# sutures — the script stitching its own wound
for i, sy in enumerate([552, 566, 580, 594]):
    d.path(f"M{543 + (i % 2) * 6},{sy} L{585 - (i % 2) * 6},{sy + 4}",
           f"Stitch {i+1}", fill=NONE, stroke=THREAD, strokeWidth=4,
           cap="round")
    d.shape("ellipse", f"Stitch dot {i+1}a", x=540 + (i % 2) * 6,
            y=sy - 2, width=5, height=5, fill=THREAD, opacity=80,
            stroke=NONE)
    d.shape("ellipse", f"Stitch dot {i+1}b", x=583 - (i % 2) * 6,
            y=sy + 2, width=5, height=5, fill=THREAD, opacity=80,
            stroke=NONE)
# support posts: left one plumb, right one giving up
d.shape("rectangle", "Post left", x=385, y=601, width=26, height=52,
        fill=POST_GRAD, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Post left foot", x=377, y=648, width=42, height=10,
        radius=3, fill=POST_GRAD, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(637, 630, 26, 56, -14), "Post right",
       fill=POST_GRAD, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(625, 658, 42, 10, -14), "Post right foot",
       fill=POST_GRAD, stroke=INK, strokeWidth=3)
# rot blotches on the beam
d.shape("ellipse", "Rot blotch 1", x=630, y=585, width=55, height=24,
        fill=ROT, opacity=30, stroke=NONE)
d.shape("ellipse", "Rot blotch 2", x=540, y=548, width=42, height=18,
        fill=ROT, opacity=22, stroke=NONE)
# bricks already fallen / mid-fall on the right
d.path(rot_rect_path(668, 636, 62, 24, 24), "Fallen brick",
       fill=BRICK_GRAD, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(724, 602, 30, 20, 38), "Debris 1",
       fill=BRICK_GRAD, stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(716, 640, 20, 14, -20), "Debris 2",
       fill=BRICK_GRAD, stroke=INK, strokeWidth=2.5)
for i, (dx, dy) in enumerate([(708, 570), (716, 585)]):
    d.shape("ellipse", f"Fall mote {i+1}", x=dx, y=dy, width=5, height=5,
            fill="#C49A78", opacity=40, stroke=NONE)

# --- footnotes drifting in space, looking for a sentence -------------------------
# one escaping top-right with a dotted trail back to the page
d.path("M668,190 Q720,205 736,238", "Drift trail 1", fill=NONE,
       stroke=KEY, strokeWidth=2.5, opacity=40, dash=[3, 8], cap="round")
d.path(rot_rect_path(770, 252, 96, 32, -14), "Drift card 1",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5, opacity=92)
d.text("*", "Drift mark 1", x=734, y=262, size=12,
       font="Virelai Sans", color=INK, justify="center")
d.shape("rectangle", "Drift line 1", x=748, y=256, width=56, height=5,
        radius=2.5, fill=INK, opacity=50, stroke=NONE)
# one hovering mid-air left, searching — dashed loop of indecision
d.path("M262,310 Q300,290 332,312", "Drift trail 2", fill=NONE,
       stroke=KEY, strokeWidth=2.5, opacity=35, dash=[3, 8], cap="round")
d.path(rot_rect_path(240, 348, 96, 32, 9), "Drift card 2",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5, opacity=90)
d.text("*", "Drift mark 2", x=210, y=358, size=12,
       font="Virelai Sans", color=INK, justify="center")
d.shape("rectangle", "Drift line 2", x=222, y=352, width=56, height=5,
        radius=2.5, fill=INK, opacity=50, stroke=NONE)

# --- aphorism line + name + role ------------------------------------------------
r = d.text("ROT IS IMMINENT —", "Key line 1", x=500, y=722,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("BUT EXTREMELY WELL-FORMATTED.", "Key line 2", x=500, y=756,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("PATCHY MX.CLI", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("PATCHY MENDS THE GAPS", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-039-patchy-mxcli-V1R00")
