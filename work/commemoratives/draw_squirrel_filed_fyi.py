#!/usr/bin/env python3
"""squirrel-filed-fyi — commemorative plate V1R00. The Link Hoard: a squirrel
in profile, tail a curve of interlocking chain-links, tucking acorn-shaped
bookmarks into a hollow log of saved things. Autumn rust and hollow-log
brown; every link buried for winter. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("squirrel-filed-fyi — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241206"              # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None, extra=None):
    stops = [{"offset": 0, "color": c0}]
    if extra: stops += extra
    stops.append({"offset": 1, "color": c1})
    g = {"kind": "linear", "stops": stops}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def cubic(p0, c1, c2, p1, t):
    x = (1-t)**3*p0[0] + 3*(1-t)**2*t*c1[0] + 3*(1-t)*t*t*c2[0] + t**3*p1[0]
    y = (1-t)**3*p0[1] + 3*(1-t)**2*t*c1[1] + 3*(1-t)*t*t*c2[1] + t**3*p1[1]
    tx = 3*(1-t)**2*(c1[0]-p0[0]) + 6*(1-t)*t*(c2[0]-c1[0]) + 3*t*t*(p1[0]-c2[0])
    ty = 3*(1-t)**2*(c1[1]-p0[1]) + 6*(1-t)*t*(c2[1]-c1[1]) + 3*t*t*(p1[1]-c2[1])
    return (x, y), (tx, ty)

def acorn(cx, cy, s, label, lean=0):
    """An acorn-shaped bookmark: cap, nut body, stem, tiny ribbon tag."""
    tr = math.radians(lean); c, sn = math.cos(tr), math.sin(tr)
    def R(x, y):
        return (cx + (x-cx)*c - (y-cy)*sn, cy + (x-cx)*sn + (y-cy)*c)
    # nut body: teardrop, point down
    p = [R(cx, cy + 1.7*s), R(cx - 0.9*s, cy + 0.1*s), R(cx - 0.62*s, cy + 1.05*s),
         R(cx, cy + 1.35*s)]
    q = [R(cx + 0.9*s, cy + 0.1*s), R(cx + 0.62*s, cy + 1.05*s)]
    d.path(f"M{p[0][0]:.0f},{p[0][1]:.0f} C{p[1][0]:.0f},{p[1][1]:.0f} "
           f"{p[2][0]:.0f},{p[2][1]:.0f} {p[3][0]:.0f},{p[3][1]:.0f} "
           f"C{q[1][0]:.0f},{q[1][1]:.0f} {q[0][0]:.0f},{q[0][1]:.0f} {p[0][0]:.0f},{p[0][1]:.0f} Z",
           f"{label} nut", fill=lin("#C87B36", "#7A4216", (cx, cy), (cx, cy + 1.4*s)),
           stroke=INK, strokeWidth=2.5)
    # cap
    e0, e1 = R(cx - 0.95*s, cy + 0.1*s), R(cx + 0.95*s, cy + 0.1*s)
    t0 = R(cx, cy - 0.85*s)
    d.path(f"M{e0[0]:.0f},{e0[1]:.0f} Q{t0[0]:.0f},{t0[1]:.0f} {e1[0]:.0f},{e1[1]:.0f} "
           f"L{e0[0]:.0f},{e0[1]:.0f} Z", f"{label} cap",
           fill=lin("#5E3312", "#331A08", (cx, cy - 0.8*s), (cx, cy + 0.1*s)),
           stroke=INK, strokeWidth=2.5)
    # stem
    s0, s1 = R(cx, cy - 0.8*s), R(cx + 0.18*s, cy - 1.15*s)
    d.path(f"M{s0[0]:.0f},{s0[0+1]:.0f} L{s1[0]:.0f},{s1[1]:.0f}", f"{label} stem",
           fill=NONE, stroke="#3A2008", strokeWidth=3, cap="round")
    # ribbon tag off the point — the bookmark tail
    r0, r1, r2 = (R(cx - 0.12*s, cy + 1.3*s), R(cx + 0.1*s, cy + 1.3*s),
                  R(cx - 0.02*s, cy + 2.1*s))
    d.path(f"M{r0[0]:.0f},{r0[1]:.0f} L{r1[0]:.0f},{r1[1]:.0f} L{r2[0]:.0f},{r2[1]:.0f} Z",
           f"{label} tag", fill="#B8442A", stroke="#6E1E0E", strokeWidth=1.5)
    # cap stipple
    for j in range(3):
        dx = (-0.45 + 0.45 * j) * s
        p0, p1 = R(cx + dx - 0.1*s, cy - 0.5*s), R(cx + dx + 0.1*s, cy - 0.42*s)
        d.path(f"M{p0[0]:.0f},{p0[1]:.0f} L{p1[0]:.0f},{p1[1]:.0f}",
               f"{label} stipple {j+1}", fill=NONE, stroke="#7A4A20",
               strokeWidth=2, opacity=70, cap="round")

def leaf(cx, cy, s, ang, label, tone):
    tr = math.radians(ang); c, sn = math.cos(tr), math.sin(tr)
    def R(x, y):
        return (cx + (x-cx)*c - (y-cy)*sn, cy + (x-cx)*sn + (y-cy)*c)
    a, b, e = R(cx - s, cy), R(cx + s, cy), R(cx, cy - 0.45*s)
    f = R(cx, cy + 0.45*s)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} Q{e[0]:.0f},{e[1]:.0f} {b[0]:.0f},{b[1]:.0f} "
           f"Q{f[0]:.0f},{f[1]:.0f} {a[0]:.0f},{a[1]:.0f} Z", label,
           fill=tone, opacity=80, stroke="#3A2008", strokeWidth=1.5)
    m0, m1 = R(cx - 0.8*s, cy), R(cx + 0.8*s, cy)
    d.path(f"M{m0[0]:.0f},{m0[1]:.0f} L{m1[0]:.0f},{m1[1]:.0f}", f"{label} vein",
           fill=NONE, stroke="#3A2008", strokeWidth=1.5, opacity=60)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#160F08", "#060402", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#452A16"},
                 {"offset": 0.66, "color": "#221307"},
                 {"offset": 1, "color": "#0F0803"}),
        stroke="#A86434", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C890", strokeWidth=3, opacity=24)
# autumn flecks + a thin hunter's moon
d.shape("ellipse", "Moon", x=210, y=150, width=56, height=56,
        fill=rad({"offset": 0, "color": "#E8C890"},
                 {"offset": 1, "color": "#9A6E3E"}), opacity=80, stroke=NONE)
d.shape("ellipse", "Moon halo", x=176, y=116, width=124, height=124,
        fill=rad({"offset": 0, "color": "#E8C890", "opacity": 0.16},
                 {"offset": 1, "color": "#E8C890", "opacity": 0}), stroke=NONE)
for i, (x, y, w) in enumerate([(350,120,4),(660,140,4),(790,230,5),(170,430,4),
                               (845,470,4),(250,700,4),(760,720,5),(420,806,3),
                               (600,812,4),(150,590,3)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Fleck {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#E8C890", opacity=18, stroke=NONE)
# drifting leaves
leaf(310, 220, 16, -30, "Drift leaf 1", "#8A4A20")
leaf(720, 300, 13, 40, "Drift leaf 2", "#A8642A")
leaf(245, 520, 12, 15, "Drift leaf 3", "#6E3A18")

# --- ground: leaf litter closing on the disc arc --------------------------------
d.path("M206.1,756 Q500,676 793.9,756 A420,420 0 0 1 206.1,756 Z", "Mound",
       fill=lin("#2E1C0C", "#120A04", (500, 686), (500, 880)), stroke=NONE)
for i, (x, y, s, a, tone) in enumerate([(300,738,15,-20,"#7A421C"),(420,724,13,30,"#8A5220"),
                                        (560,722,14,-35,"#6E3A16"),(680,736,13,15,"#7A421C"),
                                        (775,758,12,-10,"#5E3010"),(240,764,12,25,"#6E3A16")]):
    leaf(x, y, s, a, f"Ground leaf {i+1}", tone)

# --- the hollow log ----------------------------------------------------------------
LY = 628                                    # log axis
# body: horizontal cylinder
d.path("M240,584 L742,584 L742,714 L240,714 Z", "Log body",
       fill=lin("#5E3A1C", "#2C1608", (500, 584), (500, 714)),
       stroke=INK, strokeWidth=5)
# top edge highlight + bottom contact shade
d.path("M244,588 L738,588", "Log top light", fill=NONE, stroke="#9A6A38",
       strokeWidth=3, opacity=60, cap="round")
d.shape("ellipse", "Log ground shadow", x=220, y=716, width=550, height=30,
        fill="#0A0502", opacity=50, stroke=NONE)
# bark striations
for i, y in enumerate((612, 640, 668, 696)):
    d.path(f"M250,{y} Q500,{y + (6 if i % 2 else -5)} 736,{y}",
           f"Bark {i+1}", fill=NONE, stroke="#1E0E04", strokeWidth=3,
           opacity=45, cap="round")
for i, (x, y, w) in enumerate([(300,598,26),(420,646,34),(560,600,22),(640,672,30),
                               (470,700,24),(700,630,20)]):
    d.path(f"M{x},{y} L{x+w},{y - 2}", f"Bark nick {i+1}", fill=NONE,
           stroke="#7A4E26", strokeWidth=2.5, opacity=55, cap="round")
# the hollow: dark opening at the left end, lit inner rim
d.shape("ellipse", "Hollow", x=176, y=580, width=128, height=138,
        fill=rad({"offset": 0, "color": "#0E0602"},
                 {"offset": 0.75, "color": "#160A04"},
                 {"offset": 1, "color": "#4A2C12"}),
        stroke=INK, strokeWidth=5)
d.shape("ellipse", "Hollow glow", x=196, y=606, width=92, height=96,
        fill=rad({"offset": 0, "color": "#C8844A", "opacity": 0.14},
                 {"offset": 1, "color": "#C8844A", "opacity": 0}), stroke=NONE)
d.path("M186,600 Q186,706 240,712", "Hollow rim light", fill=NONE,
       stroke="#C8844A", strokeWidth=4, opacity=70, cap="round")
# saved things inside the hollow: loose links + acorn bookmarks
for i, (x, y, a) in enumerate(((218, 672, -15), (246, 652, 25), (228, 694, 10))):
    d.path(rot_rect_path(x, y, 26, 15, a), f"Hoarded link {i+1}", fill=NONE,
           stroke="#B4703A", strokeWidth=5)
acorn(258, 610, 14, "Hoard acorn 1", lean=-12)
acorn(230, 630, 12, "Hoard acorn 2", lean=14)
acorn(268, 646, 11, "Hoard acorn 3", lean=-6)
# one more acorn-bookmark mid-tuck, half out of the hollow mouth
acorn(318, 640, 13, "Mid-tuck acorn", lean=30)

# --- the squirrel, profile facing left, standing on the log ------------------------
SX = 610                                    # body centre line
# cast shadow on the log
d.shape("ellipse", "Squirrel shadow", x=560, y=590, width=160, height=18,
        fill="#0E0602", opacity=45, stroke=NONE)
# hind foot on the log top
d.path("M586,606 C584,588 598,576 620,576 C660,576 690,590 692,606 Z",
       "Hind foot", fill=lin("#8A4518", "#542408", (600, 576), (690, 606)),
       stroke=INK, strokeWidth=4)
# haunch + back: the body mass
d.path("M692,606 C700,540 690,470 648,432 C622,408 596,406 584,424 "
       "C572,442 578,470 588,494 C572,540 578,586 586,606 Z",
       "Body", fill=lin("#B05A26", "#5E2808", (640, 410), (640, 610),
                        extra=[{"offset": 0.55, "color": "#8A4218"}]),
       stroke=INK, strokeWidth=5)
# cream belly
d.path("M588,470 C578,520 580,570 590,600 C600,560 604,510 600,478 Z",
       "Belly", fill="#E8C890", opacity=75, stroke=NONE)
# head: cheek + muzzle tapering left
d.path("M584,424 C556,400 524,394 504,408 C490,418 492,438 508,447 "
       "C530,460 568,456 584,440 Z",
       "Head", fill=lin("#B05A26", "#6E3010", (540, 396), (540, 460)),
       stroke=INK, strokeWidth=5)
# ear: pointed with a small tuft
d.path("M582,414 C574,398 574,372 586,352 C598,372 608,390 612,406 "
       "L610,414 Z", "Ear",
       fill=lin("#9A4E20", "#5E2808", (593, 352), (593, 414)),
       stroke=INK, strokeWidth=4)
d.path("M583,362 L573,346 L586,353 Z", "Ear tuft", fill="#3A1804",
       stroke=NONE)
# eye + glint
d.shape("ellipse", "Eye", x=528, y=414, width=14, height=16,
        fill="#1E0E04", stroke=NONE)
d.shape("ellipse", "Eye glint", x=531, y=417, width=4, height=4,
        fill="#F4E8CC", opacity=90, stroke=NONE)
# nose + whisker hint
d.shape("ellipse", "Nose", x=495, y=420, width=10, height=9,
        fill="#2E1608", stroke=NONE)
d.path("M510,438 Q532,444 554,440", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=2.5, opacity=70, cap="round")
# foreleg reaching to the acorn in its paws
d.path("M596,486 C578,496 566,510 560,526", "Foreleg", fill=NONE,
       stroke="#7A3A14", strokeWidth=12, cap="round")
d.shape("ellipse", "Paw", x=548, y=514, width=19, height=15,
        fill="#8A4518", stroke=INK, strokeWidth=3)
# the acorn-bookmark being tucked
acorn(538, 534, 16, "Tucked acorn", lean=-16)
# second paw overlapping the acorn
d.shape("ellipse", "Paw 2", x=552, y=544, width=15, height=12,
        fill="#8A4518", stroke=INK, strokeWidth=2.5)

# --- the chain-link tail: links arcing from rump up and curling forward -------------
TAIL = [(700, 596), (782, 520), (792, 400), (712, 352)]
links = []
for t in [0.10, 0.24, 0.38, 0.52, 0.66, 0.80, 0.92]:
    (x, y), (tx, ty) = cubic(*TAIL, t)
    links.append((x, y, math.degrees(math.atan2(ty, tx))))
# tail-tip link curls inward
links.append((676, 348, 168))
sizes = [(48, 26), (46, 25), (44, 24), (42, 23), (40, 22), (38, 21),
         (36, 19), (32, 17)]
# furry nub where the chain meets the rump
d.path("M684,592 Q704,580 722,570", "Tail root", fill=NONE,
       stroke="#7A4218", strokeWidth=16, cap="round")
d.path("M684,592 Q704,580 722,570", "Tail root outline", fill=NONE,
       stroke=INK, strokeWidth=20, cap="round", opacity=25)
for i, (x, y, a) in enumerate(links):
    rot = a + (18 if i % 2 else -18)
    lw, lh = sizes[i]
    d.path(rot_rect_path(x, y, lw, lh, rot), f"Tail link {i+1}", fill=NONE,
           stroke=lin("#C97E3E", "#7A4218", (x - 20, y - 12), (x + 20, y + 12)),
           strokeWidth=8)
    # link sheen
    hx, hy = x - 10 * math.cos(math.radians(rot)), y - 8
    d.path(rot_rect_path(hx, hy, lw * 0.42, lh * 0.4, rot), f"Link sheen {i+1}",
           fill=NONE, stroke="#F0C88A", strokeWidth=3, opacity=60)

# --- name + role ------------------------------------------------------------------
d.text("SQUIRREL.FILED.FYI", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#F0DCB0", justify="center")
LINE2, SZ2, TRK = "PERSONAL LINK-LOG", 24, 320
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#C88A4E", justify="center")
d.cmd("text.setStyle", "Second line tracking", ids=[r["id"]], tracking=TRK)
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

d.finish("squirrel-filed-fyi-V1R00")
