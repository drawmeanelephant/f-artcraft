# Writers — milestone cards, new series (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece.

## Rationale

The largest untapped `WORK · YEAR` roster: a thousand years of literature
in the same portrait grammar as musicians and painters. Writers give the
plate quills, typewriters, hand-scrolls and one well-chosen prop per
card — and the widest non-Anglo spread of any proposed series.

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
  posture, not tracing a photograph. Keep dress and tools period-correct
  (a Heian lady does not hold a fountain pen); no book-cover or
  trademark imagery. The milestone line is the defining work and year —
  `WORK · YEAR`.
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/writers/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/writers/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).
- New directories on first leaf: `art/writers/`, `work/writers/`.

## Proposed leaves (12)

### murasaki shikibu — `TALE OF GENJI · 1008`

The Heian court lady: layered robes suggested by collar bands, brush
over a hand-scroll, one wisteria spray. The oldest card in the library —
let the palette be ink and silk.

### dante alighieri — `DIVINE COMEDY · 1320`

The exile in the laurel: red cappuccio hood, severe profile, a three-ring
gradient behind for the three cantiche.

### william shakespeare — `HAMLET · 1600`

The Chandos look: earring, loose collar, quill in hand. A small skull on
the disc floor is permitted — the one prop that needs no introduction.

### miguel de cervantes — `DON QUIXOTE · 1605`

The one-handed soldier: ruff, weathered face, a windmill silhouette
small on the horizon line — tilted, not tilting.

### jane austen — `PRIDE AND PREJUDICE · 1813`

Regency precision: bonnet, writing slope, modest table. The famous
silhouette is right-facing — honour the profile and the restraint.

### mary shelley — `FRANKENSTEIN · 1818`

The teenage author of the modern myth: high collar, a storm window
behind her, one stitch-line motif at the rim — never a bolt-necked
monster.

### edgar allan poe — `THE RAVEN · 1845`

Midnight palette: high collar, heavy eyes, a single raven shadow
crossing the disc floor. Keep him young and haunted, not a moustache
caricature.

### fyodor dostoevsky — `CRIME AND PUNISHMENT · 1866`

St. Petersburg fever: threadbare coat, an axe-edge of winter light, a
pawnbroker's window at most suggested.

### leo tolstoy — `WAR AND PEACE · 1869`

The count not yet turned peasant: keep the face mid-1860s, dark beard
beginning, officer's bearing; a birch line behind.

### virginia woolf — `MRS DALLOWAY · 1925`

Sharp profile, low bun, a river-stone of thought — flowing water in the
backdrop kept figurative, never literal drowning imagery.

### agatha christie — `ORIENT EXPRESS · 1934`

The duchess of death: cloche-era neatness at the typewriter; one small
clue as prop — a red kimono flash — no weapons, no gore.

### toni morrison — `BELOVED · 1987`

The Nobel voice in her editorial prime — keep the era 1980s, not the
later silver locs; a single tree line on the horizon is all the past
the card needs.

## Alternates pool

franz-kafka ·
gabriel-garcia-marquez · james-baldwin · zora-neale-hurston ·
emily-dickinson · charles-dickens · victor-hugo · jules-verne ·
oscar-wilde · alexandre-dumas · charlotte-bronte · mark-twain ·
chinua-achebe · rabindranath-tagore · matsuo-basho · rumi ·
pablo-neruda · jorge-luis-borges · isabel-allende · ursula-k-le-guin ·
octavia-butler · george-orwell · haruki-murakami · margaret-atwood ·
alexander-pushkin · vladimir-nabokov · nikolai-gogol · anton-chekhov ·
w-b-yeats · seamus-heaney · maya-angelou · audre-lorde · homer

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Writers — milestone cards, wave 1" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
