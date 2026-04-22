from __future__ import annotations

from typing import TYPE_CHECKING

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_bitflyer import __version__
from bt_api_bitflyer.registry_registration import register_bitflyer

if TYPE_CHECKING:
    from bt_api_base.gateway.registrar import GatewayRuntimeRegistrar
    from bt_api_base.registry import ExchangeRegistry


def register_plugin(
    registry: type[ExchangeRegistry], runtime_factory: type[GatewayRuntimeRegistrar]
) -> PluginInfo:
    register_bitflyer(registry)

    return PluginInfo(
        name="bt_api_bitflyer",
        version=__version__,
        core_requires=">=0.15,<1.0",
        supported_exchanges=("BITFLYER___SPOT",),
        supported_asset_types=("SPOT",),
    )
