#!/usr/bin/env python3
"""Lilt Protocol — mascot portrait V1R00.
The phonetic filter mid-certification: singing over the document stack,
pen held above the signature line. What leaves is still true — merely true
in a way that can be hummed. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lilt Protocol — Mascot Portrait", 1000, 1000)

INK = "#1C2230"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101A26"}, {"offset": 1, "color": "#0A0F18"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4E6E74"}, {"offset": 0.7, "color": "#2E4A50"},
    {"offset": 1, "color": "#1A2C30"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E8D4"}, {"offset": 0.72, "color": "#CFC3A6"},
    {"offset": 1, "color": "#A2947A"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EBD6"}, {"offset": 1, "color": "#CFC2A2"}]}}
NOTE = "#7AC8BC"
RED = "#A4463E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8288", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BFE0DA", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(204,242,8),(794,236,7),(166,538,9),(832,554,8),
                               (254,762,7),(748,750,9),(146,400,6),(854,398,7),
                               (400,118,7),(606,116,8),(340,820,6),(662,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A5A5E", opacity=45, stroke=NONE)

# --- the document stack: pages fed through flat ---------------------------------
# pile shadow + fanned sheets, each a hair off-square
d.shape("ellipse", "Stack shadow", x=280, y=760, width=440, height=40,
        fill="#0C1218", opacity=55, stroke=NONE)
for i, (rot, ox, oy) in enumerate([(-9, -16, 34), (6, 10, 26), (-4, -8, 18),
                                   (3, 6, 10), (-2, -2, 4)]):
    t = math.radians(rot); c, s = math.cos(t), math.sin(t)
    cx, cy = 500 + ox, 700 + oy
    w, h = 380, 96
    pts = []
    for dx, dy in [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]:
        pts.append((cx + dx*c - dy*s, cy + dx*s + dy*c))
    pd = f"M{pts[0][0]:.0f},{pts[0][1]:.0f} " + \
         " ".join(f"L{x:.0f},{y:.0f}" for x, y in pts[1:]) + " Z"
    d.path(pd, f"Sheet {i+1}", fill=PAGE_GRAD, stroke=INK,
           strokeWidth=3.5, join="round")

# --- top document: the page mid-scan ---------------------------------------------
d.path("M330,600 L664,586 L676,764 L342,778 Z", "Top sheet",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=4.5, join="round")
# text lines that scan perfectly
for i, y in enumerate([622, 644, 666, 688]):
    d.path(f"M356,{y} L640,{y - 8}", f"Scan line {i+1}", fill=NONE,
           stroke="#8A8272", strokeWidth=2.5, cap="round", opacity=75)
# the signature line: red rule, waiting where the pen hovers
d.path("M558,704 L666,698", "Signature line", fill=NONE, stroke=RED,
       strokeWidth=3.5, cap="round")
d.path("M540,694 L556,710 M556,694 L540,710", "Sign X", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# --- the reject tray: sentences that will not scan --------------------------------
d.path("M212,700 L320,692 L330,742 L222,750 Z", "Reject tray",
       fill="#3A4A52", stroke=INK, strokeWidth=4, join="round")
for i, (ox, oy) in enumerate([(0, -6), (4, -12), (-2, -18)]):
    d.path(f"M{226+ox},{696+oy} L{312+ox},{690+oy} L{316+ox},{706+oy} "
           f"L{230+ox},{712+oy} Z", f"Reject page {i+1}",
           fill=PAGE_GRAD, stroke=INK, strokeWidth=3, join="round",
           opacity=95)
t = d.text("ARRHYTHMIC", "Tray label", x=272, y=736, size=12,
           font="Virelai Sans", color="#D9CBA8", justify="center")

# --- the protocol itself: a soft mass of cadence ----------------------------------
# body: a rounded hum behind the stack
d.path("M412,640 C400,540 420,430 500,424 C580,430 600,540 588,640 "
       "C560,656 440,656 412,640 Z", "Body", fill=BODY_GRAD,
       stroke=INK, strokeWidth=5, join="round")
# lapel shadow of accumulated filings
d.shape("ellipse", "Body shade", x=430, y=560, width=140, height=70,
        fill="#A2947A", opacity=30, stroke=NONE)
# the open mouth, mid-resolution-tone
d.shape("ellipse", "Mouth", x=476, y=478, width=48, height=58,
        fill="#3A2024", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Mouth depth", x=486, y=500, width=28, height=26,
        fill="#241014", stroke=NONE)
# closed eyes, contented in the listening posture
d.path("M448,456 C456,448 468,448 474,456", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M526,456 C534,448 546,448 552,456", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# brows lifted, hearing the meter
d.path("M446,442 C456,436 470,436 478,442", "Brow L", fill=NONE,
       stroke="#7A6E58", strokeWidth=3, cap="round")
d.path("M522,442 C532,436 546,436 554,442", "Brow R", fill=NONE,
       stroke="#7A6E58", strokeWidth=3, cap="round")
# a small bow tie: certification formalwear
d.path("M486,556 L470,546 L470,566 Z M514,556 L530,546 L530,566 Z "
       "M486,556 L514,556", "Bow tie", fill="#5E8A86", stroke=INK,
       strokeWidth=3, join="round")

# --- resolution-tone: the audible approval ----------------------------------------
for i, rr in enumerate([64, 92, 120]):
    d.path(f"M{500 - rr},{500 + int(rr*0.12)} "
           f"A{rr},{rr} 0 0 1 {500 + rr},{500 + int(rr*0.12)}",
           f"Tone ring {i+1}", fill=NONE, stroke=NOTE,
           strokeWidth=3.5, opacity=40 - i * 10, cap="round")

# --- left arm conducting the line ------------------------------------------------
d.path("M428,560 C396,540 372,520 356,496", "Sleeve conduct",
       fill=NONE, stroke="#CFC3A6", strokeWidth=22, cap="round")
d.shape("ellipse", "Conduct hand", x=340, y=478, width=30, height=26,
        fill="#F0E8D4", stroke=INK, strokeWidth=4)

# --- right arm out to the page: the pen above the signature ------------------------
d.path("M580,560 C616,586 632,616 634,640", "Sleeve pen", fill=NONE,
       stroke="#CFC3A6", strokeWidth=22, cap="round")
d.shape("ellipse", "Pen hand", x=620, y=626, width=32, height=28,
        fill="#F0E8D4", stroke=INK, strokeWidth=4)
# the pen, hovering: it never quite lands
d.path("M634,614 L608,668", "Pen shaft", fill=NONE, stroke="#2A3444",
       strokeWidth=6, cap="round")
d.path("M608,668 L600,682 L614,680 Z", "Pen nib", fill="#C9A45C",
       stroke=INK, strokeWidth=2.5, join="round")
# a bar of nothing signed yet: the line stays open
d.path("M600,710 C612,706 624,710 636,706", "Unwritten", fill=NONE,
       stroke=NOTE, strokeWidth=2.5, cap="round", opacity=60)

# --- the song: eighth notes rising off the right shoulder --------------------------
def note(x, y, label, flag=True, scale=1.0):
    d.shape("ellipse", f"{label} head", x=x, y=y, width=15*scale,
            height=11*scale, fill=NOTE, stroke=INK, strokeWidth=2.5)
    d.path(f"M{x + 13*scale},{y + 4} L{x + 13*scale},{y - 30*scale}",
           f"{label} stem", fill=NONE, stroke=NOTE, strokeWidth=3.5,
           cap="round")
    if flag:
        d.path(f"M{x + 13*scale},{y - 30*scale} "
               f"C{x + 26*scale},{y - 26*scale} {x + 28*scale},{y - 14*scale} "
               f"{x + 24*scale},{y - 6*scale}", f"{label} flag",
               fill=NONE, stroke=NOTE, strokeWidth=3.5, cap="round")

note(600, 340, "Note 1", scale=1.0)
note(660, 280, "Note 2", scale=0.9)
note(700, 210, "Note 3", scale=0.8)
note(380, 300, "Note 4", scale=0.85)
note(340, 240, "Note 5", scale=0.75)
# the tone's own dust
for i, (x, y, w) in enumerate([(560,240,5),(640,180,4),(720,300,4),(300,340,5),
                               (430,330,4),(690,400,5),(270,440,4),(480,250,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill=NOTE, opacity=30, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("LILT PROTOCOL", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCEEEA", justify="center")
r = d.text("ACTIVE PHONETIC FILTER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9CC4BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("315.lilt-protocol-V1R00")
