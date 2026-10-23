import sys
sys.path.insert(0, "/home/hatch/workspace/vectorcraft/work")
from mcp_client import MCP
m = MCP(["--connect", "127.0.0.1:7979"]); m.init()

r = m.call("run_command", {"command": "text.setStyle", "params": {"id": 95, "style": "Bold"}})
print("bold title:", r)

DARK = "#9E3B16"
spirals = [
    ("Curl detail back L", "M185,618 C185,600 210,592 222,606 C232,617 224,632 210,630"),
    ("Curl detail back R", "M615,618 C615,600 590,592 578,606 C568,617 576,632 590,630"),
    ("Curl detail mid L",  "M220,700 C220,684 242,677 252,689 C261,699 254,712 242,710"),
    ("Curl detail mid R",  "M580,700 C580,684 558,677 548,689 C539,699 546,712 558,710"),
    ("Curl detail front L","M239,804 C239,786 263,779 274,792 C284,803 276,818 262,815"),
    ("Curl detail front R","M561,804 C561,786 537,779 526,792 C516,803 524,818 538,815"),
]
for name, d in spirals:
    r = m.call("draw_path", {"d": d, "name": name, "fill": "none", "stroke": DARK,
                             "strokeWidth": 7, "opacity": 55, "cap": "round"})
    print("ok", name, "->", r.get("id"))
