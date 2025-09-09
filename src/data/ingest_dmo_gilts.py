
from __future__ import annotations
import pathlib, sys, io
import pandas as pd
from bs4 import BeautifulSoup
import requests
from .utils import HEADERS, append_provenance

RAW = pathlib.Path("data/raw/dmo")
PROC = pathlib.Path("data/processed/dmo")

BASE = "https://www.dmo.gov.uk/data/pdfdatareport?reportCode=D1A"

def try_download_excel() -> bytes:
    for q in ["&format=excel", "&format=xlsx", ""]:
        url = BASE + q
        r = requests.get(url, headers=HEADERS, timeout=60)
        if r.ok and (r.headers.get("Content-Type","").lower().find("application/vnd") >= 0 or r.content.startswith(b"PK")):
            append_provenance(url, RAW / "gilts_in_issue.xlsx", notes="DMO Gilts in Issue – auto export")
            return r.content
    return b""

def parse_html_table(html_bytes: bytes) -> pd.DataFrame:
    soup = BeautifulSoup(html_bytes, "lxml")
    tables = pd.read_html(str(soup))
    tables.sort(key=lambda df: df.shape[0]*df.shape[1], reverse=True)
    return tables[0]

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    PROC.mkdir(parents=True, exist_ok=True)

    try:
        b = try_download_excel()
    except Exception:
        b = b""

    if not b:
        r = requests.get(BASE, headers=HEADERS, timeout=60)
        r.raise_for_status()
        df = parse_html_table(r.content)
    else:
        df = pd.read_excel(io.BytesIO(b))

    df.columns = [str(c).strip() for c in df.columns]
    raw_path = RAW / "gilts_in_issue.parquet"
    df.to_parquet(raw_path, index=False)
    (PROC / "gilts_in_issue.parquet").write_bytes(raw_path.read_bytes())
    print(f"DMO Gilts in Issue parsed: {df.shape[0]} rows. Saved to data/processed/dmo/gilts_in_issue.parquet")

if __name__ == "__main__":
    main()
