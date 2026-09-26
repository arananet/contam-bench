"""Regression checks for the frozen unresolved-verdict sensitivity table."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/generate_unresolved_sensitivity_table.py"
OUTPUT = ROOT / "paper/v3/generated-unresolved-sensitivity-table.tex"


def test_unresolved_sensitivity_table_is_reproducible():
    expected = OUTPUT.read_text()

    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True)

    actual = OUTPUT.read_text()
    assert actual == expected
    assert "8/30; 14/30" in actual
    assert "0/5; 5/5" in actual
    assert "10/10; 10/10" in actual
