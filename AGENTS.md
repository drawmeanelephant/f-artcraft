# Agent rules — f-artcraft

Vector art drawn in VectorCraft over its MCP server. The loop, prompt bank and
house style live in [PROMPTS.md](PROMPTS.md); per-round critique in
`ANALYSIS-ROUND-*.md`.

## Revision rule (mandatory)

**Never overwrite an existing piece.** Every piece is versioned
`<slug>-V<V>R<RR>` — e.g. `ember-dusk-V1R01`. `V` is the interpretation
(the original artist's take is `V1`, another artist's riff is `V2`), `R`
is the revision inside it, counting from `00`. When improving a drawing:

- Start from the newest revision of the piece.
- Save the improved result as the next revision: bump `R` (`V1R01` → `V1R02`)
  for refinements of the same design; bump `V` and reset `R` (`V1R02` → `V2R00`)
  for a redesign or new direction.
- The suffix applies to every output of that revision: `.vectorcraft`, `.svg`,
  `.pdf`, `@2x.png`, and the driving script where it is revision-specific.
- First pass of a brand-new piece starts at `V1R00`. Work received from
  elsewhere is registered as `V1R00` (or consecutive `R`s when the dump
  itself holds revisions, e.g. `bunny-avatar` → `V1R00`/`V1R01`).
- Previous revision files are read-only. If a revision is bad, the next
  revision fixes it — nothing is edited in place or deleted.

## Driving VectorCraft

`vectorcraft-cli mcp` runs the MCP server on stdio (newline-delimited
JSON-RPC). `work/mcp_client.py` is the shared client; `work/vc.py` the shared
drawing helper.

- Connected mode: launch the app with `vectorcraft --control 7979`, then the
  MCP attaches to the live window (`ui_screenshot`, `pointer_gesture`, …).
- Headless mode: pass `--automation-read-root DIR` and
  `--automation-write-root DIR` — without a write root, no file can be saved.
- Draw with `draw_shape` / `draw_path`, paint with `set_paint`, check with
  `render_preview`, batch atomic edits with `command_batch`. Coordinates are
  points, y down, origin at the first artboard's top-left.

## Deliverables

Per PROMPTS.md: every revision ships `.vectorcraft` + `.svg` + `.pdf` +
`@2x.png`. Committed to git: the `.vectorcraft` native (JSON — SVG is not
an editable format), the `.svg`, the `@2x.png` and the driving script.
PDF proofs and scratch renders in `work/out/` stay local.

## The site

`docs/` generated output (data JSONs, site HTML, media copies) is a
build artifact — never committed. The deploy job rebuilds on latest
main, so nothing needs regen-by-hand: new pieces and new
`art/<category>/` dirs are discovered automatically (unknown
categories land on the plates page). The `docs-build` check only
verifies the scan + render still runs clean:

    python3 docs/gen_data.py   # scans art/ -> docs/data/*.json + docs/site/media/
    DOGBED=<dogbed binary> sh docs/build.sh   # -> docs/site/*.html
