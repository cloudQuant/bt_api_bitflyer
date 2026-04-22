from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from bt_api_base.containers.bars.bar import BarData
from bt_api_base.functions.utils import from_dict_get_float

if TYPE_CHECKING:
    from bt_api_base._compat import Self


class BitflyerBarData(BarData):
    def __init__(
        self,
        bar_info: Any,
        symbol_name: str | None = None,
        period: str | None = None,
        has_been_json_encoded: bool = False,
    ):
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "BITFLYER"
        self.symbol_name = symbol_name
        self.period = period
        self.bar_data: dict[str, Any] | None = bar_info if has_been_json_encoded else None
        self.open_time: int | None = None
        self.open_price: float | None = None
        self.high_price: float | None = None
        self.low_price: float | None = None
        self.close_price: float | None = None
        self.volume: float | None = None
        self.quote_volume: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.bar_data = json.loads(self.bar_info)
            self.has_been_json_encoded = True

        if self.has_been_init_data:
            return self

        if isinstance(self.bar_data, dict):
            self.open_time = int(from_dict_get_float(self.bar_data, "id") or 0) * 1000
            self.open_price = from_dict_get_float(self.bar_data, "open")
            self.high_price = from_dict_get_float(self.bar_data, "high")
            self.low_price = from_dict_get_float(self.bar_data, "low")
            self.close_price = from_dict_get_float(self.bar_data, "close")
            self.volume = from_dict_get_float(self.bar_data, "volume")
            self.quote_volume = from_dict_get_float(self.bar_data, "quote_volume")

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "period": self.period,
                "open_time": self.open_time,
                "open_price": self.open_price,
                "high_price": self.high_price,
                "low_price": self.low_price,
                "close_price": self.close_price,
                "volume": self.volume,
                "quote_volume": self.quote_volume,
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

    def get_period(self) -> str | None:
        return self.period

    def get_open_time(self) -> int | None:
        return self.open_time

    def get_open_price(self) -> float | None:
        return self.open_price

    def get_high_price(self) -> float | None:
        return self.high_price

    def get_low_price(self) -> float | None:
        return self.low_price

    def get_close_price(self) -> float | None:
        return self.close_price

    def get_volume(self) -> float | None:
        return self.volume
