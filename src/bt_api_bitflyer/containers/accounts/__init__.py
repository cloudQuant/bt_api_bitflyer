from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from bt_api_base.containers.accounts.account import AccountData
from bt_api_base.functions.utils import from_dict_get_string

if TYPE_CHECKING:
    from bt_api_base._compat import Self


class BitflyerAccountData(AccountData):
    def __init__(
        self,
        account_info: Any,
        symbol_name: str | None = None,
        has_been_json_encoded: bool = False,
    ):
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "BITFLYER"
        self.symbol_name = symbol_name
        self.account_data: dict[str, Any] | None = account_info if has_been_json_encoded else None
        self.account_id = None
        self.account_type = None
        self.can_deposit = None
        self.can_trade = None
        self.can_withdraw = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.account_data = json.loads(self.account_info)
            self.has_been_json_encoded = True

        if self.has_been_init_data:
            return self

        if isinstance(self.account_data, dict):
            self.account_id = from_dict_get_string(self.account_data, "account_id")
            self.account_type = "SPOT"
            self.can_deposit = True
            self.can_trade = True
            self.can_withdraw = True

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "account_id": self.account_id,
                "account_type": self.account_type,
                "can_deposit": self.can_deposit,
                "can_trade": self.can_trade,
                "can_withdraw": self.can_withdraw,
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

    def get_asset_type(self) -> str | None:
        return "SPOT"

    def get_local_update_time(self) -> float:
        return float(self.local_update_time)

    def get_account_id(self) -> str | None:
        return self.account_id

    def get_account_type(self) -> str | None:
        return self.account_type

    def get_can_deposit(self) -> bool | None:
        return self.can_deposit

    def get_can_trade(self) -> bool | None:
        return self.can_trade

    def get_can_withdraw(self) -> bool | None:
        return self.can_withdraw
