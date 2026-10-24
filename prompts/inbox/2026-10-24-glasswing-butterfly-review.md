## Glasswing V1R00 — transparency is proven by what's underneath

- Kind: analysis
- Source: #1123, `work/insects/glasswing-butterfly-V1R00.py`, `art/insects/glasswing-butterfly/`
- Applies to: field plates — insects, transparent/translucent materials
- Status: pending

### Evidence

The brief's trap is "two glass shards with a body glued between." Three
moves kept it alive: (1) the whole insect is rotated ~14° in-plane and its
tarsi land on a real leaf line, which kills the pinned-specimen symmetry;
(2) the perch leaf is drawn *before* the wings and angled so the blade
runs under the right-hand panels — the green reads through the glass fill
(`#DCE9EE` at ~22% object opacity), which is the only honest way to prove
transparency on a plate; (3) legs are drawn before the wings so they
emerge from under the wing edges onto the leaf — legs drawn over the
panels read as stray veins crossing the membrane.

Wing construction is the monarch recipe adapted: border as a compound
path (outline + reversed `inset()`), glass panel as the inset shape at
low opacity, veins radiating to outline vertices at 3pt/50% — quiet
enough for membrane. Greta tells: cream subapical band clipped to the
apical border (quad interpolated between outline and inset edges at
vertices 5–7), small dark cell-end bar inside the forewing glass, pale
marginal thread inside the hindwing border.

### Proposed change

For `prompts/series/` insect notes on next consolidation: "Sell glass with
what shows through it: stage a leaf/part under the translucent fill before
the wing, and never draw legs over a panel." A proposal does not override
current house rules.
