#!/usr/bin/env python3
"""AV-14 Nullseal Register — mascot portrait V1R00.
An audit document mid-harmonization: findings rows dissolve to illegible
squiggles beneath a faint plum seal stamped over the margin. The seal
wears the calm face of grammatical fatigue — blank, but verified.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("AV-14 Nullseal Register — Mascot Portrait", 1000, 1000)

INK = "#232A22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10160F"}, {"offset": 1, "color": "#070B08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C6E58"}, {"offset": 0.7, "color": "#3C4A3A"},
    {"offset": 1, "color": "#1E271D"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E382C"}, {"offset": 1, "color": "#131811"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2ECDA"}, {"offset": 1, "color": "#D2C8A6"}]}}
TXT = "#6E6450"
MARG = "#8A7A60"
SEAL = "#9A5E66"
STAMP_PAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4448"}, {"offset": 1, "color": "#26222A"}]}}

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8FA488", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8C0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(196,238,8),(798,230,7),(158,524,9),(838,546,8),
                               (248,764,7),(754,748,9),(134,392,6),(862,392,7),
                               (392,112,7),(612,110,8),(334,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#42523E", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0B0F0B",
       strokeWidth=4, opacity=70)

# --- the audit document -------------------------------------------------------------
DCX, DCY, DDEG = 495, 442, -3
d.shape("ellipse", "Doc shadow", x=280, y=668, width=460, height=30,
        fill="#060906", opacity=55, stroke=NONE)
# page behind, slightly askew — the register accumulates
d.path(rot_rect_path(DCX + 14, DCY + 10, 396, 490, DDEG - 5),
       "Back page", fill="#C2B68F", stroke=INK, strokeWidth=4,
       join="round", opacity=95)
# front page
d.path(rot_rect_path(DCX, DCY, 396, 490, DDEG), "Audit page",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=5, join="round")
# header band
hx, hy = rot_pt(DCX, DCY, DCX, DCY - 196, DDEG)
d.path(rot_rect_path(DCX, DCY - 196, 340, 44, DDEG), "Header band",
       fill="#3E4A3C", stroke=INK, strokeWidth=3, join="round")
t = d.text("AUDIT FINDINGS", "Header text", x=hx, y=hy + 6, size=17,
           font="Virelai Sans", color="#EDE6CE", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "header tilt", ids=[t["id"]], angle=DDEG,
          origin=[hx, hy])

# --- findings rows: crisp up top, dissolving where the seal has landed --------------
rows = [
    # (y_offset_in_page, length, weight, opacity, wavy)
    (-150, 300, 5, 80, False), (-118, 260, 5, 75, False),
    (-86, 310, 5, 78, False), (-54, 240, 5, 70, False),
    (-22, 330, 7, 85, False),   # <- the section that used to say failure
    (10, 300, 5, 45, True), (42, 280, 5, 30, True),
    (74, 310, 5, 22, True), (106, 250, 5, 16, True),
    (138, 280, 5, 55, False),   # executive summary: bright, clean, confident
]
for i, (dy, ln, w, op, wavy) in enumerate(rows):
    x0, x1 = DCX - 150, DCX - 150 + ln
    ry = DCY + dy
    a = rot_pt(DCX, DCY, x0, ry, DDEG)
    b = rot_pt(DCX, DCY, x1, ry, DDEG)
    if not wavy:
        d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
               f"Finding {i+1}", fill=NONE, stroke=TXT, strokeWidth=w,
               cap="round", opacity=op)
    else:
        # harmonized into illegibility: a faint wandering line
        m1 = rot_pt(DCX, DCY, x0 + ln * 0.33, ry - 6, DDEG)
        m2 = rot_pt(DCX, DCY, x0 + ln * 0.66, ry + 6, DDEG)
        d.path(f"M{a[0]:.0f},{a[1]:.0f} C{m1[0]:.0f},{m1[1]:.0f} "
               f"{m2[0]:.0f},{m2[1]:.0f} {b[0]:.0f},{b[1]:.0f}",
               f"Finding {i+1} dissolved", fill=NONE, stroke=TXT,
               strokeWidth=w, cap="round", opacity=op)

# the ghost of the word that used to be there
gx, gy = rot_pt(DCX, DCY, DCX - 20, DCY - 22, DDEG)
t = d.text("failure", "Ghost word", x=gx, y=gy, size=14,
           font="Virelai Sans", color="#7A4030", justify="left")
if t and t.get("id"):
    d.cmd("object.rotate", "ghost tilt", ids=[t["id"]], angle=DDEG,
          origin=[gx, gy])
    d.cmd("object.setProps", "ghost fade", ids=[t["id"]], opacity=18)

# marginalia in the left margin, half-erased
for i, (dy, ln, op) in enumerate([(-100, 46, 50), (-70, 34, 40),
                                  (96, 40, 35)]):
    a = rot_pt(DCX, DCY, DCX - 178, DCY + dy, DDEG)
    b = rot_pt(DCX, DCY, DCX - 178 + ln, DCY + dy, DDEG)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"Margin note {i+1}", fill=NONE, stroke=MARG, strokeWidth=3,
           cap="round", opacity=op)

# --- the Nullseal itself: faint, serene, margin-high ---------------------------------
SCX, SCY = 668, 330
# stamped ink halo bleeding into the paper
d.shape("ellipse", "Seal bloom", x=SCX-118, y=SCY-118, width=236, height=236,
        fill=SEAL, opacity=14, stroke=NONE)
# double rim, stamped unevenly
d.shape("ellipse", "Seal rim", x=SCX-102, y=SCY-102, width=204, height=204,
        fill=NONE, stroke=SEAL, strokeWidth=8, opacity=48)
d.shape("ellipse", "Seal rim inner", x=SCX-84, y=SCY-84, width=168,
        height=168, fill=NONE, stroke=SEAL, strokeWidth=3, opacity=40)
# rim ticks where the legend would read, if anything still read
for i in range(12):
    a = math.radians(i * 30 + 15)
    x1, y1 = SCX + 72 * math.cos(a), SCY + 72 * math.sin(a)
    x2, y2 = SCX + 80 * math.cos(a), SCY + 80 * math.sin(a)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Seal tick {i+1}",
           fill=NONE, stroke=SEAL, strokeWidth=4, cap="round", opacity=42)
# its calm, closed face — encouraging, unreadable
d.path(f"M{SCX-38},{SCY-12} C{SCX-28},{SCY-4} {SCX-16},{SCY-4} {SCX-8},{SCY-12}",
       "Seal eye L", fill=NONE, stroke=SEAL, strokeWidth=6, cap="round",
       opacity=55)
d.path(f"M{SCX+8},{SCY-12} C{SCX+16},{SCY-4} {SCX+28},{SCY-4} {SCX+38},{SCY-12}",
       "Seal eye R", fill=NONE, stroke=SEAL, strokeWidth=6, cap="round",
       opacity=55)
d.path(f"M{SCX-16},{SCY+28} C{SCX-6},{SCY+34} {SCX+6},{SCY+34} {SCX+16},{SCY+28}",
       "Seal mouth", fill=NONE, stroke=SEAL, strokeWidth=6, cap="round",
       opacity=50)
# registration wobble: the same rim ghosted a few points off
d.shape("ellipse", "Seal rim echo", x=SCX-108, y=SCY-96, width=204,
        height=204, fill=NONE, stroke=SEAL, strokeWidth=3, opacity=22)

# a small rectangular stamp below: the word that replaced the finding
sx, sy = rot_pt(DCX, DCY, DCX + 40, DCY + 108, DDEG)
d.path(rot_rect_path(sx, sy, 150, 34, DDEG - 2), "Harmonized stamp",
       fill=NONE, stroke=SEAL, strokeWidth=3, opacity=50)
t = d.text("HARMONIZED", "Stamp text", x=sx, y=sy + 5, size=12,
           font="Virelai Sans", color=SEAL, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "stamp tilt", ids=[t["id"]], angle=DDEG - 2,
          origin=[sx, sy])
    d.cmd("text.setStyle", "stamp track", ids=[t["id"]], tracking=160)
    d.cmd("object.setProps", "stamp fade", ids=[t["id"]], opacity=60)

# --- the rubber stamp that did it, resting on the floor -------------------------------
d.shape("ellipse", "Stamp shadow", x=700, y=676, width=170, height=22,
        fill="#060906", opacity=50, stroke=NONE)
d.path(rot_rect_path(786, 636, 120, 44, -14), "Stamp base",
       fill=STAMP_PAD, stroke=INK, strokeWidth=4, join="round")
d.path(rot_rect_path(786, 598, 44, 60, -14), "Stamp neck",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#8A6A4A"}, {"offset": 1, "color": "#54402C"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.path(rot_rect_path(786, 566, 66, 30, -14), "Stamp grip",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#A8845E"}, {"offset": 1, "color": "#6E5236"}]}},
       stroke=INK, strokeWidth=4, join="round")
# residual ink on the die
d.path(rot_rect_path(786, 656, 96, 10, -14), "Die ink", fill=SEAL,
       stroke=NONE, join="round", opacity=55)

# paperclip keeping nothing in particular attached
d.path("M330,196 C330,178 350,176 352,192 L354,224 C355,240 336,244 333,228 "
       "L332,204", "Paperclip", fill=NONE, stroke="#9AA6A8", strokeWidth=5,
       cap="round", opacity=80)

# dust of dissolved wording
for i, (x, y, s) in enumerate([(600, 520, 4), (640, 560, 5), (566, 590, 4),
                               (690, 510, 3), (616, 610, 4)]):
    d.shape("ellipse", f"Lexical dust {i+1}", x=x, y=y, width=s, height=s,
            fill=MARG, opacity=35, stroke=NONE)

# --- captions ----------------------------------------------------------------------
n = d.text("AV-14 NULLSEAL REGISTER", "Name", x=500, y=930, size=56,
           font="Virelai Sans", color="#E4EBE0", justify="center")
if n and n.get("id"):
    # Virelai Sans has no digit glyphs: "14" falls back to Source Sans 3
    d.cmd("text.setStyle", "name digits", ids=[n["id"]], start=3, end=5,
          font="Source Sans 3")
r = d.text("CERTIFIES GRAMMATICAL FATIGUE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AB09A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("076.av-14-nullseal-register-V1R00")
