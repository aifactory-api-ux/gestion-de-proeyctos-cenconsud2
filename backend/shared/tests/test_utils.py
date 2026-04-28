import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

from shared.utils import format_currency


class TestFormatCurrency:
    def test_format_currency_positive(self):
        result = format_currency(1000.0)
        assert result == "$1,000.00"

    def test_format_currency_zero(self):
        result = format_currency(0.0)
        assert result == "$0.00"

    def test_format_currency_decimal(self):
        result = format_currency(1234.56)
        assert result == "$1,234.56"

    def test_format_currency_large(self):
        result = format_currency(1000000.0)
        assert result == "$1,000,000.00"

    def test_format_currency_small(self):
        result = format_currency(0.99)
        assert result == "$0.99"
