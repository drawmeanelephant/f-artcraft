#!/usr/bin/env python3
"""Rot McMascotterton — mascot portrait V1R00.
A phosphor-green beacon-ghost glowing under terminal light, antenna tipped
with a dish tuned to the pipeline's last clean timestamp; the console strip
above reads DEPLOY 02:14:07 — BUILD_OK. 1000x1000 plate format.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Rot McMascotterton — Mascot Portrait", 1000, 1000)

INK = "#1E3226"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0E1A14"}, {"offset": 1, "color": "#040906"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E4A38"}, {"offset": 0.6, "color": "#1E3328"},
    {"offset": 1, "color": "#0E1C14"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 430], "end": [0, 790], "stops": [
    {"offset": 0, "color": "#BEF2C6"}, {"offset": 0.55, "color": "#72D488"},
    {"offset": 1, "color": "#3C9E58"}]}}
CONSOLE_GRAD = {"gradient": {"kind": "linear", "start": [0, 196], "end": [0, 236], "stops": [
    {"offset": 0, "color": "#0A140E"}, {"offset": 1, "color": "#12241A"}]}}
CONE_GRAD = {"gradient": {"kind": "linear", "start": [0, 236], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#9AECB0", "opacity": 0.16},
    {"offset": 1, "color": "#9AECB0", "opacity": 0}]}}
GLOW_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#AEF4BE", "opacity": 0.30},
    {"offset": 1, "color": "#AEF4BE", "opacity": 0}]}}
POOL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#72D488", "opacity": 0.28},
    {"offset": 1, "color": "#72D488", "opacity": 0}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5E9A6E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E6250", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8ED4A0", strokeWidth=3, opacity=28)
# phosphor flecks on the dark plate
for i, (x, y, w) in enumerate([(190, 360, 5), (812, 340, 6), (172, 556, 6), (830, 590, 5),
                               (272, 780, 5), (722, 776, 6), (322, 142, 4), (668, 136, 5),
                               (240, 470, 4), (768, 480, 4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6EC488", opacity=40, stroke=NONE)
for i, (x, y, w) in enumerate([(70, 160, 4), (915, 130, 5), (60, 590, 4), (938, 660, 4),
                               (148, 915, 4), (865, 925, 5), (552, 22, 4), (262, 36, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#8EC49C", opacity=30, stroke=NONE)

# --- console strip: the pipeline's last word ----------------------------------------
d.shape("rectangle", "Console", x=300, y=196, width=400, height=40,
        radius=8, fill=CONSOLE_GRAD, stroke="#3E6250", strokeWidth=3)
for i, x in enumerate((318, 334, 350)):
    d.shape("ellipse", f"Con dot {i+1}", x=x, y=211, width=9, height=9,
            fill="#3E6250", opacity=80, stroke=NONE)
d.text("DEPLOY 02:14:07 — BUILD_OK", "Console text", x=508, y=223, size=16,
       font="Source Sans 3", color="#8EE8A8", justify="center")
# the terminal light cone falling on the mascot
d.path("M340,236 L660,236 L640,700 L360,700 Z", "Light cone",
       fill=CONE_GRAD, stroke=NONE)

# --- ground glow + shadow -------------------------------------------------------------
d.shape("ellipse", "Glow pool", x=330, y=720, width=340, height=70,
        fill=POOL_GRAD, stroke=NONE)
d.shape("ellipse", "Shadow", x=380, y=748, width=240, height=28,
        fill="#08110B", opacity=40, stroke=NONE)

# --- feet -----------------------------------------------------------------------------
d.shape("ellipse", "Foot L", x=424, y=752, width=68, height=32,
        fill="#3C9E58", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=508, y=752, width=68, height=32,
        fill="#3C9E58", stroke=INK, strokeWidth=5)

# --- beacon body ----------------------------------------------------------------------
d.shape("ellipse", "Halo", x=340, y=390, width=320, height=330,
        fill=GLOW_GRAD, stroke=NONE)
d.path("M390,760 C378,650 388,556 424,494 C452,450 548,450 576,494 "
       "C612,556 622,650 610,760 C578,780 542,788 500,788 "
       "C458,788 422,780 390,760 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Dome light", x=436, y=466, width=128, height=54,
        fill="#FFFFFF", opacity=26, stroke=NONE)
d.path("M414,706 C452,730 548,730 586,706 C558,744 442,744 414,706 Z",
       "Hem shade", fill="#2E7E46", opacity=32, stroke=NONE)
# scanline flicker across the body — it IS the render
for i, y in enumerate((560, 596, 632, 668)):
    d.path(f"M404,{y} L596,{y}", f"Body scan {i+1}", fill=NONE,
           stroke="#2E7E46", strokeWidth=3, opacity=22, cap="round")

# --- antenna: tuned to the pipeline timestamp ------------------------------------------
d.path("M500,470 C498,442 498,414 500,392", "Antenna stem", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Antenna collar", x=484, y=456, width=32, height=18,
        fill="#4EAE66", stroke=INK, strokeWidth=4)
# little dish at the tip
d.path("M478,388 C478,368 490,354 506,352 C522,354 532,368 532,388 "
       "C518,382 492,382 478,388 Z", "Dish", fill="#8EE8A8",
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Dish tip", x=498, y=344, width=14, height=14,
        fill="#C8F4D2", stroke=INK, strokeWidth=3)
# reception: two signal arcs between console and dish
d.path("M540,352 C556,362 566,378 568,396", "Signal 1", fill=NONE,
       stroke="#8EE8A8", strokeWidth=4, opacity=70, cap="round")
d.path("M560,338 C586,352 600,374 604,400", "Signal 2", fill=NONE,
       stroke="#8EE8A8", strokeWidth=4, opacity=45, cap="round")

# --- face: deliberately optimistic ------------------------------------------------------
d.shape("ellipse", "Eye L", x=440, y=540, width=42, height=50,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=518, y=540, width=42, height=50,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=452, y=556, width=18, height=24,
        fill="#1A2A20", stroke=NONE)
d.shape("ellipse", "Pupil R", x=530, y=556, width=18, height=24,
        fill="#1A2A20", stroke=NONE)
d.shape("ellipse", "Glint L", x=456, y=560, width=7, height=7,
        fill="#FFFFFF", opacity=95, stroke=NONE)
d.shape("ellipse", "Glint R", x=534, y=560, width=7, height=7,
        fill="#FFFFFF", opacity=95, stroke=NONE)
# bright trusting smile + confident blush
d.path("M460,626 C480,646 520,646 540,626", "Smile", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.shape("ellipse", "Blush L", x=414, y=606, width=30, height=16,
        fill="#2E7E46", opacity=30, stroke=NONE)
d.shape("ellipse", "Blush R", x=556, y=606, width=30, height=16,
        fill="#2E7E46", opacity=30, stroke=NONE)

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

NAME = "ROT MCMASCOTTERTON"
d.text(NAME, "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#CFEECF", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "BEACON OF CLEAN BUILDS"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#7EA886", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("085.rot-mcmascotterton-V1R00")
