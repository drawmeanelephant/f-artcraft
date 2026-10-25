# Scientists — milestone cards, wave 2 (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece. Wave 1 shipped via #1563 (leaves
#1545–1559) — every leaf below is new.

## Wave 1 inventory (do not duplicate)

ada-lovelace · alan-turing · albert-einstein · charles-darwin ·
chien-shiung-wu · galileo-galilei · isaac-newton · jane-goodall ·
jennifer-doudna · katherine-johnson · marie-curie · nikola-tesla ·
rosalind-franklin · stephen-hawking · tu-youyou

Wave 1 leaned physics/computing/biology-modern. Wave 2 widens the bench:
taxonomy, genetics, chemistry, medicine, statistics and ecology, plus
more pre-20th-century and non-Anglo subjects.

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
  posture, not tracing a photograph. Instruments stay period-correct; no
  modern-device anachronisms. The milestone line is the landmark and
  year — `WORK · YEAR`.
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/scientists/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/scientists/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).

## Proposed leaves (12)

### carl linnaeus — `SYSTEMA NATURAE · 1735`

The namer of everything: 18th-century dress, quill over a specimen
sheet, the twinflower (*Linnaea borealis*) at the disc floor.

### gregor mendel — `HEREDITY LAWS · 1866`

Augustinian friar in the abbey garden: pea plants staked in rows behind
him, round and wrinkled seeds in an open palm.

### louis pasteur — `RABIES VACCINE · 1885`

Beard and bow tie over swan-neck flasks: broth flasks on the disc floor,
one cracked open; the germ theory in glassware.

### james clerk maxwell — `ELECTROMAGNETISM · 1865`

Victorian beard and waistcoat; field-line arcs curling around a small
coil or the colour wheel he spun — the equations implied, not written.

### dmitri mendeleev — `PERIODIC TABLE · 1869`

Wild hair and beard; a loose grid of element cards dealt like a patience
layout — the empty cells waiting for undiscovered elements are the
drawing.

### george washington carver — `CROP ROTATION · 1896`

Lab coat over soil and peanut plants: beakers of dyes and oils beside
him, but the plant is the hero prop.

### alexander fleming — `PENICILLIN · 1928`

The untidy bench that changed medicine: hair parted, peering at an open
petri dish where a clear ring of mold lyses the bacteria around it.

### niels bohr — `ATOMIC MODEL · 1913`

The tall Dane with pipe or chalk; electron orbits arcing behind him like
a halo of shells — stylized, never a textbook diagram.

### florence nightingale — `POLAR CHART · 1858`

The lady with the lamp who was also the statistician: lamp in one hand,
her rose diagram (coxcomb) spread below — wedge slices in graduated
warm colours. Data as the portrait's second subject.

### barbara mcclintock — `JUMPING GENES · 1951`

In the cornfield: maize ears with variegated kernels and a field
notebook. The spotted kernels *are* the portrait of transposition — get
the kernel colour breaks right.

### jonas salk — `POLIO VACCINE · 1955`

Rolled sleeves over a rack of vaccine vials, pipette in hand, window
light — the famous pose without tracing the photograph.

### rachel carson — `SILENT SPRING · 1962`

At the tide line with a field notebook, one bird overhead; sea-air
palette, an empty nest at the rim suggesting the spring that goes quiet.

## Alternates pool

lise-meitner · emmy-noether · erwin-schrodinger · werner-heisenberg ·
richard-feynman · linus-pauling · edwin-hubble · henrietta-leavitt ·
jocelyn-bell-burnell · vera-rubin · grace-hopper · tim-berners-lee ·
margaret-hamilton · mary-anning · mary-leakey · joseph-lister ·
robert-koch · al-khwarizmi · ibn-al-haytham · zhang-heng · carl-sagan ·
alfred-russel-wallace · annie-jump-cannon · cecilia-payne-gaposchkin

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Scientists — milestone cards, wave 2" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
