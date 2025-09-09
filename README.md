# UK Debt Sustainability Analysis (UK‑DSA)

**Aim:** Reproduce the latest OBR UK debt baseline and quantify debt sustainability under deterministic scenarios and Monte‑Carlo shocks—reporting debt/GDP, interest/revenue, refinancing needs, and stabilising primary balances.

## Quickstart
```bash
conda env create -f environment.yml
conda activate uk-dsa
pre-commit install
make tests      # run unit tests
make baseline   # (after data download is wired in Step 2)
make scenarios
make figs
```

## Data Sources (to be wired in Step 2)
- OBR Public Finances Databank (PFD), latest monthly release
- OBR Economic & Fiscal Outlook (EFO) tables
- ONS Public Sector Finances (monthly outturns)
- UK DMO Gilts in Issue (redemption ladder)
- Bank of England zero‑coupon nominal & real curves

All raw downloads → `data/raw/` with SHA‑256 checksums and a `DATASOURCE.md`. Transforms → `data/processed/`.

## Repository Layout
```
uk-dsa/
  src/
    data/                 # download & ingest
    model/                # debt dynamics, scenarios, Monte‑Carlo
    viz/                  # plotting
  analysis/               # exploratory notebooks (frozen via papermill)
  data/{raw,processed}/
  results/{baseline,scenarios}/
  figures/auto/
  tests/
  docs/overleaf/          # Overleaf-ready LaTeX paper
```
## Reproducibility & Style
- Python 3.11; deterministic seeds
- `pytest` for tests; `black` + `ruff` via pre‑commit
- Figures generated from code into `figures/auto/` and included in LaTeX
- No manual edits to raw data; transforms scripted and versioned

## Make targets
- `make data` – downloads & ingests sources (Step 2)
- `make baseline` – reproduce OBR baseline (Step 3)
- `make scenarios` – run deterministic scenarios (Step 5)
- `make montecarlo` – run MC engine (Step 6)
- `make figs` – regenerate figures
- `make tests` – run unit tests
- `make lint` / `make format` – static checks / formatting
```
