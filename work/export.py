import sys, json
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from mcp_client import MCP
m = MCP(["--connect", "127.0.0.1:7979"]); m.init()
OUT = "/home/hatch/workspace/vectorcraft/work/out"
r = m.call("save_file", {"path": f"{OUT}/fart-knocker.vectorcraft"})
print("save:", json.dumps(r)[:300])
for fmt, path, scale in [("png", f"{OUT}/fart-knocker@2x.png", 2),
                         ("svg", f"{OUT}/fart-knocker.svg", None),
                         ("pdf", f"{OUT}/fart-knocker.pdf", None)]:
    args = {"path": path, "format": fmt}
    if scale: args["scale"] = scale
    r = m.call("export", args)
    print(fmt, ":", json.dumps(r)[:300])
