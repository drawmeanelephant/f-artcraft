#!/usr/bin/env python3
"""Comfort Ledgerling — mascot portrait V1R00.
A small visored ledgerling stands among the neat columns of its own open
ledger, dip pen in hand, writing a single warm smile into the totals row —
the only entry in the book that was never a number. Every other cell keeps
its tidy grey figures; the morale is entered by hand. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Comfort Ledgerling — Mascot Portrait", 1000, 1000)

INK = "#30241A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1C10"}, {"offset": 1, "color": "#0B0C06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A0937A"}, {"offset": 0.7, "color": "#6C6148"},
    {"offset": 1, "color": "#38321F"}]}}
COVER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4630"}, {"offset": 1, "color": "#2C2618"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EBD4"}, {"offset": 1, "color": "#D6CBAE"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#98A47E"}, {"offset": 1, "color": "#5A6448"}]}}
RULE = "#84805F"
ENTRY = "#938D72"
SMILE = "#8E3B30"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#AC9E80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DAC0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E5238", opacity=50, stroke=NONE)

# --- the ledger ----------------------------------------------------------------
d.shape("ellipse", "Ledger shadow", x=270, y=672, width=460, height=30,
        fill="#0E0C06", opacity=42, stroke=NONE)
# cover beneath the pages
d.path("M500,388 C430,378 336,380 230,410 L208,652 C322,620 432,616 500,632 "
       "C568,616 678,620 792,652 L770,410 C664,380 570,378 500,388 Z",
       "Cover", fill=COVER_GRAD, stroke=INK, strokeWidth=6)
# pages
d.path("M495,406 C428,396 350,398 262,424 L244,628 C342,600 434,596 495,612 Z",
       "Left page", fill=PAGE_GRAD, stroke=INK, strokeWidth=5)
d.path("M505,406 C572,396 650,398 738,424 L756,628 C658,600 566,596 505,612 Z",
       "Right page", fill=PAGE_GRAD, stroke=INK, strokeWidth=5)
d.path("M495,406 C497,474 497,544 495,612 L505,612 C503,544 503,474 505,406 Z",
       "Gutter", fill="#2A2118", stroke=NONE)

# --- the columns: ruled grids, entries in tidy grey ----------------------------
def column_grid(x0, x1, label):
    # header rule + column separators + row rules
    for i, cx in enumerate([x0 + (x1 - x0) * f for f in (0.36, 0.68)]):
        d.path(f"M{cx:.0f},436 L{cx - 14:.0f},596", f"{label} col {i+1}",
               fill=NONE, stroke=RULE, strokeWidth=2.5, opacity=70)
    for j in range(7):
        y = 446 + j * 24
        d.path(f"M{x0},{y} Q{(x0 + x1) / 2},{y - 6} {x1},{y}",
               f"{label} row {j+1}", fill=NONE, stroke=RULE,
               strokeWidth=2.5, opacity=60)

column_grid(280, 480, "Left grid")
column_grid(528, 726, "Right grid")

# entries — short tidy figures, row after row
for j in range(6):
    y = 466 + j * 24
    for i, (fx, ln) in enumerate([(0.10, 42), (0.44, 46), (0.74, 38)]):
        x0 = 280 + 200 * fx
        d.path(f"M{x0:.0f},{y} L{x0 + ln:.0f},{y}", f"L entry {j+1}.{i+1}",
               fill=NONE, stroke=ENTRY, strokeWidth=5, cap="round",
               opacity=70)
# right page entries — but the bottom row is kept clear for the comfort
for j in range(5):
    y = 466 + j * 24
    for i, (fx, ln) in enumerate([(0.08, 40), (0.42, 46), (0.72, 36)]):
        x0 = 528 + 198 * fx
        d.path(f"M{x0:.0f},{y} L{x0 + ln:.0f},{y}", f"R entry {j+1}.{i+1}",
               fill=NONE, stroke=ENTRY, strokeWidth=5, cap="round",
               opacity=70)
# two cells carry actual figures — Source Sans 3, since Virelai has no digits
d.text("847.20", "Figure 1", x=300, y=466, size=11,
       font="Source Sans 3", color="#7A7458")
d.text("1,063.44", "Figure 2", x=545, y=514, size=11,
       font="Source Sans 3", color="#7A7458")

# the totals row: a double rule, then the entry that was never a number
d.path("M534,592 C570,588 606,588 642,592 M534,600 C570,596 606,596 642,600",
       "Totals double rule", fill=NONE, stroke="#6E6A4E", strokeWidth=2,
       opacity=70)
d.shape("ellipse", "Comfort eye L", x=562, y=566, width=5, height=5,
        fill=SMILE, stroke=NONE)
d.shape("ellipse", "Comfort eye R", x=577, y=566, width=5, height=5,
        fill=SMILE, stroke=NONE)
d.path("M556,574 C563,586 581,586 588,573", "The smile", fill=NONE,
       stroke=SMILE, strokeWidth=4.5, cap="round")

# --- the ledgerling, at work among its columns ---------------------------------
d.shape("ellipse", "Ling shadow", x=618, y=596, width=96, height=14,
        fill="#8A8060", opacity=45, stroke=NONE)
# round little body, hunched forward over the pen
d.path("M622,600 C612,556 618,514 644,494 C668,478 698,486 706,516 "
       "C712,548 706,580 696,600 C672,610 640,610 622,600 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Body sheen", x=634, y=510, width=22, height=56,
        fill="#FFFFFF", opacity=10, stroke=NONE)
# head fused into the body — the ledgerling is mostly head
d.shape("ellipse", "Face", x=630, y=494, width=58, height=50,
        fill="#EDE3C8", stroke=INK, strokeWidth=4.5)
# the green eyeshade — the bookkeeper's mark
d.path("M628,506 C636,494 680,492 690,504 C684,514 636,516 628,506 Z",
       "Eyeshade", fill="#4E8A52", stroke=INK, strokeWidth=3.5,
       opacity=88)
d.shape("ellipse", "Eye", x=648, y=518, width=6, height=8,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye 2", x=668, y=517, width=6, height=8,
        fill=INK, stroke=NONE)
d.path("M650,532 C656,537 668,537 674,531", "Content mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# working arm reaching down to the totals row
d.path("M646,552 C630,560 612,568 596,574", "Arm", fill=NONE,
       stroke="#5A6448", strokeWidth=11, cap="round")
d.shape("ellipse", "Hand", x=584, y=566, width=18, height=16,
        fill="#EDE3C8", stroke=INK, strokeWidth=3.5)
# the dip pen, nib just off the smile
d.path("M604,556 L576,590", "Pen shaft", fill=NONE, stroke="#4A3A22",
       strokeWidth=5, cap="round")
d.path("M580,584 L573,594 L582,592 Z", "Pen nib", fill=INK, stroke=NONE)
# a spare pen tucked behind where an ear would be
d.path("M686,486 L700,470", "Spare pen", fill=NONE, stroke="#4A3A22",
       strokeWidth=4, cap="round")

# quiet motes over the book
for i, (x, y, w) in enumerate([(330,270,5),(690,250,4),(250,460,5),(790,440,4),
                               (400,160,4),(620,150,5),(300,730,4),(730,720,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4DCC2", opacity=35, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("COMFORT LEDGERLING", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EFE8D4", justify="center")
r = d.text("MORALE BOOKKEEPING ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4B896", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("281.comfort-ledgerling-V1R00")
