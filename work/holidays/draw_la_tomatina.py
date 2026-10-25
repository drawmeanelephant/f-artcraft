#!/usr/bin/env python3
"""La Tomatina — Festival Seal V1R00.

A plaster street wall splattered with tomato bursts behind a tilted wooden
crate spilling fruit: one big splat bloom with juice drips, a medium burst,
satellite droplets, a thrown tomato mid-flight with its streak. The crate —
slatted planks, corner posts, diagonal brace — sits on a cobbled street band
hugging the bottom rim; a squashed tomato and rolling fruit at its foot.
Warm plaster field, gold rim, vermilion chop with a drawn tomato. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI,
                          GOLD_LO, PAPER, LATIN, lin, rad, gold_lin, smooth,
                          blend)
from festival_kit import seal_disc, glow, dust, ring_dots, caption

SLUG = "la-tomatina-V1R00"
SERIF = "Source Sans 3"          # Virelai Sans has no digits -> dates use this

WALL_HI = "#F0D6A8"
WALL_MID = "#E2AE78"
WALL_LO = "#C08050"
STREET_HI = "#8A4A30"
STREET_LO = "#4E2418"
TOM_HI = "#FF8A64"
TOM = "#E8401F"
TOM_LO = "#9E1808"
SPLAT = "#D93218"
SPLAT_DK = "#9E180C"
SPLAT_LT = "#F06848"
WOOD_HI = "#D8A468"
WOOD = "#B07840"
WOOD_LO = "#6E3C1C"
LEAF = "#3E6B2E"
LEAF_LO = "#1E3A16"

p = Plate("La Tomatina — Festival Seal", 1000, 1000)
d = p.d


# --- local helpers -----------------------------------------------------------
def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


def rot(cx, cy, dx, dy, deg):
    """Point (cx+dx, cy+dy) rotated deg about (cx, cy)."""
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


def quad_pts(cx, cy, w, h, deg, x0, x1, y0, y1):
    """Rotated sub-rect of a w x h box centred at (cx, cy), local coords."""
    return [rot(cx, cy, px, py, deg)
            for px, py in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]


def quad_d(pts):
    return ("M%.1f,%.1f " % pts[0] +
            " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z")


def tomato(cx, cy, r, label, squash=0.90, stroke=INK, sw=2.4):
    """Whole tomato: squashed sphere, pale shoulder, calyx star, stem."""
    inside(cx - r, cy, 4, f"{label} L")
    inside(cx + r, cy, 4, f"{label} R")
    inside(cx, cy + r * squash, 4, f"{label} B")
    d.shape("ellipse", label, x=cx - r, y=cy - r * squash, width=2 * r,
            height=2 * r * squash,
            fill=rad((0, TOM_HI), (0.45, TOM), (1, TOM_LO)),
            stroke=stroke, strokeWidth=sw)
    # shoulder highlight
    d.shape("ellipse", f"{label} sheen", x=cx - r * 0.62, y=cy - r * squash * 0.78,
            width=r * 0.7, height=r * squash * 0.44,
            fill=rad((0, "#FFD0B8", 55), (0.7, "#FFD0B8", 12),
                     (1, "#FFD0B8", 0)), stroke=NONE)
    # shaded bottom-right crescent
    d.path(f"M{cx + r*0.25:.1f},{cy + r*squash*0.55:.1f} "
           f"Q{cx:.1f},{cy + r*squash*0.9:.1f} {cx - r*0.5:.1f},{cy + r*squash*0.5:.1f}",
           f"{label} shade", fill=NONE, stroke=TOM_LO, strokeWidth=r * 0.14,
           opacity=30, cap="round")
    # calyx: pointed sepals radiating from the top centre
    ty = cy - r * squash * 0.94
    for i in range(5):
        a = math.radians(-90 + (i - 2) * 42)
        bx, by = cx + math.cos(a) * r * 0.10, ty + math.sin(a) * r * 0.06
        tx_, ty_ = cx + math.cos(a) * r * 0.52, ty + math.sin(a) * r * 0.30
        px_, py_ = -math.sin(a), math.cos(a)
        d.path(f"M{bx + px_*r*0.09:.1f},{by + py_*r*0.09:.1f} "
               f"Q{bx + px_*r*0.10 + math.cos(a)*r*0.26:.1f},"
               f"{by + py_*r*0.10 + math.sin(a)*r*0.26:.1f} {tx_:.1f},{ty_:.1f} "
               f"Q{bx - px_*r*0.10 + math.cos(a)*r*0.26:.1f},"
               f"{by - py_*r*0.10 + math.sin(a)*r*0.26:.1f} "
               f"{bx - px_*r*0.09:.1f},{by - py_*r*0.09:.1f} Z",
               f"{label} sepal {i+1}",
               fill=lin((bx, by), (tx_, ty_), (0, LEAF), (1, LEAF_LO)),
               stroke=NONE)
    # stem stub
    d.path(f"M{cx:.1f},{ty + 2:.1f} C{cx - 1:.1f},{ty - r*0.10:.1f} "
           f"{cx + 3:.1f},{ty - r*0.16:.1f} {cx + 6:.1f},{ty - r*0.20:.1f}",
           f"{label} stem", fill=NONE, stroke="#4A5A22", strokeWidth=r * 0.10,
           cap="round")


def splat(cx, cy, r, col, label, seed, op=92, lobes=11, squash=0.82,
          drips=4, sat_n=9):
    """Tomato splat on the wall: irregular blob, pulp core, seeds, drips."""
    s = seed
    pts = []
    for i in range(lobes):
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (0.70 + 0.42 * (s / 2 ** 31))
        a = TAU2 * i / lobes + 0.13
        px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr * squash
        inside(px, py, 8, f"{label} lobe {i}")
        pts.append((px, py))
    d.path(smooth(pts, closed=True), label, fill=col, opacity=op,
           stroke=blend(col, INK, 0.45), strokeWidth=1.8)
    # pulp core: smaller off-centre blob, darker
    s2 = seed + 7
    pts2 = []
    for i in range(8):
        s2 = (1103515245 * s2 + 12345) % (2 ** 31)
        rr = r * 0.46 * (0.75 + 0.4 * (s2 / 2 ** 31))
        a = TAU2 * i / 8 + 0.4
        pts2.append((cx - r * 0.06 + math.cos(a) * rr,
                     cy + r * 0.05 + math.sin(a) * rr * squash))
    d.path(smooth(pts2, closed=True), f"{label} pulp", fill=SPLAT_DK,
           opacity=48, stroke=NONE)
    # wet sheen on the upper-left of the blob
    d.shape("ellipse", f"{label} sheen", x=cx - r * 0.52, y=cy - r * squash * 0.62,
            width=r * 0.55, height=r * squash * 0.34,
            fill=rad((0, "#FF9A78", 42), (1, "#FF9A78", 0)), stroke=NONE)
    # seeds: pale amber drops inside the blob
    for i in range(6):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = TAU2 * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * 0.52 * (s / 2 ** 31)
        sx_, sy_ = cx + math.cos(a) * rr, cy + math.sin(a) * rr * squash * 0.8
        d.shape("ellipse", f"{label} seed {i+1}", x=sx_ - 3.4, y=sy_ - 5.0,
                width=6.8, height=10, fill="#F6C078", opacity=70, stroke=NONE)
    # juice drips running down the wall from the blob's lower edge
    for i in range(drips):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = math.radians(55 + 70 * (s / 2 ** 31))
        s = (1103515245 * s + 12345) % (2 ** 31)
        x0 = cx + math.cos(a) * r * 0.9
        y0 = cy + math.sin(a) * r * squash * 0.9
        ln = r * (0.22 + 0.30 * (s / 2 ** 31))
        x1, y1 = x0 + 4, y0 + ln
        inside(x1, y1, 8, f"{label} drip {i}")
        d.path(f"M{x0:.1f},{y0:.1f} C{x0 - 3:.1f},{y0 + ln*0.4:.1f} "
               f"{x1 + 3:.1f},{y0 + ln*0.7:.1f} {x1:.1f},{y1:.1f}",
               f"{label} drip {i+1}", fill=NONE, stroke=col,
               strokeWidth=r * 0.045, opacity=62, cap="round")
        d.shape("ellipse", f"{label} drip tip {i+1}", x=x1 - r * 0.035,
                y=y1 - r * 0.035, width=r * 0.07, height=r * 0.07,
                fill=col, opacity=66, stroke=NONE)
    # satellite droplets
    for i in range(sat_n):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = TAU2 * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (1.06 + 0.30 * (s / 2 ** 31))
        s = (1103515245 * s + 12345) % (2 ** 31)
        sz = 3.0 + 6.0 * (s / 2 ** 31)
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr * squash
        inside(x, y, 8, f"{label} sat {i}")
        d.shape("ellipse", f"{label} sat {i+1}", x=x - sz / 2, y=y - sz / 2,
                width=sz, height=sz, fill=col, opacity=min(95, op + 4),
                stroke=NONE)


def squashed_tomato(cx, cy, r, label):
    """A tomato already burst on the street: low wide splat + pulp + skin."""
    d.shape("ellipse", label, x=cx - r * 1.25, y=cy - r * 0.38,
            width=r * 2.5, height=r * 0.76,
            fill=rad((0, SPLAT_LT), (0.5, SPLAT), (1, SPLAT_DK)),
            stroke=blend(SPLAT, INK, 0.4), strokeWidth=1.6)
    for i, (dx, dy, sr) in enumerate([(-0.7, -0.1, 0.28), (0.1, -0.15, 0.34),
                                      (0.75, 0.0, 0.22), (-0.2, 0.1, 0.18)]):
        d.shape("ellipse", f"{label} pulp {i+1}", x=cx + dx * r - sr * r,
                y=cy + dy * r - sr * r * 0.5, width=2 * sr * r,
                height=sr * r, fill=SPLAT_DK, opacity=42, stroke=NONE)
    for i in range(5):
        a = math.radians(200 + i * 30)
        x, y = cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.30
        d.shape("ellipse", f"{label} seed {i+1}", x=x - 3, y=y - 2,
                width=6, height=4, fill="#F6C078", opacity=70, stroke=NONE)


TAU2 = math.pi * 2

# --- field -------------------------------------------------------------------
p.backdrop(top="#2A0E0A", bottom="#100505", glow=("#6E2418", 15))
dust(d, n=42, r=402, colors=("#F6E3B8", "#F0A080"), seed=29, smin=1.0,
     smax=2.4, opmin=8, opmax=20, label="Backdrop dust")
seal_disc(p, WALL_HI, WALL_LO, rim=GOLD, rim2="#5E3A16")
# plaster mottling: soft uneven tone on the wall
d.shape("ellipse", "Wall tone 1", x=150, y=120, width=340, height=240,
        fill=rad((0, WALL_MID, 34), (1, WALL_MID, 0)), stroke=NONE)
d.shape("ellipse", "Wall tone 2", x=560, y=420, width=330, height=220,
        fill=rad((0, "#B4703E", 26), (1, "#B4703E", 0)), stroke=NONE)
glow(d, 360, 250, 300, "#FFF0C8", a=18, label="Sun glow")
ring_dots(d, r=397, n=56, size=2.4, color=GOLD, opacity=30)

# --- street band hugging the bottom rim --------------------------------------
# chord at y=690, arc along the rim through the bottom
a_r = math.asin(230 / (PR - 6))          # ~33.7 deg below centre line
n_arc = 26
arc = [(PCX + (PR - 6) * math.cos(a_r + (math.pi - 2 * a_r) * i / n_arc),
        PCY + (PR - 6) * math.sin(a_r + (math.pi - 2 * a_r) * i / n_arc))
       for i in range(n_arc + 1)]
chord_l = (PCX - (PR - 6) * math.cos(a_r), PCY + 230)
d.path(f"M{chord_l[0]:.1f},{chord_l[1]:.1f} L{arc[-1][0]:.1f},{arc[-1][1]:.1f} " +
       smooth(arc, move=False) + " Z", "Street",
       fill=lin((0, 690), (0, 880), (0, STREET_HI), (1, STREET_LO)),
       stroke=NONE)
d.path(f"M{chord_l[0]:.1f},{chord_l[1]:.1f} L{arc[-1][0]:.1f},{arc[-1][1]:.1f}",
       "Street edge", fill=NONE, stroke="#3A1C10", strokeWidth=3,
       opacity=55, cap="round")
# cobble courses: arcs parallel to the rim + short radial joints
for rr, op in ((376, 30), (336, 26), (300, 22)):
    pts = []
    for i in range(n_arc + 1):
        a = a_r * 1.06 + (math.pi - 2 * a_r * 1.06) * i / n_arc
        x, y = PCX + rr * math.cos(a), PCY + rr * math.sin(a)
        if y > 706:
            pts.append((x, y))
    if len(pts) > 2:
        d.path(smooth(pts), f"Cobble course {rr}", fill=NONE,
               stroke="#3A1C10", strokeWidth=2.2, opacity=op, cap="round")
for i, aa in enumerate((55, 75, 95, 115, 135)):
    a = math.radians(aa)
    x0, y0 = PCX + 300 * math.cos(a), PCY + 300 * math.sin(a)
    x1, y1 = PCX + 388 * math.cos(a), PCY + 388 * math.sin(a)
    d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", f"Cobble joint {i+1}",
           fill=NONE, stroke="#3A1C10", strokeWidth=2.0, opacity=24,
           cap="round")

# --- splat bursts on the wall ---------------------------------------------------
splat(360, 320, 168, SPLAT, "Splat big", seed=11, lobes=12, drips=5, sat_n=11)
splat(662, 296, 88, SPLAT, "Splat mid", seed=23, lobes=9, drips=2, sat_n=7)
splat(238, 505, 60, SPLAT, "Splat low", seed=31, lobes=8, drips=2,
      sat_n=5, op=80)

# --- thrown tomato, mid-flight --------------------------------------------------
# tomato tossed from the street below-left, arcing up over the crate;
# trail stays inside the rim
fx, fy = 246, 196
d.path("M170,300 Q204,250 238,208", "Flight streak", fill=NONE,
       stroke=SPLAT_LT, strokeWidth=10, opacity=48, cap="round")
d.path("M186,310 Q216,262 242,214", "Flight streak 2", fill=NONE,
       stroke=SPLAT, strokeWidth=5, opacity=55, cap="round")
for i, (dx, dy, sr) in enumerate([(176, 288, 4.5), (196, 262, 3.4),
                                  (213, 240, 2.8), (170, 306, 3.0)]):
    d.shape("ellipse", f"Flight drop {i+1}", x=dx - sr, y=dy - sr,
            width=2 * sr, height=2 * sr, fill=SPLAT, opacity=72, stroke=NONE)
tomato(fx, fy, 30, "Thrown tomato")

# --- back crate, half hidden behind the main one --------------------------------
BCX, BCY, BW2, BH2, BDEG = 688, 588, 168, 104, 6
bt = [rot(BCX, BCY, -BW2 / 2, -BH2 / 2, BDEG),
      rot(BCX, BCY, BW2 / 2, -BH2 / 2, BDEG)]
boff = (math.sin(math.radians(BDEG)) * 34, -math.cos(math.radians(BDEG)) * 34)
# right side face
br_ = rot(BCX, BCY, BW2 / 2, BH2 / 2, BDEG)
sp = [bt[1], (bt[1][0] + boff[0], bt[1][1] + boff[1]),
      (br_[0] + boff[0], br_[1] + boff[1]), br_]
d.path(quad_d(sp), "Crate back side",
       fill=lin((bt[1][0], bt[1][1]), (bt[1][0] + boff[0], bt[1][1] + boff[1]),
                (0, WOOD_LO), (1, "#3E2010")), stroke=INK, strokeWidth=2.2)
# top face + interior
tp = [bt[0], bt[1], (bt[1][0] + boff[0], bt[1][1] + boff[1]),
      (bt[0][0] + boff[0], bt[0][1] + boff[1])]
d.path(quad_d(tp), "Crate back top",
       fill=lin((0, min(q[1] for q in tp)), (0, max(q[1] for q in tp)),
                (0, WOOD_HI), (1, WOOD)), stroke=INK, strokeWidth=2.4)
inset = [(bt[0][0] * 0.82 + bt[1][0] * 0.18 + boff[0] * 0.3,
          bt[0][1] * 0.82 + bt[1][1] * 0.18 + boff[1] * 0.3),
         (bt[0][0] * 0.18 + bt[1][0] * 0.82 + boff[0] * 0.3,
          bt[0][1] * 0.18 + bt[1][1] * 0.82 + boff[1] * 0.3),
         (bt[1][0] + boff[0] * 0.72, bt[1][1] + boff[1] * 0.72),
         (bt[0][0] + boff[0] * 0.72, bt[0][1] + boff[1] * 0.72)]
d.path(quad_d(inset), "Crate back interior", fill="#2A140A", stroke=NONE)
# tomatoes showing in the back crate
for i, (lx, r_) in enumerate([(-46, 24), (6, 26), (54, 22)]):
    tx_, ty_ = rot(BCX, BCY, lx, -BH2 / 2 - r_ * 0.30, BDEG)
    tomato(tx_, ty_, r_, f"Back tomato {i+1}", squash=0.86, sw=2.0)
# front face planks
for i, (y0, y1) in enumerate(((-BH2 / 2, -BH2 / 6 - 2),
                              (-BH2 / 6 + 2, BH2 / 6 - 2),
                              (BH2 / 6 + 2, BH2 / 2))):
    q = quad_pts(BCX, BCY, BW2, BH2, BDEG, -BW2 / 2, BW2 / 2, y0, y1)
    d.path(quad_d(q), f"Crate back plank {i+1}",
           fill=lin((0, q[0][1]), (0, q[2][1]),
                    (0, WOOD_HI if i != 1 else WOOD),
                    (1, WOOD if i != 1 else WOOD_LO)),
           stroke=INK, strokeWidth=2.0)
for sgn, nm in ((-1, "L"), (1, "R")):
    x0 = -BW2 / 2 if sgn < 0 else BW2 / 2 - 16
    q = quad_pts(BCX, BCY, BW2, BH2, BDEG, x0, x0 + 16, -BH2 / 2, BH2 / 2)
    d.path(quad_d(q), f"Crate back post {nm}", fill=WOOD_LO,
           stroke=INK, strokeWidth=1.8, opacity=96)

# --- ground shadows ---------------------------------------------------------------
d.shape("ellipse", "Crate shadow", x=252, y=752, width=470, height=52,
        fill=rad((0, INK, 40), (0.6, INK, 18), (1, INK, 0)), stroke=NONE)
d.shape("ellipse", "Roll shadow 1", x=634, y=812, width=74, height=16,
        fill=rad((0, INK, 34), (1, INK, 0)), stroke=NONE)
d.shape("ellipse", "Roll shadow 2", x=226, y=776, width=64, height=14,
        fill=rad((0, INK, 30), (1, INK, 0)), stroke=NONE)

# --- main crate -------------------------------------------------------------------
MCX, MCY, MW, MH, MDEG = 480, 636, 322, 148, -8
moff = (math.sin(math.radians(MDEG)) * 46, -math.cos(math.radians(MDEG)) * 46)
mf = [rot(MCX, MCY, px, py, MDEG) for px, py in
      ((-MW / 2, -MH / 2), (MW / 2, -MH / 2), (MW / 2, MH / 2), (-MW / 2, MH / 2))]
# right side face
rsp = [mf[1], (mf[1][0] + moff[0], mf[1][1] + moff[1]),
       (mf[2][0] + moff[0], mf[2][1] + moff[1]), mf[2]]
d.path(quad_d(rsp), "Crate side",
       fill=lin((mf[1][0], mf[1][1]), (mf[1][0] + moff[0], mf[1][1] + moff[1]),
                (0, WOOD_LO), (1, "#381C0C")), stroke=INK, strokeWidth=2.4)
# top face + dark interior
mtp = [mf[0], mf[1], (mf[1][0] + moff[0], mf[1][1] + moff[1]),
       (mf[0][0] + moff[0], mf[0][1] + moff[1])]
d.path(quad_d(mtp), "Crate top",
       fill=lin((0, min(q[1] for q in mtp)), (0, max(q[1] for q in mtp)),
                (0, WOOD_HI), (1, WOOD)), stroke=INK, strokeWidth=2.6)
ins = [(mf[0][0] * 0.80 + mf[1][0] * 0.20 + moff[0] * 0.32,
        mf[0][1] * 0.80 + mf[1][1] * 0.20 + moff[1] * 0.32),
       (mf[0][0] * 0.20 + mf[1][0] * 0.80 + moff[0] * 0.32,
        mf[0][1] * 0.20 + mf[1][1] * 0.80 + moff[1] * 0.32),
       (mf[1][0] + moff[0] * 0.74, mf[1][1] + moff[1] * 0.74),
       (mf[0][0] + moff[0] * 0.74, mf[0][1] + moff[1] * 0.74)]
d.path(quad_d(ins), "Crate interior", fill="#2A140A", stroke=NONE)
# tomato pile inside: rows of shoulders above the rim line
for i, (lx, ly, r_) in enumerate([(-118, -0.52 * MH, 30), (-62, -0.62 * MH, 33),
                                  (-4, -0.56 * MH, 31), (56, -0.64 * MH, 34),
                                  (114, -0.52 * MH, 29), (-90, -0.80 * MH, 28),
                                  (-30, -0.86 * MH, 30), (32, -0.82 * MH, 28),
                                  (90, -0.78 * MH, 26)]):
    tx_, ty_ = rot(MCX, MCY, lx, ly, MDEG)
    tomato(tx_, ty_, r_, f"Pile tomato {i+1}", squash=0.84, sw=2.0)
# front face planks (three courses)
for i, (y0, y1) in enumerate(((-MH / 2, -MH / 6 - 3),
                              (-MH / 6 + 3, MH / 6 - 3),
                              (MH / 6 + 3, MH / 2))):
    q = quad_pts(MCX, MCY, MW, MH, MDEG, -MW / 2, MW / 2, y0, y1)
    d.path(quad_d(q), f"Crate plank {i+1}",
           fill=lin((0, q[0][1]), (0, q[2][1]),
                    (0, WOOD_HI if i == 0 else WOOD),
                    (1, WOOD_LO)),
           stroke=INK, strokeWidth=2.4)
# wood grain hints on the front planks
for i, (lx0, lx1, ly) in enumerate([(-0.36 * MW, -0.05 * MW, -0.32 * MH),
                                    (0.10 * MW, 0.38 * MW, -0.30 * MH),
                                    (-0.30 * MW, 0.05 * MW, 0.02 * MH),
                                    (0.15 * MW, 0.40 * MW, 0.34 * MH),
                                    (-0.38 * MW, -0.12 * MW, 0.36 * MH)]):
    x0, y0 = rot(MCX, MCY, lx0, ly, MDEG)
    x1, y1 = rot(MCX, MCY, lx1, ly + 3, MDEG)
    d.path(f"M{x0:.1f},{y0:.1f} Q{(x0+x1)/2:.1f},{(y0+y1)/2 + 4:.1f} {x1:.1f},{y1:.1f}",
           f"Grain {i+1}", fill=NONE, stroke="#5E3014", strokeWidth=1.8,
           opacity=40, cap="round")
# diagonal brace across the front: thin strip from lower-left to upper-right
dxl, dyl = (MW - 48), -(MH - 24)
dlen = math.hypot(dxl, dyl)
nx, ny = (-dyl / dlen) * 13, (dxl / dlen) * 13
L0 = (-MW / 2 + 24, MH / 2 - 12)
L1 = (MW / 2 - 24, -MH / 2 + 12)
br = [rot(MCX, MCY, L0[0] - nx, L0[1] - ny, MDEG),
      rot(MCX, MCY, L1[0] - nx, L1[1] - ny, MDEG),
      rot(MCX, MCY, L1[0] + nx, L1[1] + ny, MDEG),
      rot(MCX, MCY, L0[0] + nx, L0[1] + ny, MDEG)]
d.path(quad_d(br), "Crate brace",
       fill=lin((br[0][0], br[0][1]), (br[2][0], br[2][1]),
                (0, WOOD), (1, WOOD_LO)),
       stroke=INK, strokeWidth=2.4)
# corner posts over everything
for sgn, nm in ((-1, "L"), (1, "R")):
    x0 = -MW / 2 if sgn < 0 else MW / 2 - 20
    q = quad_pts(MCX, MCY, MW, MH, MDEG, x0, x0 + 20, -MH / 2 - 4, MH / 2 + 2)
    d.path(quad_d(q), f"Crate post {nm}",
           fill=lin((q[0][0], 0), (q[1][0], 0), (0, WOOD), (1, WOOD_LO)),
           stroke=INK, strokeWidth=2.2)
    for j, ly in enumerate((-MH / 4, MH / 4)):
        bx_, by_ = rot(MCX, MCY, x0 + 10, ly, MDEG)
        d.shape("ellipse", f"Crate bolt {nm}{j}", x=bx_ - 3, y=by_ - 3,
                width=6, height=6, fill="#3E2010", stroke=NONE, opacity=85)

# --- spilling + rolling fruit ------------------------------------------------------
# two tomatoes tipped over the front lip
for i, (lx, ly, r_) in enumerate([(-58, -MH / 2 - 16, 28), (18, -MH / 2 - 10, 26)]):
    tx_, ty_ = rot(MCX, MCY, lx, ly, MDEG)
    tomato(tx_, ty_, r_, f"Lip tomato {i+1}", squash=0.86)
squashed_tomato(330, 800, 46, "Splat tomato")
tomato(676, 792, 30, "Rolling tomato 1")
tomato(250, 760, 24, "Rolling tomato 2")
# juice trail from under the crate's edge onto the street
for i, (x0, y0, x1, y1, w) in enumerate([(402, 722, 380, 800, 6),
                                         (560, 706, 572, 772, 4)]):
    d.path(f"M{x0:.1f},{y0:.1f} Q{(x0+x1)/2 - 10:.1f},{(y0+y1)/2:.1f} {x1:.1f},{y1:.1f}",
           f"Juice run {i+1}", fill=NONE, stroke=SPLAT, strokeWidth=w,
           opacity=34, cap="round")
    d.shape("ellipse", f"Juice tip {i+1}", x=x1 - w * 0.7, y=y1 - w * 0.5,
            width=w * 1.4, height=w * 1.4, fill=SPLAT, opacity=40,
            stroke=NONE)

# --- seal + caption -----------------------------------------------------------------
def seal_chop(cx=744, cy=214, s=62):
    x, y = cx - s / 2, cy - s / 2
    inside(cx + s / 2, cy + s / 2, 8, "chop BR")
    d.shape("ellipse", "Chop shadow", x=x + 3, y=y + 5, width=s, height=s,
            fill=INK, opacity=28, stroke=NONE)
    d.shape("rectangle", "Chop", x=x, y=y, width=s, height=s, radius=5,
            fill=lin((x, y), (x + s, y + s), (0, "#C0473A"), (1, "#7E1F1B")),
            stroke="#4E100E", strokeWidth=2.2)
    d.shape("rectangle", "Chop inner", x=x + 4.5, y=y + 4.5, width=s - 9,
            height=s - 9, radius=2.5, fill=NONE, stroke="#F6D9A0",
            strokeWidth=1.4, opacity=78)
    # drawn tomato mark
    d.shape("ellipse", "Chop tomato", x=cx - 11, y=cy - 9, width=22, height=19,
            fill="#FBE6B4", stroke="#D8A85E", strokeWidth=1.2)
    for i in range(5):
        a = math.radians(-90 + (i - 2) * 40)
        d.path(f"M{cx + math.cos(a)*3:.1f},{cy - 8 + math.sin(a)*2:.1f} "
               f"L{cx + math.cos(a)*8:.1f},{cy - 8 + math.sin(a)*5:.1f}",
               f"Chop sepal {i+1}", fill=NONE, stroke="#D8A85E",
               strokeWidth=1.4, cap="round")


seal_chop()
caption(p, "LA TOMATINA", "LAST WEDNESDAY OF AUGUST · BUÑOL",
        name_color="#F4EBD4", sub_color="#C9A46A",
        name_size=50, tracking_name=64, sub_size=20, tracking_sub=40,
        sub_font=SERIF)
p.finish(SLUG)
