#!/usr/bin/env python3
"""Seal of Maybe Enough — mascot portrait V1R00.
An amber clerk pressing a brass seal into still-cooling wax on a document
marked APPROVED / WITH RESERVATIONS; a wall clock quietly reads five o'clock.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Seal of Maybe Enough — Mascot Portrait", 1000, 1000)

INK = "#3A2822"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B1216"}, {"offset": 1, "color": "#0A0608"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A3532"}, {"offset": 0.7, "color": "#2B1F22"},
    {"offset": 1, "color": "#150F11"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#322525"}, {"offset": 1, "color": "#130F10"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9AE6C"}, {"offset": 0.72, "color": "#B4854C"},
    {"offset": 1, "color": "#8A6234"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6B4A36"}, {"offset": 1, "color": "#3E2A20"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A30"}, {"offset": 1, "color": "#2A1C18"}]}}
WAX_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C65A4E"}, {"offset": 0.7, "color": "#9A3630"},
    {"offset": 1, "color": "#6E201E"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D9B25C"}, {"offset": 1, "color": "#8A6A2E"}]}}
PAPER = "#E3D5B4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4AE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A3A38", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A08",
       strokeWidth=4, opacity=70)

# --- the clock: it is five o'clock, no numerals ---------------------------------
d.shape("ellipse", "Clock case", x=196, y=176, width=92, height=92,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#584340"}, {"offset": 1, "color": "#36272A"}]}},
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Clock face", x=206, y=186, width=72, height=72,
        fill="#21181A", stroke="#7A5E52", strokeWidth=2)
for k in range(4):
    a = k * math.pi / 2
    x1 = 242 + math.sin(a) * 26; y1 = 222 - math.cos(a) * 26
    x2 = 242 + math.sin(a) * 31; y2 = 222 - math.cos(a) * 31
    d.path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", f"Clock tick {k+1}",
           fill=NONE, stroke="#C9A98E", strokeWidth=2.5, cap="round", opacity=80)
# hands: hour at 5, minute near 12 — the agreed hour
d.path("M242,222 L257,243", "Hour hand", fill=NONE, stroke="#D8C4AE",
       strokeWidth=4, cap="round")
d.path("M242,222 L246,196", "Minute hand", fill=NONE, stroke="#D8C4AE",
       strokeWidth=3, cap="round", opacity=90)
d.shape("ellipse", "Clock pin", x=238, y=218, width=8, height=8,
        fill="#C9A24C", stroke=NONE)

# --- framed certificate on the wall, hung straight, believed by no one ---------------
d.path(rot_rect_path(560, 252, 150, 104, 2), "Certificate frame",
       fill="#241A1A", stroke="#7A5E52", strokeWidth=4, join="round")
d.path(rot_rect_path(560, 252, 128, 84, 2), "Certificate",
       fill="#CBBB98", stroke=NONE, opacity=92)
for i, y in enumerate([232, 244, 256]):
    d.path(f"M516,{y} L604,{y}", f"Cert line {i+1}", fill=NONE,
           stroke="#8A7460", strokeWidth=2.5, opacity=70)
d.shape("ellipse", "Cert seal", x=580, y=262, width=18, height=18,
        fill=WAX_GRAD, stroke=INK, strokeWidth=2, opacity=85)

# --- the mascot: amber clerk behind the desk --------------------------------------
d.shape("ellipse", "Body shadow", x=590, y=682, width=200, height=22,
        fill="#080606", opacity=50, stroke=NONE)
d.path("M690,352 C788,352 838,440 836,548 C834,640 778,700 690,700 "
       "C602,700 546,640 544,548 C542,440 592,352 690,352 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# belly light + flank shade
d.shape("ellipse", "Belly light", x=610, y=520, width=160, height=140,
        fill="#F0D0A0", opacity=22, stroke=NONE)
d.path("M808,470 C822,540 812,616 778,664", "Flank shade", fill=NONE,
       stroke="#6E4E2E", strokeWidth=16, opacity=28, cap="round")
d.shape("ellipse", "Head sheen", x=600, y=376, width=180, height=60,
        fill="#FFFFFF", opacity=12, stroke=NONE)

# official little bowtie — the seal wears one too
d.path("M660,598 L632,584 L632,612 Z", "Bowtie L", fill="#4A3230",
       stroke=INK, strokeWidth=3, join="round")
d.path("M720,598 L748,584 L748,612 Z", "Bowtie R", fill="#4A3230",
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Bowtie knot", x=680, y=590, width=20, height=16,
        fill="#5A4038", stroke=INK, strokeWidth=3)

# the face: half-lidded, unnervingly calm about thresholds
for i, cx in enumerate([646, 726]):
    d.shape("ellipse", f"Eye {i+1}", x=cx - 13, y=452, width=26, height=26,
            fill="#241A18", stroke=NONE)
    d.shape("ellipse", f"Glint {i+1}", x=cx - 6, y=457, width=6, height=6,
            fill="#FFFFFF", opacity=85, stroke=NONE)
    d.path(f"M{cx-18},452 C{cx-8},442 {cx+8},442 {cx+18},452",
           f"Lid {i+1}", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# mouth: flat, a degree off level, technically not a frown
d.path("M650,516 C672,524 706,526 730,518", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")

# --- the desk ----------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=270, y=690, width=460, height=26,
        fill="#080606", opacity=55, stroke=NONE)
d.shape("rectangle", "Desk top", x=250, y=612, width=540, height=30,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5, radius=8)
d.shape("rectangle", "Desk front", x=268, y=642, width=504, height=60,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#3A2B24"}, {"offset": 1, "color": "#1E1412"}]}},
        stroke=INK, strokeWidth=5, radius=6)
d.path("M300,668 L430,668", "Drawer seam", fill=NONE, stroke="#161010",
       strokeWidth=3, opacity=70)
d.shape("ellipse", "Drawer pull", x=358, y=674, width=16, height=7,
        fill="#5A4438", stroke=NONE)

# --- the seal-press: arm + stamp + wax ----------------------------------------------
# the document on the desk, a second sheet accruing beneath it
d.path(rot_rect_path(438, 590, 252, 64, -7), "Under sheet",
       fill="#CBBB98", stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(418, 584, 252, 64, -3), "Document",
       fill=PAPER, stroke=INK, strokeWidth=3.5, join="round")
d.text("APPROVED", "Doc approved", x=312, y=560, size=13,
       font="Virelai Sans", color="#7E3630", justify="left")
d.text("WITH RESERVATIONS", "Doc caveats", x=312, y=576, size=8,
       font="Virelai Sans", color="#7E3630", justify="left")
for i, y in enumerate([594, 604]):
    d.path(f"M310,{y} L402,{y}", f"Doc line {i+1}", fill=NONE,
           stroke="#9A8870", strokeWidth=2.5, opacity=75)
# a previous impression, already stamped: the seal's whole opinion
d.path("M416,586 C416,578 432,577 433,585 C434,592 427,594 425,599",
       "Old seal mark", fill=NONE, stroke="#9A3630", strokeWidth=4,
       cap="round", opacity=80)
d.shape("ellipse", "Old seal dot", x=423, y=605, width=5, height=5,
        fill="#9A3630", opacity=80, stroke=NONE)

# cooling wax pool on the document's right half — scalloped pour
wax = "M486,584 "
pts = []
for k in range(12):
    a = k * 2 * math.pi / 12
    r = 46 + (7 if k % 2 == 0 else -2)
    pts.append((486 + r * math.cos(a), 592 + r * 0.62 * math.sin(a)))
wax = "M%.1f,%.1f " % pts[0]
for k in range(12):
    p = pts[k]; q = pts[(k + 1) % 12]
    wax += "Q%.1f,%.1f %.1f,%.1f " % ((p[0] + q[0]) / 2 + 6 * math.cos(k),
                                      (p[1] + q[1]) / 2 + 6 * math.sin(k),
                                      q[0], q[1])
d.path(wax + "Z", "Wax pool", fill=WAX_GRAD, stroke=INK, strokeWidth=4)
# gloss still wet on the upper rim, dull where it has set
d.path("M452,568 C468,556 504,556 520,570", "Wax gloss", fill=NONE,
       stroke="#F4B8A6", strokeWidth=5, opacity=60, cap="round")
# cooling wisps
d.path("M440,540 C434,526 446,516 440,502", "Wisp 1", fill=NONE,
       stroke="#D8C4AE", strokeWidth=3, opacity=35, cap="round")
d.path("M530,536 C538,522 526,512 532,498", "Wisp 2", fill=NONE,
       stroke="#D8C4AE", strokeWidth=3, opacity=30, cap="round")

# the stamp: brass head still buried in the wax, wood handle above
d.shape("ellipse", "Stamp base", x=452, y=566, width=68, height=30,
        fill=BRASS_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Stamp neck", x=468, y=520, width=36, height=52,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4, radius=10)
d.shape("ellipse", "Stamp grip", x=458, y=486, width=56, height=44,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Grip sheen", x=470, y=492, width=22, height=12,
        fill="#FFFFFF", opacity=18, stroke=NONE)

# the pressing arm: from the shoulder down onto the grip
d.path("M640,548 C596,545 556,532 518,520", "Arm", fill=NONE,
       stroke="#B4854C", strokeWidth=30, cap="round")
d.path("M646,532 C602,530 562,520 528,508", "Arm outline top", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M636,564 C596,560 558,548 524,536", "Arm outline bot", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# hand folded over the grip
d.shape("ellipse", "Hand", x=476, y=494, width=48, height=36,
        fill="#C2965C", stroke=INK, strokeWidth=5)
# the resting arm, hand flat on the desk edge
d.path("M780,560 C806,576 816,596 812,614", "Rest arm", fill=NONE,
       stroke="#B4854C", strokeWidth=24, cap="round")
d.shape("ellipse", "Rest hand", x=790, y=602, width=44, height=26,
        fill="#C2965C", stroke=INK, strokeWidth=4)

# --- plate-side motif: one cooling wax droplet that missed the page -------------------
d.shape("ellipse", "Stray wax", x=272, y=604, width=18, height=12,
        fill=WAX_GRAD, stroke=INK, strokeWidth=2.5, opacity=90)

# --- captions -------------------------------------------------------------------------
d.text("SEAL OF MAYBE ENOUGH", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#EDDCC6", justify="center")
r = d.text("PROVISIONAL ADEQUACY ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C9A98E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("299.seal-of-maybe-enough-V1R00")
