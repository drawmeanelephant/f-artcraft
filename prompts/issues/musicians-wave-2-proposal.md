# Musicians — milestone cards, wave 2 (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece. Wave 1 shipped via #1562 (leaves
#1529–1544) — every leaf below is new.

## Wave 1 inventory (do not duplicate)

antonio-vivaldi · aretha-franklin · billie-holiday · bob-dylan ·
david-bowie · elvis-presley · jimi-hendrix · john-coltrane ·
joni-mitchell · louis-armstrong · ludwig-van-beethoven · miles-davis ·
nina-simone · prince · wolfgang-amadeus-mozart

Wave 1 covered baroque→romantic composers, jazz anchors, soul, folk-rock
and pop. Wave 2 fills the gaps: baroque's other giant, romantic
ballet, opera, gospel, delta blues, country, gypsy jazz and big-band
swing.

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
  posture, not tracing a photograph. Keep instruments and props
  stylized; no logos, album covers or trademark imagery. The milestone
  line is the defining work and year — `WORK · YEAR`.
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/musicians/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/musicians/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).

## Proposed leaves (12)

### johann sebastian bach — `BRANDENBURG · 1721`

At a chamber organ or harpsichord: baroque wig, rolled sleeves, hands
mid-fugue, manuscript leaves pinned loose. The composer's composer —
stern warmth, not marble bust.

### pyotr ilyich tchaikovsky — `SWAN LAKE · 1876`

Bearded, high collar, baton raised. A single swan feather or small lake
vignette at the disc floor keeps the ballet inside the frame.

### maria callas — `NORMA · 1954`

La Divina mid-aria: sculpted cheekbones, dark upswept hair, statement
earrings, mouth open on the note. Candle-glow palette; the voice is the
subject, the glamour is secondary.

### django reinhardt — `MINOR SWING · 1937`

Gypsy-jazz guitarist: pomaded hair, moustache, left hand's two working
fingers on the fretboard of an oval-hole Selmer-style guitar. Keep the
instrument generic — no brand marks.

### duke ellington — `TAKE THE A TRAIN · 1939`

At the piano in profile: tuxedo, the famous half-grin, the band implied
by one muted brass shape behind. Cotton-club cream and gold.

### charlie parker — `ORNITHOLOGY · 1946`

Bird mid-flight on the alto: tilted head, horn raised high, cheeks full.
The saxophone is the drawing; a small bird-glyph nod is permitted but
not required.

### robert johnson — `CROSSROADS · 1936`

Delta bluesman at the fork: seated on a stump or crate, resonator-style
guitar, two dirt roads dividing behind. Sepia-dust palette; legendary
status shown by isolation, not hagiography.

### ella fitzgerald — `HOW HIGH THE MOON · 1947`

First lady of song at the mic: floral or pearl detail, eyes closed
mid-scat, ball-grille microphone. The voice as the drawing — posture
upright, joy contained.

### mahalia jackson — `PRECIOUS LORD · 1956`

Queen of gospel: robed or Sunday-best silhouette, head lifted, one hand
raised. Church-window gradient backdrop in amber and violet.

### patsy cline — `CRAZY · 1961`

Country torch singer: 50s stage dress, curled hair, vintage ribbon mic.
Honky-tonk neon softened to a warm disc glow.

### johnny cash — `FOLSOM PRISON · 1968`

The man in black: guitar slung high, jaw set, dark suit under a single
stage floodlight cone. Near-monochrome palette — but warm dark ink,
never pure black.

### freddie mercury — `BOHEMIAN RHAPSODY · 1975`

The showman: pick one era and own it — long-haired 1975 or iconic later
look — mic stand raised like a sceptre, mid-strut. Generic stagewear
only: no crest, no branded gear.

## Alternates pool

franz-schubert · frederic-chopin · clara-schumann · thelonious-monk ·
dave-brubeck · chet-baker · sonny-rollins · sarah-vaughan ·
muddy-waters · b-b-king · chuck-berry · buddy-holly · ray-charles ·
sam-cooke · otis-redding · james-brown · marvin-gaye · stevie-wonder ·
tina-turner · dolly-parton · hank-williams · joan-baez ·
leonard-cohen · kate-bush · bob-marley · michael-jackson ·
madonna · whitney-houston · amy-winehouse · bjork · janis-joplin ·
carlos-santana · herbie-hancock · wayne-shorter · glenn-gould ·
yo-yo-ma · luciano-pavarotti · bill-evans · edith-piaf

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Musicians — milestone cards, wave 2" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
