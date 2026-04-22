from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

from bt_api_base.containers.orders.order import OrderData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string

if TYPE_CHECKING:
    from bt_api_base._compat import Self


class BitflyerOrderData(OrderData):
    def __init__(
        self,
        order_info: Any,
        symbol_name: str | None = None,
        has_been_json_encoded: bool = False,
    ):
        super().__init__(order_info, has_been_json_encoded)
        self.exchange_name = "BITFLYER"
        self.symbol_name = symbol_name
        self.order_data: dict[str, Any] | None = order_info if has_been_json_encoded else None
        self.order_id: str | None = None
        self.client_order_id: str | None = None
        self.order_type: str | None = None
        self.side: str | None = None
        self.price: float | None = None
        self.volume: float | None = None
        self.filled_volume: float | None = None
        self.average_price: float | None = None
        self.status: str | None = None
        self.created_at: int | None = None
        self.updated_at: int | None = None
        self.all_data: dict[str, Any] | None = None
        self.local_update_time = time.time()
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.order_data = json.loads(self.order_info)
            self.has_been_json_encoded = True

        if self.has_been_init_data:
            return self

        if isinstance(self.order_data, dict):
            self.order_id = from_dict_get_string(self.order_data, "child_order_acceptance_id")
            self.client_order_id = from_dict_get_string(self.order_data, "child_order_id")
            self.order_type = from_dict_get_string(self.order_data, "child_order_type")
            self.side = from_dict_get_string(self.order_data, "side")
            self.price = from_dict_get_float(self.order_data, "price")
            self.volume = from_dict_get_float(self.order_data, "size")
            self.filled_volume = from_dict_get_float(self.order_data, "executed_size")
            self.average_price = from_dict_get_float(self.order_data, "average_price")
            self.status = from_dict_get_string(self.order_data, "child_order_state")

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "order_id": self.order_id,
                "client_order_id": self.client_order_id,
                "order_type": self.order_type,
                "side": self.side,
                "price": self.price,
                "volume": self.volume,
                "filled_volume": self.filled_volume,
                "average_price": self.average_price,
                "status": self.status,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
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

    def get_order_id(self) -> str | None:
        return self.order_id

    def get_order_type(self) -> str | None:
        return self.order_type

    def get_side(self) -> str | None:
        return self.side

    def get_price(self) -> float | None:
        return self.price

    def get_volume(self) -> float | None:
        return self.volume

    def get_filled_volume(self) -> float | None:
        return self.filled_volume

    def get_average_price(self) -> float | None:
        return self.average_price

    def get_status(self) -> str | None:
        return self.status

    def is_order_type(self) -> bool:
        return self.order_type in ("LIMIT", "MARKET")

    def is_side(self) -> bool:
        return self.side in ("BUY", "SELL")
