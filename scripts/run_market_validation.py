"""
Market validation runner for mc-option-pricer.

Runs the European Monte Carlo engine against representative spot inputs for:
- Brent crude oil
- Gold
- FirstRand Namibia (NSX: FNB)

Spot observations are recorded in run metadata. Volatility values are explicit
test assumptions, not implied-volatility estimates.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from monte_carlo import black_scholes_call, black_scholes_put, price_european_mc

RUN_DATE = "2026-09-18"
OUT = Path("data/test_runs") / RUN_DATE
SEED = 20260918
PATHS = 10_000
STEPS = 252
RISK_FREE_RATE = 0.05
MATURITY = 1.0

ASSETS = [
    {"asset":"Brent Crude Oil","symbol":"BZ=F","spot":104.61,"currency":"USD","sigma":0.35,"source":"Reuters, 2026-09-11"},
    {"asset":"Gold Spot","symbol":"XAUUSD","spot":4363.01,"currency":"USD/oz","sigma":0.20,"source":"Reuters, 2026-09-11"},
    {"asset":"FirstRand Namibia","symbol":"FNB (NSX)","spot":56.09,"currency":"NAD/share","sigma":0.18,"source":"Investing.com, 2026-09-16"},
]

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    np.random.seed(SEED)
    results = []
    for asset in ASSETS:
        S0 = K = asset["spot"]
        call, call_se, call_paths = price_european_mc(S0,K,RISK_FREE_RATE,asset["sigma"],MATURITY,"call",M=PATHS,N=STEPS)
        put, put_se, put_paths = price_european_mc(S0,K,RISK_FREE_RATE,asset["sigma"],MATURITY,"put",M=PATHS,N=STEPS)
        for option, mc, se, bs in [
            ("call", call, call_se, black_scholes_call(S0,K,RISK_FREE_RATE,asset["sigma"],MATURITY)),
            ("put", put, put_se, black_scholes_put(S0,K,RISK_FREE_RATE,asset["sigma"],MATURITY)),
        ]:
            results.append({**asset,"option":option,"strike":K,"risk_free_rate":RISK_FREE_RATE,"maturity_years":MATURITY,
                            "paths":PATHS,"steps":STEPS,"mc_price":mc,"std_error":se,"bs_price":bs,
                            "abs_error":abs(mc-bs),"within_3se":abs(mc-bs)<=3*se})
        safe=asset["asset"].lower().replace(" ","_").replace("-","_")
        pd.DataFrame({"path":np.arange(PATHS),"terminal_price":call_paths[-1]}).to_csv(
            OUT/f"{safe}_terminal_prices.csv",index=False,float_format="%.6f")
    pd.DataFrame(results).to_csv(OUT/"market_test_results.csv",index=False,float_format="%.8f")
    metadata={"run_id":f"{RUN_DATE}-market-validation-001","generated_at_utc":datetime.now(timezone.utc).isoformat(),
              "seed":SEED,"paths_per_asset":PATHS,"steps":STEPS,"risk_free_rate":RISK_FREE_RATE,"maturity_years":MATURITY,
              "method":"GBM Monte Carlo with antithetic variates",
              "validation":"European MC prices checked against Black-Scholes; all rows must be within 3 standard errors.",
              "assets":ASSETS,
              "notes":["Spot inputs are recorded market observations.","Volatility inputs are explicit test assumptions, not implied-volatility estimates.",
                       "This is a model validation run, not a trading signal or investment recommendation."]}
    (OUT/"metadata.json").write_text(json.dumps(metadata,indent=2),encoding="utf-8")
    print(pd.DataFrame(results).to_string(index=False))

if __name__=="__main__":
    main()
