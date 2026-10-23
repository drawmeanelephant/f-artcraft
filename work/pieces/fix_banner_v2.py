#!/usr/bin/env python3
"""Surgical fixes for bunny-banner-v2: stamp text into box, hide plate behind ears, tone down tail."""
import sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, OUT, NONE

INK = "#38332A"; RED = "#B03A2E"

def walk(obj, out):
    if isinstance(obj, dict):
        if "id" in obj and "name" in obj:
            out[obj["name"]] = obj["id"]
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)

d = Draw()
d.call("open_file", {"path": f"{OUT}/bunny-banner-v2.vectorcraft"}, "open banner v2")
doc = d.call("inspect_document", {}, "inspect full")
n = {}
walk(doc, n)
print("targets:", {k: n.get(k) for k in ("Label 2-0", "Handle 2-0", "Stamp text", "Stamp echo", "Tail")})

kill = [n[k] for k in ("Label 2-0", "Handle 2-0", "Stamp text", "Stamp echo", "Tail") if k in n]
d.call("run_command", {"command": "edit.clear", "params": {"ids": kill}}, "clear bad nodes")

# tail back in, toned to the shaded body
d.shape("ellipse", "Tail", x=1022, y=378, width=52, height=52, fill="#AFA486",
        stroke=INK, strokeWidth=5)

# stamp: faint second strike first, main text on top, both inside the box (y=208 proven)
d.text("ERROR", "Stamp echo", x=1308, y=210, size=74, font="Source Sans 3",
       color=RED, justify="center", opacity=22)
d.text("ERROR", "Stamp text", x=1306, y=208, size=74, font="Source Sans 3",
       color=RED, justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for nd in (doc or {}).get("nodes", []):
    if str(nd.get("name", "")).startswith("Stamp"):
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": nd["id"], "style": "Bold"}}, "bold stamp")

# re-export
d.call("run_command", {"command": "select.none", "params": {}}, "deselect")
r = d.call("save_file", {"path": f"{OUT}/bunny-banner-v2.vectorcraft"}, "save")
print("save:", json.dumps(r)[:120] if r else None)
for fmt, path, scale in [("png", f"{OUT}/bunny-banner-v2@2x.png", 2),
                         ("svg", f"{OUT}/bunny-banner-v2.svg", None),
                         ("pdf", f"{OUT}/bunny-banner-v2.pdf", None)]:
    time.sleep(1)
    args = {"path": path, "format": fmt}
    if scale: args["scale"] = scale
    r = d.call("export", args, f"export {fmt}")
    print(fmt, ":", json.dumps(r)[:120] if r else None)
print("FIXES DONE")
