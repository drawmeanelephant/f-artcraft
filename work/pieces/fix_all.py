import sys, json, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, OUT, NONE

def walk(obj, out):
    if isinstance(obj, dict):
        if "id" in obj and "name" in obj:
            out[obj["name"]] = obj["id"]
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)

def names(d):
    doc = d.call("inspect_document", {}, "inspect full")
    out = {}
    walk(doc, out)
    return out

def reexport(d, base):
    d.call("run_command", {"command": "select.none", "params": {}}, "deselect")
    r = d.call("save_file", {"path": f"{OUT}/{base}.vectorcraft"}, "save")
    print(base, "save:", json.dumps(r)[:120] if r else None)
    for fmt, path, scale in [("png", f"{OUT}/{base}@2x.png", 2), ("svg", f"{OUT}/{base}.svg", None), ("pdf", f"{OUT}/{base}.pdf", None)]:
        time.sleep(2)
        args = {"path": path, "format": fmt}
        if scale: args["scale"] = scale
        r = d.call("export", args, f"export {base} {fmt}")
        print(base, fmt, ":", json.dumps(r)[:120] if r else None)

# ---------- bunny avatar: move ERROR below the bowtie ----------
d = Draw()
d.call("open_file", {"path": f"{OUT}/bunny-avatar.vectorcraft"}, "open avatar")
n = names(d)
print("avatar nodes:", {k: v for k, v in n.items() if "ERROR" in k})
tid = [v for k, v in n.items() if k.startswith("ERROR")][0]
d.call("run_command", {"command": "edit.clear", "params": {"ids": [tid]}}, "clear ERROR")
d.text("ERROR", "ERROR text", x=500, y=912, size=72, font="Source Sans 3", color="#4A3A28", justify="center")
n = names(d)
tid = [v for k, v in n.items() if k.startswith("ERROR")][0]
d.call("run_command", {"command": "text.setStyle", "params": {"id": tid, "style": "Bold"}}, "bold ERROR")
reexport(d, "bunny-avatar")

# ---------- bunny banner: drop the stray tail, move stamp text into the box ----------
d = Draw()
d.call("open_file", {"path": f"{OUT}/bunny-banner.vectorcraft"}, "open banner")
n = names(d)
print("banner nodes:", {k: v for k, v in n.items() if k in ("Tail",) or "ERROR" in k})
if "Tail" in n:
    d.call("run_command", {"command": "edit.clear", "params": {"ids": [n["Tail"]]}}, "clear tail")
tid = [v for k, v in n.items() if k.startswith("ERROR")][0]
d.call("run_command", {"command": "edit.clear", "params": {"ids": [tid]}}, "clear stamp text")
d.text("ERROR", "Stamp text", x=1306, y=208, size=74, font="Source Sans 3", color="#B03A2E", justify="center")
n = names(d)
tid = [v for k, v in n.items() if k.startswith("ERROR")][0]
d.call("run_command", {"command": "text.setStyle", "params": {"id": tid, "style": "Bold"}}, "bold stamp")
reexport(d, "bunny-banner")

# ---------- golly: straight blade, tidy bowtie dots ----------
d = Draw()
d.call("open_file", {"path": f"{OUT}/golly.vectorcraft"}, "open golly")
n = names(d)
kill = [n[k] for k in ("Blade", "Blade facet", "Blade edge", "Bowtie dot 2", "Bowtie dot 3", "Bowtie dot 5") if k in n]
print("golly killing:", kill)
d.call("run_command", {"command": "edit.clear", "params": {"ids": kill}}, "clear blade+dots")
d.path("M312,368 L588,368 L588,428 L312,582 Z", "Blade", fill="#C9CFD4", stroke="#6E767C", strokeWidth=4)
d.path("M312,368 L588,368 L588,392 L312,528 Z", "Blade facet", fill="#E3E8EB", opacity=65, stroke=NONE)
d.path("M326,562 L574,442", "Blade edge", fill=NONE, stroke="#F4F7F8", strokeWidth=9, cap="round")
# the redrawn blade sits on top of everything; sink it back above the crossbar area is fine
# (it overlaps nothing but the posts/background). Now the dots:
for i, (x, y, c) in enumerate([(390, 914, "#3FA7D6"), (363, 906, "#7BC950"), (484, 912, "#FFD23F")]):
    d.shape("ellipse", f"Bowtie dot fix {i+1}", x=x, y=y, width=13, height=13, fill=c, stroke=NONE)
reexport(d, "golly")
print("ALL FIXES DONE")
