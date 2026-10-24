## Farmhouse table V1R00 — stroked ears need awns, and low tables can hang a drying bunch

- Kind: lesson
- Source: issue #1218, `work/furniture/draw_farmhouse_table.py`,
  `art/furniture/farmhouse-table/farmhouse-table-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: field plates — furniture (harvest/prop vocabulary, thin geometry)
- Status: pending

### Evidence

First pass had grain heads drawn as one thick stroked tip per stem (7.5pt
round cap): at plate scale they read as cattails, not wheat. Slimming the
ear to ~4.4pt and adding three pairs of short whisker awns along it
(1.5pt, opacity ~65) restored the cereal read — the broken silhouette is
what sells the species. A single thick stroke is a sausage, whatever the
colour. The same fix applied to the loose stalks lying on the top.

The piece is low and wide, so the upper disc went to a drying sheaf hung
on a cord that fades to opacity 0 well clear of the rim — same trick as
the billiard table's pendant lamp, but a harvest fixture instead of a
light. Draw-order catch: the long H-stretcher bar at z=0 is *behind* the
near legs, so it must be drawn before them or it floats over the front
leg faces.

### Proposed change

Furniture note candidate: "Grain and grass props: draw the ear as a slim
stroke plus whisker awns, never one fat tip. For low wide subjects the
upper-disc fixture can be functional, not just a lamp — a hung sheaf,
drying herbs, a rail — hung on a support faded before the rim." Pending
until consolidated.
