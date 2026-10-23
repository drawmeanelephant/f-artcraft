#!/bin/sh
# Renders the site with dogbed: docs/src/*.knap + docs/data/*.json
# -> docs/site/*.html. The data and the docs/site/media/ images come from
# docs/gen_data.py — run that first. Requires a dogbed binary
# (DOGBED env or ./dogbed / zig-out/bin/dogbed).
#
# Each page renders to a uniquely named temp file and is renamed over its
# destination only on success: a failed rebuild never clobbers the last
# good page.
set -eu
cd "$(dirname "$0")/.."
if [ -z "${DOGBED:-}" ]; then
    for c in ./dogbed zig-out/bin/dogbed; do
        [ -x "$c" ] && DOGBED="$c" && break
    done
fi
: "${DOGBED:?no dogbed binary — set DOGBED or drop one at ./dogbed}"

tmp=""
cleanup() {
    if [ -n "$tmp" ]; then rm -f "$tmp"; fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

for page in index plates machines pieces guest about; do
    case "$page" in
        index)    t="f-artcraft — the gallery" ; tpl="index" ;;
        plates)   t="f-artcraft — field plates" ; tpl="gallery" ;;
        machines) t="f-artcraft — machines & furniture" ; tpl="gallery" ;;
        pieces)   t="f-artcraft — the named pieces" ; tpl="gallery" ;;
        guest)    t="f-artcraft — guest work" ; tpl="gallery" ;;
        about)    t="f-artcraft — about" ; tpl="about" ;;
    esac
    tmp="docs/site/.$page.html.$$"
    if "$DOGBED" render "docs/src/$tpl.knap" \
        -d "docs/data/$page.json" \
        --title "$t" --css style.css --lang en \
        --head '<meta property="og:title" content="f-artcraft">' \
        --head '<meta property="og:description" content="vector art drawn live in VectorCraft">' \
        > "$tmp"
    then
        mv -f "$tmp" "docs/site/$page.html"
        tmp=""
    else
        status=$?
        rm -f "$tmp"
        tmp=""
        echo "dogbed: render failed for $page (exit $status), leaving docs/site/$page.html untouched" >&2
        exit "$status"
    fi
done
echo "rendered: index plates machines pieces guest about"
