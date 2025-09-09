
from __future__ import annotations
import pathlib, sys
import pandas as pd
import requests
from .utils import HEADERS, append_provenance
from bs4 import BeautifulSoup

RAW = pathlib.Path("data/raw/boe")
PROC = pathlib.Path("data/processed/boe")

BOE_DB_ROOT = "https://www.bankofengland.co.uk/boeapps/database"
YIELD_CURVES_LANDING = BOE_DB_ROOT + "/?search=yield%20curves"
DMO_AGG_YIELDS = "https://www.dmo.gov.uk/data/ExportReport?reportCode=D4H"

def try_boe_preview() -> pd.DataFrame | None:
    r = requests.get(YIELD_CURVES_LANDING, headers=HEADERS, timeout=60)
    r.raise_for_status()
    tables = pd.read_html(r.text)
    if tables:
        df = pd.concat([t for t in tables if t.shape[1] >= 2], axis=0, ignore_index=True)
        if df.shape[0] >= 5:
            return df
    return None

def dmo_fallback_monthly_benchmarks(start_month: int = 1, start_year: int = 2020) -> pd.DataFrame:
    params = {"StartMonth": start_month, "StartYear": start_year}
    r = requests.get(DMO_AGG_YIELDS, headers=HEADERS, params=params, timeout=60)
    r.raise_for_status()
    tables = pd.read_html(r.text)
    tables.sort(key=lambda df: df.shape[0]*df.shape[1], reverse=True)
    return tables[0]

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    PROC.mkdir(parents=True, exist_ok=True)

    df = None
    try:
        df = try_boe_preview()
        if df is not None:
            raw = RAW / "boe_yield_curves_preview.parquet"
            df.to_parquet(raw, index=False)
            (PROC / "boe_yield_curves_preview.parquet").write_bytes(raw.read_bytes())
            append_provenance(YIELD_CURVES_LANDING, raw, notes="BoE IADB – yield curves (preview scrape)")
            print(f"BoE yields (preview) saved with {df.shape[0]} rows.")
    except Exception as e:
        print("BoE scrape failed:", e)

    if df is None:
        try:
            dmdf = dmo_fallback_monthly_benchmarks()
            raw = RAW / "dmo_aggregated_yields.parquet"
            dmdf.to_parquet(raw, index=False)
            (PROC / "dmo_aggregated_yields.parquet").write_bytes(raw.read_bytes())
            append_provenance(DMO_AGG_YIELDS, raw, notes="DMO aggregated conventional gilt yields (monthly)")
            print(f"DMO aggregated yields saved with {dmdf.shape[0]} rows.")
        except Exception as e:
            print("DMO fallback failed:", e)
            sys.exit(3)

if __name__ == "__main__":
    main()
