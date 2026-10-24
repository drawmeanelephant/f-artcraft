#!/usr/bin/env python3
"""LX-2 Waiver Apron — mascot portrait V1R00.
The mascot is the apron itself: neck loop, waist ties held out like arms,
patch pockets stuffed with expired waiver slips — standing by the COMA
Exception Desk placard. It doesn't grant waivers; it remembers them.
1000x1000 plate format. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("LX-2 Waiver Apron — Mascot Portrait", 1000, 1000)

INK = "#3E2C1E"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#221608"}, {"offset": 1, "color": "#0A0502"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E6CC"}, {"offset": 0.65, "color": "#D4BC94"},
    {"offset": 1, "color": "#9E8258"}]}}
APRON_GRAD = {"gradient": {"kind": "linear", "start": [0, 420], "end": [0, 800], "stops": [
    {"offset": 0, "color": "#D8B888"}, {"offset": 0.55, "color": "#B8935E"},
    {"offset": 1, "color": "#8E6E42"}]}}
TIE_GRAD = {"gradient": {"kind": "linear", "start": [0, 590], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#C9A876"}, {"offset": 1, "color": "#9E7C4E"}]}}
SLIP_GRAD = {"gradient": {"kind": "linear", "start": [0, 590], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#F6EFDC"}, {"offset": 1, "color": "#D8CCA8"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#D8BC90", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3626", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6ECD6", strokeWidth=3, opacity=38)
d.shape("ellipse", "Patina 1", x=190, y=180, width=220, height=120,
        fill="#B0966A", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=620, width=230, height=130,
        fill="#B0966A", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(180, 350, 6), (830, 310, 7), (165, 540, 7), (840, 560, 6),
                               (265, 770, 6), (745, 755, 7), (315, 125, 5), (670, 118, 6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8E7248", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(68, 135, 4), (920, 105, 5), (50, 545, 4), (946, 605, 4),
                               (128, 892, 4), (872, 902, 5), (505, 30, 4), (255, 42, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D9BC", opacity=26, stroke=NONE)

# --- the COMA Exception Desk (signpost + counter, right side) --------------------
d.shape("ellipse", "Desk shadow", x=620, y=782, width=150, height=20,
        fill="#3A2A1A", opacity=20, stroke=NONE)
d.shape("rectangle", "Desk post", x=707, y=552, width=16, height=240,
        fill="#5E4630", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Counter", x=648, y=700, width=104, height=86, radius=10,
        fill="#6E5238", stroke=INK, strokeWidth=4)
d.path("M660,730 L740,730 M660,752 L740,752", "Counter panels", fill=NONE,
       stroke="#4E3A26", strokeWidth=3, opacity=70)
# placard card on the post
d.shape("rectangle", "Placard", x=620, y=496, width=190, height=62, radius=8,
        fill="#EEDFC0", stroke=INK, strokeWidth=4)
d.path("M634,527 L660,527 M648,515 L634,527 L648,539", "Placard arrow",
       fill=NONE, stroke="#8A3E2E", strokeWidth=4, cap="round")
d.text("EXCEPTION DESK", "Placard text", x=722, y=535, size=13,
       font="Source Sans 3", color="#4A3626", justify="center")

# --- ground shadow for the apron ---------------------------------------------------
d.shape("ellipse", "Shadow", x=350, y=782, width=270, height=26,
        fill="#3A2A1A", opacity=22, stroke=NONE)

# --- waist ties, held out like tired arms ---------------------------------------------
d.path("M432,600 C362,585 295,596 248,638 L258,660 C305,624 366,618 432,634 Z",
       "Tie L", fill=TIE_GRAD, stroke=INK, strokeWidth=4)
d.path("M528,600 C572,588 612,592 646,612 L638,634 C608,616 566,614 528,630 Z",
       "Tie R", fill=TIE_GRAD, stroke=INK, strokeWidth=4)

# --- the apron itself -----------------------------------------------------------------
# skirt: flares from the waist to a broad hem
d.path("M425,580 L535,580 C560,650 575,720 582,788 L378,788 "
       "C385,720 400,650 425,580 Z",
       "Skirt", fill=APRON_GRAD, stroke=INK, strokeWidth=6)
# skirt shading: side shadow + centre crease
d.path("M395,760 C400,700 410,640 425,596 L445,596 C432,650 425,710 422,760 Z",
       "Skirt shade L", fill="#7A5C36", opacity=30, stroke=NONE)
d.path("M470,600 C466,660 466,720 470,768", "Skirt crease", fill=NONE,
       stroke="#7A5C36", strokeWidth=4, opacity=50, cap="round")
# bib: halter top rising from the waist
d.path("M437,430 L523,430 C532,478 534,532 530,580 L430,580 "
       "C426,532 428,478 437,430 Z",
       "Bib", fill=APRON_GRAD, stroke=INK, strokeWidth=6)
# neck loop strap
d.path("M442,436 C442,360 518,360 518,436", "Neck loop", fill=NONE,
       stroke="#8A6A44", strokeWidth=13, cap="round")
# bib shading + highlight
d.shape("ellipse", "Bib light", x=446, y=444, width=68, height=40,
        fill="#FFFFFF", opacity=16, stroke=NONE)
d.path("M432,570 L528,570 L528,580 L432,580 Z", "Waist seam", fill="#7A5C36",
       opacity=40, stroke=NONE)
# brass rivets
for i, (x, y) in enumerate([(440, 434), (520, 434), (428, 588), (532, 588)]):
    d.shape("ellipse", f"Rivet {i+1}", x=x, y=y, width=11, height=11,
            fill="#D9A441", stroke=INK, strokeWidth=2)

# --- pockets stuffed with expired waivers ----------------------------------------------
def slip(cx, cy, deg, label):
    d.path(rot_rect_path(cx, cy, 44, 60, deg), label, fill=SLIP_GRAD,
           stroke=INK, strokeWidth=3)
    # cancelled stamp: red ring + slash
    d.shape("ellipse", f"{label} stamp", x=cx - 10, y=cy - 4, width=20, height=20,
            fill=NONE, stroke="#B03A2E", strokeWidth=3, opacity=80)
    d.path(f"M{cx - 8},{cy + 12} L{cx + 8},{cy - 2}", f"{label} slash",
           fill=NONE, stroke="#B03A2E", strokeWidth=3, opacity=80, cap="round")

# slips poke out of the pocket tops (pockets drawn over their lower halves)
slip(414, 622, -14, "Slip L1")
slip(440, 612, 4, "Slip L2")
slip(466, 624, -4, "Slip L3")
slip(524, 616, 12, "Slip R1")
slip(550, 626, 22, "Slip R2")
# patch pockets
d.path("M398,648 L482,648 L482,726 C482,736 476,742 466,742 L414,742 "
       "C404,742 398,736 398,726 Z",
       "Pocket L", fill=APRON_GRAD, stroke=INK, strokeWidth=4)
d.path("M500,648 L584,648 L584,726 C584,736 578,742 568,742 L516,742 "
       "C506,742 500,736 500,726 Z",
       "Pocket R", fill=APRON_GRAD, stroke=INK, strokeWidth=4)
d.path("M398,660 L482,660 M500,660 L584,660", "Pocket hems", fill=NONE,
       stroke="#7A5C36", strokeWidth=3, opacity=60)

# --- face on the bib: wry, unimpressed ------------------------------------------------
d.shape("ellipse", "Eye L", x=448, y=478, width=32, height=40,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=502, y=478, width=32, height=40,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=459, y=494, width=14, height=18,
        fill="#241C12", stroke=NONE)
d.shape("ellipse", "Pupil R", x=513, y=494, width=14, height=18,
        fill="#241C12", stroke=NONE)
d.shape("ellipse", "Glint L", x=462, y=498, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=516, y=498, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M446,474 C456,464 472,462 482,470", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M500,470 C510,462 526,464 536,474", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M466,548 C478,556 492,556 504,550", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")

# --- name + role ------------------------------------------------------------------
def text_id(text):
    # point-type nodes are named after their content, not the layer label
    doc = d.call("inspect_document", {"kind": "Type"}, "inspect type") or {}
    for nd in doc.get("nodes", []):
        if nd.get("name") == text:
            return nd["id"]
    return None

FALLBACK = set("0123456789Λ/™")
def digit_font(tid, text):
    b = 0
    for ch in text:
        n = len(ch.encode("utf-8"))
        if ch in FALLBACK:
            d.cmd("text.setStyle", f"fallback {ch}@{b}",
                  id=tid, font="Source Sans 3", start=b, end=b + n)
        b += n

NAME = "LX-2 WAIVER APRON"
d.text(NAME, "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#F4E9D2", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "REMEMBERS EVERY EXPIRED WAIVER"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#C9AE86", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("081.lx-2-waiver-apron-V1R00")
