import sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mcp_client import MCP
m = MCP(["--connect", "127.0.0.1:7979"]); m.init()

# find title id via inspect
doc = m.call("inspect_document", {"kind": "Type"})
print(json.dumps(doc)[:800])

# bold the title: style Bold on the FART KNOCKER text object
# inspect returns nodes with ids; pick the one whose name/text matches by listing all type nodes
nodes = doc.get("nodes", []) if isinstance(doc, dict) else []
for n in nodes:
    print("TYPE node:", n.get("id"), n.get("name"), n.get("bounds"))
