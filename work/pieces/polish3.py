import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_client import MCP
m = MCP(["--connect", "127.0.0.1:7979"]); m.init()
r = m.call("run_command", {"command": "edit.clear", "params": {"ids": [97, 98]}})
print("cleared back-curl details:", r)
r = m.call("run_command", {"command": "select.none", "params": {}})
print("select none:", r)
