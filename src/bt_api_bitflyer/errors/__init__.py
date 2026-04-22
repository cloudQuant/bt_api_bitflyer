from __future__ import annotations

from bt_api_base.error import ErrorCategory, ErrorTranslator, UnifiedError, UnifiedErrorCode


class BitflyerErrorTranslator(ErrorTranslator):
    ERROR_MAP = {
        "INVALID_API_KEY": (UnifiedErrorCode.INVALID_API_KEY, "Invalid API key"),
        "AUTHENTICATION_FAILED": (UnifiedErrorCode.INVALID_SIGNATURE, "Authentication failed"),
        "INVALID_SIGNATURE": (UnifiedErrorCode.INVALID_SIGNATURE, "Invalid signature"),
        "INSUFFICIENT_BALANCE": (UnifiedErrorCode.INSUFFICIENT_BALANCE, "Insufficient balance"),
        "INVALID_ORDER_SIZE": (UnifiedErrorCode.INVALID_VOLUME, "Invalid order size"),
        "INVALID_ORDER_PRICE": (UnifiedErrorCode.INVALID_PRICE, "Invalid order price"),
        "ORDER_NOT_FOUND": (UnifiedErrorCode.ORDER_NOT_FOUND, "Order not found"),
        "ORDER_ALREADY_FILLED": (UnifiedErrorCode.ORDER_ALREADY_FILLED, "Order already filled"),
        "ORDER_ALREADY_CANCELLED": (
            UnifiedErrorCode.ORDER_ALREADY_FILLED,
            "Order already cancelled",
        ),
        "MARKET_CLOSED": (UnifiedErrorCode.MARKET_CLOSED, "Market is closed"),
        "RATE_LIMIT_EXCEEDED": (UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Rate limit exceeded"),
        "SERVICE_UNAVAILABLE": (UnifiedErrorCode.EXCHANGE_OVERLOADED, "Service unavailable"),
        "MAINTENANCE": (UnifiedErrorCode.EXCHANGE_MAINTENANCE, "System under maintenance"),
    }

    @classmethod
    def translate(cls, raw_error, venue: str = "BITFLYER"):
        if isinstance(raw_error, str):
            return cls.translate_string_error(raw_error, venue)
        elif isinstance(raw_error, dict):
            return cls.translate_dict_error(raw_error, venue)
        return cls._translate_fallback(raw_error, venue)

    @classmethod
    def translate_string_error(cls, error_msg: str, venue: str):
        error_lower = error_msg.lower()

        if "invalid api key" in error_lower or "auth" in error_lower:
            return cls._create_unified_error(
                UnifiedErrorCode.INVALID_API_KEY, "Invalid API key", venue, error_msg
            )
        elif "signature" in error_lower:
            return cls._create_unified_error(
                UnifiedErrorCode.INVALID_SIGNATURE, "Invalid signature", venue, error_msg
            )
        elif "rate limit" in error_lower or "too many requests" in error_lower:
            return cls._create_unified_error(
                UnifiedErrorCode.RATE_LIMIT_EXCEEDED, "Rate limit exceeded", venue, error_msg
            )
        elif "insufficient balance" in error_lower:
            return cls._create_unified_error(
                UnifiedErrorCode.INSUFFICIENT_BALANCE, "Insufficient balance", venue, error_msg
            )
        elif "order not found" in error_lower:
            return cls._create_unified_error(
                UnifiedErrorCode.ORDER_NOT_FOUND, "Order not found", venue, error_msg
            )
        elif "maintenance" in error_lower:
            return cls._create_unified_error(
                UnifiedErrorCode.EXCHANGE_MAINTENANCE, "System under maintenance", venue, error_msg
            )
        elif "internal error" in error_lower:
            return cls._create_unified_error(
                UnifiedErrorCode.INTERNAL_ERROR, "Internal error", venue, error_msg
            )

        return cls._create_unified_error(
            UnifiedErrorCode.INTERNAL_ERROR, error_msg, venue, error_msg
        )

    @classmethod
    def translate_dict_error(cls, error_dict: dict, venue: str):
        label = error_dict.get("label", "")
        message = error_dict.get("message", "")

        if not label:
            if message:
                return cls.translate_string_error(message, venue)
            return cls._translate_fallback(error_dict, venue)

        if label in cls.ERROR_MAP:
            unified_code, default_msg = cls.ERROR_MAP[label]
            return cls._create_unified_error(
                unified_code, message or default_msg, venue, f"{label}: {message}"
            )

        return cls.translate_string_error(f"{label}: {message}", venue)

    @classmethod
    def _create_unified_error(cls, code, message, venue, original_error):
        if code in [
            UnifiedErrorCode.INVALID_API_KEY,
            UnifiedErrorCode.INVALID_SIGNATURE,
            UnifiedErrorCode.SESSION_EXPIRED,
        ]:
            category = ErrorCategory.AUTH
        elif code in [
            UnifiedErrorCode.INVALID_SYMBOL,
            UnifiedErrorCode.INVALID_PRICE,
            UnifiedErrorCode.INVALID_VOLUME,
            UnifiedErrorCode.ORDER_NOT_FOUND,
            UnifiedErrorCode.ORDER_ERROR,
            UnifiedErrorCode.ORDER_CANCEL_FAILED,
            UnifiedErrorCode.MARKET_CLOSED,
        ]:
            category = ErrorCategory.ORDER
        elif code == UnifiedErrorCode.RATE_LIMIT_EXCEEDED:
            category = ErrorCategory.RATE_LIMIT
        elif code in [
            UnifiedErrorCode.INTERNAL_ERROR,
            UnifiedErrorCode.EXCHANGE_MAINTENANCE,
            UnifiedErrorCode.EXCHANGE_OVERLOADED,
        ]:
            category = ErrorCategory.SYSTEM
        else:
            category = ErrorCategory.BUSINESS

        return UnifiedError(
            code=code,
            category=category,
            venue=venue,
            message=message,
            original_error=original_error,
            context={"raw_response": original_error},
        )

    @classmethod
    def _translate_fallback(cls, raw_error, venue: str):
        return cls._create_unified_error(
            UnifiedErrorCode.INTERNAL_ERROR, "Unknown error", venue, str(raw_error)
        )
