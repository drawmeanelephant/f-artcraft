## ocelot V1R00 — arc-closed floor does not protect scatter decor

- Kind: lesson
- Source: #1061, work/animals/draw_ocelot.py, art/animals/ocelot/ocelot-V1R00.*
- Applies to: animals field plates; any floor/foreground with loose scatter
- Status: pending

### Evidence

The leaf-litter floor closed correctly on the `A420,420` arc, but the
"fallen leaf" scatter sitting on it was placed by raw coordinates — a leaf
at (680,842) rode 2pt past the disc and `check_rim` flagged 183px. The arc
close only protects the floor shape itself; every scatter element on it
still needs its own radius check (kept leaves within ~r360 and the check
came back clean). Second note: the comma() tapered-ribbon helper (caracal's
tuft ribbon reused as a marking stamp) reads correctly as ocelot chain
spotting at 13–17pt wide.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: arc-closing the floor
seals the silhouette, not the garnish — scatter decor (leaves, pebbles,
petals) needs each anchor's dist(center)+extent held under the disc radius.
