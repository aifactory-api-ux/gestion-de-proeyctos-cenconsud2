from datetime import datetime
from typing import Optional

from shared.models import Budget


MOCK_BUDGETS = {
    1: Budget(
        id=1,
        project_id=1,
        allocated_amount=100000.0,
        spent_amount=45000.0,
        forecasted_amount=95000.0,
        last_updated=datetime(2024, 3, 15, 10, 30, 0)
    ),
    2: Budget(
        id=2,
        project_id=2,
        allocated_amount=75000.0,
        spent_amount=30000.0,
        forecasted_amount=72000.0,
        last_updated=datetime(2024, 3, 14, 14, 20, 0)
    ),
    3: Budget(
        id=3,
        project_id=3,
        allocated_amount=200000.0,
        spent_amount=50000.0,
        forecasted_amount=185000.0,
        last_updated=datetime(2024, 3, 13, 9, 0, 0)
    ),
}


def get_budget_by_project_id(project_id: int) -> Optional[Budget]:
    return MOCK_BUDGETS.get(project_id)