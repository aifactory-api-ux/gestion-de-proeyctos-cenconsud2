import pytest
import sys
import os
from datetime import datetime
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

import service
from shared.models import ForecastRequest


class TestAggregateForecast:
    @pytest.mark.asyncio
    async def test_aggregate_forecast_mock_project_1(self):
        request = ForecastRequest(project_id=1)
        result = await service.aggregate_forecast(request, "test-token")
        assert result.project_id == 1
        assert result.forecasted_cost == 98000.0
        assert result.confidence == 0.85

    @pytest.mark.asyncio
    async def test_aggregate_forecast_mock_project_2(self):
        request = ForecastRequest(project_id=2)
        result = await service.aggregate_forecast(request, "test-token")
        assert result.project_id == 2
        assert result.forecasted_cost == 73000.0
        assert result.confidence == 0.88

    @pytest.mark.asyncio
    async def test_aggregate_forecast_mock_project_3(self):
        request = ForecastRequest(project_id=3)
        result = await service.aggregate_forecast(request, "test-token")
        assert result.project_id == 3
        assert result.forecasted_cost == 190000.0
        assert result.confidence == 0.79

    @pytest.mark.asyncio
    async def test_aggregate_forecast_unknown_project(self):
        request = ForecastRequest(project_id=999)
        result = await service.aggregate_forecast(request, "test-token")
        assert result.project_id == 999
        assert result.forecasted_cost == 75000.0
        assert result.confidence == 0.75


class TestMockForecasts:
    def test_mock_forecasts_defined(self):
        assert len(service.MOCK_FORECASTS) == 3
        assert 1 in service.MOCK_FORECASTS
        assert 2 in service.MOCK_FORECASTS
        assert 3 in service.MOCK_FORECASTS

    def test_mock_forecast_1_properties(self):
        forecast = service.MOCK_FORECASTS[1]
        assert forecast.project_id == 1
        assert forecast.forecasted_cost == 98000.0
        assert forecast.confidence == 0.85
        assert isinstance(forecast.generated_at, datetime)

    def test_mock_forecast_2_properties(self):
        forecast = service.MOCK_FORECASTS[2]
        assert forecast.project_id == 2
        assert forecast.forecasted_cost == 73000.0
        assert forecast.confidence == 0.88

    def test_mock_forecast_3_properties(self):
        forecast = service.MOCK_FORECASTS[3]
        assert forecast.project_id == 3
        assert forecast.forecasted_cost == 190000.0
        assert forecast.confidence == 0.79
