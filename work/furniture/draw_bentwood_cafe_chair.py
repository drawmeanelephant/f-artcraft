#!/usr/bin/env python3
"""Bentwood cafe chair — field plate V1R00. Thonet No. 14 in a near-side
three-quarter view: one bent U-piece forms both back legs and the crest
rail, a second bent hoop fills the back, round caned seat, and the
signature stretcher ring running round all four splayed legs. Dark
ebonised gloss on a cafe-green plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bentwood Cafe Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def mix(c0, c1, t):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02X}" for p, q in zip(a, b))

# ebonised bentwood palette — near-black with warm mahogany lights
WOOD      = "#2A1D12"
WOOD_FAR  = "#1D130B"
WOOD_HI   = "#8A6238"
WOOD_GL   = "#F2D9A8"
CANE_ST   = [(0, "#E8C684"), (0.65, "#C69C58"), (1, "#9A7038")]
CANE_LN   = "#8A5E2C"

# every hand-placed point, for the disc-fit assertion at the end
FIT = []
def note(*pts):
    FIT.extend(pts)

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#141A12"), (1, "#060806")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E7A58"), (0.6, "#3E563C"), (1, "#1C2A1C")), stroke=NONE)
d.shape("ellipse", "Window light", x=120, y=80, width=560, height=500,
        fill=rad((0, "#FFF2C8", 0.16), (1, "#FFF2C8", 0)), stroke=NONE)
# cafe window: tall arch with muntin bars, faint on the plate wall
wx, wr = 290, 132
d.path(f"M{wx - wr},470 L{wx - wr},300 A{wr},{wr} 0 0 1 {wx + wr},300 L{wx + wr},470",
       "Cafe window arch", fill=NONE, stroke="#B8CCA8", strokeWidth=7, opacity=16)
for i, yy in enumerate([338, 392]):
    d.path(f"M{wx - wr},{yy} L{wx + wr},{yy}", f"Window muntin h{i+1}",
           fill=NONE, stroke="#B8CCA8", strokeWidth=5, opacity=12)
d.path(f"M{wx},168 L{wx},470", "Window muntin v",
       fill=NONE, stroke="#B8CCA8", strokeWidth=5, opacity=12)
for i, (x, y, w) in enumerate([(215, 215, 6), (775, 235, 7), (165, 620, 6), (830, 585, 7),
                               (430, 105, 6), (640, 110, 7), (850, 400, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#A8BE98", opacity=35, stroke=NONE)

HZN = 695
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#4A3A26", 0.55), (1, "#1C150C", 0.9)), stroke=NONE)
for i, yy in enumerate([742, 792, 838]):
    xx = math.sqrt(PR ** 2 - (yy - PCY) ** 2) - 6
    d.path(f"M{PCX - xx:.1f},{yy} L{PCX + xx:.1f},{yy}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#100C06", strokeWidth=3, opacity=30)
d.shape("ellipse", "Chair shadow", x=300, y=742, width=420, height=92,
        fill=rad((0, "#080604", 0.62), (1, "#080604", 0)), stroke=NONE)

# --- geometry ---------------------------------------------------------------------
SCX, SCY, SRX, SRY = 490, 575, 150, 42        # seat ellipse
RCX, RCY, RRX, RRY = 512, 692, 172, 40        # stretcher-ring ellipse

def leg_path(attach, mid, foot):
    return (f"M{foot[0]},{foot[1]} C{foot[0] + (mid[0] - foot[0]) * 0.55:.0f},{foot[1] - 90:.0f} "
            f"{mid[0]},{mid[1] + 60} {mid[0]},{mid[1]} "
            f"C{mid[0]},{mid[1] - 40} {attach[0]},{attach[1] + 30} {attach[0]},{attach[1]}")

def leg(label, attach, mid, foot, stroke, hi_side, sw=14):
    note(attach, mid, foot)
    d.path(leg_path(attach, mid, foot), label, fill=NONE, stroke=stroke, strokeWidth=sw,
           cap="round", join="round")
    d.path(leg_path((attach[0] + hi_side, attach[1]), (mid[0] + hi_side, mid[1]),
                    (foot[0] + hi_side, foot[1])),
           f"{label} edge light", fill=NONE, stroke=WOOD_HI, strokeWidth=4.5,
           cap="round", opacity=55)

# stretcher ring: back arc first (legs drawn over it), front arc later
a0, a1 = math.radians(196), math.radians(344)
rb0 = (RCX + RRX * math.cos(a0), RCY + RRY * math.sin(a0))
rb1 = (RCX + RRX * math.cos(a1), RCY + RRY * math.sin(a1))
d.path(f"M{rb0[0]:.0f},{rb0[1]:.0f} A{RRX},{RRY} 0 0 1 {rb1[0]:.0f},{rb1[1]:.0f}",
       "Ring back arc", fill=NONE, stroke=WOOD_FAR, strokeWidth=9, cap="round")
note(rb0, rb1)

# --- the U-piece: one bent member, both back legs + crest --------------------------
U = ("M622,788 C610,706 592,642 586,562 C578,470 569,382 585,287 "
     "C590,240 652,234 656,279 C651,375 651,464 663,554 C671,644 688,712 701,780")
note((622, 788), (701, 780), (620, 235))
d.path(U, "Back U-piece", fill=NONE, stroke=WOOD, strokeWidth=15, cap="round", join="round")
# warm edge lights along the uprights and over the crest
d.path("M617,760 C606,690 591,634 585,560 C578,472 571,384 585,289",
       "U left edge light", fill=NONE, stroke=WOOD_HI, strokeWidth=5, cap="round", opacity=60)
d.path("M588,282 C595,246 645,242 650,280",
       "Crest edge light", fill=NONE, stroke=WOOD_HI, strokeWidth=5, cap="round", opacity=55)
d.path("M660,300 C655,380 656,462 666,548",
       "U right edge light", fill=NONE, stroke=WOOD_HI, strokeWidth=4, cap="round", opacity=40)
d.path("M596,252 C612,243 634,241 648,249", "Crest glint",
       fill=NONE, stroke=WOOD_GL, strokeWidth=3.5, cap="round", opacity=80)

# far back leg ghosted just right of the U's far side (depth cue)
leg("Far back leg", (684, 560), (702, 656), (722, 756), WOOD_FAR, 3, sw=10)

# inner bentwood back hoop — ends socketed into the uprights
d.path("M578,466 C572,388 586,332 618,326 C646,321 655,374 656,452",
       "Back inner hoop", fill=NONE, stroke=WOOD, strokeWidth=11, cap="round", join="round")
d.path("M580,458 C576,390 590,338 618,332", "Hoop edge light",
       fill=NONE, stroke=WOOD_HI, strokeWidth=4, cap="round", opacity=55)

# front legs (near in full colour, far ghosted)
leg("Far front leg", (418, 600), (408, 690), (392, 776), WOOD_FAR, 3)
leg("Near front leg", (370, 598), (356, 686), (334, 788), WOOD, -4)

# stretcher ring: front arc crosses in front of the front legs
a2, a3 = math.radians(16), math.radians(164)
rf0 = (RCX + RRX * math.cos(a2), RCY + RRY * math.sin(a2))
rf1 = (RCX + RRX * math.cos(a3), RCY + RRY * math.sin(a3))
d.path(f"M{rf0[0]:.0f},{rf0[1]:.0f} A{RRX},{RRY} 0 0 1 {rf1[0]:.0f},{rf1[1]:.0f}",
       "Ring front arc", fill=NONE, stroke=WOOD, strokeWidth=9, cap="round")
d.path(f"M{rf0[0] - 4:.0f},{rf0[1] - 4:.0f} A{RRX},{RRY} 0 0 1 {rf1[0] - 30:.0f},{rf1[1] - 2:.0f}",
       "Ring front light", fill=NONE, stroke=WOOD_HI, strokeWidth=3.5, cap="round", opacity=55)
note(rf0, rf1)

# --- seat: bentwood frame ring + woven cane ----------------------------------------
d.shape("ellipse", "Seat frame", x=SCX - SRX - 8, y=SCY - SRY - 4, width=2 * (SRX + 8), height=2 * (SRY + 8),
        fill=lin(SCX, SCY - SRY, SCX, SCY + SRY + 10, (0, "#4A341E"), (0.5, "#2A1D12"), (1, "#160E08")),
        stroke=NONE)
note((SCX - SRX - 8, SCY), (SCX + SRX + 8, SCY))
# frame rim light on the front edge
d.path(f"M{SCX - SRX - 4},{SCY + 2} A{SRX + 4},{SRY + 6} 0 0 0 {SCX + SRX + 4},{SCY + 2}",
       "Seat rim light", fill=NONE, stroke=WOOD_HI, strokeWidth=4.5, cap="round", opacity=60)
d.shape("ellipse", "Cane seat", x=SCX - SRX + 6, y=SCY - SRY + 2, width=2 * (SRX - 6), height=2 * (SRY - 2),
        fill=rad((0, "#EFCF92"), (0.6, "#CDA35F"), (1, "#A87F42")), stroke="#6A4A22", strokeWidth=3)

# hex weave: three line families at 0 / +58 / -58 degrees, chords clipped to the cane ellipse
def chord(cx, cy, rx, ry, ang, off):
    dx, dy = math.cos(ang), math.sin(ang)
    nx, ny = -dy, dx
    a = (dx / rx) ** 2 + (dy / ry) ** 2
    c = (off * nx / rx) ** 2 + (off * ny / ry) ** 2 - 1
    t = math.sqrt(max(0.0, -c / a))
    return ((cx + nx * off - dx * t, cy + ny * off - dy * t),
            (cx + nx * off + dx * t, cy + ny * off + dy * t))

ccx, ccy, crx, cry = SCX, SCY + 2, SRX - 12, SRY - 8
k = 0
for fam, ang in enumerate([0, math.radians(58), -math.radians(58)]):
    off = -cry - 40
    while off <= cry + 40:
        p0, p1 = chord(ccx, ccy, crx, cry, ang, off)
        d.path(f"M{p0[0]:.0f},{p0[1]:.0f} L{p1[0]:.0f},{p1[1]:.0f}", f"Weave {k+1}",
               fill=NONE, stroke=CANE_LN, strokeWidth=2.4, opacity=58)
        k += 1
        off += 11
# cane sheen
d.shape("ellipse", "Cane sheen", x=SCX - 110, y=SCY - 34, width=180, height=34,
        fill=rad((0, "#FFF4D0", 0.35), (1, "#FFF4D0", 0)), stroke=NONE)

# --- fit check ---------------------------------------------------------------------
for x, y in FIT:
    assert math.hypot(x - PCX, y - PCY) <= PR - 30, (x, y)

# --- rim + captions ------------------------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0C110B", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4C8", strokeWidth=3, opacity=26)

d.text("BENTWOOD CAFE CHAIR", "Name", x=500, y=940, size=56, font="Virelai Sans",
       color="#F2EDD8", justify="center")
LINE2, SZ2, TRK = "BEECH · CANE · LACQUER", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C8D2A8", justify="center")
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

d.finish("bentwood-cafe-chair-V1R00")
