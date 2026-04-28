import pytest
import sys
import os
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

sys.modules['shared.db'] = MagicMock()
sys.modules['shared.db'].get_redis_client = MagicMock(return_value=MagicMock())

import service


class TestGetBudgetByProjectId:
    def test_get_existing_budget(self):
        budget = service.get_budget_by_project_id(1)
        assert budget is not None
        assert budget.project_id == 1
        assert budget.allocated_amount == 100000.0
        assert budget.spent_amount == 45000.0
        assert budget.forecasted_amount == 95000.0

    def test_get_budget_project_2(self):
        budget = service.get_budget_by_project_id(2)
        assert budget is not None
        assert budget.project_id == 2
        assert budget.allocated_amount == 75000.0
        assert budget.spent_amount == 30000.0

    def test_get_budget_project_3(self):
        budget = service.get_budget_by_project_id(3)
        assert budget is not None
        assert budget.project_id == 3
        assert budget.allocated_amount == 200000.0
        assert budget.spent_amount == 50000.0

    def test_get_non_existing_budget(self):
        budget = service.get_budget_by_project_id(999)
        assert budget is None


class TestMockBudgets:
    def test_mock_budgets_defined(self):
        assert len(service.MOCK_BUDGETS) == 3
        assert 1 in service.MOCK_BUDGETS
        assert 2 in service.MOCK_BUDGETS
        assert 3 in service.MOCK_BUDGETS

    def test_budget_calculations(self):
        budget = service.MOCK_BUDGETS[1]
        assert budget.allocated_amount > budget.spent_amount
        assert budget.forecasted_amount < budget.allocated_amount
