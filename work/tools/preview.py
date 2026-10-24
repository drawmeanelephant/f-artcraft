import sys, json, base64
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_client import MCP
m = MCP(["--connect", "127.0.0.1:7979"]); m.init()
r = m.call("render_preview", {"max_side": 1000})
imgs = r.get("_images", []) if isinstance(r, dict) else []
if imgs:
    open("/home/hatch/workspace/vectorcraft/work/out/preview1.png","wb").write(base64.b64decode(imgs[0]["data"]))
    print("preview saved")
else:
    print("render_preview raw:", json.dumps(r)[:500])
    # fallback: screenshot tool (artboard render)
    r2 = m.request("tools/call", {"name":"screenshot","arguments":{}})
    for c in r2.get("content",[]):
        if c.get("type")=="image":
            open("/home/hatch/workspace/vectorcraft/work/out/preview1.png","wb").write(base64.b64decode(c["data"]))
            print("screenshot-tool saved")
