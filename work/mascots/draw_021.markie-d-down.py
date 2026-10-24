#!/usr/bin/env python3
"""Markie-D-Down — mascot portrait V1R00. Spec Cleric, Semantic Purity Domain.
A clerical mascot in dark vestments holding an ASCII-only clipboard (one line
already struck in red), red pen raised; zine fragments at his feet.
Lawful pedantic. "Best viewed fenced."
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Markie-D-Down — Mascot Portrait", 1000, 1000)

INK = "#2A2430"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26241F"}, {"offset": 1, "color": "#100E0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2EBD6"}, {"offset": 0.7, "color": "#D2C29E"},
    {"offset": 1, "color": "#9A845C"}]}}
ROBE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A4350"}, {"offset": 0.72, "color": "#332E3C"},
    {"offset": 1, "color": "#211E28"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EFDA"}, {"offset": 1, "color": "#D8CBA4"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E2C2"}, {"offset": 1, "color": "#D4B98E"}]}}
RED = "#B03830"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E6A4A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4EEDA", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(205,228,8),(788,224,7),(172,516,9),(826,538,8),
                               (250,768,7),(752,750,9),(144,398,6),(854,392,7),
                               (392,116,7),(608,110,8),(334,818,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#96805C", opacity=42, stroke=NONE)

# "best viewed fenced": faint crop corners around the figure
for i, (cx, cy, sx, sy) in enumerate([(350, 268, 1, 1), (662, 268, -1, 1),
                                      (350, 762, 1, -1), (662, 762, -1, -1)]):
    d.path(f"M{cx},{cy + 26 * sy} L{cx},{cy} L{cx + 26 * sx},{cy}",
           f"Fence corner {i+1}", fill=NONE, stroke="#8A744E",
           strokeWidth=4, opacity=45, cap="round")

# floor line
d.path("M250,752 C390,738 630,738 770,748", "Floor line",
       fill=NONE, stroke="#8A6F4C", strokeWidth=3, opacity=50, cap="round")

# --- zine fragments on the floor --------------------------------------------------
frags = [
    ("M228,700 L296,692 L302,730 L236,740 Z", 244, 704, 1),
    ("M676,708 L742,700 L748,736 L684,742 Z", 690, 712, 1),
    ("M610,742 L664,736 L668,762 L616,768 Z", 622, 746, 1),
]
for i, (q, lx, ly, _) in enumerate(frags):
    d.path(q, f"Zine frag {i+1}", fill=PAPER_GRAD, stroke=INK,
           strokeWidth=3.5, join="round")
    # masthead bar + two print lines, fading scraps of protest
    d.path(f"M{lx},{ly + 6} L{lx + 42},{ly + 3}", f"Frag{i} headline",
           fill=NONE, stroke=INK, strokeWidth=5, opacity=80)
    d.path(f"M{lx},{ly + 16} L{lx + 48},{ly + 13} M{lx},{ly + 25} L{lx + 36},{ly + 22}",
           f"Frag{i} lines", fill=NONE, stroke="#7A6C50",
           strokeWidth=2.5, opacity=75)
# one torn corner fluttering free
d.path("M560,700 L586,692 L590,710 L566,714 Z", "Torn bit",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3, join="round", opacity=90)

# --- Markie: the spec cleric -----------------------------------------------------
d.shape("ellipse", "Figure shadow", x=368, y=744, width=290, height=26,
        fill="#6E5240", opacity=38, stroke=NONE)
# vestments: straighter clerical cut
d.path("M392,748 C386,650 390,560 412,496 C430,444 464,420 506,422 "
       "C552,426 584,468 592,540 C600,626 600,694 598,748 Z",
       "Vestments", fill=ROBE_GRAD, stroke=INK, strokeWidth=7, join="round")
# robe folds
d.path("M448,570 C446,628 446,686 448,734 M548,566 C554,626 556,684 554,734",
       "Robe folds", fill=NONE, stroke="#1C1922", strokeWidth=4,
       opacity=45, cap="round")
# stole: two bands down the front, ends marked with a hash each
d.path("M462,452 L486,452 L488,700 L464,700 Z", "Stole L",
       fill="#D8CBA4", opacity=88, stroke=INK, strokeWidth=3.5, join="round")
d.path("M512,452 L536,452 L534,700 L510,700 Z", "Stole R",
       fill="#D8CBA4", opacity=88, stroke=INK, strokeWidth=3.5, join="round")
for i, (hx, hy) in enumerate([(476, 664), (524, 664)]):
    d.path(f"M{hx - 7},{hy - 5} L{hx - 7},{hy + 7} M{hx + 7},{hy - 5} L{hx + 7},{hy + 7} "
           f"M{hx - 11},{hy - 2} L{hx + 11},{hy - 2} M{hx - 11},{hy + 4} L{hx + 11},{hy + 4}",
           f"Hash {i+1}", fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")

# head + clerical skullcap
d.shape("ellipse", "Head", x=436, y=340, width=134, height=116,
        fill=FACE_GRAD, stroke=INK, strokeWidth=6)
d.path("M442,388 C444,352 470,330 503,330 C536,330 562,352 564,388 "
       "C540,372 466,372 442,388 Z", "Skullcap", fill="#3A3440",
       stroke=INK, strokeWidth=5, join="round")
# stern brows, half-lidded judgemental eyes
d.path("M456,414 L486,410 M520,410 L550,414", "Brows",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M460,428 L484,428 M522,428 L546,428", "Lids",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Eye L", x=466, y=428, width=12, height=10,
        fill="#33222A", stroke=NONE)
d.shape("ellipse", "Eye R", x=528, y=428, width=12, height=10,
        fill="#33222A", stroke=NONE)
# the flat, unimpressed mouth
d.path("M478,472 C492,468 514,468 528,472", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# clerical collar peeking above the stole
d.shape("rectangle", "Collar", x=486, y=452, width=34, height=22, radius=3,
        fill="#F2EEE2", stroke=INK, strokeWidth=3.5)

# --- left arm: the ASCII clipboard, held up for inspection -------------------------
d.path("M414,540 C384,556 370,584 372,610", "Sleeve L",
       fill=NONE, stroke="#332E3C", strokeWidth=28, cap="round")
d.shape("ellipse", "Hand L", x=362, y=598, width=30, height=26,
        fill="#E8CBA0", stroke=INK, strokeWidth=4)
# clipboard: board, clip, monospace-strict contents
d.shape("rectangle", "Clipboard", x=238, y=470, width=140, height=150,
        radius=8, fill="#8A6F4E", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Clip page", x=248, y=482, width=120, height=128,
        fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
d.shape("rectangle", "Clip", x=286, y=462, width=44, height=20, radius=6,
        fill="#6E7684", stroke=INK, strokeWidth=3.5)
# ASCII lines: a heading, two rules, one struck through in red
d.path("M260,504 L344,504", "CB heading", fill=NONE, stroke=INK, strokeWidth=6)
d.path("M260,524 L352,524 M260,540 L336,540 M260,556 L352,556",
       "CB lines", fill=NONE, stroke="#6A5E48", strokeWidth=3.5, opacity=85)
d.path("M258,549 L354,532", "Red strike", fill=NONE, stroke=RED,
       strokeWidth=4.5, cap="round")
d.path("M260,578 L320,578", "CB short line", fill=NONE, stroke="#6A5E48",
       strokeWidth=3.5, opacity=85)

# --- right arm: the red pen, raised mid-verdict ------------------------------------
d.path("M580,530 C612,510 630,482 632,452", "Sleeve R",
       fill=NONE, stroke="#332E3C", strokeWidth=28, cap="round")
d.shape("ellipse", "Hand R", x=616, y=430, width=30, height=26,
        fill="#E8CBA0", stroke=INK, strokeWidth=4)
# the pen: barrel, nib, cap band
d.path(rot_rect_path(648, 398, 14, 72, 24), "Pen barrel",
       fill=RED, stroke=INK, strokeWidth=3.5, join="round")
d.path("M664,362 L676,348 L672,368 Z", "Pen nib",
       fill="#E8CBA0", stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(636, 424, 16, 10, 24), "Pen band",
       fill="#6E7684", stroke=INK, strokeWidth=2.5, join="round")
# redaction flourish: two small red ticks off the nib
d.path("M684,340 L696,330 M690,356 L702,352", "Verdict ticks",
       fill=NONE, stroke=RED, strokeWidth=4, cap="round", opacity=85)

# --- name + role -------------------------------------------------------------------
d.text("MARKIE-D-DOWN", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E8D2", justify="center")
r = d.text("RICH TEXT DENIER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C0AE88", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("021.markie-d-down-V1R00")
