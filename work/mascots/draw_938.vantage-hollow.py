#!/usr/bin/env python3
"""Vantage Hollow — mascot portrait V1R00.
A green seal glowing serenely on a dashboard while the proof cache beneath
sits open and empty. Slightly over-trusted, per the archivist's addendum.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Vantage Hollow — Mascot Portrait", 1000, 1000)

INK = "#1E2622"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1410"}, {"offset": 1, "color": "#050A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5E4C"}, {"offset": 0.7, "color": "#283E33"},
    {"offset": 1, "color": "#15231C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#243830"}, {"offset": 1, "color": "#0E1A14"}]}}
DASH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4A54"}, {"offset": 1, "color": "#202A32"}]}}
PANEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A343E"}, {"offset": 1, "color": "#141C22"}]}}
SEAL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7EF0B4"}, {"offset": 0.72, "color": "#3EC27E"},
    {"offset": 1, "color": "#1E7A4E"}]}}
TRAY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38444E"}, {"offset": 1, "color": "#1A232A"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E8A72", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE8DA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A5A4A", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1610",
       strokeWidth=4, opacity=70)

# --- the dashboard ----------------------------------------------------------------
d.shape("ellipse", "Dash shadow", x=280, y=672, width=440, height=32,
        fill="#060C08", opacity=50, stroke=NONE)
d.shape("rectangle", "Dashboard", x=295, y=235, width=410, height=445,
        fill=DASH, stroke=INK, strokeWidth=6, radius=14)
# header strip
d.shape("rectangle", "Header", x=310, y=250, width=380, height=40,
        fill=PANEL, stroke=INK, strokeWidth=3, radius=8)
d.text("TRUST SURFACE v9", "Header label", x=325, y=275, size=15,
       font="Virelai Sans", color="#8EA89A", justify="left")
d.text("BASIS: INHERITED", "Header right", x=568, y=273, size=11,
       font="Virelai Sans", color="#5E7A6C", justify="left")
# small gauges flanking the seal
for side, gx in (("L", 335), ("R", 605)):
    d.shape("ellipse", f"Gauge {side}", x=gx, y=310, width=64, height=64,
            fill=PANEL, stroke=INK, strokeWidth=4)
    d.path(f"M{gx+32},{gx-238+32+238} L{gx+44},{gx-238+22+238}",
           f"Needle {side}", fill=NONE, stroke="#8EA89A", strokeWidth=3,
           cap="round")
    d.shape("ellipse", f"Gauge dot {side}", x=gx+28, y=310+28, width=8, height=8,
            fill="#8EA89A", stroke=NONE)
# --- the seal: Vantage Hollow itself, aglow ----------------------------------------
# big soft glow
d.shape("ellipse", "Seal glow", x=370, y=320, width=260, height=230,
        fill="#5EE8A0", opacity=14, stroke=NONE)
d.shape("ellipse", "Seal glow core", x=420, y=350, width=160, height=150,
        fill="#7EF0B4", opacity=14, stroke=NONE)
# scalloped medallion rim
for i in range(14):
    a = math.radians(i * (360/14))
    cx, cy = 500 + 88*math.cos(a), 440 + 88*math.sin(a)
    d.shape("ellipse", f"Scallop {i+1}", x=cx-17, y=cy-17, width=34, height=34,
            fill=SEAL, stroke=INK, strokeWidth=3)
# medallion face
d.shape("ellipse", "Seal face", x=415, y=355, width=170, height=170,
        fill=SEAL, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Seal inner ring", x=435, y=375, width=130, height=130,
        fill=NONE, stroke="#0E5E3A", strokeWidth=3, opacity=70)
# laurel ticks on the rim
for i in range(6):
    a = math.radians(200 + i*28)
    x1, y1 = 500 + 76*math.cos(a), 440 + 76*math.sin(a)
    x2, y2 = 500 + 86*math.cos(a), 440 + 86*math.sin(a)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Laurel {i+1}",
           fill=NONE, stroke="#0E5E3A", strokeWidth=3, cap="round", opacity=70)
# serene, slightly smug face — eyes closed, content smile
d.path("M448,432 C456,440 468,440 476,432", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M524,432 C532,440 544,440 552,432", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M468,472 C485,484 515,484 532,472", "Content smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# self-satisfied highlight
d.shape("ellipse", "Seal sheen", x=452, y=382, width=70, height=30,
        fill="#FFFFFF", opacity=25, stroke=NONE)

# --- the empty proof cache beneath -------------------------------------------------
d.shape("rectangle", "Cache slot", x=355, y=545, width=290, height=60,
        fill="#0C1418", stroke=INK, strokeWidth=4, radius=6)
# open drawer, pulled forward
d.path("M370,605 L630,605 L660,668 L340,668 Z", "Drawer tray",
       fill=TRAY, stroke=INK, strokeWidth=5, join="round")
d.path("M370,605 L340,668 M630,605 L660,668", "Tray walls", fill=NONE,
       stroke="#0C1418", strokeWidth=3, opacity=60)
d.shape("rectangle", "Tray front", x=340, y=655, width=320, height=34,
        fill=PANEL, stroke=INK, strokeWidth=4, radius=5)
d.text("PROOF CACHE — EMPTY", "Tray label", x=415, y=677, size=14,
       font="Virelai Sans", color="#7A8E84", justify="left")
# inside: nothing but a cobweb and dust
d.path("M352,608 C370,620 385,622 398,615 C385,632 368,636 350,630 Z",
       "Cobweb", fill=NONE, stroke="#8A9AAE", strokeWidth=2, opacity=45)
for i, (x, y) in enumerate([(430,630),(500,622),(570,634),(480,642)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=5, height=5,
            fill="#8A9AAE", opacity=35, stroke=NONE)
# a stale attestation stub left behind
d.path("M560,608 L612,608 L608,636 L564,636 Z", "Stale stub", fill="#6A7A88",
       stroke=INK, strokeWidth=3, join="round", opacity=55)
d.text("stale", "Stub text", x=570, y=628, size=10, font="Virelai Sans",
       color="#2E3A44", justify="left")

# --- captions ------------------------------------------------------------------
d.text("VANTAGE HOLLOW", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#CFE8DA", justify="center")
r = d.text("ORNAMENTAL AUTHORITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#8EB49E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("938.vantage-hollow-V1R00")
