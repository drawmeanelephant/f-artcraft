# Art Loop — Prompts & Rounds

The loop: **prompt → build in VectorCraft → export PDF/PNG proof → written analysis
(what worked, what didn't, with specifics) → fold the analysis into the next prompt →
next round.** A prompt is "done" when its analysis section says the piece survives
its own critique. House rules learned the hard way:

- Gradients and translucent shading, never flat fills (the bunny v1 rule).
- Check the proof render before calling it finished: arcs in frame, no leaked
  shapes past badges/rims, no overset, nothing clipped at canvas edges.
- Lettering: Virelai Sans. Ornaments: Virelai Mascots glyphs (U+E002–E00A).
- Every piece ships as `.vectorcraft` + `.svg` + `.pdf` + `@2x.png`.
- Never overwrite a piece: revisions are `<slug>-V<V>R<RR>` — see the
  revision rule in [AGENTS.md](AGENTS.md).

Repo layout when this goes to git: `art/` (native + exports), `pdf/` (proofs),
`prompts/` (this file, split per round), `analysis/` (one note per round).

**Guests & correspondents:** work from guests — other agents, people who don't
natively draw, paint and mixed-media artists — is received with appreciation,
not critique. The analysis step for guest work records what it does and what it
brings; the red pen is for in-house rounds only. Effort is the entry fee, and
it's always paid in full.

---

## Round-robin bank — Fart Knocker

1. **FK-01 · The Night Shift.** Fart Knocker at a filing cabinet at 2 a.m., desk lamp
   (Mascots candle glyph for the flame), stamping paperwork FILED. Navy/olive night
   palette, one warm lamp pool. Landscape 1500×1000.
2. **FK-02 · Tea Ceremony.** Full formal: Fart Knocker pouring tea from a filing-drawer
   teapot, tentacles as the tea set handles. Deadpan. Cream/gold, square 1200×1200.
3. **FK-03 · Wanted Poster.** Old-west style poster: portrait center, "WANTED FOR
   EXCELLENT ENGINEERING" in Virelai Sans, aged paper, nail holes in corners.
   Portrait 1000×1400.
4. **FK-04 · The Flatlophone Recital.** Fart Knocker performing on the Flatlophone
   (serious engineering), music stand, three small eighth-notes as tentacle curls.
   Wide 1600×900.

## Round-robin bank — Jolly (the regular Muse)

5. **JM-01 · Jolly Gardener.** Jolly holding a tiny watering can over a sprouting
   envelope plant (correspondence art nod). Soft spring palette. 1000×1100.
6. **JM-02 · Jolly Reads a Letter.** Seated Jolly, oversized letter, eyes mid-blink,
   heart glyph small. Warm paper tones. 1000×1100.
7. **JM-03 · Jolly in the Rain.** One umbrella, too small; blush replaced by rain
   streaks on the face plate. Blue-grey palette, same body rig. 1000×1100.
8. **JM-04 · Jolly & Fart Knocker, Tea for Two.** The crossover at full size: both at
   a small table, FK's bowtie vs Jolly's blush, one teapot. 1400×1050.

## Round-robin bank — Filed & Forgotten (bunny & Golly)

9. **FF-01 · Banner Bunny, Interior.** The banner bunny at v2-avatar quality inside a
   full office: cabinets, dangling ERROR tags, one (1) ray of hope through blinds.
   1500×750.
10. **FF-02 · Golly's Day Off.** Golly the guillotine at the beach: blade up like a
    sunshade, bowtie intact, bucket and spade. Must remain cheerful. 1100×1200.
11. **FF-03 · The Bunny, Stamp POV.** Extreme close-up: bunny face behind a huge
    descending ERROR stamp, motion lines. Red/sepia. 1200×900.

## Round-robin bank — Ornaments & type

12. **OR-01 · Divider Set No. 2.** Three production dividers: (a) tentacle-scroll,
    (b) Mascots medley (candle–diamond–scroll), (c) pure geometry in Virelai spirit.
    One sheet, 1400×900, each labeled in Virelai Sans.
13. **OR-02 · Ex Libris.** A bookplate: corner-flourish frame, octopus glyph center,
    "EX LIBRIS FART KNOCKER" — print-ready at 800×1000 with a bleed-safe margin.
14. **OR-03 · The Empathegy Seal.** Take one doctrine (Symbolic Completion) and make
    its official seal: green seal circle, "SIGN ECLIPSES FACT" around a stamp core.
    (Circular text will need hand-placed letters — budget the time.) 1000×1000.

## Field plates — Animals (`art/animals/`)

A standing series, not a round-robin: one **field-guide plate** per animal,
`<slug>-V<V>R<RR>` as usual. Canvas 1000×1000. Composition: dark moody
backdrop → one large gradient plate disc → the animal → its name in caps,
Virelai Sans (~56–60pt) at the bottom. Portraits for face-forward animals,
full-body when the silhouette is the point (narwhal tusk, pangolin scales,
tardigrade segments). Living in `art/animals/<slug>/`, scripts in
`work/animals/`. Roster so far:

- axolotl · fennec fox · pangolin · aye-aye
- narwhal · okapi · tardigrade · mantis shrimp
- quokka · markhor (all V1R00)

Pool for later agents: capybara, fossa, saiga, secretary bird, jerboa,
kakapo, tapir, sun bear, shoebill, dumbo octopus, gerenuk, maned wolf,
aye-aye full body, blobfish (controversial), potoo, vaquita.

Known trap: decorative shapes near the plate's lower edge must end on the
disc's own arc (`A420,420 0 0 1 …` close) or they leak past the rim.

---

## Analysis log

- **Round 0 — the existing body of work:** see `ANALYSIS-ROUND-0.md`.
  Baseline verdict: shading standard is set (portrait, bunny v2, Jolly set);
  recurring risks are clipped geometry at canvas edges and shapes reading
  flatter inside badges than in free compositions.
