from __future__ import annotations

from typing import Any

from bt_api_base.feeds.capability import Capability

from bt_api_bitflyer.feeds.live_bitflyer.request_base import BitflyerRequestData


class BitflyerRequestDataSpot(BitflyerRequestData):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.exchange_name = kwargs.get("exchange_name", "BITFLYER___SPOT")

    def _normalize_product_code(self, symbol: str) -> str:
        symbol = symbol.upper().replace("/", "_").replace("-", "_")
        return symbol

    def _get_tick(
        self, symbol: str, extra_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        product_code = self._normalize_product_code(symbol)
        path = "GET /v1/ticker"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_tick",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_tick_normalize_function,
            }
        )
        params = {"product_code": product_code}
        return path, params, extra_data

    @staticmethod
    def _get_tick_normalize_function(
        input_data: dict[str, Any], extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        if isinstance(input_data, dict) and "product_code" in input_data:
            return [input_data], True
        return [], False

    def get_tick(self, symbol: str, extra_data: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_tick(
        self, symbol: str, extra_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> None:
        path, params, extra_data = self._get_tick(symbol, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        product_code = self._normalize_product_code(symbol)
        path = "GET /v1/board"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_depth",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_depth_normalize_function,
            }
        )
        params = {"product_code": product_code}
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(
        input_data: dict[str, Any], extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        if isinstance(input_data, dict) and "bids" in input_data:
            return [input_data], True
        return [], False

    def get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_depth(
        self,
        symbol: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        path, params, extra_data = self._get_depth(symbol, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        product_code = self._normalize_product_code(symbol)
        path = "GET /v1/executions"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_kline",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "period": period,
                "normalize_function": self._get_kline_normalize_function,
            }
        )
        params = {"product_code": product_code, "count": count}
        return path, params, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        if isinstance(input_data, list):
            return [input_data], True
        elif isinstance(input_data, dict) and isinstance(input_data.get("data"), list):
            return [input_data["data"]], True
        return [], False

    def get_kline(
        self,
        symbol: str,
        period: str,
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def async_get_kline(
        self,
        symbol: str,
        period: str = "1m",
        count: int = 20,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        path, params, extra_data = self._get_kline(symbol, period, count, extra_data, **kwargs)
        self.submit(
            self.async_request(path, params=params, extra_data=extra_data),
            callback=self.async_callback,
        )

    def _get_trades(
        self,
        symbol: str,
        limit: int = 100,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        product_code = self._normalize_product_code(symbol)
        path = "GET /v1/executions"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_trades",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_trades_normalize_function,
            }
        )
        params = {"product_code": product_code, "count": limit}
        return path, params, extra_data

    @staticmethod
    def _get_trades_normalize_function(input_data: Any, extra_data: Any) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        if isinstance(input_data, list):
            return [input_data], True
        elif isinstance(input_data, dict) and isinstance(input_data.get("data"), list):
            return [input_data["data"]], True
        return [], False

    def get_trades(
        self,
        symbol: str,
        limit: int = 100,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_trades(symbol, limit, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_exchange_info(
        self, extra_data: dict[str, Any] | None = None, **kwargs: Any
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /v1/getmarkets"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_exchange_info",
                "symbol_name": "",
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_exchange_info_normalize_function,
            }
        )
        return path, None, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(
        input_data: Any, extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        if isinstance(input_data, list):
            return [input_data], True
        return [], False

    def get_exchange_info(self, extra_data: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        path, params, extra_data = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_health(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /v1/gethealth"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "request_type": "get_health",
                "normalize_function": self._get_health_normalize_function,
            }
        )
        params: dict[str, Any] = {}
        if symbol:
            product_code = self._normalize_product_code(symbol)
            params["product_code"] = product_code
        return path, params, extra_data

    @staticmethod
    def _get_health_normalize_function(
        input_data: dict[str, Any], extra_data: Any
    ) -> tuple[list[Any], bool]:
        if not input_data:
            return [], False
        if isinstance(input_data, dict) and "status" in input_data:
            return [input_data], True
        return [], False

    def get_health(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_health(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _make_order(
        self,
        symbol: str,
        volume: Any,
        price: Any,
        order_type: str,
        offset: str = "open",
        post_only: bool = False,
        client_order_id: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        product_code = self._normalize_product_code(symbol)
        path = "POST /v1/me/sendchildorder"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "make_order",
            }
        )
        params = {
            "product_code": product_code,
            "child_order_type": order_type.upper(),
            "side": offset.upper() if offset in ("BUY", "SELL", "buy", "sell") else "BUY",
            "size": float(volume),
            "price": float(price) if order_type.upper() == "LIMIT" else 0,
        }
        return path, params, extra_data

    def make_order(
        self,
        symbol: str,
        volume: Any,
        price: Any,
        order_type: str,
        offset: str = "open",
        post_only: bool = False,
        client_order_id: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._make_order(
            symbol,
            volume,
            price,
            order_type,
            offset,
            post_only,
            client_order_id,
            extra_data,
            **kwargs,
        )
        return self.request(path, body=params, extra_data=extra_data)

    def _cancel_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        product_code = self._normalize_product_code(symbol)
        path = "POST /v1/me/cancelchildorder"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "cancel_order",
                "order_id": order_id,
            }
        )
        params = {"product_code": product_code, "child_order_acceptance_id": order_id}
        return path, params, extra_data

    def cancel_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._cancel_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, body=params, extra_data=extra_data)

    def _query_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        product_code = self._normalize_product_code(symbol)
        path = "GET /v1/me/getchildorders"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "request_type": "query_order",
                "order_id": order_id,
            }
        )
        params = {"product_code": product_code, "child_order_acceptance_id": order_id}
        return path, params, extra_data

    def query_order(
        self,
        symbol: str,
        order_id: str | int,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._query_order(symbol, order_id, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_open_orders(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /v1/me/getchildorders"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_open_orders",
            }
        )
        params = {"child_order_state": "ACTIVE"}
        if symbol:
            product_code = self._normalize_product_code(symbol)
            params["product_code"] = product_code
        return path, params, extra_data

    def get_open_orders(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_open_orders(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_account(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /v1/me/getpermissions"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_account",
            }
        )
        return path, None, extra_data

    def get_account(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_account(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)

    def _get_balance(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> tuple[str, dict[str, Any] | None, dict[str, Any]]:
        path = "GET /v1/me/getbalance"
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": symbol or "",
                "asset_type": self.asset_type,
                "request_type": "get_balance",
            }
        )
        return path, None, extra_data

    def get_balance(
        self,
        symbol: str | None = None,
        extra_data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        path, params, extra_data = self._get_balance(symbol, extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)
