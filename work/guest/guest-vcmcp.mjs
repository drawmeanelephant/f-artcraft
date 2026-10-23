#!/usr/bin/env node
// Tiny MCP stdio client for `vectorcraft-cli mcp`.
// One process = one VectorCraft session, so a whole drawing fits in one script.
//
//   node tools/vcmcp.mjs --list                 # tool names + one-line descriptions
//   node tools/vcmcp.mjs --schema <tool>        # full JSON schema of one tool
//   node tools/vcmcp.mjs path/to/session.jsonl  # run a script of tool calls
//   cat session.jsonl | node tools/vcmcp.mjs -
//
// A script line is either {"tool": "<name>", "args": {...}} or a raw
// {"method": ..., "params": ...} JSON-RPC request. Blank lines and `#` comments are skipped.
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { readFileSync } from "node:fs";

const CLI = process.env.VECTORCRAFT_CLI ?? `${process.env.HOME}/.local/bin/vectorcraft-cli`;
const argv = process.argv.slice(2);
const listOnly = argv.includes("--list");
const schemaIdx = argv.indexOf("--schema");
const schemaTool = schemaIdx >= 0 ? argv[schemaIdx + 1] : null;
const scriptPath = argv.find((a) => !a.startsWith("--") && a !== schemaTool);

const child = spawn(CLI, ["mcp", "--headless"], { stdio: ["pipe", "pipe", "pipe"] });
child.stderr.on("data", (d) => {
  const text = String(d).trim();
  if (text) console.error(`[vc] ${text}`);
});

let nextId = 1;
const pending = new Map();
const rl = createInterface({ input: child.stdout });
rl.on("line", (line) => {
  if (!line.trim()) return;
  let msg;
  try {
    msg = JSON.parse(line);
  } catch {
    console.error(`[vc] unparsable line: ${line.slice(0, 200)}`);
    return;
  }
  if (msg.id !== undefined && pending.has(msg.id)) {
    const { resolve } = pending.get(msg.id);
    pending.delete(msg.id);
    resolve(msg);
  }
});

function send(method, params, timeoutMs = 120000) {
  const id = nextId++;
  const payload = { jsonrpc: "2.0", id, method, ...(params ? { params } : {}) };
  child.stdin.write(JSON.stringify(payload) + "\n");
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new Error(`${method} timed out after ${timeoutMs} ms`));
    }, timeoutMs);
    pending.set(id, {
      resolve: (m) => {
        clearTimeout(timer);
        if (m.error) reject(new Error(`${method}: ${JSON.stringify(m.error)}`));
        else resolve(m.result);
      },
    });
  });
}

async function callTool(name, args = {}) {
  const result = await send("tools/call", { name, arguments: args });
  if (result?.isError) {
    const text = (result.content ?? []).map((c) => c.text ?? "").join("\n");
    throw new Error(`${name} failed: ${text}`);
  }
  const texts = (result?.content ?? []).filter((c) => c.type === "text").map((c) => c.text);
  if (result?.structuredContent !== undefined) return result.structuredContent;
  if (texts.length === 1) {
    try {
      return JSON.parse(texts[0]);
    } catch {
      return texts[0];
    }
  }
  return texts.length ? texts : result;
}

function lines() {
  const raw = scriptPath === "-" ? readFileSync(0, "utf8") : readFileSync(scriptPath, "utf8");
  return raw
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"));
}

async function main() {
  await send("initialize", {
    protocolVersion: "2025-06-18",
    capabilities: {},
    clientInfo: { name: "freebuff-vcmcp", version: "1.0.0" },
  });
  child.stdin.write(JSON.stringify({ jsonrpc: "2.0", method: "notifications/initialized" }) + "\n");

  if (listOnly) {
    const { tools } = await send("tools/list", {});
    for (const t of tools) {
      const first = (t.description ?? "").split("\n")[0].slice(0, 120);
      console.log(`${t.name}\t${first}`);
    }
    return;
  }
  if (schemaTool) {
    const { tools } = await send("tools/list", {});
    const tool = tools.find((t) => t.name === schemaTool);
    if (!tool) throw new Error(`no tool named ${schemaTool}`);
    console.log(JSON.stringify(tool, null, 2));
    return;
  }
  if (!scriptPath) {
    console.error("usage: vcmcp.mjs --list | --schema <tool> | <session.jsonl|->");
    process.exitCode = 2;
    return;
  }

  let n = 0;
  for (const line of lines()) {
    n++;
    const step = JSON.parse(line);
    const label = step.tool ?? step.method ?? `step ${n}`;
    try {
      const out =
        step.tool !== undefined
          ? await callTool(step.tool, step.args ?? step.arguments ?? {})
          : await send(step.method, step.params);
      const text = typeof out === "string" ? out : JSON.stringify(out);
      const cap = Number(process.env.VC_MAX_OUT ?? 4000);
      console.log(`--- ${n}. ${label} ok\n${text.length > cap ? text.slice(0, cap) + `… [${text.length} chars]` : text}`);
    } catch (e) {
      console.log(`--- ${n}. ${label} ERROR\n${e.message}`);
      if (!process.env.VC_CONTINUE) {
        process.exitCode = 1;
        return;
      }
    }
  }
}

main()
  .catch((e) => {
    console.error(`fatal: ${e.message}`);
    process.exitCode = 1;
  })
  .finally(() => {
    child.stdin.end();
    setTimeout(() => child.kill(), 200);
  });
