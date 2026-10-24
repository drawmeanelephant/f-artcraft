#!/usr/bin/env python3
"""Recliner — furniture field plate V1R00. Near-side view with a slight
three-quarter from the front right: an overstuffed leather recliner caught
mid-lounge — back slab raked ~20 degrees, rolled arms, footrest swung up on
its scissor linkage. Chocolate leather on a warm umber plate. 1000x1000.
Modelled in 3D (inches), projected with fixed yaw + pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Recliner — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241109"   # warm dark umber, not black
EXTENT = []


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def smooth(pts, closed=False, move=True):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection -------------------------------------------------------------
# x = chair's right, y = up, z = toward the back. Yaw brings the right flank
# toward the viewer; pitch looks down onto the seat and footrest.
YAW, PITCH = math.radians(20), math.radians(16)
S, OX, OY = 15.4, 516.0, 772.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * math.sin(YAW) + z * math.cos(YAW)


def puff(name, pts3, fill, ink=3, bulge=9, join="round"):
    """A puffy quad: 4 3D corners projected, edge midpoints bowed outward
    by `bulge` points — reads as an overstuffed panel."""
    c2 = [P(*p) for p in pts3]
    cx = sum(p[0] for p in c2) / 4
    cy = sum(p[1] for p in c2) / 4
    out = []
    n = len(c2)
    for i in range(n):
        a, b = c2[i], c2[(i + 1) % n]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ex, ey = mx - cx, my - cy
        L = math.hypot(ex, ey) or 1
        out += [a, (mx + ex / L * bulge, my + ey / L * bulge)]
    d.path(smooth(out, closed=True), name, fill=fill, stroke=INK,
           strokeWidth=ink, join=join)
    return out


def sheen(name, cx, cy, r, color, hi=40):
    d.shape("ellipse", name, x=round(cx - r), y=round(cy - r * 0.62), width=round(r * 2),
            height=round(r * 1.24), fill=rad((0, color, hi), (1, color, 0)), stroke=NONE)


# --- palette -------------------------------------------------------------------
LEATHER_HI = lin((0, 180), (0, 700), (0, "#B9764A"), (0.55, "#8A4E2C"), (1, "#4E2814"))
LEATHER_DK = lin((0, 180), (0, 700), (0, "#8A5432"), (0.6, "#5E3419"), (1, "#381C0C"))
LEATHER_SIDE = lin((0, 180), (0, 700), (0, "#7A4626"), (1, "#2E1608"))

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#181008"), (1, "#070504")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6A5236", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4E3D2C"), (0.6, "#332619"), (1, "#191109")),
        stroke="#0F0A05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C894", strokeWidth=3, opacity=26)
# lazy sunday sun through a window, upper left
d.shape("ellipse", "Back glow", x=140, y=90, width=580, height=580,
        fill=rad((0, "#F5C078", 28), (0.55, "#C08048", 10), (1, "#7A4A24", 0)), stroke=NONE)

# floor: a band that closes on the disc's own arc
FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#574430", 32), (1, "#171008", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E2C99E", strokeWidth=2, opacity=20)

# --- geometry (inches) -----------------------------------------------------------
# base plinth
BASE = dict(x=10.6, zf=-9.2, zb=8.6, y0=0.0, y1=9.0)
# arms: outer face, front face + roll
ARM = dict(xi=9.2, xo=13.2, zf=-9.8, zb=8.6, y0=8.5, yback=25.5, yfront=22.2)
# seat cushion between the arms
SEAT = dict(x=9.4, zf=-8.6, zb=6.8, y0=12.6, y1=15.8)
# reclined back slab: rises and rakes back; wider at the shoulders
BACK = dict(xb=8.3, xt=9.5, y0=13.8, z0=5.2, y1=34.4, z1=13.6, t=3.0)
# footrest pad, swung up
PAD = dict(x=8.2, za=-9.4, zf=-16.8, ya=11.7, yf=15.2, t=3.3)

# shadow under the whole sprawl
d.shape("ellipse", "Chair shadow", x=290, y=714, width=500, height=104,
        fill=rad((0, "#050301", 68), (0.6, "#050301", 32), (1, "#050301", 0)), stroke=NONE)
fx, fy = P(0, 1.4, -13.5)
d.shape("ellipse", "Footrest shadow", x=round(fx - 140), y=round(fy - 6), width=280, height=34,
        fill=rad((0, "#050301", 48), (1, "#050301", 0)), stroke=NONE)

# --- base plinth: front + near side ---------------------------------------------
puff("Base front", [(-BASE["x"], BASE["y1"], BASE["zf"]), (BASE["x"], BASE["y1"], BASE["zf"]),
                    (BASE["x"], BASE["y0"], BASE["zf"]), (-BASE["x"], BASE["y0"], BASE["zf"])],
     lin((0, 620), (0, 780), (0, "#6E4225"), (1, "#301708")), ink=3.5, bulge=10)
puff("Base side", [(BASE["x"], BASE["y1"], BASE["zf"]), (BASE["x"], BASE["y1"], BASE["zb"]),
                   (BASE["x"], BASE["y0"], BASE["zb"]), (BASE["x"], BASE["y0"], BASE["zf"])],
     LEATHER_SIDE, ink=3, bulge=7)

# --- footrest linkage (in front of the base, under the pad) -------------------------
def link(x, a, b, w, nm):
    A, B = P(x, a[0], a[1]), P(x, b[0], b[1])
    d.path("M%.1f,%.1f L%.1f,%.1f" % (A + B), nm, fill=NONE,
           stroke="#1E140E", strokeWidth=w, cap="round")
    d.path("M%.1f,%.1f L%.1f,%.1f" % (A + B), nm + " light", fill=NONE,
           stroke="#8A7A66", strokeWidth=max(1.5, w * 0.25), opacity=40, cap="round")


for x, nm in ((-7.2, "far"), (7.2, "near")):
    link(x, (4.8, -8.4), (12.0, -13.8), 4.2, f"Link {nm} a")
    link(x, (11.6, -8.6), (5.4, -13.4), 4.2, f"Link {nm} b")

# --- back slab ----------------------------------------------------------------------
# the slab's right side face (toward viewer) and its top face sell the recline
puff("Back side", [(BACK["xt"], BACK["y1"], BACK["z1"]),
                   (BACK["xt"], BACK["y0"] + 0.6, BACK["z0"]),
                   (BACK["xt"] - 0.2, BACK["y0"], BACK["z0"] + 2.8),
                   (BACK["xt"] - 0.6, BACK["y1"] - 1.2, BACK["z1"] + 2.5)],
     LEATHER_SIDE, ink=2.5, bulge=4)
puff("Back top", [(-BACK["xt"], BACK["y1"], BACK["z1"]),
                  (BACK["xt"], BACK["y1"], BACK["z1"]),
                  (BACK["xt"] - 0.6, BACK["y1"] - 1.3, BACK["z1"] + 2.5),
                  (-BACK["xt"] + 0.6, BACK["y1"] - 1.3, BACK["z1"] + 2.5)],
     lin((0, 200), (0, 260), (0, "#9A5E36"), (1, "#4A2410")), ink=3, bulge=6)
back_front = puff("Back cushion", [(-BACK["xb"], BACK["y0"], BACK["z0"]),
                                   (BACK["xb"], BACK["y0"], BACK["z0"]),
                                   (BACK["xt"], BACK["y1"], BACK["z1"]),
                                   (-BACK["xt"], BACK["y1"], BACK["z1"])],
                  lin((0, 290), (0, 640), (0, "#C88454"), (0.45, "#9A5A32"), (1, "#562C14")),
                  ink=4, bulge=15)
# two channel seams divide the back into its cushions
for i, ys in enumerate((21.5, 29.0)):
    zc = BACK["z0"] + (ys - BACK["y0"]) * (BACK["z1"] - BACK["z0"]) / (BACK["y1"] - BACK["y0"]) - 0.15
    xl = BACK["xb"] + (BACK["xt"] - BACK["xb"]) * (ys - BACK["y0"]) / (BACK["y1"] - BACK["y0"]) - 0.7
    seam = [P(x, ys, zc) for x in (-xl, -xl * 0.35, xl * 0.35, xl)]
    d.path(smooth(seam), f"Back seam {i+1}", fill=NONE, stroke="#3A1C0C",
           strokeWidth=3.2, opacity=55, cap="round")
# sheen pooling on the cushion crown
bx, by = P(-3.5, 29, 8.9)
sheen("Back sheen", bx, by, 70, "#F5C896", 30)

# --- arms -----------------------------------------------------------------------------
def arm(side, near):
    """side = +1 chair's right (near), -1 far."""
    xo = side * ARM["xo"]
    xi = side * ARM["xi"]
    if near:
        # outer face: front-to-back quad, top edge sloping down to the roll front
        puff("Arm outer near",
             [(xo, ARM["y0"], ARM["zf"]), (xo, ARM["y0"], ARM["zb"]),
              (xo, ARM["yback"], ARM["zb"]), (xo, ARM["yfront"], ARM["zf"] + 0.6)],
             LEATHER_HI, ink=3.5, bulge=12)
    # front face carrying the roll
    topv = ARM["yfront"] + (2.0 if not near else 1.4)
    puff(f"Arm front {'near' if near else 'far'}",
         [(xi, ARM["y0"] + 2, ARM["zf"]), (xo, ARM["y0"] + 2, ARM["zf"]),
          (xo, topv, ARM["zf"] + 0.6),
          (xi, topv - (0.4 if near else 0.9), ARM["zf"] + 0.6)],
         lin((0, 440), (0, 700), (0, "#C88454"), (0.5, "#8A4E2C"), (1, "#4A2410"))
         if near else LEATHER_DK, ink=3, bulge=10)
    # roll: fat ellipse cap on the front-top corner
    rx, ry = P((xo + xi) / 2 + (0.7 if near else -0.2), ARM["yfront"] + (0.5 if near else -0.35), ARM["zf"] + 0.9)
    rr = 2.5 * S * (0.66 if near else 0.56)
    d.shape("ellipse", f"Arm roll {'near' if near else 'far'}",
            x=round(rx - rr), y=round(ry - rr * 0.82), width=round(rr * 2),
            height=round(rr * 1.64),
            fill=rad((0, "#D89460"), (0.6, "#9A5A32"), (1, "#542C14")),
            stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Arm roll seam {'near' if near else 'far'}",
            x=round(rx - rr * 0.62), y=round(ry - rr * 0.5), width=round(rr * 1.24),
            height=round(rr), fill=NONE, stroke="#3A1C0C", strokeWidth=2.4, opacity=55)


arm(-1, False)
arm(+1, True)

# --- seat cushion ----------------------------------------------------------------------
puff("Seat cushion", [(-SEAT["x"], SEAT["y1"], SEAT["zf"]), (SEAT["x"], SEAT["y1"], SEAT["zf"]),
                      (SEAT["x"], SEAT["y1"] - 0.4, SEAT["zb"]), (-SEAT["x"], SEAT["y1"] - 0.4, SEAT["zb"])],
     rad((0, "#C88454"), (0.6, "#8A4E2C"), (1, "#5E3018")), ink=3.5, bulge=12)
# front face of the cushion
puff("Seat cushion front", [(-SEAT["x"], SEAT["y1"], SEAT["zf"]), (SEAT["x"], SEAT["y1"], SEAT["zf"]),
                            (SEAT["x"], SEAT["y0"], SEAT["zf"] + 0.4), (-SEAT["x"], SEAT["y0"], SEAT["zf"] + 0.4)],
     lin((0, 560), (0, 660), (0, "#A8643A"), (1, "#4E2814")), ink=3, bulge=9)
# cushion crown light
cx_, cy_ = P(-3, SEAT["y1"] + 0.3, -2.5)
sheen("Seat sheen", cx_, cy_, 60, "#F0C090", 34)
# welt cord along the cushion's front top edge
we = [P(x, SEAT["y1"] + 0.15, SEAT["zf"] + 0.1) for x in (-8.6, -3, 3, 8.6)]
d.path(smooth(we), "Seat welt", fill=NONE, stroke="#3A1C0C", strokeWidth=3.4, opacity=65)

# --- footrest pad -----------------------------------------------------------------------
# the pad's front band (its leading edge, toward the viewer) is what reads as
# the flipped-up leg rest; then the top sliver and a welt along the lip
puff("Pad front band", [(-PAD["x"], PAD["yf"], PAD["zf"]), (PAD["x"], PAD["yf"], PAD["zf"]),
                        (PAD["x"], PAD["yf"] - PAD["t"], PAD["zf"] + 0.2),
                        (-PAD["x"], PAD["yf"] - PAD["t"], PAD["zf"] + 0.2)],
     lin((0, 540), (0, 640), (0, "#B06E42"), (0.6, "#7A4424"), (1, "#3E1E0C")),
     ink=3.5, bulge=12)
# underside connecting the band back to the seat's underside
puff("Pad under", [(-PAD["x"], PAD["yf"] - PAD["t"], PAD["zf"] + 0.2),
                   (PAD["x"], PAD["yf"] - PAD["t"], PAD["zf"] + 0.2),
                   (PAD["x"], PAD["ya"] - 1.4, PAD["za"]), (-PAD["x"], PAD["ya"] - 1.4, PAD["za"])],
     lin((0, 560), (0, 720), (0, "#4E2A14"), (1, "#24100A")), ink=3, bulge=8)
# top face: the padded deck your calves rest on
puff("Pad top", [(-PAD["x"], PAD["ya"], PAD["za"]), (PAD["x"], PAD["ya"], PAD["za"]),
                 (PAD["x"], PAD["yf"], PAD["zf"]), (-PAD["x"], PAD["yf"], PAD["zf"])],
     lin((330, 500), (640, 660), (0, "#C88454"), (0.55, "#8A4E2C"), (1, "#562C14")),
     ink=3.5, bulge=13)
# welt cords along the lip and the rear hinge line
lip = [P(x, PAD["yf"] + 0.1, PAD["zf"] + 0.2) for x in (-7.4, -3.5, 0, 3.5, 7.4)]
d.path(smooth(lip), "Pad lip", fill=NONE, stroke="#3A1C0C", strokeWidth=4.5, cap="round")
hinge = [P(x, PAD["ya"] - 0.2, PAD["za"] - 0.1) for x in (-7.2, 0, 7.2)]
d.path(smooth(hinge), "Pad hinge welt", fill=NONE, stroke="#3A1C0C", strokeWidth=3.5,
       opacity=60, cap="round")
px, py = P(-3.0, PAD["yf"] - 0.9, -15.0)
sheen("Pad sheen", px, py, 44, "#F0C090", 30)

# --- extent check ----------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("recliner extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 30, far


# --- caption ----------------------------------------------------------------------------
def find(node, oid):
    if isinstance(node, dict):
        if node.get("id") == oid and "bounds" in node:
            return node["bounds"]
        for v in node.values():
            r = find(v, oid)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find(v, oid)
            if r:
                return r
    return None


def caption(name, mats):
    n = d.text(name, "Name", x=500, y=940, size=56, font="Virelai Sans",
               color="#F2DCBA", justify="center")
    m = d.text(mats, "Materials", x=500, y=972, size=22, font="Virelai Sans",
               color="#C4A074", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" % (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("RECLINER", "LEATHER · STEEL")
d.finish("recliner-V1R00")
