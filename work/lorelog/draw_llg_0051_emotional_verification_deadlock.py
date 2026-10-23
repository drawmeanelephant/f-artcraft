#!/usr/bin/env python3
"""LLG-0051-E Emotional Verification Deadlock — V1R00. Form 51-E nested inside
Form 51-E, paper eating itself; a clerk's stamp reading PREPARED / AMBIVALENT /
UNFIT; queues of identical forms receding to a vanishing point; Kindy
observing from a distance. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LLG-0051 Emotional Verification Deadlock", 1000, 1000)

INK = "#33271E"
PAPER = "#E8DCC0"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#211C26"}, {"offset": 1, "color": "#0E0B12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9C9A4"}, {"offset": 0.72, "color": "#A8916B"},
    {"offset": 1, "color": "#6E5B40"}]}}
DOC_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EAD2"}, {"offset": 1, "color": "#CFC2A0"}]}}
KINDY_G = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2D48A"}, {"offset": 1, "color": "#C79A4E"}]}}

def form(x, y, w, h, label, ink_op=100, q=True):
    """One Form 51-E: sheet + header + 'how does this form make you feel'."""
    d.shape("rectangle", f"{label} sheet", x=x, y=y, width=w, height=h,
            radius=max(2, w*0.03), fill=DOC_GRAD, stroke=INK,
            strokeWidth=max(1.5, w*0.016))
    if w > 90:
        d.text("FORM 51-E", f"{label} head", x=x + w/2, y=y + h*0.16,
               size=max(9, w*0.10), font="Virelai Sans",
               color=INK if ink_op >= 100 else "#5A4A3A",
               justify="center")
    if q and w > 150:
        d.text("HOW DOES THIS FORM MAKE YOU FEEL?", f"{label} question",
               x=x + w/2, y=y + h*0.30, size=max(7, w*0.052),
               font="Virelai Sans",
               color="#6A5C40" if ink_op >= 100 else "#8A7A5E",
               justify="center")
    # ruled lines
    n = 3 if w > 150 else 2
    for j in range(n):
        ly = y + h * (0.42 + j * 0.14)
        d.shape("rectangle", f"{label} rule {j+1}", x=x + w*0.12, y=ly,
                width=w*0.76, height=max(2, w*0.014), fill="#9A8A68",
                opacity=int(60 * ink_op / 100), stroke=NONE)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54462E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFE3C4", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=170, width=240, height=150,
        fill="#8C7852", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=700, width=250, height=140,
        fill="#8C7852", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(200,320,8),(790,240,7),(150,560,9),(830,540,8),
                               (260,790,7),(750,760,9),(140,420,6),(860,410,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A3C", opacity=40, stroke=NONE)

# --- queue of identical forms to the vanishing point (upper right) -------------
for i, (fx, fy, fw, fh, op) in enumerate([
        (760, 690, 170, 120, 95), (700, 600, 140, 99, 82),
        (650, 525, 112, 79, 68), (610, 465, 90, 63, 55),
        (578, 418, 72, 51, 44), (552, 382, 58, 41, 34)]):
    d.shape("rectangle", f"Queue form {i+1}", x=fx, y=fy, width=fw, height=fh,
            radius=4, fill=DOC_GRAD, stroke=INK, strokeWidth=2, opacity=op)
    d.shape("rectangle", f"Queue head {i+1}", x=fx+fw*0.12, y=fy+fh*0.14,
            width=fw*0.5, height=max(3, fh*0.10), fill="#8A7A5E",
            opacity=int(op*0.8), stroke=NONE)
    d.shape("rectangle", f"Queue rule {i+1}", x=fx+fw*0.12, y=fy+fh*0.45,
            width=fw*0.76, height=max(2, fh*0.06), fill="#9A8A68",
            opacity=int(op*0.6), stroke=NONE)
# vanishing-point convergence lines, very faint
d.path("M760,690 L540,360 M930,690 L560,368", "VP guides", fill=NONE,
       stroke="#6E5B40", strokeWidth=2, opacity=18)

# --- the central Form 51-E, nested inside itself ---------------------------------
# outer sheet
form(300, 330, 330, 400, "Outer")
# bite notches — the paper is eating itself (corner chew marks)
d.path("M300,690 Q312,672 300,652 Q320,664 322,640 Q338,656 344,632 "
       "L344,730 L300,730 Z", "Chew mark", fill="#A8916B", stroke=INK,
       strokeWidth=3)
# nested copy inside the outer form — recursion level 2
form(368, 480, 190, 230, "Nested", ink_op=80)
# recursion level 3 — a hint, fading
d.shape("rectangle", "Deep nest", x=430, y=590, width=72, height=88,
        radius=3, fill=DOC_GRAD, stroke=INK, strokeWidth=2, opacity=70)
d.text("51-E", "Deep nest head", x=466, y=620, size=12,
       font="Virelai Sans", color="#6A5C40", justify="center")
d.shape("rectangle", "Deep nest rule", x=442, y=636, width=48, height=4,
        fill="#9A8A68", opacity=50, stroke=NONE)
d.shape("rectangle", "Deeper still", x=462, y=630, width=26, height=32,
        fill=DOC_GRAD, stroke=INK, strokeWidth=1.5, opacity=45)

# --- the clerk's stamp: PREPARED / AMBIVALENT / UNFIT ------------------------------
stamp_ids = []
r = d.shape("rectangle", "Stamp box", x=320, y=740, width=250, height=98,
            radius=8, fill=NONE, stroke="#B03A2E", strokeWidth=5, opacity=85)
stamp_ids.append((r or {}).get("id"))
for j, word in enumerate(["PREPARED", "AMBIVALENT", "UNFIT"]):
    r = d.text(word, f"Stamp {word}", x=445, y=776 + j*26, size=17,
               font="Virelai Sans", color="#B03A2E", justify="center")
    stamp_ids.append((r or {}).get("id"))
ids = [i for i in stamp_ids if i]
if ids:
    d.call("transform", {"ids": ids, "rotate": -9, "origin": [445, 789]},
           "tilt stamp")

# --- Kindy observing from a distance -----------------------------------------------
d.shape("ellipse", "Kindy lantern glow", x=150, y=640, width=70, height=70,
        fill="#FFDF8A", opacity=25, stroke=NONE)
d.path("M180,650 Q205,636 230,650 L230,730 Q205,744 180,730 Z",
       "Kindy body", fill=KINDY_G, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Kindy eye L", x=192, y=676, width=8, height=10,
        fill="#2A1C16", stroke=NONE)
d.shape("ellipse", "Kindy eye R", x=210, y=676, width=8, height=10,
        fill="#2A1C16", stroke=NONE)
d.shape("ellipse", "Kindy lantern", x=152, y=686, width=34, height=34,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFF3C2"},
            {"offset": 1, "color": "#E8A33D"}]}},
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Kindy flame", x=164, y=698, width=10, height=12,
        fill="#FFF6D8", stroke=NONE)
# watching the recursion — sight line, faint
d.path("M232,668 Q380,600 470,560", "Kindy gaze", fill=NONE,
       stroke="#6E5B40", strokeWidth=2, opacity=25, dash=[6, 8])

# --- name + role ----------------------------------------------------------------------
d.text("FORM 51-E", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#EFE3C4", justify="center")
d.text("F E E L I N G S   A B O U T   F E E L I N G S", "Role", x=500,
       y=968, size=20, font="Virelai Sans", color="#B8A67E",
       justify="center")

d.finish("llg-0051-emotional-verification-deadlock-V1R00")
