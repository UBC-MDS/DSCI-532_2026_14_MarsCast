import numpy as np
from src.logic import compare

def test_compare_no_data_when_baseline_missing():
    """Verifies compare returns a safe 'no data' badge when baseline is missing, preventing misleading KPI deltas."""
    out = compare(10.0, None)
    assert out["badge"] == "no data"
    assert out["icon"] == "circle-minus"

def test_compare_positive_change_formats_badge_and_icon():
    """Verifies compare produces an upward icon and signed badge when current exceeds baseline, ensuring KPI trend meaning is stable."""
    out = compare(110.0, 100.0)
    assert out["icon"] == "arrow-trend-up"
    assert "vs last year" in out["badge"]
    assert "+" in out["badge"]


def test_compare_zero_change_uses_minus_icon():
    """Verifies compare uses a neutral icon when there is no change, avoiding false trend signals."""
    out = compare(100.0, 100.0)
    assert out["icon"] == "minus"