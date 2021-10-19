from pypfopt import black_litterman, risk_models
from pypfopt.black_litterman import BlackLittermanModel
import pandas as pd
import yfinance as yf

market_cap = {}
tickers = ["VALE3.SA", "PETR4.SA", "GGBR4.SA", "CSNA3.SA"]

for ticker in tickers:
    mktcap = yf.Ticker(ticker).info["marketCap"]
    _ticker = ticker.replace(".SA", "")
    market_cap[_ticker] = mktcap

# read data
df = pd.read_csv("../data/tickers.csv", index_col="Date")

# cov matrix
S = risk_models.sample_cov(df)

delta = black_litterman.market_implied_risk_aversion(market_prices=df)
prior_returns = pd.DataFrame(
    black_litterman.market_implied_prior_returns(market_cap, delta, S)
).transpose()

breakpoint()

view_dicts = {"VALE3": 0.10, "PETR4": 0.3, "GGBR4": -0.15, "CSNA3": 0.05}
BlackLittermanModel(cov_matrix=prior_returns, absolute_views=view_dicts)

breakpoint()

from pypfopt import EfficientFrontier, objective_functions

ef = EfficientFrontier()
ef.add_objective(objective_functions.L2_reg)

risk_models.CovarianceShrinkage().ledoit_wolf()


