#!/usr/bin/env python3
"""Serotonin Sam — mascot portrait V1R00.
A friendly KPI graph living in the dashboard sidebar: chart-card body,
a green trendline that only goes up, axis arms, and one sticker, held.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Serotonin Sam — Mascot Portrait", 1000, 1000)

INK = "#232030"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121A2A"}, {"offset": 1, "color": "#070A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3C4E6A"}, {"offset": 0.7, "color": "#283550"},
    {"offset": 1, "color": "#161E30"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#24304A"}, {"offset": 1, "color": "#111826"}]}}
PANEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E2A40"}, {"offset": 1, "color": "#121A2C"}]}}
SIDEBAR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26344E"}, {"offset": 1, "color": "#172134"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EDDC"}, {"offset": 1, "color": "#D6CBAE"}]}}
SAM_SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6F0DE"}, {"offset": 0.75, "color": "#DCD2B6"},
    {"offset": 1, "color": "#B4A888"}]}}
GREEN = "#52D98A"
GOLD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8DC8A"}, {"offset": 0.7, "color": "#D9A94E"},
    {"offset": 1, "color": "#A67C34"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7496", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D2EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(192,236,8),(800,232,7),(158,522,9),(834,544,8),
                               (246,764,7),(754,748,9),(132,392,6),(864,394,7),
                               (392,112,7),(612,110,8),(332,822,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#33445E", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0F1A",
       strokeWidth=4, opacity=70)

# --- the dashboard window -------------------------------------------------------
d.shape("ellipse", "Dash glow", x=190, y=210, width=620, height=470,
        fill="#52D98A", opacity=6, stroke=NONE)
d.shape("rectangle", "Dashboard", x=240, y=250, width=520, height=420,
        fill=PANEL, stroke="#45587A", strokeWidth=6, radius=18)
d.path("M240,296 L760,296", "Dash titlebar", fill=NONE, stroke="#45587A",
       strokeWidth=4)
for i, c in enumerate(("#E0705E", "#E8C05E", "#6AC88A")):
    d.shape("ellipse", f"Dash dot {i+1}", x=262 + i * 26, y=266, width=14, height=14,
            fill=c, stroke=NONE, opacity=85)
# main pane: dim mood charts nobody reads
for i, (x, y, w) in enumerate([(268, 330, 120), (268, 356, 84), (268, 382, 100)]):
    d.shape("rectangle", f"Pane line {i+1}", x=x, y=y, width=w, height=11,
            fill="#3A4C6C", stroke=NONE, radius=5, opacity=80)
# a drooping grey sparkline in the main pane — the unsmoothed truth
d.path("M268,450 L320,442 L372,462 L424,458 L476,478 L528,484", "Grey spark",
       fill=NONE, stroke="#56688A", strokeWidth=5, cap="round", join="round",
       opacity=85)
d.shape("rectangle", "Pane card", x=268, y=520, width=240, height=110,
        fill="#182238", stroke="#33445E", strokeWidth=3, radius=10)
for i, (y, w) in enumerate([(548, 190), (572, 150), (596, 170)]):
    d.shape("rectangle", f"Pane card line {i+1}", x=286, y=y, width=w, height=10,
            fill="#2E3E5C", stroke=NONE, radius=5)

# --- the sidebar strip ---------------------------------------------------------
d.shape("rectangle", "Sidebar", x=560, y=250, width=200, height=420,
        fill=SIDEBAR, stroke="#45587A", strokeWidth=5, radius=14)
d.path("M560,296 L760,296", "Sidebar rule", fill=NONE, stroke="#45587A",
       strokeWidth=4)
d.shape("rectangle", "Sidebar label", x=582, y=310, width=110, height=14,
        fill="#3A4C6C", stroke=NONE, radius=7)

# --- Serotonin Sam: a chart card with a head, arms, one sticker -------------------
d.shape("ellipse", "Sam shadow", x=540, y=646, width=240, height=30,
        fill="#060A10", opacity=50, stroke=NONE)
# little legs
d.path("M640,618 L636,652", "Sam leg L", fill=NONE, stroke="#B4A888",
       strokeWidth=12, cap="round")
d.path("M692,618 L696,652", "Sam leg R", fill=NONE, stroke="#A89C80",
       strokeWidth=12, cap="round")
d.shape("ellipse", "Sam shoe L", x=616, y=646, width=34, height=14, fill=INK, stroke=NONE)
d.shape("ellipse", "Sam shoe R", x=684, y=646, width=34, height=14, fill=INK, stroke=NONE)
# chart-card body
d.shape("rectangle", "Sam card", x=592, y=470, width=150, height=150,
        fill=CARD, stroke=INK, strokeWidth=5, radius=12)
# card axes + the green trendline, morale-compatible and only rising
d.path("M608,596 L608,492 M608,596 L728,596", "Sam axes", fill=NONE,
       stroke="#8A8068", strokeWidth=4, cap="round")
d.path("M612,584 L640,566 L662,576 L690,544 L722,522", "Trendline", fill=NONE,
       stroke=GREEN, strokeWidth=6, cap="round", join="round")
for i, (x, y) in enumerate([(612, 584), (640, 566), (662, 576), (690, 544), (722, 522)]):
    d.shape("ellipse", f"Trend dot {i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill=GREEN, stroke=NONE)
d.shape("ellipse", "Trend glow", x=640, y=500, width=110, height=90,
        fill=GREEN, opacity=18, stroke=NONE)
# head overlapping the card's top
d.shape("ellipse", "Sam head", x=610, y=398, width=112, height=100,
        fill=SAM_SKIN, stroke=INK, strokeWidth=5)
# face: unshakable chart-based optimism
d.path("M634,452 C640,444 652,444 658,452", "Sam eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M676,452 C682,444 694,444 700,452", "Sam eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M646,472 C656,482 676,482 686,472", "Sam smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Sam cheek L", x=622, y=462, width=18, height=10,
        fill="#E89A7E", opacity=55, stroke=NONE)
d.shape("ellipse", "Sam cheek R", x=692, y=462, width=18, height=10,
        fill="#E89A7E", opacity=55, stroke=NONE)
# chart arms: the left arm is itself an axis, ticked
d.path("M592,530 L540,530 L540,488", "Sam arm L", fill=NONE,
       stroke="#B4A888", strokeWidth=10, cap="round", join="round")
for i, y in enumerate((520, 504, 496)):
    d.path(f"M540,{y} L532,{y}", f"Arm tick {i+1}", fill=NONE,
           stroke="#8A8068", strokeWidth=4, cap="round")
# right arm out of the sidebar, offering the sticker
d.path("M742,540 C770,536 792,520 802,496", "Sam arm R", fill=NONE,
       stroke="#A89C80", strokeWidth=10, cap="round")
d.shape("ellipse", "Sam hand", x=794, y=484, width=22, height=18,
        fill="#DCD2B6", stroke=INK, strokeWidth=3)
# the sticker: one gold star, the supply never runs out
d.shape("ellipse", "Star glow", x=776, y=418, width=70, height=70,
        fill="#F8DC8A", opacity=18, stroke=NONE)
d.path("M812,424 L821,444 L843,446 L826,460 L831,482 L812,470 L793,482 "
       "L798,460 L781,446 L803,444 Z",
       "Star sticker", fill=GOLD, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Star shine", x=800, y=434, width=14, height=9,
        fill="#FFF4D0", opacity=80, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("SEROTONIN SAM", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#DCE6F4", justify="center")
r = d.text("COMFORT GLYPH WITH KPI ARMS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AAECB", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("226.serotonin-sam-V1R00")
