import sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, OUT
d = Draw()
r = d.call("export", {"path": f"{OUT}/golly.svg", "format": "svg"}, "export golly svg retry")
print("svg:", json.dumps(r)[:200] if r else None)
