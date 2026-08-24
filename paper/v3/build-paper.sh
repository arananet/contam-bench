#!/usr/bin/env bash
# Build the v3 manuscript locally. Generated files stay under build/.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
MAIN_TEX="$SCRIPT_DIR/main.tex"
BUILD_DIR="$SCRIPT_DIR/build"
PDF="$BUILD_DIR/contam-bench-paper-v3.pdf"

usage() {
  cat <<'EOF'
Usage: ./build-paper.sh [--clean]

Builds main.tex into build/contam-bench-paper-v3.pdf.
Prefers Tectonic, then latexmk, then pdflatex. Requires a local TeX engine.
EOF
}

case "${1:-}" in
  "") ;;
  --clean)
    rm -rf "$BUILD_DIR"
    echo "removed $BUILD_DIR"
    exit 0
    ;;
  --help|-h)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

[[ -f "$MAIN_TEX" ]] || { echo "missing manuscript: $MAIN_TEX" >&2; exit 1; }
mkdir -p "$BUILD_DIR"

if command -v tectonic >/dev/null 2>&1; then
  tectonic --outdir "$BUILD_DIR" --keep-logs "$MAIN_TEX"
elif command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -outdir="$BUILD_DIR" "$MAIN_TEX"
elif command -v pdflatex >/dev/null 2>&1; then
  (
    cd "$BUILD_DIR"
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory="$BUILD_DIR" "$MAIN_TEX"
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory="$BUILD_DIR" "$MAIN_TEX"
  )
else
  echo "TeX is required: install tectonic (preferred), latexmk, or pdflatex, then rerun." >&2
  exit 127
fi

if [[ -f "$BUILD_DIR/main.pdf" ]]; then
  mv "$BUILD_DIR/main.pdf" "$PDF"
fi
[[ -f "$PDF" ]] || { echo "expected PDF was not produced: $PDF" >&2; exit 1; }
echo "paper: $PDF"
