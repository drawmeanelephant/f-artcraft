#!/usr/bin/env python3
"""Minimal MCP stdio client for `vectorcraft-cli mcp` (newline JSON-RPC)."""
import json, os, shutil, subprocess, threading

# vectorcraft-cli location: env wins, then PATH, then known install spots.
CLI = (os.environ.get("VECTORCRAFT_CLI")
       or shutil.which("vectorcraft-cli")
       or next((p for p in (
           os.path.expanduser("~/.local/bin/vectorcraft-cli"),
           "/home/hatch/workspace/vectorcraft/app/vectorcraft-0.13.1-linux-x86_64/bin/vectorcraft-cli",
       ) if os.path.exists(p)), "vectorcraft-cli"))

class MCP:
    def __init__(self, args):
        self.p = subprocess.Popen([CLI, "mcp"] + args,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, text=True, bufsize=1)
        self._id = 0
        self.err = []
        threading.Thread(target=self._drain_err, daemon=True).start()

    def _drain_err(self):
        for line in self.p.stderr:
            self.err.append(line.rstrip())

    def send(self, obj):
        self.p.stdin.write(json.dumps(obj) + "\n"); self.p.stdin.flush()

    def request(self, method, params=None):
        self._id += 1
        rid = self._id
        self.send({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}})
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError(f"server closed; stderr tail: {self.err[-5:]}")
            msg = json.loads(line)
            if msg.get("id") == rid:
                if "error" in msg:
                    raise RuntimeError(f"RPC error: {msg['error']}")
                return msg.get("result")

    def call(self, tool, args=None):
        res = self.request("tools/call", {"name": tool, "arguments": args or {}})
        texts = [c["text"] for c in res.get("content", []) if c.get("type") == "text"]
        joined = "\n".join(texts)
        if res.get("isError"):
            raise RuntimeError(f"tool {tool} error: {joined[:600]}")
        try:
            return json.loads(joined) if joined else {}
        except Exception:
            return {"raw": joined, "_images": [c for c in res.get("content", []) if c.get("type") == "image"]}

    def init(self):
        r = self.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                        "clientInfo": {"name": "fart-knocker", "version": "1.0"}})
        self.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return r
