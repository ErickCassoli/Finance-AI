"""Module containing the AgentCollector class for fetching market data."""

from __future__ import annotations

import requests
import yfinance as yf
from typing import Dict, Any


class AgentCollector:
    """Collects stock, options and interest rate data for analysis.

    This agent is responsible for interacting with external APIs such as
    Yahoo Finance (via ``yfinance``) for market prices and the Brazilian
    Central Bank API for the SELIC rate.
    """

    SELIC_SERIES_ID = 432  # ID da série histórica da SELIC no Bacen

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()

    def fetch_stock_price(self, ticker: str) -> float:
        """Obtain the last closing price for ``ticker``.

        Parameters
        ----------
        ticker:
            Código da ação negociada na B3 (ex: ``PETR4.SA``).

        Returns
        -------
        float
            Último preço de fechamento disponível.
        """
        data = yf.Ticker(ticker)
        hist = data.history(period="1d")
        if hist.empty:
            raise ValueError(f"No historical data returned for {ticker}")
        return float(hist["Close"].iloc[-1])

    def fetch_option_chain(self, ticker: str) -> Dict[str, Any]:
        """Retrieve option chain data for ``ticker`` using ``yfinance``.

        The result is a dictionary mapping expiration dates to dataframes
        containing calls and puts for cada vencimento.
        """
        data = yf.Ticker(ticker)
        expirations = data.options
        if not expirations:
            return {}

        chain = {}
        for exp in expirations:
            opt = data.option_chain(exp)
            chain[exp] = {
                "calls": opt.calls,
                "puts": opt.puts,
            }
        return chain

    def fetch_selic_rate(self) -> float:
        """Fetch the latest SELIC rate from the Bacen API.

        Returns the most recent daily SELIC value expressed as a percentage.
        """
        url = (
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{self.SELIC_SERIES_ID}/"
            "dados/ultimos/1?formato=json"
        )
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise RuntimeError("No SELIC data returned")
        return float(data[0]["valor"].replace(",", "."))
