#!/usr/bin/env python3
"""Favorable Beige — mascot portrait V1R00.
A soft painter mid-stroke, rolling a warm inoffensive beige across a
dashboard that was still technically alarming. The rejected tones are
fanned in its other hand; the wet edge is the only honest line left.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Favorable Beige — Mascot Portrait", 1000, 1000)

INK = "#3A2C1E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14100E"}, {"offset": 1, "color": "#080606"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E4438"}, {"offset": 0.7, "color": "#2C261C"},
    {"offset": 1, "color": "#141008"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#322A20"}, {"offset": 1, "color": "#140F08"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#22303A"}, {"offset": 1, "color": "#0E161C"}]}}
BEIGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DAC9A8"}, {"offset": 1, "color": "#BFA87E"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFE0BC"}, {"offset": 0.7, "color": "#D2BC90"},
    {"offset": 1, "color": "#A89066"}]}}
BUCKET = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E6256"}, {"offset": 1, "color": "#3C342C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A89878", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0D4B8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4C4234", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A06",
       strokeWidth=4, opacity=70)
# drop cloth: a pale sheet already catching drips
d.path("M330,700 C420,690 580,690 700,700 L700,700 Z", "Drop cloth",
       fill="#C9BCA0", opacity=35, stroke=NONE)
d.shape("ellipse", "Drip 1", x=448, y=690, width=14, height=9,
        fill="#DAC9A8", opacity=55, stroke=NONE)
d.shape("ellipse", "Drip 2", x=592, y=694, width=10, height=7,
        fill="#DAC9A8", opacity=45, stroke=NONE)

# --- the dashboard --------------------------------------------------------------
d.shape("ellipse", "Screen shadow", x=215, y=560, width=580, height=26,
        fill="#060A08", opacity=45, stroke=NONE)
d.shape("rectangle", "Dashboard", x=220, y=168, width=560, height=400,
        fill=SCREEN, stroke=INK, strokeWidth=7, radius=16)
# status strip still showing through at the top edge
d.shape("rectangle", "Status strip", x=236, y=184, width=528, height=34,
        fill="#18222A", stroke=INK, strokeWidth=3, radius=6)
d.text("LIVE OPERATIONS FEED", "Feed label", x=250, y=206, size=13,
       font="Virelai Sans", color="#5E7A88", justify="left")
d.shape("ellipse", "Feed dot", x=738, y=192, width=12, height=12,
        fill="#C85448", stroke=NONE, opacity=85)
# faint grid the paint hasn't fully argued away
for x in (300, 380, 460, 540, 620, 700):
    d.path(f"M{x},228 L{x},548", "Grid v", fill=NONE, stroke="#2E3E48",
           strokeWidth=1.5, opacity=35)
for y in (288, 348, 408, 468, 528):
    d.path(f"M236,{y} L764,{y}", "Grid h", fill=NONE, stroke="#2E3E48",
           strokeWidth=1.5, opacity=35)
# the alarming truth, still visible where the roller hasn't reached
d.path("M240,520 C270,505 285,470 305,475 C330,482 335,430 358,432 "
       "C380,434 385,385 408,388 L408,548 L240,548 Z",
       "Alarm area", fill="#5A2E28", opacity=80, stroke=NONE)
d.path("M240,520 C270,505 285,470 305,475 C330,482 335,430 358,432 "
       "C380,434 385,385 408,388", "Alarm line", fill=NONE,
       stroke="#C85448", strokeWidth=6, cap="round")
d.path("M262,268 L288,312 L236,312 Z", "Warn triangle", fill=NONE,
       stroke="#C85448", strokeWidth=5, join="round", opacity=90)
d.path("M262,282 L262,296 M262,304 L262,306", "Warn mark", fill=NONE,
       stroke="#C85448", strokeWidth=5, cap="round", opacity=90)
# the beige advance: matte coats with a wet left edge
d.path("M400,228 L764,228 L764,548 L392,548 "
       "C404,480 386,420 398,352 C408,300 390,264 400,228 Z",
       "Beige coat", fill=BEIGE, stroke=NONE)
# wet edge sheen where the roller just passed
d.path("M392,548 C404,480 386,420 398,352 C408,300 390,264 400,228",
       "Wet edge", fill=NONE, stroke="#EFE2C4", strokeWidth=8,
       cap="round", opacity=55)
# roller passes: horizontal bands, each coat a little flatter
for i, (y, op) in enumerate([(258,20),(318,16),(378,12),(438,9),(498,7)]):
    d.shape("rectangle", f"Coat band {i+1}", x=400, y=y, width=364,
            height=44, fill="#EFE2C4", opacity=op, stroke=NONE)
# the committee-approved message, embossed in beige on beige
t = d.text("ALL CLEAR", "Screen gospel", x=470, y=296, size=26,
           font="Virelai Sans", color="#A8906A", justify="left")
if t and t.get("id"):
    d.cmd("object.setProps", "gospel hush", ids=[t["id"]], opacity=60)
# rejected tones, fanned — the dozens of shades that didn't make it
for i, (ang, col) in enumerate([(-24,"#B8A284"),(-12,"#C9B294"),
                                (0,"#D8C8A8"),(12,"#C4AE88"),(24,"#A8946E")]):
    d.path(rot_rect_path(710, 580, 40, 62, ang), f"Swatch {i+1}",
           fill=col, stroke=INK, strokeWidth=2.5, join="round", opacity=90)

# --- the mascot: mid-stroke, unbothered ---------------------------------------------
d.shape("ellipse", "Body shadow", x=470, y=668, width=240, height=28,
        fill="#0A0806", opacity=50, stroke=NONE)
# body
d.path("M570,372 C640,372 682,424 684,496 C686,568 668,622 650,668 "
       "L478,668 C458,616 444,560 448,494 C452,424 500,372 570,372 Z",
       "Body", fill=BODY, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body sheen", x=496, y=392, width=110, height=48,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# a painter's cap, beige of course
d.path("M514,382 C520,352 546,338 574,340 C600,342 620,356 624,378 "
       "C592,368 548,368 514,382 Z", "Cap", fill="#C4AE88",
       stroke=INK, strokeWidth=4, join="round")
d.path("M622,376 C640,374 652,380 656,390", "Cap brim", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")

# face: the satisfaction of a surface that says nothing
d.path("M512,462 C520,470 533,470 540,462", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M604,462 C611,470 624,470 631,462", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M544,500 C556,510 588,510 600,500", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Blush L", x=496, y=478, width=28, height=13,
        fill="#C09A72", opacity=40, stroke=NONE)
d.shape("ellipse", "Blush R", x=622, y=478, width=28, height=13,
        fill="#C09A72", opacity=40, stroke=NONE)
# a smudge of beige on the cheek — it has been at this a while
d.shape("ellipse", "Paint smudge", x=614, y=522, width=24, height=10,
        fill="#DAC9A8", opacity=70, stroke=NONE)

# --- left arm extended, roller pressed to the wet edge --------------------------------
d.path("M470,470 C436,452 414,430 406,404", "Arm L", fill=NONE,
       stroke=INK, strokeWidth=14, cap="round")
d.shape("ellipse", "Hand L", x=386, y=384, width=30, height=26,
        fill=BODY, stroke=INK, strokeWidth=4)
# roller: handle + frame + the loaded foam cylinder
d.path("M402,392 L382,356", "Roller handle", fill=NONE, stroke="#5A4E3C",
       strokeWidth=7, cap="round")
d.path("M382,356 L410,330", "Roller neck", fill=NONE, stroke="#7A6E58",
       strokeWidth=4, cap="round")
d.path(rot_rect_path(424, 322, 92, 34, -18), "Roller foam",
       fill=BEIGE, stroke=INK, strokeWidth=4)
# fresh paint bead under the roller
d.path("M398,344 C404,352 414,352 420,346", "Paint bead", fill=NONE,
       stroke="#EFE2C4", strokeWidth=4, cap="round", opacity=70)

# --- right arm down at the bucket ------------------------------------------------------
d.path("M676,560 C692,590 692,622 676,644", "Arm R", fill=NONE,
       stroke=INK, strokeWidth=14, cap="round")
d.shape("ellipse", "Hand R", x=662, y=632, width=28, height=22,
        fill=BODY, stroke=INK, strokeWidth=4)

# --- paint bucket on the floor ----------------------------------------------------------
d.shape("ellipse", "Bucket shadow", x=666, y=676, width=120, height=16,
        fill="#0A0806", opacity=50, stroke=NONE)
d.path("M690,608 L778,608 L768,678 L700,678 Z", "Bucket", fill=BUCKET,
       stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Paint surface", x=694, y=600, width=80, height=16,
        fill="#DAC9A8", stroke=INK, strokeWidth=3)
d.path("M690,608 C700,590 768,590 778,608", "Bucket rim", fill=NONE,
       stroke=INK, strokeWidth=4)
d.text("BEIGE", "Bucket label", x=712, y=650, size=15,
       font="Virelai Sans", color="#E4D6B4", justify="left")
# one drip escaping the rim — the only thing here with urgency
d.path("M782,614 C786,626 784,640 780,650", "Bucket drip", fill=NONE,
       stroke="#DAC9A8", strokeWidth=5, cap="round", opacity=80)

# --- captions ----------------------------------------------------------------------
d.text("FAVORABLE BEIGE", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E4CC", justify="center")
r = d.text("CUSTODIAN OF CALM SURFACES", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8B088", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("286.favorable-beige-V1R00")
