#!/usr/bin/env python3
"""Turn the clean mascot render into pixel art, drawn as rectangles.

Run after the styles above:  python3 work/guest-whale-pixel.py > work/out/pixel.jsonl
"""
import json
import os
from PIL import Image

SRC = "work/out/_pixelsrc.png"
GRID = 40          # cells per side
CROP = (30, 130, 970, 920)   # the mascot with a little air around it
os.makedirs("work/out", exist_ok=True)

TILE = 1000
CELL = TILE / GRID

# every colour the grid may snap to, and the pixel-art colour it becomes
PALETTE = [
    ((0xFF, 0x00, 0xFF), None),          # magenta backdrop -> skip
    ((0x4D, 0x6B, 0xFE), "#4D6BFE"),     # body
    ((0x3B, 0x55, 0xE0), "#3550DD"),     # tail
    ((0xDC, 0xE8, 0xFF), "#BFD6FF"),     # belly
    ((0xFF, 0xFF, 0xFF), "#FFFFFF"),     # eye white / shine
    ((0x12, 0x1E, 0x42), "#0B1020"),     # pupil, mouth
    ((0xFF, 0x9F, 0xB2), "#FF9FB2"),     # blush
    ((0x6F, 0x8B, 0xFF), "#7FA0FF"),     # spout
]


def snap(px):
    best, dist = None, 1e9
    for rgb, out in PALETTE:
        d = sum((px[i] - rgb[i]) ** 2 for i in range(3))
        if d < dist:
            best, dist = out, d
    return best


src = Image.open(SRC).convert("RGB").crop(CROP)
w, h = src.size
rows = max(1, round(GRID * h / w))
cells = [[None] * GRID for _ in range(GRID)]
top = (GRID - rows) // 2
# sample each cell's centre: flat art, so the centre pixel is the true colour
for cy in range(rows):
    for cx in range(GRID):
        sx = min(w - 1, int((cx + 0.5) * w / GRID))
        sy = min(h - 1, int((cy + 0.5) * h / rows))
        cells[cy + top][cx] = snap(src.getpixel((sx, sy)))

rects = []


def add(x, y, w, color):
    rects.append({"id": "draw_shape", "params": {
        "shape": "rectangle", "x": round(x * CELL, 2), "y": round(y * CELL, 2),
        "width": round(w * CELL, 2), "height": round(CELL, 2),
        "fill": color, "stroke": "none"}})


# --- pixel-art cleanup: connect the fluke to the body
for y in range(GRID):
    row = cells[y]
    body_cols = [x for x, c in enumerate(row) if c == "#4D6BFE"]
    tail_cols = [x for x, c in enumerate(row) if c == "#3550DD"]
    if body_cols and tail_cols and min(body_cols) - max(tail_cols) in (1, 2, 3):
        for x in range(max(tail_cols) + 1, min(body_cols)):
            row[x] = "#3550DD"


# --- a deliberate face at 40 x 40: clear the sampled smears, then stamp it
egx = int((742 - CROP[0]) / (CROP[2] - CROP[0]) * GRID)
egy = int((492 - CROP[1]) / (CROP[3] - CROP[1]) * rows) + top
for y in range(max(0, egy - 6), min(GRID, egy + 12)):
    for x in range(max(0, egx - 16), min(GRID, egx + 6)):
        if cells[y][x] == "#0B1020":
            cells[y][x] = "#4D6BFE"

eye = [(0, 1), (1, 0), (2, 0), (3, 1), (0, 2), (1, 1), (2, 1), (3, 2)]
for dx, dy in eye:  # 4 x 4 white
    cells[egy - 2 + dy][egx - 2 + dx] = "#FFFFFF"
for dy in (1, 2):   # 2 x 2 pupil
    for dx in (1, 2):
        cells[egy - 2 + dy][egx - 2 + dx] = "#0B1020"

mgx, mgy = egx - 7, egy + 4
for dx, dy in [(0, 0), (1, 1), (2, 1), (3, 0)]:
    cells[mgy + dy][mgx + dx] = "#0B1020"

if __import__("os").environ.get("PIXEL_DEBUG"):
    import sys
    sym = {None: ".", "#4D6BFE": "B", "#3550DD": "b", "#BFD6FF": "L", "#FFFFFF": "W",
           "#0B1020": "K", "#FF9FB2": "p", "#7FA0FF": "s"}
    for row in cells:
        print("".join(sym[c] for c in row), file=sys.stderr)

for y in range(GRID):
    x = 0
    while x < GRID:
        c = cells[y][x]
        if c is None:
            x += 1
            continue
        run = 1
        while x + run < GRID and cells[y][x + run] == c:
            run += 1
        add(x, y, run, c)
        x += run

steps = [{"id": "draw_shape", "params": {
    "shape": "rectangle", "x": 0, "y": 0, "width": TILE, "height": TILE,
    "fill": "#0B1020", "stroke": "none", "name": "Backdrop"}}] + rects

session = [
    {"tool": "run_command", "args": {"command": "file.new", "params": {
        "width": TILE, "height": TILE, "units": "Pixels", "name": "whale-pixel"}}},
    {"tool": "command_batch", "args": {"atomic": True, "label": "whale pixel", "steps": steps}},
    {"tool": "save_file", "args": {"path": "work/out/whale-pixel.vectorcraft"}},
    {"tool": "export", "args": {"path": "work/out/whale-pixel.png", "format": "png", "scale": 1}},
    {"tool": "export", "args": {"path": "work/out/whale-pixel.svg", "format": "svg"}},
]
for line in session:
    print(json.dumps(line))
