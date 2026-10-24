#!/usr/bin/env python3
"""Relief Watermark — mascot portrait V1R00.
A clerk mascot holding a document up into a shaft of light; on the sheet a
faint watermark insignia — ring and star — is barely visible, pressed once
at half pressure and never again. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Relief Watermark — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14161C"}, {"offset": 1, "color": "#08080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E6A58"}, {"offset": 0.7, "color": "#4C483C"},
    {"offset": 1, "color": "#2A2820"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46423A"}, {"offset": 1, "color": "#201C16"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8A488"}, {"offset": 0.7, "color": "#94816A"},
    {"offset": 1, "color": "#6E5E4C"}]}}
FUR_DARK = "#7A6A56"
SHEET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EFDC"}, {"offset": 1, "color": "#D6C9A8"}]}}
MARK = "#A89A76"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A8E6E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DCC2", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#56503E", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#14100C",
       strokeWidth=4, opacity=70)

# --- the light shaft, entering through the rim arc --------------------------------
d.shape("ellipse", "Lamp glow", x=190, y=150, width=180, height=110,
        fill="#F4ECC8", opacity=14, stroke=NONE)
d.path("M190,176 A420,420 0 0 1 292,97 L770,700 L500,700 Z", "Light shaft",
       fill="#F0E6C4", opacity=9, stroke=NONE)
d.path("M236,170 L300,124 L690,700 L570,700 Z", "Light shaft core",
       fill="#F8F0D4", opacity=8, stroke=NONE)
d.shape("ellipse", "Light pool", x=510, y=672, width=250, height=34,
        fill="#F0E6C4", opacity=10, stroke=NONE)
for i, (x, y, w) in enumerate([(300,220,6),(380,320,5),(470,390,7),(540,470,5),
                               (350,430,6),(610,520,5),(430,280,5)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4ECC8", opacity=45, stroke=NONE)

# --- the mascot, gazing up into the beam ------------------------------------------
d.shape("ellipse", "Mascot shadow", x=270, y=684, width=200, height=18,
        fill="#0E0A06", opacity=35, stroke=NONE)
d.shape("ellipse", "Body", x=288, y=478, width=176, height=210,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# clerk collar + tie
d.path("M350,486 L370,505 L390,486 L390,498 L370,517 L350,498 Z",
       "Collar", fill="#E8DCC8", stroke=INK, strokeWidth=3)
d.path("M366,512 L374,512 L372,548 L368,548 Z", "Tie", fill="#5A5A46",
       stroke=INK, strokeWidth=2.5)
# head, tipped up toward the sheet
d.shape("ellipse", "Head", x=310, y=352, width=136, height=132,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (322, 434):
    d.shape("ellipse", f"Ear {ex}", x=ex-11, y=348, width=26, height=24,
            fill="#94816A", stroke=INK, strokeWidth=3.5)
# face: quiet scrutiny, eyes angled up-right
d.shape("ellipse", "Eye L", x=346, y=420, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=394, y=420, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=348, y=422, width=3, height=3,
        fill="#F4ECC8", stroke=NONE)
d.shape("ellipse", "Glint R", x=396, y=422, width=3, height=3,
        fill="#F4ECC8", stroke=NONE)
d.path("M362,452 C370,457 380,457 388,452", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- arms raised, holding the sheet into the light ----------------------------------
d.path("M330,520 C380,470 440,420 500,390", "Arm left", fill=NONE,
       stroke="#94816A", strokeWidth=17, cap="round")
d.path("M440,505 C480,470 540,470 596,480", "Arm right", fill=NONE,
       stroke="#94816A", strokeWidth=17, cap="round")

# --- the document, tilted to catch the light ---------------------------------------
d.path(rot_rect_path(640, 380, 176, 216, -13), "Sheet shadow",
       fill="#141008", opacity=30, stroke=NONE)
d.path(rot_rect_path(634, 372, 176, 216, -13), "Document",
       fill=SHEET_GRAD, stroke=INK, strokeWidth=4)
# ruled lines, all but illegible
for i, (cx, cy, w) in enumerate([(618,318,104),(624,352,112),(630,386,100),
                                 (636,420,108),(640,448,64)]):
    d.path(rot_rect_path(cx, cy, w, 4, -13), f"Rule {i+1}", fill=NONE,
           stroke="#B4A884", strokeWidth=2.5, opacity=60)
# the watermark: a ring-and-star insignia, pressed once at half pressure
d.shape("ellipse", "Mark ring", x=640, y=398, width=72, height=72,
        fill=NONE, stroke=MARK, strokeWidth=4, opacity=22)
d.shape("ellipse", "Mark ring inner", x=654, y=412, width=44, height=44,
        fill=NONE, stroke=MARK, strokeWidth=2.5, opacity=18)
d.path("M676,414 L681,427 L694,428 L684,437 L687,450 L676,443 L665,450 "
       "L668,437 L658,428 L671,427 Z", "Mark star", fill=MARK,
       opacity=20, stroke=NONE)
# sheen where the light passes through the grain
d.path(rot_rect_path(614, 340, 150, 60, -13), "Sheet sheen",
       fill="#FFFFFF", opacity=16, stroke=NONE)

# --- paws gripping the sheet corners -------------------------------------------------
d.shape("ellipse", "Paw left", x=482, y=368, width=26, height=22,
        fill="#94816A", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Paw right", x=584, y=466, width=26, height=22,
        fill="#94816A", stroke=INK, strokeWidth=3.5)

# --- captions -------------------------------------------------------------------------
d.text("RELIEF WATERMARK", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EDE4CC", justify="center")
r = d.text("APPLIED INSUFFICIENTLY, BY DESIGN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4B892", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("267.relief-watermark-V1R00")
