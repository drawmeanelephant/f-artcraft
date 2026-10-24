#!/usr/bin/env python3
"""Crashy McThinkslow — mascot portrait V1R00. System Lag Embodiment:
a droopy little gremlin stalled mid-flicker, lag-smeared across two ghost
frames, a wait-spinner ticking over its head, a stalled loading bar below,
a "Thinking…" help bubble and a spinning hourglass cursor. Frozen-screen
palette: cold phosphor slate on deep navy. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Crashy McThinkslow — Mascot Plate", 1000, 1000)

INK = "#3A3242"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#14202E"}, {"offset": 1, "color": "#05080E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C6D6E2"}, {"offset": 0.62, "color": "#8FA9BD"},
    {"offset": 1, "color": "#587084"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 370], "end": [0, 680], "stops": [
    {"offset": 0, "color": "#EAF2F7"}, {"offset": 0.55, "color": "#AFC6D6"},
    {"offset": 1, "color": "#7E97AB"}]}}
BELLY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4F9FC"}, {"offset": 1, "color": "#C3D5E0"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#74D8C4"}, {"offset": 1, "color": "#3E9C8E"}]}}
GHOST = "#9FB8C8"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#7FA0B4", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1A2836", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE9F1", strokeWidth=3, opacity=40)
# screen-frost patina
d.shape("ellipse", "Patina 1", x=170, y=140, width=260, height=170, fill="#B9CFDC", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=620, width=280, height=160, fill="#7E99AC", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(190,320,6),(810,330,5),(160,540,7),(850,540,6),(230,760,5),
                               (740,770,6),(130,430,5),(862,615,5),(430,110,5),(610,130,6),
                               (330,140,4),(720,200,5),(210,650,4),(870,440,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E2EEF5", opacity=45, stroke=NONE)
# giant faint UI ghosts on the backdrop, kept well inside the canvas edges
d.path("M60,140 A90,90 0 0 1 150,60", "Ghost arc TL",
       fill=NONE, stroke="#4E6A7E", strokeWidth=16, opacity=10, cap="round")
d.path("M60,170 A120,120 0 0 1 170,60", "Ghost arc TL2",
       fill=NONE, stroke="#4E6A7E", strokeWidth=8, opacity=8, cap="round")

# --- "Thinking…" help bubble ----------------------------------------------------
# tail first so the bubble body covers the seam
d.path("M612,318 L556,384 L668,332 Z", "Bubble tail",
       fill="#E9F1F7", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Bubble", x=580, y=214, width=252, height=106, radius=30,
        fill="#E9F1F7", stroke=INK, strokeWidth=4)
for x, y in [(580, 214), (832, 214), (832, 320)]:
    assert on_disc(x, y, 6), (x, y)
d.text("Thinking…", "Bubble text", x=706, y=279, size=30, font="Source Sans 3",
       color="#3E4C5A", justify="center")

# --- wait spinner above the head ------------------------------------------------
SCX, SCY = 430, 306
for i in range(8):
    a = math.radians(i * 45 - 90)
    x0, y0 = SCX + 22 * math.cos(a), SCY + 22 * math.sin(a)
    x1, y1 = SCX + 34 * math.cos(a), SCY + 34 * math.sin(a)
    d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", f"Spinner tick {i+1}",
           fill=NONE, stroke="#43586A", strokeWidth=7,
           opacity=88 - i * 10, cap="round")

# --- loading bar (stalled at ~58%) ----------------------------------------------
d.text("LOADING", "Bar label", x=252, y=706, size=20, font="Source Sans 3",
       color="#5C7488")
d.shape("rectangle", "Bar track", x=250, y=716, width=500, height=42, radius=21,
        fill="#23303E", stroke="#5B7B8E", strokeWidth=3)
d.shape("rectangle", "Bar fill", x=258, y=724, width=290, height=26, radius=13,
        fill=BAR_GRAD, stroke=NONE)
for i, x in enumerate(range(312, 530, 26)):
    d.shape("rectangle", f"Bar stripe {i+1}", x=x, y=724, width=6, height=26,
            fill="#FFFFFF", opacity=14, stroke=NONE)
d.shape("rectangle", "Bar leading edge", x=540, y=724, width=8, height=26, radius=4,
        fill="#A8F0E0", opacity=85, stroke=NONE)
d.shape("ellipse", "Bar sheen", x=270, y=726, width=260, height=10,
        fill="#FFFFFF", opacity=16, stroke=NONE)
for x, y in [(250, 716), (750, 716), (250, 758), (750, 758)]:
    assert on_disc(x, y, 8), (x, y)

# --- hourglass cursor, spinning --------------------------------------------------
HGC = (724, 474)
d.path("M686,392 A92,92 0 0 1 800,422", "Spin arc 1",
       fill=NONE, stroke="#4E6A7E", strokeWidth=9, opacity=45, cap="round")
d.path("M792,414 L812,424 L790,434 Z", "Spin arrow 1", fill="#4E6A7E", opacity=45, stroke=NONE)
d.path("M762,556 A92,92 0 0 1 648,528", "Spin arc 2",
       fill=NONE, stroke="#4E6A7E", strokeWidth=9, opacity=30, cap="round")
d.path("M658,520 L636,528 L656,540 Z", "Spin arrow 2", fill="#4E6A7E", opacity=30, stroke=NONE)
# frame
d.shape("rectangle", "HG cap top", x=694, y=424, width=62, height=9, radius=4,
        fill="#3E4C5A", stroke=INK, strokeWidth=2)
d.shape("rectangle", "HG cap bot", x=694, y=517, width=62, height=9, radius=4,
        fill="#3E4C5A", stroke=INK, strokeWidth=2)
# glass bulbs
d.path("M699,437 L751,437 L725,472 Z", "HG top bulb",
       fill="#DCE9F2", opacity=60, stroke=INK, strokeWidth=3)
d.path("M699,513 L751,513 L725,478 Z", "HG bot bulb",
       fill="#DCE9F2", opacity=60, stroke=INK, strokeWidth=3)
# sand: top cone draining + settled base
d.path("M714,446 L736,446 L725,462 Z", "HG sand top", fill="#E8C87E", opacity=85, stroke=NONE)
d.path("M725,480 L743,510 L707,510 Z", "HG sand pile", fill="#E8C87E", opacity=85, stroke=NONE)
d.path("M725,464 L725,476", "HG sand stream", fill=NONE, stroke="#E8C87E",
       strokeWidth=2.5, opacity=80, cap="round")
# pointer arrow riding the spin
d.path("M672,530 L672,576 L685,564 L694,584 L704,580 L695,560 L712,560 Z",
       "Cursor", fill="#EDF3F7", stroke=INK, strokeWidth=3)

# --- Crashy: lag-smeared ghost frames, then the body ----------------------------
def body_path(cx, cy):
    return ("M%.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f Z" % (
        cx,      cy - 148,
        cx + 112, cy - 148, cx + 158, cy - 70, cx + 150, cy + 18,
        cx + 144, cy + 96,  cx + 92,  cy + 150, cx,      cy + 150,
        cx - 92,  cy + 150, cx - 144, cy + 96,  cx - 150, cy + 18,
        cx - 158, cy - 70,  cx - 112, cy - 148, cx,      cy - 148))

CX, CY = 440, 522
for k, (ox, oy, op) in enumerate([(-100, -30, 17), (-50, -14, 32)]):
    d.path(body_path(CX + ox, CY + oy), f"Ghost frame {k+1}",
           fill=GHOST, opacity=op, stroke=NONE)
    # the lag smear keeps its own dim stare
    for ex in (-48, 46):
        d.shape("ellipse", f"Ghost eye {k+1} {ex}", x=CX + ox + ex - 14,
                y=CY + oy - 44, width=28, height=26,
                fill="#5E7A8E", opacity=op, stroke=NONE)

# ground shadow
d.shape("ellipse", "Ground shadow", x=300, y=662, width=280, height=26,
        fill="#1E2C38", opacity=25, stroke=NONE)

# body
d.path(body_path(CX, CY), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly
d.shape("ellipse", "Belly", x=356, y=530, width=168, height=120,
        fill=BELLY_GRAD, opacity=70, stroke=NONE)
# top-of-head sheen + lower shade
d.shape("ellipse", "Head sheen", x=330, y=392, width=200, height=64,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M330,640 C390,666 490,666 550,640 C500,656 380,656 330,640 Z",
       "Base shade", fill="#5E7A8E", opacity=35, stroke=NONE)

# arms: left droops, right mid-shrug raised a beat too late
d.path("M312,574 C288,586 280,610 292,630", "Arm L",
       fill=NONE, stroke="#9DB4C4", strokeWidth=24, cap="round")
d.path("M566,556 C592,542 602,516 592,496", "Arm R",
       fill=NONE, stroke="#9DB4C4", strokeWidth=24, cap="round")

# face: heavy-lidded eyes mid-flicker (left more open than right), both
# slid down toward the loading bar
def eye(cx, cy, lid):
    d.shape("ellipse", f"Eye white {cx}", x=cx - 25, y=cy - 22, width=50, height=46,
            fill="#F4F8FA", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil {cx}", x=cx - 8, y=cy + 4, width=17, height=17,
            fill="#2C3644", stroke=NONE)
    d.shape("ellipse", f"Glint {cx}", x=cx - 4, y=cy + 7, width=5, height=5,
            fill="#FFFFFF", opacity=85, stroke=NONE)
    # lid: body-tone cap swallowing the upper part of the eye
    d.shape("ellipse", f"Lid {cx}", x=cx - 28, y=cy - 30, width=56, height=lid,
            fill="#9FB8C8", stroke=NONE)
    d.path(f"M{cx-24},{cy-24+lid*0.55:.0f} C{cx-8},{cy-16+lid*0.55:.0f} "
           f"{cx+8},{cy-16+lid*0.55:.0f} {cx+24},{cy-24+lid*0.55:.0f}",
           f"Lid crease {cx}", fill=NONE, stroke=INK, strokeWidth=3.5,
           opacity=70, cap="round")

eye(392, 486, 30)
eye(486, 486, 38)

# mouth: a small uncertain wobble
d.path("M412,596 C424,590 436,602 448,596 C456,592 462,596 466,600",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# one buffering sweat drop adrift off the temple
d.path("M610,392 C622,408 626,420 610,426 C594,420 598,408 610,392 Z",
       "Sweat drop", fill="#BFE0F0", stroke=INK, strokeWidth=2.5, opacity=90)

# --- name + role -----------------------------------------------------------------
d.text("CRASHY MCTHINKSLOW", "Name", x=500, y=930, size=52, font="Virelai Sans",
       color="#D9E6EE", justify="center")
d.text("SYSTEM LAG EMBODIMENT", "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#8FA9BC", justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    if str(n.get("name", "")) == "Role":
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "tracking": 260}}, "track role")
    if str(n.get("name", "")) == "Bar label":
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "tracking": 220}}, "track label")

d.finish("007.crashy-mcthinkslow-V1R00")
