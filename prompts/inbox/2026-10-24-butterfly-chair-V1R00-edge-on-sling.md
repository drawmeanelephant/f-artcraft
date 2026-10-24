## Butterfly chair V1R00 — a drape along the view axis renders paper-thin

- Kind: lesson
- Source: issue #1182, `work/furniture/draw_butterfly_chair.py`, `art/furniture/butterfly-chair/butterfly-chair-V1R00.*`
- Applies to: field plates — furniture (slung/fabric surfaces)
- Status: pending

### Evidence

The leather cover was parametrised u=back→front with z marching forward
linearly. Under yaw+pitch projection a surface that falls *forward and
down* at roughly the pitch angle stays near-parallel to the view axis, so
a 17-inch-deep sling drew as a ~120pt ribbon — the chair read as a
hammock, not a seat. Two fixes did the work: drive z with u**2.6 so the
bowl hangs back and the drop is mostly vertical in screen space, and
lighten the pocket (the seat faces up into the light, not away from it) —
a radial catch-light where the bowl bottoms out. Real BKF anatomy: the
four corners are the only supports; every free edge catenary-sags between
them and the front ears splay wider than the back pair.

### Proposed change

For `prompts/series/` furniture notes: when a surface recedes along the
sight line, push its far points back (nonlinear z, or raise pitch) until
its screen height is legible — linear drape + linear z = edge-on cloth.
Light the inside of a seat pocket as sky-facing, not as a shadow.
