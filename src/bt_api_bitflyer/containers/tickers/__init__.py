from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float

if TYPE_CHECKING:
    from bt_api_base._compat import Self


class BitflyerRequestTickerData(TickerData):
    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "BITFLYER"
        self.local_update_time = time.time()
        self.ticker_data: dict[str, Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, dict) else None
        )
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.volume_24h: float | None = None
        self.volume_quote_24h: float | None = None
        self.bid_size: float | None = None
        self.ask_size: float | None = None
        self.total_bid_depth: float | None = None
        self.total_ask_depth: float | None = None
        self.timestamp: int | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.ticker_data, dict):
            data = self.ticker_data
            if "product_code" in data:
                self.ticker_symbol_name = data.get("product_code")
                self.last_price = from_dict_get_float(data, "ltp")
                self.bid_price = from_dict_get_float(data, "best_bid")
                self.ask_price = from_dict_get_float(data, "best_ask")
                self.volume_24h = from_dict_get_float(data, "volume")
                self.volume_quote_24h = from_dict_get_float(data, "volume_by_product")
                self.bid_size = from_dict_get_float(data, "best_bid_size")
                self.ask_size = from_dict_get_float(data, "best_ask_size")
                self.total_bid_depth = from_dict_get_float(data, "total_bid_depth")
                self.total_ask_depth = from_dict_get_float(data, "total_ask_depth")

                timestamp_str = data.get("timestamp")
                if timestamp_str:
                    self.timestamp = self._parse_timestamp(timestamp_str)

        self.has_been_init_data = True
        return self

    @staticmethod
    def _parse_timestamp(timestamp_str: str) -> int | None:
        if not timestamp_str:
            return None
        try:
            from datetime import datetime

            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            return int(dt.timestamp() * 1000)
        except (ValueError, TypeError):
            return None

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_last_price(self) -> float | None:
        self.init_data()
        return self.last_price

    def get_bid_price(self) -> float | None:
        self.init_data()
        return self.bid_price

    def get_ask_price(self) -> float | None:
        self.init_data()
        return self.ask_price
