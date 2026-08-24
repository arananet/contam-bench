#!/usr/bin/env bash
# Package only arXiv source inputs; build products are intentionally excluded.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
ARCHIVE="$DIST_DIR/contam-bench-arxiv-v3.tar.gz"
REQUIRED=(main.tex references.bib main.bbl)

usage() {
  cat <<'EOF'
Usage: ./package-arxiv.sh

Creates dist/contam-bench-arxiv-v3.tar.gz from arXiv-safe manuscript inputs.
The archive is flat and intentionally excludes PDFs, TeX auxiliaries, and
local build directories.
EOF
}

case "${1:-}" in
  "") ;;
  --help|-h)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

for file in "${REQUIRED[@]}"; do
  [[ -f "$SCRIPT_DIR/$file" ]] || {
    echo "missing arXiv input: $SCRIPT_DIR/$file" >&2
    exit 1
  }
done

mkdir -p "$DIST_DIR"
rm -f "$ARCHIVE"
tar -C "$SCRIPT_DIR" -czf "$ARCHIVE" "${REQUIRED[@]}"

echo "archive: $ARCHIVE"
echo "contents:"
tar -tzf "$ARCHIVE"
