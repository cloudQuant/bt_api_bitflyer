from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BitflyerExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITFLYER"
        self.rest_url = "https://api.bitflyer.com"
        self.wss_url = "wss://ws.lightstream.bitflyer.com/json-rpc"
        self.kline_periods = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "4h": "4h",
            "1d": "1d",
            "1w": "1w",
        }
        self.legal_currency = ["JPY", "USD", "EUR", "BTC"]
        self.rest_paths = {}
        self.wss_paths = {}


class BitflyerExchangeDataSpot(BitflyerExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.api_key = None
        self.api_secret = None
