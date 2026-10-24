#!/usr/bin/env python3
"""Shared sexiburger mascot builder for the virelai brand pieces (#1254).

Character truth: user/src/lib/fixtures/qoi/mascot_64x64.qoi (head-on fixture)
and image/WALLPAPER.QOI (alive pose — eyes, gloves, polka-dot bow tie).
Palette from vkit: BUN lit/mid, BUN_SHADE/DEEP shadow, warm-dark INK outlines,
white gloves. Cel shading — flat fills + one shadow tone, thick outlines,
rounded terminals. Same character, poses are not redesigns.

    from virelai.sexiburger import mascot
    mascot(d, cx, top, h, arms="up")

`h` is total mascot height in px; local frame is 160x230 units scaled to h.
Returns the inked bounding box approx (x, y, w, h) for layout checks.
"""

from virelai.vkit import BUN, BUN_MID, BUN_SHADE, BUN_DEEP, GLOVE, INK

# fillings sampled off the fixture
LETTUCE = "#8BC34A"
LETTUCE_D = "#6FA03A"
TOMATO = "#E04B35"
PATTY = "#5E3D49"
CHEESE = "#FFC93C"
SEED = "#FFF0C2"
BOWTIE = "#D94F3D"
BOWTIE_DOT = "#7FD4C8"
PUPIL = "#3A2530"


def mascot(d, cx, top, h, arms="up", detail=True):
    """Draw the sexiburger presenting. cx = center x, top = dome top y,
    h = total height (~160x230 unit frame). arms: "up" (gloved hands raised
    presenting) or "out" (gloved hands extended sideways)."""
    u = h / 230.0

    def X(v):
        return cx + v * u

    def Y(v):
        return top + v * u

    def P(path, name, fill, stroke=INK, sw=4.0, cap="round", op=None):
        kw = dict(fill=fill, stroke=stroke, strokeWidth=max(1.0, sw * u))
        if stroke == "none":
            kw["strokeWidth"] = 0
        if cap:
            kw["cap"] = cap
        if op is not None:
            kw["opacity"] = op
        return d.path(path, name, **kw)

    def EL(vx, vy, w_, h_, name, fill, stroke="none", sw=0.0, op=None):
        kw = dict(x=X(vx) - w_ * u / 2, y=Y(vy) - h_ * u / 2,
                  width=w_ * u, height=h_ * u, fill=fill)
        if stroke != "none":
            kw["stroke"] = stroke
            kw["strokeWidth"] = max(1.0, sw * u)
        else:
            kw["stroke"] = "none"
        if op is not None:
            kw["opacity"] = op
        return d.shape("ellipse", name, **kw)

    def limb(p0, p1, p2, wb, wt, name, fill=BUN, outline=True):
        """Tapered quad limb: base half-width wb -> tip half-width wt."""
        import math
        # start tangent ~ p1-p0, end tangent ~ p2-p1
        def norm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy) or 1
            return -dy / ln, dx / ln
        n0 = norm(p0, p1)
        n1 = norm(p1, p2)
        b0l = (p0[0] + n0[0] * wb, p0[1] + n0[1] * wb)
        b0r = (p0[0] - n0[0] * wb, p0[1] - n0[1] * wb)
        t0l = (p2[0] + n1[0] * wt, p2[1] + n1[1] * wt)
        t0r = (p2[0] - n1[0] * wt, p2[1] - n1[1] * wt)
        c1 = (p1[0] + n0[0] * (wb + wt) / 2, p1[1] + n0[1] * (wb + wt) / 2)
        c2 = (p1[0] - n0[0] * (wb + wt) / 2, p1[1] - n0[1] * (wb + wt) / 2)
        dpath = (f"M{X(b0l[0]):.1f},{Y(b0l[1]):.1f} "
                 f"Q{X(c1[0]):.1f},{Y(c1[1]):.1f} {X(t0l[0]):.1f},{Y(t0l[1]):.1f} "
                 f"L{X(t0r[0]):.1f},{Y(t0r[1]):.1f} "
                 f"Q{X(c2[0]):.1f},{Y(c2[1]):.1f} {X(b0r[0]):.1f},{Y(b0r[1]):.1f} Z")
        return P(dpath, name, fill, INK if outline else "none", 3.4, cap=None)

    def glove(vx, vy, mirror, name):
        """White cartoon glove: palm blob + thumb nub."""
        sgn = -1 if mirror else 1
        EL(vx, vy, 30, 26, f"{name} palm", GLOVE, INK, 3.2)
        EL(vx + sgn * 13, vy - 7, 12, 14, f"{name} thumb", GLOVE, INK, 3.0)
        for i in range(3):
            P(f"M{X(vx - sgn * (8 - i * 8)):.1f},{Y(vy - 10):.1f} "
              f"q{sgn * 2 * u:.1f},{-4 * u:.1f} {sgn * 5 * u:.1f},{-6 * u:.1f}",
              f"{name} finger{i}", "none", INK, 2.2)

    # ---- rear tentacles (behind body) --------------------------------------
    limb((-30, 150), (-64, 190), (-92, 208), 13, 6, "leg L2")
    limb((-12, 158), (-22, 196), (-34, 216), 13, 6, "leg L1")
    limb((12, 158), (22, 196), (34, 216), 13, 6, "leg R1")
    limb((30, 150), (64, 190), (92, 208), 13, 6, "leg R2")

    # ---- raised arms with gloves --------------------------------------------
    if arms == "up":
        armL = ((-56, 122), (-98, 96), (-112, 56))
        armR = ((56, 122), (98, 96), (112, 56))
    else:
        armL = ((-56, 122), (-112, 118), (-136, 104))
        armR = ((56, 122), (112, 118), (136, 104))
    limb(*armL, 12, 7, "arm L")
    limb(*armR, 12, 7, "arm R")
    glove(armL[2][0], armL[2][1], True, "glove L")
    glove(armR[2][0], armR[2][1], False, "glove R")

    # ---- body: bottom bun mass ----------------------------------------------
    P(f"M{X(-68):.1f},{Y(112):.1f} "
      f"C{X(-74):.1f},{Y(142):.1f} {X(-62):.1f},{Y(160):.1f} {X(-44):.1f},{Y(170):.1f} "
      f"L{X(44):.1f},{Y(170):.1f} "
      f"C{X(62):.1f},{Y(160):.1f} {X(74):.1f},{Y(142):.1f} {X(68):.1f},{Y(112):.1f} Z",
      "body", BUN, INK, 4.2, cap=None)
    # body shadow wedge (cel)
    P(f"M{X(30):.1f},{Y(120):.1f} C{X(58):.1f},{Y(130):.1f} {X(62):.1f},{Y(150):.1f} "
      f"{X(44):.1f},{Y(164):.1f} L{X(20):.1f},{Y(164):.1f} "
      f"C{X(34):.1f},{Y(146):.1f} {X(36):.1f},{Y(132):.1f} {X(30):.1f},{Y(120):.1f} Z",
      "body shade", BUN_MID, "none", cap=None)

    # ---- fillings: patty / cheese / tomato / lettuce ------------------------
    P(f"M{X(-72):.1f},{Y(94):.1f} L{X(72):.1f},{Y(94):.1f} "
      f"C{X(78):.1f},{Y(94):.1f} {X(80):.1f},{Y(102):.1f} {X(76):.1f},{Y(108):.1f} "
      f"C{X(60):.1f},{Y(114):.1f} {X(-60):.1f},{Y(114):.1f} {X(-76):.1f},{Y(108):.1f} "
      f"C{X(-80):.1f},{Y(102):.1f} {X(-78):.1f},{Y(94):.1f} {X(-72):.1f},{Y(94):.1f} Z",
      "patty", PATTY, INK, 3.6, cap=None)
    # cheese drips over the patty edge
    for i, (vx, dl) in enumerate([(-42, 118), (2, 124), (44, 116)]):
        P(f"M{X(vx - 11):.1f},{Y(98):.1f} L{X(vx + 11):.1f},{Y(98):.1f} "
          f"L{X(vx + 2):.1f},{Y(dl):.1f} Z", f"cheese{i}", CHEESE, INK, 2.6,
          cap=None)
    # tomato band
    P(f"M{X(-76):.1f},{Y(80):.1f} L{X(76):.1f},{Y(80):.1f} L{X(74):.1f},{Y(95):.1f} "
      f"L{X(-74):.1f},{Y(95):.1f} Z", "tomato", TOMATO, INK, 3.2, cap=None)
    # lettuce: wavy frill band
    lett = [(-88, 78), (-66, 88), (-44, 76), (-22, 88), (0, 76),
            (22, 88), (44, 76), (66, 88), (88, 78)]
    lp = f"M{X(-88):.1f},{Y(72):.1f} "
    for i in range(1, len(lett)):
        px_, py_ = lett[i]
        lp += f"Q{X((lett[i-1][0]+px_)/2):.1f},{Y(lett[i-1][1]+10):.1f} {X(px_):.1f},{Y(py_):.1f} "
    lp += (f"L{X(84):.1f},{Y(68):.1f} L{X(-84):.1f},{Y(68):.1f} Z")
    P(lp, "lettuce", LETTUCE, INK, 3.0, cap=None)

    # ---- bun dome -----------------------------------------------------------
    P(f"M{X(-80):.1f},{Y(70):.1f} "
      f"C{X(-80):.1f},{Y(26):.1f} {X(-46):.1f},{Y(2):.1f} {X(0):.1f},{Y(0):.1f} "
      f"C{X(46):.1f},{Y(2):.1f} {X(80):.1f},{Y(26):.1f} {X(80):.1f},{Y(70):.1f} Z",
      "bun dome", BUN, INK, 4.4, cap=None)
    # dome lit crescent + shade wedge (cel)
    P(f"M{X(-64):.1f},{Y(58):.1f} C{X(-66):.1f},{Y(34):.1f} {X(-44):.1f},{Y(14):.1f} "
      f"{X(-18):.1f},{Y(8):.1f} C{X(-38):.1f},{Y(22):.1f} {X(-52):.1f},{Y(42):.1f} "
      f"{X(-56):.1f},{Y(62):.1f} Z", "dome light", "#FFD98A", "none", cap=None)
    P(f"M{X(30):.1f},{Y(6):.1f} C{X(56):.1f},{Y(14):.1f} {X(72):.1f},{Y(36):.1f} "
      f"{X(74):.1f},{Y(66):.1f} L{X(58):.1f},{Y(66):.1f} C{X(58):.1f},{Y(40):.1f} "
      f"{X(48):.1f},{Y(20):.1f} {X(30):.1f},{Y(6):.1f} Z",
      "dome shade", BUN_MID, "none", cap=None)
    # sesame seeds
    seeds = [(-44, 30, -18), (-16, 18, 10), (10, 26, -8), (36, 18, 14),
             (54, 36, -14), (-58, 48, 8), (-26, 44, -12), (2, 50, 16),
             (30, 46, -16), (56, 54, 10)]
    if not detail:
        seeds = seeds[::2]
    for i, (vx, vy, rot) in enumerate(seeds):
        EL(vx, vy, 9, 5, f"seed{i}", SEED)

    # ---- face: big cartoon eyes + open smile ---------------------------------
    for sgn, vx in [(-1, -22), (1, 22)]:
        EL(vx, 134, 21, 26, f"eye{sgn} white", GLOVE, INK, 3.0)
        EL(vx + sgn * 3, 137, 9, 12, f"eye{sgn} pupil", PUPIL)
        EL(vx + sgn * 5, 133, 3.6, 4.6, f"eye{sgn} glint", "#FFFFFF")
    P(f"M{X(-13):.1f},{Y(152):.1f} Q{X(0):.1f},{Y(166):.1f} {X(13):.1f},{Y(152):.1f}",
      "smile", "none", INK, 3.6)

    # ---- polka-dot bow tie ---------------------------------------------------
    kx, ky = 0, 176
    P(f"M{X(kx - 5):.1f},{Y(ky):.1f} L{X(kx - 26):.1f},{Y(ky - 10):.1f} "
      f"L{X(kx - 26):.1f},{Y(ky + 10):.1f} Z", "bow L", BOWTIE, INK, 2.8, cap=None)
    P(f"M{X(kx + 5):.1f},{Y(ky):.1f} L{X(kx + 26):.1f},{Y(ky - 10):.1f} "
      f"L{X(kx + 26):.1f},{Y(ky + 10):.1f} Z", "bow R", BOWTIE, INK, 2.8, cap=None)
    EL(kx, ky, 12, 10, "bow knot", BOWTIE, INK, 2.8)
    if detail:
        for i, (vx, vy) in enumerate([(kx - 18, ky - 4), (kx - 14, ky + 5),
                                      (kx + 16, ky - 5), (kx + 20, ky + 4)]):
            EL(vx, vy, 3.4, 3.4, f"bowdot{i}", BOWTIE_DOT)

    # rough inked bounds (for layout checks)
    return (cx - 140 * u, top, 280 * u, 230 * u)
