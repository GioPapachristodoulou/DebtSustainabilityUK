
from __future__ import annotations
import pathlib, sys
from .utils import soup, http_get, append_provenance, excel_to_parquet_per_sheet

ONS_DATASET_URL = "https://www.ons.gov.uk/economy/governmentpublicsectorandtaxes/publicsectorfinance/datasets/publicsectorfinancesappendixatables110"
RAW = pathlib.Path("data/raw/ons")
PROC = pathlib.Path("data/processed/ons")

def find_current_xlsx(url: str) -> str:
    s = soup(url)
    for a in s.find_all("a"):
        href = a.get("href","")
        if href.endswith(".xlsx"):
            if href.startswith("/"):
                return "https://www.ons.gov.uk" + href
            return href
    raise RuntimeError("No .xlsx link found on ONS dataset page.")

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    PROC.mkdir(parents=True, exist_ok=True)

    try:
        xlsx_url = find_current_xlsx(ONS_DATASET_URL)
    except Exception as e:
        print("Discovery failed:", e)
        sys.exit(2)

    raw_path = RAW / "psa_tables_current.xlsx"
    try:
        http_get(xlsx_url, raw_path)
        append_provenance(xlsx_url, raw_path, notes="ONS PSF – PSA tables 1–10")
    except Exception as e:
        print("Download failed (network?):", e)
        sys.exit(3)

    out_dir = PROC / "psa"
    paths = excel_to_parquet_per_sheet(raw_path, out_dir)
    print(f"ONS PSA saved to {raw_path}. Parsed {len(paths)} sheets into {out_dir}")

if __name__ == "__main__":
    main()
