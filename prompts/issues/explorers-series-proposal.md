# Explorers — milestone cards, new series (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece.

## Rationale

A `FEAT · YEAR` series that puts the milestone grammar in motion: ships,
sledges, aircraft and spacesuits as props — playing to the library's
strengths (the vehicles field plates already prove hulls and rigging at
disc scale). Spans a millennium and five continents; the people and the
gear get equal weight.

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
  posture, not tracing a photograph. Vessels, sledges and aircraft stay
  period-correct and generic: no real registrations, mission patches or
  flag-planting jingoism. The milestone line is the feat and year —
  `FEAT · YEAR`.
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/explorers/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/explorers/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).
- New directories on first leaf: `art/explorers/`, `work/explorers/`.

## Proposed leaves (12)

### leif erikson — `VINLAND · 1000`

The Norseman at a ship's prow: cloak pinned, shoreline spruce ahead.
Keep the gear tenth-century — no horned helmet, the perpetual trap.

### zheng he — `TREASURE VOYAGES · 1405`

Admiral of the treasure fleet: Ming robes, forearm out, a nine-masted
junk's prow behind. Vermilion and sea-green palette.

### ibn battuta — `RIHLA · 1325`

The far traveler of the Maghreb: desert robes, staff, a caravan horizon
line. Thirty years of road shown by the worn hem and the loaded mule —
the Rihla is the book he dictated at the end of them.

### ferdinand magellan — `CIRCUMNAVIGATION · 1522`

Captain-general mid-voyage: compass rose, strait spray. The line honours
the fleet's feat — brief should note Juan Sebastián Elcano completed the
circle; the card celebrates the expedition.

### roald amundsen — `SOUTH POLE · 1911`

The quiet professional: fur anorak, ski tips, a sledge dog at heel. A
white-out handled by warm light on the face; a small flag planted is
permitted but should not be the subject.

### ernest shackleton — `ENDURANCE · 1915`

The boss in the wreck: ship crushed in pack ice behind him, open
optimism in the face. The feat is the survival — draw the ice, not the
goal.

### edmund hillary — `EVEREST · 1953`

The beekeeper at the roof: oxygen mask pushed up, goggles, prayer-flag
flecks of colour on the ridge line. Paired with the tenzing-norgay card
— same summit hour, two different discs.

### tenzing norgay — `EVEREST · 1953`

The paired card: sherpa and sahib share one milestone. Ice axe raised at
the summit; his card stands alone — no shadow of the other man needed.

### nellie bly — `AROUND THE WORLD · 1890`

Seventy-two days: checkered ulster coat, one small gripsack bag, steamer
smoke behind. The world tour with a single bag — the bag is the joke and
the point.

### amelia earhart — `ATLANTIC SOLO · 1932`

Leather cap, goggles pushed up on the forehead, a Lockheed-style
silhouette low behind. Keep the aircraft generic — no real
registrations.

### yuri gagarin — `FIRST ORBIT · 1961`

The smile that circled the Earth: orange flight suit, helmet under one
arm, Earth's arc in the disc sky. No real mission patches.

### valentina tereshkova — `VOSTOK 6 · 1963`

First woman in space: white helmet ring, the seagull callsign evoked by
one bird glyph. Same Earth's curve as Gagarin, her card entirely her
own.

## Alternates pool

neil-armstrong · buzz-aldrin · mae-jemison · sally-ride · marco-polo ·
david-livingstone · gertrude-bell · isabella-bird · freya-stark ·
jacques-cousteau · thor-heyerdahl · sacagawea · matthew-henson ·
robert-falcon-scott · john-franklin · fridtjof-nansen ·
alexandra-david-neel · sven-hedin · jean-francois-champollion ·
mary-kingsley · james-cook · vitus-bering · juan-sebastian-elcano

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Explorers — milestone cards, wave 1" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
