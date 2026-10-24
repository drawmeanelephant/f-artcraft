#!/usr/bin/env python3
"""CE-5 Countersign Aggregate — mascot portrait V1R00.
A co-existence endorsement packet whose five-cell grid bears five
overlapping signatures in five inks; the newest hand has swept straight
through the margin, overwriting the comments that used to ask questions.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("CE-5 Countersign Aggregate — Mascot Portrait", 1000, 1000)

INK = "#211E26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12141C"}, {"offset": 1, "color": "#080910"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#525E74"}, {"offset": 0.7, "color": "#37404F"},
    {"offset": 1, "color": "#1C222E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C3240"}, {"offset": 1, "color": "#13161F"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EEDA"}, {"offset": 1, "color": "#D5CCA8"}]}}
RULE = "#A89878"
SIG_NAVY = "#2E4A7A"
SIG_SEPIA = "#7A5632"
SIG_WINE = "#7E3A50"
SIG_GREEN = "#3E5C46"
SIG_FRESH = "#1E2838"
PEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A4452"}, {"offset": 1, "color": "#3E2330"}]}}

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

def rp(x, y):
    return rot_pt(DCX, DCY, x, y, DDEG)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8494AC", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4CFDE", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(196,236,8),(800,230,7),(158,524,9),(836,546,8),
                               (248,766,7),(756,748,9),(134,394,6),(864,390,7),
                               (394,112,7),(610,110,8),(334,824,6),(666,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#424C60", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0E15",
       strokeWidth=4, opacity=70)

# --- the endorsement packet ------------------------------------------------------------
DCX, DCY, DDEG = 500, 432, 3
d.shape("ellipse", "Packet shadow", x=270, y=664, width=470, height=30,
        fill="#05070A", opacity=55, stroke=NONE)
# carbon sheets underneath — the aggregate has been places
d.path(rot_rect_path(DCX - 10, DCY + 12, 430, 460, DDEG - 6),
       "Carbon under A", fill="#B6AE96", stroke=INK, strokeWidth=4,
       join="round", opacity=90)
d.path(rot_rect_path(DCX + 12, DCY + 6, 430, 460, DDEG + 6),
       "Carbon under B", fill="#C6BD9E", stroke=INK, strokeWidth=4,
       join="round", opacity=95)
# face sheet
d.path(rot_rect_path(DCX, DCY, 430, 460, DDEG), "Packet page",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=5, join="round")

# header band
hx, hy = rp(DCX, DCY - 186)
d.path(rot_rect_path(DCX, DCY - 186, 366, 46, DDEG), "Header band",
       fill="#3A4456", stroke=INK, strokeWidth=3, join="round")
t = d.text("ENDORSEMENT PACKET", "Header text", x=hx, y=hy + 6, size=16,
           font="Virelai Sans", color="#EDE6D0", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "header tilt", ids=[t["id"]], angle=DDEG,
          origin=[hx, hy])
# form number, small, in the header margin — digit via Source Sans 3
fx, fy = rp(DCX - 160, DCY - 150)
t = d.text("FORM CEP-1", "Form number", x=fx, y=fy, size=10,
           font="Virelai Sans", color="#9A8F74", justify="left")
if t and t.get("id"):
    d.cmd("object.rotate", "form tilt", ids=[t["id"]], angle=DDEG,
          origin=[fx, fy])
    d.cmd("text.setStyle", "form digit", ids=[t["id"]], start=9, end=10,
          font="Source Sans 3")

# the pre-ticked intent box
bx, by = rp(DCX - 150, DCY - 118)
d.path(rot_rect_path(bx, by, 18, 18, DDEG), "Intent box", fill=NONE,
       stroke=INK, strokeWidth=3)
p1 = rp(DCX - 153, DCY - 118); p2 = rp(DCX - 148, DCY - 112)
p3 = rp(DCX - 138, DCY - 126)
d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f} "
       f"L{p3[0]:.0f},{p3[1]:.0f}", "Pre-tick", fill=NONE,
       stroke=SIG_FRESH, strokeWidth=3.5, cap="round", join="round")
lx, ly = rp(DCX - 124, DCY - 112)
t = d.text("INTENT TO CO-EXIST", "Intent label", x=lx, y=ly, size=11,
           font="Virelai Sans", color="#6E6450", justify="left")
if t and t.get("id"):
    d.cmd("object.rotate", "intent tilt", ids=[t["id"]], angle=DDEG,
          origin=[lx, ly])

# --- the five-row endorsement grid ------------------------------------------------------
GX0, GX1 = DCX - 180, DCX + 100   # grid spans; margin keeps the right strip
GY0, RH = DCY - 92, 52
for i in range(6):  # rules
    a = rp(GX0, GY0 + i * RH); b = rp(GX1, GY0 + i * RH)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"Grid rule {i+1}", fill=NONE, stroke=RULE, strokeWidth=2.5,
           opacity=75)
for gx in (GX0, GX0 + 44, GX1):  # uprights: left edge, numeral gutter, right
    a = rp(gx, GY0); b = rp(gx, GY0 + 5 * RH)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"Grid upright {gx}", fill=NONE, stroke=RULE, strokeWidth=2.5,
           opacity=75)
# roman numerals down the gutter — Virelai-pure, no digits needed
for i, num in enumerate(["I", "II", "III", "IV", "V"]):
    nx, ny = rp(GX0 + 22, GY0 + i * RH + 32)
    t = d.text(num, f"Row numeral {i+1}", x=nx, y=ny, size=13,
               font="Virelai Sans", color=RULE, justify="center")
    if t and t.get("id"):
        d.cmd("object.rotate", f"numeral {i+1} tilt", ids=[t["id"]],
              angle=DDEG, origin=[nx, ny])

# --- the signatures: five inks, none respecting the rows -------------------------------
def sig(points, color, w, label, op=92):
    d.path(points, label, fill=NONE, stroke=color, strokeWidth=w,
           cap="round", join="round", opacity=op)

# 1 — navy, careful, first to sign
sig("M340,336 C352,310 380,308 384,330 C388,352 366,362 356,348 "
    "C352,338 372,330 396,336 C424,344 458,334 478,326",
    SIG_NAVY, 5, "Sig 1 navy")
sig("M342,372 C400,366 448,366 500,360", SIG_NAVY, 3, "Sig 1 flourish", 70)

# 2 — sepia, a tight zigzag with a tail that wanders into row three
sig("M348,406 L366,384 L378,412 L396,386 L410,410 L428,390 "
    "C448,412 470,410 486,420 C500,428 512,436 524,432",
    SIG_SEPIA, 4.5, "Sig 2 sepia")

# 3 — wine, two great loops; in the tangle they nearly read as eyes
sig("M436,478 C410,460 414,424 446,424 C478,424 484,466 456,482 "
    "C444,490 430,486 436,478",
    SIG_WINE, 5, "Sig 3 loop L")
sig("M534,484 C510,466 516,428 548,430 C580,432 584,472 556,488 "
    "C544,494 530,492 534,484",
    SIG_WINE, 5, "Sig 3 loop R")
sig("M456,470 C480,458 506,462 534,472", SIG_WINE, 4, "Sig 3 bridge")

# 4 — green, hasty slashes drifting downward
sig("M352,510 L392,486 L384,518 L430,494 L422,524 L468,502 L460,530",
    SIG_GREEN, 4.5, "Sig 4 green")

# 5 — fresh ink: it signs the grid, then overwrites the margin itself
sig("M348,556 C420,534 500,552 570,522 C620,502 652,478 668,452",
    SIG_FRESH, 7, "Sig 5 sweep")
sig("M368,576 C452,560 540,574 640,536", SIG_FRESH, 4, "Sig 5 second", 80)

# marginal comments, half-buried under the fifth signature
for i, (my, words) in enumerate([(DCY - 40, "seems fine"),
                                 (DCY - 4, "already"),
                                 (DCY + 22, "happened")]):
    mx, myy = rp(DCX + 128, my)
    t = d.text(words, f"Margin {i+1}", x=mx, y=myy, size=10.5,
               font="Virelai Sans", color="#8A7E64", justify="left")
    if t and t.get("id"):
        d.cmd("object.rotate", f"margin {i+1} tilt", ids=[t["id"]],
              angle=DDEG, origin=[mx, myy])
        d.cmd("object.setProps", f"margin {i+1} fade", ids=[t["id"]],
              opacity=55)
# fresh ink strikes through the comments
a = rp(DCX + 116, DCY - 44); b = rp(DCX + 196, DCY - 30)
d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}", "Margin strike 1",
       fill=NONE, stroke=SIG_FRESH, strokeWidth=3.5, cap="round", opacity=75)
a = rp(DCX + 116, DCY + 2); b = rp(DCX + 190, DCY + 20)
d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}", "Margin strike 2",
       fill=NONE, stroke=SIG_FRESH, strokeWidth=3.5, cap="round", opacity=75)

# received stamp, crooked at the foot — chronology, outweighed
sx, sy = rp(DCX + 60, DCY + 176)
d.path(rot_rect_path(sx, sy, 150, 32, DDEG + 7), "Received stamp",
       fill=NONE, stroke="#8A4A3E", strokeWidth=3, opacity=55)
t = d.text("RECEIVED LATE", "Stamp text", x=sx, y=sy + 4, size=11,
           font="Virelai Sans", color="#8A4A3E", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "stamp tilt", ids=[t["id"]], angle=DDEG + 7,
          origin=[sx, sy])
    d.cmd("text.setStyle", "stamp track", ids=[t["id"]], tracking=140)
    d.cmd("object.setProps", "stamp fade", ids=[t["id"]], opacity=62)

# --- the pen that signed last, dropped on the floor --------------------------------------
d.shape("ellipse", "Pen shadow", x=252, y=680, width=160, height=18,
        fill="#05070A", opacity=50, stroke=NONE)
d.path(rot_rect_path(320, 664, 150, 20, -16), "Pen barrel",
       fill=PEN_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.path(rot_rect_path(392, 656, 26, 20, -16), "Pen cap band",
       fill="#C8A84E", stroke=INK, strokeWidth=3, join="round")
d.path("M262,672 L238,684 L258,690 Z", "Pen nib", fill="#C8A84E",
       stroke=INK, strokeWidth=3, join="round")
# a fresh ink drip beside it
d.shape("ellipse", "Ink drip", x=226, y=688, width=14, height=9,
        fill=SIG_FRESH, opacity=85, stroke=NONE)

# --- captions ----------------------------------------------------------------------
n = d.text("CE-5 COUNTERSIGN AGGREGATE", "Name", x=500, y=930, size=52,
           font="Virelai Sans", color="#E4E9F0", justify="center")
if n and n.get("id"):
    # Virelai Sans has no digit glyphs: "5" falls back to Source Sans 3
    d.cmd("text.setStyle", "name digit", ids=[n["id"]], start=3, end=4,
          font="Source Sans 3")
r = d.text("ENDORSEMENT OVERGROWTH", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA8BE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("077.ce-5-countersign-aggregate-V1R00")
