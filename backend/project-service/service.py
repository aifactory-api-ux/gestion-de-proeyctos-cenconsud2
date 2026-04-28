from datetime import date
from typing import List, Optional

from shared.models import Project


MOCK_PROJECTS = [
    Project(
        id=1,
        name="Project Alpha",
        description="First project",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31),
        manager_id=1,
        status="active"
    ),
    Project(
        id=2,
        name="Project Beta",
        description="Second project",
        start_date=date(2024, 3, 1),
        end_date=date(2024, 9, 30),
        manager_id=2,
        status="active"
    ),
    Project(
        id=3,
        name="Project Gamma",
        description="Third project",
        start_date=date(2024, 6, 1),
        end_date=date(2025, 3, 31),
        manager_id=1,
        status="planning"
    ),
]


def list_projects() -> List[Project]:
    return MOCK_PROJECTS


def get_project_by_id(project_id: int) -> Optional[Project]:
    for project in MOCK_PROJECTS:
        if project.id == project_id:
            return project
    return None