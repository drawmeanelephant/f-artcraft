#!/usr/bin/env python3
"""MA-LCGU Porter — mascot portrait V1R00.
A hunched little porter-clerk straining under a tall stack of archive boxes,
shelved stock looming behind under a sign reading RETAINED FOR CONTEXT; one
box tag dangles LCGU. 1000x1000 plate format.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("MA-LCGU Porter — Mascot Portrait", 1000, 1000)

INK = "#3B2F26"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#241A12"}, {"offset": 1, "color": "#0D0806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E5CC"}, {"offset": 0.65, "color": "#D6C5A0"},
    {"offset": 1, "color": "#A08A62"}]}}
SHELF_GRAD = {"gradient": {"kind": "linear", "start": [0, 168], "end": [0, 196], "stops": [
    {"offset": 0, "color": "#6B5638"}, {"offset": 1, "color": "#4A3826"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 420], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#A9BCC4"}, {"offset": 0.6, "color": "#7B93A0"},
    {"offset": 1, "color": "#556873"}]}}
BOX_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 90], "stops": [
    {"offset": 0, "color": "#D9BC8C"}, {"offset": 1, "color": "#B28F5E"}]}}
BOX_GRAD2 = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 80], "stops": [
    {"offset": 0, "color": "#CEAF7E"}, {"offset": 1, "color": "#A3804F"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#C8B58E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3B28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6EEDC", strokeWidth=3, opacity=38)
# aged-paper patina + flecks
d.shape("ellipse", "Patina 1", x=170, y=560, width=250, height=140,
        fill="#B09468", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=140, width=210, height=110,
        fill="#B09468", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(180, 350, 6), (830, 320, 7), (160, 540, 7), (845, 575, 6),
                               (260, 775, 6), (735, 768, 7), (310, 132, 5), (680, 125, 6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A744C", opacity=35, stroke=NONE)
# faint dust on the dark margin
for i, (x, y, w) in enumerate([(70, 140, 4), (925, 110, 5), (50, 570, 4), (950, 640, 4),
                               (130, 905, 4), (875, 915, 5), (540, 28, 4), (250, 42, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C8A8", opacity=28, stroke=NONE)

# --- archive shelf band across the upper plate --------------------------------
# stored boxes + binders silhouetted on the shelf
for i, (x, w, h) in enumerate([(272, 56, 48), (336, 40, 56), (384, 52, 40),
                               (640, 52, 56), (704, 42, 48), (728, 30, 34)]):
    assert on_disc(x, 168 - h) and on_disc(x + w, 168 - h), (x, w, h)
    d.shape("rectangle", f"Shelf stock {i+1}", x=x, y=168 - h, width=w, height=h,
            fill="#5A4630", opacity=55, stroke=NONE)
    d.path(f"M{x + 8},{168 - h + 10} L{x + w - 8},{168 - h + 10}",
           f"Stock label {i+1}", fill=NONE, stroke="#8A744C",
           strokeWidth=3, opacity=45)
d.shape("rectangle", "Shelf plank", x=210, y=168, width=580, height=18,
        radius=4, fill=SHELF_GRAD, stroke="#3A2C1E", strokeWidth=3)
# hanging sign: RETAINED FOR CONTEXT
d.path("M668,186 L668,208 M756,186 L756,208", "Sign strings", fill=NONE,
       stroke="#6B5638", strokeWidth=3)
d.shape("rectangle", "Sign plaque", x=640, y=208, width=192, height=44,
        radius=6, fill="#E8D9B4", stroke="#4A3B28", strokeWidth=3)
d.text("RETAINED FOR", "Sign line 1", x=736, y=227, size=14,
       font="Virelai Sans", color="#4A3B28", justify="center")
d.text("CONTEXT", "Sign line 2", x=736, y=244, size=14,
       font="Virelai Sans", color="#4A3B28", justify="center")

# --- ground shadow -------------------------------------------------------------
d.shape("ellipse", "Shadow", x=350, y=756, width=300, height=30,
        fill="#4A3B28", opacity=24, stroke=NONE)

# --- feet ----------------------------------------------------------------------
d.shape("ellipse", "Foot L", x=412, y=762, width=76, height=36,
        fill="#4A5C66", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=512, y=762, width=76, height=36,
        fill="#4A5C66", stroke=INK, strokeWidth=5)

# --- porter body: hunched, straining --------------------------------------------
d.path("M360,756 C352,640 366,540 408,478 C438,436 562,436 592,478 "
       "C634,540 648,640 640,756 C606,776 556,784 500,784 "
       "C444,784 394,776 360,756 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# slump shading at the shoulders + belly crease
d.path("M404,478 C440,500 560,500 596,478 C560,516 440,516 404,478 Z",
       "Shoulder shade", fill="#4E6068", opacity=35, stroke=NONE)
d.shape("ellipse", "Dome light", x=425, y=455, width=150, height=58,
        fill="#FFFFFF", opacity=16, stroke=NONE)
d.path("M392,700 C430,724 570,724 608,700 C580,738 420,738 392,700 Z",
       "Hem shade", fill="#3E4E58", opacity=30, stroke=NONE)

# face: effort — squeezed-shut eyes, flat gritted mouth
d.path("M438,542 C452,526 474,526 486,540", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M514,540 C526,526 548,526 562,542", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M470,592 L530,592", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
# one bead of effort rolling off the temple
d.path("M628,506 C636,518 638,528 630,534 C622,528 622,516 628,506 Z",
       "Sweat drop", fill="#CFE4EC", stroke=INK, strokeWidth=3)

# --- arms raised, steadying the stack -------------------------------------------
d.path("M392,560 C370,520 366,470 384,430 L414,440 C400,474 402,512 416,548 Z",
       "Arm L", fill="#8AA2AE", stroke=INK, strokeWidth=5)
d.path("M608,560 C630,520 634,470 616,430 L586,440 C600,474 598,512 584,548 Z",
       "Arm R", fill="#8AA2AE", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Hand L", x=372, y=408, width=44, height=34,
        fill="#9FB4BE", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Hand R", x=584, y=408, width=44, height=34,
        fill="#9FB4BE", stroke=INK, strokeWidth=5)

# --- the box stack on his head ---------------------------------------------------
# bottom box sits on the dome
d.path(rot_rect_path(500, 388, 250, 84, -2), "Box bottom", fill=BOX_GRAD,
       stroke=INK, strokeWidth=5)
d.path(rot_rect_path(500, 388, 250, 14, -2), "Box bottom tape", fill="#8A6A44",
       opacity=70, stroke=NONE)
d.path("M436,414 L470,412 L470,420 L436,422 Z", "Bottom label", fill="#EFE4CC",
       stroke=INK, strokeWidth=2)
# middle box, leaning right
d.path(rot_rect_path(512, 316, 196, 72, 4), "Box middle", fill=BOX_GRAD2,
       stroke=INK, strokeWidth=5)
d.path(rot_rect_path(512, 316, 196, 12, 4), "Box middle tape", fill="#7E6240",
       opacity=70, stroke=NONE)
# top box, leaning left
d.path(rot_rect_path(488, 252, 150, 58, -6), "Box top", fill=BOX_GRAD,
       stroke=INK, strokeWidth=5)
d.path(rot_rect_path(488, 252, 150, 10, -6), "Box top tape", fill="#8A6A44",
       opacity=70, stroke=NONE)
# scuffs on the stack
d.path("M540,366 L560,362", "Scuff 1", fill=NONE, stroke="#7E6240",
       strokeWidth=3, opacity=60, cap="round")
d.path("M560,304 L574,298", "Scuff 2", fill=NONE, stroke="#6E5238",
       strokeWidth=3, opacity=60, cap="round")
# dangling tag off the bottom box: LCGU
d.path("M612,414 C622,428 626,442 624,456", "Tag string", fill=NONE,
       stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(624, 474, 52, 30, 8), "Tag", fill="#EFE4CC",
       stroke=INK, strokeWidth=2.5)
d.text("LCGU", "Tag text", x=622, y=483, size=14, font="Virelai Sans",
       color="#4A3B28", justify="center")

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

NAME = "MA-LCGU PORTER"
d.text(NAME, "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#EADFBE", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "MASTER OF DIGNIFIED NON-REMOVAL"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#A8906A", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("082.ma-lcgu-porter-V1R00")
