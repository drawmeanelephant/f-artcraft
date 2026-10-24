#!/usr/bin/env python3
"""Peppy Clerk — mascot portrait V1R00.
A containment clerk in a green eyeshade visor, badge pinned on, standing
beside Bin 8C with one hand on the lid; a hazardous request half-shut
inside, a stool nearby. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Peppy Clerk — Mascot Portrait", 1000, 1000)

INK = "#2E2620"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A2024"}, {"offset": 1, "color": "#10181A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7E8E7C"}, {"offset": 0.7, "color": "#56685C"},
    {"offset": 1, "color": "#26302C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4A42"}, {"offset": 1, "color": "#1A221E"}]}}
CLERK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2B49A"}, {"offset": 0.72, "color": "#9A8A72"},
    {"offset": 1, "color": "#665C4C"}]}}
BIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E909A"}, {"offset": 1, "color": "#42525A"}]}}
LID_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#96A6AE"}, {"offset": 1, "color": "#566670"}]}}
BRASS = "#C9B06A"
PAPER = "#EDE3C8"
WARN = "#C8624E"

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A9C8E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4D6", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,234,8),(806,232,7),(158,520,9),(838,544,8),
                               (252,764,7),(750,750,9),(134,392,6),(864,394,7),
                               (394,112,7),(612,112,8),(334,822,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E6058", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#121A16",
       strokeWidth=4, opacity=70)

# --- Bin 8C: the archive's hazardous mouth, kept shut ---------------------------------
d.shape("ellipse", "Bin shadow", x=540, y=682, width=260, height=26,
        fill="#0E1412", opacity=45, stroke=NONE)
# body: tapering steel bin
d.path("M576,446 L784,446 L768,700 L592,700 Z", "Bin body",
       fill=BIN_GRAD, stroke=INK, strokeWidth=6, join="round")
# corrugation ridges
for i, bx in enumerate([620, 660, 700, 740]):
    d.path(f"M{bx},470 L{bx-4},688", f"Ridge {i+1}", fill=NONE,
           stroke="#2E3C42", strokeWidth=5, opacity=55)
    d.path(f"M{bx+4},470 L{bx},688", f"Ridge hi {i+1}", fill=NONE,
           stroke="#A8B8BE", strokeWidth=2.5, opacity=40)
# bin sheen
d.path("M596,470 L590,680", "Bin sheen", fill=NONE, stroke="#C4D2D6",
       strokeWidth=10, opacity=20, cap="round")
# placard: digits need Source Sans 3 — Virelai has no digit glyphs
d.shape("rectangle", "Placard", x=648, y=540, width=96, height=60,
        fill=BRASS, stroke=INK, strokeWidth=5, radius=6)
d.text("8C", "Placard text", x=696, y=583, size=38, font="Source Sans 3",
       color="#3E3420", justify="center")
d.shape("ellipse", "Placard rivet L", x=656, y=564, width=8, height=8,
        fill="#7A6428", stroke=NONE)
d.shape("ellipse", "Placard rivet R", x=728, y=564, width=8, height=8,
        fill="#7A6428", stroke=NONE)
# side handles
for lbl, hy in [("Handle L", 566), ("Handle R", 782)]:
    d.path(f"M{hy},520 C{hy-14 if lbl=='Handle L' else hy+14},520 "
           f"{hy-14 if lbl=='Handle L' else hy+14},548 {hy},548",
           lbl, fill=NONE, stroke="#3A464C", strokeWidth=8, cap="round")
# lid: sits on the bin, holding everything down
d.path("M556,414 C556,398 572,388 596,388 L764,388 C788,388 804,398 804,414 "
       "L804,434 C804,446 792,452 780,452 L580,452 C568,452 556,446 556,434 Z",
       "Bin lid", fill=LID_GRAD, stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "Lid sheen", x=596, y=396, width=140, height=16,
        fill="#DCE6EA", opacity=35, stroke=NONE)
# lid knob
d.shape("ellipse", "Lid knob", x=668, y=368, width=26, height=24,
        fill="#4A5A62", stroke=INK, strokeWidth=4)
# the request halfway in: a form jammed under the lid's front edge,
# its hazard-striped tail still hanging out
d.path("M688,446 L688,512 C694,522 708,522 714,514 C720,522 734,522 740,512 "
       "L740,446 Z", "Trapped form", fill=PAPER, stroke=INK, strokeWidth=4,
       join="round")
d.path("M696,462 L732,462 M696,474 L730,474", "Form lines", fill=NONE,
       stroke="#9A8A66", strokeWidth=3, opacity=80)
d.path("M688,494 L740,494 L740,512 C734,522 720,522 714,514 C708,522 694,522 "
       "688,512 Z", "Hazard corner", fill=WARN, stroke=NONE, opacity=85)
# and a folded corner of it still peeking over the lid near the clerk's hand
d.path("M566,452 L566,398 C566,384 578,376 592,380 C604,374 618,382 618,396 "
       "L618,452 Z", "Form over lid", fill=PAPER, stroke=INK, strokeWidth=4,
       join="round")
d.path("M576,398 L608,398 M576,410 L606,410", "Lid form lines", fill=NONE,
       stroke="#9A8A66", strokeWidth=2.5, opacity=80)

# --- the stool, waiting nearby --------------------------------------------------------
d.shape("ellipse", "Stool shadow", x=176, y=684, width=140, height=20,
        fill="#0E1412", opacity=40, stroke=NONE)
d.shape("ellipse", "Seat", x=192, y=592, width=116, height=34,
        fill=BRASS, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Seat top", x=196, y=584, width=108, height=30,
        fill="#DCC180", stroke=INK, strokeWidth=4)
for lbl, pts in [("Leg L", "M214,616 L204,690"), ("Leg mid", "M250,620 L250,692"),
                 ("Leg R", "M288,616 L298,690")]:
    d.path(pts, lbl, fill=NONE, stroke="#8A7240", strokeWidth=10, cap="round")
d.path("M210,662 L292,662", "Leg brace", fill=NONE, stroke="#8A7240",
       strokeWidth=6, cap="round")

# --- Peppy Clerk: standing, hand on the lid ---------------------------------------------
d.shape("ellipse", "Clerk shadow", x=280, y=686, width=230, height=24,
        fill="#0E1412", opacity=45, stroke=NONE)
# body: upright clerk bell, leaning slightly toward the bin
d.path("M400,392 C478,392 522,452 528,548 C532,632 522,680 508,700 "
       "L292,700 C278,680 268,632 272,548 C278,452 322,392 400,392 Z",
       "Clerk body", fill=CLERK_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=316, y=430, width=96, height=44,
        fill="#FFFFFF", opacity=14, stroke=NONE)
# cardigan seam + buttons
d.path("M400,516 L400,668", "Cardigan seam", fill=NONE, stroke="#6E6048",
       strokeWidth=4, opacity=70)
for i, by in enumerate([540, 580, 620]):
    d.shape("ellipse", f"Button {i+1}", x=394, y=by, width=11, height=11,
            fill=BRASS, stroke=INK, strokeWidth=2)
# feet
for lbl, fx in [("Foot L", 296), ("Foot R", 452)]:
    d.shape("ellipse", lbl, x=fx, y=684, width=64, height=26,
            fill="#8A7A5E", stroke=INK, strokeWidth=4)

# right arm: reaches to the lid, palm flat on it — shutting is the whole job
d.path("M510,500 C548,478 574,452 592,430", "Arm R", fill=NONE,
       stroke="#9A8A72", strokeWidth=20, cap="round")
d.path("M588,442 C586,428 598,420 614,422 C630,420 640,430 638,442 "
       "C636,452 624,456 612,455 C598,456 590,452 588,442 Z",
       "Palm R", fill="#C2B49A", stroke=INK, strokeWidth=4)
# left arm: relaxed at the side, holding a folded docket
d.path("M296,512 C270,548 264,592 274,626", "Arm L", fill=NONE,
       stroke="#9A8A72", strokeWidth=20, cap="round")
d.path("M262,600 L310,592 L316,634 L268,642 Z", "Docket", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
d.path("M272,610 L304,605 M274,620 L306,615", "Docket lines", fill=NONE,
       stroke="#9A8A66", strokeWidth=2.5, opacity=80)
d.shape("ellipse", "Palm L", x=264, y=620, width=28, height=20,
        fill="#C2B49A", stroke=INK, strokeWidth=4)

# the badge: archivally asserted, pinned at chest height
d.path("M346,528 L346,552", "Badge clip", fill=NONE, stroke="#6E6048",
       strokeWidth=5, cap="round")
d.shape("rectangle", "Badge", x=324, y=550, width=46, height=58,
        fill=PAPER, stroke=INK, strokeWidth=4, radius=5)
d.shape("rectangle", "Badge photo", x=332, y=560, width=30, height=22,
        fill="#8FA89C", stroke=INK, strokeWidth=2.5, radius=3)
d.path("M338,570 C342,564 352,564 356,570", "Badge face", fill=NONE,
       stroke=INK, strokeWidth=2.5, cap="round")
d.shape("ellipse", "Badge eye L", x=340, y=566, width=4, height=4,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Badge eye R", x=352, y=566, width=4, height=4,
        fill=INK, stroke=NONE)
d.path("M332,592 L362,592 M332,599 L356,599", "Badge lines", fill=NONE,
       stroke="#9A8A66", strokeWidth=3, opacity=80)

# face: eyes up, the cheer of a clerk who has already decided
d.shape("ellipse", "Eye L", x=352, y=452, width=26, height=26,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye L glint", x=358, y=456, width=8, height=8,
        fill="#FFFFFF", stroke=NONE)
d.shape("ellipse", "Eye R", x=424, y=452, width=26, height=26,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R glint", x=430, y=456, width=8, height=8,
        fill="#FFFFFF", stroke=NONE)
d.path("M374,512 C386,524 414,524 426,512", "Smile", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.shape("ellipse", "Cheek L", x=336, y=494, width=26, height=13,
        fill="#A89078", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=438, y=494, width=26, height=13,
        fill="#A89078", opacity=45, stroke=NONE)

# the green eyeshade: peppy is a working clerk, not a decorative one
d.path("M336,436 C350,414 380,404 402,404 C424,404 452,414 466,436 "
       "C452,428 424,422 402,422 C380,422 352,428 336,436 Z",
       "Visor band", fill="#4E6E50", stroke=INK, strokeWidth=4, join="round")
d.path("M330,438 C360,424 440,424 472,438 C472,448 466,452 456,450 "
       "C424,440 378,440 346,450 C336,452 330,448 330,438 Z",
       "Visor brim", fill="#5E8262", stroke=INK, strokeWidth=4,
       join="round", opacity=88)
d.path("M348,432 C372,424 430,424 454,432", "Visor sheen", fill=NONE,
       stroke="#A8C4A0", strokeWidth=3, opacity=60, cap="round")

# --- captions ---------------------------------------------------------------------------
d.text("PEPPY CLERK", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E2EAD9", justify="center")
r = d.text("CONTAINMENT CLERK, BIN EIGHT-C", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B2C4B0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("325.peppy-clerk-V1R00")
