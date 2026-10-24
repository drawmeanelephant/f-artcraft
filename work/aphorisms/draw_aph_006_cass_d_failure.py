#!/usr/bin/env python3
"""APH-006 Cass D. Failure — aphorism plate V1R00. Two polite standing
mirrors holding the same intact record, the right replica ghosted and
drifting out of sync; a timestamp dropped mid-fall between them; the sync
arrows never quite arriving; background clusters quietly decomposing.
Cool indigo palette — teal silver vs stale amber. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-006 Cass D. Failure — Aphorism Plate", 1000, 1000)

INK = "#1A2238"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141A2E"}, {"offset": 1, "color": "#07090F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E4066"}, {"offset": 0.7, "color": "#18223C"},
    {"offset": 1, "color": "#0C1224"}]}}
GLASS_TEAL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8E4E0"}, {"offset": 0.7, "color": "#8AB8B2"},
    {"offset": 1, "color": "#56827E"}]}}
GLASS_AMBER = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4D2A8"}, {"offset": 0.7, "color": "#B89A62"},
    {"offset": 1, "color": "#826C40"}]}}
METAL = "#5E7290"
CREAM = "#DCE8F0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6A8A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9FC4D8", strokeWidth=3, opacity=40)

# --- background clusters: one intact, one quietly decomposing --------------------
# intact cluster, upper left — nodes and edges holding
nodes = [(205, 215), (260, 180), (305, 210), (230, 265), (288, 258), (335, 228)]
for i, (x1, y1) in enumerate(nodes):
    for j, (x2, y2) in enumerate(nodes):
        if j > i and abs(i - j) <= 2:
            d.path(f"M{x1},{y1} L{x2},{y2}", f"Edge {i}-{j}", fill=NONE,
                   stroke="#5E82A0", strokeWidth=1.5, opacity=35)
for i, (x, y) in enumerate(nodes):
    d.shape("ellipse", f"Node {i+1}", x=x - 6, y=y - 6, width=12, height=12,
            fill="#7FA8C4", stroke=NONE, opacity=80)
# decomposing cluster, upper right — edges dashed/broken, nodes drifting to dots
dnodes = [(650, 225), (705, 195), (755, 230), (675, 275), (735, 275), (785, 255)]
for i, (x1, y1) in enumerate(dnodes):
    for j, (x2, y2) in enumerate(dnodes):
        if j > i and abs(i - j) <= 2:
            d.path(f"M{x1},{y1} L{x2},{y2}", f"Dedge {i}-{j}", fill=NONE,
                   stroke="#5E82A0", strokeWidth=1.5, opacity=25, dash=[4, 7])
for i, (x, y) in enumerate(dnodes):
    # each node sheds smaller dots as it drifts
    d.shape("ellipse", f"Dnode {i+1}", x=x - 5, y=y - 5, width=10, height=10,
            fill="#7FA8C4", stroke=NONE, opacity=55)
    d.shape("ellipse", f"Dnode {i+1} shed a", x=x + 10, y=y - 12,
            width=5, height=5, fill="#7FA8C4", stroke=NONE, opacity=35)
    d.shape("ellipse", f"Dnode {i+1} shed b", x=x + 17, y=y - 20,
            width=3, height=3, fill="#7FA8C4", stroke=NONE, opacity=20)

# --- floor glow under each mirror -----------------------------------------------
d.shape("ellipse", "Floor glow L", x=215, y=610, width=230, height=60,
        fill="#6EA8A0", opacity=25, stroke=NONE)
d.shape("ellipse", "Floor glow R", x=555, y=625, width=230, height=60,
        fill="#C4A468", opacity=22, stroke=NONE)

# --- sync arrows between the mirrors ---------------------------------------------
# upper arc L->R: it starts, it fades — it does not arrive
d.path("M395,340 Q500,290 605,330", "Sync arc fwd", fill=NONE,
       stroke="#9FC4D8", strokeWidth=4, opacity=70, dash=[14, 10],
       cap="round")
d.path("M595,318 L613,330 L593,340", "Sync head fwd", fill="#9FC4D8",
       opacity=70, stroke=NONE)
# lower arc R->L: already stale — pale, dissolving mid-arc
d.path("M605,560 Q500,610 395,575", "Sync arc back", fill=NONE,
       stroke="#C4A468", strokeWidth=4, opacity=40, dash=[10, 14],
       cap="round")
d.path("M405,565 L387,575 L407,587", "Sync head back", fill="#C4A468",
       opacity=40, stroke=NONE)

# --- the timestamp, dropped mid-fall -------------------------------------------------
d.path("M500,300 L500,420", "Fall path", fill=NONE, stroke=CREAM,
       strokeWidth=2, opacity=25, dash=[3, 12], cap="round")
# the clock itself, tilted in flight
d.shape("ellipse", "Clock face", x=468, y=424, width=64, height=64,
        fill="#DCE8F0", stroke=INK, strokeWidth=4, opacity=95)
d.shape("ellipse", "Clock rim", x=474, y=430, width=52, height=52,
        fill=NONE, stroke=METAL, strokeWidth=3)
d.path("M500,456 L500,438", "Clock hand long", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M500,456 L515,462", "Clock hand short", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Clock pin", x=496, y=452, width=8, height=8,
        fill=INK, stroke=NONE)
# trailing fall dots
for i, (fy, fr, fo) in enumerate([(388, 4, 45), (366, 3, 30), (348, 2, 18)]):
    d.shape("ellipse", f"Fall dot {i+1}", x=498 - fr, y=fy - fr,
            width=fr * 2, height=fr * 2, fill=CREAM, opacity=fo, stroke=NONE)

# --- the mirrors ----------------------------------------------------------------------
def mirror(cx, cy, glass, ghost, label):
    """Standing oval mirror: rim, glass, record inside, stem, foot."""
    if ghost:
        # afterimage of where the replica thinks it still is
        d.shape("ellipse", f"{label} afterimage", x=cx - 60 + 18,
                y=cy - 95 - 14, width=120, height=190, fill=NONE,
                stroke=glass["gradient"]["stops"][0]["color"],
                strokeWidth=3, opacity=20)
    # rim + glass
    d.shape("ellipse", f"{label} rim", x=cx - 66, y=cy - 101, width=132,
            height=202, fill=METAL, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"{label} glass", x=cx - 56, y=cy - 91, width=112,
            height=182, fill=glass, stroke=NONE, opacity=90)
    # glass sheen
    d.path(f"M{cx - 40},{cy - 70} Q{cx - 52},{cy - 10} {cx - 38},{cy + 55}",
           f"{label} sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=8,
           opacity=25, cap="round")
    # stem + foot
    d.shape("rectangle", f"{label} stem", x=cx - 8, y=cy + 101, width=16,
            height=44, fill=METAL, stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"{label} foot", x=cx - 46, y=cy + 140, width=92,
            height=22, fill=METAL, stroke=INK, strokeWidth=3)

def record(cx, cy, label, divergent=False):
    """The intact record page both mirrors hold — replica's drifts."""
    ox, oy = (10, -6) if divergent else (0, 0)
    d.path(rot_rect_path(cx + ox, cy + oy, 64, 84, 0 if not divergent else 4),
           f"{label} record", fill="#E8F0F4", stroke=INK, strokeWidth=2.5)
    for k in range(3):
        ly = cy + oy - 22 + k * 18
        lw = 44 - k * 6
        d.path(rot_rect_path(cx + ox - 2 + k * 2, ly, lw, 3.5,
                             0 if not divergent else 4),
               f"{label} line {k+1}", fill=INK, opacity=55, stroke=NONE)
    if divergent:
        # the record is intact — it is just not the same record
        d.path(f"M{cx + ox - 14},{cy + oy + 30} L{cx + ox + 14},{cy + oy + 30}",
               f"{label} conflict", fill=NONE, stroke="#B0543C",
               strokeWidth=3, opacity=80, cap="round")
    else:
        d.shape("ellipse", f"{label} seal", x=cx + 12, y=cy + 20, width=14,
                height=14, fill="#6EA8A0", stroke=INK, strokeWidth=1.5,
                opacity=90)

# mirror L: crisp teal, holding its record properly
mirror(330, 430, GLASS_TEAL, False, "Mirror L")
record(330, 430, "L record")
# mirror R: the stale amber replica — shifted up-right, ghosted
mirror(670, 445, GLASS_AMBER, True, "Mirror R")
record(670, 445, "R record", divergent=True)
d.shape("ellipse", "Mirror R veil", x=614, y=354, width=112, height=182,
        fill="#141A2E", opacity=35, stroke=NONE)
# drift particles leaking off the stale replica
for i, (px, py, pr, po) in enumerate([(745, 360, 5, 40), (762, 330, 4, 30),
                                       (775, 300, 3, 20), (785, 272, 2, 12)]):
    d.shape("ellipse", f"Drift {i+1}", x=px, y=py, width=pr * 2, height=pr * 2,
            fill="#C4A468", opacity=po, stroke=NONE)

# --- aphorism line + name + role ----------------------------------------------------
r = d.text("EVENTUAL CONSISTENCY REMAINS", "Key line 1", x=500, y=716,
           size=22, font="Virelai Sans", color="#9FC4D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=110)
r = d.text("AN ASPIRATIONAL THEORY.", "Key line 2", x=500, y=750,
           size=22, font="Virelai Sans", color="#9FC4D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=110)

d.text("CASS D. FAILURE", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("EVENTUAL CONSISTENCY IS THEORY", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#7FA8C4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-006-cass-d-failure-V1R00")
