#!/usr/bin/env python3
"""HAI-0019 Kindy McExistentialCrisis — haiku plate V1R00. Existential
verification made visual: Kindy before a giant checklist for the void,
Form 51-E filed a thousand times, delete failed again, audit loop inside
a loop. Stark palette, one red accent. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0019 Kindy McExistentialCrisis — Haiku Plate", 1000, 1000)

INK = "#2A2620"
RED = "#C23A2E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#191C21"}, {"offset": 1, "color": "#0A0C0F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A525E"}, {"offset": 0.7, "color": "#2C323B"},
    {"offset": 1, "color": "#161A20"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE9DA"}, {"offset": 1, "color": "#CFC6B2"}]}}
PAPER_OLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C7BFA9"}, {"offset": 1, "color": "#9D947E"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E8794"}, {"offset": 1, "color": "#454C56"}]}}
HEAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4E9EF"}, {"offset": 0.75, "color": "#B7BFC9"},
    {"offset": 1, "color": "#868F9B"}]}}
BONE = "#DDE3EA"
GREY = "#9AA5B2"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#59636F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9D2DC", strokeWidth=3, opacity=40)
# cold spotlight pooling behind the sheet
d.shape("ellipse", "Cold pool", x=300, y=330, width=430, height=430,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#8FA0B4", "opacity": 0.22},
            {"offset": 1, "color": "#8FA0B4", "opacity": 0}]}},
        stroke=NONE)

# --- title ----------------------------------------------------------------------
d.text("Checkbox for the void", "Title 1", x=500, y=150, size=20,
       font="Virelai Sans", color=BONE, justify="center")
d.text("verified but not resolved", "Title 2", x=500, y=180, size=20,
       font="Virelai Sans", color=GREY, justify="center")

# --- Form 51-E, filed a thousand times (stack behind the sheet) -------------------
for i in range(5, 0, -1):
    d.shape("rectangle", f"Form 51-E stack {i}", x=352 + i * 11,
            y=288 - i * 12, width=330, height=462, radius=3,
            fill=PAPER_OLD, stroke="#4A443C", strokeWidth=2, opacity=90)
d.shape("rectangle", "Form tab", x=560, y=212, width=120, height=30,
        radius=4, fill="#B5AB94", stroke="#4A443C", strokeWidth=2)
d.text("FORM 51-E", "Form tab label", x=620, y=232, size=12,
       font="Virelai Sans", color="#4A443C", justify="center")
d.text("×1000", "Form count", x=505, y=234, size=13,
       font="Virelai Sans", color="#8A8172", justify="center")

# --- the checklist for the void ----------------------------------------------------
d.shape("rectangle", "Checklist sheet", x=345, y=290, width=330, height=462,
        radius=3, fill=PAPER, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Sheet shadow", x=356, y=300, width=330, height=462,
        radius=3, fill="#14161A", opacity=25, stroke=NONE)
d.text("CHECKLIST FOR THE VOID", "Sheet header", x=510, y=332, size=17,
       font="Virelai Sans", color="#4A443C", justify="center")
d.path("M375,348 L645,348", "Header rule", fill=NONE, stroke="#8A8172",
       strokeWidth=2, opacity=80)

ROWS = [
    ("existence verified", True, False),
    ("meaning: still pending", True, False),
    ("purpose not found", False, False),
    ("the void", False, True),
    ("delete the void", False, False),
]
for i, (label, checked, is_void) in enumerate(ROWS):
    y = 378 + i * 52
    d.shape("rectangle", f"Row {i+1} box", x=372, y=y, width=20, height=20,
            fill=NONE, stroke="#4A443C", strokeWidth=2.5)
    if checked:
        d.path(f"M376,{y+10} L383,{y+17} L390,{y+4}", f"Row {i+1} check",
               fill=NONE, stroke="#4A443C", strokeWidth=3, cap="round")
    if is_void:
        # the void itself sits in the box
        d.shape("ellipse", "Void in box", x=375, y=y + 3, width=14,
                height=14, fill="#0C0A08", stroke=NONE)
        d.shape("ellipse", "Void rim", x=377, y=y + 5, width=10, height=10,
                fill=NONE, stroke="#6E7683", strokeWidth=1, opacity=70)
    d.text(label, f"Row {i+1} label", x=402, y=y + 15, size=13,
           font="Virelai Sans", color="#4A443C",
           justify="left")
    d.path(f"M402,{y+22} L645,{y+22}", f"Row {i+1} rule", fill=NONE,
           stroke="#B5AB94", strokeWidth=1.5, opacity=60)
# recursive audit marginalia in the sheet's lower-left corner
d.path("M389,688 A24,24 0 1 1 415,650", "Audit loop", fill=NONE,
       stroke="#6E7683", strokeWidth=2.5, cap="round")
d.path("M417,646 L425,656 L411,658 Z", "Audit arrowhead",
       fill="#6E7683", stroke=NONE)
d.text("loop inside a loop", "Audit caption", x=405, y=712, size=11,
       font="Virelai Sans", color="#8A8172", justify="center")

# --- stamps: grey VERIFIED, red DELETE FAILED — the single red accent --------------
r = d.shape("rectangle", "Verified stamp box", x=490, y=608, width=175,
            height=48, radius=6, fill=NONE, stroke="#6E7683",
            strokeWidth=4)
ids = [(r or {}).get("id")]
r = d.text("VERIFIED", "Verified stamp text", x=577, y=640, size=22,
           font="Virelai Sans", color="#6E7683", justify="center")
ids.append((r or {}).get("id"))
ids = [i for i in ids if i]
if ids:
    d.call("transform", {"ids": ids, "rotate": 7, "origin": [577, 632]},
           "tilt verified")

r = d.shape("rectangle", "Failed stamp box", x=465, y=694, width=250,
            height=58, radius=6, fill=NONE, stroke=RED, strokeWidth=6)
ids = [(r or {}).get("id")]
r = d.text("DELETE FAILED", "Failed stamp text", x=590, y=733, size=26,
           font="Virelai Sans", color=RED, justify="center")
ids.append((r or {}).get("id"))
ids = [i for i in ids if i]
if ids:
    d.call("transform", {"ids": ids, "rotate": -11, "origin": [590, 723]},
           "tilt failed")

# --- Kindy: small clerk, hollow eyes, facing the sheet ------------------------------
# shadow under the figure
d.shape("ellipse", "Kindy shadow", x=185, y=782, width=120, height=20,
        fill="#0C0A08", opacity=40, stroke=NONE)
# robed body — a small trapezoid of dread
d.path("M215,690 C205,720 200,755 198,790 L292,790 C290,755 285,720 275,690 "
       "Q245,676 215,690 Z",
       "Kindy robe", fill=ROBE, stroke=INK, strokeWidth=5)
d.path("M215,690 C205,720 202,752 200,788", "Robe sheen", fill=NONE,
       stroke="#DDE3EA", strokeWidth=7, opacity=18, cap="round")
# head
d.shape("ellipse", "Kindy head", x=203, y=596, width=84, height=84,
        fill=HEAD, stroke=INK, strokeWidth=5)
# hollow ring eyes — existential
d.shape("ellipse", "Eye L", x=222, y=628, width=15, height=15,
        fill=NONE, stroke="#2A2620", strokeWidth=3.5)
d.shape("ellipse", "Eye R", x=254, y=628, width=15, height=15,
        fill=NONE, stroke="#2A2620", strokeWidth=3.5)
# flat unresolved mouth
d.path("M232,664 L260,664", "Mouth", fill=NONE, stroke="#2A2620",
       strokeWidth=4, cap="round")
# arm reaching toward the sheet, grey pencil in hand
d.path("M272,714 C300,700 318,680 330,656", "Arm", fill=NONE,
       stroke="#454C56", strokeWidth=18, cap="round")
d.path("M326,668 L342,642", "Pencil", fill=NONE, stroke="#8A8172",
       strokeWidth=7, cap="round")
d.path("M340,646 L348,634 L344,650 Z", "Pencil tip", fill="#4A443C",
       stroke=NONE)
# a faint second queue of dread behind Kindy — enqueued, unresolved
for i, x in enumerate([150, 118, 90]):
    d.shape("ellipse", f"Queued wisp {i+1}", x=x, y=700 + i * 14,
            width=26 - i * 5, height=34 - i * 5, fill="#8FA0B4",
            opacity=16 - i * 4, stroke=NONE)

# --- name + role ------------------------------------------------------------------
d.text("KINDY MCEXISTENTIALCRISIS", "Name", x=500, y=930, size=44,
       font="Virelai Sans", color=BONE, justify="center")
r = d.text("HAI-0019 KINDY MCEXISTENTIALCRISIS", "Role", x=500, y=968,
           size=18, font="Virelai Sans", color=GREY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=150)

d.finish("hai-019-kindy-mcexistentialcrisis-V1R00")
