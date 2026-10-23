#!/usr/bin/env python3
"""Pedestal table — field plate V1R00. One leg doing all the work: a turned
column flaring up into a round top with a lit edge, the base splayed on
four feet. White lacquer against a deep teal plate. Near-side view,
1000x1000. House style: gradients + translucent shading, never flat.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pedestal Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

LACQ_HI  = "#FAF8F2"    # lit lacquer
LACQ_MID = "#D9D5C8"
LACQ_LO  = "#9A968A"
LACQ_INK = "#4A463C"

FIT = []
def note(*pts):
    FIT.extend(pts)

# --- backdrop + plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#0E1A1A"), (1, "#04080A")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3E7A72"), (0.6, "#26554E"), (1, "#0E2826")), stroke=NONE)
d.shape("ellipse", "Overhead light", x=180, y=70, width=560, height=440,
        fill=rad((0, "#EAF6EC", 0.18), (1, "#EAF6EC", 0)), stroke=NONE)
for i, (x, y, w) in enumerate([(205, 215, 6), (780, 240, 7), (168, 615, 6), (828, 590, 7),
                               (425, 102, 6), (645, 108, 7), (152, 420, 6), (855, 405, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#8EB8AE", opacity=32, stroke=NONE)

HZN = 700
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#2C2620", 0.55), (1, "#100D0A", 0.9)), stroke=NONE)
d.shape("ellipse", "Table shadow", x=280, y=756, width=440, height=86,
        fill=rad((0, "#06080A", 0.6), (1, "#06080A", 0)), stroke=NONE)

# --- four splayed feet (tops covered by the column base lip) ------------------------------
def foot(label, start, ctrl, end, sw, color, hi_color=None, pad=True):
    note(end)
    d.path(f"M{start[0]},{start[1]} Q{ctrl[0]},{ctrl[1]} {end[0]},{end[1]}",
           label, fill=NONE, stroke=color, strokeWidth=sw, cap="round")
    if hi_color:
        d.path(f"M{start[0]},{start[1] - sw * 0.22:.0f} Q{ctrl[0]},{ctrl[1] - sw * 0.22:.0f} {end[0]},{end[1] - sw * 0.22:.0f}",
               f"{label} light", fill=NONE, stroke=hi_color, strokeWidth=sw * 0.38,
               cap="round", opacity=60)
    if pad:
        d.shape("ellipse", f"{label} pad", x=end[0] - 20, y=end[1] - 2, width=40, height=13,
                fill=rad((0, "#5A564C", 0.85), (1, "#5A564C", 0.5)), stroke=NONE)

# rear feet first: slimmer tips landing higher (farther back), just past the skirt edges
foot("Rear foot L", (458, 686), (398, 712), (334, 742), 15, "#8A867A")
foot("Rear foot R", (550, 688), (612, 710), (678, 738), 15, "#7C786C")
# front feet: full lacquer, wider
foot("Front foot L", (472, 698), (432, 744), (352, 794), 24, "#CFCAB9", hi_color="#FDFBF4")
foot("Front foot R", (538, 700), (592, 746), (672, 788), 24, "#B4B0A0", hi_color="#E4E0D2")

# --- the column: turned profile, smoothed ---------------------------------------------
# right-side silhouette control points, neck (just under the top) down to the foot line
r_pts = [(534, 412), (528, 438), (530, 458), (550, 472), (553, 488), (542, 505),
         (540, 528), (556, 545), (561, 565), (548, 588), (545, 615), (557, 636),
         (560, 655), (575, 668), (585, 686), (610, 700), (634, 712), (640, 726)]
CX = 500
l_pts = [(2 * CX - x, y) for x, y in reversed(r_pts)]

def smooth_chain(pts):
    """Path through pts, quadratic-smoothed: vertices at midpoints, controls at pts."""
    seg = f"M{pts[0][0]},{pts[0][1]} "
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
        seg += f"Q{pts[i][0]},{pts[i][1]} {mx:.0f},{my:.0f} "
    seg += f"L{pts[-1][0]},{pts[-1][1]}"
    return seg

col = smooth_chain(r_pts) + " L" + " L".join(f"{x},{y}" for x, y in [l_pts[0]]) + " "
# left side drawn as its own smoothed chain back up, closing at the neck
col = smooth_chain(r_pts) + f" L{l_pts[0][0]},{l_pts[0][1]} "
seg_l = f""
for i in range(1, len(l_pts) - 1):
    mx, my = (l_pts[i][0] + l_pts[i + 1][0]) / 2, (l_pts[i][1] + l_pts[i + 1][1]) / 2
    seg_l += f"Q{l_pts[i][0]},{l_pts[i][1]} {mx:.0f},{my:.0f} "
col += seg_l + " Z"
note(r_pts[0], r_pts[-1], l_pts[-1])

d.path(col, "Column silhouette", fill=lin(430, 500, 575, 500,
       (0, LACQ_MID), (0.35, LACQ_HI), (0.75, LACQ_MID), (1, "#6E6A5E")),
       stroke=LACQ_INK, strokeWidth=3.5, join="round")
# turning grooves: horizontal arcs across the column at the profile pinch points
def col_w(y):
    """half-width of the column at height y, interpolated over r_pts."""
    for i in range(len(r_pts) - 1):
        (x0, y0), (x1, y1) = r_pts[i], r_pts[i + 1]
        if y0 <= y <= y1:
            return (x0 - CX) + (x1 - x0) * (y - y0) / (y1 - y0)
    return r_pts[-1][0] - CX

for i, yy in enumerate([446, 498, 535, 580, 622, 652, 692]):
    w = col_w(yy) - 5
    d.path(f"M{CX - w:.0f},{yy} A{w:.0f},{w * 0.24:.0f} 0 0 0 {CX + w:.0f},{yy}",
           f"Turning groove {i+1}", fill=NONE, stroke="#7A7668", strokeWidth=3.2, opacity=45)
for i, yy in enumerate([462, 552, 610, 668]):
    w = col_w(yy) - 4
    d.path(f"M{CX - w:.0f},{yy} A{w:.0f},{w * 0.22:.0f} 0 0 0 {CX + w:.0f},{yy}",
           f"Turning bead {i+1}", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=45)
# soft shading bands: shadow on the right of the column, sheen on the left
d.shape("ellipse", "Column sheen", x=458, y=430, width=46, height=250,
        fill=rad((0, "#FFFFFF", 0.4), (1, "#FFFFFF", 0)), stroke=NONE)
d.shape("ellipse", "Column shade", x=528, y=480, width=52, height=230,
        fill=rad((0, "#3C382E", 0.35), (1, "#3C382E", 0)), stroke=NONE)

# --- the round top -----------------------------------------------------------------------
TX, TY, TRX, TRY = 500, 384, 196, 54
# flare where the column meets the top: underside shadow disc
d.shape("ellipse", "Top underside", x=TX - 96, y=TY + 18, width=192, height=34,
        fill=rad((0, "#201C16", 0.7), (1, "#201C16", 0)), stroke=NONE)
# edge band (the table's apron/thickness)
d.shape("ellipse", "Top edge band", x=TX - TRX, y=TY - TRY + 10, width=2 * TRX, height=2 * TRY,
        fill=lin(TX, TY - TRY, TX, TY + TRY + 8, (0, "#B4B0A2"), (0.5, "#8E8A7C"), (1, "#565248")),
        stroke=LACQ_INK, strokeWidth=3)
# the lit surface
d.shape("ellipse", "Top surface", x=TX - TRX + 6, y=TY - TRY - 2, width=2 * (TRX - 6), height=2 * (TRY - 4),
        fill=rad((0, "#FDFBF6"), (0.55, "#E6E2D4"), (1, "#B2AE9E")),
        stroke="#7A7668", strokeWidth=2.5)
note((TX - TRX, TY), (TX + TRX, TY), (TX, TY - TRY))
# lit edge: bright arc along the front-left rim
d.path(f"M{TX - TRX + 10},{TY + 6} A{TRX - 2},{TRY - 2} 0 0 0 {TX - 30},{TY + TRY - 2}",
       "Top lit edge", fill=NONE, stroke="#FFFFFF", strokeWidth=5, cap="round", opacity=75)
d.shape("ellipse", "Top sheen", x=TX - 150, y=TY - 44, width=210, height=40,
        fill=rad((0, "#FFFFFF", 0.5), (1, "#FFFFFF", 0)), stroke=NONE)
# faint cool reflection on the right of the top
d.shape("ellipse", "Top cool pool", x=TX + 40, y=TY - 20, width=120, height=46,
        fill=rad((0, "#9FB8B0", 0.25), (1, "#9FB8B0", 0)), stroke=NONE)

# --- fit check ----------------------------------------------------------------------------
for x, y in FIT:
    assert math.hypot(x - PCX, y - PCY) <= PR - 30, (x, y)

# --- rim + captions ------------------------------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#08100E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E0D6", strokeWidth=3, opacity=26)

d.text("PEDESTAL TABLE", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#EAF2EA", justify="center")
LINE2, SZ2, TRK = "BEECH · WHITE LACQUER", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#A8C8BC", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit

b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("pedestal-table-V1R00")
