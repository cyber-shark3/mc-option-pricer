# Monte Carlo Option Pricer

A Python quantitative-finance project implementing Monte Carlo option pricing with Geometric Brownian Motion (GBM) and antithetic variates.

## Features

- GBM asset-price path simulation
- Antithetic variates for variance reduction
- European call and put Monte Carlo pricing
- Black-Scholes closed-form benchmarks
- Monte Carlo standard-error reporting
- American put pricing using Longstaff-Schwartz regression
- GBM path visualisation

## Project structure

mc-option-pricer/
├── requirements.txt
├── monte_carlo.py
├── main.py
└── README.md

## Installation

Python 3.10+ is recommended.

    python -m pip install -r requirements.txt

## Run

    python main.py

The default run uses 100,000 paths for the European options and American put.

## Mathematical model

GBM:

    dS_t = r S_t dt + sigma S_t dW_t

Exact discretisation:

    S(t+dt) = S(t) * exp((r - 0.5*sigma^2)dt + sigma*sqrt(dt)*Z)

where Z is standard normal.

For a European option, the Monte Carlo estimator is:

    Price = exp(-rT) * mean(Payoff)

## Default parameters

- Spot price: 100
- Strike price: 100
- Risk-free rate: 5%
- Volatility: 20%
- Maturity: 1 year
- European paths: 100,000
- American put paths: 100,000

## Validation

The European Monte Carlo results are compared directly with Black-Scholes values. Increasing the number of simulations should reduce Monte Carlo sampling error.

The American put implementation is an educational Longstaff-Schwartz implementation and should be validated with convergence tests and independent benchmark values before production use.

## Disclaimer

This project is for educational and research purposes. It does not model transaction costs, liquidity, jumps, stochastic volatility, dividends, or real-world execution, and it is not investment advice.
