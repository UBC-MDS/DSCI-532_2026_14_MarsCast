# src/logic.py

import pandas as pd

def compare(current, baseline):
    """Compare current vs baseline and return dict(icon, badge)."""
    if baseline is None or baseline == 0 or pd.isna(current) or pd.isna(baseline):
        return dict(icon="circle-minus", badge="no data")

    pct = (current - baseline) / abs(baseline) * 100
    sign = "+" if pct >= 0 else ""
    diff = current - baseline
    badge = f"{sign}{diff:.1f} ({sign}{pct:.1f}%) vs last year"

    if diff > 0:
        icon = "arrow-trend-up"
    elif diff < 0:
        icon = "arrow-trend-down"
    else:
        icon = "minus"

    return dict(icon=icon, badge=badge)