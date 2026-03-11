import numpy as np
from src.logic import compare

def test_compare_no_data_when_baseline_missing():
    """Verifies compare returns a safe 'no data' badge when baseline is missing, preventing misleading KPI deltas."""
    out = compare(10.0, None)
    assert out["badge"] == "no data"
    assert out["icon"] == "circle-minus"
