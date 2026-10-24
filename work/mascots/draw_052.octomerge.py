#!/usr/bin/env python3
"""Octomerge — mascot portrait V1R00.
Octopus in an abandoned repository, eight limbs tangled through
incompatible branch lines, detached HEADs drifting loose, a terminal
still showing the conflict markers nobody resolved. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Octomerge — Mascot Portrait", 1000, 1000)

INK = "#2A1E26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0B1616"}, {"offset": 1, "color": "#040A0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A6A62"}, {"offset": 0.7, "color": "#32493F"},
    {"offset": 1, "color": "#1C2926"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#26332E"}, {"offset": 1, "color": "#121B18"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9A74A8"}, {"offset": 0.65, "color": "#744E84"},
    {"offset": 1, "color": "#4C3257"}]}}
LIMB_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5FA0"}, {"offset": 1, "color": "#5A3C6E"}]}}
TERM_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#18201E"}, {"offset": 1, "color": "#0C1211"}]}}
MAGENTA = "#D46AA0"
GREEN = "#7FD08A"
AMBER = "#E8B86A"
CYAN = "#7AC8D8"
RED = "#D45A5A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6E64", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D4C8", strokeWidth=3, opacity=35)
for i, (x, y, w) in enumerate([(190,240,8),(802,234,7),(152,522,9),(842,540,8),
                               (254,768,7),(748,754,9),(130,392,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,822,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5A50", opacity=50, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -----------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1210",
       strokeWidth=4, opacity=70)

# --- abandoned terminal, left-rear: the conflict nobody resolved ---------------
d.shape("ellipse", "Term shadow", x=140, y=672, width=330, height=20,
        fill="#060A09", opacity=55, stroke=NONE)
d.shape("rectangle", "Terminal", x=128, y=196, width=340, height=300,
        fill=TERM_GRAD, stroke=INK, strokeWidth=6, radius=10)
d.shape("rectangle", "Term bar", x=140, y=208, width=316, height=26,
        fill="#222B28", stroke=NONE, radius=6)
d.text("ABANDONED-REPO — READ ONLY", "Term title", x=150, y=226, size=11,
       font="Virelai Sans", color="#7E8E88", justify="left")
for i, bx in enumerate([418, 434, 450]):
    d.shape("ellipse", f"Term dot {i+1}", x=bx, y=216, width=9, height=9,
            fill="#46544E", stroke=NONE)
# conflict scroll: markers + hex without digits stay Virelai-safe anyway,
# but the log is code — Source Sans 3 throughout.
lines = [("% git merge hotfix", "#9AA8A2"),
         ("Auto-merging src/core.c", "#6E7E78"),
         ("CONFLICT (content): merge", RED),
         ("<<<<<<< HEAD", MAGENTA),
         ("release = deadbee", "#A9B8B0"),
         ("=======", "#8E9E96"),
         ("release = cafebabe", CYAN),
         (">>>>>>> hotfix-wip", AMBER),
         ("hint: fix and commit", "#5E6E68")]
for i, (txt, col) in enumerate(lines):
    d.text(txt, f"Log {i+1}", x=146, y=262+i*24, size=12,
           font="Source Sans 3", color=col, justify="left")
# cursor, stalled forever
d.shape("rectangle", "Log cursor", x=146, y=462, width=8, height=13,
        fill=GREEN, opacity=60, stroke=NONE)
# cobwebs across the terminal corners — nobody has been here a while
d.path("M128,196 C170,210 210,206 250,220 M128,196 C140,236 138,256 150,290 "
       "M250,220 C220,240 190,260 150,290", "Cobweb L", fill=NONE,
       stroke="#C8D8D0", strokeWidth=1.5, opacity=30)
d.path("M468,196 C430,214 400,210 372,226 M468,196 C458,232 460,254 448,282",
       "Cobweb R", fill=NONE, stroke="#C8D8D0", strokeWidth=1.5, opacity=25)

# --- incompatible branch lines threading the scene -------------------------------
# Each is a stroked path with commit-node dots; two clash mid-air.
def branch(pts, color, label):
    # pts[0] is the M point; each following triple is (c1, c2, end)
    p = pts[0]
    s = f"M{p[0]},{p[1]}"
    for a, b, c in pts[1:]:
        s += f" C{a[0]},{a[1]} {b[0]},{b[1]} {c[0]},{c[1]}"
    d.path(s, label, fill=NONE, stroke=color, strokeWidth=5,
           cap="round", opacity=85)

branch([(620,140), ((700,170),(740,230),(728,300)), ((716,360),(700,420),(668,470))],
       MAGENTA, "Branch magenta")
branch([(330,150), ((380,200),(420,250),(452,320)), ((470,390),(500,440),(540,470))],
       GREEN, "Branch green")
branch([(830,260), ((790,320),(770,390),(742,440)), ((720,480),(690,520),(660,540))],
       AMBER, "Branch amber")
branch([(170,470), ((240,480),(300,470),(360,470)), ((420,470),(470,480),(520,500))],
       CYAN, "Branch cyan")
# commit nodes on the branches
for i, (x, y, c) in enumerate([(700,196,MAGENTA),(736,268,MAGENTA),(382,204,GREEN),
                               (446,306,GREEN),(806,300,AMBER),(758,410,AMBER),
                               (228,476,CYAN),(312,470,CYAN),(426,474,CYAN)]):
    d.shape("ellipse", f"Commit {i+1}", x=x-7, y=y-7, width=14, height=14,
            fill=c, stroke=INK, strokeWidth=2.5)
# the clash: the magenta branch ruptures at its origin — sparks fly
d.path("M620,138 L636,124 M620,138 L608,120 M620,138 L640,142 M620,138 L602,144",
       "Clash sparks", fill=NONE, stroke="#F0D8A0", strokeWidth=3,
       cap="round", opacity=90)
d.shape("ellipse", "Clash node", x=613, y=131, width=14, height=14,
        fill="#E8E0C8", stroke=INK, strokeWidth=2.5)

# --- detached HEADs drifting loose ----------------------------------------------
def detached_head(x, y, label):
    d.shape("ellipse", f"{label} ring", x=x-24, y=y-24, width=48, height=48,
            fill="#22302C", stroke="#D8CCA0", strokeWidth=3)
    d.shape("ellipse", f"{label} dot", x=x-6, y=y-6, width=12, height=12,
            fill="#D8CCA0", stroke=NONE)
    d.text("HEAD", f"{label} tag", x=x, y=y+40, size=10,
           font="Virelai Sans", color="#D8CCA0", justify="center")

detached_head(790, 180, "Detached A")
detached_head(190, 580, "Detached B")
detached_head(845, 425, "Detached C")
# C dangles from a dashed leash off the amber branch, tangled in the limbs
d.path("M758,410 C790,412 810,418 822,422", "HEAD leash", fill=NONE,
       stroke="#D8CCA0", strokeWidth=2, dash=[4, 7], cap="round", opacity=60)

# --- Octomerge -------------------------------------------------------------------
d.shape("ellipse", "Octo shadow", x=380, y=676, width=300, height=26,
        fill="#060A09", opacity=55, stroke=NONE)

# eight limbs — ink under-stroke, gradient over-stroke, sucker dots after.
# Each limb curls away from under the mantle; a few seize commit nodes.
limbs = [
    # (path_d, sucker_pts)
    ("M520,560 C470,590 420,640 430,690 C434,712 458,720 470,706",
     [(452,626),(434,664),(438,696)]),
    ("M560,570 C530,620 520,670 540,706 C550,724 574,722 578,704",
     [(538,630),(532,672),(546,700)]),
    ("M610,570 C640,620 660,668 650,708 C644,728 620,728 614,710",
     [(636,634),(650,676),(644,704)]),
    ("M650,560 C700,590 740,640 736,688 C734,712 710,720 698,704",
     [(700,620),(726,660),(730,694)]),
    ("M490,540 C430,560 370,590 350,640 C340,668 356,686 374,678",
     [(432,576),(392,606),(364,640)]),
    ("M680,540 C740,560 790,600 800,650 C806,680 788,696 770,686",
     [(730,578),(768,616),(792,652)]),
    ("M470,500 C400,500 330,520 300,560 C282,584 292,606 312,600",
     [(404,516),(354,534),(316,560)]),
    ("M700,500 C760,490 830,510 856,552 C872,578 860,600 840,592",
     [(764,510),(816,530),(848,560)]),
]
for i, (dd, sux) in enumerate(limbs):
    d.path(dd, f"Limb {i+1} ink", fill=NONE, stroke=INK, strokeWidth=30,
           cap="round")
    d.path(dd, f"Limb {i+1}", fill=NONE, stroke=LIMB_GRAD, strokeWidth=22,
           cap="round")
    for j, (sx, sy) in enumerate(sux):
        d.shape("ellipse", f"Limb {i+1} sucker {j+1}", x=sx, y=sy,
                width=9, height=7, fill="#D8B8DC", opacity=70, stroke=NONE)

# seized commits: two limbs grip stray nodes
d.shape("ellipse", "Seized node L", x=296, y=556, width=16, height=16,
        fill=CYAN, stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Seized node R", x=834, y=548, width=16, height=16,
        fill=AMBER, stroke=INK, strokeWidth=2.5)

# mantle: bulbous dome over the limb roots
d.path("M585,300 C660,300 716,368 716,460 C716,540 660,586 585,586 "
       "C510,586 454,540 454,460 C454,368 510,300 585,300 Z",
       "Mantle", fill=BODY_GRAD, stroke=INK, strokeWidth=7, join="round")
d.shape("ellipse", "Mantle hi", x=496, y=344, width=110, height=70,
        fill="#FFFFFF", opacity=14, stroke=NONE)
d.shape("ellipse", "Mantle shade", x=640, y=480, width=90, height=80,
        fill="#3A2444", opacity=25, stroke=NONE)
# mantle creases
d.path("M500,330 C520,346 540,352 566,354 M670,330 C650,346 630,352 604,354",
       "Mantle creases", fill=NONE, stroke=INK, strokeWidth=3,
       cap="round", opacity=35)

# eyes: half-lidded, profoundly unbothered by your merge
for side, ex in [("L", 522), ("R", 614)]:
    d.shape("ellipse", f"Eye {side} white", x=ex, y=428, width=34, height=38,
            fill="#E8DEE8", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Eye {side} pupil", x=ex+8, y=440, width=16, height=18,
            fill=INK, stroke=NONE)
    d.shape("ellipse", f"Eye {side} glint", x=ex+11, y=443, width=6, height=6,
            fill=MAGENTA, opacity=90, stroke=NONE)
    d.path(f"M{ex-2},436 C{ex+8},424 {ex+26},424 {ex+36},434",
           f"Eye {side} lid", fill=NONE, stroke=INK, strokeWidth=5,
           cap="round")
# beak-mouth: a small flat line. it has seen your rebases.
d.path("M572,506 C580,512 592,512 600,506", "Beak", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=506, y=492, width=26, height=13,
        fill="#B87EA0", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=640, y=492, width=26, height=13,
        fill="#B87EA0", opacity=40, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("OCTOMERGE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4ECE6", justify="center")
r = d.text("PLEASE RESOLVE CONFLICTS BEFORE I RESOLVE YOU", "Role",
           x=500, y=968, size=21, font="Virelai Sans", color="#9AB4A8",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=140)

d.finish("052.octomerge-V1R00")
