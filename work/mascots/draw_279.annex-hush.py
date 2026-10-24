#!/usr/bin/env python3
"""Annex Hush — mascot portrait V1R00.
A cowled figure stands at the gutter of a great open volume, hand cupped,
whispering a liability clause into the binding itself. The back of the book
recedes in greying page edges; on the rear spread the difficult graphs are
filed — present, accurately drawn, and set in a grey the diligent must lean
in to read. Faint dampening rings hang over the book: the hush at work.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Annex Hush — Mascot Portrait", 1000, 1000)

INK = "#2E2136"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1D1428"}, {"offset": 1, "color": "#0B0712"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8C7E9A"}, {"offset": 0.7, "color": "#5E5270"},
    {"offset": 1, "color": "#332A42"}]}}
COVER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A5C"}, {"offset": 1, "color": "#2A1E38"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E7D2"}, {"offset": 1, "color": "#D2C6A8"}]}}
REAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DCD4BE"}, {"offset": 1, "color": "#B0A890"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A5A80"}, {"offset": 1, "color": "#3A3048"}]}}
RULE = "#9A9078"
GREY = "#9E9AA4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A90AC", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D2E4", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A4258", opacity=50, stroke=NONE)

# the hush: three dampening rings dying over the book, strongest at the binding
for i, (rx, ry, op) in enumerate([(300, 240, 22), (340, 275, 15), (380, 310, 9)]):
    d.path(f"M{500 - rx},{360} A{rx},{ry} 0 0 1 {500 + rx},{360}",
           f"Hush ring {i+1}", fill=NONE, stroke="#C8C0D8",
           strokeWidth=4, cap="round", opacity=op)

# --- the book: cover, rear page-block, open spreads -------------------------------
d.shape("ellipse", "Book shadow", x=290, y=688, width=420, height=28,
        fill="#120C1A", opacity=40, stroke=NONE)
# cover: shallow tent under both spreads
d.path("M500,352 C420,338 320,342 210,384 L184,672 C310,632 430,628 500,646 "
       "C570,628 690,632 816,672 L790,384 C680,342 580,338 500,352 Z",
       "Cover", fill=COVER_GRAD, stroke=INK, strokeWidth=6)
# spine crease running down the cover's back
d.path("M500,352 C497,450 497,550 500,646", "Spine crease", fill=NONE,
       stroke="#1E1428", strokeWidth=5, opacity=70)

# rear page block — the back of the book, edges greying layer by layer
for i in range(5):
    off = i * 8
    shade = ["#C9C0AA", "#B4AC98", "#9F9889", "#8B857A", "#77726C"][i]
    d.path(f"M{764 - off},{404 + off} C{672 - off},{368 + off} "
           f"{580 - off},{366 + off} 512,376 L512,{622 - off} "
           f"C{580 - off},{612 - off} {672 - off},{616 - off} "
           f"{786 - off},{650 - off} Z",
           f"Rear leaf {i+1}", fill=shade, opacity=92 - i * 9,
           stroke=NONE)

# left spread — the near page, warm and fully lit
d.path("M494,372 C420,358 336,362 240,398 L218,646 C330,610 436,608 494,624 Z",
       "Left page", fill=PAGE_GRAD, stroke=INK, strokeWidth=5)
# right spread — the rear page, already cooler at its far edge
d.path("M506,372 C580,358 664,362 760,398 L782,646 C670,610 564,608 506,624 Z",
       "Right page", fill=REAR_GRAD, stroke=INK, strokeWidth=5)
# the gutter — the dark channel the whisper enters
d.path("M494,372 C496,450 496,540 494,624 L506,624 C504,540 504,450 506,372 Z",
       "Gutter", fill="#241A30", stroke=NONE)
d.path("M500,382 L500,616", "Gutter line", fill=NONE, stroke="#120A1C",
       strokeWidth=3, cap="round")

# left page text — honest body copy, warm ink, full strength
for i, w in enumerate([160, 172, 152, 118]):
    y = 430 + i * 30
    d.path(f"M{280},{y} C{330},{y - 5} {400},{y - 5} {280 + w},{y}",
           f"Left line {i+1}", fill=NONE, stroke=RULE, strokeWidth=8,
           cap="round", opacity=80)
for i, w in enumerate([150, 140]):
    y = 566 + i * 26
    d.path(f"M{272},{y} C{322},{y - 4} {392},{y - 4} {272 + w},{y}",
           f"Left low {i+1}", fill=NONE, stroke=RULE, strokeWidth=7,
           cap="round", opacity=60)

# right page — the annex: the clause, then the greying graphs
# the clause: two slightly darker lines, present but hushed
for i, w in enumerate([150, 124]):
    y = 416 + i * 26
    d.path(f"M{548},{y} C{600},{y - 4} {660},{y - 4} {548 + w},{y}",
           f"Clause {i+1}", fill=NONE, stroke=GREY, strokeWidth=6,
           cap="round", opacity=70)
# the difficult graph, filed at the back in grey font:
# chart frame + sinking bars + one descending trend, all in muted grey
d.path("M560,486 L560,572 L724,578", "Chart frame", fill=NONE,
       stroke=GREY, strokeWidth=4, cap="round", opacity=55)
for i, (bx, bh) in enumerate([(576, 40), (606, 52), (636, 64), (666, 78)]):
    d.shape("rectangle", f"Grey bar {i+1}", x=bx, y=568 - bh, width=22,
            height=bh, fill=GREY, opacity=45 - i * 4, stroke=NONE)
d.path("M566,502 C614,520 666,548 714,564", "Churn line", fill=NONE,
       stroke="#8E8A96", strokeWidth=4, cap="round", opacity=60)
d.path("M706,556 L720,566 L704,568", "Trend arrow", fill=NONE,
       stroke="#8E8A96", strokeWidth=4, cap="round", opacity=60)
# caption under the chart — the greyest line on the page
d.path("M566,592 C614,588 666,588 706,592", "Grey caption", fill=NONE,
       stroke=GREY, strokeWidth=5, cap="round", opacity=38)

# --- Annex Hush: the whisperer at the gutter --------------------------------------
d.shape("ellipse", "Hush shadow", x=414, y=596, width=110, height=18,
        fill="#8A8068", opacity=45, stroke=NONE)
# robe: a quiet bell leaning into the gutter
d.path("M434,600 C424,548 428,496 450,468 L500,476 C514,510 516,556 508,602 "
       "C486,612 452,612 434,600 Z", "Robe", fill=ROBE_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M450,484 L442,588", "Robe fold", fill=NONE, stroke="#2A2038",
       strokeWidth=3, opacity=60)
d.shape("ellipse", "Robe sheen", x=450, y=496, width=22, height=70,
        fill="#FFFFFF", opacity=8, stroke=NONE)
# hood + face, bowed toward the binding
d.path("M440,470 C432,428 448,398 476,396 C504,396 518,422 512,460 "
       "C504,478 456,484 440,470 Z", "Hood", fill=ROBE_GRAD,
       stroke=INK, strokeWidth=5)
d.shape("ellipse", "Face", x=466, y=414, width=34, height=34,
        fill="#E4D6C0", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye, lowered", x=488, y=424, width=6, height=8,
        fill=INK, stroke=NONE)
# the shhh: a small hand below the mouth, one finger raised across the lips
d.shape("ellipse", "Shh hand", x=496, y=444, width=16, height=14,
        fill="#D8C8AE", stroke=INK, strokeWidth=3.5)
d.path("M504,432 L504,458", "Shh finger", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")

# the whisper — three attenuating curls sinking into the gutter
for i, (x0, w_, op) in enumerate([(518, 26, 60), (538, 20, 45), (554, 14, 30)]):
    d.path(f"M{x0},{442 + i * 10} C{x0 + w_},{438 + i * 10} "
           f"{x0 + w_},{452 + i * 10} {x0},{456 + i * 10}",
           f"Whisper {i+1}", fill=NONE, stroke="#C8C0D4",
           strokeWidth=3.5, cap="round", opacity=op)
# two faint clauses escaping upward — what little the front page ever hears
d.path("M462,388 C472,374 486,368 498,371", "Faint clause 1", fill=NONE,
       stroke="#B8B0C4", strokeWidth=3, cap="round", opacity=35)
d.path("M484,382 C494,372 506,369 516,372", "Faint clause 2", fill=NONE,
       stroke="#B8B0C4", strokeWidth=3, cap="round", opacity=25)

# dust motes hanging in the hush
for i, (x, y, w) in enumerate([(330,260,5),(690,250,4),(250,440,5),(780,430,4),
                               (380,160,4),(640,155,5),(300,720,4),(720,710,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#CCC4DC", opacity=35, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("ANNEX HUSH", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4E0EC", justify="center")
r = d.text("SUPPLEMENTAL DISCLOSURE ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B0AAC2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("279.annex-hush-V1R00")
