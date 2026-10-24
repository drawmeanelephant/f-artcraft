## The Orient series — zodiac, festivals, symbols

A second standing series, sharing the field-plate grammar (1000×1000, disc
centre 500,460 r420, name baseline 934, second line 970) but with its own
dressings. Every plate carries a small vermilion seal chop at the top right,
outside the disc; that chop is a deliberate exception to the rim rule, like
the name block.

Four sub-series live under `art/`. These are the original shipped rosters,
not a per-branch queue:

- **`zodiac/` — Celestial Seals.** The twelve animals, one bust per seal,
  each on the disc of its fixed element (Wood green, Fire red, Earth ochre,
  Metal silver, Water blue). A ring of the twelve earthly branches runs
  inside the rim; the animal's branch character is stamped in the chop. The
  second line is the animal character and its current/next years.
  Shipped: rat · ox · tiger · rabbit · dragon · snake · horse · goat ·
  monkey · rooster · dog · pig.
- **`chinese-festivals/` — Festival Seals.** One emblem per festival, warm
  ink and a festival-specific palette, with the date line in the second
  line. Shipped: spring-festival · lantern-festival · dragon-boat ·
  qingming · qixi · mid-autumn. (Roster complete.)
- **`indian-festivals/` — Festival Seals.** Diya, rangoli, torana and
  marigold vocabulary; no deities in scene, no flags. Shipped: diwali ·
  holi · navratri · ganesh-chaturthi · raksha-bandhan · onam. (Roster
  complete.)
- **`indian-symbols/` — Yantra plates.** One symbol per plate on a deep
  field, gold geometry: om · mandala · lotus · peacock · kalash · rangoli.

Shared code: `work/orient/plate.py` (canvas grammar, motifs, caption/chop),
`work/orient/zodiac.py` (element palettes, branch ring, beast parts),
`work/festivals-cn/cn_kit.py`, `work/festivals-in/festival_kit.py`.
Drivers live in `work/zodiac/`, `work/festivals-cn/`, `work/festivals-in/`,
`work/symbols/` and follow the same revision rule as every other piece.

Cultural guardrails: traditional characters for the zodiac seals; festival
plates show objects and settings, not worshippers; Ganesh Chaturthi, when it
lands, is an iconic emblem, not caricature; no national flags, maps or
political symbols anywhere in the series.
