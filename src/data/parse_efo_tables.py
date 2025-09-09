
from __future__ import annotations
import pathlib, sys
from .utils import http_get, append_provenance, excel_to_parquet_per_sheet

EFO_XLSX = "https://obr.uk/docs/dlm_uploads/Executive_summary_charts_and_tables_March_2025.xlsx"
RAW = pathlib.Path("data/raw/obr")
PROC = pathlib.Path("data/processed/obr")

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    PROC.mkdir(parents=True, exist_ok=True)

    raw_path = RAW / "efo_march_2025_exec_summary.xlsx"
    try:
        http_get(EFO_XLSX, raw_path)
        append_provenance(EFO_XLSX, raw_path, notes="OBR EFO March 2025 – Exec summary charts/tables")
    except Exception as e:
        print("Download failed (network?):", e)
        sys.exit(3)

    out_dir = PROC / "efo_march_2025"
    paths = excel_to_parquet_per_sheet(raw_path, out_dir)
    print(f"EFO workbook saved to {raw_path}. Parsed {len(paths)} sheets into {out_dir}")

if __name__ == "__main__":
    main()
