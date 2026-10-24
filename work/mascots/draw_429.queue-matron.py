#!/usr/bin/env python3
"""Queue Matron — mascot portrait V1R00. HTTP 429, "Too Many Requests".
Matron watching a single-file queue of requests, Retry-After slip in hand.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Queue Matron — Mascot Portrait", 1000, 1000)

INK = "#3A2A2E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2C1E22"}, {"offset": 1, "color": "#140C10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EFE0D8"}, {"offset": 0.7, "color": "#CBA9A0"},
    {"offset": 1, "color": "#94706A"}]}}
DRESS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54687A"}, {"offset": 0.7, "color": "#3A4A5A"},
    {"offset": 1, "color": "#28323E"}]}}
PACKET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E6C8"}, {"offset": 1, "color": "#CDB684"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A645C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4EAE2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(220,220,7),(770,205,6),(235,720,7),(755,715,7),(175,455,6),
                               (838,448,6),(345,150,6),(650,142,7),(300,795,6),(700,790,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A645C", opacity=40, stroke=NONE)
# floor line, ends well inside the rim
d.path("M270,742 C400,730 640,730 780,740", "Floor line",
       fill=NONE, stroke="#7A564E", strokeWidth=3, opacity=50, cap="round")

# --- the queue of requests, single file ------------------------------------------
# each: little envelope-packet body + flap + hopeful eyes, receding right
packets = [
    (570, 646, 80, 72),   # front of the line, biggest
    (652, 656, 68, 62),
    (722, 664, 58, 52),
    (780, 670, 48, 42),
]
for i, (x, y, w, h) in enumerate(packets):
    d.shape("ellipse", f"Q{i} shadow", x=x-6, y=y+h+2, width=w+12, height=10,
            fill="#6E4A42", opacity=35, stroke=NONE)
    d.shape("rectangle", f"Q{i} body", x=x, y=y, width=w, height=h, radius=8,
            fill=PACKET_GRAD, stroke=INK, strokeWidth=4, opacity=max(55, 100 - i*14))
    d.path(f"M{x+4},{y+6} L{x+w/2},{y+h*0.45} L{x+w-4},{y+6}",
           f"Q{i} flap", fill=NONE, stroke=INK, strokeWidth=3,
           join="round", opacity=max(55, 90 - i*14))
    es = w * 0.16
    d.shape("ellipse", f"Q{i} eye L", x=x+w*0.30, y=y+h*0.55, width=es, height=es*1.2,
            fill="#33222A", stroke=NONE, opacity=max(55, 100 - i*14))
    d.shape("ellipse", f"Q{i} eye R", x=x+w*0.58, y=y+h*0.55, width=es, height=es*1.2,
            fill="#33222A", stroke=NONE, opacity=max(55, 100 - i*14))
    # little feet
    d.path(f"M{x+w*0.3},{y+h} L{x+w*0.3-4},{y+h+8} M{x+w*0.65},{y+h} L{x+w*0.65+4},{y+h+8}",
           f"Q{i} feet", fill=NONE, stroke=INK, strokeWidth=3.5,
           cap="round", opacity=max(55, 90 - i*14))
# patient shiver marks on the last in line
d.path("M774,656 L782,648 M814,660 L820,652", "Shiver", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round", opacity=45)

# --- the matron ----------------------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=296, y=744, width=280, height=28,
        fill="#6E4A42", opacity=40, stroke=NONE)
# dress: wide bell silhouette
d.path("M330,744 C322,650 330,556 360,496 C386,444 430,422 468,428 "
       "C512,436 540,488 546,556 C552,636 552,694 550,744 Z",
       "Dress", fill=DRESS_GRAD, stroke=INK, strokeWidth=7, join="round")
# apron panel
d.path("M392,540 C424,560 470,560 500,542 C514,612 514,676 508,724 "
       "L380,724 C376,662 380,598 392,540 Z",
       "Apron", fill="#E8DFC8", opacity=90, stroke=INK, strokeWidth=4, join="round")
d.path("M404,700 L486,700", "Apron hem", fill=NONE, stroke="#B9AC90", strokeWidth=3, opacity=70)
# shawl across the shoulders
d.path("M346,512 C356,452 400,420 452,420 C504,420 544,452 552,508 "
       "C520,478 486,466 450,466 C412,466 378,482 346,512 Z",
       "Shawl", fill="#6E3E4E", stroke=INK, strokeWidth=5, join="round")
# head
d.shape("ellipse", "Head", x=388, y=336, width=132, height=120,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F2DEC4"}, {"offset": 1, "color": "#D2AE8E"}]}},
        stroke=INK, strokeWidth=6)
# hair: center part + bun
d.path("M390,388 C392,344 420,318 456,318 C492,318 518,344 520,388 "
       "C492,368 420,368 390,388 Z", "Hair", fill="#5E5348", stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Bun", x=438, y=296, width=40, height=34,
        fill="#5E5348", stroke=INK, strokeWidth=5)
d.path("M446,312 C452,304 462,302 470,306", "Bun swirl",
       fill=NONE, stroke="#3A322C", strokeWidth=3, cap="round", opacity=70)
# spectacles + eyes watching the queue (looking right)
d.shape("ellipse", "Lens L", x=414, y=398, width=34, height=30,
        fill="#FFFFFF", opacity=25, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Lens R", x=474, y=398, width=34, height=30,
        fill="#FFFFFF", opacity=25, stroke=INK, strokeWidth=3.5)
d.path("M448,410 L474,410", "Bridge", fill=NONE, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye L", x=428, y=404, width=13, height=15, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Eye R", x=490, y=404, width=13, height=15, fill="#33222A", stroke=NONE)
# long-suffering mouth
d.path("M448,448 C456,444 470,444 478,448", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Cheek", x=500, y=432, width=22, height=10, fill="#D98C7A", opacity=40, stroke=NONE)
# left hand on hip — elbow out
d.path("M346,540 C320,560 312,596 322,622 C330,640 344,648 360,646",
       "Arm L", fill=NONE, stroke="#3A4A5A", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand hip", x=348, y=628, width=30, height=26,
        fill="#E8CBA8", stroke=INK, strokeWidth=4)
# right arm holding the slip toward the queue
d.path("M540,520 C566,530 578,552 576,576", "Arm R",
       fill=NONE, stroke="#3A4A5A", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand R", x=560, y=562, width=30, height=28,
        fill="#E8CBA8", stroke=INK, strokeWidth=4)
# the Retry-After slip
d.path("M556,530 L668,516 L676,572 L564,586 Z", "Slip",
       fill="#F6EFDA", stroke=INK, strokeWidth=4, join="round")
d.text("RETRY-AFTER", "Slip text", x=614, y=548, size=13, font="Virelai Sans",
       color="#8A3444", justify="center")
d.path("M576,564 L650,555", "Slip rule", fill=NONE, stroke="#9A9482", strokeWidth=3, opacity=70)

# --- name + role ----------------------------------------------------------------------
d.text("QUEUE MATRON", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F2E6DC", justify="center")
d.text(" ".join("TOO MANY REQUESTS"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C89E92", justify="center")

d.finish("429.queue-matron-V1R00")
