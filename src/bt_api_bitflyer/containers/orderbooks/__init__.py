from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.functions.utils import from_dict_get_list

if TYPE_CHECKING:
    from bt_api_base._compat import Self


class BitflyerOrderBookData(OrderBookData):
    def __init__(
        self,
        orderbook_info: Any,
        symbol_name: str | None = None,
        has_been_json_encoded: bool = False,
    ):
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BITFLYER"
        self.symbol_name = symbol_name
        self.orderbook_data: dict[str, Any] | None = (
            orderbook_info if has_been_json_encoded else None
        )
        self.bids: list[list[float]] = []
        self.asks: list[list[float]] = []
        self.timestamp: int | None = None
        self.all_data: dict[str, Any] | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.orderbook_data = json.loads(self.orderbook_info)
            self.has_been_json_encoded = True

        if self.has_been_init_data:
            return self

        if isinstance(self.orderbook_data, dict):
            bids_raw = from_dict_get_list(self.orderbook_data, "bids")
            asks_raw = from_dict_get_list(self.orderbook_data, "asks")
            self.bids = [[float(x[0]), float(x[1])] for x in bids_raw] if bids_raw else []
            self.asks = [[float(x[0]), float(x[1])] for x in asks_raw] if asks_raw else []

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "bids": self.bids,
                "asks": self.asks,
                "timestamp": self.timestamp,
                "local_update_time": self.local_update_time,
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str | None:
        return self.symbol_name

    def get_bids(self) -> list[list[float]]:
        self.init_data()
        return self.bids

    def get_asks(self) -> list[list[float]]:
        self.init_data()
        return self.asks

    def get_best_bid(self) -> float | None:
        self.init_data()
        return self.bids[0][0] if self.bids else None

    def get_best_ask(self) -> float | None:
        self.init_data()
        return self.asks[0][0] if self.asks else None
