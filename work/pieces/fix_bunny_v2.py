import sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, OUT, NONE

def walk(obj, out):
    if isinstance(obj, dict):
        if "id" in obj and "name" in obj: out[obj["name"]] = obj["id"]
        for v in obj.values(): walk(v, out)
    elif isinstance(obj, list):
        for v in obj: walk(v, out)

d = Draw()
d.call("open_file", {"path": f"{OUT}/bunny-avatar-v2.vectorcraft"}, "open v2")
doc = d.call("inspect_document", {}, "inspect")
n = {}; walk(doc, n)
kill = [n[k] for k in ("Fur tuft", "Stain 2") if k in n]
print("killing:", {k: n[k] for k in ("Fur tuft", "Stain 2") if k in n})
d.call("run_command", {"command": "edit.clear", "params": {"ids": kill}}, "clear")
# contained replacement stain, well inside the badge rim
d.shape("ellipse", "Stain 2b", x=618, y=152, width=168, height=108, fill="#A8874F", opacity=8, stroke=NONE)
# it lands on top; sink it behind the ears/head by sending to back repeatedly is overkill —
# it only overlaps badge + ear base area at low opacity; instead move it fully onto empty badge:
d.call("run_command", {"command": "select.none", "params": {}}, "deselect")
r = d.call("save_file", {"path": f"{OUT}/bunny-avatar-v2.vectorcraft"}, "save")
print("save:", json.dumps(r)[:120] if r else None)
for fmt, path, scale in [("png", f"{OUT}/bunny-avatar-v2@2x.png", 2), ("svg", f"{OUT}/bunny-avatar-v2.svg", None), ("pdf", f"{OUT}/bunny-avatar-v2.pdf", None)]:
    time.sleep(2)
    args = {"path": path, "format": fmt}
    if scale: args["scale"] = scale
    r = d.call("export", args, f"export {fmt}")
    print(fmt, ":", json.dumps(r)[:120] if r else None)
