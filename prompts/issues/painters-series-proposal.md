# Painters — milestone cards, new series (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece.

## Rationale

The portrait side of the milestone grammar, sibling to `musicians` and
`scientists`. Same `WORK · YEAR` line as musicians; the subject is the
person, the work survives only as a stylized backdrop motif. The roster
spans six centuries and five traditions — easel, woodblock, fresco,
abstraction — so no two cards should share a posture or palette.

## Format (milestone cards — field-plate chassis)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (centre 500,460, r≈420) → subject → name in caps, Virelai Sans ~56–60pt
  at y≈930.
- The milestone line under the name in caps, Virelai Sans ~22–24pt, wide
  tracking, y≈968, ≤760pt wide — check it clears the disc's lower arc.
- Gradients and translucent shading, never flat fills. Warm dark ink,
  never pure black. Nothing crosses the rim; shapes near the lower edge
  close on the disc's own arc.
- Likeness comes from interpreting references — iconic traits and
  posture, not tracing a photograph. The named work is evoked as a
  backdrop motif, never reproduced — the card is a portrait, not a print
  of the painting. No museum logos or trademark imagery. The milestone
  line is the defining work and year — `WORK · YEAR`.
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/painters/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/painters/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).
- New directories on first leaf: `art/painters/`, `work/painters/`.

## Proposed leaves (12)

### leonardo da vinci — `MONA LISA · 1503`

The universal man at the easel: long beard, soft cap, a sketchbook of
mirror-script; sfumato haze as the backdrop texture — a smile implied in
smoke, not drawn.

### michelangelo — `SISTINE CEILING · 1512`

Working overhead on scaffold planks, brush raised, plaster dust falling;
the famous near-touch of two hands implied in negative space at the rim,
never quoted.

### rembrandt — `THE NIGHT WATCH · 1642`

The master of light holding a palette against deep brown-black; the
light itself is the portrait — one warm source, everything else sinking
to umber.

### johannes vermeer — `THE PEARL EARRING · 1665`

The quiet interior: easel by a left window, a map on the wall behind,
cool Delft light laid on the face. Keep the pearl as one glint at the
edge of shadow.

### hokusai — `THE GREAT WAVE · 1831`

The elderly brushman of the eastern capital: wave-curl vignette curling
under the disc floor like a held breath; indigo and paper-white.

### vincent van gogh — `THE STARRY NIGHT · 1889`

Straw hat, pipe, a swirling impasto sky rendered as translucent spiral
strokes — the brushstroke is the man.

### edvard munch — `THE SCREAM · 1893`

On the bridge boards: elongated sunset bands behind him, his own posture
a quieter echo of the famous figure — hands at the lapels, not the
cheeks.

### gustav klimt — `THE KISS · 1908`

In the famous smock, cat under one arm; gold-leaf shimmer confined to a
small corner motif — gradients and broken gilding, never a flat gold
block.

### pablo picasso — `GUERNICA · 1937`

Striped shirt before a huge canvas; angular black-and-white shapes
suggested in the backdrop — a bull profile at most, no reproduction of
the mural.

### frida kahlo — `THE TWO FRIDAS · 1939`

Braided crown with flowers, the joined brow, Tehuana dress suggested by
collar embroidery; one small charm — monkey or hummingbird — no
self-portrait quotation.

### edward hopper — `NIGHTHAWKS · 1942`

The solitary realist at a diner-window edge: a wedge of lit glass at his
back, hat brim level, the loneliest light in the series.

### yayoi kusama — `INFINITY NETS · 1959`

The queen of dots: bobbed hair, a field of net-dot rings spreading
across the disc floor around her — the only card where the backdrop
pattern is the work's own idiom.

## Alternates pool

claude-monet · salvador-dali · georgia-okeeffe · jean-michel-basquiat ·
mark-rothko · jackson-pollock · artemisia-gentileschi ·
hilma-af-klint · caspar-david-friedrich · grant-wood · rene-magritte ·
m-c-escher · sandro-botticelli · raphael · caravaggio ·
j-m-w-turner · mary-cassatt · henri-matisse · wassily-kandinsky ·
andy-warhol · diego-rivera · jacob-lawrence · john-james-audubon ·
henri-de-toulouse-lautrec · edgar-degas · paul-cezanne · francisco-goya ·
diego-velazquez · berthe-morisot · norman-rockwell · grandma-moses

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Painters — milestone cards, wave 1" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
