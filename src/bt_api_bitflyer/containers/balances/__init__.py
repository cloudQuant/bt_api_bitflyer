from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string

if TYPE_CHECKING:
    from bt_api_base._compat import Self


class BitflyerBalanceData(BalanceData):
    def __init__(
        self, balance_info: Any, asset_type: str = "SPOT", has_been_json_encoded: bool = False
    ):
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "BITFLYER"
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.currency = None
        self.available = None
        self.locked = None
        self.all_data = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.balance_data = json.loads(self.balance_info)
            self.has_been_json_encoded = True

        if self.has_been_init_data:
            return self

        if isinstance(self.balance_data, dict):
            self.currency = from_dict_get_string(self.balance_data, "currency")
            self.available = from_dict_get_float(self.balance_data, "available")
            self.locked = from_dict_get_float(self.balance_data, "locked")
        elif isinstance(self.balance_data, list):
            if len(self.balance_data) >= 2:
                self.currency = self.balance_data[0]
                self.available = float(self.balance_data[1]) if self.balance_data[1] else None
                self.locked = 0.0

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "currency": self.currency,
                "available": self.available,
                "locked": self.locked,
                "total": (self.available or 0.0) + (self.locked or 0.0),
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_local_update_time(self) -> float:
        return float(self.local_update_time)

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_currency(self) -> str | None:
        return self.currency

    def get_available(self) -> float | None:
        return self.available

    def get_locked(self) -> float | None:
        return self.locked

    def get_total(self) -> float:
        if self.available and self.locked:
            return self.available + self.locked
        return 0.0

    def is_zero_balance(self) -> bool:
        return not (self.available and self.available > 0) and not (self.locked and self.locked > 0)


class BitflyerRequestBalanceData(BitflyerBalanceData):
    pass


class BitflyerWssBalanceData(BitflyerBalanceData):
    pass
