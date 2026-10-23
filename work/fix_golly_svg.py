import sys, json
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from vc import Draw, OUT
d = Draw()
r = d.call("export", {"path": f"{OUT}/golly.svg", "format": "svg"}, "export golly svg retry")
print("svg:", json.dumps(r)[:200] if r else None)
