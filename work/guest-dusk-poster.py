#!/usr/bin/env python3
"""Generate the JSONL session that draws the Dusk poster in VectorCraft.

Run from the repo root:  python3 work/guest-dusk-poster.py > work/out/dusk.jsonl
"""
import json
import os
import math
import random

os.makedirs("work/out", exist_ok=True)

W, H = 1080, 1350
rng = random.Random(7)

steps = []


def shape(**kw):
    steps.append({"id": "draw_shape", "params": kw})


def path(d, fill, name=None, **kw):
    p = {"d": d, "closed": True, "fill": fill, "stroke": "none"}
    if name:
        p["name"] = name
    p.update(kw)
    steps.append({"id": "draw_path", "params": p})


def grad(stops, kind="linear", angle=90):
    return {
        "gradient": {
            "kind": kind,
            "angle": angle,
            "stops": [{"offset": o, "color": c, **({"opacity": op} if op is not None else {})} for o, c, op in stops],
        }
    }


# ---------------------------------------------------------------- sky
shape(
    shape="rectangle", x=0, y=0, width=W, height=H, name="Sky",
    fill=grad([(0, "#8f2d3f", None), (0.32, "#4a1b46", None), (0.58, "#1b1238", None), (1, "#04050e", None)]),
    stroke="none",
)

# ---------------------------------------------------------------- stars
for i in range(78):
    x = rng.uniform(20, W - 20)
    y = rng.uniform(40, 640)
    # thin the field out near the horizon glow
    if rng.random() < (y - 40) / 600 * 0.75:
        continue
    r = rng.choice([0.9, 1.1, 1.4, 1.8, 2.4])
    shape(
        shape="ellipse", x=x - r, y=y - r, width=r * 2, height=r * 2, name="Star",
        fill="#fff6e3", stroke="none",
        opacity=rng.randint(35, 100),
    )

# ---------------------------------------------------------------- horizon haze
shape(
    shape="rectangle", x=0, y=620, width=W, height=260, name="Haze",
    fill=grad([(0, "#ff7a4d", 0.0), (0.55, "#ff7a4d", 0.30), (1, "#ff7a4d", 0.0)]),
    stroke="none",
    opacity=70,
)

# ---------------------------------------------------------------- sun
SUN_X, SUN_Y, SUN_R = 540, 700, 232
shape(
    shape="ellipse",
    x=SUN_X - SUN_R, y=SUN_Y - SUN_R, width=SUN_R * 2, height=SUN_R * 2, name="Sun",
    fill=grad(
        [(0, "#fff8cf", None), (0.34, "#ffe08a", None), (0.62, "#ff9f52", None), (0.85, "#ff5f6d", None), (1, "#e8365f", None)],
        kind="radial",
    ),
    stroke="none",
    effects=[
        {"effect": "stylize.outerGlow", "params": {"color": "#ff8a5c", "opacity": 85, "blur": 90, "mode": "screen"}},
        {"effect": "stylize.outerGlow", "params": {"color": "#ff3f6d", "opacity": 55, "blur": 30, "mode": "screen"}},
    ],
)

# ---------------------------------------------------------------- birds
for bx, by, s in [(268, 548, 1.0), (330, 512, 0.72), (742, 586, 0.86), (800, 552, 0.6)]:
    d = (
        f"M{bx - 18 * s},{by} Q{bx - 9 * s},{by - 11 * s} {bx},{by} "
        f"Q{bx + 9 * s},{by - 11 * s} {bx + 18 * s},{by}"
    )
    steps.append({"id": "draw_path", "params": {
        "d": d, "closed": False, "fill": "none", "stroke": "#2c1436",
        "strokeWidth": 3.2 * s, "name": "Bird"}})

def ridge(crest, fill, rim, rim_opacity, name):
    """A mountain silhouette plus a warm rim light along its crest."""
    path(crest + " L1080,1350 L0,1350 Z", fill, name=name)
    if rim:
        steps.append({"id": "draw_path", "params": {
            "d": crest, "closed": False, "fill": "none", "stroke": rim,
            "strokeWidth": 2.4, "opacity": rim_opacity, "name": name + " rim"}})


# ---------------------------------------------------------------- far range
ridge(
    "M0,838 L96,742 L188,812 L286,676 L392,800 L470,742 L556,822 L642,716 L742,808 L836,744 L928,820 L1010,770 L1080,830",
    "#2c1436", "#ff9f7a", 55, "Far ridge",
)

# ---------------------------------------------------------------- mid range
ridge(
    "M0,952 L104,848 L214,932 L328,802 L446,918 L556,860 L664,946 L782,838 L892,930 L986,872 L1080,946",
    "#1b0c27", "#ff8a6a", 30, "Mid ridge",
)

# ---------------------------------------------------------------- front ridge
ridge(
    "M0,1082 L126,976 L258,1064 L398,930 L536,1058 L672,986 L812,1084 L944,1002 L1080,1084",
    "#0b0513", "#c9605f", 18, "Front ridge",
)


def pine(x, base_y, h, w, fill, name="Pine"):
    def y_at(frac):
        return round(base_y - h * frac, 2)

    d = (
        f"M{x},{y_at(1)} "
        f"L{x - w / 2},{y_at(0.42)} L{x - w * 0.17},{y_at(0.42)} "
        f"L{x - w * 0.37},{base_y} L{x + w * 0.37},{base_y} "
        f"L{x + w * 0.17},{y_at(0.42)} L{x + w / 2},{y_at(0.42)} Z"
    )
    path(d, fill, name=name)


for x, base, h, w in [
    (86, 1078, 176, 62), (150, 1072, 118, 44), (214, 1052, 74, 30),
    (330, 1006, 92, 34), (470, 1050, 138, 50), (604, 1040, 104, 40),
    (742, 1062, 158, 56), (812, 1086, 96, 36), (900, 1040, 128, 46),
    (1010, 1076, 168, 60), (1054, 1090, 108, 40),
]:
    pine(x, base, h, w, "#100718")

# ---------------------------------------------------------------- typography
steps.append({
    "id": "text.create",
    "params": {
        "x": 540, "y": 1178, "text": "DUSK", "size": 196,
        "font": "Helvetica", "justify": "center", "color": "#fff6ec",
    },
})
steps.append({
    "id": "effect.apply",
    "params": {"effect": "stylize.outerGlow", "params": {"color": "#ff5f7a", "opacity": 70, "blur": 34, "mode": "screen"}},
})
steps.append({
    "id": "text.create",
    "params": {
        "x": 540, "y": 1236,        "text": "AN EVENING STUDY", "size": 27,
        "font": "Helvetica", "justify": "center", "color": "#ffc9b4",
    },
})
steps.append({
    "id": "draw_shape",
    "params": {
        "shape": "rectangle", "x": 430, "y": 1268, "width": 220, "height": 1.5,
        "fill": "#ff8a7a", "stroke": "none", "opacity": 55, "name": "Rule",
    },
})
steps.append({
    "id": "text.create",
    "params": {
        "x": 540, "y": 1300, "text": "DRAWN BY AN AGENT  ·  VECTORCRAFT MCP", "size": 15,
        "font": "Helvetica", "justify": "center", "color": "#ff9d8b",
    },
})
steps.append({
    "id": "object.setProps",
    "params": {"name": "Colophon", "opacity": 62},
})

session = [
    {"tool": "run_command", "args": {"command": "file.new", "params": {
        "width": W, "height": H, "units": "Pixels", "name": "Dusk"}}},
    {"tool": "command_batch", "args": {"atomic": True, "label": "Dusk poster", "steps": steps}},
    {"tool": "run_command", "args": {"command": "document.inspect", "params": {"depth": 1}}},
    {"tool": "save_file", "args": {"path": "work/out/dusk.vectorcraft"}},
    {"tool": "export", "args": {"path": "work/out/dusk.svg", "format": "svg"}},
    {"tool": "export", "args": {"path": "work/out/dusk.png", "format": "png", "scale": 1}},
]
for line in session:
    print(json.dumps(line))
