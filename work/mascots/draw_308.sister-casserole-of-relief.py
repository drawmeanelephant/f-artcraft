#!/usr/bin/env python3
"""Sister Casserole of Relief — mascot portrait V1R00.
Kitchen steward holding an enamel casserole dish over the open memorial
supper ledger, handwritten recipe card pinned nearby. Warm, pressed,
faintly exhausted. 1000x1000. Gradients + translucency, never flat."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sister Casserole of Relief — Mascot Portrait", 1000, 1000)

INK = "#3B2620"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2B1B14"}, {"offset": 1, "color": "#120A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E5C2"}, {"offset": 0.7, "color": "#DCBB8C"},
    {"offset": 1, "color": "#A67C50"}]}}
DRESS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54405A"}, {"offset": 0.7, "color": "#3A2A40"},
    {"offset": 1, "color": "#241A28"}]}}
KERCHIEF_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8EFDC"}, {"offset": 1, "color": "#DCC6A0"}]}}
APRON_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4E8CE"}, {"offset": 1, "color": "#D8C29C"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4D8BC"}, {"offset": 1, "color": "#DCAF8E"}]}}
ENAMEL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CC5A3C"}, {"offset": 0.65, "color": "#9A3524"},
    {"offset": 1, "color": "#6E2418"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F7F0DC"}, {"offset": 1, "color": "#DFD2B0"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5E36"}, {"offset": 1, "color": "#5C3C20"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8EFDC", strokeWidth=3, opacity=50)
# warm patina flecks, kept inside the ring
for i, (x, y, w) in enumerate([(208,222,7),(788,214,6),(238,716,7),(752,706,7),(168,448,6),
                               (836,452,6),(348,148,6),(648,142,7),(292,798,6),(708,802,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6A42", opacity=38, stroke=NONE)

# --- recipe card, pinned upper right -------------------------------------------
import math
def rot(cx, cy, pts, deg):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    return [(cx + px*c - py*s, cy + px*s + py*c) for px, py in pts]

card_pts = rot(712, 268, [(-72,-58),(72,-58),(72,58),(-72,58)], -7)
d.path("M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in card_pts) + " Z",
       "Card shadow", fill="#6E4E2E", opacity=30, stroke=NONE)
card_pts = rot(706, 260, [(-72,-58),(72,-58),(72,58),(-72,58)], -7)
d.path("M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in card_pts) + " Z",
       "Recipe card", fill=PAPER_GRAD, stroke=INK, strokeWidth=4, join="round")
# handwritten rows: wavy unauthenticated script
for j, (yy, w0) in enumerate([(232,110),(254,118),(276,96)]):
    x0 = 706 - w0/2
    d.path(f"M{x0:.0f},{yy} C{x0+22:.0f},{yy-7} {x0+36:.0f},{yy+7} {x0+58:.0f},{yy} "
           f"C{x0+76:.0f},{yy-6} {x0+92:.0f},{yy+5} {x0+w0:.0f},{yy-2}",
           f"Card line {j+1}", fill=NONE, stroke="#7A6248",
           strokeWidth=3.2, cap="round", opacity=80)
d.path("M664,296 C680,291 700,297 716,293", "Card line short",
       fill=NONE, stroke="#7A6248", strokeWidth=3, cap="round", opacity=70)
# flour smudge + a crossed-out scribble (the correction never entered)
d.shape("ellipse", "Flour smudge", x=734, y=284, width=30, height=14,
        fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M646,232 L662,246 M662,232 L646,246", "Crossed line",
       fill=NONE, stroke="#9A5A3C", strokeWidth=2.5, cap="round", opacity=70)
# the pin
d.shape("ellipse", "Pin shadow", x=700, y=198, width=20, height=10,
        fill="#6E4E2E", opacity=35, stroke=NONE)
d.shape("ellipse", "Pin", x=697, y=186, width=22, height=22,
        fill="#B43A28", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pin glint", x=702, y=190, width=7, height=7,
        fill="#FFFFFF", opacity=80, stroke=NONE)

# --- the sister -------------------------------------------------------------------
# ground shadow
d.shape("ellipse", "Figure shadow", x=300, y=752, width=340, height=30,
        fill="#7A5632", opacity=40, stroke=NONE)
# dress: bell of dark plum-brown cloth
d.path("M340,752 C336,640 348,540 384,470 C408,424 452,404 480,414 "
       "C532,430 566,502 572,582 C576,652 574,706 570,752 Z",
       "Dress", fill=DRESS_GRAD, stroke=INK, strokeWidth=7, join="round")
# dress folds
d.path("M378,724 C374,620 386,530 414,472", "Dress fold L",
       fill=NONE, stroke="#1C141F", strokeWidth=8, opacity=45, cap="round")
d.path("M548,704 C552,624 542,542 516,484", "Dress fold R",
       fill=NONE, stroke="#1C141F", strokeWidth=7, opacity=40, cap="round")
# kerchief: drape over the head, knotted at her right
d.path("M356,432 C348,342 404,270 470,274 C542,278 582,346 576,432 "
       "C592,472 586,512 562,532 C542,482 402,482 386,534 C362,512 348,472 356,432 Z",
       "Kerchief", fill=KERCHIEF_GRAD, stroke=INK, strokeWidth=6, join="round")
# kerchief knot + tails at her right shoulder
d.shape("ellipse", "Knot", x=566, y=500, width=26, height=24,
        fill=KERCHIEF_GRAD, stroke=INK, strokeWidth=4)
d.path("M576,516 L596,556 L576,548 Z", "Knot tail 1",
       fill=KERCHIEF_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.path("M566,520 L578,562 L560,550 Z", "Knot tail 2",
       fill=KERCHIEF_GRAD, stroke=INK, strokeWidth=3.5, join="round")
# face
d.shape("ellipse", "Face", x=406, y=342, width=130, height=134,
        fill=FACE_GRAD, stroke=INK, strokeWidth=5)
# kerchief band across the forehead
d.path("M406,384 C422,342 520,342 534,384 C528,352 500,332 470,332 "
       "C440,332 412,352 406,384 Z",
       "Kerchief band", fill=KERCHIEF_GRAD, stroke=INK, strokeWidth=4)
# faintly exhausted eyes: soft lowered lids, gently shut
d.path("M426,414 C434,422 448,422 456,414", "Eye L",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M494,414 C502,422 516,422 524,414", "Eye R",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M428,432 C436,436 446,436 454,432", "Undereye L",
       fill=NONE, stroke="#B0836A", strokeWidth=3, cap="round", opacity=70)
d.path("M496,432 C504,436 514,436 522,432", "Undereye R",
       fill=NONE, stroke="#B0836A", strokeWidth=3, cap="round", opacity=70)
# brow crease, pressed
d.path("M436,398 C446,394 458,394 466,398", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=60)
d.path("M484,398 C494,394 506,394 514,398", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=60)
# the warm small smile that keeps the room intact
d.path("M452,452 C462,460 484,460 494,452", "Smile",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# floury cheeks
d.shape("ellipse", "Cheek L", x=418, y=434, width=26, height=11, fill="#D9A08C", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=500, y=434, width=26, height=11, fill="#D9A08C", opacity=40, stroke=NONE)
# one flour fingerprint on the jaw
d.shape("ellipse", "Flour mark", x=500, y=458, width=16, height=7,
        fill="#F8EFDC", opacity=55, stroke=NONE)

# --- apron over the dress --------------------------------------------------------
d.path("M404,752 C400,656 404,584 414,548 L536,548 C546,584 550,656 546,752 Z",
       "Apron skirt", fill=APRON_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M432,552 L432,506 C432,494 442,488 452,488 L498,488 C508,488 518,494 518,506 L518,552 Z",
       "Apron bib", fill=APRON_GRAD, stroke=INK, strokeWidth=4.5, join="round")
# apron ties + pocket
d.path("M414,560 C390,568 372,584 364,604", "Tie L",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=70)
d.path("M536,560 C560,568 578,584 586,604", "Tie R",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=70)
d.path("M446,646 L504,646 L500,700 L450,700 Z", "Apron pocket",
       fill="#E4D2AE", stroke=INK, strokeWidth=4, join="round")
d.path("M446,668 L504,668", "Pocket seam", fill=NONE, stroke=INK, strokeWidth=3, opacity=70)
# flour dust on the apron
d.shape("ellipse", "Flour 1", x=430, y=590, width=34, height=16, fill="#FFFFFF", opacity=35, stroke=NONE)
d.shape("ellipse", "Flour 2", x=496, y=716, width=26, height=12, fill="#FFFFFF", opacity=30, stroke=NONE)
d.shape("ellipse", "Flour 3", x=466, y=556, width=18, height=9, fill="#FFFFFF", opacity=40, stroke=NONE)

# --- the casserole dish, held over the ledger -------------------------------------
# sleeves reaching in
d.path("M384,560 C372,576 368,594 374,612 L400,606 C396,592 398,576 406,564 Z",
       "Sleeve L", fill=DRESS_GRAD, stroke=INK, strokeWidth=4)
d.path("M566,560 C578,576 582,594 576,612 L550,606 C554,592 552,576 544,564 Z",
       "Sleeve R", fill=DRESS_GRAD, stroke=INK, strokeWidth=4)
# dish body: squat enamel oval
d.path("M376,606 C376,578 420,562 470,562 C520,562 564,578 564,606 "
       "C564,640 522,662 470,662 C418,662 376,640 376,606 Z",
       "Casserole", fill=ENAMEL_GRAD, stroke=INK, strokeWidth=6, join="round")
# lid: shallow dome + rim + knob
d.path("M386,588 C398,552 542,552 554,588 C520,574 420,574 386,588 Z",
       "Lid", fill=ENAMEL_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Knob", x=456, y=540, width=28, height=20,
        fill=KERCHIEF_GRAD, stroke=INK, strokeWidth=4)
d.path("M392,592 C430,580 510,580 548,592", "Lid rim",
       fill=NONE, stroke="#F0C9A8", strokeWidth=4, cap="round", opacity=60)
# handles + her mitten hands on them
d.path("M376,600 C360,596 350,604 354,616 C358,626 370,626 378,618",
       "Handle L", fill=ENAMEL_GRAD, stroke=INK, strokeWidth=4)
d.path("M564,600 C580,596 590,604 586,616 C582,626 570,626 562,618",
       "Handle R", fill=ENAMEL_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=352, y=596, width=32, height=36,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=556, y=596, width=32, height=36,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
# enamel shine + heat shadow under
d.shape("ellipse", "Dish shine", x=404, y=594, width=56, height=22,
        fill="#FFFFFF", opacity=25, stroke=NONE)
d.shape("ellipse", "Dish glow", x=404, y=650, width=134, height=18,
        fill="#F4A45C", opacity=30, stroke=NONE)
# steam venting off the lid edges, curling outward past her shoulders
d.path("M408,548 C392,522 378,502 384,474 C389,452 404,440 418,434",
       "Steam L", fill=NONE, stroke="#FFFFFF", strokeWidth=9,
       cap="round", opacity=42)
d.path("M532,548 C548,522 562,502 556,474 C551,452 536,440 522,434",
       "Steam R", fill=NONE, stroke="#FFFFFF", strokeWidth=9,
       cap="round", opacity=42)
d.path("M470,534 C462,512 480,496 471,474 C465,460 473,448 479,440",
       "Steam C", fill=NONE, stroke="#FFFFFF", strokeWidth=7,
       cap="round", opacity=30)

# --- the memorial supper ledger, open on its stand below the dish -------------------
# stand: plank + two legs
d.shape("rectangle", "Stand plank", x=356, y=762, width=228, height=16,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4, radius=4)
d.shape("rectangle", "Stand leg L", x=384, y=776, width=14, height=34,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4, radius=3)
d.shape("rectangle", "Stand leg R", x=542, y=776, width=14, height=34,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4, radius=3)
# open book: two cream pages, spine at 470
d.path("M368,714 L464,698 L464,756 L368,772 Z", "Page L",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M572,714 L476,698 L476,756 L572,772 Z", "Page R",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M464,698 L476,698 L476,756 L464,756 Z", "Spine",
       fill="#DCC6A0", stroke=INK, strokeWidth=3)
# names column + credit marks: the roll kept warm
for j, yy in enumerate([716, 730, 744, 758]):
    d.path(f"M382,{yy} L418,{yy-4}", f"Name L{j+1}", fill=NONE,
           stroke="#8A7454", strokeWidth=3, cap="round", opacity=85)
    d.path(f"M488,{yy-4} L524,{yy-8}", f"Name R{j+1}", fill=NONE,
           stroke="#8A7454", strokeWidth=3, cap="round", opacity=85)
# gratitude checkmarks accruing to the absent
for j, (x, y) in enumerate([(434,712),(434,726),(536,708),(536,722),(536,736)]):
    d.path(f"M{x},{y} L{x+4},{y+5} L{x+11},{y-4}", f"Credit {j+1}",
           fill=NONE, stroke="#9A6A34", strokeWidth=3, cap="round")
# one faint strike-through the record refuses to finish
d.path("M382,730 L418,726", "Soft correction", fill=NONE, stroke="#B45A40",
       strokeWidth=2.5, cap="round", opacity=45)
# the pencil, laid down mid-entry
d.path("M500,742 L546,736 L550,742 L504,748 Z", "Pencil",
       fill="#D9A03C", stroke=INK, strokeWidth=2.5, join="round")
d.path("M546,736 L556,737 L550,742 Z", "Pencil tip",
       fill="#3B2620", stroke=NONE)

# --- name + role -------------------------------------------------------------------
d.text("SISTER CASSEROLE OF RELIEF", "Name", x=500, y=930, size=47,
       font="Virelai Sans", color="#F4E5C2", justify="center")
r = d.text("AUXILIARY KITCHEN CONTINUITY STEWARD", "Role", x=500, y=968,
           size=22, font="Virelai Sans", color="#C9A87A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("308.sister-casserole-of-relief-V1R00")
