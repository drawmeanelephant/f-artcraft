# Poetry — wave 2 proposal

Status: draft, not posted. Expansion proposal for `art/poetry/`. Each row
below is a **separate leaf-issue candidate**, not one task — the wave splits
into individual `Poetry graphic: <Subject>` issues when approved.

## Format reminder (from shipped pieces)

Per `work/poetry/draw_lim_0194_semantic_seymour.py` and
`work/poetry/draw_hai_019_kindy_mcexistentialcrisis.py`:

- Canvas 1000×1000. Dark backdrop gradient, plate ellipse `x=80 y=40
  w=840 h=840` (centre 500,460, r≈420), ~6pt rim stroke, 792×792 inner
  ring. The poem is the plate: stanzas set around a central vignette, or
  the whole composition dressed as a poster/document.
- Verse lines sit inside the disc as a title couplet (~20pt, upper area)
  or as the caption punch line; `NAME` ~56–58pt at y≈930–948; the
  second tracked line at y≈968 carries the catalogue number (e.g.
  `LIM-0194 SEMANTIC SEYMOUR`, tracking ≈170).
- Slugs prefix by form — `hai-` haiku set, `lim-` limerick — followed by
  the piece's own catalogue number, which is **not** the mascot number
  (`lim-0194-semantic-seymour` is Seymour M-071). New forms take new
  prefixes; numbers below are proposals, assigned at draw time.
- Driver `work/poetry/draw_<slug>.py` → `d.finish("<slug>-V1R00")`;
  commit `.vectorcraft`, `.svg`, `@2x.png`. Ghost tags/flecks stay
  ≤40 opacity; rim rule applies to anything touching the disc edge.

## Leaf briefs

Wave 1 shipped `hai-`/`lim-` only. Wave 2 opens the catalogue to other
verse forms — one plate per form, each with a subject the archive
already half-remembers.

| Slug | Subject | Mood / the drawing's job |
| --- | --- | --- |
| `con-0201-the-form-funnel` | Concrete (shaped) poem | Typographic plumbing; the lines themselves pour through a funnel silhouette into one stamp box |
| `ghz-0033-in-triplicate` | Ghazal | Incantatory filing; the radif `in triplicate` closing every couplet, drawn as three carbon layers |
| `vil-0504-do-not-fold` | Villanelle | Dogged recurrence; twin refrains `DO NOT FOLD` / `RETURN TO SENDER` alternating as stamped impressions |
| `son-0404-for-the-missing-page` | Sonnet | Formal grief, comic; fourteen ruled lines where the thirteenth is torn out |
| `ode-0412-ode-to-the-red-pencil` | Ode | Grateful severity; the pencil at rest, its shavings arranged as laurel |
| `bal-0121-ballad-of-archiva-dustwhisper` | Ballad | Archive legend; the whole plate dressed as a wanted poster, stanzas in the warrant text |
| `epi-0068-veritas-two-liner` | Epigram | Aphoristic bite with ceremony; two lines and a wax seal, nothing else needed |
| `ele-0512-elegy-for-a-deprecated-field` | Elegy | Tender deprecation; ruled lines fading to blank where the field retired |
| `tan-0070-uncacheable-ursula` | Tanka | Perishable grace; fresh on every load, remembered never |
| `hbn-0313-archive-napkin` | Haibun | Lunch-break reverie; a prose paragraph on a preserved napkin, closing haiku in the fold |
| `epc-0001-the-ledgeriad` | Mock-epic fragment | Heroic bookkeeping; canto markers down the margin, the hero a running total |
| `fnd-0103-dead-letter-office` | Found poem | Accidental lyricism; verse assembled entirely from dead-letter labels |

## Guardrails

- Recheck `art/poetry/` and `art/limericks/`/`art/haikus/` (the umbrella
  shares subjects with both), plus open/closed issues and open PRs,
  before writing any leaf issue or claiming.
- Prefixes are proposals: pick the next free catalogue number at draw
  time and record it on the second line, as wave 1 does.
- Forms new to the house (concrete, ghazal, villanelle, haibun) should
  ship one pilot first; a V2 riff follows the revision rule, not an
  in-place fix.
- Labels per `.github/LABELS.md`: `type:*` for the deliverable plus an
  explicit `work:*` intent per leaf.
