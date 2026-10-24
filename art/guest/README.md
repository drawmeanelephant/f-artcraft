# Guest set — Freebuff

Seven SVGs from a guest: six renderings of a whale mascot for DeepSeek, and a dusk poster. Drawn
headless through VectorCraft's MCP server, one session per document, the same command-API way the
rest of this repo was drawn. Guest work, so no red pen — this note just records what it is and what
it brings.

| file | what it is |
|---|---|
| `whale-flat.svg` | flat mascot: halo, sparkles, bubbles, soft ground shadow |
| `whale-sticker.svg` | 20 px white outline, drop shadow, peach starburst, wordmark |
| `whale-neon.svg` | stroke-only whale, two stacked outer glows, teal spout, grid |
| `whale-doodle.svg` | 13 px navy outline, pastel fills, confetti, "hello, ocean" |
| `whale-sunset.svg` | the same path rotated −8° and scaled 0.62 over a gradient sky and glowing sun |
| `whale-pixel.svg` | 68 rectangles from a 40×40 grid sampled off a clean render |
| `dusk-poster.svg` | 1080×1350: gradient sky, glowing sun, three ridges with rim light, pines, live type |

The whale is one shape: seven cubic segments for the body, a two-lobed fluke, and a belly derived by
sampling the body outline and insetting it 26 px — so the light patch can't leave the silhouette.
Each style recomposes that geometry; the transform used for the sunset tile scales, rotates and
translates the same path data.

## Rebuild

```
mkdir -p work/out
python3 work/guest/guest-whale-styles.py > work/out/whales.jsonl
node work/guest/guest-vcmcp.mjs work/out/whales.jsonl           # SVGs, PNGs, natives, and _pixelsrc.png
python3 work/guest/guest-whale-pixel.py > work/out/pixel.jsonl  # reads that _pixelsrc.png
node work/guest/guest-vcmcp.mjs work/out/pixel.jsonl
python3 work/guest/guest-dusk-poster.py > work/out/dusk.jsonl
node work/guest/guest-vcmcp.mjs work/out/dusk.jsonl
```

`work/guest/guest-vcmcp.mjs` is a ~150-line stdio JSON-RPC client for `vectorcraft-cli mcp --headless`
(looks for `~/.local/bin/vectorcraft-cli`; `VECTORCRAFT_CLI` overrides it). The machine this was
drawn on had no MCP client of its own, so it speaks the protocol directly. The pixel pass needs
Pillow.

The SVGs here are byte-identical to what those commands produce. Natives, PDFs and PNG renders
land in `work/out/` and stay out of git, as with everything else in this repo.
