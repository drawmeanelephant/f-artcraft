#!/usr/bin/env python3
"""AC-11 Sealloop Auditor — mascot portrait V1R00.
A grey seal pressing one more wax seal onto a certificate already crowded
with them, flipper on the stamp, fresh impression still warm; a faint seal
watermark rings the plate behind. 1000x1000 plate format.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("AC-11 Sealloop Auditor — Mascot Portrait", 1000, 1000)

INK = "#3A3030"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#141C26"}, {"offset": 1, "color": "#070A10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6EBEF"}, {"offset": 0.65, "color": "#B2C0C9"},
    {"offset": 1, "color": "#7A8E9A"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 430], "end": [0, 790], "stops": [
    {"offset": 0, "color": "#AEBFC8"}, {"offset": 0.6, "color": "#7C929E"},
    {"offset": 1, "color": "#54666F"}]}}
CERT_GRAD = {"gradient": {"kind": "linear", "start": [0, 575], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#F4EDD9"}, {"offset": 1, "color": "#DCCFAC"}]}}
HANDLE_GRAD = {"gradient": {"kind": "linear", "start": [580, 500], "end": [660, 590], "stops": [
    {"offset": 0, "color": "#7E6244"}, {"offset": 1, "color": "#54402A"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#9DB6C2", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E4250", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDF3F5", strokeWidth=3, opacity=38)
# faint concentric seal watermark behind the mascot — the ornate border growing
d.shape("ellipse", "Seal echo outer", x=196, y=156, width=608, height=608,
        fill=NONE, stroke="#6E8896", strokeWidth=10, opacity=10)
d.shape("ellipse", "Seal echo inner", x=226, y=186, width=548, height=548,
        fill=NONE, stroke="#6E8896", strokeWidth=6, opacity=8)
for i, (x, y, w) in enumerate([(180, 350, 6), (825, 330, 7), (165, 545, 7), (840, 580, 6),
                               (265, 780, 6), (730, 775, 7), (315, 138, 5), (675, 130, 6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E7A86", opacity=35, stroke=NONE)
for i, (x, y, w) in enumerate([(65, 150, 4), (920, 120, 5), (55, 580, 4), (945, 650, 4),
                               (140, 910, 4), (870, 920, 5), (545, 26, 4), (255, 40, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#C6D6DE", opacity=28, stroke=NONE)

# --- ground shadow -------------------------------------------------------------
d.shape("ellipse", "Shadow", x=340, y=772, width=320, height=30,
        fill="#2E4250", opacity=24, stroke=NONE)

# --- tail flippers behind the body ----------------------------------------------
d.path("M400,742 C350,742 312,758 288,792 C322,802 372,798 404,782 Z",
       "Tail L", fill="#627886", stroke=INK, strokeWidth=5)
d.path("M600,742 C650,742 688,758 712,792 C678,802 628,798 596,782 Z",
       "Tail R", fill="#627886", stroke=INK, strokeWidth=5)

# --- seal body --------------------------------------------------------------------
d.path("M370,760 C358,650 368,552 405,488 C432,444 568,444 595,488 "
       "C632,552 642,650 630,760 C598,782 552,790 500,790 "
       "C448,790 402,782 370,760 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly patch + shading
d.path("M430,690 C436,750 564,750 570,690 C570,742 560,768 500,770 "
       "C440,768 430,742 430,690 Z", "Belly", fill="#C4D2D8",
       opacity=55, stroke=NONE)
d.shape("ellipse", "Dome light", x=425, y=462, width=150, height=58,
        fill="#FFFFFF", opacity=16, stroke=NONE)
d.path("M396,712 C434,736 566,736 604,712 C576,748 424,748 396,712 Z",
       "Hem shade", fill="#44555E", opacity=28, stroke=NONE)

# face: earnest auditor eyes, seal muzzle, whiskers
d.shape("ellipse", "Eye L", x=440, y=498, width=40, height=46,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=520, y=498, width=40, height=46,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=452, y=516, width=17, height=22,
        fill="#26202A", stroke=NONE)
d.shape("ellipse", "Pupil R", x=532, y=516, width=17, height=22,
        fill="#26202A", stroke=NONE)
d.shape("ellipse", "Glint L", x=456, y=520, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=536, y=520, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# muzzle lobes + nose + prim little mouth
d.shape("ellipse", "Muzzle L", x=470, y=552, width=32, height=22,
        fill="#C8D6DC", opacity=80, stroke=NONE)
d.shape("ellipse", "Muzzle R", x=498, y=552, width=32, height=22,
        fill="#C8D6DC", opacity=80, stroke=NONE)
d.path("M490,548 C494,540 506,540 510,548 C508,556 492,556 490,548 Z",
       "Nose", fill="#2A2226", stroke=NONE)
d.path("M486,568 C494,574 506,574 514,568", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# whiskers
for lbl, dd in [("Whisker L1", "M452,548 L416,540"), ("Whisker L2", "M450,558 L410,560"),
                ("Whisker L3", "M452,566 L418,578"), ("Whisker R1", "M548,548 L584,540"),
                ("Whisker R2", "M550,558 L590,560"), ("Whisker R3", "M548,566 L582,578")]:
    d.path(dd, lbl, fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")

# --- certificate held in front ----------------------------------------------------
d.shape("rectangle", "Certificate", x=330, y=575, width=340, height=205,
        fill=CERT_GRAD, stroke="#6E5636", strokeWidth=4)
d.shape("rectangle", "Cert inner rule", x=342, y=587, width=316, height=181,
        fill=NONE, stroke="#8A6A44", strokeWidth=2, opacity=70)
d.text("CERTIFIED", "Cert header", x=430, y=618, size=17,
       font="Virelai Sans", color="#6E5636", justify="center")
for i, y in enumerate((642, 662, 682)):
    d.path(f"M366,{y} L494,{y}", f"Cert line {i+1}", fill=NONE,
           stroke="#9A8A6A", strokeWidth=4, opacity=60, cap="round")
# crowded seals already applied — wax medallions + ribbon tails
def wax(cx, cy, r, color, label, ribbon=True):
    if ribbon:
        d.path(f"M{cx - 8},{cy + r - 4} L{cx - 14},{cy + r + 26} L{cx - 2},{cy + r + 18} Z",
               f"{label} tail L", fill=color, opacity=85, stroke=NONE)
        d.path(f"M{cx + 8},{cy + r - 4} L{cx + 16},{cy + r + 24} L{cx + 4},{cy + r + 16} Z",
               f"{label} tail R", fill=color, opacity=85, stroke=NONE)
    d.shape("ellipse", label, x=cx - r, y=cy - r, width=2 * r, height=2 * r,
            fill=color, stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"{label} ring", x=cx - r + 6, y=cy - r + 6,
            width=2 * r - 12, height=2 * r - 12,
            fill=NONE, stroke="#F6EEDD", strokeWidth=2, opacity=60)

wax(388, 748, 20, "#B5453C", "Seal old 1")
wax(452, 756, 22, "#C9963C", "Seal old 2")
wax(516, 744, 19, "#4A6E9E", "Seal old 3")
wax(566, 762, 21, "#5A8A5E", "Seal old 4")
wax(624, 748, 19, "#7A5A8C", "Seal old 5")
wax(424, 726, 16, "#4A6E9E", "Seal old 6", ribbon=False)
wax(598, 716, 15, "#B5453C", "Seal old 7", ribbon=False)

# --- left flipper holding the certificate edge ------------------------------------
d.path("M372,640 C340,634 322,614 328,590 L364,594 C364,610 372,624 386,634 Z",
       "Flipper L", fill="#8CA2AE", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Grip L", x=314, y=578, width=48, height=38,
        fill="#9FB4BE", stroke=INK, strokeWidth=5)

# --- right flipper on the stamp ---------------------------------------------------
d.path("M632,616 C660,584 658,548 630,530 L606,556 C624,568 628,592 616,614 Z",
       "Flipper R", fill="#8CA2AE", stroke=INK, strokeWidth=5)
# the audit stamp: knob, handle, die — pressing the fresh seal
d.path("M650,500 L604,574", "Stamp handle", fill=NONE, stroke="#5A4632",
       strokeWidth=20, cap="round")
d.shape("ellipse", "Stamp knob", x=634, y=486, width=34, height=30,
        fill=HANDLE_GRAD, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(602, 582, 48, 22, -35), "Stamp die", fill="#4A3A28",
       stroke=INK, strokeWidth=4)
# the fresh seal, still glossy
wax(598, 632, 22, "#C24638", "Seal fresh", ribbon=False)
d.shape("ellipse", "Fresh gleam", x=590, y=622, width=12, height=8,
        fill="#FFFFFF", opacity=50, stroke=NONE)
# impact ticks
for i, (x1, y1, x2, y2) in enumerate([(560, 600, 548, 592), (640, 606, 652, 598),
                                      (588, 586, 584, 574)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Stamp tick {i+1}", fill=NONE,
           stroke="#8A6A44", strokeWidth=4, cap="round")

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

NAME = "AC-11 SEALLOOP AUDITOR"
d.text(NAME, "Name", x=500, y=930, size=52, font="Virelai Sans",
       color="#DCE6EA", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "ACCREDITATION NESTING COLLEGIUM"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#8EA8B2", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("083.ac-11-sealloop-auditor-V1R00")
