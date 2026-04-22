"""Tests for BitflyerExchangeData container."""

from __future__ import annotations

from bt_api_bitflyer.exchange_data import BitflyerExchangeData


class TestBitflyerExchangeData:
    """Tests for BitflyerExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = BitflyerExchangeData()

        assert exchange.exchange_name == "BITFLYER"
        assert "bitflyer.com" in exchange.rest_url
