"""
Monte Carlo option pricing core.
"""

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def generate_gbm_paths(S0, r, sigma, T, M, N, antithetic=True):
    """Simulates Geometric Brownian Motion (GBM) paths."""
    dt = T / N

    if antithetic:
        half_M = M // 2
        Z = np.random.standard_normal((N, half_M))
        Z = np.concatenate([Z, -Z], axis=1)
        if M % 2:
            Z = np.concatenate([Z, np.random.standard_normal((N, 1))], axis=1)
        Z = Z[:, :M]
    else:
        Z = np.random.standard_normal((N, M))

    S = np.zeros((N + 1, M))
    S[0] = S0

    for t in range(1, N + 1):
        S[t] = S[t - 1] * np.exp(
            (r - 0.5 * sigma**2) * dt
            + sigma * np.sqrt(dt) * Z[t - 1]
        )

    return S


def black_scholes_call(S, K, r, sigma, T):
    """Closed-form Black-Scholes call price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def black_scholes_put(S, K, r, sigma, T):
    """Closed-form Black-Scholes put price."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def price_european_mc(S0, K, r, sigma, T, option_type, M=50_000, N=252):
    """Price a European option via Monte Carlo simulation."""
    S = generate_gbm_paths(S0, r, sigma, T, M, N, antithetic=True)

    if option_type.lower() == "call":
        payoffs = np.maximum(S[-1] - K, 0)
    elif option_type.lower() == "put":
        payoffs = np.maximum(K - S[-1], 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    discount = np.exp(-r * T)
    price = discount * np.mean(payoffs)
    std_err = discount * np.std(payoffs) / np.sqrt(M)

    return price, std_err, S


def price_american_put_mc(S0, K, r, sigma, T, M=50_000, N=50):
    """Price an American put using the Longstaff-Schwartz Method (LSM)."""
    S = generate_gbm_paths(S0, r, sigma, T, M, N, antithetic=True)
    dt = T / N
    V = np.maximum(K - S[-1], 0)

    for t in range(N - 1, 0, -1):
        exercise = np.maximum(K - S[t], 0)
        itm = exercise > 0

        if np.any(itm):
            Y = np.exp(-r * dt) * V[itm]
            X = S[t, itm]
            coeffs = np.polyfit(X, Y, 2)
            continuation = np.polyval(coeffs, X)
            hold = continuation > exercise[itm]
            V[itm] = np.where(hold, Y, exercise[itm])

        V[~itm] = np.exp(-r * dt) * V[~itm]

    price = np.mean(V) * np.exp(-r * dt)
    return price, S
