"""Run Monte Carlo option pricing examples and plot simulated paths."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from monte_carlo import (
    price_european_mc,
    price_american_put_mc,
    black_scholes_call,
    black_scholes_put,
)


def main():
    np.random.seed(42)

    S0 = 100.0
    K = 100.0
    r = 0.05
    sigma = 0.20
    T = 1.0

    print("=== Monte Carlo Option Pricer ===\n")

    print("Calculating European Call...")
    mc_call, call_err, call_paths = price_european_mc(
        S0, K, r, sigma, T, "call", M=100_000, N=252
    )
    bs_call = black_scholes_call(S0, K, r, sigma, T)

    print("Calculating European Put...")
    mc_put, put_err, _ = price_european_mc(
        S0, K, r, sigma, T, "put", M=100_000, N=252
    )
    bs_put = black_scholes_put(S0, K, r, sigma, T)

    print("Calculating American Put (Longstaff-Schwartz)...")
    am_put, _ = price_american_put_mc(
        S0, K, r, sigma, T, M=100_000, N=50
    )

    print("\n--- Pricing Results ---")
    print(f"European Call: MC = ${mc_call:.4f} (±{call_err:.4f}) | BS = ${bs_call:.4f}")
    print(f"European Put:  MC = ${mc_put:.4f} (±{put_err:.4f}) | BS = ${bs_put:.4f}")
    print(f"American Put:  MC = ${am_put:.4f} (No closed-form BS available)")
    print("Note: American Put > European Put due to early exercise premium.\n")

    plot_sample_paths(call_paths, K, T)


def plot_sample_paths(paths, K, T):
    """Plot a sample of simulated GBM paths."""
    plt.figure(figsize=(10, 6))
    time_grid = np.linspace(0, T, paths.shape[0])

    num_paths_to_plot = min(50, paths.shape[1])
    for i in range(num_paths_to_plot):
        plt.plot(time_grid, paths[:, i], lw=1, alpha=0.5)

    plt.title(f"Simulated Geometric Brownian Motion ({num_paths_to_plot} Paths)")
    plt.xlabel("Time (Years)")
    plt.ylabel("Asset Price")
    plt.axhline(K, linestyle="--", lw=2, label=f"Strike Price ({K})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
