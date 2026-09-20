#!/usr/bin/env bash
# Verify the exact source archive arXiv receives can compile from its root.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ARCHIVE="$SCRIPT_DIR/dist/contam-bench-arxiv-v3.tar.gz"
WORK_DIR=""
EXPECTED_FILES=$'main.tex\nreferences.bib\nmain.bbl'

usage() {
  cat <<'EOF'
Usage: ./check-arxiv.sh

Packages the manuscript, verifies the flat arXiv input set, extracts it into a
temporary directory, compiles main.tex there, and rejects undefined citations
or references in the TeX log.
EOF
}

cleanup() {
  [[ -n "$WORK_DIR" ]] && rm -rf "$WORK_DIR"
}
trap cleanup EXIT

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

"$SCRIPT_DIR/package-arxiv.sh"

ARCHIVE_FILES="$(tar -tzf "$ARCHIVE")"
if [[ "$ARCHIVE_FILES" != "$EXPECTED_FILES" ]]; then
  echo "unexpected arXiv archive contents:" >&2
  printf '%s\n' "$ARCHIVE_FILES" >&2
  exit 1
fi

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/contam-bench-arxiv.XXXXXX")"
tar -xzf "$ARCHIVE" -C "$WORK_DIR"
mkdir -p "$WORK_DIR/build"

if command -v tectonic >/dev/null 2>&1; then
  (
    cd "$WORK_DIR"
    tectonic --outdir build --keep-logs main.tex
  )
elif command -v latexmk >/dev/null 2>&1; then
  (
    cd "$WORK_DIR"
    latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
  )
elif command -v pdflatex >/dev/null 2>&1; then
  (
    cd "$WORK_DIR"
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
  )
else
  echo "TeX is required: install tectonic (preferred), latexmk, or pdflatex, then rerun." >&2
  exit 127
fi

PDF="$WORK_DIR/build/main.pdf"
LOG="$WORK_DIR/build/main.log"
[[ -f "$PDF" ]] || { echo "expected PDF was not produced: $PDF" >&2; exit 1; }
[[ -f "$LOG" ]] || { echo "expected TeX log was not produced: $LOG" >&2; exit 1; }

if grep -Eq 'Citation .* undefined|Reference .* undefined|There were undefined references' "$LOG"; then
  echo "undefined citations or references in arXiv package log:" >&2
  grep -E 'Citation .* undefined|Reference .* undefined|There were undefined references' "$LOG" >&2
  exit 1
fi

echo "arXiv package check passed"
