#!/usr/bin/env python3
"""V2 look — the ember-dusk idiom: noir gradient fields, radial spotlight
glows, translucent shading passes, vignette. Shared by the V2R00 riffs."""
import os, json
from vc import Draw, NONE, ROOT

ART = os.path.join(ROOT, "art")
PDF = os.path.join(ROOT, "pdf")
os.makedirs(ART, exist_ok=True)
os.makedirs(PDF, exist_ok=True)


def backdrop(d, w, h, top="#17102e", mid="#241a3f", bottom="#0b0716"):
    d.shape("rectangle", "Backdrop", x=0, y=0, width=w, height=h, stroke=NONE,
            fill={"gradient": {"kind": "linear", "start": [0, 0], "end": [0, h],
                  "stops": [{"offset": 0, "color": top},
                            {"offset": 0.55, "color": mid},
                            {"offset": 1, "color": bottom}]}})


def glow(d, name, cx, cy, r, color, opacity=55, aspect=1.0):
    w, h = 2 * r, 2 * r * aspect
    d.shape("ellipse", name, x=cx - w / 2, y=cy - h / 2, width=w, height=h,
            stroke=NONE, opacity=opacity,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": color, "opacity": 1},
                {"offset": 1, "color": color, "opacity": 0}]}})


def vignette(d, w, h, opacity=38):
    d.shape("rectangle", "Vignette", x=0, y=0, width=w, height=h, stroke=NONE,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#0a0514", "opacity": 0},
                {"offset": 0.6, "color": "#0a0514", "opacity": 0},
                {"offset": 1, "color": "#0a0514", "opacity": opacity / 100}]}})


def sparkle(d, name, cx, cy, r, color="#ffe9b0", opacity=85):
    d.path(f"M{cx},{cy-r} L{cx+r*0.22},{cy-r*0.22} L{cx+r},{cy} "
           f"L{cx+r*0.22},{cy+r*0.22} L{cx},{cy+r} "
           f"L{cx-r*0.22},{cy+r*0.22} L{cx-r},{cy} L{cx-r*0.22},{cy-r*0.22} Z",
           name, fill=color, stroke=NONE, opacity=opacity)


def ship(d, slug, rev):
    base = f"{slug}-{rev}"
    d.cmd("select.none", "select.none")
    print(json.dumps(d.call("save_file", {"path": f"{ART}/{base}.vectorcraft"}, "save"))[:140])
    for fmt, path, scale in [("svg", f"{ART}/{base}.svg", None),
                             ("png", f"{ART}/{base}@2x.png", 2),
                             ("pdf", f"{PDF}/{base}.pdf", None)]:
        a = {"path": path, "format": fmt}
        if scale:
            a["scale"] = scale
        print(" ", fmt, json.dumps(d.call("export", a, f"export {fmt}"))[:140])
    d.m.call("render_preview", {"max_side": 1100})
    print(f"DONE {base}: calls={d.count} errors={len(d.errors)}")
    for lbl, e in d.errors:
        print(" -", lbl, ":", e[:200])
