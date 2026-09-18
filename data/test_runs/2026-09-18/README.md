# Market Validation Run — 2026-09-18

The Monte Carlo option pricer was exercised against three market reference assets: Brent crude oil, gold, and FirstRand Namibia (NSX: FNB).

## Configuration

- 10,000 simulated paths per asset
- 252 time steps
- 1-year maturity
- 5% risk-free rate
- Antithetic variates enabled
- Fixed random seed: 20260918
- At-the-money strike: K = S0
- European call and put
- Black-Scholes used as the reference value

## Result

All six European Monte Carlo prices landed within 3 Monte Carlo standard errors of the corresponding Black-Scholes reference value.

## Data captured

- `metadata.json` — complete run configuration and source notes
- `market_test_results.csv` — pricing results and validation checks
- The reproducible runner lives at `scripts/run_market_validation.py`

The raw simulation matrix is intentionally not committed as millions of CSV cells. The repository records the complete configuration, deterministic seed, pricing outputs, errors, and validation flags so the run can be reproduced exactly.

## Market inputs

Brent crude was recorded at $104.61/bbl and gold at $4,363.01/oz in the cited 11 September 2026 Reuters reports. FirstRand Namibia was recorded at N$56.09/share in the cited 16 September 2026 historical market data.

The volatility values (35% oil, 20% gold, 18% FNB) are explicit model-test assumptions, not claims about historical or implied volatility.

This is a model validation run, not a trading signal or investment recommendation.
