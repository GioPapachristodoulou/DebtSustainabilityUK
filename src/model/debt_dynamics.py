"""Debt dynamics core routines and baseline (deterministic).

Implements both nominal and (r-g) formulations.

d_{t+1} = ((1 + i_t)/(1 + g_t)) * d_t - s_{t+1}   (exact nominal ratio law)
Approximate: Δd ≈ (i_t - g_t) d_t - s_{t+1}
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import argparse

@dataclass
class State:
    debt_ratio: float  # d_t
    primary_balance: float  # s_{t+1} as % of GDP (+ surplus)
    nominal_rate: float  # i_t
    nominal_gdp_growth: float  # g_t

def next_debt_ratio_exact(d: float, i: float, g: float, s: float) -> float:
    return ((1.0 + i) / (1.0 + g)) * d - s

def next_debt_ratio_rg(d: float, r_minus_g: float, s: float) -> float:
    return (1.0 + r_minus_g) * d - s

def stabilising_primary(d: float, i: float, g: float) -> float:
    """Primary balance that keeps debt ratio constant next period."""
    return ((1.0 + i) / (1.0 + g) - 1.0) * d

def simulate_path(d0: float, i: float, g: float, s: float, T: int = 5, exact=True):
    d = d0
    out = [d0]
    for _ in range(T):
        if exact:
            d = next_debt_ratio_exact(d, i, g, s)
        else:
            d = next_debt_ratio_rg(d, i - g, s)
        out.append(d)
    return np.array(out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", action="store_true", help="Run a synthetic baseline demo")
    args = parser.parse_args()
    if args.baseline:
        # Synthetic demo (until Step 3 wires real OBR data)
        d0, i, g, s = 0.97, 0.045, 0.035, 0.005  # 97% debt/GDP; 4.5% rate; 3.5% nom g; 0.5% PB
        path = simulate_path(d0, i, g, s, T=5, exact=True)
        np.savetxt("results/baseline/debt_path_demo.csv", path, delimiter=",", fmt="%.5f")
        print("Baseline demo path written to results/baseline/debt_path_demo.csv")
    else:
        print("Run with --baseline for a synthetic demo. Real baseline arrives in Step 3.")

if __name__ == "__main__":
    main()
