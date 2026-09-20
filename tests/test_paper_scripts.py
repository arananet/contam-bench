"""Archive-level paper checks for the arXiv submission surface."""

import shutil
import subprocess
import tarfile
from pathlib import Path

import pytest

PAPER_DIR = Path("paper/v3")


def test_arxiv_check_compiles_the_packaged_sources():
    if not any(shutil.which(command) for command in ("tectonic", "latexmk", "pdflatex")):
        pytest.skip("requires a local TeX compiler")

    completed = subprocess.run(
        ["bash", "check-arxiv.sh"], cwd=PAPER_DIR, check=True,
        text=True, capture_output=True,
    )

    assert "arXiv package check passed" in completed.stdout
    with tarfile.open(PAPER_DIR / "dist/contam-bench-arxiv-v3.tar.gz") as archive:
        assert archive.getnames() == ["main.tex", "references.bib", "main.bbl"]
