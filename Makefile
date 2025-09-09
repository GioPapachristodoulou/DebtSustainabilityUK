.PHONY: help setup data baseline scenarios montecarlo figs tests lint format

help:
	@echo "Targets: setup, data, baseline, scenarios, montecarlo, figs, tests, lint, format"

setup:
	pre-commit install

data:
	python -m src.data.download_obr_pfd
	python -m src.data.parse_efo_tables
	python -m src.data.ingest_ons_psf
	python -m src.data.ingest_dmo_gilts
	python -m src.data.ingest_boe_yields

baseline:
	python -m src.model.debt_dynamics --baseline

scenarios:
	python -m src.model.scenarios

montecarlo:
	python -m src.model.monte_carlo

figs:
	python -m src.viz.charts

tests:
	pytest -q

lint:
	ruff check .

format:
	black .
