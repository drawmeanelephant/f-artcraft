#!/usr/bin/env python3
"""Shared drawing helper over the VectorCraft MCP remote session."""
import sys, json
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from mcp_client import MCP

OUT = "/home/hatch/workspace/vectorcraft/work/out"
NONE = "none"

class Draw:
    def __init__(self):
        self.m = MCP(["--connect", "127.0.0.1:7979"])
        self.m.init()
        self.errors = []
        self.count = 0

    def call(self, tool, args, label):
        try:
            r = self.m.call(tool, args)
            self.count += 1
            return r
        except Exception as e:
            self.errors.append((label, str(e)))
            print(f"ERR {label}: {str(e)[:300]}")
            return None

    def new_doc(self, name, w, h):
        return self.call("run_command", {"command": "file.new", "params": {
            "name": name, "width": w, "height": h, "units": "Pixels",
            "backgroundContents": "white", "colorMode": "rgb"}}, f"file.new {name}")

    def shape(self, shape_, label, **kw):
        a = {"shape": shape_, "name": label}; a.update(kw)
        return self.call("draw_shape", a, label)

    def path(self, d, label, **kw):
        a = {"d": d, "name": label}; a.update(kw)
        return self.call("draw_path", a, label)

    def text(self, txt, label, **kw):
        a = {"text": txt}; a.update(kw)
        return self.call("add_text", a, label)

    def finish(self, base, scales=(2,)):
        self.call("run_command", {"command": "select.none", "params": {}}, "select.none")
        r = self.call("save_file", {"path": f"{OUT}/{base}.vectorcraft"}, "save")
        print("save:", json.dumps(r)[:160] if r else None)
        for fmt, path, scale in [("png", f"{OUT}/{base}@2x.png", 2),
                                 ("svg", f"{OUT}/{base}.svg", None),
                                 ("pdf", f"{OUT}/{base}.pdf", None)]:
            args = {"path": path, "format": fmt}
            if scale: args["scale"] = scale
            r = self.call("export", args, f"export {fmt}")
            print(fmt, ":", json.dumps(r)[:160] if r else None)
        r = self.m.call("render_preview", {"max_side": 1100})
        print(f"DONE {base}: calls={self.count} errors={len(self.errors)}")
        for lbl, e in self.errors:
            print(" -", lbl, ":", e[:200])
        return r

def rot_rect_path(cx, cy, w, h, deg):
    import math
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    pts = []
    for dx, dy in [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]:
        pts.append((cx + dx*c - dy*s, cy + dx*s + dy*c))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    return d
