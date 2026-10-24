#!/usr/bin/env python3
"""rc-links.sh — The Chain Checker. Necropolis plate V1R00.
A long chain of links dragged across the crypt floor while a lamplighter
inspects each one — sound links left gleaming, dead links tagged with
small burial flags: 404. Every reference audited, every orphan mourned.
Iron links, lantern gold. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-Links — Necropolis Plate", 1000, 1000)

INK = "#141820"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10141E"}, {"offset": 1, "color": "#07090F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#424A5E"}, {"offset": 0.7, "color": "#262C3C"},
    {"offset": 1, "color": "#10131C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#222838"}, {"offset": 1, "color": "#0C0F16"}]}}
IRON = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A94A4"}, {"offset": 1, "color": "#48505E"}]}}
IRON_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5260"}, {"offset": 1, "color": "#272C38"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3F52"}, {"offset": 1, "color": "#1A1D2A"}]}}
FLAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFE8A0"}, {"offset": 1, "color": "#E89A40"}]}}
PANE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFD98A"}, {"offset": 1, "color": "#D88428"}]}}
FLAG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B8BCC8"}, {"offset": 1, "color": "#6E7484"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E7484", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCE8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E5668", opacity=35, stroke=NONE)

# --- crypt architecture: vault ribs + a far doorway ------------------------------
d.path("M500,150 L500,330", "Vault rib C", fill=NONE, stroke="#1C212E",
       strokeWidth=9, opacity=80)
d.path("M330,170 C350,240 390,290 430,330", "Vault rib L", fill=NONE,
       stroke="#1C212E", strokeWidth=8, opacity=70)
d.path("M670,170 C650,240 610,290 570,330", "Vault rib R", fill=NONE,
       stroke="#1C212E", strokeWidth=8, opacity=70)
# far doorway where the chain came from
d.path("M205,645 L205,440 C205,385 285,385 285,440 L285,645 Z", "Far door",
       fill="#0A0D14", stroke=INK, strokeWidth=5, join="round")
d.path("M205,440 C205,385 285,385 285,440", "Far door arch", fill=NONE,
       stroke="#3A4254", strokeWidth=6, opacity=80)
d.path("M195,645 L295,645 L289,662 L201,662 Z", "Door sill", fill="#2A3040",
       stroke=INK, strokeWidth=4, join="round")

# --- lantern glow pools ---------------------------------------------------------
d.shape("ellipse", "Lamplight", x=350, y=380, width=330, height=330,
        fill="#E8A850", opacity=11, stroke=NONE)
d.shape("ellipse", "Lamplight core", x=430, y=460, width=170, height=170,
        fill="#F0BC68", opacity=14, stroke=NONE)
d.shape("ellipse", "Floor light pool", x=350, y=630, width=380, height=80,
        fill="#D89240", opacity=12, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0C12",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Figure shadow", x=520, y=682, width=180, height=18,
        fill="#030408", opacity=55, stroke=NONE)
d.shape("ellipse", "Chain shadow", x=210, y=682, width=600, height=14,
        fill="#030408", opacity=40, stroke=NONE)

# --- the dragged chain, snaking across the floor ----------------------------------
# serpentine: links every ~26px, alternating flat / on-edge orientation
DEAD = {5, 19, 23}          # indices of broken links
GLEAM = {10, 11, 13, 14}    # sound links catching the lantern
chain_pts = []
for x in range(205, 815, 26):
    y = 662 + 22 * math.sin((x - 205) / 610 * math.pi * 2)
    chain_pts.append((x, y))
for i, (cx, cy) in enumerate(chain_pts):
    if i % 2 == 0:
        w, h = 24, 13
    else:
        w, h = 13, 22
    dead = i in DEAD
    d.shape("ellipse", f"Link {i+1}", x=cx - w/2, y=cy - h/2, width=w,
            height=h, fill=NONE,
            stroke=(IRON_DK["gradient"]["stops"][1]["color"] if dead
                    else "#78828F"),
            strokeWidth=(7 if i % 2 == 0 else 6), opacity=(55 if dead else 95))
    if dead:
        # crack through the link
        d.path(f"M{cx-5},{cy-10} L{cx},{cy} L{cx+4},{cy+10}", f"Crack {i+1}",
               fill=NONE, stroke="#0A0C12", strokeWidth=6, cap="round",
               join="round")
    elif i in GLEAM:
        d.path(f"M{cx-w/2+2},{cy-2} L{cx-w/2+8},{cy-4}", f"Gleam {i+1}",
               fill=NONE, stroke="#F4E2A8", strokeWidth=3, opacity=75,
               cap="round")

# --- burial flags on the dead links ------------------------------------------------
for i, (fx, fy, tip) in enumerate([
        (chain_pts[5][0], chain_pts[5][1], -1),
        (chain_pts[19][0], chain_pts[19][1], 1),
        (chain_pts[23][0], chain_pts[23][1], -1)]):
    top = fy - 64
    d.path(f"M{fx},{fy-6} L{fx},{top}", f"Flag stick {i+1}", fill=NONE,
           stroke="#3A3020", strokeWidth=4, cap="round")
    d.path(f"M{fx},{top} L{fx + 46*tip},{top + 12} L{fx},{top + 24} Z",
           f"Flag {i+1}", fill=FLAG, stroke=INK, strokeWidth=3, join="round")
    d.text("404", f"Flag text {i+1}", x=fx + 22*tip, y=top + 20, size=10,
           font="Source Sans 3", color="#1E1410", justify="center")
# scattered fragments by the second dead link
fx2, fy2 = chain_pts[19]
for i, (dx, dy, a) in enumerate([(-30, 14, 0), (34, 10, 1), (-18, 22, 0)]):
    d.path(f"M{fx2+dx-8},{fy2+dy} C{fx2+dx-4},{fy2+dy-6} {fx2+dx+4},{fy2+dy-6} "
           f"{fx2+dx+8},{fy2+dy}", f"Fragment {i+1}", fill=NONE,
           stroke="#4A5260", strokeWidth=4, opacity=80, cap="round")

# --- the lamplighter, bent over the chain --------------------------------------------
# robe: shoulders hunched, hem trailing to the floor
d.path("M585,470 C545,478 528,520 530,570 C532,620 540,660 545,690 "
       "L660,690 C662,640 660,580 648,535 C640,505 622,478 605,470 Z",
       "Robe", fill=ROBE, stroke=INK, strokeWidth=5, join="round")
# hood + dark face + ember eyes
d.path("M572,472 C572,432 634,432 634,472 C634,494 624,506 603,506 "
       "C582,506 572,494 572,472 Z", "Hood", fill=ROBE, stroke=INK,
       strokeWidth=5, join="round")
d.path("M582,474 C582,446 624,446 624,474 C624,492 616,498 603,498 "
       "C590,498 582,492 582,474 Z", "Face", fill="#0B0D14", stroke=NONE)
for i, ex in enumerate([596, 612]):
    d.shape("ellipse", f"Eye {i+1}", x=ex-3, y=470, width=6, height=6,
            fill="#E8A850", stroke=NONE, opacity=95)
# hem folds
d.path("M560,560 C566,600 566,650 564,685 M625,560 C622,610 624,655 626,685",
       "Robe folds", fill=NONE, stroke="#12141E", strokeWidth=4, opacity=70)

# left arm reaching down to the held link
d.path("M560,540 C540,570 528,600 522,634", "Arm reach", fill=NONE,
       stroke="#4A5066", strokeWidth=13, cap="round")
d.shape("ellipse", "Hand", x=512, y=626, width=20, height=18,
        fill="#B9BCC8", stroke=INK, strokeWidth=3)
# the held link, tilted in his hand
d.shape("ellipse", "Held link", x=505, y=636, width=26, height=15,
        fill=NONE, stroke="#98A2B0", strokeWidth=7)

# right arm holding the lantern low
d.path("M630,520 C612,545 588,565 556,578", "Arm lantern", fill=NONE,
       stroke="#3A3F52", strokeWidth=13, cap="round")
# lantern: cap, glowing panes, base, ring
d.shape("ellipse", "Lantern ring", x=540, y=566, width=16, height=14,
        fill=NONE, stroke="#8A94A4", strokeWidth=4)
d.path("M538,584 L572,584 L576,600 L534,600 Z", "Lantern cap", fill=IRON_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M538,600 L572,600 L568,640 L542,640 Z", "Lantern panes", fill=PANE,
       stroke=INK, strokeWidth=3, join="round")
d.path("M544,602 L544,638 M560,602 L560,638", "Pane bars", fill=NONE,
       stroke="#2A2018", strokeWidth=3)
d.path("M555,634 C550,622 552,612 555,606 C558,612 560,622 555,634 Z",
       "Lantern flame", fill=FLAME, stroke=NONE)
d.path("M534,640 L576,640 L572,650 L538,650 Z", "Lantern base", fill=IRON_DK,
       stroke=INK, strokeWidth=3, join="round")

# a few sound links glinting extra in the light pool
for i, (gx, gy) in enumerate([(452, 656), (486, 668)]):
    d.path(f"M{gx},{gy} L{gx+5},{gy-6} M{gx+7},{gy-1} L{gx+9},{gy-8}",
           f"Glint {i+1}", fill=NONE, stroke="#FFE8A0", strokeWidth=2,
           opacity=70, cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-LINKS", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#DEE2EC", justify="center")
r = d.text("DEAD LINK CORONER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA2B8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-links-V1R00")
