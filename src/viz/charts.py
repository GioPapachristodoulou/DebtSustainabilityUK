"""Generate figures (placeholder uses synthetic path until baselines wired)."""
from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def main():
    f = Path("results/baseline/debt_path_demo.csv")
    if not f.exists():
        print("No demo path found. Run: make baseline")
        return
    y = np.loadtxt(f, delimiter=",")
    plt.figure()
    plt.plot(range(len(y)), 100*y)
    plt.xlabel("Year")
    plt.ylabel("Debt / GDP (%)")
    plt.title("Demo debt path (synthetic; Step 3 will be OBR baseline)")
    Path("figures/auto").mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig("figures/auto/demo_debt_path.png", dpi=200)
    print("Saved figures/auto/demo_debt_path.png")

if __name__ == "__main__":
    main()
