from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bt_api_base.balance_utils import nested_balance_handler as _bitflyer_balance_handler

from bt_api_bitflyer.exchange_data import BitflyerExchangeDataSpot
from bt_api_bitflyer.feeds.live_bitflyer.spot import BitflyerRequestDataSpot

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def _bitflyer_spot_subscribe_handler(
    data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any
) -> None:
    topic_list = [i["topic"] for i in topics]
    bt_api.log(f"bitFlyer Spot topics requested: {topic_list}")


def register_bitflyer(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("BITFLYER___SPOT", BitflyerRequestDataSpot)
    registry.register_exchange_data("BITFLYER___SPOT", BitflyerExchangeDataSpot)
    registry.register_balance_handler("BITFLYER___SPOT", _bitflyer_balance_handler)
    registry.register_stream("BITFLYER___SPOT", "subscribe", _bitflyer_spot_subscribe_handler)
