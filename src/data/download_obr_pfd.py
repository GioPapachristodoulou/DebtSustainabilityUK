
from __future__ import annotations
import pathlib, re, sys
import pandas as pd
from .utils import soup, http_get, append_provenance, excel_to_parquet_per_sheet

PFD_INDEX_URL = "https://obr.uk/public-finances-databank-2025-26/"
RAW = pathlib.Path("data/raw/obr")
PROC = pathlib.Path("data/processed/obr")

def find_latest_pfd_xlsx(url: str) -> tuple[str, str]:
    # Return (download_url, label) for the most recent PFD xlsx on the page.
    s = soup(url)
    links = [(a.get("href",""), a.get_text(strip=True)) for a in s.find_all("a")]
    xlsxs = [(href, text) for href, text in links if href.endswith(".xlsx") and "Public finances databank" in text]
    if not xlsxs:
        xlsxs = [(href, text) for href, text in links if href.endswith(".xlsx")]
    href, text = xlsxs[0]
    return href, text

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    PROC.mkdir(parents=True, exist_ok=True)

    try:
        xlsx_url, label = find_latest_pfd_xlsx(PFD_INDEX_URL)
    except Exception as e:
        print("Could not discover latest PFD xlsx:", e)
        sys.exit(2)

    tag = re.sub(r"[^A-Za-z0-9]+", "_", label).strip("_").lower()
    raw_path = RAW / f"{tag}.xlsx"
    try:
        http_get(xlsx_url, raw_path)
        append_provenance(xlsx_url, raw_path, notes=f"OBR PFD: {label}")
    except Exception as e:
        print("Download failed (network?):", e)
        sys.exit(3)

    out_dir = PROC / f"pfd_{tag}"
    paths = excel_to_parquet_per_sheet(raw_path, out_dir)
    print(f"PFD downloaded to {raw_path}. Parsed {len(paths)} sheets into {out_dir}")

if __name__ == "__main__":
    main()
