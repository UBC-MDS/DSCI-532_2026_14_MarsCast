# Adapted from Lecture 7 

import duckdb
from pathlib import Path

BASE = Path(__file__).parent.parent  # Go up one level from src/

CSV = BASE / "data/raw/mars-weather.csv"
OUT = BASE / "data/processed/mars-weather.parquet"


duckdb.execute(f"""
    COPY (SELECT * FROM read_csv_auto('{CSV}'))
    TO '{OUT}' (FORMAT PARQUET)
""")