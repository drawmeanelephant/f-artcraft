#!/usr/bin/env python3
"""Htaccessius The Doorman — mascot portrait V1R00.
The ceremonial access guardian at the server gate, cap and braided coat,
reading a scroll labeled .HTACCESS by the light of the gate lantern.
He is precise. If you are blocked, it is because you should be. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Htaccessius The Doorman — Mascot Portrait", 1000, 1000)

INK = "#1E1A24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101620"}, {"offset": 1, "color": "#0C1018"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6678"}, {"offset": 0.7, "color": "#40485A"},
    {"offset": 1, "color": "#1E2430"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3E4C"}, {"offset": 1, "color": "#181C24"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5878"}, {"offset": 0.72, "color": "#38445E"},
    {"offset": 1, "color": "#232A3C"}]}}
GATE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4252"}, {"offset": 1, "color": "#1C2230"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2B45E"}, {"offset": 0.55, "color": "#8A6242"},
    {"offset": 1, "color": "#3A3242"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F8D68A"}, {"offset": 0.55, "color": "#EEA94E"},
    {"offset": 1, "color": "#C87A32"}]}}
PAPER = "#E8D8AE"
BRASS = "#C9A85E"
AMBER = "#F0B45C"

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#78829A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCD4E4", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,234,8),(806,232,7),(158,520,9),(838,544,8),
                               (252,764,7),(750,750,9),(134,392,6),(864,394,7),
                               (394,112,7),(612,112,8),(334,822,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#464E5E", opacity=45, stroke=NONE)

# --- the lanternlight: it reaches the scroll and stops there ---------------------------
d.shape("ellipse", "Lantern glow", x=330, y=170, width=460, height=400,
        fill=GLOW, opacity=70, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E1218",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Glow pool", x=420, y=676, width=320, height=40,
        fill=AMBER, opacity=20, stroke=NONE)

# --- the server gate ---------------------------------------------------------------------
d.shape("ellipse", "Gate shadow", x=170, y=686, width=270, height=22,
        fill="#0A0E14", opacity=45, stroke=NONE)
# gate posts
d.path("M176,232 L176,700 L212,700 L212,232 Z", "Post L", fill=GATE_GRAD,
       stroke=INK, strokeWidth=5, join="round")
d.path("M392,232 L392,700 L428,700 L428,232 Z", "Post R", fill=GATE_GRAD,
       stroke=INK, strokeWidth=5, join="round")
# lintel across the posts
d.path("M164,196 L440,196 L440,240 L164,240 Z", "Lintel", fill=GATE_GRAD,
       stroke=INK, strokeWidth=5, join="round")
d.path("M176,208 L428,208", "Lintel seam", fill=NONE, stroke="#4E5A6E",
       strokeWidth=3, opacity=70)
# the dark beyond, held back by bars
d.path("M212,240 L392,240 L392,700 L212,700 Z", "Gate dark",
       fill="#0C1018", stroke=NONE)
for i, gx in enumerate([236, 268, 300, 332, 364]):
    d.path(f"M{gx},252 L{gx},696", f"Bar {i+1}", fill=NONE,
           stroke="#2E3646", strokeWidth=9)
    d.path(f"M{gx+3},252 L{gx+3},696", f"Bar hi {i+1}", fill=NONE,
           stroke="#5A6678", strokeWidth=2, opacity=50)
# portcullis chains at the top of the dark
for i, cy in enumerate([260, 276]):
    d.path(f"M216,{cy} L388,{cy+4}", f"Chain {i+1}", fill=NONE,
           stroke="#3A4250", strokeWidth=6, cap="round")
# the server LEDs on the left post: some allow, mostly deny
for i, (ly, lc) in enumerate([(300, "#7EC48A"), (330, "#C46A5A"),
                              (360, "#C4A85E"), (390, "#C46A5A"),
                              (420, "#4A5464"), (450, "#C46A5A")]):
    d.shape("ellipse", f"LED {i+1}", x=184, y=ly, width=12, height=12,
            fill=lc, stroke=INK, strokeWidth=2.5, opacity=90)
# small plate on the lintel
d.shape("rectangle", "Gate plate", x=246, y=200, width=112, height=30,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=3)
d.text("GATE", "Gate label", x=302, y=221, size=16, font="Virelai Sans",
       color="#33260F", justify="center")

# --- the lantern on the right post --------------------------------------------------------
d.path("M428,266 L472,266 L472,278", "Lantern bracket", fill=NONE,
       stroke="#2A3242", strokeWidth=7, cap="round")
d.path("M460,278 L460,290", "Lantern hook", fill=NONE, stroke="#2A3242",
       strokeWidth=5, cap="round")
# housing
d.path("M440,292 L480,292 L486,308 L434,308 Z", "Lantern cap", fill="#3A3242",
       stroke=INK, strokeWidth=4, join="round")
d.path("M436,308 L484,308 L478,368 L442,368 Z", "Lantern glass", fill=GLASS,
       stroke=INK, strokeWidth=4, join="round", opacity=92)
d.path("M448,308 L444,368 M460,308 L460,368 M472,308 L476,368",
       "Lantern ribs", fill=NONE, stroke="#4A3C30", strokeWidth=3, opacity=70)
# the flame inside
d.path("M460,352 C450,342 450,330 460,318 C470,330 470,342 460,352 Z",
       "Flame", fill="#FFF0C0", stroke="#E8A850", strokeWidth=2.5)
d.path("M434,368 L486,368 L480,382 L440,382 Z", "Lantern base",
       fill="#3A3242", stroke=INK, strokeWidth=4, join="round")
# light spill down the gate's edge
d.path("M434,382 C440,440 440,520 434,600", "Light spill", fill=NONE,
       stroke=AMBER, strokeWidth=10, opacity=18, cap="round")

# --- Htaccessius: grim, resolute, on shift -------------------------------------------------
d.shape("ellipse", "Doorman shadow", x=470, y=686, width=250, height=24,
        fill="#0A0E14", opacity=45, stroke=NONE)
# the coat: a long navy bell, hem to the floor
d.path("M580,392 C656,392 698,452 702,548 C704,620 700,664 694,700 "
       "L452,700 C446,664 442,620 446,548 C452,452 504,392 580,392 Z",
       "Coat", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Coat hi", x=498, y=424, width=96, height=44,
        fill="#FFFFFF", opacity=10, stroke=NONE)
# braided frogging down the front
d.path("M580,452 L580,684", "Coat seam", fill=NONE, stroke="#2A3244",
       strokeWidth=4, opacity=80)
for i, by in enumerate([480, 528, 576, 624]):
    d.path(f"M560,{by} C570,{by+8} 590,{by+8} 600,{by} M560,{by} L560,{by+10} "
           f"M600,{by} L600,{by+10}", f"Frog {i+1}", fill=NONE,
           stroke=BRASS, strokeWidth=4, opacity=90)
    d.shape("ellipse", f"Frog button {i+1}", x=574, y=by-2, width=11,
            height=11, fill=BRASS, stroke=INK, strokeWidth=2)
# epaulettes, earned the hard way
for lbl, ex in [("Epaulette L", 452), ("Epaulette R", 660)]:
    d.shape("ellipse", lbl, x=ex, y=400, width=54, height=26,
            fill=BRASS, stroke=INK, strokeWidth=4)
    for k in range(3):
        d.path(f"M{ex+12+k*14},{424} L{ex+10+k*14},{436}", f"{lbl} fringe {k+1}",
               fill=NONE, stroke=BRASS, strokeWidth=4, cap="round")
# the peaked cap
d.path("M500,388 C500,342 534,320 580,320 C626,320 660,342 660,388 "
       "C640,372 612,364 580,364 C548,364 520,372 500,388 Z",
       "Cap crown", fill="#2E3850", stroke=INK, strokeWidth=5, join="round")
d.path("M500,388 C530,372 630,372 660,388 L660,400 C630,384 530,384 500,400 Z",
       "Cap band", fill=BRASS, stroke=INK, strokeWidth=4, join="round")
d.path("M498,398 C540,382 620,382 662,398 C662,412 646,418 630,414 "
       "C600,406 560,406 530,414 C514,418 498,412 498,398 Z",
       "Cap brim", fill="#232A3C", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Cap badge", x=572, y=330, width=16, height=20,
        fill=BRASS, stroke=INK, strokeWidth=2.5)

# face: half-lidded, precise, unreadable
d.shape("ellipse", "Eye L", x=524, y=452, width=26, height=22,
        fill=INK, stroke=NONE)
d.path("M520,446 C530,438 544,438 552,444", "Lid L", fill=NONE,
       stroke="#232A3C", strokeWidth=7, cap="round")
d.shape("ellipse", "Eye R", x=608, y=452, width=26, height=22,
        fill=INK, stroke=NONE)
d.path("M604,444 C614,438 628,438 638,446", "Lid R", fill=NONE,
       stroke="#232A3C", strokeWidth=7, cap="round")
# the flat mouth of irreversible judgment
d.path("M550,512 C566,516 594,516 610,512", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.shape("ellipse", "Cheek L", x=508, y=492, width=26, height=13,
        fill="#4A5470", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=626, y=492, width=26, height=13,
        fill="#4A5470", opacity=45, stroke=NONE)
# lantern light catching the left side of the coat
d.path("M452,470 C448,540 448,610 456,668", "Rim light", fill=NONE,
       stroke=AMBER, strokeWidth=7, opacity=35, cap="round")

# --- the scroll: .HTACCESS, read and enforced ----------------------------------------------
# held open at chest height, catching the light
d.path("M470,540 L688,528 L692,608 L474,620 Z", "Scroll leaf", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
# curled ends
d.shape("ellipse", "Scroll curl L", x=456, y=534, width=30, height=92,
        fill="#D8C79A", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Scroll curl R", x=676, y=522, width=30, height=92,
        fill="#D8C79A", stroke=INK, strokeWidth=4)
d.text(".HTACCESS", "Scroll title", x=581, y=570, size=26,
       font="Virelai Sans", color="#3E2E18", justify="center")
# directive lines, kept vague — the details are for him
d.path("M502,588 L560,585 M502,598 L586,594 M602,584 L656,581 M596,594 L660,591",
       "Directive lines", fill=NONE, stroke="#A89468", strokeWidth=3,
       opacity=85)
# both hands on the scroll edges
d.path("M478,560 C470,586 472,606 480,616", "Hand L hint", fill=NONE,
       stroke="#38445E", strokeWidth=18, cap="round")
d.shape("ellipse", "Hand L", x=456, y=560, width=34, height=26,
        fill="#4A5878", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=668, y=548, width=34, height=26,
        fill="#4A5878", stroke=INK, strokeWidth=4)

# --- captions ---------------------------------------------------------------------------
d.text("HTACCESSIUS THE DOORMAN", "Name", x=500, y=930, size=44,
       font="Virelai Sans", color="#D8DCE8", justify="center")
r = d.text("DIRECTIVE GATEKEEPER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8B0C4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("403.htaccessius-the-doorman-V1R00")
