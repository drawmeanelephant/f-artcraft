## Reticulated python V1R00 — a coil mound needs stagger, not stacking

- Kind: lesson
- Source: issue #1107, `work/animals/draw_reticulated_python.py`,
  `art/animals/reticulated-python/reticulated-python-V1R00.*`
- Applies to: animals field plates; any coiled/looped subject
- Status: pending

### Evidence

The mound is three closed blobs bottom-to-top, each carrying a `net_chain`:
dark diamond cells along a quad spine, joined corner-to-corner by cream
strands. The cream strands — not the diamonds — sell the reticulation; the
diamonds alone read as armour plates.

What worked: name at 48pt keeps the 18-char `RETICULATED PYTHON` at 619pt,
well inside the rim; the river reads from only a fading linear-glint strip
+ a dark far-bank ribbon behind the floor arc. What nearly failed: coils
stacked dead-centre read as pancakes/wedding cake; offsetting the middle
coil ~16pt right makes the pile spiral. A fully centred stack is the trap.
The neck is a thick stroked curve whose "ribs" are just alternating
dark/cream cross-strands — cheap and effective at plate scale.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: "Coiled subjects: build
the mound as stacked loops, but stagger each loop's centre or the pile
reads as pancakes. Link pattern cells with a second light strand colour —
cells alone read as armour, the net is what reads as reticulated."
